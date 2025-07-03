# Projeto - Sistemas Operacionais  
**UTFPR – 2025/1**

## 📌 Sobre o Projeto
Este projeto foi desenvolvido como parte da disciplina de Sistemas Operacionais (SO) na UTFPR.

O objetivo do projeto é aplicar conceitos fundamentais de sistemas operacionais, como gerenciamento de processos, uso de chamadas de sistema, monitoramento de recursos e concorrência.

## 🖥️ Tecnologias Utilizadas
- 🐧 Linux
- 🐳 Docker e Docker Compose
- 🐍 Python (coleta e monitoramento de processos)
- 📊 Grafana (visualização dos dados)
- 🌐 FastAPI (backend REST)
- 📁 /proc (coleta de dados diretamente do kernel)
- 🔧 Traefik (proxy reverso com TLS)

## 🎯 Funcionalidades
- Monitoramento de uso de CPU, memória e disco
- Coleta de dados por processo (PID, uso de CPU individual, memória, UID, etc.)
- Visualização via dashboard
- Backend multithread para coleta contínua de dados

## 📁 Estrutura do Projeto
```bash
.
├── app/                  # API FastAPI com coleta de dados do sistema
├── grafana-storage/      # Apresentação no Grafana
├── Dockerfile
├── docker-compose.yml    # Orquestração dos serviços
└── README.md
```

## 🚀 Como Executar
1. Clone o repositório:
   ```bash
   git clone https://github.com/SEU_USUARIO/os-dashboard.git
   cd os-dashboard
   ```

2. Defina variáveis no `.env`:
   ```env
   PASSWORD=senha_admin_grafana
   GRAFANA_DOMAIN=grafana.seudominio.com
   ```

3. Execute com Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Acesse:
   - Grafana: `https://grafana.seudominio.com` (login padrão: admin / sua senha)
