using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace AuthServer.Data
{
    public class Client
    {
        public int Id { get; set; }

        public string ClientId { get; set; } = "";

        public string? ClientSecretHash { get; set; }

        public string RedirectUris { get; set; } = ""; // newline or space-separated list

        public bool RequirePkce { get; set; } = true;

        public string AllowedScopes { get; set; } = "openid profile api1";

    }
}
