"""
Autor: Thiago Costa
Data: 01/05/2025
Disciplina: Sistemas Operacionais - UTFPR

Backend feito com FastAPI que expoe os dados do sistema operacional em um dicionario
consumido pelo frontend no grafana
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from cpu_info import CpuInfo
from memory_info import MemoryInfo
from process_info import ProcessInfo

app = FastAPI()

cpu = CpuInfo(proc_path="/host_proc")
memory = MemoryInfo(proc_path="/host_proc")
proc = ProcessInfo(proc="/host_proc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/cpu")
def get_cpu():
    cpu.update()
    return cpu.as_dict()


@app.get("/api/memory")
def get_memory():
    memory.update()
    return memory.as_dict()


@app.get("/api/processes")
def get_processes():
    proc.update()
    return proc.as_dict()
