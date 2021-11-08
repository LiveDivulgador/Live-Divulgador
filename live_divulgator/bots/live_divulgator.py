from logging import getLogger

from live_divulgator.bots.bases import Bot

logger = getLogger(__name__)


class LiveDivulgator(Bot):
    def run(self):
        logger.info("Running LiveDivulgator routines")
        self.load_plugins()
