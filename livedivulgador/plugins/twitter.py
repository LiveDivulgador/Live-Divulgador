from logging import getLogger
from typing import Callable

from livedivulgador.handlers.post_tweet import PostTweet
from livedivulgador.plugins.plugin import Plugin

logger = getLogger(__name__)


class TwitterPlugin(Plugin):
    @staticmethod
    def run():
        logger.info("Running twitter plugin")
        PostTweet.handle()
