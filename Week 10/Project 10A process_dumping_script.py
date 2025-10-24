#process_details.py
#we are using pids() and process() from psutils to check for all the 'netstat' functionlity. psutil has a huge collection
#of very useful utility functions which are woth exploring.
import psutil
import random

class ProcessDetails:
    def print_process_details(self) -> None:
        print('Printing all the PIDs:')
        print(psutil.pids())
        pid = random.choice(psutil.pids())
        print('\nPrinting details about a randomly selected process:')
        print('Process Id (PID):', pid)
        process = psutil.Process(pid)
        print('\n==== Process basic details ====')
        print('\n--- Process name: ', process.name())
        print('\n--- Process status: ', process.status())
        print('\n--- Process username (started as): ', process.username())
        print('\n--- Process created at: ', process.create_time())
        print('\n--- Process executable: ', process.exe())
        print('\n--- Process working directory: ', process.cwd())
        print('\n--- Process command line: ', process.cmdline())
        print('\n--- Process children: ', process.children(recursive=True))
        print('\n--- Process parent: ', process.parent())
        print('\n=== Process memory and CPU information ===')
        print('\n--- Process CPU percent: ', process.cpu_percent())
        print('\n--- Process CPU times (accumulated CPU time): ', process.cpu_times())
        print('\n--- Process memory percent: ', process.memory_percent())
        print('\n--- Process memory info: ', process.memory_info())

if  __name__ == "__main__":
    details = ProcessDetails()
    details.print_process_details()
    