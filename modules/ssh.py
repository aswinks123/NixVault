import subprocess
from utils.logging import log_output
import time
import os

def ssh_hardening():
    print("\n✨ SSH Security Hardening \n")
    time.sleep(1)
    ssh_config = "/etc/ssh/sshd_config"
    success = True
    if not os.path.isfile(ssh_config):
        print(f"❌ SSH configuration file not found at: {ssh_config}. Is SSH installed? Skipping this step...")
        return False

    # Define hardening rules
    harden_rules = {
        "PermitRootLogin": "no",
        "PasswordAuthentication": "no",  # Use only key-based auth
        "PermitEmptyPasswords": "no",
        "Protocol": "2",
        "X11Forwarding": "no",
        "MaxAuthTries": "3",
        "ClientAliveInterval": "300",  # Disconnect idle sessions after 5 mins
        "ClientAliveCountMax": "0",  # Disconnect immediately after 1 interval
        "AllowTcpForwarding": "no",
        "UseDNS": "no",
        "LoginGraceTime": "30",  # Shorten login grace time
        "Banner": "/etc/issue.net"
    }

    # Backup the original file
    backup_file = f"{ssh_config}.bak"
    if not os.path.exists(backup_file):
        log_output(["cp", ssh_config, backup_file], "Created backup of SSH config", "SSH Hardening")

    # Process each setting
    for key, value in harden_rules.items():

        # First remove any existing entries (commented or not)
        log_output(
            ["sed", "-i", f"/^#*{key}[[:space:]]/d", ssh_config],
            f"Removed existing and added new entries for {key}",
            "SSH Hardening"
        )
        
        # Then append the new setting at the end of the file
        with open(ssh_config, "a") as f:
            f.write(f"\n{key} {value}\n")

    try:
        # Create custom login banner message
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
        # Write the banner to the /etc/issue.net file
        with open("/etc/issue.net", "w") as banner_file:
            banner_file.write(banner_message)
        # Set permissions for the banner
        log_output(["chmod", "644", "/etc/issue.net"], "Set SSH login Banner", "SSH Secure Banner")
    except Exception as e:
        print(f"⚠️ Error creating banner: {str(e)}")
        success = False

    # Restart SSH service to apply the changes
    success &= log_output(["systemctl", "restart", "ssh"], "Restart SSH service", "SSH Hardening")

    # Final success or failure message
    if success:
        print(f"✅ SSH Secured Successfully")
    else:
        print(f"❌ Failed to Secure SSH")

    return success