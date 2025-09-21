# Build individual images manually

# Backend Image
Write-Host "Building FastAPI Backend..." -ForegroundColor Yellow
docker build -t your-dockerhub-username/docker-swarm-stack-backend:latest -f ./backend/Dockerfile ./backend

# Frontend Image  
Write-Host "Building Next.js Frontend..." -ForegroundColor Yellow
docker build -t your-dockerhub-username/docker-swarm-stack-frontend:latest -f ./frontend/Dockerfile ./frontend

# Full Stack Image
Write-Host "Building Full Stack Application..." -ForegroundColor Yellow
docker build -t your-dockerhub-username/docker-swarm-stack-fullstack:latest -f ./Dockerfile.fullstack .

# Push to Docker Hub (login first)
Write-Host "Pushing to Docker Hub..." -ForegroundColor Green
docker login

docker push your-dockerhub-username/docker-swarm-stack-backend:latest
docker push your-dockerhub-username/docker-swarm-stack-frontend:latest  
docker push your-dockerhub-username/docker-swarm-stack-fullstack:latest

Write-Host "Complete! Your images are now on Docker Hub." -ForegroundColor Green