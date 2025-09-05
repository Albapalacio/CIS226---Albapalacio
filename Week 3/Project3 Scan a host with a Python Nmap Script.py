import os
import nmap

# Ensure Nmap is in PATH for this session
os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Nmap"

class PortScanner:
    def __init__(self):
        self.scanner = nmap.PortScanner()

    def scan_top_ports(self, host, top_ports=10, show_only_open=False):
        print(f"\nScanning top {top_ports} ports for {host}...\n")
        # Run the scan
        self.scanner.scan(hosts=host, arguments=f"--top-ports {top_ports} -Pn")

        for host in self.scanner.all_hosts():
            print(f"Nmap scan report for {host}")
            print(f"Host is {self.scanner[host].state()}\n")

            for proto in self.scanner[host].all_protocols():
                ports = sorted(self.scanner[host][proto].keys())
                for port in ports:
                    state = self.scanner[host][proto][port]["state"]
                    service = self.scanner[host][proto][port].get("name", "unknown")

                    if show_only_open and state != "open":
                        continue  # skip non-open ports if user requested

                    print(f"Port {port}/{proto}\t{state}\t{service}")

        print("\nScan complete!")


if __name__ == "__main__":
    target_host = input("Enter the target host IP (or leave blank for default 52.234.30.228): ").strip()
    if not target_host:
        target_host = "52.234.30.228"

    try:
        top_ports = int(input("Enter the number of top ports to scan (e.g., 5, 10, 15): ").strip())
    except ValueError:
        top_ports = 10

    show_only_open = input("Show only open ports? (yes/no): ").strip().lower() == "yes"

    scanner = PortScanner()
    scanner.scan_top_ports(target_host, top_ports, show_only_open)
