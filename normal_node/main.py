import socket
import time
import random
from datetime import datetime

TARGET_IP = "172.20.0.100"
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
last_dis = time.time()


def send_dio():
    payload = b"DIO:Rank=2:Parent=Root"

    sock.sendto(payload, (TARGET_IP, PORT))

    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] [NORMAL] Sent DIO heartbeat")

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