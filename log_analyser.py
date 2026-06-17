import re
import os
import time
from email_handler import EmailHandler
from file_handler import FileHandler

class log_monitoring_and_alerting:
    def __init__(self, file_name):
        self.ippattern = r"\d+\.\d+\.\d+\.\d+"
        self.position = 0
        self.file_name = file_name
        self.wait = 0
        self.email_handler = EmailHandler()
        self.file_handler = FileHandler()
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                f.seek(0, 2)
                self.position = f.tell()
    
    def analyser(self):
        with open(self.file_name, "r") as f:
            stats = {
                "brute_force": 0,
                "lockout": 0,
                "pam_failure": 0,
                "other_failed": 0
            }

            recent_logs = {
                "brute_force": [],
                "lockout": [],
                "pam_failure": [],
                "other_failed": []
            }
            patterns = [
                (re.compile(r'Failed password for (?:invalid user )?(\S+) from (\d+\.\d+\.\d+\.\d+)'), "brute_force_attempt_standard"),  # creates a regex object from a string pattern
                (re.compile(r'Failed password for (?:invalid user )?(\S+) from (::1)'), "brute_force_attempt_localhost"),
                (re.compile(r'error: maximum authentication attempts exceeded for .*? from (\d+\.\d+\.\d+\.\d+)'), "brute_force_lockout_event"),
                (re.compile(r'authentication failure;.*rhost=(\d+\.\d+\.\d+\.\d+)'), "pam_authentication_failure"),
                (re.compile(r'pam_unix\(sshd:auth\): authentication failure;.*rhost=(\S+)'), "pam_authentication_failure_rhost")]
            while True:
                f.seek(self.position)
                line = f.readline()
                if not line.strip() or len(line) <= 7:
                    self.position = f.tell()
                    if not line:
                        time.sleep(2)
                        self.wait += 1
                        if(self.wait > 3):
                            print("waitting for new logs ")
                            self.wait = 0
                    continue
                ip_pattern = re.compile(self.ippattern)
                for regex, name in patterns:
                    match = regex.search(line)
                    if match:
                        ip = ip_pattern.search(line)
                        if ip:
                            with open("ips_detected.txt", "a") as ip_file:
                                ip_file.write(f"{ip.group()}\n")
                        atk = f"Detected: {name} :- {match.groups()}\n"
                        self.file_handler.output_log(atk)  # attack shown for cli interface
                        if name in ["brute_force_attempt_standard", "brute_force_attempt_localhost"]:
                            stats["brute_force"] += 1
                            recent_logs["brute_force"].append(line)
                            recent_logs["brute_force"] = recent_logs["brute_force"][-10:]
                            self.file_handler.file_manager(stats, recent_logs)
                            self.file_handler.file_manager_json(stats, recent_logs)
                                       
                        elif name in ["brute_force_lockout_event", "pam_authentication_failure_rhost"]:                    
                            stats["lockout"] += 1
                            recent_logs["lockout"].append(line)
                            recent_logs["lockout"] = recent_logs["lockout"][-10:]
                            
                            self.file_handler.file_manager(stats, recent_logs)
                            self.file_handler.file_manager_json(stats, recent_logs)
                        elif name in ["pam_authentication_failure"]:
                            stats["pam_failure"] += 1
                            recent_logs["pam_failure"].append(line)
                            recent_logs["pam_failure"] = recent_logs["pam_failure"][-10:]
                            self.file_handler.file_manager(stats, recent_logs)
                            self.file_handler.file_manager_json(stats, recent_logs)
                        elif "failed" in line.lower():
                            stats["other_failed"] += 1
                            recent_logs["other_failed"].append(line)
                            recent_logs["other_failed"] = recent_logs["other_failed"][-10:]
                            self.file_handler.file_manager(stats, recent_logs)
                            self.file_handler.file_manager_json(stats, recent_logs)
                                                                          

                        total_atk = sum(stats.values())
                        #if total_atk>=500: # email alert sent for every 500 attacks detected for better performance and to avoid sending multiple emails for the same attack type and also to keep the log file clean for new attacks and also to avoid confusion for the user
                        if total_atk%500 == 0 and total_atk != 0: # email alert sent for every 500 attacks detected for better performance and to avoid sending multiple emails for the same attack type and also to keep the log file clean for new attacks and also to avoid confusion for the user
                            try:
                                self.email_handler.mutt()
                            except:
                                self.email_handler.smtp_mailer_main()
                            open("threat_ip.log", "w").close()
                            open("threat_ip.json", "w").close()
                            # option for user to reset the stats and recent logs after sending the email alert for better performance and to avoid sending multiple emails for the same attack type and also to keep the log file clean for new attacks and also to avoid confusion for the user
                            # for key in stats:
                            #     stats[key] = 0
                            #     recent_logs[key] = []
                            print("Mail Sent Successfully")          
                self.position = f.tell()
