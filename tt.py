from tweepy import OAuthHandler, API
from utils import getImage
from twitch import get1StreamerId
import sys
import os

DIR_IMAGE = os.path.abspath(os.path.dirname("."))
DIR_IMAGE = os.path.join(DIR_IMAGE, "img")

# Unicode para o círculo vermelho
emojis = {"red_dot": u"\U0001F534", "arrow": u"\U000027A1"}


def twitter_OAuth(streamer_type):
    """ Função que faz OAuth na conta correta"""

    CONSUMER_KEY = os.environ["CONSUMER_KEY_C"]
    CONSUMER_SECRET = os.environ["CONSUMER_SECRET_C"]
    ACCESS_TOKEN = os.environ["ACCESS_TOKEN_C"]
    ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET_C"]

    if streamer_type == "art":
        CONSUMER_KEY = os.environ["CONSUMER_KEY_A"]
        CONSUMER_SECRET = os.environ["CONSUMER_SECRET_A"]
        ACCESS_TOKEN = os.environ["ACCESS_TOKEN_A"]
        ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET_A"]

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


def tweet(twitch, twitter, title, isPrint, streamer_type, hashtags):

    # Obter o objecto API
    api = twitter_OAuth(streamer_type)

    # Se o streamer não tiver Twitter, usamos o nome da twitch
    if twitter == "NaN":
        twitter = twitch.split("/")[-1]
    else:
        twitter = "@" + twitter

    tweet = f"""{emojis["arrow"]} {twitter} está em Live neste momento!{emojis["red_dot"]}

	
{title.replace("#", " - ")}

Entra aí: https://www.{twitch}

{hashtags}"""

    # Verificar se streamer tem imagem propria
    streamer_id = get1StreamerId(twitch.split("/")[-1])
    name_img = os.path.join(DIR_IMAGE, streamer_id + ".png")
    isStreamerImage = os.path.exists(name_img)
    isImage = False

    if not isStreamerImage:

        # Nome do ficheiro de imagem criado
        # e se conseguiu descarregar a imagem
        name_img, isImage = getImage(twitch.split("/")[-1])

    # Se conseguiu descarregar a imagem e se os streamer permitiu o print
    if isImage and isPrint:
        # Enviar tweet com media
        api.update_with_media(name_img + ".png", status=tweet)

        # Elminar Imagens
        os.remove(name_img + ".png")
        os.remove(name_img + ".jpg")

    elif isStreamerImage and isPrint:
        api.update_with_media(name_img, status=tweet)

    else:
        api.update_status(tweet)

    return
