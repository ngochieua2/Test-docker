using AuthServer.Data;
using Microsoft.AspNetCore.Identity;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Security.Cryptography;
using System.Text;

namespace AuthServer.Services
{
    public class JwtOptions
    {
        public string[] ValidAudiences { get; set; } = Array.Empty<string>();
        public string ValidIssuer { get; set; } = "";
        public string SigningSecurityKey { get; set; } = "";
        public int AccessTokenExpiries { get; set; }
        public int RefreshTokenExpiries { get; set; }
    }

    public interface ITokenService
    {
        public string CreateAccessToken(ApplicationUser user, IEnumerable<Claim>? extraClaims = null);
        public string CreateIdToken(ApplicationUser user, IEnumerable<Claim>? extra = null);
        public (string refreshToken, string hashed) GenerateRefreshToken();
        public string HashToken(string token);
    }

    public class TokenService : ITokenService
    {
        private readonly JwtOptions _opts;
        private readonly UserManager<ApplicationUser> _um;

        public TokenService(IOptions<JwtOptions> opts, UserManager<ApplicationUser> um)
        {
            _opts = opts.Value;
            _um = um;
        }

        public string CreateAccessToken(ApplicationUser user, IEnumerable<Claim>? extraClaims = null)
        {
            var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_opts.SigningSecurityKey));
            var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

            var claims = new List<Claim>
            {
                new Claim(JwtRegisteredClaimNames.Sub, user.Id),
                new Claim(JwtRegisteredClaimNames.UniqueName, user.UserName ?? ""),
                new Claim("email", user.Email ?? "")
            };

            // Add multiple audiences manually
            foreach (var aud in _opts.ValidAudiences)
            {
                claims.Add(new Claim(JwtRegisteredClaimNames.Aud, aud));
            }

            if (extraClaims != null) claims.AddRange(extraClaims);

            var token = new JwtSecurityToken(
                issuer: _opts.ValidIssuer,
                claims: claims,
                expires: DateTime.UtcNow.AddSeconds(_opts.AccessTokenExpiries),
                signingCredentials: creds);

            return new JwtSecurityTokenHandler().WriteToken(token);
        }

        public string CreateIdToken(ApplicationUser user, IEnumerable<Claim>? extra = null)
        {
            // Minimal id_token — in OpenID connect you'd include nonce and more
            return CreateAccessToken(user, new[] { new Claim("id_token", "true") });
        }

        public (string refreshToken, string hashed) GenerateRefreshToken()
        {
            var bytes = new byte[64];
            using var rng = RandomNumberGenerator.Create();
            rng.GetBytes(bytes);
            var token = Convert.ToBase64String(bytes);
            var hashed = HashToken(token);
            return (token, hashed);
        }

        public string HashToken(string token)
        {
            using var sha = SHA256.Create();
            var hashed = sha.ComputeHash(Encoding.UTF8.GetBytes(token));
            return Convert.ToBase64String(hashed);
        }
    }
}