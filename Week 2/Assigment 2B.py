"""
Assignment 2B 
This script uses Python with os, json, and subprocess to run
PowerShell commands that list scheduled tasks in JSON format.
"""

import os
import json
import subprocess


def get_scheduled_tasks():
    # PowerShell command to export scheduled tasks as JSON
    command = [
        "powershell",
        "-Command",
        "Get-ScheduledTask | Select-Object TaskName | ConvertTo-Json"
    ]

    try:
        # Run the command and capture output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        # Convert JSON string to Python object
        tasks = json.loads(result.stdout)  

        # If tasks is a dict (single object), put it in a list
        if isinstance(tasks, dict):
            tasks = [tasks]

        # Extract just the TaskName values
        task_names = [task["TaskName"] for task in tasks if "TaskName" in task]
        return task_names

    except Exception as e:
        print(f"Error retrieving tasks: {e}")
        return []

# Save the current scheduled tasks as the baseline.
def create_baseline(filename="baseline_tasks.json"):
    
    tasks = get_scheduled_tasks()
    print(f"impresion tasks {tasks}")
    with open(filename, "w") as f:
        json.dump(tasks, f, indent=4)
    print(f"Baseline saved with {len(tasks)} tasks.")
 

#Compare current scheduled tasks against baseline, and print new tasks
def check_for_new_tasks(filename="baseline_tasks.json"):
    
    # Load baseline
    if not os.path.exists(filename):
        print("No baseline found. Run create_baseline() first.")
        return

    with open(filename, "r") as f:
        baseline_tasks = json.load(f)

    # Get current tasks
    current_tasks = get_scheduled_tasks()

    # Find differences
    new_tasks = [task for task in current_tasks if task not in baseline_tasks]

    if new_tasks:
        print("⚠️ New scheduled tasks detected (investigate these):")
        for task in new_tasks:
            print(f" - {task}")
    else:
        print("No new scheduled tasks found. System is clean.")


# --------- MAIN SCRIPT ----------
if __name__ == "__main__":
    print("Scheduled Task Monitor")

    # Uncomment one of the lines below depending on what you want to do:
    # Step 1: Run once to create baseline
    #create_baseline()

    # Step 2: Run later to detect new tasks
    check_for_new_tasks()
   
    
   