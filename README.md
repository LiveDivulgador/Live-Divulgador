# Live-Divulgador
Divulgador de Twitch streams de Ciência e Tecnologia, Artes e Artesanato e Criadores no Twitter

### Pré Requesitos
- Python3.x
- PostgreSQL

# Ficheiros e pastas
Neste repositório temos vários ficheiros e é importante entendermos o propóstio de cada um deles.
- **.env_example**: Este ficheiro deve ser renomenado para `.env`. Dentro dele terão vários nomes(variáveis) com um valor exemplo atribuído que deve ser alterado para o valor real.

-  **img**: Esta pasta serve para colocar as imagens personalizadas de cada streamer. Cada imagem deve estar no formato `.png` e o nome deve ser o ID do streamer.

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

## Banco de Dados
Banco de dados PostgreSQL
- Criar um banco com o nome `streamers`
- Insira as credenciais no arquivo `.env` nas variáveis `user_db` e `passwd_db`

Será, automaticamente, criada a tabela com as devidas colunas, porém será necessário adicionar manualmente, através do `psql`, os dados das pessoas a serem divulgadas.

**Nota**: Isso pode ser trabalhoso de fazer, já que é preciso saber o ID da Twitch de cada streamer. No entanto, já está planeado fazer-se uma interface para o utilizador fazer tudo isso graficamente e de forma simples.

### Importar e Exportar o banco
Se você já populacionou o seu banco, pode criar um ficheiro `.sql` com todos os dados. Para isso use o seguinte comando no seu terminal:

`pg_dump --host localhost --port 5432 --username <user_db> --format plain --verbose --file "seu_ficheiro.sql" --table public.livecoders streamers`

Posteriormente, pode exportar novamente, bastanto ter já criada a base de dados `streamers`:

sudo -u postgres psql streamers < seu_ficheiro.sql

# Colaboração
Se gostou do projeto e tem interesse em ajudar, pode sempre seguir as contas do bot no Twitter: [@LiveDivulgador](https://twitter.com/LiveDivulgador) e [@LiveDivulgador2](https://twitter.com/LiveDivulgador2)

Dessa forma estará a ajudar o projeto e os streamers divulgados por ele!

Também pode contribuir com código ou mesmo reportando falhas e dando palpites de novas funcionalidades.

Opiniões são sempre bem vindas!
