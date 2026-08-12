# Módulo 6 — Índices e pacotes (PyPI, --index-url, wheels vs sdist)

## Teoria

### Índice de pacotes
Quando rodamos `pip install pacote`, o pip busca o pacote em um **índice** — por padrão, o PyPI (pypi.org). Um índice é um catálogo de pacotes com metadados e links de download. Empresas costumam manter índices privados (Artifactory, devpi, etc.) para pacotes internos.

### --index-url vs --extra-index-url
- `--index-url` **substitui** o índice padrão inteiro. O pip passa a olhar *só* pra esse índice.
- `--extra-index-url` **adiciona** um índice extra, mantendo os demais ativos.

Importante: quando múltiplos índices estão ativos, o pip **não** tenta o primário e só cai pro extra em caso de falha — ele agrega os candidatos de *todos* os índices informados e escolhe a versão mais alta entre eles.

Esse comportamento é a base de uma vulnerabilidade real de supply chain conhecida como **dependency confusion** (documentada desde 2021, por Alex Birsan, usada como PoC contra empresas como Apple, Microsoft e Tesla): se uma empresa usa `--extra-index-url` apontando pro PyPI público como complemento de um índice privado, um atacante pode publicar no PyPI público um pacote com o mesmo nome de um pacote interno, numa versão bem alta (ex: `99.0.0`). Como o pip escolhe a versão mais alta entre todos os índices, o pacote malicioso "vence" o pacote interno legítimo. A defesa recomendada é usar `--index-url` (não `--extra-index-url`) apontando só pro índice privado ao instalar pacotes internos, ou usar namespaces nos nomes desses pacotes.

### Wheels vs sdist
O PyPI hospeda, para um mesmo pacote, até dois formatos de distribuição:

| | sdist (`.tar.gz`) | wheel (`.whl`) |
|---|---|---|
| Conteúdo | Código-fonte completo + metadados de build (pyproject.toml, setup.py, tests, etc.) | Pacote pré-construído, pronto pra copiar no `site-packages` |
| Instalação | Precisa ser *construído* localmente (invoca o build backend) | Cópia direta, sem build |
| Velocidade | Mais lenta | Mais rápida |
| Preferência do pip | Só usado se não houver wheel compatível | Preferido por padrão |

Ao baixar um sdist, o pip precisa invocar o build backend pra descobrir os metadados (nome, versão, dependências) — por isso aparecem os passos `Installing build dependencies`, `Getting requirements to build wheel`, `Preparing metadata (pyproject.toml)`. Isso é o **PEP 517** em ação. O wheel já vem com `dist-info/METADATA` pronto, sem precisar de nenhum desses passos.

## Prática

1. Baixado wheel isolado do `requests` com `pip download --no-deps -d ./pacote requests` — trouxe só o `.whl`, confirmando a preferência padrão do pip por wheels.
2. Forçado o download do sdist com `pip download --no-deps --no-binary :all: -d ./pacote-sdist requests` — trouxe o `.tar.gz`, com os passos de build (PEP 517) visíveis no log.
3. Extraídos os dois (`unzip` no wheel, `tar -xzf` no sdist) e comparado o conteúdo:
- wheel: só o pacote `requests/` pronto + `dist-info/` (METADATA, RECORD, WHEEL, top_level.txt)
- sdist: árvore completa do projeto (`src/`, `tests/`, `pyproject.toml`, `setup.py`, `setup.cfg`, `README.md`, `HISTORY.md`, `PKG-INFO`, `requirements-dev.txt`)
4. Testado `--index-url https://test.pypi.org/simple/` sozinho — instalou `requests-2.5.4.1`, uma versão de teste que não existe no PyPI oficial, confirmando que o TestPyPI é um índice totalmente separado, não um mirror.
5. Testado `--index-url` (TestPyPI) + `--extra-index-url` (PyPI oficial) juntos — instalou `requests-2.34.2` (a versão mais alta agregando os dois índices), demonstrando na prática o mecanismo por trás do dependency confusion.

**Módulo 6 (Índices e pacotes) CONCLUÍDO.**
