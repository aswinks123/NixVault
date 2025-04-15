#==================================================================================
#DEVELOPER: Aswin KS
#DATE: 15-04-2025
#ABOUT: NixVault: NixVault is a comprehensive Linux security hardening tool designed to safeguard your system from internal vulnerabilities and external threats.
#Built with a focus on simplicity and power, NixVault automates best-practice configurations, manages sensitive data securely, and reinforces system integrity.
#==================================================================================

import subprocess  # module is used to execute system-level commands in Python
import sys  # This module provides access to system-specific parameters and functions
import os
#---------------------------------------------

LOG_FILE = "result.log"
summary = {}



# Check if the script is run as root
def check_root():
    if os.geteuid() != 0:
        print("❌ This script must be run as root. Re-running with sudo or switch to root!")
        # Exit the program
        exit(1)
        
    else:
        print("✅ Running as root.\n")

# --------------------------------------------
# Helper function to run commands and log output
def log_output(command, task_name, section_name):
    with open(LOG_FILE, "a") as log:
        log.write(f"\n====={task_name}=====\n")
        result = subprocess.run(command, stdout=log, stderr=log)
    
    # Store each task's result in the summary dictionary, categorized by section
    if section_name not in summary:
        summary[section_name] = []
    summary[section_name].append((task_name, result.returncode == 0))
    return result.returncode == 0

# ---------------------------------------------

# Function to install UFW Firewall
def install_ufw():
    return log_output(["apt-get", "install", "-y", "ufw"], "Installing UFW Firewall", "Configuring UFW Firewall")

# Function to configure UFW Firewall
def configure_firewall():
    success = True
     # Reset UFW to remove all existing rules
    success &= log_output(["sh", "-c", "yes | ufw reset"], "Resetting UFW", "Configuring UFW Firewall")
    

    success &= log_output(["ufw", "default", "deny", "incoming"], "Set default deny incoming", "Configuring UFW Firewall")
    success &= log_output(["ufw", "default", "allow", "outgoing"], "Set default allow outgoing", "Configuring UFW Firewall")
    success &= log_output(["ufw", "allow", "ssh"], "Allowed SSH Port", "Configuring UFW Firewall")
    success &= log_output(["ufw", "allow", "https"], "Allowed SSH Port", "Configuring UFW Firewall")
    success &= log_output(["ufw", "--force", "enable"], "UFW activated & enabled on startup", "Configuring UFW Firewall")
    return success

# ---------------------------------------------

# Function to print the summary
def print_summary():
    print("\n📋 Summary Report:")
    print("-" * 80)

    # Iterate through each section in the summary
    for section, tasks in summary.items():
        print(f"\n{section}:\n" + "-" * len(section))
        for task, result in tasks:
            status = "✅ Success" if result else "❌ Failed"
            print(f"{task:<50} {status}")
    
    print("-" * 80)
    print("🔍 See 'result.log' for more details.\n")

# ---------------------------------------------

# Function to apply system updates and upgrades
def apply_updates():
    print("\n🔄 Apply latest Updates \n")

    # Step 1: Check updates
    step1 = "Checking for updates"
    if log_output(["apt-get", "update", "-y"], step1, "Apply latest Updates"):
        print("✅ Task1: System update check completed successfully.\n")
    else:
        print("❌ Task1: Failed to check for updates. See 'result.log' for details.\n")
        print_summary()
        return False

    # Step 2: Apply system upgrades
    step2 = "Applying system upgrades"
    if log_output(["apt-get", "upgrade", "-y"], step2, "Apply latest Updates"):
        print("✅ Task2: System upgraded successfully.\n")
    else:
        print("❌ Task2: System upgrade failed. See 'result.log' for details.\n")
        return False

    return True

# ---------------------------------------------

# Function to perform firewall configuration
def configure_ufw():
    print("🛡️ Configuring UFW Firewall \n")
    
    if install_ufw() and configure_firewall():
        print("✅ Task1: UFW firewall installed and configured.\n")
    else:
        print("❌ Task1: UFW firewall configuration failed. Check 'result.log' for details.\n")
        return False

    return True

# ---------------------------------------------

# Function to clear the log file before starting
def clear_log():
    open(LOG_FILE, "w").close()



def about():
    description = """
    NixVault is a comprehensive Linux security hardening tool designed to safeguard your system from internal vulnerabilities and external threats. 
    Built with a focus on simplicity and power, NixVault automates best-practice configurations, manages sensitive data securely, and reinforces system integrity.
    """
    print(description)
# ---------------------------------------------

# Main function that calls the above functions
def linux_hardening():
    # Clear the log file before starting
    clear_log()

    # Apply updates and upgrades
    if not apply_updates():
        return

    # Configure UFW Firewall
    if not configure_ufw():
        return

    # Print the summary of the tasks
    print_summary()

# ---------------------------------------------

if __name__ == "__main__":
    about() # Print about section of the program
    check_root()  # Ensure the script runs as root or with sudo
    linux_hardening()