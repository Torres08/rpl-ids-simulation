import socket
import time
import statistics
from datetime import datetime

PORT = 9999
WINDOW_TIME = 10
TRAINING_WINDOWS = 10

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))

print("IDS started...")

# =========================
# Baseline containers
# =========================
dis_baseline = []
dio_baseline = []
rank_baseline = []

baseline_ready = False

mu_dis = sigma_dis = thr_dis = 0
mu_dio = sigma_dio = thr_dio = 0
mu_rank = sigma_rank = 0

# =========================
# Current window counters
# =========================
dis_count = 0
dio_count = 0
rank_values = []

start_time = time.time()


# =====================================================
# MAIN LOOP
# =====================================================
while True:
    sock.settimeout(1)

    try:
        data, addr = sock.recvfrom(2048)
        msg = data.decode()

        # -------------------------
        # Packet classification
        # -------------------------
        if "DIS" in msg:
            dis_count += 1

        if "DIO" in msg:
            dio_count += 1

            # extract rank if present
            if "rank=" in msg:
                try:
                    rank = int(msg.split("rank=")[1].split("|")[0])
                    rank_values.append(rank)
                except:
                    pass

    except socket.timeout:
        pass


    # =====================================================
    # WINDOW END
    # =====================================================
    if time.time() - start_time >= WINDOW_TIME:

        print("\n===== IDS WINDOW CHECK =====")
        print(f"DIS={dis_count}  DIO={dio_count}")

        # =================================================
        # TRAINING PHASE
        # =================================================
        if not baseline_ready:

            dis_baseline.append(dis_count)
            dio_baseline.append(dio_count)

            if rank_values:
                rank_baseline.extend(rank_values)

            print(f"[TRAINING] window {len(dis_baseline)}/{TRAINING_WINDOWS}")

            if len(dis_baseline) >= TRAINING_WINDOWS:

                # DIS baseline
                mu_dis = statistics.mean(dis_baseline)
                sigma_dis = statistics.stdev(dis_baseline) if len(dis_baseline) > 1 else 0
                thr_dis = mu_dis + 3 * sigma_dis

                # DIO baseline
                mu_dio = statistics.mean(dio_baseline)
                sigma_dio = statistics.stdev(dio_baseline) if len(dio_baseline) > 1 else 0
                thr_dio = mu_dio + 3 * sigma_dio

                # Rank baseline
                if rank_baseline:
                    mu_rank = statistics.mean(rank_baseline)
                    sigma_rank = statistics.stdev(rank_baseline) if len(rank_baseline) > 1 else 0

                baseline_ready = True

                print("\n✅ BASELINES LEARNED")
                print(f"DIS → μ={mu_dis:.2f} σ={sigma_dis:.2f} thr={thr_dis:.2f}")
                print(f"DIO → μ={mu_dio:.2f} σ={sigma_dio:.2f} thr={thr_dio:.2f}")
                print(f"Rank→ μ={mu_rank:.2f} σ={sigma_rank:.2f}")

        # =================================================
        # DETECTION PHASE
        # =================================================
        else:

            now = datetime.now().strftime("%H:%M:%S")

            print(f"DIS thr={thr_dis:.2f} | DIO thr={thr_dio:.2f}")

            # -------- DIS flood --------
            if dis_count > thr_dis:
                print(f"[{now}] 🚨 ALERT: DIS Flood detected!")

            # -------- Neighbor/DIO flood --------
            if dio_count > thr_dio:
                print(f"[{now}] 🚨 ALERT: Neighbor/DIO Flood detected!")

            # -------- Rank anomaly --------
            if rank_values and sigma_rank > 0:
                for r in rank_values:
                    if r < (mu_rank - 3 * sigma_rank):
                        print(f"[{now}] 🚨 ALERT: Suspicious low rank detected ({r})")
                        break


        # reset window
        dis_count = 0
        dio_count = 0
        rank_values = []
        start_time = time.time()
