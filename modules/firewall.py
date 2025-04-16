from utils.logging import log_output
import time

def install_ufw():
    """Install UFW Firewall"""
    return log_output(["apt-get", "install", "-y", "ufw"], "Installing UFW Firewall", "Configuring UFW Firewall")

def configure_firewall():
    """Configure UFW firewall rules"""
    success = True
    success &= log_output(["sh", "-c", "yes | ufw reset"], "Resetting UFW", "Configuring UFW Firewall")
    success &= log_output(["ufw", "default", "deny", "incoming"], "Set default deny incoming", "Configuring UFW Firewall")
    success &= log_output(["ufw", "default", "allow", "outgoing"], "Set default allow outgoing", "Configuring UFW Firewall")
    success &= log_output(["ufw", "allow", "ssh"], "Allowed SSH Port", "Configuring UFW Firewall")
    success &= log_output(["ufw", "allow", "https"], "Allowed SSH Port", "Configuring UFW Firewall")
    success &= log_output(["ufw", "--force", "enable"], "UFW activated & enabled on startup", "Configuring UFW Firewall")
    return success

def configure_ufw():
    """Main function for UFW configuration"""
    print("\n🛡️  Configuring UFW Firewall \n")
    time.sleep(1)
    
    if install_ufw() and configure_firewall():
        print("✅ Task1: UFW firewall installed and configured.\n")
    else:
        print("❌ Task1: UFW firewall configuration failed. Check 'result.log' for details.\n")
        return False

    return True