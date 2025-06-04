"""
Autor: Thiago Costa
Data: 03/06/2025
Disciplina: Sistemas Operacionais - UTFPR

Classe desenvolvida para navegar e coletar informacoes detalhadas sobre os arquivos e diretorios
de um caminho base no sistema de arquivos, simulando um navegador de diretorios.

Usa a biblioteca os mais basica para listar entradas no diretorio indicado, coletando para cada item:
    - nome
    - se eh diretorio ou arquivo
    - tamanho em bytes
    - permissoes
    - data e hora da altima modificacao
"""

import os
import stat
import time


class DirectoryNavigator:
    def __init__(self, base_path="/host_root"):
        self.base_path = base_path
        self.relative_path = "/"
        self.entries = []

    def set_path(self, relative_path="/"):
        self.relative_path = relative_path

    def update(self):
        self.entries = self._collect_directory_info()

    def as_dict(self):
        return {"path": self.relative_path, "entries": self.entries}

    def _collect_directory_info(self):
        abs_path = os.path.join(self.base_path, self.relative_path.lstrip("/"))
        entries = []

        try:
            with os.scandir(abs_path) as it:
                for entry in it:
                    try:
                        stats = entry.stat(follow_symlinks=False)
                        entry_info = {
                            "name": entry.name,
                            "is_dir": entry.is_dir(follow_symlinks=False),
                            "size_bytes": stats.st_size,
                            "permissions": stat.filemode(stats.st_mode),
                            "modified_time": time.strftime(
                                "%Y-%m-%d %H:%M:%S", time.localtime(stats.st_mtime)
                            ),
                        }
                        entries.append(entry_info)
                    except Exception as e:
                        entries.append({"name": entry.name, "error": str(e)})
        except Exception as e:
            return [{"error": str(e)}]

        return entries
