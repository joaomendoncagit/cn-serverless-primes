import csv
import json
import os
import statistics
import time
from datetime import datetime

import requests


API_URL = os.getenv("API_URL")
N = 1000
REQUESTS = 100
OUTPUT_FILE = "results/latency_n1000.csv"


def load_env():
    global API_URL

    if API_URL:
        return

    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("API_URL="):
                    API_URL = line.strip().split("=", 1)[1]


def main():
    load_env()

    if not API_URL:
        raise RuntimeError("API_URL is not defined. Create .env with API_URL=...")

    os.makedirs("results", exist_ok=True)

    rows = []
    latencies = []

    for i in range(REQUESTS):
        payload = {"n": N}

        start = time.perf_counter()
        response = requests.post(API_URL, json=payload, timeout=30)
        elapsed_ms = (time.perf_counter() - start) * 1000

        status_code = response.status_code

        try:
            data = response.json()
        except Exception:
            data = {}

        function_time_ms = data.get("execution_time_ms")

        rows.append({
            "timestamp": datetime.now().isoformat(),
            "request_id": i + 1,
            "n": N,
            "status_code": status_code,
            "client_latency_ms": round(elapsed_ms, 3),
            "function_time_ms": function_time_ms,
            "prime_count": data.get("prime_count"),
        })

        latencies.append(elapsed_ms)

        print(
            f"{i + 1}/{REQUESTS} "
            f"status={status_code} "
            f"client_latency_ms={elapsed_ms:.3f} "
            f"function_time_ms={function_time_ms}"
        )

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print()
    print(f"Saved: {OUTPUT_FILE}")
    print(f"Requests: {REQUESTS}")
    print(f"n: {N}")
    print(f"min_ms: {min(latencies):.3f}")
    print(f"mean_ms: {statistics.mean(latencies):.3f}")
    print(f"median_ms: {statistics.median(latencies):.3f}")
    print(f"max_ms: {max(latencies):.3f}")
    print(f"stdev_ms: {statistics.stdev(latencies):.3f}")


if __name__ == "__main__":
    main()
