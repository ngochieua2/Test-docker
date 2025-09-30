namespace AuthServer.Models.Users
{
    public class RegisterAccountModel
    {
        public string UserName { get; set; } = string.Empty;

        public string Password { get; set; } = string.Empty;

        public string ConfirmPassword { get; set; } = string.Empty;

        public string CallbackUrl { get; set; } = string.Empty;
    }
}
