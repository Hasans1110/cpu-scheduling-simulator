# CPU Scheduling Simulator

This project simulates various CPU scheduling algorithms as part of CS 3502 - Operating Systems.

## Files
- `scheduling_simulator.py` - Main Python source code containing all implemented scheduling algorithms and plot generation.

## Scheduling Algorithms Implemented
- First-Come-First-Served (FCFS)
- Shortest Job First (SJF)
- Round Robin (RR) with quantum=3
- Priority Scheduling (Non-preemptive)
- Highest Response Ratio Next (HRRN)
- Multi-Level Queue (MLQ)

## How to Run
1. Ensure you have Python 3 installed.
2. Install the required libraries (only matplotlib):
```bash
pip install matplotlib
```
3. Open a terminal or command prompt.
4. Navigate to the project directory.
5. Run the Python file:
```bash
python scheduling_simulator.py
```
6. The scheduling results will be printed, and performance graphs will be displayed.

## Notes
- No external libraries are required other than matplotlib (for plotting).
- Customize the process list in the code if you want to test with different input processes.
