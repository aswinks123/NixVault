import subprocess
from utils.logging import log_output
from configuration.config import LOG_FILE
import time
import os


def ssh_hardening():
    print("\n✨ SSH Security Hardening \n")
    time.sleep(1)
    ssh_config = "/etc/ssh/sshd_config"
    success = True
    if not os.path.isfile(ssh_config):
        print(f"❌ SSH configiguration file not found at: {ssh_config} .Is SSH installed?. Skipping this step...")
        return False

    

    harden_rules = {
        "PermitRootLogin": "no",
        "PasswordAuthentication": "no",         # Use only key-based auth
        "PermitEmptyPasswords": "no",
        "Protocol": "2",
        "X11Forwarding": "no",
        "MaxAuthTries": "3",
        "ClientAliveInterval": "300",           # Disconnect idle sessions after 5 mins
        "ClientAliveCountMax": "0",             # Disconnect immediately after 1 interval
        "AllowTcpForwarding": "no",
        "UseDNS": "no",
        "LoginGraceTime": "30",                 # Shorten login grace time
        "Banner": "/etc/issue.net"
    }

    # Apply each setting
    for key, value in harden_rules.items():
        log_output([
            "sed", "-i",
            f"s|^#*{key}.*|{key} {value}|",
            ssh_config
        ], f"Set {key} to {value}", "SSH Hardening")
    
    try:
        banner_message = f"""
************************************************************
*                                                          *
*  WARNING: Authorized access only.                        *
*  Disconnect IMMEDIATELY if you are not an authorized     *
*  Created by nixVault Automation                          *
*  All activity is monitored and recorded.                 *
*                                                          *
************************************************************
"""
        with open("/etc/issue.net", "w") as banner_file:
            banner_file.write(banner_message)
        log_output(["chmod", "644", "/etc/issue.net"], "Set SSH login Banner", "SSH Secure Banner")
    except Exception as e:
        print(f"⚠️ Error creating banner: {str(e)}")


    # Restart SSH to apply changes
    success &= log_output(["systemctl", "restart", "ssh"], "Restart SSH service", "SSH Hardening")

    if success:

        print(f"✅ Task1: SSH Secured Successfully")
    else:
        print(f"❌ Task1: Failed to Secure SSH")

    return True


