from livedivulgador.handlers.post_tweet import PostTweet
from dotenv import load_dotenv
from os import getenv
from livedivulgador.twitter.client import ClientKeys
from livedivulgador.twitch.categories import LiveStreamCategories


load_dotenv()

CONSUMER_KEY_B = getenv("CONSUMER_KEY_B")
CONSUMER_SECRET_B = getenv("CONSUMER_SECRET_B")
ACCESS_TOKEN_B = getenv("ACCESS_TOKEN_B")
ACCESS_TOKEN_SECRET_B = getenv("ACCESS_TOKEN_SECRET_B")


class PostTweetAlternative(PostTweet):
    client_keys = ClientKeys(
        CONSUMER_KEY_B, CONSUMER_SECRET_B, ACCESS_TOKEN_B, ACCESS_TOKEN_SECRET_B
    )

    live_stream_categories = LiveStreamCategories()
    live_stream_categories.reflect_enabled_categories("LiveDivulgador2")
    enabled_categories = live_stream_categories.get_enabled_categories()
