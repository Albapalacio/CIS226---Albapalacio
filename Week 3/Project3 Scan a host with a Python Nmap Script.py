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

        for h in self.scanner.all_hosts():
            print(f"Nmap scan report for {h}")
            print(f"Host state {self.scanner[h].state()}\n")

            for p in self.scanner[h].all_protocols():
                ports = sorted(self.scanner[h][p].keys())
                for port in ports:
                    state = self.scanner[h][p][port]["state"]
                    service = self.scanner[h][p][port].get("name", "unknown")

                    if show_only_open and state != "open":
                        continue  # skip non-open ports if user requested

                    print(f"Port {port}/{p}\t{state}\t{service}")

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
