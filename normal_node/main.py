import time
import random
from datetime import datetime
from scapy.all import *

# CONFIGURATION
TARGET_IP = "172.20.0.100"
MY_IP = "172.20.0.11"

def send_dio():
    payload = b"\x01:DIO:Rank=2:Parent=Root"
    pkt = IP(src=MY_IP, dst=TARGET_IP)/UDP(dport=9999)/Raw(load=payload)
    send(pkt, verbose=0)
    
    
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] [NORMAL] Sent DIO Heartbeat to {TARGET_IP}")

if __name__ == "__main__":
    print("--- NORMAL NODE STARTED ---")
    time.sleep(5)
    while True:
        send_dio()
        time.sleep(random.randint(5, 10))