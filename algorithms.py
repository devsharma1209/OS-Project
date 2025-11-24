import heapq
from collections import deque

# Standard Linux CFS Weight Table (Nice levels -20 to +19)
PRIO_TO_WEIGHT = [
    88761, 71755, 56483, 46273, 36291, 29154, 23254, 18705, 14949, 11916,
    9548,  7620,  6100,  4904,  3906,  3121,  2501,  1991,  1586,  1277,
    1024,  820,   655,   526,   423,   335,   272,   215,   172,   137,
    110,   87,    70,    56,    45,    36,    29,    23,    18,    15
]

def record_history(timeline, pid, start, finish):
    """Stitches adjacent timeline entries for cleaner charts."""
    if timeline and timeline[-1]['pid'] == pid and timeline[-1]['finish'] == start:
        timeline[-1]['finish'] = finish
    else:
        timeline.append({'pid': pid, 'start': start, 'finish': finish})

def add_idle_if_needed(timeline, current_time, next_arrival):
    """Inserts IDLE (pid=-1) if there is a gap."""
    if current_time < next_arrival:
        record_history(timeline, -1, current_time, next_arrival)
        return next_arrival
    return current_time

def fcfs(processes):
    processes.sort(key=lambda x: x['arrival'])
    time = 0
    timeline = []
    
    if processes and processes[0]['arrival'] > 0:
        time = add_idle_if_needed(timeline, 0, processes[0]['arrival'])

    for p in processes:
        time = add_idle_if_needed(timeline, time, p['arrival'])
        start = time
        finish = start + p['burst']
        record_history(timeline, p['pid'], start, finish)
        time = finish
    return timeline

def sjf(processes):
    procs = sorted(processes, key=lambda x: (x['arrival'], x['burst']))
    ready_q = []
    timeline = []
    time = 0
    completed = 0
    n = len(processes)
    
    while completed < n:
        while procs and procs[0]['arrival'] <= time:
            heapq.heappush(ready_q, (procs[0]['burst'], procs[0]['arrival'], procs[0]['pid'], procs.pop(0)))
        
        if ready_q:
            burst, arr, pid, p = heapq.heappop(ready_q)
            start = time
            finish = start + burst
            record_history(timeline, pid, start, finish)
            time = finish
            completed += 1
        else:
            if procs: time = add_idle_if_needed(timeline, time, procs[0]['arrival'])
            else: break
    return timeline

def srtf(processes):
    procs = sorted(processes, key=lambda x: x['arrival'])
    ready_q = [] 
    timeline = []
    time = 0
    remaining = {p['pid']: p['burst'] for p in processes}
    completed = 0
    n = len(processes)
    
    while completed < n:
        while procs and procs[0]['arrival'] <= time:
            p = procs.pop(0)
            heapq.heappush(ready_q, (remaining[p['pid']], p['arrival'], p['pid']))

        if ready_q:
            rem, arr, pid = ready_q[0] # O(1) peek
            start = time
            time += 1
            remaining[pid] -= 1
            record_history(timeline, pid, start, time)
            
            if remaining[pid] == 0:
                completed += 1
                heapq.heappop(ready_q) 
            else:
                heapq.heappop(ready_q)
                heapq.heappush(ready_q, (remaining[pid], arr, pid))
        else:
            if procs: time = add_idle_if_needed(timeline, time, procs[0]['arrival'])
            else: break
    return timeline

def round_robin(processes, quantum=2):
    procs = sorted(processes, key=lambda x: x['arrival'])
    queue = deque()
    timeline = []
    time = 0
    remaining = {p['pid']: p['burst'] for p in processes}
    
    i = 0
    while i < len(procs) and procs[i]['arrival'] <= time:
        queue.append(procs[i])
        i += 1
        
    while queue or i < len(procs):
        if not queue:
            time = add_idle_if_needed(timeline, time, procs[i]['arrival'])
            while i < len(procs) and procs[i]['arrival'] <= time:
                queue.append(procs[i])
                i += 1
        
        p = queue.popleft()
        pid = p['pid']
        exec_time = min(quantum, remaining[pid])
        
        start = time
        finish = start + exec_time
        record_history(timeline, pid, start, finish)
        
        remaining[pid] -= exec_time
        time += exec_time
        
        while i < len(procs) and procs[i]['arrival'] <= time:
            queue.append(procs[i])
            i += 1
            
        if remaining[pid] > 0: queue.append(p)
            
    return timeline

def priority_sched(processes):
    procs = sorted(processes, key=lambda x: x['arrival'])
    ready_q = []
    timeline = []
    time = 0
    completed = 0
    n = len(processes)
    
    while completed < n:
        while procs and procs[0]['arrival'] <= time:
            p = procs.pop(0)
            heapq.heappush(ready_q, (p['priority'], p['arrival'], p['pid'], p))
            
        if ready_q:
            pri, arr, pid, p = heapq.heappop(ready_q)
            start = time
            finish = start + p['burst']
            record_history(timeline, pid, start, finish)
            time = finish
            completed += 1
        else:
            if procs: time = add_idle_if_needed(timeline, time, procs[0]['arrival'])
            else: break
    return timeline

def cfs_simplified(processes, min_granularity=1):
    procs = sorted(processes, key=lambda x: x['arrival'])
    timeline = []
    time = 0
    
    def get_linux_weight(prio):
        idx = max(0, min(39, prio))
        return PRIO_TO_WEIGHT[idx]
        
    proc_state = {}
    for p in processes:
        proc_state[p['pid']] = {
            'remaining': p['burst'],
            'vruntime': 0,
            'weight': get_linux_weight(p.get('priority', 20)),
            'p': p
        }

    ready_q = [] 
    completed = 0
    n = len(processes)
    
    while completed < n:
        while procs and procs[0]['arrival'] <= time:
            p = procs.pop(0)
            heapq.heappush(ready_q, (0, p['pid'])) 
            
        if ready_q:
            vruntime, pid = heapq.heappop(ready_q)
            state = proc_state[pid]
            slice_time = min(min_granularity, state['remaining'])
            start = time
            finish = start + slice_time
            
            record_history(timeline, pid, start, finish)
            time = finish
            state['remaining'] -= slice_time
            state['vruntime'] += slice_time * (1024 / state['weight'])
            
            if state['remaining'] > 0:
                heapq.heappush(ready_q, (state['vruntime'], pid))
            else:
                completed += 1
        else:
            if procs: time = add_idle_if_needed(timeline, time, procs[0]['arrival'])
            else: break
            
    return timeline
