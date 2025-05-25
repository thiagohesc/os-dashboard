"""
Autor: Thiago Costa
Data: 01/05/2025
Disciplina: Sistemas Operacionais - UTFPR

Classe desenvolvida para coletar e calcular informacoes sobre todos os
processos em execucao no sistema usando:
    /proc/[pid]/status: para obter nome do processo, UID, numero de threads e memoria (VmRSS)
    /proc/[pid]/cmdline: para capturar os argumentos de execucao do processo
    /proc/[pid]/stat: para calcular o tempo de CPU
    /proc/stat: para calcular o tempo total da CPU

As informacoes extraidas:
    PID, name, user e threads;
    uso de memoria (VmRSS);
    uso de CPU;
    argumentos de execucao do processo

Usei multithreading com a biblioteca `threading` para coletar as informacoes dos processos em paralelo
"""

import os
import threading
import time
import pwd


class ProcessInfo:
    def __init__(self, proc="/proc"):
        self.proc = proc
        self.processes = []

    def update(self, delay=1.0, max_threads=8):
        self.processes = self._get_all_processes_with_cpu(
            delay=delay, max_threads=max_threads
        )

    def as_dict(self):
        return {
            "processes": [
                {
                    "pid": p["pid"],
                    "name": p["name"],
                    "user": p["user"],
                    "threads": p["threads"],
                    "cpu_percent": f'{p["cpu_percent"]:.2f}',
                    "mem_rss_mb": round(p.get("mem_rss_mb", 0), 2),
                    "args": p["args"],
                }
                for p in self.processes
            ]
        }

    def _list_pids(self):
        try:
            return [pid for pid in os.listdir(self.proc) if pid.isdigit()]
        except:
            return []

    def _read_status(self, pid):
        info = {"name": "", "uid": "", "user": "", "threads": 0, "mem": {}}
        try:
            with open(f"{self.proc}/{pid}/status") as f:
                for line in f:
                    if line.startswith("Name:"):
                        info["name"] = line.split()[1]
                    elif line.startswith("Uid:"):
                        info["uid"] = line.split()[1]
                        try:
                            info["user"] = pwd.getpwuid(int(info["uid"])).pw_name
                        except:
                            info["user"] = info["uid"]
                    elif line.startswith("Threads:"):
                        info["threads"] = int(line.split()[1])
                    elif line.startswith("VmRSS:"):
                        info["mem"]["rss"] = int(line.split()[1])
        except:
            pass
        return info

    def _read_cmdline(self, pid):
        try:
            with open(f"{self.proc}/{pid}/cmdline", "rb") as f:
                raw = f.read()
                args = raw.decode().split("\0")
                return " ".join(arg for arg in args if arg)
        except:
            return ""

    def _read_cpu_time(self, pid):
        try:
            with open(f"{self.proc}/{pid}/stat") as f:
                parts = f.readline().split()
                utime = int(parts[13])
                stime = int(parts[14])
                return utime + stime
        except:
            return 0

    def _get_total_cpu_time(self):
        try:
            with open(f"{self.proc}/stat") as f:
                parts = list(map(int, f.readline().strip().split()[1:]))
            return sum(parts)
        except:
            return 0

    def _get_process_info(self, pid):
        try:
            info = {
                "pid": pid,
                "args": self._read_cmdline(pid),
                "cpu_time": self._read_cpu_time(pid),
                "cpu_percent": 0.0,
            }
            info.update(self._read_status(pid))
            mem_kb = info.get("mem", {}).get("rss", 0)
            info["mem_rss_mb"] = mem_kb / 1024
            return info
        except:
            return None

    def _get_all_processes(self, max_threads=8):
        results = []
        threads = []
        lock = threading.Lock()
        semaphore = threading.Semaphore(max_threads)

        def collect(pid):
            with semaphore:
                proc_info = self._get_process_info(pid)
                if proc_info:
                    with lock:
                        results.append(proc_info)

        for pid in self._list_pids():
            t = threading.Thread(target=collect, args=(pid,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return results

    def _get_all_processes_with_cpu(self, delay=1.0, max_threads=8):
        pids = self._list_pids()
        cpu1 = self._get_total_cpu_time()
        proc1 = {pid: self._read_cpu_time(pid) for pid in pids}

        time.sleep(delay)

        cpu2 = self._get_total_cpu_time()
        proc2 = {pid: self._read_cpu_time(pid) for pid in pids}
        delta_cpu = cpu2 - cpu1

        processes = self._get_all_processes(max_threads=max_threads)

        for proc in processes:
            pid = proc["pid"]
            delta_proc = proc2.get(pid, 0) - proc1.get(pid, 0)
            if delta_cpu > 0:
                proc["cpu_percent"] = round(
                    (delta_proc / delta_cpu) * os.cpu_count() * 100, 2
                )
            else:
                proc["cpu_percent"] = 0.0

        return processes
