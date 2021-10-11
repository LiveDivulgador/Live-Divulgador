import datetime
import os
import sys

from tweepy import API, OAuthHandler
from twitch import get_1_streamer_id
from utils import ROOT_DIR, get_image

# Diretório referente às imagens personalizadas
DIR_IMAGE = os.path.join(ROOT_DIR, "img")

# Unicode emojis
EMOJIS = {"red_dot": u"\U0001F534", "arrow": u"\U000027A1"}


def twitter_OAuth(streamer_type):
    """
    Função que faz OAuth na conta correta
    """

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


def tweeted(twitter_username):
    """
    Verifica se a pessoa fora divulgada nos
    últimos 15 minutos

    [!} FUNÇÃO EM TESTE
    """

    minutes_threshold = 15
    num_last_tweets = 100
    now = datetime.datetime.now()

    # Obter o objecto API
    api = twitter_OAuth(streamer_type)

    # Obter os últimos 100 tweets
    tweets = Cursor(api.user_timeline, id="LiveDivulgador").items(
        num_last_tweets
    )

    for tweet in tweets:

        # Primeira linha do tweet (onde se encontra o @)
        tweet_first_line = tweet.text.split('\n')[0]

        if twitter_username in tweet_first_line:

            # Minutos passados após o tweet
            minutes_elapsed = (now - tweet.created_at).total_seconds() // 60

            # Caso já tenha sido tweetado há menos de 15 minutos
            # retornamos True
            if minutes_elapsed <= minutes_threshold:
                return True

    return False


def tweet(
    idt,
    name,
    twitch,
    twitter,
    title,
    isPrint,
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
    api = twitter_OAuth(streamer_type)

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
        if os.getenv("Env") == "Prod":
            # Se conseguiu descarregar a imagem
            # Se o streamer permitiu o print
            if is_image and isPrint:

                name_img = os.path.join(ROOT_DIR, name_img)

                # Enviar tweet com media
                api.update_with_media(name_img + ".png", status=tweet)

                # Elminar Imagens
                os.remove(name_img + ".png")
                os.remove(name_img + ".jpg")

            elif is_streamer_image and isPrint:
                api.update_with_media(name_img, status=tweet)

            else:
                api.update_status(tweet)

        # Caso estejamos no ambiente Dev, printamos o tweet
        else:
            print(tweet)

    return
