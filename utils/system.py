import os

def check_root():
    """Check if the script is run as root"""
    if os.geteuid() != 0:
        print("\n❌ This script must be run as root. Re-running with sudo or switch to root!")
        exit(1)
    else:
        print("\n✅ Running as root or with privilaged access.\n")