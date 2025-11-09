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
    # Handle empty inputs
    if not timeline or not processes:
        return [], {
            "Avg Waiting Time": 0,
            "Avg Turnaround Time": 0,
            "Avg Response Time": 0,
            "Min Waiting Time": 0,
            "Max Waiting Time": 0,
            "Std Dev Waiting Time": 0,
            "CPU Utilization (%)": 0,
            "Throughput (proc/unit time)": 0,
            "Context Switches": 0,
            "Makespan": 0,
        }
    
    # Group slices by PID
    by_pid = defaultdict(list)
    for sl in sorted(timeline, key=lambda x: (x["start"], x["finish"])):
        by_pid[sl["pid"]].append(sl)
    
    # Create lookup for process info
    info = {p["pid"]: p for p in processes}
    
    # Calculate per-process metrics
    per_proc = []
    for pid, slices in by_pid.items():
        arrival = info[pid]["arrival"]
        burst = info[pid]["burst"]
        first_start = min(s["start"] for s in slices)
        last_finish = max(s["finish"] for s in slices)
        active = sum(s["finish"] - s["start"] for s in slices)
        
        turnaround = last_finish - arrival              # TAT
        waiting = turnaround - burst                    # WT
        response = first_start - arrival                # RT (first response time)
        
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
    
    # Sort by PID for consistent display
    per_proc = sorted(per_proc, key=lambda x: x["pid"])
    
    # Calculate global metrics
    makespan = max(s["finish"] for s in timeline) - min(s["start"] for s in timeline)
    cpu_busy = sum(s["finish"] - s["start"] for s in timeline)
    cpu_util = (cpu_busy / makespan * 100) if makespan > 0 else 0
    throughput = (len(per_proc) / makespan) if makespan > 0 else 0
    
    # Context switches: count PID changes between consecutive time-ordered slices
    ordered = sorted(timeline, key=lambda s: (s["start"], s["finish"]))
    ctx_switches = 0
    for i in range(1, len(ordered)):
        if ordered[i-1]["pid"] != ordered[i]["pid"]:
            ctx_switches += 1
    
    # Average metrics
    avg_wait = sum(p["waiting"] for p in per_proc) / len(per_proc)
    avg_tat = sum(p["turnaround"] for p in per_proc) / len(per_proc)
    avg_resp = sum(p["response"] for p in per_proc) / len(per_proc)
    
    # Statistical distribution metrics
    waiting_times = [p["waiting"] for p in per_proc]
    min_wait = min(waiting_times)
    max_wait = max(waiting_times)
    std_wait = statistics.stdev(waiting_times) if len(waiting_times) > 1 else 0
    
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
    }
    
    return per_proc, globals_


def print_table(timeline, processes):
    """
    Print detailed per-process metrics and global performance metrics.
    
    Args:
        timeline: list of execution slices
        processes: list of process definitions
    
    Returns:
        tuple: (per_proc_metrics, global_metrics) for further analysis
    """
    per_proc, globals_ = aggregate_metrics(timeline, processes)
    
    if not per_proc:
        print("⚠️  No process data to display")
        return per_proc, globals_
    
    # Per-process summary table
    cols = ["pid", "arrival", "burst", "start", "finish", "response", "waiting", "turnaround"]
    print(tabulate(per_proc, headers=cols, tablefmt="fancy_grid"))
    
    # Global metrics block
    print("\n" + "="*50)
    print("  PERFORMANCE METRICS")
    print("="*50)
    
    # Group metrics for better readability
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
