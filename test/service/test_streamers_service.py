from livedivulgador.service.streamers_service import StreamersService
from livedivulgador.database.entities.streamer import Streamer
from livedivulgador.service.streamers_service import StreamersService
from pytest import fixture, mark


@fixture(scope="module")
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
