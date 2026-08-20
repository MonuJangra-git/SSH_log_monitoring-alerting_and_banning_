#!/bin/bash
# MJ-IPguard — Interactive Control Menu

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR" || exit 1

echo ""
echo "======================================================"
echo "        🛡️  MJ-IPguard — SSH Attack Defense"
echo "======================================================"
echo ""
echo "  1)  Start          — Setup firewall & start all services"
echo "  2)  Stop           — Stop all running services"
echo "  3)  Restart        — Restart all services"
echo "  4)  Status         — Check if services are running"
echo "  5)  Web Dashboard  — Live threat chart at http://localhost:8080"
echo "  6)  Terminal Chart — Live threat chart in terminal window"
echo "  7)  Live Logs      — Stream main service logs (Ctrl+C to exit)"
echo "  8)  Firewall Logs  — Stream firewall action logs (Ctrl+C to exit)"
echo "  9)  Recent Threats — Show last 20 detected threats"
echo "  0)  Exit"
echo ""
read -r -p "Choose an option [0-9]: " choice
echo ""

case "$choice" in
    1)
        sudo bash init.sh start
        ;;
    2)
        sudo bash init.sh stop
        ;;
    3)
        sudo bash init.sh restart
        ;;
    4)
        bash init.sh status
        ;;
    5)
        echo "🌐 Starting web dashboard..."
        echo "   Open http://localhost:8080 in your browser"
        echo "   Press Ctrl+C to stop"
        echo ""
        python3 visualize_web.py
        ;;
    6)
        echo "📊 Starting terminal chart..."
        echo "   Press Ctrl+C to stop"
        echo ""
        python3 visualize_threats.py
        ;;
    7)
        echo "📄 Streaming main service logs (Ctrl+C to exit)..."
        echo ""
        tail -f analysis_output/main.log
        ;;
    8)
        echo "🔥 Streaming firewall action logs (Ctrl+C to exit)..."
        echo ""
        tail -f analysis_output/firewall_rules.log
        ;;
    9)
        echo "🚨 Recent threats detected:"
        echo ""
        tail -20 analysis_output/threat_ip.log
        ;;
    0)
        echo "👋 Exiting MJ-IPguard menu."
        ;;
    *)
        echo "❌ Invalid option. Please run 'bash run.sh' and choose 0-9."
        exit 1
        ;;
esac

echo ""
echo "======================================================"
echo "👤 Author: Monu Jangra"
echo "📍 GitHub: MonuJangra-git"
echo "💼 LinkedIn: Monu Jangra"
echo "⭐ Star this project on GitHub!"
echo "======================================================"
