#!/bin/bash

# Docker Swarm Stack Monitoring Script
# This script provides monitoring and health check capabilities

set -e

STACK_NAME="swarm-demo"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

log_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# Check service health
check_service_health() {
    local service=$1
    log_info "Checking health for service: $service"
    
    # Get service details
    local service_info=$(docker service inspect ${STACK_NAME}_${service} 2>/dev/null)
    if [ $? -ne 0 ]; then
        log_error "Service ${service} not found"
        return 1
    fi
    
    # Get running tasks
    local running_tasks=$(docker service ps ${STACK_NAME}_${service} --filter "desired-state=running" --format "table {{.Name}}\t{{.CurrentState}}\t{{.Error}}")
    echo "$running_tasks"
    echo
}

# Monitor all services
monitor_all() {
    log_info "Monitoring all services in stack: $STACK_NAME"
    echo
    
    local services=("frontend" "backend" "postgresql" "sqlserver")
    
    for service in "${services[@]}"; do
        echo "=== $service ==="
        check_service_health $service
        echo
    done
}

# Check API endpoints
check_endpoints() {
    log_info "Checking API endpoints..."
    
    # Get the external IP (or use localhost for testing)
    local host="localhost"
    
    # Check frontend
    log_debug "Checking frontend health..."
    if curl -s -o /dev/null -w "%{http_code}" http://$host:3000/health | grep -q "200"; then
        log_info "✅ Frontend is healthy"
    else
        log_error "❌ Frontend is not responding"
    fi
    
    # Check backend directly
    log_debug "Checking backend health..."
    if curl -s -o /dev/null -w "%{http_code}" http://$host:8080/health | grep -q "200"; then
        log_info "✅ Backend is healthy"
    else
        log_error "❌ Backend is not responding"
    fi
    
    # Check sample API
    log_debug "Checking sample API..."
    if curl -s -o /dev/null -w "%{http_code}" http://$host:8080/sample | grep -q "200"; then
        log_info "✅ Sample API is working"
    else
        log_error "❌ Sample API is not responding"
    fi
    
    # Check PostgreSQL health
    log_debug "Checking PostgreSQL health..."
    if curl -s -o /dev/null -w "%{http_code}" http://$host:8080/health/postgres | grep -q "200"; then
        log_info "✅ PostgreSQL is healthy"
    else
        log_error "❌ PostgreSQL is not responding"
    fi
    
    log_debug "Checking SQL Server health..."
    if curl -s -o /dev/null -w "%{http_code}" http://$host:8080/health/sqlserver | grep -q "200"; then
        log_info "✅ SQL Server is healthy"
    else
        log_error "❌ SQL Server is not responding"
    fi
}

# Show resource usage
show_resources() {
    log_info "Resource usage for stack: $STACK_NAME"
    echo
    
    # Get all services in the stack
    local services=$(docker stack services $STACK_NAME --format "{{.Name}}")
    
    for service in $services; do
        echo "=== $service ==="
        # Get service constraints and resource limits
        docker service inspect $service --format '
Resource Limits:
  Memory: {{.Spec.TaskTemplate.Resources.Limits.MemoryBytes}}
  CPU: {{.Spec.TaskTemplate.Resources.Limits.NanoCPUs}}
Resource Reservations:
  Memory: {{.Spec.TaskTemplate.Resources.Reservations.MemoryBytes}}
  CPU: {{.Spec.TaskTemplate.Resources.Reservations.NanoCPUs}}
Replicas: {{.Spec.Mode.Replicated.Replicas}}
'
        echo
    done
}

# Continuous monitoring
continuous_monitor() {
    local interval=${1:-30}
    log_info "Starting continuous monitoring (interval: ${interval}s)"
    log_info "Press Ctrl+C to stop"
    
    while true; do
        clear
        echo "=== Docker Swarm Stack Monitor ==="
        echo "Timestamp: $(date)"
        echo "Stack: $STACK_NAME"
        echo
        
        monitor_all
        check_endpoints
        
        echo
        log_info "Next update in ${interval} seconds..."
        sleep $interval
    done
}

# Show stack overview
show_overview() {
    log_info "Stack Overview: $STACK_NAME"
    echo
    
    # Stack services
    echo "Services:"
    docker stack services $STACK_NAME
    echo
    
    # Stack networks
    echo "Networks:"
    docker network ls --filter "label=com.docker.stack.namespace=$STACK_NAME"
    echo
    
    # Stack volumes
    echo "Volumes:"
    docker volume ls --filter "label=com.docker.stack.namespace=$STACK_NAME"
    echo
}

# Show help
show_help() {
    echo "Docker Swarm Stack Monitoring Script"
    echo
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo
    echo "Commands:"
    echo "  health             Check health of all services"
    echo "  endpoints          Check API endpoints"
    echo "  resources          Show resource usage"
    echo "  overview           Show stack overview"
    echo "  monitor [interval] Start continuous monitoring (default: 30s)"
    echo "  service <name>     Check specific service health"
    echo "  help               Show this help"
    echo
    echo "Examples:"
    echo "  $0 health"
    echo "  $0 endpoints"
    echo "  $0 monitor 10"
    echo "  $0 service backend"
}

# Main script logic
case "${1:-help}" in
    "health")
        monitor_all
        ;;
    "endpoints")
        check_endpoints
        ;;
    "resources")
        show_resources
        ;;
    "overview")
        show_overview
        ;;
    "monitor")
        continuous_monitor $2
        ;;
    "service")
        if [ -z "$2" ]; then
            log_error "Service name required"
            exit 1
        fi
        check_service_health $2
        ;;
    "help"|*)
        show_help
        ;;
esac