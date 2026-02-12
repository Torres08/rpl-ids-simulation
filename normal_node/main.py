import os
import socket
import time
import random
from datetime import datetime

TARGET_IP = "172.20.0.100"
PORT = 9999
BASE_RANK = int(os.getenv("BASE_RANK", 3))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
last_dis = time.time()


def send_dio():
    rank = BASE_RANK + random.choice([-1, 0, 1])
    rank = max(1, rank)

    payload = f"DIO|rank={rank}|parent=root".encode()
    sock.sendto(payload, (TARGET_IP, PORT))

    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] [NORMAL] Sent DIO rank={rank}")


def send_dis():
    payload = b"DIS:Requesting DIO"

    sock.sendto(payload, (TARGET_IP, PORT))

    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] [NORMAL] Sent DIS request")


print("--- NORMAL NODE STARTED ---")
time.sleep(5)

while True:
    send_dio()

    # occasionally send DIS
    if time.time() - last_dis > random.randint(30, 45):
        send_dis()
        last_dis = time.time()

    time.sleep(random.randint(5, 10))