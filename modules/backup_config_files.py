import subprocess
from utils.logging import log_output
from configuration.config import LOG_FILE
import time
import shutil
import os


def backup_config_files():
    print("\n💾 Backing up Important Configuration Files\n")
    time.sleep(1)

    # Define important configuration files
    config_files = [
        "/etc/passwd",
        "/etc/shadow",
        "/etc/group",
        "/etc/sudoers",
        "/etc/ssh/sshd_config",
        "/etc/fstab",
        "/etc/hostname",
        "/etc/network/interfaces"
    ]

    # Get the home directory of the current user
    home_dir = os.path.expanduser("~")
    backup_dir = os.path.join(home_dir, "config_backups")

     # Create the backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    success = True

    for file_path in config_files:
        # Check if the file exists
        if os.path.exists(file_path):
            # Determine the destination backup path
            dest_path = os.path.join(backup_dir, os.path.basename(file_path))

            # Copy the file to the backup directory
            try:
                shutil.copy(file_path, dest_path)
                log_output(
                    ["cp", file_path, dest_path],
                    f"Backup of {file_path} to {dest_path}",
                    "Configuration Backup"
                )
                print(f"✅ Successfully backed up {file_path} to {dest_path}")
            except Exception as e:
                print(f"⚠️ Failed to back up {file_path}: {str(e)}")
                success = False
        else:
            print(f"⚠️ {file_path} does not exist. Skipping...")

    if success:
        print(f"\n✅ Task: Configuration files backed up successfully to {backup_dir}\n")
    else:
        print(f"\n❌ Task: Some configuration files failed to back up.\n")

    return success

