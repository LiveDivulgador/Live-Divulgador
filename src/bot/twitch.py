import os

import requests

from .db import delete_streamer

# Credenciais da API Twitch
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

    r = requests.get(url, params=param, headers=header).json()

    return str(r["data"][0]["id"])


def is_streamer_live(streamer_id, header):

    """
    Verifica se a pessoa está em live
    """

    url = "https://api.twitch.tv/helix/streams"
    param = {"user_id": streamer_id}

    r = requests.get(url, params=param, headers=header).json()

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

    r = requests.get(url, params=param, headers=header).json()

    return r["data"][0]["title"]
