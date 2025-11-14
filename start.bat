@echo off
REM Ornakala Backend Startup Script for Windows
REM This script sets up the environment and starts the application

echo 🚀 Starting Ornakala Backend...

REM Check if .env file exists
if not exist .env (
    echo 📋 Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Please update .env file with your configuration before running again
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo 🔧 Creating virtual environment...
    python -m venv venv
)

echo 📦 Activating virtual environment...
call venv\Scripts\activate.bat

echo 📦 Installing dependencies...
pip install -r requirements.txt

echo 🗃️  Initializing database...
python -c "import asyncio; from app.infrastructure.database import DatabaseManager; asyncio.run(DatabaseManager.initialize()); print('Database initialized successfully')"

echo 🎯 Starting application...
python main.py

pause