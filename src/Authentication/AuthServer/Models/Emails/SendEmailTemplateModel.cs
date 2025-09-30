using System.Text.Json.Nodes;
using System.Text.Json.Serialization;

namespace AuthServer.Models.Emails
{
    public class SendEmailTemplateModel
    {
        [JsonPropertyName("sender")]
        public SendEmailTemplateModelSender Sender { get; set; } = new SendEmailTemplateModelSender();

        [JsonPropertyName("to")]
        public SendEmailTemplateModelReceiver[] To { get; set; } = Array.Empty<SendEmailTemplateModelReceiver>();

        [JsonPropertyName("templateId")]
        public int TemplateId { get; set; }

        [JsonPropertyName("subject")]
        public string? Subject { get; set; }

        [JsonPropertyName("params")]
        public Dictionary<string, string>? Params { get; set; }

        [JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)]
        [JsonPropertyName("messageVersions")]
        public JsonObject? MessageVersions { get; set; }
    }

    public class SendEmailTemplateModelSender
    {
        [JsonPropertyName("email")]
        public string Email { get; set; } = string.Empty;

        [JsonPropertyName("name")]
        public string Name { get; set; } = string.Empty;
    }

    public class SendEmailTemplateModelReceiver
    {
        [JsonPropertyName("email")]
        public string Email { get; set; } = string.Empty;

        [JsonPropertyName("name")]
        public string Name { get; set; } = string.Empty;
    }
}
