@echo off
echo 🚀 AI Assistant - Quick Deploy Script
echo =====================================

echo.
echo 📋 Checking prerequisites...

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found. Please install Node.js 18+ first.
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.11+ first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed!
echo.

echo 🔧 Choose deployment method:
echo 1. Local Development
echo 2. Production Build
echo 3. Docker Deployment
echo 4. Vercel Deployment
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto local
if "%choice%"=="2" goto production
if "%choice%"=="3" goto docker
if "%choice%"=="4" goto vercel

echo ❌ Invalid choice. Exiting...
pause
exit /b 1

:local
echo.
echo 🔄 Starting Local Development...
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv .venv
)

REM Activate virtual environment and install Python dependencies
echo 📦 Installing Python dependencies...
call .venv\Scripts\activate.bat
pip install -r requirements.txt

REM Install Node.js dependencies
echo 📦 Installing Node.js dependencies...
cd frontend
npm install
cd ..

REM Start servers
echo 🚀 Starting development servers...
start "Backend" cmd /c "cd /d %cd% && .venv\Scripts\python.exe api\main.py"
timeout /t 3 /nobreak >nul
cd frontend
start "Frontend" cmd /c "npm run dev"
cd ..

echo ✅ Development servers started!
echo 🌐 Frontend: http://localhost:3000
echo 🔗 Backend: http://localhost:8000
pause
exit /b 0

:production
echo.
echo 🏗️ Building for Production...
echo.

REM Install dependencies
echo 📦 Installing dependencies...
call .venv\Scripts\activate.bat || (
    python -m venv .venv
    call .venv\Scripts\activate.bat
)
pip install -r requirements.txt

cd frontend
npm install
echo 🔨 Building frontend...
npm run build

echo ✅ Production build complete!
echo 💡 To start: npm start (frontend) and python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
cd ..
pause
exit /b 0

:docker
echo.
echo 🐳 Docker Deployment...
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker not found. Please install Docker first.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found. Creating template...
    echo GEMINI_API_KEY=your_gemini_api_key_here > .env
    echo.
    echo 🔑 Please edit .env file and add your GEMINI_API_KEY
    echo Then run this script again.
    pause
    exit /b 1
)

echo 🔨 Building and starting with Docker Compose...
docker-compose up --build -d

echo ✅ Docker deployment complete!
echo 🌐 App running at: http://localhost:3000
echo 📊 Check status: docker-compose ps
echo 📋 View logs: docker-compose logs -f
pause
exit /b 0

:vercel
echo.
echo ☁️  Vercel Deployment...
echo.

REM Check if Vercel CLI is installed
vercel --version >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing Vercel CLI...
    npm install -g vercel
)

echo 🚀 Deploying to Vercel...
cd frontend
npm install
cd ..

echo 🌐 Starting deployment...
vercel --prod

echo.
echo ✅ Vercel deployment initiated!
echo 🔑 Don't forget to add GEMINI_API_KEY in Vercel dashboard:
echo    Project Settings > Environment Variables
echo.
pause
exit /b 0