from logging import getLogger

from live_divulgator.service.streamers_service import StreamersService

logger = getLogger(__name__)


class FetchStreamerIds:
    @staticmethod
    def handle():
        try:
            logger.info("Fetching streamer ids")
            result = StreamersService.select_all_by_twitch_id()
        except Exception as e:
            logger.error(e)
            raise e

        filtered = [str(r.twitch_id) for r in result]

        return filtered
