#!/bin/bash
# Log Monitor - Helper Script
# Wrapper for init.sh to simplify command execution

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR" || exit 1

case "$1" in
  start)
    sudo bash init.sh start
    ;;
  stop)
    sudo bash init.sh stop
    ;;
  view)
    bash init.sh view
    ;;
  restart)
    sudo bash init.sh restart
    ;;
  status)
    bash init.sh status
    ;;
  logs)
    bash init.sh logs
    ;;
  firewall-logs)
    bash init.sh firewall-logs
    ;;
  threats)
    bash init.sh threats
    ;;
  *)
    echo "🛡️ Log Monitor Control Script"
    echo ""
    echo "Usage: bash run.sh {command}"
    echo ""
    echo "Commands:"
    echo "  start           - Start Log monitoring and firewall blocker"
    echo "  stop            - Stop all services"
    echo "  restart         - Restart services"
    echo "  status          - Check service status"
    echo "  view            - Launch threat visualization"
    echo "  logs            - View main service logs"
    echo "  firewall-logs   - View firewall action logs"
    echo "  threats         - View recent threats"
    echo ""
    echo "Examples:"
    echo "  bash run.sh start"
    echo "  bash run.sh status"
    echo "  bash run.sh logs"
    ;;
esac
