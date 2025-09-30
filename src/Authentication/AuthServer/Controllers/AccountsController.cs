using AuthServer.Data;
using AuthServer.Helpers;
using AuthServer.Models.Users;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.WebUtilities;
using System.Text;
using System.Text.Encodings.Web;

namespace AuthServer.Controllers
{
    [Route("api/account/v1.0")]
    [ApiController]
    public class AccountsController : ControllerBase
    {
        private readonly UserManager<ApplicationUser> userManager;
        private readonly SignInManager<ApplicationUser> signInManager;
        private readonly IUserStore<ApplicationUser> userStore;
        private readonly IEmailSender<ApplicationUser> emailSender;
        private readonly LinkGenerator linkGenerator;

        public AccountsController(
            UserManager<ApplicationUser> userManager,
            SignInManager<ApplicationUser> signInManager,
            IUserStore<ApplicationUser> userStore,
            IEmailSender<ApplicationUser> emailSender,
            LinkGenerator linkGenerator)
        {
            this.userManager = userManager;
            this.signInManager = signInManager;
            this.userStore = userStore;
            this.emailSender = emailSender;
            this.linkGenerator = linkGenerator;
        }

        [HttpPost("sign-up")]
        public async Task<IActionResult> RegisterAccountAsync([FromForm] RegisterAccountModel request)
        {
            var user = new ApplicationUser();

            await userStore.SetUserNameAsync(user, request.UserName, CancellationToken.None);

            if (!userManager.SupportsUserEmail)
            {
                throw new NotSupportedException("The default UI requires a user store with email support.");
            }

            var emailStore = (IUserEmailStore<ApplicationUser>)userStore;

            await emailStore.SetEmailAsync(user, request.UserName, CancellationToken.None);
            var result = await userManager.CreateAsync(user, request.Password);

            if (!result.Succeeded)
            {
                return BadRequest(result.Errors);
            }

            if (userManager.Options.SignIn.RequireConfirmedAccount)
            {
                var userId = await userManager.GetUserIdAsync(user);
                var code = await userManager.GenerateEmailConfirmationTokenAsync(user);
                code = WebEncoders.Base64UrlEncode(Encoding.UTF8.GetBytes(code));

                var callbackUrl = linkGenerator.GetUriByAction(
                    HttpContext,
                    action: "ConfirmEmail",
                    controller: "Accounts",
                    scheme: HttpContext.Request.Scheme,
                    host: HttpContext.Request.Host,
                    values: new
                    {
                        user_id = userId,
                        code = code,
                        email = request.UserName,
                        callback = request.CallbackUrl
                    });

                if (string.IsNullOrEmpty(callbackUrl))
                {
                    return BadRequest();
                }

                await emailSender.SendConfirmationLinkAsync(user, request.UserName, callbackUrl);
            }

            return Ok();
        }

        [HttpGet("confirm-email")]
        public async Task<IActionResult> ConfirmEmailAsync(
            [FromQuery] string? user_id,
            [FromQuery] string? email,
            [FromQuery] string? code,
            [FromQuery] string? callback)
        {
            string returnUrl = string.Empty;

            if (string.IsNullOrEmpty(user_id) 
                || string.IsNullOrEmpty(email) 
                || string.IsNullOrEmpty(code) 
                || string.IsNullOrEmpty(callback)
            )
            {
                returnUrl = CallbackHelper.ExternalUrl.GetAbsoluteUriByQueryString(callback, new Dictionary<string, string?>
                {
                    ["status"] = "failure",
                    ["reason"] = "invalid_grant"
                });

                return Redirect(returnUrl);
            }

            var user = await userManager.FindByIdAsync(user_id);

            if (user is null)
            {
                returnUrl = CallbackHelper.ExternalUrl.GetAbsoluteUriByQueryString(callback, new Dictionary<string, string?>
                {
                    ["status"] = "failure",
                    ["reason"] = "invalid_grant"
                });

                return Redirect(returnUrl);
            }

            var decodeToken = Encoding.UTF8.GetString(WebEncoders.Base64UrlDecode(code));
            var confirmEmailResult = await userManager.ConfirmEmailAsync(user, decodeToken);

            if (!confirmEmailResult.Succeeded)
            {
                returnUrl = CallbackHelper.ExternalUrl.GetAbsoluteUriByQueryString(callback, new Dictionary<string, string?>
                {
                    ["status"] = "failure",
                    ["reason"] = "invalid_token"
                });

                return Redirect(returnUrl);
            }

            returnUrl = CallbackHelper.ExternalUrl.GetAbsoluteUriByQueryString(callback, new Dictionary<string, string?>
            {
                ["status"] = "success",
                ["reason"] = "success"
            });

            return Redirect(returnUrl);
        }
    }
}
