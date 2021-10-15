from os import getenv

import requests

# Credenciais da API Twitch
client_id = getenv("CLIENT_ID")
client_secret = getenv("CLIENT_SECRET")


if client_id is None or client_id == '':
    raise ValueError('client_id não encontrado')

if client_secret is None or client_secret == '':
    raise ValueError('client_secret não encontrado')


def make_request(url, params, method="get", header=None):
    """
    Faz requests para a API da twitch
    """
    if method == "get" and header:
        r = requests.get(url, params=params, headers=header)

    elif method == "post":
        if header:
            r = requests.post(url, data=params, headers=header)

        # Para o OAuth
        else:
            r = requests.post(url, data=params)

    else:
        raise ValueError('Passou um método errado ou esqueceu do header')

    return r.json(), r.status_code


def create_twitch_url(streamer_name):
    """
    Retorna o URL do canal e o nome do mesmo
    """
    return "twitch.tv/" + streamer_name, streamer_name


def get_OAuth():

    """
    Obter credenciais de login para usar
    na API da Twitch
    """

    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }

    data, status_code = make_request(url, params, method="post")

    if status_code == 400:
        raise ConnectionError(data)

    access_token = data["access_token"]

    # Criamos o header para futuras requisições
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
    params = {"login": name}

    data, _ = make_request(url, params, header=header)

    return data["data"][0]["id"]


def get_stream_title(streamer_id, header):

    """
    Retorna o título da live
    """

    url = "https://api.twitch.tv/helix/channels"
    params = {"broadcaster_id": streamer_id}

    data, _ = make_request(url, params, header=header)

    return data["data"][0]["title"]


def get_streamer_name(streamer_id, header):
    """
    Retorna o nome do canal
    """

    url = "https://api.twitch.tv/helix/channels"

    params = {"broadcaster_id": streamer_id}

    data, _ = make_request(url, params, header=header)

    return create_twitch_url(data["data"][0]["broadcaster_login"])


def is_streamer_live(streamer_id, header):

    """
    Verifica se a pessoa está em live
    """

    url = "https://api.twitch.tv/helix/streams"
    params = {"user_id": streamer_id}

    data, _ = make_request(url, params, header=header)

    # Se sim retorna True e a categoria
    if data["data"]:
        return True, data["data"][0]["game_name"]

    # Se nao retorna False
    return False, None
