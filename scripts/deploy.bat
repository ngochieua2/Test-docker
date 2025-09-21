@echo off
REM Windows batch script for Docker Swarm Stack deployment

set STACK_NAME=swarm-demo
set COMPOSE_FILE=docker-compose.yml

echo Docker Swarm Stack Management (Windows)
echo.

if "%1"=="build" goto build
if "%1"=="deploy" goto deploy
if "%1"=="remove" goto remove
if "%1"=="status" goto status
if "%1"=="help" goto help
goto help

:build
echo Building Docker images...
docker build -t swarm-demo/backend:latest ./backend
docker build -t swarm-demo/frontend:latest ./frontend
echo Images built successfully
goto end

:deploy
echo Deploying stack: %STACK_NAME%
call :build
docker stack deploy -c %COMPOSE_FILE% %STACK_NAME%
echo Stack deployed successfully
goto end

:remove
echo Removing stack: %STACK_NAME%
set /p CONFIRM=Are you sure? (y/N): 
if /i "%CONFIRM%"=="y" (
    docker stack rm %STACK_NAME%
    echo Stack removed successfully
) else (
    echo Operation cancelled
)
goto end

:status
echo Stack status for: %STACK_NAME%
echo.
docker stack services %STACK_NAME%
goto end

:help
echo Usage: %0 [COMMAND]
echo.
echo Commands:
echo   build    Build all Docker images
echo   deploy   Deploy the full stack
echo   remove   Remove the stack
echo   status   Show stack status
echo   help     Show this help
echo.
echo Examples:
echo   %0 build
echo   %0 deploy
echo   %0 status
echo   %0 remove
goto end

:end