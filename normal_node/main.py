import os
import socket
import time
import random
from datetime import datetime
import csv

TARGET_IP = "172.20.0.100"
PORT = 9999
NODE_ID = os.getenv("NODE_ID", "nodeX")
MY_IP = os.getenv("MY_IP", "172.20.0.XX")
BASE_RANK = int(os.getenv("BASE_RANK", 3))
LOG_FILE = "logs/normal_nodes.csv"

# Ensure logs directory exists and log file is initialized
file_exists = os.path.isfile(LOG_FILE)
log = open(LOG_FILE, "a", newline="")
writer = csv.writer(log)

if not file_exists:
    writer.writerow(["timestamp","node_id","src","event","info"])
    log.flush()

# set up socket for sending DIO and DIS messages
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
last_dis = time.time()


def send_dio():
    rank = BASE_RANK + random.choice([-1, 0, 1])
    rank = max(1, rank)
    payload = f"DIO|rank={rank}|parent=root".encode()
    sock.sendto(payload, (TARGET_IP, PORT))
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] [NORMAL] Sent DIO rank={rank}")
    writer.writerow([now, NODE_ID, MY_IP, "DIO",f"rank={rank}"])
    log.flush()



def send_dis():
    payload = b"DIS:Requesting DIO"
    sock.sendto(payload, (TARGET_IP, PORT))
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] [NORMAL] Sent DIS request")
    writer.writerow([ now, NODE_ID, MY_IP, "DIS", "request"])
    log.flush()


print("--- NORMAL NODE STARTED ---")
time.sleep(5)

while True:
    send_dio()

    # occasionally send DIS
    if time.time() - last_dis > random.randint(30, 45):
        send_dis()
        last_dis = time.time()

    time.sleep(random.randint(5, 10))