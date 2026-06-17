import csv
import os
import time
from datetime import datetime

import requests


API_URL = os.getenv("API_URL")
N = 1000
WAIT_SECONDS = 900
ROUNDS = 5
OUTPUT_FILE = "results/coldstart_n1000.csv"


def load_env():
    global API_URL

    if API_URL:
        return

    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("API_URL="):
                    API_URL = line.strip().split("=", 1)[1]


def invoke(label, round_id):
    start = time.perf_counter()
    response = requests.post(API_URL, json={"n": N}, timeout=30)
    elapsed_ms = (time.perf_counter() - start) * 1000

    data = response.json()

    row = {
        "timestamp": datetime.now().isoformat(),
        "round_id": round_id,
        "label": label,
        "n": N,
        "status_code": response.status_code,
        "client_latency_ms": round(elapsed_ms, 3),
        "function_time_ms": data.get("execution_time_ms"),
        "prime_count": data.get("prime_count"),
    }

    print(row)
    return row


def main():
    load_env()

    if not API_URL:
        raise RuntimeError("API_URL is not defined. Create .env with API_URL=...")

    os.makedirs("results", exist_ok=True)

    rows = []

    for round_id in range(1, ROUNDS + 1):
        print(f"\nRound {round_id}/{ROUNDS}")
        print(f"Waiting {WAIT_SECONDS} seconds before cold candidate...")
        time.sleep(WAIT_SECONDS)

        rows.append(invoke("cold_candidate", round_id))
        time.sleep(2)
        rows.append(invoke("warm_followup", round_id))

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
