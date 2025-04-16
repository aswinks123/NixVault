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
from modules.user_security import enforce_password_policy, disable_root_ssh
import time


def show_welcome():
    
    print("NixVault")
    print("Version: 1.0")
    print("Source code: https://github.com/aswinks123/NixVault")
    print("")
    print("\nThis script will perform the following tasks:\n")
    print("1. 🔄 Apply System Updates")
    print("2. 🛡️  Configure UFW Firewall")
    print("3. ⚙️  Disable Insecure/Unnecessary Services")
    print("4. 🔐 Enforce User Account Security (password policies, SSH root login)")
    print("5. 📄 Show Summary Report")
    print("")
    print("-" * 70)



def ask_confirmation():
    while True:
        choice = input("\n▶️  Do you want to continue? (yes/no): ").strip().lower()
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
    
    if not apply_updates():
        return

    if not configure_ufw():
        return
    
    if not disable_services():
        return

    if not enforce_password_policy():     
        return
    
    if not disable_root_ssh():     
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