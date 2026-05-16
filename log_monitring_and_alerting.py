import re
import os
import time 
import subprocess
import smtplib
import mimetypes
from email.message import EmailMessage
# Set ALERT_EMAIL_SENDER, ALERT_EMAIL_PASSWORD, ALERT_EMAIL_RECIPIENT in the environment for GitHub-safe email configuration
class log_monitoring_and_alerting:
    def ip_blocker(self,ip):
        block = subprocess.run(["firewall-cmd", f"--add-rich-rule=rule family='ipv4' source address={ip} drop","--timeout=100"], capture_output=True, text=True)
    def file_writer(self,content):
        with open("threat_ip.log", "a") as file:
            file.write(content+"\n")
    def file_structure(self,attack_type,attack_number,list):
        self.file_writer(f"{'-'*75}\n[CRITICAL] {attack_type} \n Failed_attempts={attack_number} \n Recent_logs={'\\n'.join(map(str, list))}")
    def mail_sender(self, search):
        if search and re.match(self.ippattern, str(search)):
            ip = search
            print(f"Suspicious IP detected: {ip}")
            self.smtp_mailer_main(ip, f"IP threat detected by this IP {ip}")
        else:       # no IP found or unavailable
            print("Suspicious activity detected (no IP found)")
            self.smtp_mailer_main(None, "Alert: anonymous or unknown threat activity detected")
    def smtp_mailer_main(self, ip, search): 
        try:
            if ip and re.match(self.ippattern, str(ip)):
                self.ip_blocker(ip)
            with open("threat.txt", 'a') as file:
                file.write(f"{search}\n")
            sender = os.getenv("ALERT_EMAIL_SENDER", "your_sender@example.com")
            key = os.getenv("ALERT_EMAIL_PASSWORD", "your_app_password_here")  # Use an app password or encrypted secret
            receiver = os.getenv("ALERT_EMAIL_RECIPIENT", "your_recipient@example.com")
            body = f"threat detected {search} .... check your server"
            subject = "ALERT MAIL FROM SERVER"
            msg = EmailMessage()
            msg['subject'] = subject
            msg['from'] = sender
            msg['to'] = receiver
            msg.set_content(body)
            # send the alert email without attaching the full log file for speed
            with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(sender, key)
                server.send_message(msg)
            print("mail sent successfully")
        except Exception as error:
            print(f"Error sending email: {error}")
    def __init__(self,file_name):
        self.ippattern=r"\d+\.\d+\.\d+\.\d+"
        self.position = 0
        self.file_name=file_name
        self.wait=0
        if os.path.exists(file_name) :
            with open(file_name,'r') as f:
                f.seek(0,2)
                self.position=f.tell()
    def analyser(self):
        with open(self.file_name,"r") as f:
            atk_typ_1_,atk_typ_2_,atk_typ_3_,atk_typ_4_=0,0,0,0
            list1,list2,list3,list4=[],[],[],[]
            while True:
                f.seek(self.position)
                line = f.readline()
                if not line.strip() or len(line) <=7 :
                    self.position=f.tell()
                    if not line:
                        time.sleep(2)
                        self.wait+=1
                        if(self.wait>3):
                            print("waitting for new logs ")
                            self.wait=0
                    continue
                # here we are using list and inside list there are two seperate elements of touple
                # list = {(e1,e2)} 
                patterns = [
        (re.compile(r'Failed password for (?:invalid user )?(\S+) from (\d+\.\d+\.\d+\.\d+)'), "brute_force_attempt_standard"),#creates a regex object from a string pattern
        (re.compile(r'Failed password for (?:invalid user )?(\S+) from (::1)'), "brute_force_attempt_localhost"),
        (re.compile(r'Failed password for (?:invalid user )?(\S+)'), "brute_force_attempt_no_ip"),
        (re.compile(r'error: maximum authentication attempts exceeded for .*? from (\d+\.\d+\.\d+\.\d+)'), "brute_force_lockout_event"),
        (re.compile(r'authentication failure;.*rhost=(\d+\.\d+\.\d+\.\d+)'), "pam_authentication_failure"),
        (re.compile(r'pam_unix\(sshd:auth\): authentication failure;.*rhost=(\S+)'), "pam_authentication_failure_rhost")
    ]
                ip_pattern = re.compile(self.ippattern)

                for regex,name in patterns:
                    match = regex.search(line)
                    if match:
                        ip = ip_pattern.search(line)
                        if ip:
                            with open("ips_detected.log", "a") as ip_file:
                                ip_file.write(f"{ip.group()}\n")
                        atk = f"Detected: {name} :- {match.groups()}\n"
                        print(atk)
                        if name in ["brute_force_attempt_standard", "brute_force_attempt_localhost", "brute_force_attempt_no_ip"]:
                            atk_typ_1_+=1
                            if atk_typ_1_>=50:
                             
                                list1.append(line)
                                if len(list1)==10:
                                    self.file_structure("bruteforce_attempt_level_1",atk_typ_1_,list1)
                                    self.mail_sender("Alert!!")
                                    list1.clear()
                                    atk_typ_1_=0
                        elif name in ["brute_force_lockout_event", "pam_authentication_failure_rhost"]:
                            self.file_writer(atk)
                            atk_typ_2_+=1
                            if atk_typ_2_>=50:
                                
                                list2.append(line)
                                if len(list2)==10:
                                    self.file_structure("bruteforce_attempt_level_1",atk_typ_2_,list2)
                                    self.mail_sender("Alert!!")
                                    list2.clear()
                                    atk_typ_2_=0
                        elif name in ["pam_authentication_failure"]:
                            self.file_writer(match.group(1))
                            atk_typ_3_+=1
                            if atk_typ_3_>=50:
                                
                                list3.append(line)
                                if len(list3)==10:
                                    self.file_structure("bruteforce_attempt_level_1",atk_typ_3_,list3)
                                    self.mail_sender("Alert!!")
                                    list3.clear()
                                    atk_typ_3_=0
                        elif "failed" in line.lower():
                            print("failed attempt it may be user own ")
                            atk_typ_4_+=1
                            if atk_typ_4_>=50:
                                
                                list4.append(line)
                                if len(list4)==10:
                                    self.file_structure("bruteforce_attempt_level_1",atk_typ_4_,list4)
                                    self.mail_sender("Alert!!")
                                    list4.clear()
                                    atk_typ_4_=0
                self.position=f.tell()
if __name__=="__main__":
    file_name="/var/log/auth.log"
    try :
        monitor=log_monitoring_and_alerting(file_name)   
        monitor.analyser()
    except KeyboardInterrupt:
        print("exit successfully ")
                # if os.path.exists("threat_ip.log") and os.path.getsize("threat_ip.log") > 1024*100:
                #     self.mail_sender("⚠️ high alert saw your system what is happening someone try to hacking your device check the server immediately")
                #     open("threat_ip.log","w").close()


