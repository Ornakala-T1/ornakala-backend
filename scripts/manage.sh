#!/bin/bash

# Ornakala Backend Process Management Script
# Usage: ./manage.sh [start|stop|restart|status|logs]

PROCESS_NAME="python.*main.py"
APP_DIR="$HOME/ornakala-backend"
LOG_FILE="$APP_DIR/app.log"

case "$1" in
    start)
        echo "🚀 Starting main.py..."
        cd "$APP_DIR" || {
            echo "❌ Directory $APP_DIR not found"
            exit 1
        }
        
        # Check if already running
        if pgrep -f "$PROCESS_NAME" > /dev/null; then
            echo "⚠️ main.py is already running. PID: $(pgrep -f "$PROCESS_NAME")"
            exit 1
        fi
        
        # Start the process
        nohup python3 main.py > "$LOG_FILE" 2>&1 &
        sleep 2
        
        # Verify it started
        if pgrep -f "$PROCESS_NAME" > /dev/null; then
            echo "✅ main.py started successfully!"
            echo "📋 Process ID: $(pgrep -f "$PROCESS_NAME")"
        else
            echo "❌ Failed to start main.py. Check logs:"
            tail -10 "$LOG_FILE"
        fi
        ;;
        
    stop)
        echo "🛑 Stopping main.py..."
        if pgrep -f "$PROCESS_NAME" > /dev/null; then
            pkill -f "$PROCESS_NAME"
            sleep 2
            
            if pgrep -f "$PROCESS_NAME" > /dev/null; then
                echo "⚠️ Process still running, force killing..."
                pkill -9 -f "$PROCESS_NAME"
            fi
            
            echo "✅ main.py stopped successfully!"
        else
            echo "⚠️ main.py is not running"
        fi
        ;;
        
    restart)
        echo "🔄 Restarting main.py..."
        $0 stop
        sleep 1
        $0 start
        ;;
        
    status)
        echo "📊 Checking main.py status..."
        if pgrep -f "$PROCESS_NAME" > /dev/null; then
            PID=$(pgrep -f "$PROCESS_NAME")
            echo "✅ main.py is running"
            echo "📋 Process ID: $PID"
            echo "⏰ Started: $(ps -o lstart= -p $PID)"
            echo "💾 Memory usage: $(ps -o %mem= -p $PID | xargs)%"
            echo "⚡ CPU usage: $(ps -o %cpu= -p $PID | xargs)%"
        else
            echo "❌ main.py is not running"
        fi
        ;;
        
    logs)
        echo "📜 Showing recent logs from $LOG_FILE:"
        echo "----------------------------------------"
        if [ -f "$LOG_FILE" ]; then
            tail -50 "$LOG_FILE"
        else
            echo "❌ Log file not found: $LOG_FILE"
        fi
        ;;
        
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start main.py in background"
        echo "  stop    - Stop running main.py process"
        echo "  restart - Stop and start main.py"
        echo "  status  - Check if main.py is running"
        echo "  logs    - Show recent application logs"
        exit 1
        ;;
esac