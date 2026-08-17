#Módulo 15 — uv na prática



Teoria



uv é um gerenciador de pacotes e projetos Python escrito em Rust pela Astral (mesma equipe do Ruff). Substitui, num único binário, o papel que hoje é dividido entre pip, pip-tools, virtualenv, pyenv e pipx. Principais diferenciais em relação ao que vimos nos módulos 1-14:



• Build backend próprio (uv_build) — não depende de setuptools/hatchling/poetry-core

• Lockfile universal (uv.lock) — resolve pra múltiplas plataformas e versões de Python no mesmo arquivo, diferente do pip-compile (módulo 11), que gera um lock específico da plataforma atual

• Gerencia interpretadores Python — uv python install baixa CPython isolado, sem depender do gerenciador de pacotes do sistema

• Separação explícita entre resolver e instalar — uv lock só resolve dependências e grava o lockfile; uv sync lê o lockfile e instala. uv add/uv remove fazem os dois passos automaticamente



Ambiente: por que não rodou direto no Termux



uv não tem suporte oficial a Android/Termux — os binários oficiais cobrem apenas Linux (glibc/musl), macOS, Windows e FreeBSD, sem target para aarch64-linux-android. O instalador oficial (curl | sh) detecta essa plataforma e recusa a instalação; pip install uv também falha, pois tentaria compilar do zero com Rust/maturin — mesma classe de barreira do nh3 no módulo 14.



Solução: instalar um Ubuntu 24.04 via proot-distro dentro do Termux (container rootless com glibc de verdade) e rodar o uv lá dentro normalmente.

pkg install proot-distro
proot-distro install ubuntu:24.04
proot-distro login ubuntu
apt update && apt upgrade -y
apt install -y curl git python3 build-essential
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

Prática — os 6 comandos



Comando O que faz Observação

uv init Cria projeto novo (pyproject.toml, src/, .git, .python-version) requires-python detectado automaticamente a partir do interpretador do sistema

uv add <pkg> Adiciona dependência, cria .venv, resolve e grava uv.lock Tudo num comando só — substitui o fluxo manual pip+venv+freeze

uv run <cmd> Roda comando/entry point dentro do venv do projeto Não precisa source .venv/bin/activate

uv sync Instala exatamente o que está no uv.lock Não resolve nada — só materializa o lock. Testado: rm -rf .venv && uv sync reconstruiu o ambiente idêntico em 11ms

uv lock Resolve dependências e grava o uv.lock, sem instalar Testado: editar pyproject.toml na mão + uv lock atualiza o lockfile mas não mexe no .venv até rodar uv sync

uv python install <versão> Baixa e instala um CPython gerenciado pelo uv Isolado em ~/.local/share/uv/python/, não conflita com o Python do sistema



Detalhe de ambiente



Dentro do proot-distro, o uv python list mostra tanto interpretadores nativos do Ubuntu (/usr/bin/python3.12) quanto do Termux host (/data/data/com.termux/files/usr/bin/python3.14) — o proot expõe o PATH do Termux dentro do container por padrão.


