using AuthServer.Contexts;
using AuthServer.Data;
using AuthServer.Models.Emails;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.UI.Services;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;

namespace AuthServer.Services
{
    public class MailServiceConfigure<T>
    {
        public string Email { get; set; } = string.Empty;

        public string Name { get; set; } = string.Empty;

        [ConfigurationKeyName("Brevo")]
        public T Settings { get; set; } = Activator.CreateInstance<T>();
    }

    public class BravoMailService
    {
        public string ApiKey { get; set; } = string.Empty;

        public string Host { get; set; } = string.Empty;
    }

    public class MailService : IEmailSender
    {
        private readonly IHttpClientFactory _httpClientFactory;
        private readonly MailServiceConfigure<BravoMailService> mailServiceConfigure;
        private readonly ILogger<MailService> _logger;
        private readonly IConfiguration _configuration;

        public MailService(
            IHttpClientFactory httpClientFactory,
            IOptions<MailServiceConfigure<BravoMailService>> mailServiceConfigureOption,
            ILogger<MailService> logger,
            IConfiguration configuration)
        {
            this._httpClientFactory = httpClientFactory;
            this.mailServiceConfigure = mailServiceConfigureOption.Value;
            this._logger = logger;
            this._configuration = configuration;
        }

        public async Task SendEmailAsync(string email, string subject, string jObject)
        {
            using (var httpClient = _httpClientFactory.CreateClient(Core.MailService.SERVICE_NAME))
            {
                try
                {
                    HttpRequestMessage requestMessage = new HttpRequestMessage(HttpMethod.Post, "v3/smtp/email");

                    requestMessage.Headers.Accept.Clear();
                    requestMessage.Headers.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
                    requestMessage.Headers.Add("api-key", mailServiceConfigure.Settings.ApiKey);
                    requestMessage.Content = new StringContent(jObject, Encoding.UTF8, "application/json");

                    using (var cts = new CancellationTokenSource(TimeSpan.FromSeconds(30)))
                    {
                        using (var response = await httpClient.SendAsync(requestMessage, cts.Token))
                        {
                            response.EnsureSuccessStatusCode();
                        }
                    }
                }
                catch (Exception)
                {
                    _logger.LogError("Exception when send mail");
                    throw;
                }
            }
        }
    }

    public class IdentityEmailSender : IEmailSender<ApplicationUser>
    {
        private readonly IEmailSender emailSender;
        private readonly MailServiceConfigure<BravoMailService> mailServiceConfigure;

        public IdentityEmailSender(
            IEmailSender emailSender,
            IOptions<MailServiceConfigure<BravoMailService>> mailServiceConfigureOption)
        {
            this.emailSender = emailSender;
            this.mailServiceConfigure = mailServiceConfigureOption.Value;
        }

        public async Task SendConfirmationLinkAsync(ApplicationUser user, string email, string confirmationLink)
        {
            SendEmailTemplateModel template = new SendEmailTemplateModel();
            template.Sender.Email = mailServiceConfigure.Email;
            template.Sender.Name = mailServiceConfigure.Name;
            template.Subject = "Confirmation Link";
            template.TemplateId = 2;
            template.To = new SendEmailTemplateModelReceiver[]
            {
                new SendEmailTemplateModelReceiver
                {
                    Email = email,
                    Name = user.UserName ?? string.Empty
                }
            };
            template.Params = new Dictionary<string, string>
            {
                { "CONFIRMATION_LINK", confirmationLink }
            };

            await emailSender.SendEmailAsync(email ?? throw new ArgumentNullException("Can not send to null email"), "Confirmation Link", JsonSerializer.Serialize(template));
        }

        public Task SendPasswordResetCodeAsync(ApplicationUser user, string email, string resetCode)
        {
            throw new NotImplementedException();
        }

        public Task SendPasswordResetLinkAsync(ApplicationUser user, string email, string resetLink)
        {
            throw new NotImplementedException();
        }
    }
}
