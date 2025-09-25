@echo off
REM Quick PostgreSQL setup for development (Windows)

echo 🐘 Starting PostgreSQL for Todo Service...

REM Stop and remove existing container if it exists
docker stop todo-postgres >nul 2>&1
docker rm todo-postgres >nul 2>&1

REM Start PostgreSQL container
docker run -d ^
  --name todo-postgres ^
  -p 5432:5432 ^
  -e POSTGRES_USER=postgres ^
  -e POSTGRES_PASSWORD=password ^
  -e POSTGRES_DB=todoapp ^
  -v todo_postgres_data:/var/lib/postgresql/data ^
  postgres:15-alpine

echo ⏳ Waiting for PostgreSQL to be ready...
timeout /t 5 /nobreak >nul

REM Check if container is running
docker ps | findstr todo-postgres >nul
if %errorlevel% equ 0 (
    echo ✅ PostgreSQL is running!
    echo 📋 Connection details:
    echo    Host: localhost
    echo    Port: 5432
    echo    Database: todoapp
    echo    Username: postgres
    echo    Password: password
    echo.
    echo 🔗 Connection string: postgresql://postgres:password@localhost:5432/todoapp
    echo.
    echo 🛑 To stop: docker stop todo-postgres
    echo 🗑️  To remove: docker rm todo-postgres
) else (
    echo ❌ Failed to start PostgreSQL container
    exit /b 1
)