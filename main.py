#==================================================================================================================================================================

#DEVELOPER: Aswin KS
#DATE: 15-04-2025
#ABOUT: NixVault: NixVault is a comprehensive Linux security hardening tool designed to safeguard your system from internal vulnerabilities and external threats.
#Built with a focus on simplicity and power, NixVault automates best-practice configurations, manages sensitive data securely, and reinforces system integrity.

#==================================================================================================================================================================

import subprocess  # module is used to execute system-level commands in Python
import sys  # This module provides access to system-specific parameters and functions
import os
import time
#---------------------------------------------< General configurations >

LOG_FILE = "result.log"
summary = {}

# Function to clear the log file before starting
def clear_log():
    open(LOG_FILE, "w").close()

#---------------------------------------------< Function to create an ASCII art and description for the program >

# Function to add ASCII art and about
def about():
    logo = r"""
  _   _ _    __      __         _ _   
 | \ | (_)   \ \    / /        | | |  
 |  \| |___  _\ \  / /_ _ _   _| | |_ 
 | . ` | \ \/ /\ \/ / _` | | | | | __|
 | |\  | |>  <  \  / (_| | |_| | | |_ 
 |_| \_|_/_/\_\  \/ \__,_|\__,_|_|\__|
                                      
                                      

                ~ NixVault - Created by Aswin KS ~
    """
    
    description = """
NixVault is a comprehensive Linux security hardening tool designed to safeguard your system from internal vulnerabilities and external threats. 
Built with a focus on simplicity and power, NixVault automates best-practice configurations, manages sensitive data securely, and reinforces system integrity.
    """

    print(logo)
    print(description)
    print("-" * 158)
# ---------------------------------------------< Function to check whether the user is running with sudo privilage >

# function to check if the script is run as root
def check_root():
    if os.geteuid() != 0:
        print("\n❌ This script must be run as root. Re-running with sudo or switch to root!")
        # Exit the program
        exit(1)
        
    else:
        print("\n✅ Running as root or with privilaged access.\n")

# --------------------------------------------< Function to run commands and log the output to result.log file and in summary dictionary >

# function to run commands and log output (Here is where actual comamnds are run)
def log_output(command, task_name, section_name):
    with open(LOG_FILE, "a") as log:
        log.write(f"\n====={task_name}=====\n")
        result = subprocess.run(command, stdout=log, stderr=log)
    
    # Store each task's result in the summary dictionary, categorized by section
    if section_name not in summary:
        summary[section_name] = []
    summary[section_name].append((task_name, result.returncode == 0))
    return result.returncode == 0

# ---------------------------------------------< Function to create a progress bar >

#function to create a progress bar for summay report-(for visual representation)
def show_progress_bar(seconds=5, message="\n\n⏳ Generating Summary Report. Please wait..."):
    print(message)
    for i in range(seconds):
        time.sleep(1)
        bar = "#" * (i + 1) + "-" * (seconds - i - 1)
        sys.stdout.write(f"\r[{bar}] {i+1}/{seconds}s")
        sys.stdout.flush()
    print("\n")  # Newline after progress bar finishes

# ---------------------------------------------< Function to install and configure ufw firewall >

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

# ---------------------------------------------< Function to print summary report >

# Function to print the summary
def print_summary():
    print("\n📋 Summary Report:")
    print("-" * 158)
    time.sleep(1)

    # Iterate through each section in the summary
    for section, tasks in summary.items():
        print(f"\n{section}:\n" + "-" * len(section))
        for task, result in tasks:
            status = "✅ Success" if result else "❌ Failed"
            print(f"{task:<50} {status}")
    
    print("-" * 158)
    print("🔍 See 'result.log' for more details.\n")

# ---------------------------------------------< Function to update the system >

# Function to apply system updates and upgrades
def apply_updates():
    
    print("\n🔄 Apply latest Updates \n")
    time.sleep(1)
    
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

# --------------------------------------------- < Function to configure ufw firewall >

# Function to perform firewall configuration
def configure_ufw():
    
    print("\n🛡️ Configuring UFW Firewall \n")
    time.sleep(1)
    
    if install_ufw() and configure_firewall():
        print("✅ Task1: UFW firewall installed and configured.\n")
    else:
        print("❌ Task1: UFW firewall configuration failed. Check 'result.log' for details.\n")
        return False

    return True

# ---------------------------------------------< Function to disable unwanted services >

# Function to disable unwanted services
def disable_services():
    
    print("\n🔧 Disabling Unnecessary Services \n")
    time.sleep(1)

    # List of services to disable with descriptions
    services_to_disable = [
        ("telnet", "Insecure remote login service"),
        ("cups", "Printing service (often unnecessary on servers)"),
        ("nginx", "Webserver (Not needed by default)"),
        ("snapd.service", "Not useful for remote servers - Optional"),
        ("rsh", "Remote shell service (insecure)"),
        ("rlogin", "Remote login service (insecure)"),
        ("rexec", "Remote execution service (insecure)")
    ]
    
    all_success = True

    for service, description in services_to_disable:
        try:
            # Check if service exists and is enabled
            check_enabled = subprocess.run(["systemctl", "is-enabled", service], 
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE) 
            check_active = subprocess.run(["systemctl", "is-active", service], 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)
            
            if check_enabled.returncode == 0 or check_active.returncode == 0:  # Service is enabled or active
                print(f"ℹ️ Attempting to disable {service} ({description})")
                
                # Stop the service
                stop_ok = log_output(["systemctl", "stop", service], 
                                   f"Stopping {service}", 
                                   "Service Hardening")

                # Disable service from startup
                disable_ok = log_output(["systemctl", "disable", service], 
                                      f"Disabling {service}", 
                                      "Service Hardening")

                if stop_ok and disable_ok:
                    print(f"✅ Successfully disabled {service}")
                else:
                    print(f"❌ Failed to disable {service}")
                    all_success = False
            else:
                print(f"ℹ️ {service} is not enabled or not present (skipping)")
                
        except Exception as e:
            print(f"⚠️ Error processing {service}: {str(e)}")
            all_success = False
    
    return all_success

# ---------------------------------------------< Main Function >

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
    
    # Disabling and stopping unwanted services
    if not disable_services():
        return

    # Print the summary of the tasks
    show_progress_bar()
    print_summary()


# ---------------------------------------------< Program starts here >

if __name__ == "__main__":
    about() # Print about section of the program
    check_root()  # Ensure the script runs as root or with sudo
    linux_hardening()