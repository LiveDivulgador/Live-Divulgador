from logging import getLogger
from os import getenv

from dotenv import load_dotenv

from live_divulgator.handlers.fetch_streamer_ids import FetchStreamerIds
from live_divulgator.twitch.client import TwitchClient

load_dotenv()

logger = getLogger(__name__)


class VerifyOnlineStreamers:
    twitch_client = TwitchClient(getenv("CLIENT_ID"), getenv("CLIENT_SECRET"))

    @classmethod
    def handle(cls) -> list[dict]:
        try:
            streamer_ids = FetchStreamerIds.handle()
            logger.info("Verifying online streamers")
            response = cls.twitch_client.get_streams(streamer_ids)
        except Exception as e:
            logger.error(e)
            raise e
        return response
