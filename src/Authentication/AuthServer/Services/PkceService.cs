using System.Security.Cryptography;
using System.Text;

namespace AuthServer.Services
{
    public interface IPkceService
    {
        string ComputeCodeChallengeS256(string codeVerifier);
    }

    public class PkceService : IPkceService
    {
        public string ComputeCodeChallengeS256(string codeVerifier)
        {
            using var sha = SHA256.Create();
            var bytes = sha.ComputeHash(Encoding.ASCII.GetBytes(codeVerifier));
            return Base64UrlEncode(bytes);
        }

        private static string Base64UrlEncode(byte[] input)
        {
            return Convert.ToBase64String(input)
                .TrimEnd('=')
                .Replace('+', '-')
                .Replace('/', '_');
        }

    }
}
