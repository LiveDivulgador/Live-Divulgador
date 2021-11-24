from logging import getLogger

from livedivulgador.handlers.post_tweet_alternative import PostTweetAlternative
from livedivulgador.plugins.plugin import Plugin

logger = getLogger(__name__)


class TwitterAlternativePlugin(Plugin):
    @staticmethod
    def run():
        logger.debug(f"Running {__class__.__name__}")
        PostTweetAlternative().handle()
