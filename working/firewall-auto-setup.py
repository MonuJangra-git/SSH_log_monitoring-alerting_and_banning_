import subprocess
import sys
print("welcome to firewall management system v2.0 \n you can set rules and manage your firewall using this interface ")
def log_file(write_data:str):
    with open("firewall_rules.log","a") as file:
        file.write(write_data)
        print(write_data)
def run_cmd(cmd:list):
    try:
        output=subprocess.run(cmd,text=True,capture_output=True,timeout=20)
        return output.returncode==0,output.stdout.strip(),output.stderr.strip()
        # 0 means true command runned successfully
    except subprocess.TimeoutExpired:
        return False,"","timeout_error"
    except Exception as error:
        return False,"",error
def admin_check():
    id_cmd=["id","-u"]
    success,stdout,stderr=run_cmd(id_cmd)
    if success:
        if stdout=="0":
            print("user can use the script ")
            return 1
        if stdout !="0":
            print("user can not use the script \nlogin as admin 1st  \nexiting")
            return 0
        if stderr:
            print(f"there are some issue {stderr}")
    else :
        print("failed to check")
def firewall_check():
    # now initially we making it 
    cmd = ["which","firewalld"]
    success,stdout,stderr=run_cmd(cmd)
    if success :
        if stdout:
            print("firewalld is installed ")
            return 1
        if stderr:
            print("firewalld is not installed , use sudo apt install firewalld -y and make sure internet work properly  ")
            return 0
    else :
        print("there are some issue in checking the firewall, use need to install firewall 1st using \n 'sudo apt install firewalld' or \n 'sudo yum install firewalld'")
        sys.exit("please use command , this is not big issue  ")
def firewall_deploy():
    if firewall_check() ==1:
        cmd=["systemctl","enable","firewalld"]
        cmd_start=["systemctl","start","firewalld"]
        cmd_check_status=["systemctl","is-active","firewalld"]
        rok,stdout1,error2=run_cmd(cmd_check_status)
        start,ok,error=run_cmd(cmd_start)
        print(ok)
        success,stdout,stderr=run_cmd(cmd)
        if success:
            if str(stdout1).strip()=="active":
                print("firewalld_status_active and now your firewalld is running")
                return 1
            else:
                print("status inactive \n checking status \nwait to reactive it ")   
                firewall_deploy()
                return 1 
        else :
            print("there are some issue.........")
            return 0 
if __name__ == "__main__":
    print("checking the admin ")
    if admin_check() == 1:
        print("admin check successfull \n checking the firewall")
        if firewall_check()==1:
            print("firewall checked successfully \n deploting the firewall ")
            if firewall_deploy()==1:
                print("firewall setup is complete ypu can use it now ")
