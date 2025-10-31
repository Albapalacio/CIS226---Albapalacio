from scapy.all import IP, TCP, send
import time

TARGET = "52.234.30.228"   # <- IP of my teacher
DPORT = 80
SPORT = 12345

ip_layer = IP(dst=TARGET)
tcp_layer = TCP(dport=DPORT, sport=SPORT, flags="S")

##HTTP GET with personalized payload
http_payload = (
    "GET /index.html HTTP/1.1\r\n"
    f"Host: {TARGET}\r\n"
    "User-Agent: ScapyTest/1.0\r\n"
    "Accept: */*\r\n"
    "Custom-Payload: This is a payload for the assignment\r\n"
    "\r\n"
)

packet = ip_layer / tcp_layer / http_payload

print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Sending 1 crafted packet to {TARGET}:{DPORT}")
send(packet)
print("Sent 1 packet.")
print("\n--- Payload sent ---\n")
print(http_payload)
