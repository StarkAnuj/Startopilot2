@echo off
echo Starting Gemini AI Assistant Frontend...
echo.

cd frontend

echo Installing/checking dependencies...
call npm install

if %ERRORLEVEL% NEQ 0 (
    echo Error: npm install failed
    pause
    exit /b 1
)

echo.
echo Starting Next.js development server...
echo Frontend will be available at: http://localhost:3000
echo.

call npm run dev