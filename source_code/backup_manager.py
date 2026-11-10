import os
import shutil
import time
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ANALYSIS_DIR = BASE_DIR.parent / "analysis_output"
THRESHOLD_BYTES = 50 * 1024 * 1024
CHECK_INTERVAL_SECONDS = 10


def monitored_files() -> list[Path]:
    candidates = [
        Path(os.environ.get("LOG_FILE_PATH", "/var/log/auth.log")),
        BASE_DIR / "output.log",
        BASE_DIR / "threat_ip.log",
        BASE_DIR / "threat_ip.json",
        BASE_DIR / "ips_detected.txt",
        BASE_DIR / "firewall_rules.log",
        ANALYSIS_DIR / "main.log",
        ANALYSIS_DIR / "firewall.log",
        ANALYSIS_DIR / "firewall_rules.log",
        ANALYSIS_DIR / "threat_ip.log",
    ]
    return list(dict.fromkeys(candidates))


def next_backup_path(source: Path) -> Path:
    number = 1
    while True:
        candidate = source.with_name(f"{source.name}.bkup{number}")
        if not candidate.exists():
            return candidate
        number += 1


def backup_if_needed(source: Path, backed_up_sizes: dict[Path, int]) -> Path | None:
    try:
        size = source.stat().st_size
    except (FileNotFoundError, PermissionError, OSError):
        return None

    last_size = backed_up_sizes.get(source, 0)
    if size < THRESHOLD_BYTES or size < last_size + THRESHOLD_BYTES:
        return None

    destination = next_backup_path(source)
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    except (PermissionError, OSError) as error:
        print(f"Backup failed for {source}: {error}", flush=True)
        return None

    backed_up_sizes[source] = size
    print(f"Backup created: {destination}", flush=True)
    return destination


def run() -> None:
    backed_up_sizes: dict[Path, int] = {}
    while True:
        for source in monitored_files():
            backup_if_needed(source, backed_up_sizes)
        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("Backup manager stopped.", flush=True)
# this file is written by co-pilot and idea is mine and is intended to be used as a backup manager for log files. It monitors specific log files and creates backups when they exceed a certain size threshold. The script runs indefinitely until interrupted by the user.
# by default, it checks the monitored files every 10 seconds and creates a backup if the file size exceeds 50 MB. The backups are stored in the same directory as the original files with a numbered suffix to avoid overwriting existing backups.ex filename.bkup1, filename.bkup2, etc. larger the number latest will be the backup .