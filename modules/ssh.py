import subprocess
from utils.logging import log_output
from configuration.config import LOG_FILE
import time
import os


def ssh_hardening():
    print("\n🔒 SSH Security Hardening\n")
    time.sleep(1)
    ssh_config = "/etc/ssh/sshd_config"
    success = True

    if not os.path.isfile(ssh_config):
        print(f"❌ SSH configuration file not found at: {ssh_config}. Is SSH installed? Skipping this step...")
        return False

    harden_rules = {
        "PermitRootLogin": "no",
        "PasswordAuthentication": "no",
        "PermitEmptyPasswords": "no",
        "Protocol": "2",
        "X11Forwarding": "no",
        "MaxAuthTries": "3",
        "ClientAliveInterval": "300",
        "ClientAliveCountMax": "0",
        "AllowTcpForwarding": "no",
        "UseDNS": "no",
        "LoginGraceTime": "30",
        "Banner": "/etc/issue.net"
    }

    # Apply settings
    for key, value in harden_rules.items():
        try:
            with open(ssh_config, "r") as file:
                content = file.read()

            if key in content:
                # Replace existing line
                cmd = [
                    "sed", "-i",
                    f"s/^#*\\s*{key}\\s\\+.*/{key} {value}/g",
                    ssh_config
                ]
            else:
                # Append if not present
                cmd = [
                    "bash", "-c",
                    f"echo '{key} {value}' >> {ssh_config}"
                ]

            success &= log_output(cmd, f"Set {key} to {value}", "SSH Security Hardening")

        except Exception as e:
            print(f"⚠️ Error processing {key}: {e}")
            success = False

    # Create the banner
    try:
        with open("/etc/issue.net", "w") as banner_file:
            banner_file.write("🚫 Authorized access only. Disconnect IMMEDIATELY if you are not authorized.\n")
        success &= log_output(["chmod", "644", "/etc/issue.net"], "Set SSH login Banner", "SSH Security Hardening")
    except Exception as e:
        print(f"⚠️ Error creating banner: {str(e)}")
        success = False

    # Restart SSH to apply changes
    success &= log_output(["systemctl", "restart", "ssh"], "Restart SSH service", "SSH Hardening")

    if success:
        print(f"\n✅ Task1: SSH Secured Successfully\n")
    else:
        print(f"\n❌ Task1: Failed to Secure SSH\n")

    return success
