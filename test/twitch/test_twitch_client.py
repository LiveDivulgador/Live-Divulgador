from src.bot.twitch.client import TwitchClient
from pytest import fixture
from dotenv import load_dotenv
from os import getenv
from pytest_schema import schema


load_dotenv()

TWITCH_CLIENT_ID = getenv("CLIENT_ID")

TWITCH_CLIENT_SECRET = getenv("CLIENT_SECRET")

STREAMER_SCHEMA = {
    'id': str,
    'user_id': str,
    'user_login': str,
    'user_name': str,
    'game_id': str,
    'game_name': str,
    'type': str,
    'title': str,
    'viewer_count': int,
    'started_at': str,
    'language': str,
    'thumbnail_url': str,
    'tag_ids': list[str],
    'is_mature': bool,
}


@fixture
def twitch_client():
    client = TwitchClient(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
    return client

def test_get_oauth():
    oauth = TwitchClient.get_oauth(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
    assert isinstance(oauth, str)

def test_get_streamer_id(twitch_client):
    streamer_id = twitch_client.get_streamer_id("dornellestv")
    assert streamer_id == "518380427"


def test_get_streams(twitch_client):
    response = twitch_client.get_random_streams()[0]
    assert response == schema(STREAMER_SCHEMA)

def test_get_stream_should_return_list_of_streams_if_stream_exists_else_empty_list(twitch_client):
    user_id = twitch_client.get_random_streams()
    user_ids = list(map(lambda x: x['user_id'], user_id))
    response = twitch_client.get_streams(user_ids)
    if response == []:
        assert True
    assert response == schema(list[STREAMER_SCHEMA])
