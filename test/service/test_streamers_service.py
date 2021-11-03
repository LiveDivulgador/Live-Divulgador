from src.bot.service.streamers_service import StreamersService
from src.bot.database.engine import Session
from src.bot.database.entities.streamer import Streamer
from src.bot.database.entities.streamer import Base, Streamer
from src.bot.service.streamers_service import StreamersService
from src.bot.database.engine import engine
from pytest import fixture, mark


@fixture
def created_streamer(twitch_id):
    streamer = Streamer(twitch_id=twitch_id, twitter_id=8250, name="Radhy")
    StreamersService.create_streamer(streamer)

    yield streamer

    StreamersService.delete_streamer(twitch_id)


@mark.parametrize("twitch_id", [89037])
def test_get_streamer(created_streamer, twitch_id):

    response = StreamersService.get_streamer(twitch_id)

    assert twitch_id == response[0].twitch_id


def test_database_get_streamers():
    streamers = StreamersService.get_streamers()

    assert len(streamers) > 0
