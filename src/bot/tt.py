import os
import sys

from tweepy import API, OAuthHandler
from utils import ROOT_DIR, get_image

# Diretório referente às imagens personalizadas
DIR_IMAGE = os.path.join(ROOT_DIR, "img")

# Unicode emojis
EMOJIS = {"red_dot": u"\U0001F534", "arrow": u"\U000027A1"}


def twitter_oauth(streamer_type):
    """
    Função que faz OAuth na conta correta
    """

    CONSUMER_KEY = os.environ["CONSUMER_KEY_A"]
    CONSUMER_SECRET = os.environ["CONSUMER_KEY_A"]
    ACCESS_TOKEN = os.environ["CONSUMER_KEY_A"]
    ACCESS_TOKEN_SECRET = os.environ["CONSUMER_KEY_A"]

    if streamer_type == "art":
        CONSUMER_KEY = os.environ["CONSUMER_KEY_B"]
        CONSUMER_SECRET = os.environ["CONSUMER_KEY_B"]
        ACCESS_TOKEN = os.environ["CONSUMER_KEY_B"]
        ACCESS_TOKEN_SECRET = os.environ["CONSUMER_KEY_B"]

    try:
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.secure = True
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = API(
            auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True
        )

    except BaseException as e:
        print("Error in twitter.py", e)
        sys.exit(1)

    return api


def tweet(
    idt,
    name,
    twitch,
    twitter,
    title,
    is_print,
    streamer_type,
    category,
    hashtags,
):

    # Definir tipo de streamer com base na categoria
    # da stream atual
    if category == "Science & Technology":
        streamer_type = "code"

    elif category == "Art" or category == "Makers & Crafting":
        streamer_type = "art"

    # Obter o objecto API
    api = twitter_oauth(streamer_type)

    # Se o streamer não tiver Twitter, usamos o nome da twitch
    if twitter == "NaN":
        twitter = twitch.split("/")[-1]
    else:
        twitter = "@" + twitter

    tweet = f"""{EMOJIS["arrow"]} {twitter} está em Live neste momento!{EMOJIS["red_dot"]}


{title.replace("#", " - ")}

Entra aí: https://www.{twitch}

{hashtags}"""

    # Verificar se streamer tem imagem propria
    name_img = os.path.join(DIR_IMAGE, str(idt) + ".png")
    is_streamer_image = os.path.exists(name_img)
    is_image = False

    if not is_streamer_image:

        # Nome do ficheiro de imagem criado
        # e se conseguiu descarregar a imagem
        name_img, is_image = get_image(name, ROOT_DIR)

        # Se estivermos em produção
        if os.getenv("ENV") == "Prod":
            # Se conseguiu descarregar a imagem
            # Se o streamer permitiu o print
            if is_image and is_print:

                name_img = os.path.join(ROOT_DIR, name_img)

                # Enviar tweet com media
                api.update_with_media(name_img + ".png", status=tweet)

                # Elminar Imagens
                os.remove(name_img + ".png")
                os.remove(name_img + ".jpg")

            elif is_streamer_image and is_print:
                api.update_with_media(name_img, status=tweet)

            else:
                api.update_status(tweet)

        # Caso estejamos no ambiente Dev, printamos o tweet
        else:
            print(tweet)
