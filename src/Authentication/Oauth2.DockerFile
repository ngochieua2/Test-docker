# Stage 1: Build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy csproj and restore
COPY src/Authentication/AuthServer/*.csproj ./AuthServer/
RUN dotnet restore ./AuthServer/AuthServer.csproj

# Copy everything else
COPY src/Authentication/AuthServer ./AuthServer

# Publish the project
WORKDIR /src/AuthServer
RUN dotnet publish -c Release -o /app/publish /p:UseAppHost=false


# Stage 2: Runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app

COPY --from=build /app/publish .

# Expose ports
EXPOSE 80
EXPOSE 443

ENV PATH="$PATH:/root/.dotnet/tools"

# Copy published app
COPY --from=build /app/publish .

# Start the application
ENTRYPOINT ["dotnet", "AuthServer.dll"]