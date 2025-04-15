import subprocess #module is used to execute system-level commands in Python
import sys #This module provides access to system-specific parameters and functions

#---------------------------------------------

LOG_FILE = "result.log"
summary = {}

def log_output(command, task_name, section_name):
    with open(LOG_FILE, "a") as log:
        log.write(f"\n====={task_name}=====\n")
        result = subprocess.run(command, stdout=log, stderr=log)
    # Store each task's result in the summary dictionary, categorized by section
    if section_name not in summary:
        summary[section_name] = []
    summary[section_name].append((task_name, result.returncode == 0))
    return result.returncode == 0
#---------------------------------------------

def install_ufw():
    return log_output(["apt-get", "install", "-y", "ufw"], "Installing UFW Firewall", "Configuring UFW Firewall")

def setup_firewall():
    success = True
    success &= log_output(["ufw", "default", "deny", "incoming"], "Set default deny incoming", "Configuring UFW Firewall")
    success &= log_output(["ufw", "default", "allow", "outgoing"], "Set default allow outgoing", "Configuring UFW Firewall")
    success &= log_output(["ufw", "allow", "ssh"], "Allowed SSH Port", "Configuring UFW Firewall")
    success &= log_output(["ufw", "--force", "enable"], "UFW activated & enabled on startup", "Configuring UFW Firewall")
    return success
#---------------------------------------------

def print_summary():
    print("\n📋 Summary Report:")
    print("-" * 80)

    # Iterate through each section in the summary
    for section, tasks in summary.items():
        print(f"\n{section}:\n" + "-" * len(section))
        for task, result in tasks:
            status = "✅ Success" if result else "❌ Failed"
            print(f"{task:<50} {status}")
        print("-" * len(section))  # Print a line after each section
    
    print("-" * 80)
    print("🔍 See 'result.log' for more details.\n")    

#---------------------------------------------

def linux_hardening():
    # ✅ Clear the log file before starting
    open(LOG_FILE, "w").close()

    print("🔄 Apply latest Updates \n")

    # Step 1: Check updates
    step1 = "Step 1: Checking for updates"
    if log_output(["apt-get", "update", "-y"], step1, "Apply latest Updates"):
        print("✅ Task 1: System update check completed successfully.\n")
    else:
        print("❌ Task 1: Failed to check for updates. See 'result.log' for details.\n")
        print_summary()
        return

    # Step 2: Apply system upgrades
    step2 = "Step 2: Applying system upgrades"
    if log_output(["apt-get", "upgrade", "-y"], step2, "Apply latest Updates"):
        print("✅ Task 2: System upgraded successfully.\n")
    else:
        print("❌ Task 2: System upgrade failed. See 'result.log' for details.\n")

    # Step 3: UFW Firewall Setup
    print("🛡️ Configuring UFW Firewall \n")
    firewall_step = "Step 3: Firewall installation & config"
    if install_ufw() and setup_firewall():
        print("✅ Task 1: UFW firewall installed and configured.\n")
    else:
        print("❌ Task 1: UFW firewall configuration failed. Check 'result.log' for details.\n")

    print_summary()    

#---------------------------------------------
if __name__ == "__main__":
    linux_hardening()
