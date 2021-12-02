from logging import getLogger

from livedivulgador.bots.bases import Bot

logger = getLogger(__name__)


class LiveDivulgador(Bot):
    def run(self):
        logger.info("Running LiveDivulgador routines")
        self.load_plugins()
