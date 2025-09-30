using AuthServer.Data;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Data.Common;

namespace AuthServer.Controllers;

[ApiController]
[Route("api/[controller]")]
public class HealthController : ControllerBase
{
    private readonly ApplicationDbContext _context;
    private readonly ILogger<HealthController> _logger;

    public HealthController(ApplicationDbContext context, ILogger<HealthController> logger)
    {
        _context = context;
        _logger = logger;
    }

    /// <summary>
    /// Basic health check endpoint
    /// </summary>
    /// <returns>Health status</returns>
    [HttpGet]
    public IActionResult Get()
    {
        return Ok(new { status = "Healthy", timestamp = DateTime.UtcNow });
    }

    /// <summary>
    /// Database connectivity health check
    /// </summary>
    /// <returns>Database connection status</returns>
    [HttpGet("database")]
    public async Task<IActionResult> CheckDatabase()
    {
        try
        {
            // Test basic database connectivity
            var canConnect = await _context.Database.CanConnectAsync();
            
            if (!canConnect)
            {
                _logger.LogWarning("Database connectivity check failed - Cannot connect");
                return StatusCode(503, new 
                { 
                    status = "Unhealthy", 
                    service = "Database",
                    message = "Cannot connect to database",
                    timestamp = DateTime.UtcNow 
                });
            }

            var serverInfo = await GetDatabaseServerInfo();

            _logger.LogInformation("Database connectivity check passed");
            
            return Ok(new 
            { 
                status = "Healthy", 
                service = "Database",
                message = "Database connection successful",
                serverInfo = serverInfo,
                timestamp = DateTime.UtcNow 
            });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Database connectivity check failed with exception");
            return StatusCode(503, new 
            { 
                status = "Unhealthy", 
                service = "Database",
                message = ex.Message,
                timestamp = DateTime.UtcNow 
            });
        }
    }

    private async Task<object> GetDatabaseServerInfo()
    {
        try
        {
            using var connection = _context.Database.GetDbConnection();
            await connection.OpenAsync();
            
            using var command = connection.CreateCommand();
            command.CommandText = "SELECT @@VERSION as ServerVersion, DB_NAME() as DatabaseName, @@SERVERNAME as ServerName";
            
            using var reader = await command.ExecuteReaderAsync();
            if (await reader.ReadAsync())
            {
                return new
                {
                    serverVersion = reader["ServerVersion"]?.ToString()?.Split('\n')[0], // First line only
                    databaseName = reader["DatabaseName"]?.ToString(),
                };
            }
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Failed to retrieve database server info");
            return new { error = "Could not retrieve server info" };
        }

        return new { error = "No data returned" };
    }
}