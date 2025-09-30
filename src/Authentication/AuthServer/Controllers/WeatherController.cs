using Microsoft.AspNetCore.Mvc;

namespace AuthServer.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class WeatherController : ControllerBase
    {
        private readonly LinkGenerator _linkGenerator;

        public WeatherController(LinkGenerator linkGenerator)
        {
            _linkGenerator = linkGenerator;
        }

        [HttpGet("forecast")]
        public IActionResult Get()
        {
            var callbackUrl = _linkGenerator.GetUriByAction(
                HttpContext,
                action: "ConfirmEmail",
                controller: "Accounts",
                scheme: HttpContext.Request.Scheme,
                host: HttpContext.Request.Host,
                values: new { user_id = "123", code = "123", email = "tai@gmail.com" });

            return Ok(callbackUrl);
        }
    }
}
