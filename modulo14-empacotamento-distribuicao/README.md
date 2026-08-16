# meupacote-joao-teste


# Módulo 14 — Empacotamento e distribuição (build, twine, TestPyPI)

## Objetivo
Entender o fluxo de empacotamento de um projeto Python: gerar os
artefatos de distribuição (sdist + wheel) e o processo de publicação
num índice via twine/TestPyPI.

## Ferramentas
- **build**: front-end oficial (PEP 517) que lê o `pyproject.toml` e
gera os artefatos em `dist/`.
- **twine**: faz upload dos artefatos pro índice (PyPI/TestPyPI) via
HTTPS, e valida metadados com `twine check`.
- **TestPyPI**: índice de teste (test.pypi.org), separado do PyPI
real, pra testar publicação sem sujar o índice de produção.

## Limitação de ambiente (Termux)
`pip install twine` falha ao compilar `nh3` (dependência do
`readme-renderer`, extensão Rust via PyO3/maturin):

1. Primeiro erro: falta de `ANDROID_API_LEVEL` — resolvido com
`export ANDROID_API_LEVEL=24`.
2. Segundo erro, mais profundo: `crate X required to be available
in rlib format` em dezenas de crates da std do Rust. É um bug
conhecido e ainda aberto do toolchain Rust no Termux ao compilar
extensões PyO3/maturin — sem solução simples disponível no momento.

Como `build` não tem nenhuma dependência Rust, segui só com
`pip install build`, e tratei `twine`/upload na teoria. Publicação
real fica pendente pra um ambiente sem essa limitação (Colab,
Codespaces, Linux comum), onde `nh3` já tem wheel pronta.

## Prática

### Estrutura do pacote de teste
modulo14-empacotamento-distribuicao/

├── pyproject.toml

├── README.md

└── meupacote/

└── init.py


`pyproject.toml`:
```toml
[build-system]
requires = ["setuptools>=64"]
build-backend = "setuptools.build_meta"

[project]
name = "meupacote-joao-teste"
version = "0.1.0"
description = "Pacote de teste do modulo 14"
requires-python = ">=3.9"
readme = "README.md"
Build

python -m build
Gera:



• dist/meupacote_joao_teste-0.1.0.tar.gz (sdist)

• dist/meupacote_joao_teste-0.1.0-py3-none-any.whl (wheel)



Mesmo passando por uma pasta intermediária de build específica de

plataforma (build/bdist.android-24-arm64_v8a), a wheel final ficou

py3-none-any — universal, porque o código não tem extensão nativa.



Conteúdo da wheel (extraída com unzip)

meupacote/__init__.py
meupacote_joao_teste-0.1.0.dist-info/
├── METADATA # Name, Version, Summary, Requires-Python
├── WHEEL # Generator, Root-Is-Purelib, Tag
├── RECORD # hash SHA256 + tamanho de cada arquivo
└── top_level.txt # módulos importáveis
Sem entry_points.txt porque não há [project.scripts] definido.



Publicação (fluxo teórico, não executado neste ambiente)

twine check dist/*
twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ meupacote-joao-teste
Autenticação via API token (__token__ + pypi-...), configurável

em ~/.pypirc. PyPI não aceita mais login por senha desde abr/2024.



Conclusão



Módulo cobriu o fluxo completo de empacotamento na prática (build)

e o fluxo de publicação na teoria, documentando uma limitação real

de ambiente (Termux/Rust) como parte do aprendizado, não como

bloqueio.


