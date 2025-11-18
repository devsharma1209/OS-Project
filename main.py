from algorithms import (
    fcfs, sjf, srtf,
    round_robin, priority_scheduling,
    cfs, mlfq
)
from linux_fetch import fetch_linux_processes
from utils import print_table


def run_scheduler(name, func, processes, **kwargs):
    print(f"\nRunning {name} Scheduler...")

    # Run the algorithm
    timeline = func(processes, **kwargs) if kwargs else func(processes)

    # Print full metrics table (requires timeline + processes)
    per_proc, globals_ = print_table(timeline, processes)

    return timeline, per_proc, globals_


def main():
    print("Fetching Linux processes...")
    processes = fetch_linux_processes(top_n=5)

    print("\nFetched Processes:")
    for p in processes:
        print(p)

    schedulers = [
        ("FCFS", fcfs, {}),
        ("SJF (Non-Preemptive)", sjf, {}),
        ("SRTF (Preemptive SJF)", srtf, {}),
        ("Round Robin", round_robin, {"quantum": 2}),
        ("Priority Scheduling", priority_scheduling, {}),
        ("Completely Fair Scheduler (CFS)", cfs, {}),
        ("Multilevel Feedback Queue (MLFQ)", mlfq, {})
    ]

    summary = []

    for name, func, params in schedulers:
        timeline, per_proc, globals_ = run_scheduler(name, func, processes, **params)

        summary.append({
            "Scheduler": name,
            "Avg Waiting Time": globals_["Avg Waiting Time"],
            "Avg Turnaround Time": globals_["Avg Turnaround Time"],
            "Avg Response Time": globals_["Avg Response Time"],
            "CPU Util (%)": globals_["CPU Utilization (%)"],
            "Context Switches": globals_["Context Switches"],
        })

    print("\n=== Scheduler Comparison Summary ===")
    from tabulate import tabulate
    print(tabulate(summary, headers="keys", tablefmt="grid"))


if __name__ == "__main__":
    main()
