# Módulo 1 — Ambientes Virtuais (venv, virtualenv, conda)

## Teoria
- Sem isolamento, tudo cai no Python do sistema e projetos diferentes podem exigir versões conflitantes da mesma biblioteca.
- Um ambiente virtual cria uma cópia isolada do interpretador + um diretório próprio de pacotes.
- **venv**: módulo nativo da stdlib, leve, sem instalação extra — usado neste currículo.
- **virtualenv**: ferramenta de terceiros, antecessora do venv.
- **conda**: gerenciador mais pesado, comum em data science, gerencia também dependências não-Python.

## Prática
- `python -m venv .venv` cria o ambiente.
- Estrutura gerada: `pyvenv.cfg` (aponta pro Python base), `bin/` (executáveis python/pip + scripts de ativação), `lib/`+`lib64/` (onde pacotes instalados ficam, em site-packages), `include/` (headers C).
- `source .venv/bin/activate` ativa o ambiente; `command -v python` confirma que passa a apontar pra dentro de `.venv/bin/python`.
- `deactivate` volta o PATH ao normal; `command -v python` volta a apontar pro Python do sistema.
- Isolamento confirmado: `pip install requests` dentro do venv só instala ali; `import requests` funciona dentro do venv e dá `ModuleNotFoundError` fora dele.

## Observações
- No Termux, `which` não vem instalado por padrão — usado `command -v` como alternativa nativa do shell.
- Ativar um venv é só uma mudança de PATH; nada é "instalado" globalmente.
