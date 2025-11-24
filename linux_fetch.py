# linux_fetch.py
import subprocess
import sys
import os
import random

def fetch_linux_processes(top_n=10):
    """
    Fetches real processes if on Linux.
    Returns MOCK data if on Windows (so you can test code logic).
    """
    if os.name == 'nt': # Windows check
        print("⚠️  Windows detected: Generating MOCK Linux data for testing...")
        return _generate_mock_data(top_n)
        
    # LINUX COMMAND:
    # ps -eo pid,comm,pri,etimes,time --sort=-%cpu
    cmd = ["ps", "-eo", "pid,comm,pri,etimes,time", "--sort=-%cpu"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')[1:top_n+1]
        
        processes = []
        for line in lines:
            parts = line.split(None, 4) # Limit split to handle spaces in names
            if len(parts) < 5: continue
            
            pid = int(parts[0])
            name = parts[1]
            priority = int(parts[2])
            elapsed = int(parts[3])
            time_str = parts[4]
            
            # Convert time HH:MM:SS to seconds for Burst
            h, m, s = 0, 0, 0
            if ':' in time_str:
                t_parts = time_str.split(':')
                if len(t_parts) == 3: h, m, s = map(int, t_parts)
                elif len(t_parts) == 2: m, s = map(int, t_parts)
            else:
                s = int(float(time_str)) # Handle '00:01' or '1.2'
            
            cpu_burst = (h*3600) + (m*60) + s
            if cpu_burst == 0: cpu_burst = 1 # Avoid 0 burst
            
            # For Snapshot mode, we assume they all "arrived" now (0)
            processes.append({
                'pid': pid,
                'name': name,
                'arrival': 0, 
                'burst': cpu_burst,
                'priority': priority,
                'elapsed': elapsed # Need this for "Actual Wait" calc
            })
            
        return processes
        
    except Exception as e:
        print(f"Error fetching Linux processes: {e}")
        return []

def _generate_mock_data(n):
    data = []
    for i in range(n):
        burst = random.randint(1, 20)
        elapsed = burst + random.randint(0, 50) # Simulate wait
        data.append({
            'pid': 1000 + i,
            'name': f"mock_proc_{i}",
            'arrival': 0,
            'burst': burst,
            'priority': random.randint(1, 40),
            'elapsed': elapsed
        })
    return data