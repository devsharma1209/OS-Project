import subprocess
import random

def fetch_linux_processes(top_n=5):
    """
    Fetch top N processes from Linux sorted by CPU usage.
    Returns a list of dicts: pid, name, priority, burst, arrival
    """
    cmd = f"ps -eo pid,comm,pri,etimes,%cpu --sort=-%cpu | head -n {top_n+1}"
    output = subprocess.getoutput(cmd).splitlines()[1:]  # skip header
    processes = []
    for i, line in enumerate(output):
        parts = line.split()
        if len(parts) < 5:
            continue
        pid = int(parts[0])
        name = parts[1][:15].lower()
        pri_kernel = int(parts[2])
        etimes = int(parts[3])

        processes.append({
            "pid": pid,
            "name": name,
            # Convert Linux PRI into a "scheduler priority": smaller is better.
            # Here we invert around 140 to make typical user processes near ~20–40.
            "priority": max(1, 140 - pri_kernel),
            # crude exec time proxy: elapsed/10 but at least 1
            "burst": max(1, etimes // 10),
            # stagger arrivals a bit for interesting schedules
            "arrival": random.randint(0, 5 * i)
        })
    return processes


# ---- Optional "mini task manager" helpers ----

def kill_process(pid: int) -> bool:
    """Try to kill a process by pid. Returns True if the signal was sent."""
    try:
        subprocess.check_call(["kill", "-9", str(pid)])
        return True
    except Exception:
        return False


def renice_process(pid: int, nice: int) -> bool:
    """Change process priority (nice value). Lower nice = higher priority."""
    try:
        subprocess.check_call(["renice", str(nice), "-p", str(pid)])
        return True
    except Exception:
        return False
