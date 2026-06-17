import os
import pandas as pd
import matplotlib.pyplot as plt


RESULTS_DIR = "results"
FIGURES_DIR = "figures"

LATENCY_FILE = f"{RESULTS_DIR}/latency_n1000.csv"
CONCURRENCY_STABLE_FILE = f"{RESULTS_DIR}/concurrency_stable_n1000.csv"
CONCURRENCY_SATURATION_FILE = f"{RESULTS_DIR}/concurrency_saturation_n1000.csv"
COLDSTART_FILE = f"{RESULTS_DIR}/coldstart_n1000.csv"


def save_figure(name):
    os.makedirs(FIGURES_DIR, exist_ok=True)
    path = f"{FIGURES_DIR}/{name}"
    plt.tight_layout()
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"Saved: {path}")


def analyze_latency():
    df = pd.read_csv(LATENCY_FILE)

    summary = df["client_latency_ms"].describe()
    print("\nSequential latency summary:")
    print(summary)

    plt.figure(figsize=(8, 5))
    plt.plot(df["request_id"], df["client_latency_ms"], marker="o", linewidth=1)
    plt.xlabel("Request number")
    plt.ylabel("Client latency (ms)")
    plt.title("Sequential latency for n=1000")
    plt.grid(True, alpha=0.3)
    save_figure("latency_sequential_n1000.png")

    plt.figure(figsize=(6, 5))
    plt.boxplot(df["client_latency_ms"], orientation="vertical")
    plt.ylabel("Client latency (ms)")
    plt.title("Sequential latency distribution for n=1000")
    plt.grid(True, alpha=0.3)
    save_figure("latency_boxplot_n1000.png")


def analyze_concurrency():
    stable = pd.read_csv(CONCURRENCY_STABLE_FILE)
    saturation = pd.read_csv(CONCURRENCY_SATURATION_FILE)

    df = pd.concat([stable, saturation], ignore_index=True)

    summary = df.groupby("concurrency_level").agg(
        total_requests=("status_code", "count"),
        successful_requests=("status_code", lambda x: (x == 200).sum()),
        failed_requests=("status_code", lambda x: (x != 200).sum()),
        mean_latency_ms=("client_latency_ms", "mean"),
        median_latency_ms=("client_latency_ms", "median"),
        min_latency_ms=("client_latency_ms", "min"),
        max_latency_ms=("client_latency_ms", "max"),
    ).reset_index()

    summary["success_rate_percent"] = (
        summary["successful_requests"] / summary["total_requests"] * 100
    )

    summary_path = f"{RESULTS_DIR}/concurrency_summary_n1000.csv"
    summary.to_csv(summary_path, index=False)
    print(f"\nSaved: {summary_path}")
    print("\nConcurrency summary:")
    print(summary)

    plt.figure(figsize=(8, 5))
    plt.plot(
        summary["concurrency_level"],
        summary["mean_latency_ms"],
        marker="o",
        label="Mean latency"
    )
    plt.plot(
        summary["concurrency_level"],
        summary["median_latency_ms"],
        marker="o",
        label="Median latency"
    )
    plt.xlabel("Concurrency level")
    plt.ylabel("Client latency (ms)")
    plt.title("Latency under concurrent load for n=1000")
    plt.legend()
    plt.grid(True, alpha=0.3)
    save_figure("concurrency_latency_n1000.png")

    plt.figure(figsize=(8, 5))
    plt.bar(
        summary["concurrency_level"].astype(str),
        summary["success_rate_percent"]
    )
    plt.xlabel("Concurrency level")
    plt.ylabel("Success rate (%)")
    plt.title("Success rate under concurrent load for n=1000")
    plt.ylim(0, 105)
    plt.grid(True, axis="y", alpha=0.3)
    save_figure("concurrency_success_rate_n1000.png")

    plt.figure(figsize=(8, 5))
    plt.bar(
        summary["concurrency_level"].astype(str),
        summary["failed_requests"]
    )
    plt.xlabel("Concurrency level")
    plt.ylabel("Failed requests")
    plt.title("Failed requests under concurrent load for n=1000")
    plt.grid(True, axis="y", alpha=0.3)
    save_figure("concurrency_failures_n1000.png")


def analyze_coldstart():
    df = pd.read_csv(COLDSTART_FILE)

    summary = df.groupby("label").agg(
        count=("client_latency_ms", "count"),
        mean_latency_ms=("client_latency_ms", "mean"),
        median_latency_ms=("client_latency_ms", "median"),
        min_latency_ms=("client_latency_ms", "min"),
        max_latency_ms=("client_latency_ms", "max"),
        mean_function_time_ms=("function_time_ms", "mean"),
    ).reset_index()

    summary_path = f"{RESULTS_DIR}/coldstart_summary_n1000.csv"
    summary.to_csv(summary_path, index=False)
    print(f"\nSaved: {summary_path}")
    print("\nCold start summary:")
    print(summary)

    pivot = df.pivot(index="round_id", columns="label", values="client_latency_ms")

    plt.figure(figsize=(8, 5))
    plt.plot(
        pivot.index,
        pivot["cold_candidate"],
        marker="o",
        label="Cold-start candidate"
    )
    plt.plot(
        pivot.index,
        pivot["warm_followup"],
        marker="o",
        label="Warm follow-up"
    )
    plt.xlabel("Round")
    plt.ylabel("Client latency (ms)")
    plt.title("Cold-start candidates versus warm invocations")
    plt.legend()
    plt.grid(True, alpha=0.3)
    save_figure("coldstart_line_n1000.png")

    plt.figure(figsize=(7, 5))
    data = [
        df[df["label"] == "cold_candidate"]["client_latency_ms"],
        df[df["label"] == "warm_followup"]["client_latency_ms"],
    ]
    plt.boxplot(data, tick_labels=["Cold candidate", "Warm follow-up"])
    plt.ylabel("Client latency (ms)")
    plt.title("Cold-start latency comparison for n=1000")
    plt.grid(True, axis="y", alpha=0.3)
    save_figure("coldstart_boxplot_n1000.png")

    df["label_readable"] = df["label"].replace({
        "cold_candidate": "Cold candidate",
        "warm_followup": "Warm follow-up"
    })

    plt.figure(figsize=(7, 5))
    means = df.groupby("label_readable")["client_latency_ms"].mean()
    plt.bar(means.index, means.values)
    plt.ylabel("Mean client latency (ms)")
    plt.title("Average cold-start candidate versus warm latency")
    plt.grid(True, axis="y", alpha=0.3)
    save_figure("coldstart_mean_latency_n1000.png")


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    analyze_latency()
    analyze_concurrency()
    analyze_coldstart()

    print("\nAnalysis complete.")


if __name__ == "__main__":
    main()
