using System.Security.Cryptography;
using System.Text;
using CoffeeShop.Data;

namespace CoffeeShop.Services;

public static class AuthService
{
    private const int SaltSize = 16;

    public static string HashPassword(string password, string salt)
    {
        using var sha = SHA256.Create();
        var bytes = Encoding.UTF8.GetBytes(salt + password);
        return Convert.ToHexString(sha.ComputeHash(bytes));
    }

    public static bool VerifyPassword(
        string password, string salt, string expectedHash)
    {
        var actual = HashPassword(password, salt);
        return CryptographicOperations.FixedTimeEquals(
            Convert.FromHexString(actual),
            Convert.FromHexString(expectedHash));
    }

    public static Models.User? Authenticate(string login, string password)
    {
        var user = UserRepository.FindByLogin(login);
        if (user is null)
        {
            return null;
        }
        return VerifyPassword(password, user.Salt, user.PasswordHash)
            ? user
            : null;
    }

    public static string CreateSalt()
    {
        return Convert.ToHexString(RandomNumberGenerator.GetBytes(SaltSize));
    }
}
