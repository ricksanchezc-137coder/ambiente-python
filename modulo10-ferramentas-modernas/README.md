# Módulo 10 — Ferramentas modernas: visão comparativa (Poetry, PDM, Hatch, uv)

## Objetivo

Entender o cenário atual de gerenciadores de projeto Python que vão além do
pip básico — o que cada um resolve, como se diferenciam entre si, e por que
o ecossistema convergiu pra PEP 621 como padrão comum de metadados.

Este módulo é só teórico. A prática com uv fica reservada pro Módulo 16.

## Contexto: por que essas ferramentas existem

Historicamente, montar um projeto Python exigia várias ferramentas
separadas, cada uma resolvendo um pedaço do problema: pip pra instalar,
virtualenv pra isolar, pip-tools pra gerar lockfile, pyenv pra trocar de
versão do Python, pipx pra rodar CLI tools sem poluir o ambiente global.
Poetry, PDM, Hatch e uv nasceram pra consolidar esse conjunto de tarefas
numa interface só.

## Poetry

- Foi pioneiro entre os gerenciadores "tudo em um": dependências, venv,
build e publish num único fluxo (`poetry install`, `poetry add`,
`poetry publish`).
- Escrito em Python. O resolver de dependências é metódico, mas pode ficar
perceptivelmente lento em árvores grandes ou com muitos conflitos de
versão.
- Originalmente usava formato de metadados próprio, sob `[tool.poetry]`
no pyproject.toml — não o padrão da comunidade. A versão 2.0 (jan/2025)
passou a suportar PEP 621, mas boa parte dos projetos antigos ainda usa
o formato pré-padrão. Um projeto `[tool.poetry.dependencies]` precisa de
conversão manual antes de outra ferramenta (Hatch, PDM, uv) conseguir ler.
- Lockfile próprio: `poetry.lock`.
- Continua forte em bibliotecas publicadas no PyPI, pelo fluxo de publish
maduro, e em bases de código já estabelecidas em Poetry.

## PDM

- Fica no meio-termo entre Poetry e uv: segue os padrões de perto (PEP 621
nativo desde o início) e tem lockfile próprio.
- Pode usar o uv como resolver/instalador por baixo dos panos, herdando
parte da velocidade sem abrir mão da interface PDM.
- Suporta grupos múltiplos de dependências (como o Poetry) e instalação
automática de versão do Python (como o uv).
- Suporta PEP 582 (diretório `__pypackages__`, dependências dentro do
projeto sem venv) como recurso opcional — vale notar que essa PEP em si
foi rejeitada pelo Python Steering Council em 2023, então é um recurso
"órfão" do padrão oficial.
- Faz mais sentido pra quem já tem projeto em PDM e não tem motivo urgente
pra migrar.

## Hatch

- Foco em desenvolvimento de pacote, com abordagem diferente de ambiente:
permite nomear ambientes customizados (ex: um pra testes, outro pra
docs), cada um com suas próprias dependências e scripts, podendo usar um
como template pros outros.
- Nunca se desvia dos padrões PEP — é o mais "purista" do grupo nesse
sentido, e vive sob o guarda-chuva do PyPA (Python Packaging Authority).
- Bom pra quem quer a matriz de ambientes múltiplos pra testar contra
várias versões, ou já está no ecossistema PyPA.

## uv

- Escrito em Rust pela Astral (mesma equipe do Ruff). Comprado pela OpenAI
em março de 2026 para integração com o Codex — as ferramentas seguem
open-source e o ritmo de desenvolvimento não desacelerou até o momento.
- Escopo mais amplo do grupo: um binário só cobrindo pip, pip-tools,
virtualenv, pyenv e pipx — inclusive gerenciamento de versão do Python
(`uv python install`) e execução de CLI tool sem instalar globalmente
(`uvx`).
- Usa exclusivamente metadados PEP 621 e especificadores PEP 508. Qualquer
ferramenta compatível (Hatch, Flit, PDM) lê o pyproject.toml de um
projeto uv sem modificação nenhuma — ponto importante contra o
argumento de "lock-in": se o pyproject.toml já é PEP 621, trocar de
ferramenta no futuro não exige conversão.
- Lockfile próprio: `uv.lock` — não compatível com `poetry.lock` (não dá
simplesmente renomear um pro outro).
- Ambiente virtual sem abstração escondida: `uv venv` cria `.venv` no
projeto, sem cache oculto nem configuração adicional pra IDE detectar.
- Recurso exclusivo do grupo: suporte nativo a PEP 723, rodando um único
arquivo `.py` com dependências declaradas inline (`uv run script.py`),
sem projeto nem venv.
- Em benchmarks de 2026: instalação fria de um projeto com ~80
dependências leva ~8s no uv contra ~90s no pip, ~50s no Poetry e ~38s
no PDM. Em CI (GitHub Actions), resolver um lockfile levou 1,4s no uv
contra 22,3s no Poetry.
- Hoje é a escolha padrão pra projeto novo, principalmente em CI pesado e
monorepos.

## Resolução de dependências: cuidado ao trocar de ferramenta

Poetry e uv resolvem dependências de forma diferente entre si — um
projeto que funciona sob uv pode apresentar conflito no resolver do
Poetry (e vice-versa). Trocar de ferramenta num projeto existente exige
teste, não é troca automática.

## Tabela-resumo: quando escolher cada um

| Ferramenta | Escolha quando... |
|------------|---------------------------------------------------------------------------|
| Poetry | autor de biblioteca publicando no PyPI, ou base já estável em Poetry |
| PDM | já tem projeto PDM sem motivo urgente pra migrar |
| Hatch | quer matriz de ambientes nomeados, ou já está no ecossistema PyPA |
| uv | projeto novo, monorepo, CI pesado, ou quer um binário só pra tudo |

## Conclusão

O ecossistema convergiu pra PEP 621 como formato comum de metadados —
isso é o que faz a interoperabilidade entre ferramentas ser possível hoje.
uv se tornou o padrão de mercado em 2026 por velocidade e escopo, mas
Poetry, PDM e Hatch continuam viáveis dependendo do contexto do projeto
(legado, publish de biblioteca, ou preferência de fluxo de trabalho).

Esse levantamento teórico prepara o terreno pro Módulo 16, onde o uv será
aplicado na prática ao sistema-bancario.
