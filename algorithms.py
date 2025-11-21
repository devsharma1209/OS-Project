from collections import deque
import heapq

def fcfs(processes):
    processes.sort(key=lambda x: x['arrival'])
    time = 0
    timeline = []
    for p in processes:
        if time < p['arrival']:
            time = p['arrival']
        start = time
        finish = start + p['burst']
        timeline.append({'pid': p['pid'], 'start': start, 'finish': finish})
        time = finish
    return timeline

def sjf(processes):
    # Non-preemptive SJF
    # Sort by arrival first to handle initial stability
    procs = sorted(processes, key=lambda x: (x['arrival'], x['burst']))
    ready_q = []
    timeline = []
    time = 0
    completed = 0
    n = len(processes)
    
    # Jump to first arrival if needed
    if procs: time = procs[0]['arrival']
    
    while completed < n:
        # Add all processes that have arrived by 'time'
        while procs and procs[0]['arrival'] <= time:
            # Heap sort by BURST, then ARRIVAL
            heapq.heappush(ready_q, (procs[0]['burst'], procs[0]['arrival'], procs[0]['pid'], procs.pop(0)))
        
        if ready_q:
            burst, arr, pid, p = heapq.heappop(ready_q)
            start = time
            finish = start + burst
            timeline.append({'pid': pid, 'start': start, 'finish': finish})
            time = finish
            completed += 1
        else:
            if procs:
                time = procs[0]['arrival']
            else:
                time += 1
    return timeline

def srtf(processes):
    # Preemptive SJF (Shortest Remaining Time First)
    procs = sorted(processes, key=lambda x: x['arrival'])
    ready_q = [] 
    timeline = []
    time = 0
    remaining = {p['pid']: p['burst'] for p in processes}
    completed = 0
    n = len(processes)
    
    if procs: time = procs[0]['arrival']
    
    while completed < n:
        # Add arrivals
        while procs and procs[0]['arrival'] <= time:
            p = procs.pop(0)
            heapq.heappush(ready_q, (remaining[p['pid']], p['arrival'], p['pid']))

        if ready_q:
            rem, arr, pid = list(ready_q[0]) # Peek
            
            # Run for 1 unit
            start = time
            time += 1
            remaining[pid] -= 1
            
            # Add to timeline (Coalesce if same as last)
            if timeline and timeline[-1]['pid'] == pid and timeline[-1]['finish'] == start:
                timeline[-1]['finish'] = time
            else:
                timeline.append({'pid': pid, 'start': start, 'finish': time})
            
            if remaining[pid] == 0:
                completed += 1
                heapq.heappop(ready_q) # Remove
            else:
                # Re-sort heap because remaining time changed
                # (Python heapq doesn't auto-update, we pop and push or re-heapify)
                heapq.heappop(ready_q)
                heapq.heappush(ready_q, (remaining[pid], arr, pid))
        else:
            if procs: time = procs[0]['arrival']
            else: time += 1
            
    return timeline

def round_robin(processes, quantum=2):
    procs = sorted(processes, key=lambda x: x['arrival'])
    queue = deque()
    timeline = []
    time = 0
    remaining = {p['pid']: p['burst'] for p in procs}
    
    if procs: time = procs[0]['arrival']
    
    # Push initial
    i = 0
    while i < len(procs) and procs[i]['arrival'] <= time:
        queue.append(procs[i])
        i += 1
        
    while queue or i < len(procs):
        if not queue:
            time = procs[i]['arrival']
            while i < len(procs) and procs[i]['arrival'] <= time:
                queue.append(procs[i])
                i += 1
        
        p = queue.popleft()
        pid = p['pid']
        
        exec_time = min(quantum, remaining[pid])
        start = time
        finish = start + exec_time
        
        # Timeline recording
        if timeline and timeline[-1]['pid'] == pid and timeline[-1]['finish'] == start:
             timeline[-1]['finish'] = finish
        else:
            timeline.append({'pid': pid, 'start': start, 'finish': finish})
        
        remaining[pid] -= exec_time
        time += exec_time
        
        # Check for new arrivals BEFORE re-queueing current process
        while i < len(procs) and procs[i]['arrival'] <= time:
            queue.append(procs[i])
            i += 1
            
        if remaining[pid] > 0:
            queue.append(p)
            
    return timeline

def priority_sched(processes):
    # Non-preemptive Priority (Lower is better)
    procs = sorted(processes, key=lambda x: x['arrival'])
    ready_q = []
    timeline = []
    time = 0
    completed = 0
    n = len(processes)
    
    if procs: time = procs[0]['arrival']
    
    while completed < n:
        while procs and procs[0]['arrival'] <= time:
            p = procs.pop(0)
            heapq.heappush(ready_q, (p['priority'], p['arrival'], p['pid'], p))
            
        if ready_q:
            pri, arr, pid, p = heapq.heappop(ready_q)
            start = time
            finish = start + p['burst']
            timeline.append({'pid': pid, 'start': start, 'finish': finish})
            time = finish
            completed += 1
        else:
            if procs: time = procs[0]['arrival']
            else: time += 1
    return timeline

def cfs_simplified(processes, min_granularity=1):
    """
    Simplified Linux CFS. 
    Uses 'vruntime' = execution_time * (1024 / weight).
    Lower vruntime runs first.
    """
    procs = sorted(processes, key=lambda x: x['arrival'])
    timeline = []
    time = 0
    
    # Setup vruntime and weights
    # Mapping Priority 1-10 to Weights (Lower prio # = Higher Weight)
    # Pri 1=1024, Pri 2=512, etc.
    def get_weight(prio):
        return 1024 / (max(1, prio)) # Simplified weight formula
        
    proc_state = {}
    for p in processes:
        proc_state[p['pid']] = {
            'remaining': p['burst'],
            'vruntime': 0,
            'weight': get_weight(p.get('priority', 1)),
            'p': p
        }

    ready_q = [] # Heap of (vruntime, pid)
    completed = 0
    n = len(processes)
    
    if procs: time = procs[0]['arrival']
    
    while completed < n:
        # Add arrivals
        while procs and procs[0]['arrival'] <= time:
            p = procs.pop(0)
            heapq.heappush(ready_q, (0, p['pid'])) # Initial vruntime 0
            
        if ready_q:
            vruntime, pid = heapq.heappop(ready_q)
            state = proc_state[pid]
            
            # Run for a slice (min_granularity)
            slice_time = min(min_granularity, state['remaining'])
            start = time
            finish = start + slice_time
            
            # Record
            if timeline and timeline[-1]['pid'] == pid and timeline[-1]['finish'] == start:
                 timeline[-1]['finish'] = finish
            else:
                timeline.append({'pid': pid, 'start': start, 'finish': finish})
            
            time = finish
            state['remaining'] -= slice_time
            
            # Update vruntime
            # Delta Vruntime = Delta Exec * (1024 / Weight)
            state['vruntime'] += slice_time * (1024 / state['weight'])
            
            if state['remaining'] > 0:
                heapq.heappush(ready_q, (state['vruntime'], pid))
            else:
                completed += 1
        else:
            if procs: time = procs[0]['arrival']
            else: time += 1
            
    return timeline