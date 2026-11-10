import json
import os
import subprocess
import sys
import threading
from pathlib import Path

import psutil
from flask import Flask, jsonify, render_template


BASE_DIR = Path(__file__).resolve().parent
ANALYSIS_DIR = BASE_DIR.parent / "analysis_output"
RUNTIME_DIR = BASE_DIR / "analysis_output"
LOG_PATH = Path(os.environ.get("LOG_FILE_PATH", "/var/log/auth.log"))
INIT_SCRIPT = BASE_DIR / "init.sh"
SIMULATOR_NAMES = ("attacker.py", "attaker.py")
test_process: subprocess.Popen | None = None
test_lock = threading.Lock()

app = Flask(__name__)


def read_tail(path: Path, limit: int = 120) -> list[str]:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as file:
            return file.readlines()[-limit:]
    except (FileNotFoundError, PermissionError, OSError):
        return []


def first_existing(*paths: Path) -> Path:
    for path in paths:
        if path.exists():
            return path
    return paths[0]


def load_threat_data() -> dict:
    threat_json = first_existing(BASE_DIR / "threat_ip.json", ANALYSIS_DIR / "threat_ip.json")
    try:
        with threat_json.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {"total_attacks": 0, "attack_details": {}}


def process_for(script_name: str) -> psutil.Process | None:
    pid_name = "main.pid" if script_name == "main.py" else "firewall.pid"
    for pid_file in (RUNTIME_DIR / pid_name, ANALYSIS_DIR / pid_name):
        try:
            if pid_file.exists():
                process = psutil.Process(int(pid_file.read_text().strip()))
                command_line = process.cmdline()
                if process.is_running() and any(
                    Path(argument).name == script_name for argument in command_line
                ):
                    return process
        except (ValueError, FileNotFoundError, psutil.Error):
            continue

    for process in psutil.process_iter(["pid", "cmdline"]):
        try:
            command_line = process.info["cmdline"] or []
            if any(Path(argument).name == script_name for argument in command_line):
                return process
        except (psutil.Error, TypeError):
            continue
    return None


def process_status(process: psutil.Process | None) -> dict:
    if process is None:
        return {
            "running": False,
            "pid": None,
            "cpu_percent": 0,
            "memory_percent": 0,
            "message": "Process is not running",
        }
    try:
        return {
            "running": process.is_running(),
            "pid": process.pid,
            "cpu_percent": round(process.cpu_percent(interval=0.1), 1),
            "memory_percent": round(process.memory_percent(), 1),
            "message": "Running",
        }
    except psutil.Error:
        return {
            "running": False,
            "pid": None,
            "cpu_percent": 0,
            "memory_percent": 0,
            "message": "Process ended",
        }


def email_status() -> dict:
    required = ("ALERT_EMAIL_SENDER", "ALERT_EMAIL_PASSWORD", "ALERT_EMAIL_RECIPIENT")
    configured = all(
        os.environ.get(key)
        and "your_" not in os.environ[key]
        and "here" not in os.environ[key]
        for key in required
    )
    return {"configured": configured, "label": "Configured" if configured else "Not configured"}


def simulator_path() -> Path | None:
    for name in SIMULATOR_NAMES:
        path = BASE_DIR / name
        if path.exists():
            return path
    return None


def stop_test_process(process: subprocess.Popen) -> None:
    global test_process
    try:
        process.terminate()
        process.wait(timeout=5)
    except (subprocess.TimeoutExpired, OSError):
        try:
            process.kill()
            process.wait(timeout=5)
        except (subprocess.TimeoutExpired, OSError):
            pass
    finally:
        with test_lock:
            if test_process is process:
                test_process = None


def test_is_running() -> bool:
    with test_lock:
        return test_process is not None and test_process.poll() is None


def get_state() -> dict:
    data = load_threat_data()
    details = data.get("attack_details", {})
    threat_json = first_existing(BASE_DIR / "threat_ip.json", ANALYSIS_DIR / "threat_ip.json")
    main_process = process_for("main.py")
    firewall_process = process_for("firewall_auto_ip_blocker.py")
    return {
        "updated": os.path.getmtime(threat_json) if threat_json.exists() else 0,
        "log_path": str(LOG_PATH),
        "attack_counts": {
            name: int(value.get("failed_attempts", 0))
            for name, value in details.items()
        },
        "total_attacks": int(data.get("total_attacks", 0)),
        "logs": {
            "main": read_tail(LOG_PATH),
            "failed": read_tail(first_existing(BASE_DIR / "threat_ip.log", ANALYSIS_DIR / "threat_ip.log")),
            "banned": read_tail(first_existing(BASE_DIR / "ips_detected.txt", ANALYSIS_DIR / "ips_detected.txt")),
        },
        "services": {
            "monitor": process_status(main_process),
            "firewall": process_status(firewall_process),
        },
        "system": {
            "cpu_percent": psutil.cpu_percent(interval=None),
            "memory_percent": psutil.virtual_memory().percent,
        },
        "email": email_status(),
        "test": {"running": test_is_running(), "duration_seconds": 20},
    }


@app.get("/")
def index():
    return render_template("dashboard.html")


@app.get("/api/state")
def state():
    return jsonify(get_state())


@app.post("/api/control/<action>")
def control(action: str):
    if action not in {"start", "restart", "stop"}:
        return jsonify({"error": "Unsupported action"}), 400
    if os.geteuid() != 0:
        return jsonify({
            "error": "Dashboard controls require root. Start it with: sudo ./web-working.sh"
        }), 403

    try:
        result = subprocess.run(
            ["bash", str(INIT_SCRIPT), action],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return jsonify({"error": str(error)}), 500

    if result.returncode != 0:
        return jsonify({"error": result.stderr.strip() or "Command failed"}), 500
    return jsonify({"status": action, "output": result.stdout[-2000:]})


@app.post("/api/test/start")
def start_test():
    global test_process
    if os.geteuid() != 0:
        return jsonify({
            "error": "Testing requires root because the simulator writes to auth.log. Start with: sudo ./web-working.sh"
        }), 403

    script = simulator_path()
    if script is None:
        return jsonify({"error": "Simulator not found. Expected attacker.py or attaker.py."}), 404

    with test_lock:
        if test_process is not None and test_process.poll() is None:
            return jsonify({"error": "A test is already running."}), 409
        try:
            test_process = subprocess.Popen(
                [sys.executable, str(script)],
                cwd=BASE_DIR,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError as error:
            test_process = None
            return jsonify({"error": str(error)}), 500
        process = test_process

    threading.Timer(20, stop_test_process, args=(process,)).start()
    return jsonify({"status": "started", "duration_seconds": 20})


@app.post("/api/test/stop")
def stop_test():
    with test_lock:
        process = test_process
    if process is None or process.poll() is not None:
        return jsonify({"status": "not_running"})
    stop_test_process(process)
    return jsonify({"status": "stopped"})


if __name__ == "__main__":
    app.run(
        host=os.environ.get("DASHBOARD_BIND_HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "8080")),
    )
