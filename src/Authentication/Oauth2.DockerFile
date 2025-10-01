# Stage 1: Build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy csproj and restore
COPY AuthServer/*.csproj ./AuthServer/
RUN dotnet restore ./AuthServer/AuthServer.csproj

# Copy everything else
COPY AuthServer ./AuthServer

# Publish the project
WORKDIR /src/AuthServer
RUN dotnet publish -c Release -o /app/publish /p:UseAppHost=false

# Stage 2: Runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app

# Create non-root user for security
RUN adduser --disabled-password --gecos '' --uid 1001 appuser

# Copy published app
COPY --from=build /app/publish .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Expose ports
EXPOSE 80

# Start the application
ENTRYPOINT ["dotnet", "AuthServer.dll"]