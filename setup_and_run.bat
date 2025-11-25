@echo off
echo Gemini AI Assistant - Complete Setup
echo ====================================
echo.

echo Step 1: Running setup script...
call .venv_gemini_demo\Scripts\activate.bat
python setup.py

if %ERRORLEVEL% NEQ 0 (
    echo Setup failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Setup completed successfully!
echo.
echo To start the application:
echo 1. Run run_backend.bat (in one terminal)
echo 2. Run run_frontend.bat (in another terminal)
echo 3. Open http://localhost:3000 in your browser
echo.
pause