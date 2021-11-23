from logging import getLogger

from livedivulgador.service.streamers_service import StreamersService

logger = getLogger(__name__)


class FetchStreamerIds:
    is_cached = False
    streamer_ids = []

    @classmethod
    def handle(cls):
        if not cls.is_cached:
            try:
                logger.info("Fetching streamer ids")
                result = StreamersService.select_all_by_twitch_id()
                cls.streamer_ids = [str(r.twitch_id) for r in result]
            except Exception as e:
                logger.error(e)
                raise e

            cls.is_cached = True

        return cls.streamer_ids
