# IoT Intrusion Detection System (RPL Protocol)

## Overview
This project simulates an IoT network using the RPL protocol to demonstrate **Attack Detection** using an Anomaly-Based Intrusion Detection System (IDS).

It is based on the research paper: *"An Anomaly-Based IDS for Detecting Attacks in RPL-Based Internet of Things"*.

## Architecture
The simulation runs entirely in **Docker** containers:
* **Normal Nodes:** Simulate standard IoT sensor traffic (DIO/DAO messages).
* **Attacker:** Injects malicious packets (DIS Flooding, Neighbor Attacks).
* **IDS:** Sniffs network traffic and applies statistical thresholds to detect anomalies.

## Technologies
* Python 3.9
* Scapy (Packet manipulation)
* Docker & Docker Compose
* Linux Networking

## How to Run
1. `docker-compose build`
2. `docker-compose up`
