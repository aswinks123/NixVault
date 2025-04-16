import subprocess
from utils.logging import log_output
import time

def disable_services():
    """Disable unnecessary services"""
    print("\n🔧 Disabling Unnecessary Services \n")
    time.sleep(1)

    services_to_disable = [
        ("telnet", "Insecure remote login service"),
        ("cups", "Printing service (often unnecessary on servers)"),
        ("nginx", "Webserver"),
        ("apache2", "Webserver"),
        ("rsh", "Remote shell service (insecure)"),
        ("rlogin", "Remote login service (insecure)"),
        ("rexec", "Remote execution service (insecure)")
    ]
    
    all_success = True

    for service, description in services_to_disable:
        try:
            check_enabled = subprocess.run(["systemctl", "is-enabled", service], 
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE) 
            check_active = subprocess.run(["systemctl", "is-active", service], 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)
            
            if check_enabled.returncode == 0 or check_active.returncode == 0:
                print(f"ℹ️ Attempting to disable {service} ({description})")
                
                stop_ok = log_output(["systemctl", "stop", service], 
                                   f"Stopping {service}", 
                                   "Service Hardening")

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