using AuthServer.Data;
using AuthServer.Services;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.Tokens;
using System.Security.Claims;

namespace AuthServer.Controllers
{
    [Microsoft.AspNetCore.Mvc.Route("api/connect")]
    [ApiController]
    public class AuthorizesController : ControllerBase
    {
        private readonly UserManager<ApplicationUser> userManager;
        private readonly SignInManager<ApplicationUser> signInManager;
        private readonly ApplicationDbContext _dbContext;
        private readonly ITokenService tokenService;
        private readonly IPkceService pkceService;
        private readonly JwtOptions _jwtConfig;

        public AuthorizesController(
            UserManager<ApplicationUser> userManager,
            SignInManager<ApplicationUser> signInManager,
            ApplicationDbContext db,
            ITokenService ts,
            IPkceService pkceService,
            IOptions<JwtOptions> jwtOptions)
        {
            this.userManager = userManager;
            this.signInManager = signInManager;
            this._dbContext = db;
            this.tokenService = ts;
            this.pkceService = pkceService;
            this._jwtConfig = jwtOptions.Value;
        }

        [HttpGet("authorize")]
        public async Task<IActionResult> Authorize([FromQuery] string client_id,
                                                   [FromQuery] string redirect_uri,
                                                   [FromQuery] string response_type,
                                                   [FromQuery] string code_challenge,
                                                   [FromQuery] string code_challenge_method,
                                                   [FromQuery] string username,
                                                   [FromQuery] string password,
                                                   [FromQuery] string scope,
                                                   [FromQuery] string? state)
        {
            // basic validation
            if (response_type != "code")
                return BadRequest(new { error = "unsupported_response_type" });

            var client = await _dbContext.Clients.FirstOrDefaultAsync(c => c.ClientId == client_id);
            if (client == null) return BadRequest(new { error = "invalid_client" });

            // check redirect uri permitted
            if (!string.IsNullOrEmpty(redirect_uri))
            {
                var allowed = client.RedirectUris?.Split(new[] { '\n', '\r', ' ', ';' }, StringSplitOptions.RemoveEmptyEntries) ?? new string[] { };
                if (!allowed.Contains(redirect_uri))
                    return BadRequest(new { error = "invalid_redirect_uri" });
            }

            // authenticate user with username/password
            var user = await userManager.FindByNameAsync(username);
            if (user == null) return Unauthorized(new { error = "invalid_grant" });

            var signInResult = await signInManager.PasswordSignInAsync(username, password, isPersistent: false, lockoutOnFailure: false);
            if (!signInResult.Succeeded) return Unauthorized(new { error = "invalid_grant" });

            // create auth code (store hash)
            var codePlain = Guid.NewGuid().ToString("N");
            var codeHash = tokenService.HashToken(codePlain);

            if (string.IsNullOrEmpty(code_challenge))
            {
                return BadRequest(new { error = "PKCe is required code challenge" });
            }

            if (string.IsNullOrEmpty(code_challenge_method))
            {
                return BadRequest(new { error = "PKCe is required code challenge method" });
            }

            if (!code_challenge_method.ToUpper().Equals("S256"))
            {
                return BadRequest(new { error = $"server not support code_challenge_method={code_challenge_method}" });
            }

            var codeChallengeS256Hash = pkceService.ComputeCodeChallengeS256(code_challenge);
            var auth = new AuthCode
            {
                CodeHash = codeHash,
                ClientId = client_id,
                RedirectUri = redirect_uri ?? string.Empty,
                SubjectId = user.Id,
                Expires = DateTime.UtcNow.AddSeconds(30),
                CodeChallenge = codeChallengeS256Hash,
                CodeChallengeMethod = code_challenge_method.ToUpper(),
                Scopes = scope ?? "openid profile api"
            };
            _dbContext.AuthCodes.Add(auth);
            await _dbContext.SaveChangesAsync();

            // Return code in JSON (since no UI). Client should then call token endpoint.
            return Ok(new
            {
                code = codePlain,
                state = state
            });
        }

        [HttpPost("token")]
        public async Task<IActionResult> Token([FromForm] string grant_type)
        {
            if (grant_type == "authorization_code")
            {
                var code = Request.Form["code"].FirstOrDefault();
                var redirectUri = Request.Form["redirect_uri"].FirstOrDefault() ?? string.Empty;
                var clientId = Request.Form["client_id"].FirstOrDefault();
                var codeVerifier = Request.Form["code_verifier"].FirstOrDefault();

                if (string.IsNullOrEmpty(code) || string.IsNullOrEmpty(clientId))
                    return BadRequest(new { error = "invalid_request" });

                // verify PKCE
                var client = await _dbContext.Clients.FirstOrDefaultAsync(p => p.ClientId == clientId);
                if (client == null) return BadRequest(new { error = "invalid_client" });

                var hash = tokenService.HashToken(code);

                var authCode = await _dbContext.AuthCodes.FirstOrDefaultAsync(c => c.CodeHash == hash && !c.Consumed);
                if (authCode == null || authCode.Expires < DateTime.UtcNow || authCode.ClientId != clientId || authCode.RedirectUri != redirectUri)
                    return BadRequest(new { error = "invalid_grant" });

                if (client.RequirePkce && !string.IsNullOrEmpty(authCode.CodeChallenge))
                {
                    if (string.IsNullOrEmpty(codeVerifier))
                        return BadRequest(new { error = "invalid_request", error_description = "missing code_verifier" });

                    string computed;

                    if (authCode.CodeChallengeMethod?.ToUpper() == "S256")
                    {
                        computed = codeVerifier;
                    }
                    else
                    {
                        throw new NotSupportedException($"server not support code_challenge_method={authCode.CodeChallengeMethod?.ToUpper()}");
                    }

                    if (computed != authCode.CodeChallenge)
                        return BadRequest(new { error = "invalid_grant", error_description = "PKCE verification failed" });
                }

                // Mark code consumed
                authCode.Consumed = true;
                await _dbContext.SaveChangesAsync();

                // create tokens
                var user = await userManager.FindByIdAsync(authCode.SubjectId);

                if (user == null) return BadRequest(new { error = "invalid_grant", error_description = "User not found" });

                var scopes = authCode.Scopes?.Split(' ', StringSplitOptions.RemoveEmptyEntries) ?? Array.Empty<string>();

                var access = tokenService.CreateAccessToken(user, scopes?.Select(p => new Claim("scope", p)));
                var id = tokenService.CreateIdToken(user);
                var (refreshPlain, refreshHash) = tokenService.GenerateRefreshToken();

                var r = new RefreshToken
                {
                    HashedToken = refreshHash,
                    ClientId = clientId,
                    Scopes = !scopes.IsNullOrEmpty() ? string.Join(" ", scopes ?? Array.Empty<string>()) : string.Empty,
                    SubjectId = user.Id,
                    Created = DateTime.UtcNow,
                    Expires = DateTime.UtcNow.AddSeconds(_jwtConfig.RefreshTokenExpiries)
                };
                _dbContext.RefreshTokens.Add(r);
                await _dbContext.SaveChangesAsync();

                return Ok(new
                {
                    access_token = access,
                    token_type = "Bearer",
                    access_token_expires = (int)TimeSpan.FromSeconds(_jwtConfig.AccessTokenExpiries).TotalSeconds,
                    refresh_token = refreshPlain,
                    refresh_token_expires = (int)TimeSpan.FromSeconds(_jwtConfig.RefreshTokenExpiries).TotalSeconds
                });
            }
            else if (grant_type == "refresh_token")
            {
                var clientId = Request.Form["client_id"].FirstOrDefault();
                var refreshToken = Request.Form["refresh_token"].FirstOrDefault();

                if (string.IsNullOrEmpty(refreshToken) || string.IsNullOrEmpty(clientId))
                    return BadRequest(new { error = "invalid_request" });

                var client = await _dbContext.Clients.FirstOrDefaultAsync(c => c.ClientId == clientId);
                if (client == null) return BadRequest(new { error = "invalid_client" });

                var hashed = tokenService.HashToken(refreshToken);
                var stored = await _dbContext.RefreshTokens.FirstOrDefaultAsync(t => t.HashedToken == hashed && !t.Revoked && t.ClientId == client.ClientId);
                if (stored == null || stored.Expires < DateTime.UtcNow) return BadRequest(new { error = "invalid_grant" });

                // rotate: revoke old
                stored.Revoked = true;

                var user = await userManager.FindByIdAsync(stored.SubjectId);
                if (user == null) return BadRequest(new { error = "invalid_grant", error_description = "User not found" });

                var scopes = stored.Scopes?.Split(' ', StringSplitOptions.RemoveEmptyEntries) ?? Array.Empty<string>();

                var newAccess = tokenService.CreateAccessToken(user, scopes?.Select(p => new Claim("scope", p)));
                var newId = tokenService.CreateIdToken(user);
                var (newRefresh, newRefreshHash) = tokenService.GenerateRefreshToken();

                var newStored = new RefreshToken
                {
                    HashedToken = newRefreshHash,
                    ClientId = client.ClientId,
                    Scopes = !scopes.IsNullOrEmpty() ? string.Join(" ", scopes ?? Array.Empty<string>()) : string.Empty,
                    SubjectId = user.Id,
                    Created = DateTime.UtcNow,
                    Expires = DateTime.UtcNow.AddSeconds(_jwtConfig.AccessTokenExpiries),
                    Revoked = false
                };
                _dbContext.RefreshTokens.Add(newStored);
                await _dbContext.SaveChangesAsync();

                var resp2 = new
                {
                    access_token = newAccess,
                    token_type = "Bearer",
                    access_token_expires = (int)TimeSpan.FromSeconds(_jwtConfig.AccessTokenExpiries).TotalSeconds,
                    refresh_token = newRefresh,
                    refresh_token_expires = (int)TimeSpan.FromSeconds(_jwtConfig.RefreshTokenExpiries).TotalSeconds
                };
                return Ok(resp2);
            }


            return BadRequest(new { error = "unsupported_grant_type" });
        }

        // POST /connect/revoke  (revoke refresh token)
        [HttpPost("revoke")]
        public async Task<IActionResult> Revoke(
            [FromQuery] string refresh_token,
            [FromQuery] string client_id)
        {
            if (string.IsNullOrEmpty(refresh_token) || string.IsNullOrEmpty(client_id)) return BadRequest();

            var client = await _dbContext.Clients.FirstOrDefaultAsync(c => c.ClientId == client_id);
            if (client == null) return BadRequest();

            var hashed = tokenService.HashToken(refresh_token);
            var stored = await _dbContext.RefreshTokens.FirstOrDefaultAsync(t => t.HashedToken == hashed && t.ClientId == client.ClientId);
            if (stored == null) return Ok(); // RFC 7009: return 200 even if not found

            stored.Revoked = true;
            await _dbContext.SaveChangesAsync();
            return Ok();
        }
    }
}
