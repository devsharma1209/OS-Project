# Process-Scheduler
OS Project - Process Scheduler


- simulator that mimics how an OS schedules processes like FCFS, SJF, Round Robin, and Priority Scheduling
- compare your simulated results with real Linux processes


---


things to do rn:
1. Stop using Linux processes — they destroy your entire experiment -  Can't tell if what im doing rn is correct or not
    Stop using fetch_linux_processes() for experiments.
    Replace it with proper, handcrafted scheduling test sets.

2. Create multiple benchmark datasets
  You need at least 4–6 workloads, each designed to reveal specific scheduler behavior.
  Dataset A – Basic small example
      5–6 processes
      Staggered arrivals
      Mixed bursts
      This shows classic FCFS/SJF behavior.
  Dataset B – Convoy effect
      One long job + many short jobs.
      This highlights SJF vs FCFS differences.
  Dataset C – Heavy preemption test
      Lots of short processes arriving frequently.
      Shows how RR, SRTF, MLFQ behave.
  Dataset D – Priority starvation scenario
      Processes with very different priorities to test aging.
      Dataset E – I/O-intensive workload

  
  Use short bursts and frequent arrivals.
  
  You run all schedulers on all datasets.
  Then your results become meaningful.
