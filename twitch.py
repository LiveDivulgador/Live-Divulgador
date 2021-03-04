import requests
import os
from db import deleteStreamer

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

if client_id is None or client_id == '':
    raise ValueError('client_id não encontrado')

if client_secret is None or client_secret == '':
    raise ValueError('client_secret não encontrado')


def getOAuth():
    # Obter Oauth Token
    url = "https://id.twitch.tv/oauth2/token"
    param = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }

    r = requests.post(url, data=param)

    access_token = r.json()["access_token"]
    header = {"Client-ID": client_id, "Authorization": "Bearer " + access_token}

    return access_token, header


def get1StreamerId(name):
    # Obter o ID de um streamer
    _, header = getOAuth()

    url = "https://api.twitch.tv/helix/users"
    param = {"login": name}

    r = requests.get(url, params=param, headers=header).json()

    return str(r["data"][0]["id"])


def getStreamerId(streamers, header):
    # Obter o id de cada streamer
    for streamer in streamers["Nome"]:
        url = "https://api.twitch.tv/helix/users"
        param = {"login": streamer}

        r = requests.get(url, params=param, headers=header).json()

        # Encontrar o índice cujo nome == streamer
        index = streamers[streamers["Nome"] == streamer].index
        streamers.loc[index, "Id"] = r["data"][0]["id"]

    return streamers


def isStreamerLive(streamer_id, header):
    # Verificar se o streamer está em live
    url = "https://api.twitch.tv/helix/streams"
    param = {"user_id": streamer_id}

    r = requests.get(url, params=param, headers=header).json()

    # Se sim retorna True
    if r["data"]:
        return True

    # Se nao retorna False
    return False


def getStreamTitle(streamer_id, header):
    url = "https://api.twitch.tv/helix/channels"
    param = {"broadcaster_id": streamer_id}

    r = requests.get(url, params=param, headers=header).json()

    return r["data"][0]["title"]


def nameChanged(streamers, header):
    """ Função que verifica se o nome na base de dados está correto
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
        r = requests.get(url, params=param, headers=header).json()

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
            deleteStreamer(idt)

    return streamers, streamers_modified
