import socket
import time
import random
import os
from datetime import datetime
import csv

TARGET_IP = "172.20.0.100"
PORT = 9999
LOG_FILE = "logs/neighbor_attack.csv"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

os.makedirs("logs", exist_ok=True)
log = open(LOG_FILE, "a", newline="")
writer = csv.writer(log)

if os.stat(LOG_FILE).st_size == 0:
    writer.writerow(["timestamp","event","src","dst","info"])

print("Neighbor attack started (fake best parent)")

while True:
    payload = b"DIO|rank=0|parent=attacker"
    sock.sendto(payload, (TARGET_IP, PORT))
    time.sleep(random.uniform(4, 8))  # normal timing
    now = datetime.now().strftime("%H:%M:%S")
    writer.writerow([now, "DIO_ATTACK", os.getenv("MY_IP", "172.20.0.XX"), TARGET_IP, "rank=0"])
    log.flush()



