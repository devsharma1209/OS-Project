import argparse
import json
import os
import time  # <--- Added for timing
from algorithms import fcfs, sjf, srtf, round_robin, priority_sched, cfs_simplified
from utils import aggregate_metrics, print_metrics
from gantt import plot_gantt_grid
from linux_fetch import fetch_linux_processes

SCHEDULERS = {
    "FCFS": fcfs,
    "SJF (Non-Preemptive)": sjf,
    "SRTF (Preemptive)": srtf,
    "RR (Quantum=2)": round_robin,
    "Priority": priority_sched,
    "CFS (Simplified)": cfs_simplified
}

# --- Helper Class for Saving Output ---
class DualLogger:
    """Prints to console and appends to a file simultaneously."""
    def __init__(self, filepath):
        self.filepath = filepath
        self.file = open(filepath, "w", encoding="utf-8")
    
    def log(self, message=""):
        print(message)
        self.file.write(message + "\n")
        
    def close(self):
        self.file.close()
        print(f"\n[System] 💾 Report saved to: {self.filepath}")

def load_workload(filename):
    path = os.path.join("workloads", filename)
    if not os.path.exists(path):
        print(f"❌ Error: File {path} not found.")
        return []
    with open(path, 'r') as f:
        return json.load(f)['processes']

def check_starvation(metrics, threshold=20):
    starved = [p for p in metrics if p['waiting'] > threshold]
    if starved:
        print(f"\n⚠️  STARVATION DETECTED (Wait > {threshold}s):")
        for p in starved:
            print(f"   - PID {p['pid']} waited {p['waiting']:.2f}s")

def run_scientific(filename):
    print(f"\n🔬 RUNNING SCIENTIFIC MODE: {filename}")
    processes = load_workload(filename)
    if not processes: return
    
    results_store = {}
    
    for name, func in SCHEDULERS.items():
        print(f"\n--- Scheduler: {name} ---")
        proc_copy = [p.copy() for p in processes] 
        
        # Timing the algorithm
        start_t = time.perf_counter()
        timeline = func(proc_copy)
        end_t = time.perf_counter()
        runtime_ms = (end_t - start_t) * 1000
        
        results, metrics = aggregate_metrics(timeline, proc_copy)
        print_metrics(results, metrics)
        print(f"⏱️  Simulation Runtime: {runtime_ms:.4f} ms") # <--- Timing Log
        
        check_starvation(results, threshold=15)
        
        label = f"{name} (Avg TAT: {metrics['Avg Turnaround Time']:.2f})"
        results_store[label] = timeline
        
    output_file = os.path.basename(filename).replace('.json', '.png')
    plot_gantt_grid(results_store, output_file)

def run_live():
    # Ensure directories exist
    if not os.path.exists("results"): os.makedirs("results")
    if not os.path.exists("workloads"): os.makedirs("workloads")

    # Initialize Logger
    logger = DualLogger("results/live_mode_report.txt")

    logger.log("\n🐧 RUNNING LINUX LIVE MODE")
    logger.log("-------------------------------------------------------")
    logger.log("NOTE: This is a simplified simulation.")
    logger.log("Real Linux processes have I/O blocking and variable arrival.")
    logger.log("We assume Arrival=0 and Burst=Active_CPU_Time for comparison.")
    logger.log("-------------------------------------------------------\n")
    
    processes = fetch_linux_processes(top_n=10)
    if not processes: 
        logger.close()
        return
        
    logger.log(f"Captured {len(processes)} active processes from System.")

    # --- BONUS: Save Snapshot as JSON ---
    snapshot_path = "workloads/live_snapshot.json"
    with open(snapshot_path, "w") as f:
        json.dump({"name": "Live Snapshot", "processes": processes}, f, indent=2)
    logger.log(f"[System] 📸 Snapshot saved to: {snapshot_path}")
    
    # 1. Reality Check
    logger.log("\n=== 📊 REALITY CHECK (Simulated vs Actual Wait) ===")
    logger.log(f"{'PID':<8} | {'Name':<15} | {'Sim Wait (RR)':<15} | {'Actual Wait':<15} | {'Diff'}")
    logger.log("-" * 75)
    
    proc_copy = [p.copy() for p in processes]
    timeline = round_robin(proc_copy)
    rr_res, _ = aggregate_metrics(timeline, proc_copy)
    rr_map = {r['pid']: r['waiting'] for r in rr_res}
    
    for p in processes:
        sim_wait = rr_map.get(p['pid'], 0)
        actual_wait = max(0, p['elapsed'] - p['burst'])
        diff = actual_wait - sim_wait
        logger.log(f"{p['pid']:<8} | {p['name'][:15]:<15} | {sim_wait:>13.2f}s | {actual_wait:>13.2f}s | {diff:>+8.2f}")

    # 2. Recommender
    logger.log("\n=== 🤖 ALGORITHM RECOMMENDER ===")
    best_algo = None
    lowest_tat = float('inf')
    
    for name, func in SCHEDULERS.items():
        proc_copy = [p.copy() for p in processes]
        
        # Measure Algorithm Speed
        start_t = time.perf_counter()
        timeline = func(proc_copy)
        end_t = time.perf_counter()
        runtime = (end_t - start_t) * 1000 # ms
        
        _, metrics = aggregate_metrics(timeline, proc_copy)
        tat = metrics['Avg Turnaround Time']
        
        logger.log(f"{name:<25}: Avg TAT = {tat:.2f}s  (Calc Time: {runtime:.3f}ms)")
        
        if tat < lowest_tat:
            lowest_tat = tat
            best_algo = name
            
    logger.log(f"\n✅ RECOMMENDATION: **{best_algo}** handles this snapshot most efficiently.")
    logger.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['scientific', 'live'], required=True)
    parser.add_argument('--workload', default='dataset_A_basic.json')
    args = parser.parse_args()
    
    if args.mode == 'scientific':
        run_scientific(args.workload)
    elif args.mode == 'live':
        run_live()