#!/usr/bin/env python3
"""
Cross-platform script to run Todo Service
Works on Windows, Mac, and Ubuntu
"""

import os
import sys
import subprocess
import platform
import argparse
from pathlib import Path

class Colors:
    """ANSI color codes for cross-platform colored output"""
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def colored_print(text, color=Colors.RESET):
    """Print colored text"""
    print(f"{color}{text}{Colors.RESET}")

def show_help():
    """Display help information"""
    colored_print("🚀 Todo Service Runner", Colors.CYAN)
    print("")
    colored_print("Usage:", Colors.YELLOW)
    print("  python run_todo_service.py           # Run with system Python")
    print("  python run_todo_service.py --venv    # Run with virtual environment")
    print("  python run_todo_service.py --help    # Show this help")
    print("")
    colored_print("Service Details:", Colors.YELLOW)
    print("  Port: 8002")
    print("  API Docs: http://localhost:8002/docs")
    print("  Health: http://localhost:8002/health")
    print("  Database: PostgreSQL (localhost:15432/appdb)")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run Todo Service', add_help=False)
    parser.add_argument('--venv', action='store_true', help='Use virtual environment')
    parser.add_argument('--help', action='store_true', help='Show help')
    
    args = parser.parse_args()
    
    if args.help:
        show_help()
        return
    
    colored_print("🚀 Starting Todo Service...", Colors.GREEN)
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    service_dir = os.path.join(script_dir, "services", "todo-service")
    
    # Check if service directory exists
    if not os.path.exists(service_dir):
        colored_print(f"❌ Service directory not found: {service_dir}", Colors.RED)
        sys.exit(1)
    
    # Change to service directory
    os.chdir(service_dir)
    colored_print(f"📁 Working directory: {service_dir}", Colors.CYAN)
    
    # Handle virtual environment
    if args.venv:
        colored_print("🐍 Setting up virtual environment...", Colors.YELLOW)
        
        venv_path = Path("venv")
        if not venv_path.exists():
            try:
                subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            except subprocess.CalledProcessError:
                colored_print("❌ Failed to create virtual environment", Colors.RED)
                sys.exit(1)
        
        # Determine venv paths based on OS
        if platform.system() == "Windows":
            venv_python = os.path.join("venv", "Scripts", "python.exe")
            venv_pip = os.path.join("venv", "Scripts", "pip.exe")
        else:
            venv_python = os.path.join("venv", "bin", "python")
            venv_pip = os.path.join("venv", "bin", "pip")
        
        colored_print("✓ Virtual environment activated", Colors.GREEN)
    else:
        venv_python = sys.executable
        venv_pip = sys.executable
    
    # Install requirements
    colored_print("📦 Installing requirements...", Colors.YELLOW)
    try:
        if args.venv:
            result = subprocess.run([venv_pip, "install", "-r", "requirements.txt"], 
                                  capture_output=True, text=True)
        else:
            result = subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], 
                                  capture_output=True, text=True)
        
        if result.returncode != 0:
            colored_print("❌ Failed to install requirements", Colors.RED)
            colored_print(result.stderr, Colors.RED)
            sys.exit(1)
            
    except subprocess.CalledProcessError as e:
        colored_print(f"❌ Failed to install requirements: {e}", Colors.RED)
        sys.exit(1)
    
    colored_print("✓ Requirements installed", Colors.GREEN)
    
    # Display service information
    print("")
    colored_print("🌟 Starting Todo Service...", Colors.MAGENTA)
    colored_print("🔗 Service URL: http://localhost:8002", Colors.CYAN)
    colored_print("📚 API Documentation: http://localhost:8002/docs", Colors.CYAN)
    colored_print("❤️  Health Check: http://localhost:8002/health", Colors.CYAN)
    colored_print("🗂️  Database: PostgreSQL (localhost:15432/appdb)", Colors.CYAN)
    colored_print("🛑 Press Ctrl+C to stop the service", Colors.YELLOW)
    print("")
    
    # Run the service
    try:
        subprocess.run([venv_python, "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        colored_print(f"❌ Error starting service: {e}", Colors.RED)
        sys.exit(1)
    except KeyboardInterrupt:
        print("")
        colored_print("👋 Todo Service stopped", Colors.YELLOW)

if __name__ == "__main__":
    main()