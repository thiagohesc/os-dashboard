"""
Autor: Thiago Costa
Data: 03/06/2025
Disciplina: Sistemas Operacionais - UTFPR

Classe criada para coletar informacoes sobre os sistemas de arquivos montados no sistema,
lendo os pontos de montagem a partir do arquivo /proc/mounts

Para cada ponto de montagem valido, coleta uso do sistema de arquivos,
incluindo:
    - dispositivo montado
    - ponto de montagem
    - espaco total, usado e livre (em MB)
    - percentual de uso do disco

Ignora pontos de montagem duplicados ou inexistentes no caminho do sistema de arquivos host.
Em caso de erro na leitura, registra mensagem de erro na saida.
"""

import os


class FileSystemInfo:
    def __init__(self, proc_mounts_path="/host_proc/mounts", host_root="/host_root"):
        self.proc_mounts_path = proc_mounts_path
        self.host_root = host_root
        self.mounts = []

    def update(self):
        self.mounts = self._collect_mount_info()

    def as_dict(self):
        return {"data": self.mounts}

    def _collect_mount_info(self):
        seen = set()
        data = []

        try:
            with open(self.proc_mounts_path, "r") as f:
                for line in f:
                    parts = line.split()
                    if len(parts) >= 2:
                        device = parts[0]
                        mount_point = parts[1]

                        if mount_point in seen:
                            continue
                        seen.add(mount_point)

                        full_mount_path = os.path.join(
                            self.host_root, mount_point.lstrip("/")
                        )

                        if not os.path.exists(full_mount_path):
                            continue

                        try:
                            stats = os.statvfs(full_mount_path)
                            total = stats.f_frsize * stats.f_blocks
                            free = stats.f_frsize * stats.f_bfree
                            used = total - free
                            percent = (used / total) * 100 if total > 0 else 0
                        except Exception:
                            total = free = used = percent = 0

                        data.append(
                            {
                                "mount_point": mount_point,
                                "device": device,
                                "total_mb": round(total / 1024**2, 2),
                                "used_mb": round(used / 1024**2, 2),
                                "free_mb": round(free / 1024**2, 2),
                                "percent_used": round(percent, 2),
                            }
                        )
        except Exception as e:
            data.append({"error": str(e)})

        return data
