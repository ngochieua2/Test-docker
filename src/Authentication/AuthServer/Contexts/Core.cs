namespace AuthServer.Contexts
{
    public sealed class Core
    {
        public static IDictionary<string, string> Auth2Context = new Dictionary<string, string>()
        {
            { MailService.SERVICE_NAME, MailService.SERVICE_NAME },
            { MailService.HOST_NAME, MailService.HOST_NAME }
        };

        public class MailService
        {
            public const string SERVICE_NAME = "Brevo";

            public const string HOST_NAME = "MailService:Brevo:Host";
        }
    }
}
