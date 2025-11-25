#!/bin/bash

# AI Assistant - Cross-platform Deploy Script
# Works on Linux, macOS, and Windows (with WSL)

set -e

echo "🚀 AI Assistant - Quick Deploy Script"
echo "====================================="
echo

# Color codes for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js not found. Please install Node.js 18+ first."
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    print_error "Python not found. Please install Python 3.11+ first."
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

print_status "Prerequisites check passed!"
echo

# Show deployment options
echo "🔧 Choose deployment method:"
echo "1. Local Development"
echo "2. Production Build"
echo "3. Docker Deployment"
echo "4. Vercel Deployment"
echo "5. Quick Test (Build + Run)"
echo

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo
        echo "🔄 Starting Local Development..."
        echo

        # Create virtual environment if it doesn't exist
        if [ ! -d ".venv" ]; then
            print_info "Creating Python virtual environment..."
            $PYTHON_CMD -m venv .venv
        fi

        # Activate virtual environment
        source .venv/bin/activate

        # Install Python dependencies
        print_info "Installing Python dependencies..."
        pip install -r requirements.txt

        # Install Node.js dependencies
        print_info "Installing Node.js dependencies..."
        cd frontend
        npm install
        cd ..

        print_status "Dependencies installed!"

        # Start backend in background
        print_info "Starting backend server..."
        source .venv/bin/activate
        $PYTHON_CMD api/main.py &
        BACKEND_PID=$!

        # Wait a moment for backend to start
        sleep 3

        # Start frontend
        print_info "Starting frontend server..."
        cd frontend
        npm run dev &
        FRONTEND_PID=$!
        cd ..

        print_status "Development servers started!"
        echo "🌐 Frontend: http://localhost:3000"
        echo "🔗 Backend: http://localhost:8000"
        echo
        print_info "Press Ctrl+C to stop both servers"

        # Wait for user interrupt
        trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
        wait
        ;;

    2)
        echo
        echo "🏗️ Building for Production..."
        echo

        # Create and activate virtual environment
        if [ ! -d ".venv" ]; then
            $PYTHON_CMD -m venv .venv
        fi
        source .venv/bin/activate

        # Install Python dependencies
        print_info "Installing Python dependencies..."
        pip install -r requirements.txt

        # Build frontend
        cd frontend
        print_info "Installing Node.js dependencies..."
        npm install
        
        print_info "Building frontend..."
        npm run build

        cd ..

        print_status "Production build complete!"
        echo
        print_info "To start production servers:"
        echo "  Frontend: cd frontend && npm start"
        echo "  Backend: python -m uvicorn api.main:app --host 0.0.0.0 --port 8000"
        ;;

    3)
        echo
        echo "🐳 Docker Deployment..."
        echo

        # Check if Docker is installed
        if ! command -v docker &> /dev/null; then
            print_error "Docker not found. Please install Docker first."
            exit 1
        fi

        # Check if .env file exists
        if [ ! -f ".env" ]; then
            print_warning ".env file not found. Creating template..."
            echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
            echo
            print_info "Please edit .env file and add your GEMINI_API_KEY"
            print_info "Then run this script again."
            exit 1
        fi

        print_info "Building and starting with Docker Compose..."
        docker-compose up --build -d

        print_status "Docker deployment complete!"
        echo "🌐 App running at: http://localhost:3000"
        echo "📊 Check status: docker-compose ps"
        echo "📋 View logs: docker-compose logs -f"
        ;;

    4)
        echo
        echo "☁️ Vercel Deployment..."
        echo

        # Check if Vercel CLI is installed
        if ! command -v vercel &> /dev/null; then
            print_info "Installing Vercel CLI..."
            npm install -g vercel
        fi

        print_info "Preparing for deployment..."
        cd frontend
        npm install
        cd ..

        print_info "Starting Vercel deployment..."
        vercel --prod

        print_status "Vercel deployment initiated!"
        echo
        print_warning "Don't forget to add GEMINI_API_KEY in Vercel dashboard:"
        print_info "Project Settings > Environment Variables"
        ;;

    5)
        echo
        echo "🧪 Quick Test Build..."
        echo

        # Quick setup and test
        if [ ! -d ".venv" ]; then
            $PYTHON_CMD -m venv .venv
        fi
        source .venv/bin/activate
        
        pip install -r requirements.txt
        
        cd frontend
        npm install
        npm run build
        cd ..

        # Test backend
        print_info "Testing backend..."
        timeout 10 $PYTHON_CMD -c "
import sys
sys.path.append('.')
from api.main import app
print('✅ Backend imports successful')
"

        print_status "Quick test completed!"
        print_info "All components are ready for deployment!"
        ;;

    *)
        print_error "Invalid choice. Exiting..."
        exit 1
        ;;
esac

echo
print_status "Deployment script completed!"
echo