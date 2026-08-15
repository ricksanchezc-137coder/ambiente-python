## Módulo 12 — Entry points e scripts ([project.scripts])

### Teoria
- `[project.scripts]` (PEP 621) mapeia um comando de terminal para uma função Python: `comando = "pacote.modulo:funcao"`.
- Ao instalar o pacote (`pip install -e .` ou build normal), o pip gera um executável em `<venv>/bin/<comando>`.
- O executável é um script Python gerado automaticamente: shebang apontando pro Python do venv, import direto da função, e `sys.exit(funcao())`.
- Existe também `[project.gui-scripts]` (sem console, usado em apps GUI no Windows) e `[project.entry-points.<grupo>]` genérico, mecanismo usado por sistemas de plugin (ex: pytest descobre plugins de terceiros assim).
- Substitui o antigo `entry_points={"console_scripts": [...]}` do `setup.py` — mesma mecânica por baixo, agora declarativa em TOML.
- A função referenciada precisa ser chamável sem argumentos obrigatórios: o wrapper sempre chama `funcao()` sem parâmetros. CLIs reais contornam isso lendo argumentos de dentro da função, via `sys.argv`, `argparse` ou `click`.

### Prática
- Criado `meupacote/` com `__init__.py` e `cli.py` (`def main(): print("rodando!")`).
- `pyproject.toml` com `[build-system]` (setuptools>=64), `[project]` (name, version) e `[project.scripts]` (`meucomando = "meupacote.cli:main"`).
- `.venv` criado e `pip install -e .` executado — gerou wheel editável e instalou o pacote.
- `meucomando` executado com sucesso, imprimindo `rodando!`.
- Inspecionado `.venv/bin/meucomando`: confirmado shebang + import + `sys.exit(main())`, além de uma linha de compatibilidade com Windows (`sys.argv[0].removesuffix('.exe')`), gerada mesmo em ambiente Linux/Termux.
- Testado cenário de erro: alterada `main()` para exigir argumento `nome` — rodar `meucomando` gerou `TypeError: main() missing 1 required positional argument: 'nome'`, confirmando que o wrapper chama a função sem argumentos.
- Revertido `cli.py` ao estado original; `meucomando` voltou a funcionar normalmente.
