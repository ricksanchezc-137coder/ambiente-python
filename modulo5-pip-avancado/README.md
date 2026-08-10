MÓDULO 5 — PIP AVANÇADO



1. EDITABLE INSTALL (-e)



Teoria

pip install -e <caminho> instala um pacote em modo “editável”: em vez de copiar os arquivos para site-packages/, o pip cria uma referência que aponta de volta pro código-fonte. Mudanças no código refletem imediatamente, sem reinstalar.



Desde pip 21.3 + setuptools>=64, editable installs seguem o PEP 660 (wheels editáveis). O mecanismo gera dois artefatos em site-packages/: um .pth (editable.<pacote>-<versão>.pth), processado automaticamente pelo Python no startup, e um finder customizado (editable_<pacote>_finder.py), que intercepta o import system e redireciona pro caminho absoluto do código-fonte.



Requer que o pyproject.toml declare um build backend compatível com build_editable (setuptools>=64, hatchling, poetry-core, etc).



Prática

Pacote de teste em pacote-teste/, com pacote-teste/pyproject.toml e pacote-teste/meupacote/ (contendo init.py e saudacao.py).



pyproject.toml:

[build-system]

requires = [“setuptools>=64”]

build-backend = “setuptools.build_meta”



[project]

name = “meupacote”

version = “0.1.0”



Comando de instalação:

pip install -e ./pacote-teste



Editou saudacao.py com o venv ativo, sem reinstalar — mudança refletiu na próxima execução. Artefatos confirmados em site-packages/: editable.meupacote-0.1.0.pth e __editable___meupacote_0_1_0_finder.py, este último contendo o caminho absoluto até pacote-teste/meupacote/.



2. EXTRAS



Teoria

Grupos de dependências opcionais declarados no pyproject.toml, em [project.optional-dependencies]. Sintaxe de instalação: pip install pacote[extra1,extra2]. No metadata (Requires-Dist), cada dependência de extra vem marcada com ; extra == “nome” — só vira obrigatória se o extra for pedido.



Prática

pip install “requests[socks]”

pip show requests    (Requires: inalterado, 4 deps obrigatórias)

pip list              (PySocks aparece instalado a mais)

cat .venv/lib/python3.13/site-packages/requests-*.dist-info/METADATA | grep -i “Requires-Dist”



Confirmado: requests declara dois extras — socks e use-chardet-on-py3.



3. CONSTRAINTS (-c)



Teoria

Mesma sintaxe de um requirements.txt, mas não instala nada sozinho — só limita a versão de um pacote SE ele for instalado por outro motivo (pedido direto ou dependência transitiva). Serve pra travar versões indiretas sem listar tudo manualmente.



Prática

echo “urllib3==2.0.0” > constraints.txt

pip install -c constraints.txt urllib3      (direto)

pip uninstall urllib3 -y

pip install -c constraints.txt requests     (indireto — não pede urllib3, mas respeita o teto)

pip show urllib3   (Version: 2.0.0, Required-by: requests)



Observação: urllib3==2.0.0 está yanked no PyPI (PEP 592, bug de streaming). O pip evita yanked na resolução automática, mas honra um pin exato (==) mesmo assim, só avisando.



4. –NO-DEPS



Teoria

Instala só o pacote pedido, sem resolver dependências declaradas.



Prática

pip install –no-deps requests

pip show requests   (Requires ainda lista as 4 deps, do metadata declarado)

pip list             (só requests instalado de fato)

python -c “import requests; requests.get(‘https://example.com’)”

ModuleNotFoundError: No module named ‘urllib3’



Confirma: declarado no metadata é diferente de presente no ambiente.



5. HASH CHECKING (–require-hashes)



Teoria

Camada de segurança de supply-chain. requirements.txt pode incluir hash SHA-256 esperado por pacote (requests==2.34.2 –hash=sha256:<hash>). –require-hashes recusa qualquer arquivo cujo hash não bata.



IMPORTANTE: –require-hashes exige hash + pin == em TODAS as dependências, diretas e transitivas. Não implica –no-deps automaticamente — sem cobrir as transitivas, falha com erro dizendo que as versões precisam estar pinadas com =. Pra testar hash checking isolado, é preciso combinar –require-hashes –no-deps.



Prática

mkdir -p ~/pkgs-tmp   (/tmp é read-only no Termux)

pip download requests –no-deps -d ~/pkgs-tmp

pip hash ~/pkgs-tmp/requests-2.34.2-py3-none-any.whl

resultado: –hash=sha256:2a0d60c172f83ac6ab31e4554906c0f3b3588d37b5cb939b1c061f4907e278e0



echo “requests==2.34.2 –hash=sha256:2a0d60c172f83ac6ab31e4554906c0f3b3588d37b5cb939b1c061f4907e278e0” > requirements-hash.txt



pip install –require-hashes -r requirements-hash.txt

ERRO: charset_normalizer (transitiva) sem pin/hash



pip install –require-hashes –no-deps -r requirements-hash.txt

Successfully installed requests-2.34.2



Teste de adulteração — trocado um caractere no hash do arquivo, reinstalado:

ERROR: THESE PACKAGES DO NOT MATCH THE HASHES FROM THE REQUIREMENTS FILE

Expected sha256 2a0d60c272f83ac6ab31e4554906c0f3b3588d37b5cb939b1c061f4907e278e0

Got 2a0d60c172f83ac6ab31e4554906c0f3b3588d37b5cb939b1c061f4907e278e0



NOTAS DE AMBIENTE (TERMUX)

/tmp é somente leitura; usar pasta dentro de $HOME.

which não disponível por padrão; command -v <programa> é a alternativa.

