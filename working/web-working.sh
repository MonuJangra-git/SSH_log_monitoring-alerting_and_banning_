#!/bin/bash

set -u

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR" || exit 1

PORT="${PORT:-8080}"

if [[ "$(id -u)" -ne 0 ]]; then
    if ! command -v sudo >/dev/null 2>&1; then
        echo "sudo is required so dashboard controls can manage the monitoring services."
        exit 1
    fi
    exec sudo -E "$0" "$@"
fi

bind_host="127.0.0.1"
read -r -p "Serve the dashboard on another local IP? [y/N]: " expose

if [[ "$expose" == "y" || "$expose" == "Y" ]]; then
    read -r -p "Enter the local IP to allow on port $PORT: " allowed_ip
    if [[ ! "$allowed_ip" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]]; then
        echo "Invalid IPv4 address."
        exit 1
    fi

    IFS='.' read -r octet1 octet2 octet3 octet4 <<< "$allowed_ip"
    for octet in "$octet1" "$octet2" "$octet3" "$octet4"; do
        if (( octet > 255 )); then
            echo "Invalid IPv4 address."
            exit 1
        fi
    done

    if ! command -v firewall-cmd >/dev/null 2>&1; then
        echo "firewall-cmd is required for external dashboard access."
        exit 1
    fi

    rule="rule family=\"ipv4\" source address=\"$allowed_ip\" port port=\"$PORT\" protocol=\"tcp\" accept"
    if ! firewall-cmd --permanent --add-rich-rule="$rule"; then
        echo "Failed to add firewall rule for $allowed_ip:$PORT."
        exit 1
    fi
    if ! firewall-cmd --reload; then
        echo "Failed to reload firewalld."
        exit 1
    fi
    bind_host="0.0.0.0"
    echo "Dashboard access allowed from $allowed_ip:$PORT and localhost."
else
    echo "Dashboard will be available on localhost only."
fi

export DASHBOARD_BIND_HOST="$bind_host"
export PORT
exec python3 visualize_web.py
