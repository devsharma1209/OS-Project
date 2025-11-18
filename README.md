# 🧵 Process-Scheduler  
A complete Operating Systems project that simulates, compares, and analyzes classic CPU scheduling algorithms on curated workloads.

## 🚀 Overview
This project implements a full CPU scheduling simulator supporting:
- FCFS (First Come First Serve)
- SJF (Non-preemptive)
- SRTF (Preemptive SJF)
- Round Robin (RR)
- Priority Scheduling (Preemptive & Non-preemptive)
- MLFQ (optional but highly rewarding for marks)

It focuses on **controlled, academic-style workloads** rather than unpredictable real Linux processes, enabling meaningful comparisons and reproducible experiments.

---

# 🎯 Goals
- Understand how different scheduling algorithms behave under different workload patterns.
- Visualize scheduling using multi-panel Gantt charts.
- Detect starvation, convoy effect, and fairness gaps.
- Present a dataset-by-scheduler comparative analysis.

---

# 📂 Project Structure
```
Process-Scheduler/
│── workloads/
│     ├── dataset_A_basic.json
│     ├── dataset_B_convoy.json
│     ├── dataset_C_preemption.json
│     ├── dataset_D_priority_starvation.json
│     ├── dataset_E_io_mixed.json
│
│── schedulers/
│     ├── fcfs.py
│     ├── sjf.py
│     ├── srtf.py
│     ├── rr.py
│     ├── priority.py
│     ├── mlfq.py
│
│── utils/
│     ├── gantt_plotter.py
│     ├── metrics.py
│     ├── workload_loader.py
│     ├── detection.py   # starvation / convoy / fairness
│
│── results/
│     ├── tables/
│     ├── gantt_charts/
│     ├── summary/
│
│── main.py
│── README.md
```

---

# 📊 Workloads You Must Include
Each workload is handcrafted to expose specific scheduler behavior.

### **Dataset A – Basic Mixed Workload**
- 5–6 processes  
- Staggered arrivals  
- Mixed burst times  
- Shows classic FCFS vs SJF differences  

### **Dataset B – Convoy Effect**
- 1 long CPU burst  
- 5–8 short processes behind it  
- Shows FCFS weakness  
- Highlights why SJF/MLFQ shines  

### **Dataset C – Preemption Stress Test**
- Dozens of tiny jobs  
- Frequent arrivals  
- Round Robin + SRTF tested heavily  
- Shows context-switch patterns  

### **Dataset D – Priority Starvation**
- Huge priority gap (e.g., 1 vs 10)  
- Shows starvation path  
- Used to test anti-starvation / aging  

### **Dataset E – I/O Heavy Mixed**
- Mix of CPU and I/O bursts  
- Shows how schedulers respond to blocking  

---

# ❗ Absolute Rules for Testing
✔ Run all schedulers on all workloads  
✔ Save outputs inside `/results`  
✔ Each workload gets **one panel** showing all Gantt charts side-by-side  
✔ Report must include tables + interpretation

---

# 📋 To-Do Checklist

## **PHASE 1 — Clean the foundation**
- [ ] Remove Linux process fetching (kill fetch_linux_processes entirely)
- [ ] Add structured `workloads/` folder
- [ ] Implement JSON-based workload loader

---

## **PHASE 2 — Build curated workloads**
- [ ] Dataset A – Basic
- [ ] Dataset B – Convoy Effect
- [ ] Dataset C – Preemption Storm
- [ ] Dataset D – Priority Starvation
- [ ] Dataset E – I/O Mixed
- [ ] Validate each dataset loads correctly

---

## **PHASE 3 — Fix scheduling engine**
- [ ] Ensure each scheduler outputs:
  - Timeline of executed jobs
  - Wait time, turnaround time, response time
- [ ] Standardize return format across all schedulers
- [ ] Add support for preemption tracking (remaining burst)

---

## **PHASE 4 — Visualization**
- [ ] Rewrite Gantt panel generator  
- [ ] One figure = one dataset  
- [ ] Columns = schedulers  
- [ ] Uniform colors for processes across all schedulers  
- [ ] Save PNG/PDF into `/results/gantt_charts`

---

## **PHASE 5 — Detection & Analysis Tools**
- [ ] Starvation detection (priority & MLFQ)
- [ ] Convoy effect detection
- [ ] Fairness analysis (variance in wait times)
- [ ] Generate per-workload summary table

---

## **PHASE 6 — CLI Runner (Bonus but makes you stand out)**
```
python main.py --workload A --scheduler rr --quantum 4 --save
```

---

## **PHASE 7 — Final Report**
- [ ] Explain each scheduler  
- [ ] Explain each dataset and why it exposes specific behavior  
- [ ] Insert tables + Gantt screenshots  
- [ ] Interpret results (not just numbers)  
- [ ] Write a conclusion ranking schedulers by scenario  

---

# 🧠 Advanced Features (Optional but boosts marks massively)

### **⭐ Automatic Scheduler Recommendation**
Run all schedulers and auto-suggest the best one based on:
- Avg wait time  
- Fairness  
- Starvation count  
- Turnaround  

### **⭐ Aging (Anti-starvation) Implementation**
Add an option:
```
--aging 1
```
Increase priority of starving processes.

### **⭐ MLFQ with configurable queues**
Config file:
```
queues: 3
quantums: [4, 8, 12]
policy: demotion_on_use
```

### **⭐ I/O-aware simulation**
Model I/O bursts to see realistic interleaving.

---

# 📝 Example Workload JSON
```
{
  "name": "dataset_A_basic",
  "processes": [
    { "pid": 1, "arrival": 0, "burst": 7, "priority": 3 },
    { "pid": 2, "arrival": 2, "burst": 4, "priority": 1 },
    { "pid": 3, "arrival": 4, "burst": 1, "priority": 2 },
    { "pid": 4, "arrival": 5, "burst": 6, "priority": 4 }
  ]
}
```

---

# 🏁 Final Output Expectations
By the end, your repo must include:
- ✔ All workloads  
- ✔ All scheduler results  
- ✔ Multi-panel Gantt charts  
- ✔ Tables of metrics  
- ✔ Starvation & convoy analysis  
- ✔ A polished report  

This is the version that looks like a **real OS project** — not a student script dump.

