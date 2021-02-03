# Live-Divulgador
Divulgador de Twitch streams de Ciência e Tecnologia, Artes e Artesanato e Criadores no Twitter

# Ficheiros e pastas
Neste repositório temos vários ficheiros e é importante entendermos o propóstio de cada um deles.
- **.env_example**: Este ficheiro deve ser renomenado para `.env`. Dentro dele terão vários nomes(variáveis) com um valor exemplo atribuído que deve ser alterado para o valor real.

-  **img**: Esta pasta serve para colocar as imagens personalizadas de cada streamer. Cada imagem deve estar no formato `.png` e o nome deve ser o ID do streamer.

- **streamers.csv**: Neste ficheiro devem ser preenchidas todas as colunas ***exceto*** a coluna `Id`. Apesar de o nome das mesmas ser bastante sugestivo irei explicar:
	- **Nome**: Nome do streamer
	
	- **Twitch**: URL da Twitch do streamer no seguinte formato: `twitch.tv/nome_do_streamer`
	
	- **Twitter**: Nome de utilizador (A.K.A @) do Twitter do streamer (caso não tenha, deixar em branco)
	
	- **OnStream**: Booleano (TRUE, FALSE) que indica se o streamer está em live ou não (por padrão deixar FALSE)
	
	- **Print**: Booleano (TRUE, FALSE) que confirma se o streamer aceitou ou não o print do bot
	
	- **Tipo**: Categoria das streams: `code` ou `art` (art abrange não só arte, mas também artesanato e criadores)

	- **Hashtags**: Hashtags que serão mostradas no tweet

- **main.py**: Ficheiro de código com a lógica principal do bot

- **tt.py**: Ficheiro de código com as funções referentes a funcionalidades do Twitter (como tweetar por exemplo)

- **twitch.py**: Ficheiro de código com funções referentes a funcionalidades da Twitch (como obter as credenciais da API)

- **utils.py**: Ficheiro de código com funções gerais (criar um DataFrame a partir de um .csv)
- **requirements.txt**: Ficheiro com os pacotes necessários de Python para o bot funcionar


# Utilização
Como já referido acima é importante criar o ficheiro `.env` com todas as credenciais corretas.
No caso de estar num ambiente de desenvolvimento, pode ser interessante criar um python env (correr o comando abaixo dentro do diretório raiz do projeto):
`python -m venv env`

Isto criará um diretório `env` onde ficarão todos os pacotes instalados via `pip`. Agora só falta instalar os pacotes:
`python -m pip install -r requirements.txt`

No fim de tudo isto bastará iniciar o bot com:
`python main.py`

# Colaboração
Se gostou do projeto e tem interesse em ajudar, pode sempre seguir as contas do bot no Twitter: [@LiveDivulgador](https://twitter.com/LiveDivulgador) e [@LiveDivulgador2](https://twitter.com/LiveDivulgador2)

Dessa forma estará a ajudar o projeto e os streamers divulgados por ele!

Também pode contribuir com código ou mesmo reportando falhas e dando palpites de novas funcionalidades.

Opiniões são sempre bem vindas!
