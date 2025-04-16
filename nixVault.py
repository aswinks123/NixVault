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
from modules.user_security import enforce_password_policy
import time

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

    show_progress_bar()
    print_summary()

if __name__ == "__main__":
    about()
    check_root()
    linux_hardening()