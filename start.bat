@echo off
REM Church Community Bot - Windows Start Script
REM Created by: PINLON-YOUTH

echo ==========================================
echo Church Community Bot Setup
echo Created by: PINLON-YOUTH
echo ==========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo Python found
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed successfully
echo.

REM Check if .env exists
if not exist .env (
    echo WARNING: .env file not found. Creating from template...
    copy .env.example .env
    echo .env file created
    echo.
    echo Please edit .env file and add your:
    echo   1. BOT_TOKEN (get from @BotFather)
    echo   2. ADMIN_IDS (get from @userinfobot)
    echo.
    notepad .env
    echo.
    pause
)

echo.
echo ==========================================
echo Starting Church Community Bot...
echo ==========================================
echo.

REM Run the bot
python bot.py

pause
