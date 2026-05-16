# log_monitoring,alerting_and_banning

This repository contains a GitHub-ready copy of the `log_monitring_and_alerting.py` script for real-time SSH log monitoring, alerting, and banning. for real-time SSH authentication log monitoring, automatic threat logging, firewall blocking, and email alerts.

> Note: The script in this repository uses environment variables for email credentials so your real Gmail addresses are hidden from GitHub. The original project folder remains unchanged.

## Features

- Real-time monitoring of `/var/log/auth.log` for SSH authentication issues
- Detects brute-force login attempts, PAM failures, lockouts, and suspicious IP activity
- Automatically writes detected threat summaries to `threat_ip.log`
- Logs detected IPs to `ips_detected.log`
- Sends email alerts via SMTP when a threat threshold is reached
- Uses `firewall-cmd` rich rules to block suspicious IP addresses
- Simple setup and extension points for future monitoring rules

## Setup

1. Copy `log_monitring_and_alerting.py` to your target host.
2. Install Python 3 and required packages (standard library only).
3. Ensure the script has permission to read `/var/log/auth.log` and run `firewall-cmd`.
4. Set email credentials using environment variables:

   ```bash
   export ALERT_EMAIL_SENDER="your_sender@example.com"
   export ALERT_EMAIL_PASSWORD="your_email_app_password"
   export ALERT_EMAIL_RECIPIENT="your_recipient@example.com"
   ```

5. Run the script:

   ```bash
   python3 log_monitring_and_alerting.py
   ```

## Recommended GitHub upload

- Repository name: `log_monitoring,alerting_and_banning`
- Only tracked files: `log_monitring_and_alerting.py` and `README.md`
- Keep all real credentials out of source control

## Future plans

- Add a configuration file for log paths, thresholds, and alert rules
- Support multiple log sources, including `secure`, `syslog`, and custom audit logs
- Add a whitelist for trusted IPs and network ranges
- Implement asynchronous email sending and retry logic
- Add Docker support for containerized deployment
- Add a simple web dashboard or Slack/Telegram alert integration

## Notes

- The original project folder still contains your current script and settings.
- This repo copy is designed to be safe for GitHub by using placeholder credentials and environment-based email configuration.
