"""
Autor: Thiago Costa
Data: 01/05/2025
Disciplina: Sistemas Operacionais - UTFPR

Classe criada para coletar informacoes gerais sobre a CPU usando os dados do /proc/stat,
como:
    Uso total e por core
    tempo de sistema ligado
    numero de processos e quantos estao em execucao
"""

from typing import Dict
from datetime import datetime, timezone
import tzlocal
import os


class CpuInfo:
    def __init__(self, proc_path: str = "/proc"):
        self.proc_path = proc_path
        self._prev_stats: Dict[str, Dict[str, int]] = {}
        self.usage_per_core: Dict[str, float] = {}
        self.total_usage_percent: float = 0.0
        self.idle_time: int = 0
        self.total_processes: int = 0
        self.procs_running: int = 0
        self.boot_time: int = 0

    def update(self):
        self._parse_cpu_lines()
        self._parse_metadata()

    def _parse_cpu_lines(self):
        try:
            with open(os.path.join(self.proc_path, "stat")) as f:
                lines = f.readlines()

            for line in lines:
                if not line.startswith("cpu"):
                    continue

                parts = line.strip().split()
                core = parts[0]
                values = list(map(int, parts[1:]))[:8]

                user, nice, system, idle, iowait, irq, softirq, steal = values
                user_total = user + nice
                system_total = system + irq + softirq
                idle_total = idle + iowait
                total = user_total + system_total + idle_total + steal

                prev_total = self._prev_stats.get(core, {}).get("total", 0)
                prev_idle = self._prev_stats.get(core, {}).get("idle", 0)

                diff_total = total - prev_total
                diff_idle = idle_total - prev_idle

                usage_percent = (
                    (1 - (diff_idle / diff_total)) * 100 if diff_total > 0 else 0.0
                )
                self.usage_per_core[core] = round(usage_percent, 2)

                if core == "cpu":
                    self.total_usage_percent = round(usage_percent, 2)
                    self.idle_time = idle_total

                self._prev_stats[core] = {
                    "total": total,
                    "idle": idle_total,
                    "user": user_total,
                    "system": system_total,
                }

        except Exception as e:
            print(f"[CpuInfo] Erro ao ler {self.proc_path}/stat (CPU lines): {e}")

    def _parse_metadata(self):
        try:
            with open(os.path.join(self.proc_path, "stat")) as f:
                for line in f:
                    if line.startswith("processes"):
                        self.total_processes = int(line.strip().split()[1])
                    elif line.startswith("procs_running"):
                        self.procs_running = int(line.strip().split()[1])
                    elif line.startswith("btime"):
                        self.boot_time = int(line.strip().split()[1])
        except Exception as e:
            print(f"[CpuInfo] Erro ao ler {self.proc_path}/stat (metadata): {e}")

    def as_dict(self):
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_cpu_usage_percent": self.total_usage_percent,
            "idle_time": self.idle_time,
            "total_processes": self.total_processes,
            "procs_running": self.procs_running,
            "boot_time": datetime.fromtimestamp(
                self.boot_time, tzlocal.get_localzone()
            ).strftime("%d/%m/%Y %H:%M:%S"),
            "cores": {
                core: {
                    "usage_percent": self.usage_per_core.get(core, 0.0),
                    "user": self._prev_stats.get(core, {}).get("user", 0),
                    "system": self._prev_stats.get(core, {}).get("system", 0),
                    "idle": self._prev_stats.get(core, {}).get("idle", 0),
                    "total": self._prev_stats.get(core, {}).get("total", 0),
                }
                for core in self.usage_per_core
            },
        }
