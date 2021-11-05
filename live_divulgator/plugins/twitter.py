from logging import getLogger
from typing import Callable

from live_divulgator.handlers.post_tweet import PostTweet
from live_divulgator.plugins.plugin import Plugin

logger = getLogger(__name__)


class TwitterPlugin(Plugin):
    @staticmethod
    def run():
        logger.info("Running twitter plugin")
        PostTweet.handle()
