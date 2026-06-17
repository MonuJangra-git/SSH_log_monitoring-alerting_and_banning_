# v1.5 - SSH Log Monitoring and Alerting System

## Features
- Real-time SSH log monitoring from /var/log/auth.log
- Automatic threat detection using regex patterns
- Email alerting on suspicious activity
- Automated firewall IP blocking
- JSON-based threat reporting

## Setup

1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Configure environment variables in .env file
4. Run: `python main.py`

## Configuration

Set environment variables in .env:
- ALERT_EMAIL_SENDER: Gmail sender address
- ALERT_EMAIL_PASSWORD: Gmail app-specific password
- ALERT_EMAIL_RECIPIENT: Alert recipient email
- LOG_FILE_PATH: Path to SSH log file (default: /var/log/auth.log)

## Output
- analysis_output/threat_ip.log: Detected threats summary
- analysis_output/threat_ip.json: Threat data in JSON format
- analysis_output/ips_detected.txt: List of detected IPs
- analysis_output/firewall_rules.log: Firewall blocking log
- analysis_output/output.log: Main application log
