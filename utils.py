from tabulate import tabulate
from collections import defaultdict
import statistics

def aggregate_metrics(timeline, processes):
    """
    Aggregate per-process and global metrics from timeline slices.

    Args:
        timeline: list of slice dicts with keys: {"pid", "start", "finish"}
        processes: list of process dicts with keys: {"pid", "arrival", "burst", ...}

    Returns:
        tuple: (per_proc_metrics, global_metrics)
    """
    if not timeline or not processes:
        return [], {
            "Avg Waiting Time": 0.0,
            "Avg Turnaround Time": 0.0,
            "Avg Response Time": 0.0,
            "Min Waiting Time": 0.0,
            "Max Waiting Time": 0.0,
            "Std Dev Waiting Time": 0.0,
            "CPU Utilization (%)": 0.0,
            "Throughput (proc/unit time)": 0.0,
            "Context Switches": 0,
            "Makespan": 0.0,
            "Idle Time": 0.0,
        }

    # group slices by PID
    by_pid = defaultdict(list)
    for sl in sorted(timeline, key=lambda x: (x["start"], x["finish"], x["pid"])):
        by_pid[sl["pid"]].append(sl)

    info = {p["pid"]: p for p in processes}

    # per-process metrics
    per_proc = []
    for pid, slices in by_pid.items():
        arrival = info[pid]["arrival"]
        burst = info[pid]["burst"]
        first_start = min(s["start"] for s in slices)
        last_finish = max(s["finish"] for s in slices)
        active = sum(s["finish"] - s["start"] for s in slices)

        turnaround = last_finish - arrival        # TAT
        waiting = turnaround - burst              # WT
        response = first_start - arrival          # RT (time until first scheduled)

        per_proc.append({
            "pid": pid,
            "arrival": arrival,
            "burst": burst,
            "start": first_start,
            "finish": last_finish,
            "response": response,
            "waiting": waiting,
            "turnaround": turnaround,
            "active": active,
        })

    per_proc = sorted(per_proc, key=lambda x: x["pid"])

    # CPU / system metrics
    earliest = min(s["start"] for s in timeline)
    latest = max(s["finish"] for s in timeline)
    makespan = latest - earliest

    cpu_busy = sum(s["finish"] - s["start"] for s in timeline)
    cpu_util = (cpu_busy / makespan * 100) if makespan > 0 else 0.0
    idle_time = max(0.0, makespan - cpu_busy)
    throughput = (len(per_proc) / makespan) if makespan > 0 else 0.0

    # Context switches = PID changes between consecutive slices
    ordered = sorted(timeline, key=lambda s: (s["start"], s["finish"]))
    ctx_switches = 0
    for i in range(1, len(ordered)):
        if ordered[i-1]["pid"] != ordered[i]["pid"]:
            ctx_switches += 1

    # Averages & distribution
    avg_wait = sum(p["waiting"] for p in per_proc) / len(per_proc)
    avg_tat = sum(p["turnaround"] for p in per_proc) / len(per_proc)
    avg_resp = sum(p["response"] for p in per_proc) / len(per_proc)

    waiting_times = [p["waiting"] for p in per_proc]
    min_wait = min(waiting_times)
    max_wait = max(waiting_times)
    std_wait = statistics.stdev(waiting_times) if len(waiting_times) > 1 else 0.0

    globals_ = {
        "Avg Waiting Time": avg_wait,
        "Avg Turnaround Time": avg_tat,
        "Avg Response Time": avg_resp,
        "Min Waiting Time": min_wait,
        "Max Waiting Time": max_wait,
        "Std Dev Waiting Time": std_wait,
        "CPU Utilization (%)": cpu_util,
        "Throughput (proc/unit time)": throughput,
        "Context Switches": ctx_switches,
        "Makespan": makespan,
        "Idle Time": idle_time,
    }

    return per_proc, globals_


def print_table(timeline, processes):
    per_proc, globals_ = aggregate_metrics(timeline, processes)

    if not per_proc:
        print("⚠️  No process data to display")
        return per_proc, globals_

    # Custom order
    cols = ["pid", "arrival", "burst", "start", "finish", "response", "waiting", "turnaround"]
    rows = [[p[c] for c in cols] for p in per_proc]

    print(tabulate(rows, headers=cols, tablefmt="fancy_grid"))

    print("\n" + "="*50)
    print("  PERFORMANCE METRICS")
    print("="*50)

    time_metrics = [
        ("Avg Waiting Time", globals_["Avg Waiting Time"]),
        ("Avg Turnaround Time", globals_["Avg Turnaround Time"]),
        ("Avg Response Time", globals_["Avg Response Time"]),
    ]

    distribution_metrics = [
        ("Min Waiting Time", globals_["Min Waiting Time"]),
        ("Max Waiting Time", globals_["Max Waiting Time"]),
        ("Std Dev Waiting Time", globals_["Std Dev Waiting Time"]),
    ]

    system_metrics = [
        ("CPU Utilization (%)", globals_["CPU Utilization (%)"]),
        ("Throughput (proc/unit time)", globals_["Throughput (proc/unit time)"]),
        ("Context Switches", globals_["Context Switches"]),
        ("Makespan", globals_["Makespan"]),
        ("Idle Time", globals_["Idle Time"]),
    ]

    print("\n📊 Time Metrics:")
    for k, v in time_metrics:
        print(f"  • {k:<25}: {v:>8.2f}")

    print("\n📈 Distribution Metrics:")
    for k, v in distribution_metrics:
        print(f"  • {k:<25}: {v:>8.2f}")

    print("\n⚙️  System Metrics:")
    for k, v in system_metrics:
        if isinstance(v, float):
            print(f"  • {k:<25}: {v:>8.2f}")
        else:
            print(f"  • {k:<25}: {v:>8}")

    print("="*50 + "\n")

    return per_proc, globals_



# ---------- Starvation detection ----------

def detect_starvation(per_proc_metrics, threshold: int = 20):
    """
    Return PIDs whose waiting time exceeds `threshold`.
    (You can set threshold to e.g. 2x median burst or a fixed value.)
    """
    starving = []
    for row in per_proc_metrics:
        if row["waiting"] > threshold:
            starving.append(row["pid"])
    return starving

