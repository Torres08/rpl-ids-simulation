import socket
import time
import statistics
from datetime import datetime

PORT = 9999
WINDOW_TIME = 10
TRAINING_WINDOWS = 6      # <-- number of normal windows to learn baseline

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))

print("IDS started...")

baseline_counts = []
baseline_ready = False

mu = 0
sigma = 0
threshold = 0

current_count = 0
start_time = time.time()

while True:
    sock.settimeout(1)

    try:
        data, addr = sock.recvfrom(2048)
        msg = data.decode()

        if "DIS" in msg:
            current_count += 1

    except socket.timeout:
        pass

    # ---- Window finished ----
    if time.time() - start_time >= WINDOW_TIME:

        print("\n===== IDS WINDOW CHECK =====")
        print(f"count={current_count}")

        # -------------------------
        # TRAINING PHASE
        # -------------------------
        if not baseline_ready:
            baseline_counts.append(current_count)
            print(f"[TRAINING] window {len(baseline_counts)}/{TRAINING_WINDOWS}")

            if len(baseline_counts) == TRAINING_WINDOWS:
                mu = statistics.mean(baseline_counts)
                sigma = statistics.stdev(baseline_counts) if len(baseline_counts) > 1 else 0
                threshold = mu + 3 * sigma

                baseline_ready = True

                print("\n✅ BASELINE LEARNED")
                print(f"μ={mu:.2f}  σ={sigma:.2f}  threshold={threshold:.2f}")

        # -------------------------
        # DETECTION PHASE
        # -------------------------
        else:
            print(f"μ={mu:.2f}  σ={sigma:.2f}  threshold={threshold:.2f}")

            if current_count > threshold:
                now = datetime.now().strftime("%H:%M:%S")
                print(f"[{now}] 🚨 ALERT: DIS Flood detected!")

        current_count = 0
        start_time = time.time()
