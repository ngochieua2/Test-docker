using Microsoft.AspNetCore.WebUtilities;

namespace AuthServer.Helpers
{
    public sealed class CallbackHelper
    {
        public class ExternalUrl
        {
            public static string GetAbsoluteUriByQueryString(string? callbackUrl, Dictionary<string, string?> param)
            {
                if (string.IsNullOrEmpty(callbackUrl)) throw new ArgumentNullException("Callbacl was null");

                return QueryHelpers.AddQueryString(callbackUrl, param);
            }
        }
    }
}
