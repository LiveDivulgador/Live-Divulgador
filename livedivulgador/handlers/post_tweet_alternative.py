from os import getenv

from dotenv import load_dotenv

from livedivulgador.handlers.post_tweet import PostTweet
from livedivulgador.twitch.categories import LiveStreamCategories
from livedivulgador.twitter.client import ClientKeys, TwitterClient

load_dotenv()

CONSUMER_KEY_B = getenv("CONSUMER_KEY_B")
CONSUMER_SECRET_B = getenv("CONSUMER_SECRET_B")
ACCESS_TOKEN_B = getenv("ACCESS_TOKEN_B")
ACCESS_TOKEN_SECRET_B = getenv("ACCESS_TOKEN_SECRET_B")


class PostTweetAlternative(PostTweet):
    cache: dict = {
        "tweeted": [],
    }

    client_keys = ClientKeys(
        CONSUMER_KEY_B, CONSUMER_SECRET_B, ACCESS_TOKEN_B, ACCESS_TOKEN_SECRET_B
    )

    enabled_categories = LiveStreamCategories("LiveDivulgador2").enabled_categories

    twitter_client = TwitterClient(client_keys)
