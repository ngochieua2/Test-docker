#!/bin/bash

# Docker Swarm Stack Deployment Script
# This script helps deploy the entire stack or individual services

set -e

STACK_NAME="swarm-demo"
COMPOSE_FILE="docker-compose.yml"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker Swarm is initialized
check_swarm() {
    if ! docker info | grep -q "Swarm: active"; then
        log_error "Docker Swarm is not initialized"
        log_info "Run: docker swarm init"
        exit 1
    fi
    log_info "Docker Swarm is active"
}

# Build images
build_images() {
    log_info "Building Docker images..."
    
    log_info "Building backend image..."
    docker build -t swarm-demo/backend:latest ./backend
    
    log_info "Building frontend image..."
    docker build -t swarm-demo/frontend:latest ./frontend
    
    log_info "Images built successfully"
}

# Deploy full stack
deploy_stack() {
    log_info "Deploying full stack: $STACK_NAME"
    docker stack deploy -c $COMPOSE_FILE $STACK_NAME
    log_info "Stack deployed successfully"
}

# Deploy individual service
deploy_service() {
    local service=$1
    log_info "Deploying service: $service"
    docker service update --force ${STACK_NAME}_${service}
    log_info "Service $service updated successfully"
}

# Remove stack
remove_stack() {
    log_warn "Removing stack: $STACK_NAME"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker stack rm $STACK_NAME
        log_info "Stack removed successfully"
    else
        log_info "Operation cancelled"
    fi
}

# Show stack status
show_status() {
    log_info "Stack status for: $STACK_NAME"
    echo
    docker stack services $STACK_NAME
    echo
    log_info "Service logs (use 'docker service logs <service>' for detailed logs)"
}

# Scale service
scale_service() {
    local service=$1
    local replicas=$2
    log_info "Scaling service $service to $replicas replicas"
    docker service scale ${STACK_NAME}_${service}=$replicas
    log_info "Service scaled successfully"
}

# Show help
show_help() {
    echo "Docker Swarm Stack Management Script"
    echo
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo
    echo "Commands:"
    echo "  build              Build all Docker images"
    echo "  deploy             Deploy the full stack"
    echo "  deploy-service     Deploy/update a specific service"
    echo "  remove             Remove the stack"
    echo "  status             Show stack status"
    echo "  scale              Scale a service"
    echo "  logs               Show service logs"
    echo "  help               Show this help"
    echo
    echo "Examples:"
    echo "  $0 build"
    echo "  $0 deploy"
    echo "  $0 deploy-service backend"
    echo "  $0 scale frontend 3"
    echo "  $0 logs backend"
    echo "  $0 status"
    echo "  $0 remove"
}

# Show service logs
show_logs() {
    local service=$1
    if [ -z "$service" ]; then
        log_error "Service name required"
        echo "Available services: frontend, backend, postgresql, sqlserver, nginx"
        exit 1
    fi
    
    log_info "Showing logs for service: $service"
    docker service logs -f ${STACK_NAME}_${service}
}

# Main script logic
case "${1:-help}" in
    "build")
        check_swarm
        build_images
        ;;
    "deploy")
        check_swarm
        build_images
        deploy_stack
        ;;
    "deploy-service")
        if [ -z "$2" ]; then
            log_error "Service name required"
            exit 1
        fi
        check_swarm
        deploy_service $2
        ;;
    "remove")
        check_swarm
        remove_stack
        ;;
    "status")
        check_swarm
        show_status
        ;;
    "scale")
        if [ -z "$2" ] || [ -z "$3" ]; then
            log_error "Service name and replica count required"
            echo "Usage: $0 scale <service> <replicas>"
            exit 1
        fi
        check_swarm
        scale_service $2 $3
        ;;
    "logs")
        if [ -z "$2" ]; then
            log_error "Service name required"
            exit 1
        fi
        check_swarm
        show_logs $2
        ;;
    "help"|*)
        show_help
        ;;
esac