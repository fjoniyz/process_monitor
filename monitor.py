import psutil
import datetime
from tabulate import tabulate
import os
import time
def get_process():
    processes = []
    for p in psutil.process_iter():
        with p.oneshot():
            process_id = p.pid
            if process_id == 0:
                continue
            name = p.name()
            try:
                create_time = datetime.datetime.fromtimestamp(p.create_time())
            except OSError:
                create_time = datetime.datetime.fromtimestamp(psutil.boot_time())
            cpu_usage = p.cpu_percent()
            try:
                cpu_affinity = len(p.cpu_affinity())
            except psutil.AccessDenied:
                cpu_affinity = 0
            status = p.status()
            try:
                memory = p.memory_full_info().uss
            except psutil.AccessDenied:
                memory = 0
            try:
                user = p.username()
            except psutil.AccessDenied:
                user = "N/A"
        processes.append({
            'process_id': process_id,
            'name': name,
            'create_time': create_time,
            'cpu_usage': cpu_usage,
            'status': status,
            'cpu_affinity': cpu_affinity,
            'memory': get_size(memory),
            'user': user
        })
    return processes

def get_size(bytes):
    for i in ['', 'K', 'M', 'G', 'T', 'P', 'E']:
        if bytes < 1024:
            return f"{bytes:.2f}{i}B"
        bytes /= 1024
def print_processes(ps):
    print(tabulate(ps, headers="keys"))
processes = get_process()
while True:
    print_processes(processes)
    time.sleep(1)
    processes = get_process()   
    if "nt" in os.name:
        os.system("cls")
    else:
        os.system("clear")