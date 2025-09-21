import os
import json
from shodan import Shodan, APIError

#Read API key from environment variable
def get_shodan_client():
    api_key = os.environ.get("SHODAN_API_KEY")
    if not api_key:
        api_key = input("Enter your Shodan API key: ").strip()
    return Shodan(api_key)

#Return a dict with the most interesting keys 
def parse_host_record(rec: dict) -> dict:
    parsed = {
        "ip": rec.get("ip_str") or rec.get("ip"),
        "org": rec.get("org"),
        "asn": rec.get("asn"),
        "hostnames": rec.get("hostnames") or [],
        "open_ports": rec.get("ports") or [],
        "location": rec.get("location") or {},
        "vulns": [],
        "services": []
    }

    # Normalize vulnerabilities
    vulns = rec.get("vulns")
    if isinstance(vulns, dict):
        parsed["vulns"] = list(vulns.keys())
    elif isinstance(vulns, list):
        parsed["vulns"] = vulns

    # Extract service banners
    for svc in rec.get("data", []):
        service_info = {
            "port": svc.get("port"),
            "transport": svc.get("transport"),
            "product": svc.get("product"),
            "version": svc.get("version"),
            "banner_snippet": (svc.get("data")[:200] + "...") if svc.get("data") else None
        }
        if svc.get("ssl"):
            cert = svc.get("ssl", {}).get("cert", {})
            service_info["ssl_subject"] = cert.get("subject")
            service_info["ssl_alt_names"] = cert.get("alt_names")
        parsed["services"].append(service_info)

    return parsed

#Handles Shodan parsing, printing, and saving
class ShodanHostDetails:
    def __init__(self, client):
        self.client = client

    #Return raw host dict 
    def get_raw_host(self, ip_address: str) -> dict:
        return self.client.host(ip_address)

    #print parsed JSON, and save to files
    def print_host_details(self, ip_address: str):
        try:
            raw = self.get_raw_host(ip_address)
        except APIError as e:
            print(f"Shodan API error: {e}")
            return
        except Exception as e:
            print(f"Unexpected error: {e}")
            return

        parsed = parse_host_record(raw)

        print("\nParsed host info:")
        print(json.dumps(parsed, indent=2, ensure_ascii=False))

        # Save both raw and parsed outputs
        safe_name = ip_address.replace(":", "_")
        raw_file = f"shodan_host_raw_{safe_name}.json"
        parsed_file = f"shodan_host_parsed_{safe_name}.json"

        with open(raw_file, "w", encoding="utf-8") as f:
            json.dump(raw, f, indent=2, ensure_ascii=False)
        with open(parsed_file, "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=2, ensure_ascii=False)

        print(f"\nSaved raw JSON: {raw_file}")
        print(f"Saved parsed JSON: {parsed_file}")

if __name__ == "__main__":
    client = get_shodan_client()
    sh = ShodanHostDetails(client)
    ip = input("Enter IP address to lookup (e.g., 8.8.8.8): ").strip()
    if ip:
        sh.print_host_details(ip)
    else:
        print("No IP provided. Exiting.")