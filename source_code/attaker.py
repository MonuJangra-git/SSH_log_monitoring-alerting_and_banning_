import random
import time
from datetime import datetime

LOG_FILE = "/var/log/auth.log"

# Random username list
USERNAMES = [
    "root", "admin", "test", "ubuntu",
    "oracle", "postgres", "guest", "dev"
]

# Random IP pool (expandable)
IP_POOL = [f"192.168.1.{i}" for i in range(10, 50)] + \
          [f"10.0.0.{i}" for i in range(2, 20)] + \
          [f"172.16.0.{i}" for i in range(5, 25)]


def current_time():
    return datetime.now().strftime("%b %d %H:%M:%S")


def brute_force_standard():
    username = random.choice(USERNAMES)
    ip = random.choice(IP_POOL)
    return f"{current_time()} server sshd[1234]: Failed password for invalid user {username} from {ip} port 22 ssh2\n"


def brute_force_localhost():
    username = random.choice(USERNAMES)
    return f"{current_time()} server sshd[1234]: Failed password for invalid user {username} from ::1 port 22 ssh2\n"


def lockout_event():
    ip = random.choice(IP_POOL)
    return f"{current_time()} server sshd[1234]: error: maximum authentication attempts exceeded for root from {ip} port 22 ssh2\n"


def pam_auth_failure():
    ip = random.choice(IP_POOL)
    return f"{current_time()} server sshd[1234]: authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost={ip}\n"


def pam_unix_failure():
    ip = random.choice(IP_POOL)
    return f"{current_time()} server sshd[1234]: pam_unix(sshd:auth): authentication failure; rhost={ip}\n"


# All attack generators
ATTACK_TYPES = [
    brute_force_standard,
    brute_force_localhost,
    lockout_event,
    pam_auth_failure,
    pam_unix_failure
]


def generate_random_attack():
    attack_function = random.choice(ATTACK_TYPES)
    return attack_function()


def run_simulation():
    print("🚀 Advanced Attack Simulator Running...")
    print("Press CTRL+C to stop.\n")

    try:
        while True:
            attack_line = generate_random_attack()

            with open(LOG_FILE, "a") as f:
                f.write(attack_line)

            print("[+] Injected:", attack_line.strip())

            time.sleep(0.2)  # delay per attack

    except KeyboardInterrupt:
        print("\n Simulation stopped.")


if __name__ == "__main__":
    run_simulation()