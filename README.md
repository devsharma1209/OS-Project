# ⚡ OS Process Scheduler & Linux Integration Toolkit

### Operating Systems & Networking Group Project – 2025  
A hybrid **CPU Scheduling Simulator** + **Linux System Analysis Toolkit** that connects classroom algorithms to real-world Linux behavior.

![Status](https://img.shields.io/badge/Status-Complete-green)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Platform](https://img.shields.io/badge/Platform-Linux%20%2F%20AWS-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

# 📖 Overview

This project implements classical CPU scheduling algorithms and compares them with **actual Linux scheduler behavior (CFS)** using real process snapshots.

It operates in two coordinated modes:

### **🔬 Scientific Mode (Simulated CPU Scheduling)**
Deterministic algorithm testing on controlled JSON workloads.  
Includes full metrics, starvation detection, and Gantt chart visualization.

### **🐧 Live Mode (Real Linux Integration)**
Captures live process data from the Linux kernel using `ps`,  
estimates scheduling states, and runs a “**Reality Check**” comparing:

- Simulated wait time (from RR)
- Actual Linux wait time (elapsed - CPU time)

---

# 🚀 Features

### **Implemented Scheduling Algorithms**
- FCFS  
- SJF (Non-Preemptive)  
- SRTF (Preemptive)  
- Round Robin (quantum=2)  
- Priority Scheduling (Non-Preemptive)  
- CFS (Simplified Model Using Virtual Runtime)

### **Advanced System Analysis**
- Live Linux process capture (pid, CPU time, priority)
- Real vs simulated wait time comparison
- Starvation flagging for long-wait processes
- Convoy Effect demonstration
- Gantt Chart Visualization (Matplotlib)
- Dual logging (Console + results/ files)

---

# 🛠 Installation

```bash
git clone https://github.com/devsharma1209/OS-Project.git
cd OS-Project
pip install -r requirements.txt
```

---

# 💻 Usage

## **1️⃣ Scientific Mode (Simulations on Static Workloads)**

### **Dataset A – Mixed Workload**
```bash
python3 main.py --mode scientific --workload dataset_A_basic.json
```

### **Dataset B – Convoy Effect Demonstration**
```bash
python3 main.py --mode scientific --workload dataset_B_convoy.json
```

### **Dataset D – Priority Starvation**
```bash
python3 main.py --mode scientific --workload dataset_D_starvation.json
```

---

## **2️⃣ Live Mode (Linux System Analysis)**  
*Requires Linux: AWS EC2 recommended.*

```bash
python3 main.py --mode live
```

Live mode:

- Fetches the top 10 active processes
- Computes real vs simulated wait time
- Saves snapshot to `workloads/live_snapshot.json`
- Generates analysis → `results/live_mode_report.txt`

---

## **3️⃣ Bridge Mode (Replay the Live Snapshot)**  
Visualize and analyze real Linux processes using algorithms:

```bash
python3 main.py --mode scientific --workload live_snapshot.json
```

---

# 🧪 Stress Test: Reproducing the Convoy Effect

1. Run CPU-intensive spam processes:
```bash
yes > /dev/null &
yes > /dev/null &
yes > /dev/null &
```
2. Capture live snapshot:
```bash
python3 main.py --mode live
```
3. Terminate load:
```bash
killall yes
```
4. Replay the snapshot:
```bash
python3 main.py --mode scientific --workload live_snapshot.json
```

---

# 📊 Highlighted Results

### **1. Convoy Effect (High Load Scenario)**

| Metric | FCFS | SJF | Improvement |
|-------|------|------|-------------|
| Avg Waiting Time | 55.10s | 14.70s | **3.7× faster** |
| Responsiveness | Poor | Excellent | SJF avoids convoy blocking |

The Gantt charts (in `results/`) clearly show short processes trapped behind CPU hogs under FCFS.

---

### **2. Reality Check (Live Linux Processes)**

Example:

```
PID      | Sim Wait | Actual Wait | Diff
1        | 10.00s   | 360.00s     | +350s
```

**Insight:**  
Actual Linux wait time is massive because real processes spend most time in the **Blocked/IO** state — something classical schedulers don't simulate.

---

# 📂 Project Structure

```
OS-Project/
│
├── main.py                # CLI entry point
├── algorithms.py          # Scheduling algorithms
├── linux_fetch.py         # Live Linux process capture
├── utils.py               # Metrics, calculations, helpers
├── gantt.py               # Gantt chart visualizer
│
├── workloads/
│   ├── dataset_A_basic.json
│   ├── dataset_B_convoy.json
│   ├── dataset_D_starvation.json
│   └── live_snapshot.json   # Auto-generated
│
├── results/
│   ├── live_mode_report.txt
│   └── live_snapshot.png
│
├── screenshots/
│   └── aws_run.png
│
├── requirements.txt
└── LICENSE
```

---

# ⚠️ Notes & Limitations

- True Linux wait time is not exposed to user-space.  
  This project approximates it as:

  **`actual_wait = elapsed_time - cpu_time`**

- Simplified CFS does not reflect the fully accurate Linux kernel implementation.
- All arrival times in scientific mode default to 0 unless specified.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

Copyright (c) 2025 Dev Sharma
