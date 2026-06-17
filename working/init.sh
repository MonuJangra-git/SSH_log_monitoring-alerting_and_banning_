#!/bin/bash
root=$(id -u)
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR" || exit 1
if [[ ${root} != 0 ]]; then
    echo "❌ User must be logged in as root"
    echo "Exiting..............."
    exit 
fi


case "$1" in
    start)
        echo "🔍 Checking firewall status..."
        # ensure we run the setup script from this directory
        python3 ./firewall-auto-setup.py || true
        echo "▶️  Starting services..."

        # start main.py if not already running
        if pgrep -f main.py > /dev/null; then
            echo "✓ main.py already running."
        else
            nohup python3 main.py > analysis_output/main.log 2>&1 &
            echo $! > analysis_output/main.pid
            echo "✓ main.py started (PID: $!)"
        fi

        # start firewall blocker if not already running
        if pgrep -f firewall_auto_ip_blocker.py > /dev/null; then
            echo "✓ firewall_auto_ip_blocker.py already running."
        else
            nohup python3 firewall_auto_ip_blocker.py > analysis_output/firewall.log 2>&1 &
            echo $! > analysis_output/firewall.pid
            echo "✓ firewall_auto_ip_blocker.py started (PID: $!)"
        fi

        echo "======================================"
        echo "🛡️  MJ-IPguard is active!"
        echo "Do your work without distraction"
        echo "======================================"
        ;;

    stop)
        echo "⏹️  Stopping services..."

        if [ -f analysis_output/main.pid ]; then
            kill $(cat analysis_output/main.pid) 2>/dev/null
            rm -f analysis_output/main.pid
            echo "✓ main.py stopped."
        else
            echo "ℹ️  main.py not running."
        fi

        if [ -f analysis_output/firewall.pid ]; then
            kill $(cat analysis_output/firewall.pid) 2>/dev/null
            rm -f analysis_output/firewall.pid
            echo "✓ firewall_auto_ip_blocker.py stopped."
        else
            echo "ℹ️  firewall_auto_ip_blocker.py not running."
        fi

        echo "👋 Thanks for using MJ-IPguard!"
        ;;

    restart)
        echo "🔄 IPguard is restarting..."
        $0 stop
        sleep 2
        $0 start
        ;;

    status)
        echo " Checking service status..."
        pgrep -f main.py > /dev/null && echo "✓ main.py is running." || echo "✗ main.py is NOT running."
        pgrep -f firewall_auto_ip_blocker.py > /dev/null && echo "✓ firewall_auto_ip_blocker.py is running." || echo "✗ firewall_auto_ip_blocker.py is NOT running."
        ;;
    view)
        echo " Starting threat visualization..."
        python3 visualize_threats.py
        ;;

    logs)
        echo " Main service logs:"
        tail -f analysis_output/main.log
        ;;

    firewall-logs)
        echo " Firewall action logs:"
        tail -f analysis_output/firewall_rules.log
        ;;

    threats)
        echo "🚨 Recent threats detected:"
        tail -20 analysis_output/threat_ip.log
        ;;

esac

echo "======================================"
echo "👤 Author: Monu Jangra"
echo "📍 GitHub: MonuJangra-git"
echo "💼 LinkedIn: Monu Jangra"
echo "⭐ Star this project on GitHub!"
echo "======================================"
