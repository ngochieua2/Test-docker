using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace AuthServer.Data;

public class ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : IdentityDbContext<ApplicationUser>(options)
{
    public DbSet<AuthCode> AuthCodes { get; set; }

    public DbSet<RefreshToken> RefreshTokens { get; set; }

    public DbSet<Client> Clients { get; set; }
}
