@echo off
echo Starting Gemini AI Assistant Backend...
echo.

REM Activate virtual environment
call .venv_gemini_demo\Scripts\activate.bat

REM Check if activation was successful
if %ERRORLEVEL% NEQ 0 (
    echo Error: Could not activate virtual environment
    echo Make sure .venv_gemini_demo exists and is properly configured
    pause
    exit /b 1
)

echo Virtual environment activated
echo Starting FastAPI server on port 8000...
echo.
echo Backend will be available at: http://localhost:8000
echo API Documentation at: http://localhost:8000/docs
echo.

python -m uvicorn api.main:app --reload --port 8000