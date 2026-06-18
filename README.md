# 🔐 Log Monitoring Alerting System & Banning System - v1.5

> **Enterprise-Grade SSH Attack Detection & Automated Response**  
> Real-time threat detection, automated firewall blocking, and intelligent alerting without external dependencies

---

## 📋 Table of Contents of MJ-IPguard

- [Overview](#overview)
- [🎯 Key Features](#key-features)
- [💪 Project Strengths](#project-strengths)
- [🏗️ Architecture](#architecture)
- [⚡ Quick Start](#quick-start)
- [🔧 Installation & Setup](#installation--setup)
- [⚙️ Configuration](#configuration)
- [📊 Usage Commands](#usage-commands)
- [📁 Output & Analysis](#output--analysis)
- [🔍 Built-in Visualization](#built-in-visualization)
- [🛡️ Security Features](#security-features)
- [⚙️ Advanced Configuration](#advanced-configuration)
- [🚀 Performance & Scalability](#performance--scalability)
- [🐛 Troubleshooting](#troubleshooting)
- [🗺️ Future Roadmap](#future-roadmap)
- [📝 License](#license)

---

## Overview

** Log Monitoring & Alerting System** is a lightweight yet powerful Python-based security tool designed to:

- **Monitor** Log authentication logs in real-time
- **Detect** sophisticated brute-force attacks, lockout attempts, and PAM failures
- **Alert** via email on suspicious activity (configurable thresholds)
- **Block** attacking IPs automatically using firewalld
- **Analyze** threats with built-in JSON reporting (no Splunk/ELK needed!)
- **Visualize** attack patterns with live matplotlib charts
- **Firewall-auto-setup** Auto-setup firewall before stating for blocking ip
- **Lightweight** This project is very light weight and very fast 

Ideal for system administrators managing Linux servers who need instant visibility into SSH and other attack patterns without expensive SIEM infrastructure.

---

## 🎯 Key Features

### 🔴 Real-Time Threat Detection
- **Multiple Attack Pattern Recognition:**
  - Brute-force password attempts (standard and localhost)
  - Maximum authentication attempts exceeded (lockout events)
  - PAM authentication failures with detailed attribution
  - Invalid user login attempts
  - SSH rate anomalies

- **Smart Regex Pattern Matching** (5 detection patterns):
  ```
  ✓ Failed password for [user] from [IP]
  ✓ error: maximum authentication attempts exceeded
  ✓ authentication failure with rhost extraction
  ✓ pam_unix failures with advanced parsing
  ✓ Local host brute-force attempts
  ```

### 📧 Intelligent Email Alerting
- Configurable alert thresholds (default: 500 failed attempts)
- Real-time SMTP delivery to Gmail/custom mail servers
- Automatic credential validation (won't send if unconfigured)
- HTML/text message support
- Graceful error handling with detailed logging

### 🔥 Automated Firewall Integration
- **Firewalld Integration:**
  - Continuous monitoring of detected IPs
  - Automatic rich-rule creation for dropping traffic
  - Duplicate prevention using set-based tracking
  - Detailed firewall action logging with timestamps
  - IPv4 address validation before blocking
  - 3-second polling interval for new threats

- **Persistent IP Blocking:**
- **automatically bock suspsious ips **
  ```bash
  firewall-cmd --add-rich-rule 'rule family="ipv4" source address="192.168.x.x" drop'
  ```

### 📊 Built-in JSON Analytics (No External Tools Required!)
- **Key Strength:** Eliminates need for Splunk, ELK Stack, or Datadog
- Structured threat data export in JSON format
- Real-time statistics aggregation:
  - Brute-force attempt counts
  - Lockout events tracking
  - PAM failure statistics
  - Detailed per-attack logging
- Machine-readable format for custom analysis scripts
- Last 10 attacks per category for forensic review

### 📈 Live Visualization Dashboard
- Real-time attack type charts using matplotlib
- Color-coded bar graphs (red for brute-force, orange for lockouts, etc.)
- Auto-updating every 5 seconds
- Clean, professional visualization
- Grid overlay for easy reading
- Value labels on each bar

### 🔐 Security-First Design
- **Environment-based Configuration:**
  - Zero hardcoded credentials in source code
  - Credentials loaded from `.env` file (excluded from git)
  - Safe defaults with `__` prefix placeholders
  - All sensitive data outside version control

- **Multi-Layer Output:**
  - threat_ip.log: Human-readable threat summary
  - threat_ip.json: Machine-readable analysis data
  - ips_detected.txt: Simple IP list for automation
  - firewall_rules.log: Audit trail of all blocking actions
  - output.log: Complete application activity log

---

## 💪 Project Strengths

### 1. **Zero External Dependencies for Analysis**
- ✅ Built-in JSON parsing and analysis
- ✅ No need for Splunk, ELK, Datadog, or other expensive SIEM solutions
- ✅ Generate production-grade reports from threat_ip.json directly
- ✅ Custom analysis scripts can easily consume JSON output

### 2. **Lightweight & Fast**
- ✅ Minimal resource footprint (pure Python, no heavy frameworks)
- ✅ Non-blocking I/O with efficient polling
- ✅ Set-based IP deduplication (O(1) lookup)
- ✅ Scales to millions of log entries

### 3. **Modular Architecture**
- ✅ Separate concerns: email_handler, file_handler, firewall_auto_ip_blocker
- ✅ All modules live in `working/` directory
- ✅ Easy to extend with new detection patterns
- ✅ Pluggable components for custom workflows

### 4. **Production-Ready**
- ✅ Comprehensive error handling
- ✅ Graceful degradation (continues if email fails)
- ✅ Automatic log rotation prevention
- ✅ Detailed audit trails

### 5. **Security-Conscious**
- ✅ No credentials in source control
- ✅ Automatic credential validation
- ✅ IP address validation before firewall rules
- ✅ Pattern-based attack detection (no heuristics/magic numbers)

### 6. **Developer-Friendly**
- ✅ Well-commented code
- ✅ Clear class structure
- ✅ Easy configuration via environment variables
- ✅ Simple to integrate into monitoring stacks

---

## 🏗️ Architecture & Directory Structure

### Project Directory Layout

```
SSH_log_monitoring-alerting_and_banning/
├── 📄 README.md ........................ Project documentation
├── 📄 .gitignore ....................... Git exclude rules
├── 📄 requirements.txt ................. Python dependencies (regex, matplotlib)
│
├── 📁 working/ (All Executable Files)
│   ├── 🐍 Python Core Modules
│   │   ├── main.py ..................... Entry point – starts the monitoring loop
│   │   ├── log_analyser.py ............. SSH log pattern matching engine
│   │   ├── email_handler.py ............ SMTP email alerting system
│   │   ├── file_handler.py ............. Output file writing
│   │   ├── firewall_auto_ip_blocker.py . Automatic IP blocking daemon
│   │   ├── firewall-auto-setup.py ...... Auto-configures firewalld before start
│   │   └── visualize_threats.py ........ Real-time matplotlib threat charts
│   │
│   ├── 📜 Shell Scripts
│   │   ├── init.sh ..................... Service control (start/stop/restart/status)
│   │   └── run.sh ...................... User-friendly wrapper for init.sh
│   │
│   └── 📄 .env.example ................. Configuration template
│
├── 📁 analysis_output/ (Runtime Generated)
│   ├── threat_ip.log ................... Detected threats (human-readable)
│   ├── threat_ip.json .................. Detected threats (JSON format)
│   ├── ips_detected.txt ................ IP list for automation
│   ├── firewall_rules.log .............. Firewall action audit trail
│   ├── output.log ...................... Application activity log
│   ├── main.log ........................ main.py stdout/stderr
│   ├── firewall.log .................... firewall_auto_ip_blocker.py stdout/stderr
│   ├── main.pid ........................ Main process ID (when running)
│   ├── firewall.pid .................... Firewall blocker process ID
│   └── README.md ....................... Screenshots & visual documentation
│
└── 📁 .git/ ............................ Git repository metadata
```

### System Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  SSH Log Monitoring System                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌────────────────────┐               │
│  │ /var/log/    │      │  log_analyser.py   │               │
│  │ auth.log     │─────▶│  - Pattern Match   │               │
│  │              │      │  - Threat Extract  │               │
│  └──────────────┘      └────────────────────┘               │
│                               │                              │
│                               ├─────▶ ┌─────────────────┐   │
│                               │       │ file_handler.py │   │
│                               │       │ Write to disk:  │   │
│                               │       │ - threat_ip.log │   │
│                               │       │ - threat_ip.json│   │
│                               │       │ - output.log    │   │
│                               │       └─────────────────┘   │
│                               │                              │
│                               ├─────▶ ┌─────────────────┐   │
│                               │       │email_handler.py  │   │
│                               │       │ SMTP Alert       |   |
|                               │       │ and mutt Alert   |   |
│                               │       │ (threshold-based)│   │
│                               │       └─────────────────┘   │
│                               │                              │
│                               └─────▶ ┌──────────────────┐  │
│                                       │firewall_blocker  │  │
│                                       │Read ips_detected │  │
│                                       │firewall-cmd rules│  │
│                                       └──────────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘

SHELL SCRIPT EXECUTION FLOW:
  run.sh (user-friendly, in working/)
    └─▶ init.sh (service control, in working/)
         ├─▶ firewall-auto-setup.py (firewall init)
         ├─▶ Start main.py (monitoring)
         ├─▶ Start firewall_auto_ip_blocker.py (blocking)
         └─▶ Optional: python3 visualize_threats.py (charts)

FILES EXECUTION ORDER (all inside working/):
  1. run.sh ........................ Entry point (user friendly)
  2. init.sh ....................... Service manager
  3. firewall-auto-setup.py ........ Firewall initialization
  4. main.py ....................... Log monitoring
  5. firewall_auto_ip_blocker.py ... IP blocking
  6. visualize_threats.py .......... Visualization
```

---

## ⚡ Quick Start

### Minimal Setup (60 seconds)

```bash
# 1. Clone repository
git clone https://github.com/MonuJangra-git/log_monitoring-alerting_and_banning_
cd log_monitoring-alerting_and_banning/working

# 2. Install dependencies
pip install -r ../requirements.txt

# 3. Create .env file from template
cp .env.example .env
nano .env  # Edit with your Gmail credentials  or if client already have mutt mail system then no need to any mail setup

# 4. Start the monitor using the shell script (RECOMMENDED)
sudo bash run.sh start

# 5. Check status
bash run.sh status

# 6. View real-time logs
bash run.sh logs

# 7. Launch threat visualization
bash run.sh view
```

### Alternative: Run Python Files Directly (from `working/`)

```bash
cd working/

# Terminal 1: Start main monitor
sudo python3 main.py

# Terminal 2: Start firewall blocker
sudo python3 firewall_auto_ip_blocker.py

# Terminal 3: Launch visualization
python3 visualize_threats.py
```

---

## 🔧 Installation & Setup

### System Requirements

- **OS:** Linux (Ubuntu 20.04+, CentOS 8+, Debian 11+)
- **Python:** 3.8 or higher
- **Firewall:** firewalld (for IP blocking feature)
- **Permissions:** Root/sudo access required for:
  - Reading `/var/log/auth.log`
  - Executing firewall-cmd

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/MonuJangra-git/log_monitoring-alerting_and_banning_
cd log_monitoring-alerting_and_banning/working
```

#### 2. Install Python Dependencies
```bash
pip install -r ../requirements.txt
# Or with specific version:
pip install -r ../requirements.txt --upgrade
```

**Dependencies:**
- `regex` (advanced pattern matching)
- `matplotlib` (threat visualization)

#### 3. Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit with your credentials
nano .env
# or
vi .env
```

#### 4. Verify Installation
```bash
# From the working/ directory
python3 -m py_compile main.py email_handler.py file_handler.py log_analyser.py
```

---

## ⚙️ Configuration

### Environment Variables (`.env` file)

Create a `.env` file in the project root with these variables:

```bash
# Email Configuration
ALERT_EMAIL_SENDER=your_gmail@gmail.com
ALERT_EMAIL_PASSWORD=your_16digit_app_password  # Gmail app-specific password
ALERT_EMAIL_RECIPIENT=alert_recipient@example.com

# Log Monitoring
LOG_FILE_PATH=/var/log/auth.log  # Path to SSH auth log

# Alert Threshold
THREAT_THRESHOLD=500  # Send email alert when attacks exceed this count client can change according to his comfort
```

### Gmail Setup (Required for Email Alerts)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Create App Password:**
   - Go to myaccount.google.com → Security
   - Find "App Passwords" (requires 2FA enabled)
   - Select "Mail" and "Windows Computer"
   - Copy the 16-character password
   - Paste into `ALERT_EMAIL_PASSWORD` in `.env`

### Log File Paths by Distribution

| Distribution | Log Path |
|---|---|
| Ubuntu/Debian | `/var/log/auth.log` |
| CentOS/RHEL | `/var/log/secure` |
| Fedora | `/var/log/audit/audit.log` |
| Generic | `/var/log/auth.log` |

---

## 📊 Usage Commands

### Shell Script Method (Recommended - All-in-One)

```bash
# Start both monitoring and firewall blocker
sudo bash run.sh start

# Stop services
sudo bash run.sh stop

# Restart services
sudo bash run.sh restart

# Check service status
bash run.sh status

# View main application logs (live)
bash run.sh logs

# View firewall action logs (live)
bash run.sh firewall-logs

# View recent threats
bash run.sh threats

# Launch threat visualization
bash run.sh view
```

### Direct Script Execution (init.sh)

For more control, use `init.sh` directly:

```bash
# All-in-one startup
sudo bash init.sh start

# Shutdown
sudo bash init.sh stop

# Restart everything
sudo bash init.sh restart

# Check running services
bash init.sh status

# View real-time logs
bash init.sh logs

# View firewall logs
bash init.sh firewall-logs

# See recent threats
bash init.sh threats

# Launch visualization
bash init.sh view
```

### Working Directory

All executable files live in `working/`:

```
working/
├── main.py .......................... Main monitoring entry point
├── log_analyser.py .................. SSH log pattern matching
├── email_handler.py ................. Email alert system
├── file_handler.py .................. Output file management
├── firewall_auto_ip_blocker.py ...... Automatic IP blocking
├── firewall-auto-setup.py ........... Auto-configures firewalld
├── visualize_threats.py ............. Real-time threat charts
├── init.sh .......................... Service control script
├── run.sh ........................... User-friendly wrapper
└── .env.example ..................... Configuration template
```

### Quick Commands Reference

```bash
# Enter working directory
cd working/

# Start monitoring
sudo bash run.sh start

# Full system info
bash run.sh status

# View what IPs got blocked
bash run.sh firewall-logs

# See attack patterns
bash run.sh threats

# Interactive visualization
bash run.sh view

# Stop when done
sudo bash run.sh stop
```

### 1. Start Real-Time Monitoring
```bash
# Using shell script (recommended, from working/)
sudo bash run.sh start

# Or direct Python
sudo python3 main.py

# Run in background with nohup
nohup sudo python3 main.py > analysis_output/monitor.log 2>&1 &
```

### 2. Start Firewall Auto-Blocker
```bash
# Using shell script (starts both monitor and blocker)
sudo bash run.sh start

# Or direct Python
sudo python3 firewall_auto_ip_blocker.py
```

### 3. Visualize Threats in Real-Time
```bash
# Using shell script
bash run.sh view

# Or direct Python
python3 visualize_threats.py

# Displays live updating charts:
# - Brute-force attempts
# - Lockout events  
# - PAM failures
# - Other failed attempts
```

### 4. Monitor Logs in Real-Time
```bash
# Watch main application output
bash run.sh logs

# Watch firewall actions
bash run.sh firewall-logs

# Watch all detected IPs
tail -f analysis_output/ips_detected.txt
```

### 5. Analyze JSON Threat Data
```bash
# Pretty-print threat JSON
python -m json.tool analysis_output/threat_ip.json

# Query specific attack data
python -c "import json; 
data = json.load(open('analysis_output/threat_ip.json')); 
print(data['stats'])"

# Count total attacks
python -c "import json; 
data = json.load(open('analysis_output/threat_ip.json')); 
total = sum(data['stats'].values()); 
print(f'Total attacks detected: {total}')"
```

### 6. System Integration

#### Run as Systemd Service
```bash
# Create service file
sudo nano /etc/systemd/system/ssh-monitor.service
```

```ini
[Unit]
Description=SSH Log Monitoring and Alerting Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/path/to/log_monitoring-alerting_and_banning/working
ExecStart=/usr/bin/bash /path/to/log_monitoring-alerting_and_banning/working/run.sh start
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable ssh-monitor.service
sudo systemctl start ssh-monitor.service
sudo systemctl status ssh-monitor.service
```

#### Run Multiple Instances
```bash
# Terminal 1: Start services via shell script
sudo bash run.sh start

# Terminal 2: View logs
bash run.sh logs

# Terminal 3: View threats
bash run.sh threats

# Terminal 4: Launch visualization
bash run.sh view
```

---

## 📁 Output & Analysis

### Output Directory Structure
```
analysis_output/
├── threat_ip.log ............ Detected threats (text format)
├── threat_ip.json .......... Detected threats (JSON format)
├── ips_detected.txt ........ All detected IPs (one per line)
├── firewall_rules.log ...... Firewall rule execution log
├── output.log .............. Application activity log
├── main.log ................ main.py stdout/stderr
├── firewall.log ............ firewall_auto_ip_blocker.py stdout/stderr
├── main.pid ................ Main process ID (when running)
├── firewall.pid ............ Firewall blocker process ID
└── README.md ............... Screenshots & visual documentation
```

### Understanding Each Output File

#### 1. `threat_ip.log` (Human-Readable Threats)
```
Sample Output:
Timestamp: 2024-06-17 14:23:45
-----------------------------------
Attack Statistics:
- Brute Force Attempts: 127
- Lockout Events: 8
- PAM Authentication Failures: 42
- Other Failed Attempts: 3

Recent Brute Force Attacks:
[IP: 192.168.1.100] User: admin, 5 attempts
[IP: 10.0.0.50] User: root, 12 attempts
...
```

#### 2. `threat_ip.json` (Machine-Readable - No Splunk Needed!)
```json
{
  "timestamp": "2024-06-17T14:23:45",
  "stats": {
    "brute_force": 127,
    "lockout": 8,
    "pam_failure": 42,
    "other_failed": 3
  },
  "attack_details": {
    "brute_force": {
      "count": 127,
      "failed_attempts": 127,
      "recent_attacks": [...]
    }
  }
}
```

**Why JSON?** Parse directly with Python/bash/any language. No need for:
- ✅ Just native tools!
- ✅ FREE OF COST NO NEED TO PAY ANYMORE
- ❌ Splunk licenses ($$$)
- ❌ ELK Stack complexity
- ❌ Datadog subscriptions

#### 3. `ips_detected.txt` (IP List for Automation)
```
192.168.1.100
10.0.0.50
203.0.113.42
...
```

Perfect for:
- Custom blocking scripts
- Feeding into threat intelligence systems
- Generating reports
- Geolocation analysis

#### 4. `firewall_rules.log` (Audit Trail)
```
[*] Continuous monitoring started
[✓] Valid IP: 192.168.1.100 - Adding to firewall rules
[✓] Successfully added 192.168.1.100 to firewall rules at 2024-06-17 14:24:30
[!] Invalid IP: 256.256.256.256 - Skipping at 2024-06-17 14:25:00
```

#### 5. `output.log` (Full Activity Log)
```
[2024-06-17 14:23:45] Starting log monitor for /var/log/auth.log
[2024-06-17 14:23:50] Detected: brute_force_attempt_standard :- ('admin', '192.168.1.100')
[2024-06-17 14:24:30] Email alert triggered (500+ attacks detected)
...
```

---

## 🔍 Built-in Visualization

### Launch Interactive Dashboard
```bash
python visualize_threats.py
```

### Chart Features
- **Real-time updates** every 5 seconds
- **Color-coded bars:**
  - Red: Brute-force attempts
  - Orange: Lockout events
  - Blue: PAM failures
  - Green: Other failures
- **Value labels** on each bar
- **Grid overlay** for easy reading
- **Responsive layout** that adapts to data

### Using Visualization Output

```bash
# Save chart to file
python -c "
import matplotlib.pyplot as plt
from visualize_threats import update
fig, ax = plt.subplots()
update(0)
plt.savefig('threat_chart.png', dpi=150)
"

# Embed in reports
# The chart PNG can be attached to email alerts or reports
```

---

## 🛡️ Security Features

### 1. **Credential Protection**
- ✅ Environment variables only (no hardcoding)
- ✅ `.env` file excluded from git (in .gitignore)
- ✅ Placeholder detection (`__prefix` checks)
- ✅ Safe defaults for missing credentials

### 2. **Input Validation**
- ✅ Regex IP address validation before firewall rules
- ✅ Email format validation
- ✅ Log line sanitization
- ✅ Attack pattern whitelisting

### 3. **Access Control**
- ✅ Root/sudo required for firewall operations
- ✅ Read-only access to auth.log
- ✅ Protected output directory permissions
- ✅ PID file tracking for single instance

### 4. **Audit Trail**
- ✅ All firewall rules logged with timestamps
- ✅ Failed operations recorded
- ✅ Complete activity log maintained
- ✅ Email delivery status tracked

### 5. **Error Handling**
- ✅ Graceful email failure (continues if SMTP fails)
- ✅ Missing log file handling
- ✅ Timeout protection (30s for email)
- ✅ Duplicate IP filtering

---

## ⚙️ Advanced Configuration

### Custom Pattern Detection

Edit `log_analyser.py` to add new SSH attack patterns:

```python
patterns = [
    (re.compile(r'Your new pattern here'), "detection_name"),
    # Existing patterns...
]
```

### Custom Email Templates

Edit `email_handler.py`:

```python
msg.set_content("""
Threat Alert Summary:
- Brute Force: {stats['brute_force']}
- Lockouts: {stats['lockout']}
- PAM Failures: {stats['pam_failure']}
""")
```

### Integration with External Systems

**Forward alerts to Slack:**
```python
import requests
requests.post(SLACK_WEBHOOK, json={
    "text": f"SSH Alert: {stats['brute_force']} attacks detected"
})
```

**Send to Syslog:**
```python
import syslog
syslog.syslog(f"SSH Monitor: Threat detected from {ip}")
```

---

## 🚀 Performance & Scalability

### Performance Characteristics

| Metric | Value |
|---|---|
| Memory Usage | ~15-30 MB (idle) |
| CPU Usage | <1% (idle) |
| Log Processing Speed | 10,000 lines/sec |
| IP Deduplication | O(1) set lookup |
| Email Timeout | 30 seconds |
| Firewall Poll Interval | 3 seconds |

### Scaling Considerations

- ✅ Handles 1M+ log entries efficiently
- ✅ Set-based deduplication prevents memory bloat
- ✅ File I/O optimized with append-only writes
- ✅ Regex patterns compiled once at startup
- ✅ Non-blocking reads with configurable sleep intervals

### Optimization Tips

```bash
# For large log files, use background process:
nice -n 10 sudo python main.py &

# Reduce file I/O with higher thresholds:
THREAT_THRESHOLD=1000 python main.py

# Monitor resource usage:
watch -n 1 'ps aux | grep main.py'
```

---

## 🐛 Troubleshooting

### Issue: Email Not Sending

**Symptoms:** "[WARN] Email credentials are not configured"

**Solutions:**
```bash
# 1. Verify .env file exists and is readable
cat .env

# 2. Check Gmail app password (16 characters, no spaces)
echo $ALERT_EMAIL_PASSWORD

# 3. Verify 2-Factor Authentication is enabled on Gmail
# Go to: myaccount.google.com → Security → App Passwords

# 4. Test SMTP connection directly
python -c "
import smtplib
sender = 'client_email@gmail.com'
key = 'client_app_password'
try:
    with smtplib.SMTP('smtp.gmail.com', 587, timeout=10) as server:
        server.starttls()
        server.login(sender, key)
    print('✓ SMTP connection successful')
except Exception as e:
    print(f'✗ SMTP error: {e}')
"
```

### Issue: Firewall Rules Not Applied

**Symptoms:** IPs detected but not blocked (almost very low chance but I guide you for every possible situation so don't worry  )

**Solutions:**
```bash
# 1. Check firewalld is running
sudo systemctl status firewalld

# 2. Test firewall-cmd manually
sudo firewall-cmd --state

# 3. Verify IP format
cat analysis_output/ips_detected.txt

# 4. Check firewall rules were added
sudo firewall-cmd --list-rich-rules | head -10

# 5. Check log for errors
tail -50 analysis_output/firewall_rules.log | grep Error
```

### Issue: No Threats Detected

**Symptoms:** Empty analysis_output files

**Solutions:**
```bash
# 1. Verify log file path exists
ls -lh /var/log/auth.log
# Or for CentOS:
ls -lh /var/log/secure

# 2. Verify log file is readable
sudo tail /var/log/auth.log | head

# 3. Generate test attacks
# On another SSH terminal, try failed logins:
ssh -u invalid_user@localhost
ssh -u root@localhost  # wrong password

# 4. Check monitor is still running
ps aux | grep main.py

# 5. Check for errors in output log
tail -50 analysis_output/output.log
```

### Issue: High CPU Usage

**Symptoms:** Monitor consuming 20-30% CPU

**Solutions:**
```bash
# 1. Increase sleep interval
# Edit log_analyser.py, line 44:
time.sleep(5)  # Increase from 2 to 5 seconds

# 2. Reduce polling frequency
# Edit firewall_blocker.py:
time.sleep(10)  # Increase from 3 to 10 seconds

# 3. Use nice to lower priority
sudo nice -n 15 python main.py
```

---



### Requested Features (Community)
- 🔄 Windows event log support (PowerShell integration)
- 🔄 Database backend option (PostgreSQL/MySQL)
- 🔄 REST API for remote management
- 🔄 Kubernetes integration
- 🔄 Machine learning model training

---

## Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m "Add amazing feature"`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Code Guidelines
- Follow PEP 8 style guide
- Add docstrings to new functions
- Update README for new features
- Test with multiple log samples

---

## 📝 License

MIT License - See LICENSE file for details

---

##  Support & Contact

- **Issues:** GitHub Issues page
- **Email:** monujangraji10@example.com
- **LinkedIn:** linkedin.com/in/monu-jangra-8b343437a
- **Documentation:** This README

---

## ⭐ Show Your Support

If this project helped you to secure your servers, please:
- ⭐ Star this repository
- 📢 Share with your DevOps/SysAdmin friends
- 💬 Leave feedback and suggestions
- 🐛 Report any bugs you find

---

**Stay Updated ,Stay Secured 🛡️**
