import subprocess
from utils.logging import log_output
from configuration.config import LOG_FILE
import time


def user_account_management():
    print("\n🔐 User Account Security Configurations \n")
    time.sleep(1)
    success = True
    success &= log_output(["sed", "-i", "s/^PASS_MAX_DAYS.*/PASS_MAX_DAYS   31/", "/etc/login.defs"], 
               "Set max password age", "User account Configurations")
    success &= log_output(["sed", "-i", "s/^PASS_MIN_DAYS.*/PASS_MIN_DAYS   2/", "/etc/login.defs"], 
               "Set min password age", "User account Configurations")
    success &= log_output(["sed", "-i", "s/^PASS_WARN_AGE.*/PASS_WARN_AGE   7/", "/etc/login.defs"], 
               "Set password warning age", "User account Configurations")
    success &= log_output(["sed", "-i", "s/^#*PermitRootLogin.*/PermitRootLogin no/", "/etc/ssh/ssh_config"], 
                "Disable root SSH login", "User account Configurations")
    
    check_active = subprocess.run(["systemctl", "is-active", "ssh"],   #Only restart ssh if its running
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)
    if check_active.returncode == 0:
        success &= log_output(["systemctl", "reload", "ssh"], 
                    "Reload SSH service", "User account Configurations")    
               
    if success:

        print(f"✅ Task1: Account Configured Successfully")
    else:
        print(f"❌ Task1: Account Configuration Failed")

    return True



