# Módulo 9 — Metadados do projeto no pyproject.toml

## Teoria

A seção `[project]` do `pyproject.toml` (definida na PEP 621) concentra os
metadados que descrevem um pacote Python — nome, versão, dependências,
autores, etc. É o formato moderno que substitui o `setup.py`/`setup.cfg`
do setuptools clássico.

Campos usados neste módulo:

- `name`, `version`, `description`, `requires-python` — já vistos no
Módulo 7.
- `dependencies` — lista de pacotes **obrigatórios**. Equivale ao
`requirements.txt`, mas embutido no próprio pyproject.toml. Todo pacote
listado aqui é instalado sempre que o projeto é instalado.
- `[project.optional-dependencies]` — grupos **nomeados** de dependências
extras. Cada grupo só é instalado se for pedido explicitamente com a
sintaxe `pacote[grupo]`. Serve para separar dependências de dev, teste,
docs, etc. das dependências que o usuário final realmente precisa em
produção.

Por baixo dos panos, o pip traduz isso para o formato de metadata
(`Requires-Dist`) que fica dentro do `.dist-info` do pacote instalado:

- Uma dependência obrigatória vira `Requires-Dist: pacote` (sem condição).
- Um grupo opcional gera um `Provides-Extra: nome-do-grupo` e cada
dependência dele vira `Requires-Dist: pacote; extra == "nome-do-grupo"`.

Ou seja, `optional-dependencies` não é um mecanismo separado — é a mesma
lista de `Requires-Dist` de sempre, só que com uma condição (`extra == ...`)
anexada, resolvida pelo pip no momento da instalação.

## Prática

Criado pacote mínimo `meupacote` com `pyproject.toml` contendo:

```toml
[project]
dependencies = ["requests"]

[project.optional-dependencies]
dev = ["pytest"]
Testes feitos:



1. pip install -e . (sem extras) — instalou requests e as dependências

dele (certifi, charset-normalizer, idna, urllib3). pytest

não apareceu em pip list.

2. pip install -e ".[dev]" — reinstalou o meupacote (pip refaz o

editable install porque a metadata mudou) e desta vez pytest entrou

junto, trazendo suas próprias dependências (iniconfig, packaging,

pluggy, pygments).

3. Inspecionado o METADATA gerado em

.venv/lib/python3.13/site-packages/meupacote-0.1.0.dist-info/METADATA,

confirmando na prática:

• Requires-Dist: requests (obrigatória, sem condição)

• Provides-Extra: dev

• Requires-Dist: pytest; extra == "dev" (condicional ao extra)



Confirma que optional-dependencies é resolvido inteiramente via metadata

condicional — não existe um sistema paralelo de “dependências extras”,

é a mesma mecânica de Requires-Dist com uma marcação a mais.



