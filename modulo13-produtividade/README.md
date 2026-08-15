
## Módulo 13 — Produtividade (pipx, .env, variáveis de ambiente)

### Teoria
- **pipx** instala aplicações CLI Python cada uma no seu próprio venv isolado, mas expõe o comando globalmente no PATH — resolve o problema de instalar ferramentas (black, httpie, poetry) sem poluir o Python do sistema nem misturar com dependências de projetos.
- Diferente de `pip install --user`, que joga tudo num único ambiente global compartilhado, o pipx cria um venv por aplicação em `~/.local/share/pipx/venvs/`.
- **Variáveis de ambiente** são o mecanismo do sistema operacional pra passar configuração a processos filhos. Em Python, acessadas via `os.environ` ou `os.getenv()` — que retorna `None` (sem erro) se a variável não existir.
- **.env** é um arquivo de texto com pares `CHAVE=valor`. Python não lê `.env` nativamente — precisa da lib `python-dotenv`, cuja função `load_dotenv()` lê o arquivo e popula `os.environ` manualmente.
- `os.getenv()` sempre retorna `str` ou `None`, nunca outro tipo — valores como `"true"` precisam de conversão manual pra virar bool de verdade.
- `.env` nunca deve ser commitado quando contém segredos reais — entra no `.gitignore`.

### Prática
- Instalado pipx via `pip install --user pipx` + `python -m pipx ensurepath`; confirmado `pipx --version` (1.16.7) após reabrir a sessão do Termux.
- Instalado `httpie` com `pipx install httpie`; comando `http --version` funcionou globalmente sem nenhum venv ativo.
- Confirmado isolamento: `pipx list` mostrou o venv próprio do httpie; `pip show requests` (fora de venv) retornou "not found", provando que a dependência do httpie não vazou pro ambiente global.
- Testado mecanismo cru de variáveis de ambiente: `export MINHA_VAR=...` seguido de `os.getenv()` num subprocesso Python confirmou herança da variável; `os.getenv()` numa variável inexistente retornou `None`.
- Criado `.venv` dedicado ao módulo, instalado `python-dotenv`, criado `.env` com `API_KEY` e `DEBUG`.
- Script de teste confirmou: `os.getenv("API_KEY")` retorna `None` antes de `load_dotenv()`, e o valor do `.env` depois — e `DEBUG` chega como string `"true"`, não bool.
- `.env` adicionado ao `.gitignore` da raiz do repo, ao lado de `.venv/`.
