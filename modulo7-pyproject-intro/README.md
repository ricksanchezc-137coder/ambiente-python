# Módulo 7 — pyproject.toml — introdução (PEP 518/517/621)

## Teoria

- **PEP 518** — criou o `pyproject.toml` e a seção `[build-system]`, com `requires` (dependências de build) e `build-backend` (ferramenta que constrói o pacote). Resolveu o problema de ovo-e-galinha do `setup.py`: antes, não havia lugar padronizado pra declarar as dependências necessárias *antes* de executar o script de build.
- **PEP 517** — define a interface padronizada que todo build backend implementa (`build_wheel`, `build_sdist`, `get_requires_for_build_wheel`, etc.), permitindo que o pip funcione com qualquer backend (setuptools, hatchling, poetry-core...) sem precisar saber dos detalhes internos de cada um.
- **PEP 621** — padronizou a seção `[project]`, onde ficam os metadados do próprio pacote (nome, versão, descrição, dependências, requires-python), em vez de espalhados em `setup.py`/`setup.cfg`.

Resumo da divisão: `[build-system]` diz *como construir*; `[project]` diz *o que é* o pacote; o build backend implementa a interface do PEP 517 pra fazer a ponte entre os dois.

## Prática

1. Criado pacote mínimo (`meupacote/__init__.py`) com `pyproject.toml` contendo **só** `[build-system]` (setuptools), sem `[project]`.
2. `pip install -e .` funcionou mesmo assim — sem erro. O setuptools usou seu mecanismo de *package discovery* (flat-layout) pra achar `meupacote/` sozinho, e gerou metadados com valores-padrão: `Name: meupacote`, `Version: 0.0.0`, todos os outros campos (Summary, Author, License, Requires) vazios.
3. Confirmado via `pip show meupacote` e leitura direta do `METADATA` real em `.venv/.../meupacote-0.0.0.dist-info/METADATA` — `Metadata-Version: 2.4`, `Generator: setuptools (84.0.0)`.
4. **Achado bônus**: o editable install gerou `__editable__.meupacote-0.0.0.pth` + `__editable___meupacote_0_0_0_finder.py` — o mecanismo moderno de editable install (**PEP 660**), que usa um finder Python customizado pra interceptar o import e apontar pro código-fonte. Substitui o método antigo (`.egg-link` + symlink via `easy-install.pth`).
5. Adicionado `[project]` de verdade (`name`, `version = "0.1.0"`, `description`, `requires-python`) e reinstalado com `pip install -e . --force-reinstall --no-deps`. Comparação do METADATA antes/depois:

| Campo | Sem `[project]` | Com `[project]` |
|---|---|---|
| Version | 0.0.0 (fallback) | 0.1.0 (declarado) |
| Summary | vazio | "Pacote de teste do Modulo 7" |
| Requires-Python | ausente | >=3.9 |

**Módulo 7 (pyproject.toml — introdução) CONCLUÍDO.**
