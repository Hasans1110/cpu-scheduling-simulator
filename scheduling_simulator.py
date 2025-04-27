import copy
from collections import deque
import matplotlib.pyplot as plt

class Process:
    def __init__(self, pid, arrival, burst, priority=None):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.priority = priority
        self.start = -1
        self.end = -1
        self.waiting = 0
        self.turnaround = 0

def calculate_metrics(processes, total_time):
    total_waiting = 0
    total_turnaround = 0
    total_burst = sum(p.burst for p in processes)
    num_processes = len(processes)

    for p in processes:
        p.turnaround = p.end - p.arrival
        p.waiting = p.turnaround - p.burst
        total_waiting += p.waiting
        total_turnaround += p.turnaround

    return {
        "AWT": total_waiting / num_processes,
        "ATT": total_turnaround / num_processes,
        "CPU Utilization": (total_burst / total_time) * 100 if total_time > 0 else 0,
        "Throughput": num_processes / total_time if total_time > 0 else 0
    }

def fcfs(processes):
    procs = sorted(copy.deepcopy(processes), key=lambda x: x.arrival)
    current_time = 0
    for p in procs:
        if current_time < p.arrival:
            current_time = p.arrival
        p.start = current_time
        current_time += p.burst
        p.end = current_time
    return calculate_metrics(procs, current_time)

def sjf(processes):
    procs = copy.deepcopy(processes)
    current_time = 0
    completed = []
    ready = []
    while len(completed) < len(procs):
        ready += [p for p in procs if p.arrival <= current_time and p not in completed and p not in ready]
        if ready:
            ready.sort(key=lambda x: x.burst)
            current_process = ready.pop(0)
            current_process.start = current_time
            current_time += current_process.burst
            current_process.end = current_time
            completed.append(current_process)
        else:
            current_time += 1
    return calculate_metrics(completed, current_time)

def round_robin(processes, quantum=3):
    procs = copy.deepcopy(processes)
    queue = deque()
    current_time = 0
    completed = []
    procs_sorted = sorted(procs, key=lambda x: x.arrival)
    ptr = 0
    while ptr < len(procs_sorted) or queue:
        while ptr < len(procs_sorted) and procs_sorted[ptr].arrival <= current_time:
            queue.append(procs_sorted[ptr])
            ptr += 1
        if queue:
            current_process = queue.popleft()
            if current_process.start == -1:
                current_process.start = current_time
            exec_time = min(quantum, current_process.remaining)
            current_time += exec_time
            current_process.remaining -= exec_time
            if current_process.remaining > 0:
                queue.append(current_process)
            else:
                current_process.end = current_time
                completed.append(current_process)
        else:
            current_time += 1
    return calculate_metrics(completed, current_time)

def priority_scheduling(processes):
    procs = copy.deepcopy(processes)
    current_time = 0
    completed = []
    ready = []
    while len(completed) < len(procs):
        ready += [p for p in procs if p.arrival <= current_time and p not in completed and p not in ready]
        if ready:
            ready.sort(key=lambda x: x.priority)
            current_process = ready.pop(0)
            current_process.start = current_time
            current_time += current_process.burst
            current_process.end = current_time
            completed.append(current_process)
        else:
            current_time += 1
    return calculate_metrics(completed, current_time)

def hrrn(processes):
    procs = copy.deepcopy(processes)
    current_time = 0
    completed = []
    ready = []
    while len(completed) < len(procs):
        ready += [p for p in procs if p.arrival <= current_time and p not in completed and p not in ready]
        if ready:
            ready.sort(key=lambda x: ((current_time - x.arrival) + x.burst)/x.burst, reverse=True)
            current_process = ready.pop(0)
            current_process.start = current_time
            current_time += current_process.burst
            current_process.end = current_time
            completed.append(current_process)
        else:
            current_time += 1
    return calculate_metrics(completed, current_time)

def mlq(processes, high_prio_cutoff=2, quantum=3):
    procs = copy.deepcopy(processes)
    current_time = 0
    completed = []
    high_queue = [p for p in procs if p.priority < high_prio_cutoff]
    low_queue = deque([p for p in procs if p.priority >= high_prio_cutoff])
    high_queue.sort(key=lambda x: x.arrival)
    for p in high_queue:
        if current_time < p.arrival:
            current_time = p.arrival
        p.start = current_time
        current_time += p.burst
        p.end = current_time
        completed.append(p)
    while low_queue:
        current_process = low_queue.popleft()
        if current_process.start == -1:
            current_process.start = max(current_process.arrival, current_time)
        exec_time = min(quantum, current_process.remaining)
        current_time += exec_time
        current_process.remaining -= exec_time
        if current_process.remaining > 0:
            low_queue.append(current_process)
        else:
            current_process.end = current_time
            completed.append(current_process)
    return calculate_metrics(completed, current_time)

if __name__ == "__main__":
    processes = [
        Process(1, 0, 5, 1),
        Process(2, 1, 3, 3),
        Process(3, 2, 8, 2),
        Process(4, 3, 2, 1),
        Process(5, 4, 4, 2)
    ]
    algorithms = {
        "FCFS": fcfs,
        "SJF": sjf,
        "Round Robin": round_robin,
        "Priority": priority_scheduling,
        "HRRN": hrrn,
        "MLQ": mlq
    }
    results = {}
    for name, func in algorithms.items():
        results[name] = func(processes)

    print(f"{'Algorithm':<12} | {'AWT':<6} | {'ATT':<6} | {'CPU Util (%)':<10} | {'Throughput':<10}")
    print("-" * 60)
    for algo, metrics in results.items():
        print(f"{algo:<12} | {metrics['AWT']:.2f} | {metrics['ATT']:.2f} | {metrics['CPU Utilization']:.2f}%      | {metrics['Throughput']:.2f}")

    metrics = ['AWT', 'ATT', 'CPU Utilization', 'Throughput']
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    for i, metric in enumerate(metrics):
        ax = axs[i//2, i%2]
        values = [results[algo][metric] for algo in algorithms]
        ax.bar(algorithms.keys(), values)
        ax.set_title(metric)
        if '%' in metric:
            ax.set_ylabel('Percentage')
        else:
            ax.set_ylabel('Time' if 'Time' in metric else 'Rate')
    plt.tight_layout()
    plt.show()
