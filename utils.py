from tabulate import tabulate

def aggregate_metrics(timeline, processes):
    if not timeline: return {}, {}
    
    # 1. Map process info for easy lookup
    proc_info = {p['pid']: p for p in processes}
    stats = {}
    
    # 2. Find the LAST finish time for each process
    for slice in timeline:
        pid = slice['pid']
        finish = slice['finish']
        
        if pid not in stats:
            stats[pid] = {'finish': finish}
        else:
            stats[pid]['finish'] = max(stats[pid]['finish'], finish)
            
    results = []
    total_wait = 0
    total_tat = 0
    total_response = 0 # Optional but good
    
    # 3. Calculate metrics using the Standard OS Formulas
    # Turnaround = Completion - Arrival
    # Waiting = Turnaround - Burst
    
    for pid, data in stats.items():
        original = proc_info[pid]
        arrival = original['arrival']
        burst = original['burst']
        
        finish = data['finish']
        turnaround = finish - arrival
        waiting = turnaround - burst
        
        # Avoid negative wait (sanity check for edge cases)
        if waiting < 0: waiting = 0
        
        # Find First Start time for Response Time
        # Filter timeline for this pid, get min start
        starts = [x['start'] for x in timeline if x['pid'] == pid]
        first_start = min(starts) if starts else 0
        response = first_start - arrival
        
        results.append({
            'pid': pid,
            'arrival': arrival,
            'burst': burst,
            'finish': finish,
            'turnaround': turnaround,
            'waiting': waiting,
            'response': response
        })
        
        total_wait += waiting
        total_tat += turnaround
        total_response += response
        
    results.sort(key=lambda x: x['pid'])
    
    n = len(results)
    if n == 0: n = 1
    
    # Calculate Throughput (Processes / Total Time)
    max_finish = max([r['finish'] for r in results]) if results else 1
    throughput = n / max_finish
    
    global_metrics = {
        "Avg Waiting Time": total_wait / n,
        "Avg Turnaround Time": total_tat / n,
        "Avg Response Time": total_response / n,
        "Throughput": throughput
    }
    
    return results, global_metrics

def print_metrics(results, global_metrics):
    # Define columns explicitly for clean order
    headers = ['pid', 'arrival', 'burst', 'finish', 'turnaround', 'waiting', 'response']
    rows = [[r[h] for h in headers] for r in results]
    
    print(tabulate(rows, headers=headers, tablefmt="simple_grid"))
    print("\nSUMMARY METRICS:")
    for k, v in global_metrics.items():
        print(f"{k:<20}: {v:.4f}")