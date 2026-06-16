import asyncio
import csv
import os
import statistics
import time
from datetime import datetime

import aiohttp


API_URL = os.getenv("API_URL")
N = 1000
CONCURRENCY_LEVELS = [1, 5, 10, 20, 50, 100]
OUTPUT_FILE = "results/concurrent_n1000.csv"


def load_env():
    global API_URL

    if API_URL:
        return

    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("API_URL="):
                    API_URL = line.strip().split("=", 1)[1]


async def single_request(session, level, request_id):
    start = time.perf_counter()

    try:
        async with session.post(API_URL, json={"n": N}, timeout=30) as response:
            elapsed_ms = (time.perf_counter() - start) * 1000

            try:
                data = await response.json()
            except Exception:
                data = {}

            return {
                "timestamp": datetime.now().isoformat(),
                "concurrency_level": level,
                "request_id": request_id,
                "n": N,
                "status_code": response.status,
                "client_latency_ms": round(elapsed_ms, 3),
                "function_time_ms": data.get("execution_time_ms"),
                "prime_count": data.get("prime_count"),
                "error": ""
            }

    except Exception as e:
        elapsed_ms = (time.perf_counter() - start) * 1000

        return {
            "timestamp": datetime.now().isoformat(),
            "concurrency_level": level,
            "request_id": request_id,
            "n": N,
            "status_code": None,
            "client_latency_ms": round(elapsed_ms, 3),
            "function_time_ms": None,
            "prime_count": None,
            "error": str(e)
        }


async def run_level(level):
    connector = aiohttp.TCPConnector(limit=level)

    async with aiohttp.ClientSession(connector=connector) as session:
        start = time.perf_counter()

        tasks = [
            single_request(session, level, i + 1)
            for i in range(level)
        ]

        rows = await asyncio.gather(*tasks)
        total_elapsed_s = time.perf_counter() - start

    successful = [r for r in rows if r["status_code"] == 200]
    failed = [r for r in rows if r["status_code"] != 200]

    latencies = [r["client_latency_ms"] for r in successful]

    print()
    print(f"Concurrency level: {level}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    print(f"Total elapsed s: {total_elapsed_s:.3f}")

    if latencies:
        print(f"Mean latency ms: {statistics.mean(latencies):.3f}")
        print(f"Median latency ms: {statistics.median(latencies):.3f}")
        print(f"Min latency ms: {min(latencies):.3f}")
        print(f"Max latency ms: {max(latencies):.3f}")
        print(f"Throughput req/s: {len(successful) / total_elapsed_s:.3f}")

    return rows


async def main():
    load_env()

    if not API_URL:
        raise RuntimeError("API_URL is not defined. Create .env with API_URL=...")

    os.makedirs("results", exist_ok=True)

    all_rows = []

    for level in CONCURRENCY_LEVELS:
        rows = await run_level(level)
        all_rows.extend(rows)
        await asyncio.sleep(3)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_rows[0].keys())
        writer.writeheader()
        writer.writerows(all_rows)

    print()
    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
