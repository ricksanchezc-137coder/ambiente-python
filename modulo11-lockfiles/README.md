# Módulo 11 — Lockfiles e reprodutibilidade

## Teoria

Um `requirements.txt` gerado por `pip freeze` (módulo 4) pina versões, mas
mistura dependências diretas e transitivas numa lista plana, sem hashes
por padrão. Um lockfile de verdade resolve isso registrando:
- a árvore de dependências (quem depende de quem)
- hashes de integridade de cada artefato
- separação entre "o que eu pedi" (arquivo de input) e "o que foi resolvido"

## pip-tools

- `requirements.in` → dependências diretas, sem versão fixa
- `pip-compile requirements.in` → resolve e gera `requirements.txt` com
pinning completo + comentários `# via <origem>` mostrando a árvore
- `pip-compile --generate-hashes` → adiciona hash de cada wheel/sdist;
pacotes com extensão em C (ex: markupsafe) geram dezenas de hashes,
um por plataforma/versão de Python
- `pip-sync requirements.txt` → sincroniza o venv para bater exatamente
com o lockfile, **removendo** o que não está listado (diferente de
`pip install -r`, que só adiciona/atualiza)

## poetry.lock

- Gerado automaticamente a partir do `pyproject.toml`
- Formato TOML estruturado: cada pacote é um bloco `[[package]]` com
`name`, `version`, `groups` (main/dev/etc.), `files` (hashes)
- Seção `[metadata]` no final guarda um `content-hash` calculado sobre
as dependências declaradas no `pyproject.toml`
- `poetry check` compara esse hash com o `pyproject.toml` atual; se
divergir (ex: dependência nova adicionada sem re-lockar), recusa
seguir até rodar `poetry lock` de novo

## Conclusão

Os dois mecanismos resolvem o mesmo problema — reprodutibilidade exata
via árvore + hashes — mas o Poetry integra isso ao ciclo de vida do
projeto (pyproject.toml → lock → check), enquanto pip-tools é uma
camada mais fina, focada só em compilar/sincronizar requirements.
