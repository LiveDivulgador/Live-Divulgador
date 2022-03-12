from livedivulgador.database.entities.streamer import Streamer
from livedivulgador.service.streamers_service import StreamersService
from livedivulgador.twitch.client import TwitchClient

from logging import getLogger
from os import getenv

from dotenv import load_dotenv

from livedivulgador.twitter.client import (
    ClientKeys,
    TwitterClient,
)

load_dotenv()


logger = getLogger(__name__)


class CreateStreamerFromUsername:
    twitch_client = TwitchClient(getenv("CLIENT_ID"), getenv("CLIENT_SECRET"))

    twitter_client = TwitterClient(
        ClientKeys(
            getenv("CONSUMER_KEY_A"),
            getenv("CONSUMER_SECRET_A"),
            getenv("ACCESS_TOKEN_A"),
            getenv("ACCESS_TOKEN_SECRET_A"),
        )
    )

    @classmethod
    def handle(cls, twitch_username, twitter_username=None):
        try:
            twitch_id = cls.twitch_client.get_streamer_id(twitch_username)
            if twitter_username:
                twitter_id = cls.twitter_client.get_user_id(twitter_username)
            else:
                twitter_id = None
            streamer = Streamer(
                twitch_id=twitch_id,
                twitter_id=twitter_id,
                name=twitch_username,
            )

            StreamersService.create_streamer(streamer)
            logger.info(
                f"Streamer `{twitch_username}` created: twitch_id={twitch_id}, twitter_id={twitter_id}"
            )
            return True
        except Exception as e:
            logger.error(e)
            return False
