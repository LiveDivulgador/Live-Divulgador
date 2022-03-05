import pytest
import sqlalchemy

from livedivulgador.handlers.create_streamer import CreateStreamerFromUsername
from livedivulgador.service.streamers_service import StreamersService


def test_create_streamer_already_exists_should_raise_sqlalchemy_exception():
    with pytest.raises(sqlalchemy.exc.SQLAlchemyError):
        CreateStreamerFromUsername.handle("vcwild")


def test_create_streamer_should_create_streamer_in_database():
    assert CreateStreamerFromUsername.handle("alanzoka") == True
    StreamersService.delete_streamer(38244180)


def test_create_streamer_w_twitter_should_create_streamer_in_database():
    assert CreateStreamerFromUsername.handle("alanzoka", "alanzoka") == True
    StreamersService.delete_streamer(38244180)
