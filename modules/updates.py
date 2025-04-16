from utils.logging import log_output
import time

def apply_updates():
    """Apply system updates and upgrades"""
    print("\n🔄 Apply latest Updates \n")
    time.sleep(1)
    
    # Step 1: Check updates
    step1 = "Checking for updates"
    if log_output(["apt-get", "update", "-y"], step1, "Apply latest Updates"):
        print("✅ Task1: System update check completed successfully.\n")
    else:
        print("❌ Task1: Failed to check for updates. See 'result.log' for details.\n")
        return False

    # Step 2: Apply system upgrades
    step2 = "Applying system upgrades"
    if log_output(["apt-get", "upgrade", "-y"], step2, "Apply latest Updates"):
        print("✅ Task2: System upgraded successfully.\n")
    else:
        print("❌ Task2: System upgrade failed. See 'result.log' for details.\n")
        return False

    return True