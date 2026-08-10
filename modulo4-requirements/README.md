Módulo 4 — requirements.txt



Gerar



pip freeze > requirements.txt — captura tudo que está instalado no ambiente ativo, no formato pacote==versão.



Instalar



pip install -r requirements.txt — reinstala cada pacote na versão especificada. Testado do zero (venv limpo): reproduziu exatamente o mesmo ambiente, byte a byte na versão de cada pacote.



Comportamento importante: o pip não reinstala pacotes já satisfeitos. Se a versão instalada cai dentro da faixa pedida, ele pula (Requirement already satisfied). Só desinstala/reinstala quando a versão atual não satisfaz mais a exigência.



Pinning — as três formas



|Sintaxe |Significado |Uso típico |
|----------|-----------------------------------------------------------------|-----------------------------------------|
|`==2.34.2`|Versão exata |Aplicações finais (previsibilidade) |
|`>=2.34.2`|Mínima, sem teto |Raramente usado sozinho — risco de quebra|
|`~=2.34.2`|Compatível (`>=2.34.2, <2.35.0`) ou `~=3.1.0` → `>=3.1.0, <3.2.0`|Meio-termo comum em apps |


Wheels específicos de plataforma



Nem todo pacote é py3-none-any (Python puro). O markupsafe baixou um wheel cp313-cp313-android_24_arm64_v8a por ter extensão em C — compilado pra essa versão exata de Python e arquitetura. Isso é por que um requirements.txt pode instalar sem problema numa máquina e falhar (ou compilar do zero) em outra com plataforma diferente.



Dependências mudam entre versões



Ao trocar Flask de 3.1.3 pra 3.0.3, o Requires do pip show mudou (MarkupSafe saiu da lista direta). Dependências declaradas não são fixas do pacote — mudam conforme a versão.


