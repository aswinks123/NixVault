import subprocess
from utils.logging import log_output
from configuration.config import LOG_FILE
import time


def enforce_password_policy():
    print("\n🔐 Setting Password Policies \n")
    time.sleep(1)
    success = True
    success &= log_output(["sed", "-i", "s/^PASS_MAX_DAYS.*/PASS_MAX_DAYS   31/", "/etc/login.defs"], 
               "Set max password age", "User Security")
    success &= log_output(["sed", "-i", "s/^PASS_MIN_DAYS.*/PASS_MIN_DAYS   2/", "/etc/login.defs"], 
               "Set min password age", "User Security")
    success &= log_output(["sed", "-i", "s/^PASS_WARN_AGE.*/PASS_WARN_AGE   7/", "/etc/login.defs"], 
               "Set password warning age", "User Security")
    if success:

        print(f"✅ Password Policies set Successfully")
    else:
        print(f"❌ Failed to apply Password Policies")

    return True
