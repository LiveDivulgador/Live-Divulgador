from pytest import fixture, mark
from dotenv import load_dotenv
from os import getenv
from livedivulgador.twitch.client import TwitchClient

from livedivulgador.twitter.client import ClientKeys, TweetMetadata, TwitterClient

load_dotenv()


CONSUMER_KEY_A = getenv("CONSUMER_KEY_A")
CONSUMER_SECRET_A = getenv("CONSUMER_SECRET_A")
ACCESS_TOKEN_A = getenv("ACCESS_TOKEN_A")
ACCESS_TOKEN_SECRET_A = getenv("ACCESS_TOKEN_SECRET_A")

TWITCH_CLIENT_ID = getenv("CLIENT_ID")
TWITCH_CLIENT_SECRET = getenv("CLIENT_SECRET")


@fixture
def twitch_live():
    client = TwitchClient(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)

    live = client.get_random_streams()[1]

    return live


@fixture
def twitter_client():
    client_keys = ClientKeys(
        CONSUMER_KEY_A, CONSUMER_SECRET_A, ACCESS_TOKEN_A, ACCESS_TOKEN_SECRET_A
    )
    client = TwitterClient(client_keys)
    return client


def test_internal_api_works(twitter_client):
    assert isinstance(twitter_client._api.rate_limit_status(), dict)


def test_send_tweet(twitter_client, twitch_live):
    user_name = twitch_live["user_name"]
    live_title = twitch_live["title"]
    twitch_channel = f"https://twitch.tv/{twitch_live['user_name']}"
    tags = "#Twitch #live"

    tweet_metadata = TweetMetadata(
        twitter_display_name=user_name,
        twitch_channel=twitch_channel,
        twitch_stream_title=live_title,
        tags=tags,
        thumbnail="",
        # thumbnail=f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{twitch_live['user_name']}-1280x720.png",
    )

    twitter_client.send_tweet(tweet_metadata)
