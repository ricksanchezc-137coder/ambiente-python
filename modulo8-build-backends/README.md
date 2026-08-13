Módulo 8 — Build backends (setuptools, hatchling, poetry-core)



Teoria



A tabela [build-system] do pyproject.toml tem dois campos: requires (dependências necessárias pra fazer o build) e build-backend (qual ferramenta implementa os hooks do PEP 517 — build_wheel, build_sdist etc., chamados por frontends como pip ou python -m build).



Os três backends explorados:



• setuptools (setuptools.build_meta) — o mais antigo e maduro. Suporta tanto o [project] moderno (PEP 621) quanto o formato legado (setup.py/setup.cfg). Mais flexível pra casos complexos (extensões em C, build customizado).

• hatchling (hatchling.build) — backend do projeto Hatch. Configuração enxuta, pensado pra pacotes Python puros, com detecção automática do pacote pelo nome.

• poetry-core (poetry.core.masonry.api) — extraído do Poetry pra ser só o backend (sem o gerenciador de dependências/lockfile junto). Historicamente exigia a tabela [tool.poetry] em vez do [project] padrão, mas desde a versão 2.0 do Poetry (lançada em janeiro de 2025) já suporta [project] (PEP 621) também, mantendo [tool.poetry] como alternativa/complemento.



Prática



Criadas 4 subpastas dentro de modulo8-build-backends, todas com o mesmo pacote mínimo (meupacote/__init__.py com a função saudacao(nome)), variando só o pyproject.toml:



1) pacote-setuptools — [build-system] com setuptools>=64, [project] completo (name, version, description, requires-python). python -m build gerou sdist e wheel com sucesso. Log verboso, mostrando os passos internos de egg_info e build/lib, build/bdist.*. O wheel final ficou com 5 arquivos (incluindo top_level.txt), com timestamps reais do momento do build.



2) pacote-hatchling — só trocado o [build-system] pra hatchling. Build funcionou de primeira, log bem mais enxuto (sem os passos de egg_info visíveis). Wheel com 4 arquivos (sem top_level.txt) e — achado interessante — todos os timestamps fixos em 2020-02-02 00:00, não a hora real do build.



3) pacote-poetry-core (formato [project]) — primeira tentativa deu erro: digitei poetry-core-masonry.api (traço) em vez de poetry.core.masonry.api (ponto) no build-backend, resultando em BackendUnavailable: Cannot import 'poetry-core-masonry.api'. Corrigido e o build funcionou. Wheel também com 4 arquivos, mas timestamps fixos em 2016-01-01 00:00 (data diferente da do hatchling — cada backend tem seu próprio valor padrão pra build reprodutível). Inspecionando o METADATA, apareceram 6 linhas Classifier: Programming Language :: Python :: X.Y (3.9 até 3.14) geradas automaticamente a partir do requires-python = ">=3.9" — nem setuptools nem hatchling fazem isso por padrão.



4) pacote-poetry-classico (formato [tool.poetry]) — mesmo backend poetry-core, mas com a tabela clássica: name, version, description, authors = ["João <joao@example.com>"] dentro de [tool.poetry], e python = ">=3.9" dentro de [tool.poetry.dependencies] (em vez de um requires-python solto). Build funcionou sem erro. Diferença no METADATA em relação à versão [project]: agora aparecem as linhas Author: joao e Author-email: joao@example.com — porque na versão [project] anterior nenhum autor tinha sido declarado. Os mesmos 6 classifiers automáticos de versão do Python voltaram a aparecer.



Comparação final



Backend Formato de metadados Arquivos no wheel Timestamp Particularidade

setuptools [project] (ou legado) 5 (com top_level.txt) real (hora do build) log verboso com egg_info/build/bdist

hatchling [project] 4 fixo — 2020-02-02 log enxuto, detecção automática do pacote

poetry-core [project] ou [tool.poetry] 4 fixo — 2016-01-01 gera Classifier de versão Python automaticamente a partir do requires-python/python



Conceito-chave que perpassa os 3: hatchling e poetry-core fixam timestamps de propósito — é a prática de build reprodutível (mesmo código-fonte → wheel byte-a-byte idêntico em qualquer build, útil pra verificação de integridade/supply chain). O setuptools, por padrão, não segue essa prática e usa o horário real.

