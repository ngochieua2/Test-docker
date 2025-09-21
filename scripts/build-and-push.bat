@echo off
REM Docker Hub Build and Push Script for Windows
REM Usage: build-and-push.bat [your-dockerhub-username]

if "%1"=="" (
    echo Usage: %0 [your-dockerhub-username]
    echo Example: %0 myusername
    exit /b 1
)

set DOCKERHUB_USERNAME=%1
set PROJECT_NAME=docker-swarm-stack
set VERSION=latest

echo Building and pushing Docker images to Docker Hub...
echo Docker Hub Username: %DOCKERHUB_USERNAME%

REM Login to Docker Hub
echo.
echo Logging in to Docker Hub...
docker login

REM Build and push FastAPI backend
echo.
echo === Building FastAPI Backend ===
echo Building %DOCKERHUB_USERNAME%/%PROJECT_NAME%-backend:%VERSION%...
docker build -t %DOCKERHUB_USERNAME%/%PROJECT_NAME%-backend:%VERSION% -f ./backend/Dockerfile ./backend
if errorlevel 1 (
    echo Failed to build backend image
    exit /b 1
)

echo Pushing %DOCKERHUB_USERNAME%/%PROJECT_NAME%-backend:%VERSION% to Docker Hub...
docker push %DOCKERHUB_USERNAME%/%PROJECT_NAME%-backend:%VERSION%
if errorlevel 1 (
    echo Failed to push backend image
    exit /b 1
)

REM Build and push Next.js frontend
echo.
echo === Building Next.js Frontend ===
echo Building %DOCKERHUB_USERNAME%/%PROJECT_NAME%-frontend:%VERSION%...
docker build -t %DOCKERHUB_USERNAME%/%PROJECT_NAME%-frontend:%VERSION% -f ./frontend/Dockerfile ./frontend
if errorlevel 1 (
    echo Failed to build frontend image
    exit /b 1
)

echo Pushing %DOCKERHUB_USERNAME%/%PROJECT_NAME%-frontend:%VERSION% to Docker Hub...
docker push %DOCKERHUB_USERNAME%/%PROJECT_NAME%-frontend:%VERSION%
if errorlevel 1 (
    echo Failed to push frontend image
    exit /b 1
)

REM Build and push full stack application
echo.
echo === Building Full Stack Application ===
echo Building %DOCKERHUB_USERNAME%/%PROJECT_NAME%-fullstack:%VERSION%...
docker build -t %DOCKERHUB_USERNAME%/%PROJECT_NAME%-fullstack:%VERSION% -f ./Dockerfile.fullstack .
if errorlevel 1 (
    echo Failed to build fullstack image
    exit /b 1
)

echo Pushing %DOCKERHUB_USERNAME%/%PROJECT_NAME%-fullstack:%VERSION% to Docker Hub...
docker push %DOCKERHUB_USERNAME%/%PROJECT_NAME%-fullstack:%VERSION%
if errorlevel 1 (
    echo Failed to push fullstack image
    exit /b 1
)

echo.
echo === Build and Push Complete ===
echo Your images are now available on Docker Hub:
echo • %DOCKERHUB_USERNAME%/%PROJECT_NAME%-backend:%VERSION%
echo • %DOCKERHUB_USERNAME%/%PROJECT_NAME%-frontend:%VERSION%
echo • %DOCKERHUB_USERNAME%/%PROJECT_NAME%-fullstack:%VERSION%

echo.
echo To use these images, update your docker-compose.yml:
echo backend:
echo   image: %DOCKERHUB_USERNAME%/%PROJECT_NAME%-backend:%VERSION%
echo frontend:
echo   image: %DOCKERHUB_USERNAME%/%PROJECT_NAME%-frontend:%VERSION%