import requests
import os
import json

# Read API key from environment variable
def get_virustotal_apikey():
    api_key = os.environ.get("VIRUSTOTAL_API_KEY")
    if not api_key:
        api_key = input("Enter your VIRUS TOTAL API key: ").strip()
    return api_key


def check_hash(hash_value, api_key):
    url = f"https://www.virustotal.com/api/v3/files/{hash_value}"
    headers = {"x-apikey": api_key}
    response = requests.get(url, headers=headers)
    print(f"\n[DEBUG] Response code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        stats = result.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
        print("VirusTotal Report for File Hash:")
        print(json.dumps(stats, indent=4))  # Beautify results
    else:
        print(f"Error {response.status_code}: {response.text}")


def check_ip(ip_address, api_key):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}"
    headers = {"x-apikey": api_key}
    response = requests.get(url, headers=headers)
    print(f"\n[DEBUG] Response code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        stats = result.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
        print("VirusTotal Report for IP Address:")
        print(json.dumps(stats, indent=4))
    else:
        print(f"Error {response.status_code}: {response.text}")


if __name__ == "__main__":
    API_KEY = get_virustotal_apikey()

    print("\nChoose check type:")
    print("1. Check File Hash (MD5, SHA1, SHA256)")
    print("2. Check IP address")

    choice = input("Enter choice (1/2): ").strip()

    if choice == "1":
        hash_to_check = input("\nEnter file hash to check: ").strip()
        check_hash(hash_to_check, API_KEY)

    elif choice == "2":
        ip_to_check = input("\nEnter an IP address to check: ").strip()
        check_ip(ip_to_check, API_KEY)

    else:
        print("Invalid choice. Exiting.")

