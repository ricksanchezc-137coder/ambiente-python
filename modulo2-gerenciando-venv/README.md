# Módulo 2 — Criando e Gerenciando venv

## Teoria

### O script de ativação
`activate` não é mágica — é um script shell comum. Quando ativado (`source .venv/bin/activate`), ele:
- Guarda os valores antigos de `PATH`, `PYTHONHOME` e `PS1` em variáveis `_OLD_VIRTUAL_*`, pra poder restaurar depois
- Define `VIRTUAL_ENV` com o caminho absoluto do venv
- Coloca `$VIRTUAL_ENV/bin` na **frente** do `PATH` (não remove nada, só muda a ordem de busca)
- Define `VIRTUAL_ENV_PROMPT` (é isso que gera o `(.venv)` no prompt)
- Dá `unset` em `PYTHONHOME` se estiver setada, pra não confundir o Python sobre onde buscar a stdlib

O `deactivate` faz o processo inverso: restaura tudo a partir das variáveis `_OLD_VIRTUAL_*` e dá `unset` nelas.

### Symlink vs cópia real
No Linux/Termux, `.venv/bin/python` é um **link simbólico** apontando pro Python do sistema (ex: `/data/data/com.termux/files/usr/bin/python`), não uma cópia real do interpretador. Implicação: como o link usa caminho absoluto, mover a pasta `.venv` não quebra ela sozinha — mas desinstalar ou trocar o Python do sistema quebra o venv na hora, já que ele não carrega interpretador próprio.

### Flags úteis
- `--system-site-packages`: dá acesso aos pacotes globais do sistema além dos instalados no próprio venv (quebra o isolamento total; o `sys.path` passa a incluir os dois site-packages)
- `--without-pip`: cria o venv sem instalar `pip`/`pip3` dentro dele

### .gitignore — dois mecanismos coexistindo
- **Manual, na raiz do repo:** regra `.venv/` no `.gitignore` da raiz — cobre qualquer pasta chamada exatamente `.venv`, em qualquer subpasta do repositório
- **Automático, do próprio venv:** a partir do **Python 3.13**, o módulo `venv` passa a criar um `.gitignore` com conteúdo `*` **dentro de cada venv criado**, não importa o nome da pasta (`.venv-sistema`, `.venv-sempip`, etc.)

Isso significa que, no Python 3.13+, a regra manual da raiz é redundante pra venvs novos — mas continua útil como rede de segurança pra quem clonar o repo usando uma versão mais antiga do Python, que não gera esse `.gitignore` automático.

## Prática
1. Criado `.venv` na subpasta do módulo; inspecionado `.venv/bin/activate` linha por linha (função `deactivate()` primeiro, depois a lógica de ativação)
2. Confirmado via `ls -la .venv/bin/python*` que `python`, `python3` e `python3.13` são symlinks, não cópias
3. Configurado `.gitignore` na raiz do repo com a regra `.venv/`
4. Criados `.venv-sistema` (com `--system-site-packages`) e `.venv-sempip` (com `--without-pip`) pra testar as flags
5. Confirmado: `.venv-sempip/bin` não tem nenhum `pip`; `sys.path` do `.venv-sistema` inclui o site-packages do venv **e** o do sistema
6. Investigado por que `.venv-sistema`/`.venv-sempip` apareciam como ignorados mesmo sem bater com a regra `.venv/` da raiz — descoberto, via `git status --ignored=matching`, que cada um tinha seu próprio `.gitignore` interno (conteúdo `*`), gerado automaticamente pelo `venv` desde o Python 3.13

## Observações
- `find` no Termux não suporta `-maxdepth` do jeito GNU tradicional (deu erro `unknown predicate`) — usado `-maxdepth` depois de reordenar os argumentos corretamente (`find . -maxdepth 1 ...`)
- `git status --ignored=matching` é melhor que `--ignored` puro pra depurar regras de ignore, porque lista arquivo por arquivo em vez de colapsar pastas ignoradas num único `./`
