#!/bin/bash

# Ornakala Backend Startup Script
# This script sets up the environment and starts the application

echo "🚀 Starting Ornakala Backend..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📋 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env file with your configuration before running again"
    exit 1
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

echo "📦 Activating virtual environment..."
source venv/bin/activate

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🗃️  Initializing database..."
python3 -c "
import asyncio
from app.infrastructure.database import DatabaseManager

async def init_db():
    await DatabaseManager.initialize()
    print('Database initialized successfully')

if __name__ == '__main__':
    asyncio.run(init_db())
"

echo "🎯 Starting application..."
python3 main.py