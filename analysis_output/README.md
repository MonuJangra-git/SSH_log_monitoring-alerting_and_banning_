# Below Documentation show every thing how project starts and how a client can visualise it easily in different formats according to requirement 
#  Firewall Deployment and Service Status

<img width="785" height="678" alt="starting-tutorial" src="https://github.com/user-attachments/assets/207da4f1-f715-461f-ba17-dfd5604c01b7" />


**Explanation:**
This screenshot shows the execution of `run.sh` to start the firewall management system.  
It verifies the firewall installation, confirms admin checks, and deploys `firewalld`.  
The output highlights that `MJ-IPguard` service is running, ensuring automated protection.  
Additionally, the `status` command confirms that both `main.py` and `firewall_auto_ip_blocker.py` are active, proving the system is functioning as intended.


#  Process Verification with ps aux

<img width="987" height="383" alt="Proof-that-file-is-working" src="https://github.com/user-attachments/assets/d62c822f-9033-49f4-b6d8-85c7074628de" />


**Explanation:**
This screenshot displays the `ps aux` command output, listing active processes.  
Highlighted entries confirm that `python3 main.py` and `python3 firewall_auto_ip_blocker.py` are running.  
This serves as proof that the firewall automation scripts are live and continuously monitoring the system.  
Including this screenshot validates the backend execution of the security modules.
# Screenshot Overview: Network IP Monitoring

<img width="809" height="674" alt="ips_detected" src="https://github.com/user-attachments/assets/98c2e24f-ea85-4841-b469-7284589e1cc4" />


**Explanation:**
This screenshot shows a terminal listing multiple private IP addresses (192.168.x.x, 172.16.x.x) detected during monitoring.  
The background includes the project workspace in VS Code, confirming integration with the “BLACKHACK” project files.  
This serves as proof of active network scanning and monitoring, validating the system’s ability to track connected devices in a cybersecurity context.
# Screenshot Overview: Attack Type Visualization

<img width="850" height="615" alt="Visualising_log_file_using_matplotlib" src="https://github.com/user-attachments/assets/7a439067-4fa8-4144-830d-6ebc351a9f56" />

**Explanation:**
This screenshot presents a bar chart generated from `threat_ip.json`, showing counts of different attack types.  
The chart compares **brute_force (50)**, **lockout (56)**, **pam_failure (48)**, and **other_failed (0)** attempts.  
By visualizing the data, it highlights that lockout attacks were the most frequent, providing a clear statistical overview of intrusion attempts.


#  Threat Detection Log (Detailed)

<img width="1111" height="689" alt="logs-scoorecard-in-scorecard-format" src="https://github.com/user-attachments/assets/72c1f330-6a18-4fe0-8b94-4474e0dc6072" />


**Explanation:**
This screenshot displays the `threat_ip.log` file with categorized intrusion attempts.  
It summarizes failed SSH login attempts under **BRUTE_FORCE**, **LOCKOUT**, and **PAM_FAILURE**, with timestamps and IP addresses.  
The log confirms a total of **154 attacks detected**, serving as detailed proof of the system’s monitoring and detection capabilities.  
This evidence demonstrates how the system records unauthorized access attempts for forensic and security analysis.


#  Firewall Rule Updates Log

<img width="911" height="681" alt="firewall_ips_blocked" src="https://github.com/user-attachments/assets/983c9862-e412-4392-957a-0df978a9f9fb" />


**Explanation:**
This screenshot displays log entries confirming successful addition of multiple IP addresses to firewall rules.  
Each entry includes a timestamp and a success message, showing automated rule deployment in real time.  
The presence of both private and internal IP ranges demonstrates the system’s capability to secure diverse network segments.  
Including this screenshot validates the automation of firewall management and continuous security enforcement.
# Screenshot Overview: Active Firewall Configuration

<img width="890" height="709" alt="proof-blocked-ips" src="https://github.com/user-attachments/assets/b022acf2-051a-43c9-a1e5-d7ee574dbf68" />


**Explanation:**
This screenshot shows the output of the `firewall-cmd --list-all` command, displaying the active configuration for the public zone.  
It lists allowed services such as HTTP, HTTPS, MySQL, and SSH, along with multiple rich rules that drop traffic from specific IPv4 source addresses.  
These entries confirm that the firewall is actively blocking malicious or unauthorized IPs, demonstrating effective network access control and rule enforcement.


#  Threat Detection Scorecard Log

<img width="1111" height="689" alt="logs-scoorecard-in-scorecard-format" src="https://github.com/user-attachments/assets/b1b2ccba-cb32-4d63-b626-90ed33262409" />

**Explanation:**
This screenshot presents the contents of the `threat_ip.log` file, summarizing detected attacks under categories like **BRUTE_FORCE**, **LOCKOUT**, and **PAM_FAILURE**.  
Each section includes timestamps, IP addresses, and authentication failure messages, providing detailed insight into intrusion attempts.  
This serves as proof of the system’s real-time threat monitoring and logging capabilities, showcasing its ability to detect and categorize unauthorized access attempts.

# Conclusion

These screenshots collectively demonstrate the **deployment, monitoring, and security enforcement** features of the Firewall Management & Threat Detection System.  
They provide verifiable proof of functionality, making the project transparent and reliable for presentation, audits, or client review.
> Note: All screenshots were captured in a controlled lab environment using test SSH attack simulations.
