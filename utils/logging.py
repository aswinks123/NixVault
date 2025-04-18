import subprocess
from configuration.config import LOG_FILE
import time
from datetime import datetime

summary = {}

def clear_log():
    """Clear the log file before starting"""
    open(LOG_FILE, "w").close()


    # Get the current time
    current_time = datetime.now()

    # Print the current time
    print("Current time:", current_time.strftime("%Y-%m-%d %H:%M:%S \n\n"))

    with open(LOG_FILE, "a") as log:
        log.write(current_time.strftime("%Y-%m-%d %H:%M:%S"))


def log_output(command, task_name, section_name):

    """Run commands and log output to result.log file and in summary dictionary"""
    with open(LOG_FILE, "a") as log:
        log.write(f"\n--->{task_name}  <success>\n")
        result = subprocess.run(command, stdout=log, stderr=log)
    
    # Store each task's result in the summary dictionary
    if section_name not in summary:
        summary[section_name] = []
    summary[section_name].append((task_name, result.returncode == 0))
    return result.returncode == 0

def print_summary():
    """Print the summary of operations"""
    print("-" * 158)
    print("\n📝 Summary Report:")
    print("-" * 158)
    time.sleep(1)

    for section, tasks in summary.items():
        print(f"\n{section}:\n" + "-" * len(section))
        for task, result in tasks:
            status = "✅ Success" if result else "❌ Failed"
            #print(f"{task:<50} {status}")
            print(f"{task:<120} {status:>36}")
    
    print("-" * 158)
    print("🔍 See result located at 'logs/result.log' for more details.\n")