import subprocess
from utils.logging import log_output
from configuration.config import LOG_FILE
import time
import os #To use os commands


def filesystem_security():
    print("\n📁 Filesystem Security Permissons Hardening \n")
    time.sleep(1)
    success = True

    # 2. Restrict access to critical config files
    sensitive_files = {
        "/etc/passwd": "644",
        "/etc/shadow": "640",
        "/etc/gshadow": "640",
        "/etc/group": "644",
        "/etc/ssh/sshd_config": "600",
    }

    for file_path, perms in sensitive_files.items():
        if os.path.exists(file_path):
            success &= log_output(
                ["chmod", perms, file_path],
                f"Set permissions {perms} on {file_path}",
                "Filesystem Security"
            )
        else:
             print(f"⚠️ {file_path} not found. Skipping...")
    if success:
        print("✅ Filesystem Security Permisson applied successfully.\n")
    else:
        print("❌ Some filesystem configurations failed.\n")

    return success