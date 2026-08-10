Módulo 3 — pip básico



O que é o pip



Gerenciador de pacotes padrão do Python. Baixa, instala e remove bibliotecas do PyPI, resolvendo dependências automaticamente. Dentro de um venv ativo, ele opera isolado do Python do sistema — cada venv tem seu próprio pip e seu próprio site-packages.



Comandos praticados



pip install <pacote>

Resolve a árvore de dependências, baixa os wheels (usando cache local quando já baixados antes) e instala na ordem certa — dependências primeiro, pacote principal por último.



pip list

Lista os pacotes instalados no ambiente ativo, em formato de tabela (nome + versão).



pip freeze

Lista no formato pacote==versão, uma linha por pacote. É esse formato que alimenta o requirements.txt (pip freeze > requirements.txt — módulo 4).



pip show <pacote>

Mostra metadados de um pacote específico: versão, local de instalação (Location), dependências dele (Requires) e quem depende dele (Required-by).



pip uninstall <pacote>

Remove um pacote e seus arquivos, pedindo confirmação (Proceed (Y/n)?) antes de apagar.



Observação importante: dependência declarada ≠ dependência obrigatória em runtime



Desinstalei o charset_normalizer (uma dependência declarada do requests, listada em Requires) e o requests continuou funcionando — só emitiu um aviso (RequestsDependencyWarning), sem quebrar. Isso acontece porque o código do requests trata essa dependência como opcional internamente (try/except na importação), usando-a pra detecção de encoding mas sem travar se ela não existir.



Conclusão: o Requires do pip show reflete o que foi declarado na hora do empacotamento (o que o instalador vai buscar), não necessariamente o que é obrigatório pra cada linha de código rodar. A obrigatoriedade real depende de como a biblioteca foi programada.



Cache do pip



As mensagens Using cached ...whl mostram que o pip mantém um cache local de pacotes já baixados — reinstalações não precisam buscar da internet de novo.

