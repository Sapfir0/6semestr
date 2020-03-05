using System;
using System.IO;
using System.Net;
using System.Text;

namespace siteParser
{
    class Program
    {
        static void Main(string[] args)
        {
            var url = "https://www.google.com/";
            var key = "trnsl.1.1.20200204T065404Z.3b343a9f66e226a4.1fba6ea1ff5edc50c66c58a812846873dece1e9a";
            HttpWebRequest request = (HttpWebRequest) WebRequest.Create(url);
            request.Credentials = CredentialCache.DefaultCredentials; 
            
            HttpWebResponse response = (HttpWebResponse)request.GetResponse();

            using (var stream = response.GetResponseStream())
            using (var streamReader = new StreamReader(stream, Encoding.UTF8))
            {
                Console.SetBufferSize(80, 10000);
                Console.WriteLine(streamReader.ReadToEnd());

                Console.ReadKey(); 
 
 
            } 
        }
    }
}