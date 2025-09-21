#!/bin/bash

# Docker Hub Build and Push Script
# Usage: ./build-and-push.sh [your-dockerhub-username]

if [ -z "$1" ]; then
    echo "Usage: $0 [your-dockerhub-username]"
    echo "Example: $0 myusername"
    exit 1
fi

DOCKERHUB_USERNAME=$1
PROJECT_NAME="docker-swarm-stack"
VERSION="latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Building and pushing Docker images to Docker Hub...${NC}"
echo -e "${YELLOW}Docker Hub Username: ${DOCKERHUB_USERNAME}${NC}"

# Function to build and push an image
build_and_push() {
    local context=$1
    local dockerfile=$2
    local image_name=$3
    local tag="${DOCKERHUB_USERNAME}/${image_name}:${VERSION}"
    
    echo -e "\n${YELLOW}Building ${image_name}...${NC}"
    
    if docker build -t "${tag}" -f "${dockerfile}" "${context}"; then
        echo -e "${GREEN}✓ Successfully built ${tag}${NC}"
        
        echo -e "${YELLOW}Pushing ${tag} to Docker Hub...${NC}"
        if docker push "${tag}"; then
            echo -e "${GREEN}✓ Successfully pushed ${tag}${NC}"
        else
            echo -e "${RED}✗ Failed to push ${tag}${NC}"
            return 1
        fi
    else
        echo -e "${RED}✗ Failed to build ${tag}${NC}"
        return 1
    fi
}

# Login to Docker Hub
echo -e "\n${YELLOW}Logging in to Docker Hub...${NC}"
docker login

# Build and push FastAPI backend
echo -e "\n${YELLOW}=== Building FastAPI Backend ===${NC}"
build_and_push "./backend" "./backend/Dockerfile" "${PROJECT_NAME}-backend"

# Build and push Next.js frontend
echo -e "\n${YELLOW}=== Building Next.js Frontend ===${NC}"
build_and_push "./frontend" "./frontend/Dockerfile" "${PROJECT_NAME}-frontend"

# Build and push full stack application
echo -e "\n${YELLOW}=== Building Full Stack Application ===${NC}"
build_and_push "." "./Dockerfile.fullstack" "${PROJECT_NAME}-fullstack"

echo -e "\n${GREEN}=== Build and Push Complete ===${NC}"
echo -e "${YELLOW}Your images are now available on Docker Hub:${NC}"
echo -e "• ${DOCKERHUB_USERNAME}/${PROJECT_NAME}-backend:${VERSION}"
echo -e "• ${DOCKERHUB_USERNAME}/${PROJECT_NAME}-frontend:${VERSION}"
echo -e "• ${DOCKERHUB_USERNAME}/${PROJECT_NAME}-fullstack:${VERSION}"

echo -e "\n${YELLOW}To use these images, update your docker-compose.yml:${NC}"
echo -e "backend:"
echo -e "  image: ${DOCKERHUB_USERNAME}/${PROJECT_NAME}-backend:${VERSION}"
echo -e "frontend:"
echo -e "  image: ${DOCKERHUB_USERNAME}/${PROJECT_NAME}-frontend:${VERSION}"