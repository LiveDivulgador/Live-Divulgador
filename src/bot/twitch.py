import requests
import os
from db import delete_streamer
import logging

# Configuração para criar logs deste ficheiro
log = logging.getLogger("twitch-log")
log.setLevel(logging.DEBUG)
fh = logging.FileHandler('twitch.log')
fh.setLevel(logging.DEBUG)
log.addHandler(fh)

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")


if client_id is None or client_id == '':
    raise ValueError('client_id não encontrado')

if client_secret is None or client_secret == '':
    raise ValueError('client_secret não encontrado')


def get_OAuth():

    """
    Obter credenciais de login para usar
    na API da Twitch
    """

    url = "https://id.twitch.tv/oauth2/token"
    param = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }

    r = requests.post(url, data=param)

    log.debug("[!] Func: get_OAuth - Status: %s" % r.status_code)

    if r.status_code == 400:
        raise ConnectionError(r.json())

    access_token = r.json()["access_token"]
    header = {
        "Client-ID": client_id,
        "Authorization": "Bearer " + access_token,
    }

    return access_token, header


def get_1_streamer_id(name):

    """
    Obter o id da pessoa através do seu
    nome na Twitch
    """

    _, header = get_OAuth()

    url = "https://api.twitch.tv/helix/users"
    param = {"login": name}

    r = requests.get(url, params=param, headers=header)
    log.debug(
        "[!] Func: get_1_streamer_id - Status: %s - Streamer: %s"
        % (r.status_code, name)
    )

    r = r.json()

    return str(r["data"][0]["id"])


def get_streamer_id(streamers, header):

    """
    Obter o id de todas as pessoas na
    base de dados, através do seu nome
    na Twitch
    """

    for streamer in streamers["Nome"]:
        url = "https://api.twitch.tv/helix/users"
        param = {"login": streamer}

        r = requests.get(url, params=param, headers=header)
        log.debug(
            "[!] Func: get_streamer_id - Status: %s - Streamer: %s"
            % (r.status_code, streamer)
        )

        r = r.json()

        # Encontrar o índice cujo nome == streamer
        index = streamers[streamers["Nome"] == streamer].index
        streamers.loc[index, "Id"] = r["data"][0]["id"]

    return streamers


def is_streamer_live(streamer_id, header):

    """
    Verifica se a pessoa está em live
    """

    url = "https://api.twitch.tv/helix/streams"
    param = {"user_id": streamer_id}

    r = requests.get(url, params=param, headers=header)
    log.debug(
        "[!] Func: is_streamer_live - Status: %s - Streamer: %s"
        % (r.status_code, streamer_id)
    )

    r = r.json()

    # Se sim retorna True e a categoria
    if r["data"]:
        return True, r["data"][0]["game_name"]

    # Se nao retorna False
    return False, None


def get_stream_title(streamer_id, header):

    """
    Retorna o título da live
    """

    url = "https://api.twitch.tv/helix/channels"
    param = {"broadcaster_id": streamer_id}

    r = requests.get(url, params=param, headers=header)
    log.debug(
        "[!] Func: get_stream_title - Status: %s - Streamer: %s"
        % (r.status_code, streamer_id)
    )

    r = r.json()

    return r["data"][0]["title"]


def name_changed(streamers, header):
    """
    NOTA: Precisa ser alterada para funcionar apenas com os dados
          da BD

    Função que verifica se o nome na base de dados está correto
    ou se precisa alterar
    """

    # Booleano que guarda o estado de modificação do dataframe
    streamers_modified = False

    for streamer in streamers["Id"]:

        # Obter o indice do streamer e o ID
        index = streamers[streamers["Id"] == streamer].index
        idt = streamers.loc[index, "Id"].values[0]

        # Obter nome do streamer utilizando o ID
        url = "https://api.twitch.tv/helix/channels"
        param = {"broadcaster_id": str(idt)}

        try:
            r = requests.get(url, params=param, headers=header).json()
        except:
            with open("log.txt", "a+") as f:
                f.write(f"#### Streamer: {idt} - Func: {get_stream_title}\n")

        # Obter nome real e o nome da DB do streamer
        streamer_name = str(r["data"][0]["broadcaster_name"]).lower()
        bd_name = str(streamers.loc[index, "Nome"].values[0]).lower()

        # Verificar se são iguais
        if streamer_name == bd_name:
            pass
        else:

            # Se não temos de atualizar na DB e no dataframe

            streamers_modified = True

            name = streamer_name
            twitch_link = "twitch.tv/" + name

            # Atualizar o CSV/DataFrame
            streamers.loc[index, "Nome"] = name
            streamers.loc[index, "Twitch"] = twitch_link

            # Apagar o velho valor da DB
            delete_streamer(idt)

    return streamers, streamers_modified


get_OAuth()
