"""
Autor: Thiago Costa
Data: 01/05/2025
Disciplina: Sistemas Operacionais - UTFPR

Classe criada para coletar informacoes de uso de memoria RAM e SWAP
a partir do arquivo /proc/meminfo

A classe calcula a memoria total, disponivel, utilizada e percentual de uso,
tanto da memoria principal quanto da memoria swap
"""

from typing import Dict
import os


class MemoryInfo:
    def __init__(self, proc_path: str = "/proc"):
        self.proc_path = proc_path
        self.mem_total_kb = 0
        self.mem_free_kb = 0
        self.mem_available_kb = 0
        self.swap_total_kb = 0
        self.swap_free_kb = 0

    def update(self):
        meminfo_path = os.path.join(self.proc_path, "meminfo")
        try:
            with open(meminfo_path) as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) < 2:
                        continue
                    key, value = parts[0], int(parts[1])
                    if key == "MemTotal:":
                        self.mem_total_kb = value
                    elif key == "MemFree:":
                        self.mem_free_kb = value
                    elif key == "MemAvailable:":
                        self.mem_available_kb = value
                    elif key == "SwapTotal:":
                        self.swap_total_kb = value
                    elif key == "SwapFree:":
                        self.swap_free_kb = value
        except Exception as e:
            print(f"[MemoryInfo] Erro ao ler meminfo: {e}")

    def as_dict(self) -> Dict[str, float]:
        mem_used_kb = self.mem_total_kb - self.mem_available_kb
        swap_used_kb = self.swap_total_kb - self.swap_free_kb

        return {
            "mem_total_mb": round(self.mem_total_kb / 1024, 2),
            "mem_available_mb": round(self.mem_available_kb / 1024, 2),
            "mem_used_mb": round(mem_used_kb / 1024, 2),
            "mem_used_percent": (
                round((mem_used_kb / self.mem_total_kb) * 100, 2)
                if self.mem_total_kb
                else 0
            ),
            "swap_total_mb": round(self.swap_total_kb / 1024, 2),
            "swap_used_mb": round(swap_used_kb / 1024, 2),
            "swap_used_percent": (
                round((swap_used_kb / self.swap_total_kb) * 100, 2)
                if self.swap_total_kb
                else 0
            ),
        }
