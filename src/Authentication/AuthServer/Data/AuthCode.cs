namespace AuthServer.Data
{
    public class AuthCode
    {
        public int Id { get; set; }

        public string CodeHash { get; set; } = string.Empty; // store the code (or hashed)

        public string ClientId { get; set; } = string.Empty;

        public string RedirectUri { get; set; } = string.Empty;

        public string SubjectId { get; set; } = string.Empty; // user id

        public DateTime Expires { get; set; }

        public string CodeChallenge { get; set; } = string.Empty; // PKCE

        public string CodeChallengeMethod { get; set; } = string.Empty; // "S256" or "plain"

        public string Scopes { get; set; } = string.Empty; // space-separated

        public bool Consumed { get; set; }

    }
}
