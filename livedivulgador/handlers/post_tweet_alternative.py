from os import getenv

from dotenv import load_dotenv

from livedivulgador.handlers.post_tweet import PostTweet
from livedivulgador.twitter.client import ClientKeys

load_dotenv()

CONSUMER_KEY_B = getenv("CONSUMER_KEY_B")
CONSUMER_SECRET_B = getenv("CONSUMER_SECRET_B")
ACCESS_TOKEN_B = getenv("ACCESS_TOKEN_B")
ACCESS_TOKEN_SECRET_B = getenv("ACCESS_TOKEN_SECRET_B")

CLIENT_KEYS_B = ClientKeys(
    CONSUMER_KEY_B, CONSUMER_SECRET_B, ACCESS_TOKEN_B, ACCESS_TOKEN_SECRET_B
)


class PostTweetAlternative(PostTweet):
    def __init__(
        self,
        client_keys: ClientKeys = CLIENT_KEYS_B,
        bot_name: str = "LiveDivulgador2",
    ):
        super().__init__(client_keys=client_keys, bot_name=bot_name)
