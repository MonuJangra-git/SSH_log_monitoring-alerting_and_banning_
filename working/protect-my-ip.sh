#!/bin/bash
set -euo pipefail

SERVICE="ssh"        # Leave empty to allow all traffic
PRIORITY="-1"

if [[ $EUID -ne 0 ]]; then
    echo "Run as root: sudo $0" >&2
    exit 1
fi

systemctl is-active --quiet firewalld || { echo "firewalld not running"; exit 1; }

# 1. Collect all local IPv4 addresses (excluding loopback)
mapfile -t local_ips < <(ip -4 -o addr show | awk '{print $4}' | cut -d'/' -f1 | grep -v '^127\.')

# 2. Also try to get public IP (in case no local private IP is found)
public_ip=""
if command -v curl >/dev/null; then
    for svc in "https://api.ipify.org" "https://ifconfig.me" "https://icanhazip.com"; do
        if public_ip=$(curl -4 -s --max-time 5 "$svc"); then
            break
        fi
    done
fi

# Combine and remove duplicates
ips=("${local_ips[@]}")
if [[ -n "$public_ip" ]] && [[ ! " ${ips[*]} " =~ " $public_ip " ]]; then
    ips+=("$public_ip")
fi

if [[ ${#ips[@]} -eq 0 ]]; then
    echo "No IP addresses found." >&2
    exit 1
fi

for ip in "${ips[@]}"; do
    echo "Processing IP: $ip"
    # Remove any old rule for this IP (to avoid duplicates)
    old_rule=$(firewall-cmd --permanent --list-rich-rules | grep "source address=\"$ip\"" || true)
    if [[ -n "$old_rule" ]]; then
        firewall-cmd --permanent --remove-rich-rule="$old_rule"
    fi

    # Build new rule
    if [[ -n "$SERVICE" ]]; then
        rule="rule family=\"ipv4\" source address=\"$ip\" service name=\"$SERVICE\" accept priority=\"$PRIORITY\""
    else
        rule="rule family=\"ipv4\" source address=\"$ip\" accept priority=\"$PRIORITY\""
    fi

    firewall-cmd --permanent --add-rich-rule="$rule"
done

firewall-cmd --reload
echo "Done."