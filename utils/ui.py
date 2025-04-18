import time
import sys

def about():
    """Display ASCII art and description"""
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

def show_progress_bar(seconds=3, message="\n\n⏳ Generating Summary Report. Please wait..."):
    """Display a progress bar"""
    print(message)
    for i in range(seconds):
        time.sleep(1)
        bar = "#" * (i + 1) + "-" * (seconds - i - 1)
        sys.stdout.write(f"\r[{bar}] {i+1}/{seconds}s")
        sys.stdout.flush()
    print("\n")