# ⚡ OS Process Scheduler & Linux Integration Toolkit

### Operating Systems & Networking Group Project

  

## 📖 Overview

This project is a hybrid **CPU Scheduling Simulator** and **Linux System Analysis Tool**. It bridges the gap between theoretical OS algorithms and real-world process management.

It operates in two distinct modes:

1.  **🔬 Scientific Mode:** A deterministic environment to simulate, visualize, and compare classical scheduling algorithms (FCFS, SJF, SRTF, RR, Priority) using controlled JSON workloads.
2.  **🐧 Live Mode:** A real-time system integrator that fetches active processes from the Linux kernel, analyzes their states, and performs a "Reality Check" comparing theoretical scheduling against the actual Linux CFS (Completely Fair Scheduler).

-----

## 🚀 Key Features

### 1\. Algorithms Implemented

  * **FCFS** (First-Come, First-Served)
  * **SJF** (Shortest Job First - Non-Preemptive)
  * **SRTF** (Shortest Remaining Time First - Preemptive)
  * **Round Robin** (Configurable Time Quantum)
  * **Priority Scheduling** (Non-Preemptive)
  * **Linux CFS** (Simplified Simulation)

### 2\. Advanced Analytics

  * **Live Linux Snapshotting:** Captures `pid`, `burst` (CPU time), and `priority` from real system daemons.
  * **Reality Check Engine:** Compares **Simulated Wait Time** (CPU Ready Queue) vs. **Actual Linux Wait Time** (Total Blocked/Sleep Time).
  * **Stress Test Analysis:** visualizes the **Convoy Effect** under high load.
  * **Starvation Detection:** Automatically flags processes waiting beyond a dynamic threshold.
  * **Dual Logging:** Outputs analysis to both Console and `results/` text files simultaneously.

-----

## 🛠️ Installation

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/devsharma1209/OS-Project.git
    cd OS-Project
    ```

2.  **Install Dependencies:**
    This project requires `matplotlib` for Gantt charts and `tabulate` for formatted tables.

    ```bash
    pip install matplotlib tabulate
    ```

-----

## 💻 Usage Guide

### Mode 1: Scientific Simulation

Run the simulator on a pre-defined workload to generate Gantt charts and metric tables.

```bash
python3 main.py --mode scientific --workload dataset_A_basic.json
```

  * **Input:** JSON file in `workloads/`.
  * **Output:** Console metrics + PNG Gantt chart in `results/`.

### Mode 2: Live Linux Analysis

**Note:** *Must be run on a Linux environment (e.g., AWS EC2, Ubuntu) to fetch real process data.*

```bash
python3 main.py --mode live
```

  * **Action:** Fetches top 10 active processes using `ps -eo`.
  * **Output:**
      * Generates a `live_mode_report.txt`.
      * Saves a snapshot to `workloads/live_snapshot.json`.
      * Recommends the best algorithm for the current system load.

### Mode 3: The "Bridge" (Visualizing Live Data)

After running Live Mode, you can visualize the real-world data by feeding the snapshot back into the simulator:

```bash
python3 main.py --mode scientific --workload live_snapshot.json
```

  * **Result:** Generates a Gantt chart of your actual Cloud Server's state.

-----

## 📊 Sample Results & Analysis

### 1\. The Convoy Effect (Stress Test)

By injecting high-burst CPU processes (`yes > /dev/null`), we observed the failure of FCFS in a live environment.

| Metric | FCFS (Baseline) | SJF (Optimized) | Result |
| :--- | :--- | :--- | :--- |
| **Avg Wait Time** | 55.10s | 14.70s | **3.7x Improvement** |
| **responsiveness** | Frozen | Fluid | SJF prioritizes system daemons |

**Visual Proof:**
*(Place your `live_snapshot.png` here)*

> *The Gantt chart above shows FCFS (Top) blocking system tasks behind heavy loads, while Round Robin (4th Row) fragments the load to maintain responsiveness.*

### 2\. Reality Check (Simulated vs Actual)

```text
PID      | Name            | Sim Wait (RR)   | Actual Wait     | Diff
1        | systemd         | 10.00s          | 360.00s         | +350.00
```

**Insight:** The massive difference (+350s) indicates that real OS processes spend the majority of their time in the **Blocked/Waiting State** (waiting for I/O), not the **Ready State** (waiting for CPU).

-----

## 📂 Project Structure

```text
OS-Project/
│
├── main.py                # Entry point (CLI Argument Parser)
├── algorithms.py          # Core Scheduling Logic (FCFS, SJF, RR, etc.)
├── linux_fetch.py         # Interface to Linux Kernel (subprocess/ps)
├── utils.py               # Metrics Calculation & Math
├── gantt.py               # Matplotlib Visualization Engine
│
├── workloads/             # JSON Datasets
│   ├── dataset_A_basic.json
│   ├── dataset_B_convoy.json
│   └── live_snapshot.json # Auto-generated from Live Mode
│
└── results/               # Output Artifacts
    ├── live_mode_report.txt
    └── live_snapshot.png
```

-----

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

Copyright (c) 2025 Dev Sharma
