namespace AuthServer.Data
{
    public class RefreshToken
    {
        public int Id { get; set; }

        public string HashedToken { get; set; } = string.Empty; // store hashed

        public string ClientId { get; set; } = string.Empty;

        public string Scopes { get; set; } = string.Empty;

        public string SubjectId { get; set; } = string.Empty;

        public DateTime Created { get; set; }

        public DateTime Expires { get; set; }

        public bool Revoked { get; set; }

    }
}
