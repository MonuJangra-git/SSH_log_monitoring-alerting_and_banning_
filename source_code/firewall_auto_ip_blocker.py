import subprocess
try:
    import regex as re
except Exception:
    # fallback to stdlib `re` if `regex` is not installed
    import re
import time
import os


print("welcome to firewall management system v2.0 \n you can set rules and manage your firewall using this interface ")
def log_file(write_data:str):
    with open("firewall_rules.log","a") as file:
        file.write(write_data)
def run_cmd(cmd:list):
    try:
        output=subprocess.run(cmd,text=True,capture_output=True,timeout=20)
        return output.returncode==0,output.stdout.strip(),output.stderr.strip()
        # 0 means true command runned successfully
    except subprocess.TimeoutExpired:
        return False,"","timeout_error"
    except Exception as error:
        return False,"",error
def rules_setter(): 
    pattern = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    processed_ips = set()  # Track processed IPs to avoid duplicates # we use set instead of list because set is faster for lookups and it automatically handles duplicates 
    last_file_size = 0  # Track file size for changes
    log_file("[*] Continuous monitoring started\n")
    while True:
        try:
            if not os.path.exists("ips_detected.txt"):
                time.sleep(10)
                continue     
            current_file_size = os.path.getsize("ips_detected.txt")     
            # Only process if file has changed
            if current_file_size != last_file_size:
                last_file_size = current_file_size
                
                with open("ips_detected.txt","r") as file:
                    for line in file:
                        ip=line.strip()
                        
                        # Skip empty lines and already processed IPs
                        if not ip or ip in processed_ips:
                            continue
                        
                        if pattern.match(ip):
                            log_file(f"[✓] Valid IP: {ip} - Adding to firewall rules")
                            cmd=["firewall-cmd","--add-rich-rule",f'rule family="ipv4" source address="{ip}" drop']
                            success,stdout,stderr=run_cmd(cmd)
                            if success:
           
                                log_file(f"[✓] Successfully added {ip} to firewall rules at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                                processed_ips.add(ip)
                            else :
                                log_file(f"[✗] Failed to add {ip} to firewall rules | Error: {stderr} at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                        else :
                            log_file(f"[!] Invalid IP: {ip} - Skipping at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                            processed_ips.add(ip)
            time.sleep(3)  # Check every 3 seconds
        except KeyboardInterrupt:
            log_file("[*] Monitoring stopped by user\n")
            break
        except Exception as e:
            log_file(f"[!] Error during monitoring: {e}\n")
            time.sleep(5)
rules_setter()
