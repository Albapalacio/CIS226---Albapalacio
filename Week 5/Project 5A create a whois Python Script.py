import requests
import json
import whois as ws

class WhoisInfo:
    def __init__(self, host):
        self.host = host
        self.data = None  # None indicates no data available

    def fetch(self):
        # Ensure URL has http:// or https://
        url = self.host
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url  

        # Check if the page exists
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            print(f"The Page exists: {url}")

            # Fetch WHOIS info only if page exists
            try:
                info = ws.whois(self.host)
                self.data = {
                    "domain_name": info.get("domain_name"),
                    "registrar": info.get("registrar"),
                    "creation_date": str(info.get("creation_date")),
                    "expiration_date": str(info.get("expiration_date")),
                    "name_servers": info.get("name_servers")
                }
            except Exception as e:
                print(f"Error fetching WHOIS info for {self.host}: {e}")

        except requests.exceptions.RequestException as err:
            print(f"Page does not exist or cannot be reached: {err}")
            self.data = None  

    def print_json(self):
        if self.data:
            print(f"\nWHOIS Information for: {self.host}")
            print("=" * 60)
            print(json.dumps(self.data, indent=4))
        else:
            print(f"\nNo WHOIS data available because the page '{self.host}' does not exist.")

    def save_json(self):
        if self.data:
            filename = f"{self.host.replace('.', '_')}_whois.json"
            with open(filename, "w") as f:
                json.dump(self.data, f, indent=4)
            print("=" * 60)
            print(f"\n File saved as: {filename}\n")
        else:
            print(f"No file saved because the page '{self.host}' does not exist.")


if __name__ == "__main__":
    domain = input("Enter a domain: ").strip()
    whois_info = WhoisInfo(domain)
    whois_info.fetch()
    whois_info.print_json()
    whois_info.save_json()
