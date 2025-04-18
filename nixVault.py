#==================================================================================================================================================================

#DEVELOPER: Aswin KS
#DATE: 15-04-2025
#ABOUT: NixVault: NixVault is a comprehensive Linux security hardening tool designed to safeguard your system from internal vulnerabilities and external threats.
#Built with a focus on simplicity and power, NixVault automates best-practice configurations, manages sensitive data securely, and reinforces system integrity.

#==================================================================================================================================================================

from utils.ui import about, show_progress_bar
from utils.system import check_root
from utils.logging import clear_log, print_summary
from modules.updates import apply_updates
from modules.firewall import configure_ufw
from modules.services import disable_services
from modules.user_security import user_account_management
from modules.ssh import ssh_hardening
import time


def show_welcome():
    
    print("NixVault")
    print("Version: 1.0")
    print("Source code: https://github.com/aswinks123/NixVault")
    print("")
    print("\n📌 Following Tasks will be performed:\n")
    print("1. Apply Latest Updates")
    print("2. Configure UFW Firewall")
    print("3. Disable Insecure/Unnecessary Services")
    print("4. Enforce User Account Security (password policies)")
    print("5. SSH Security Hardening")
    print("6. Show Summary Report")

    print("")
    print("-" * 70)



def ask_confirmation():
    while True:
        choice = input("\n▶ Do you want to continue? (yes/no): ").strip().lower()
        if choice in ["yes", "y"]:
            return True
        elif choice in ["no", "n"]:
            print("\n❌ Exiting. No changes made.\n")
            return False
        else:
            print("Please enter 'yes' or 'no'.")




def linux_hardening():
    """Main hardening function"""
    clear_log()
    
    # if not apply_updates():
    #     return

    # if not configure_ufw():
    #     return
    
    # if not disable_services():
    #     return

    # if not user_account_management():     
    #     return
    
    if not ssh_hardening():     
        return  
    
    
    show_progress_bar()
    print_summary()

if __name__ == "__main__":
    try:

        about()
        check_root()
        show_welcome()
        if ask_confirmation():
            linux_hardening()
    except:
         print("\n\n⚠️  Interrupted by user. Exiting...\n")