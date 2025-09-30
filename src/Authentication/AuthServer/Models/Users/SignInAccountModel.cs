namespace AuthServer.Models.Users
{
    public class SignInAccountModel
    {
        public string Username { get; set; } = string.Empty;

        public string Password { get; set; } = string.Empty;

        public string? CallbackUrl { get; set; }
    }
}
