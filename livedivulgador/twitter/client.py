from logging import getLogger

from tweepy import API, OAuthHandler
from tweepy.errors import Forbidden
from livedivulgador.twitter.generics import ClientKeys, TweetMetadata
from livedivulgador.twitter.message import Message

logger = getLogger(__name__)


class TwitterClient:
    def __init__(self, client_keys: ClientKeys) -> None:
        self._api = __class__.get_api(client_keys)

    @staticmethod
    def fetch_api(client_keys: ClientKeys) -> API:
        auth = OAuthHandler(client_keys.consumer_key, client_keys.consumer_secret)
        auth.set_access_token(client_keys.access_token, client_keys.access_token_secret)

        api = API(auth)

        try:
            api.verify_credentials()
        except Exception as err:
            logger.error(f"{__class__.__name__} error: {err}")
            raise err

        return api

    @staticmethod
    def get_api(client_keys: ClientKeys):
        api = __class__.fetch_api(client_keys)

        return api

    def send_tweet(self, tweet_metadata: TweetMetadata) -> None:
        message = Message.PROTOTYPE.value.format(
            tweet_metadata.twitter_display_name,
            tweet_metadata.twitch_stream_title,
            tweet_metadata.twitch_channel,
            tweet_metadata.tags,
            tweet_metadata.thumbnail,
        )

        channel_name = str(tweet_metadata.twitch_channel).split("/")[-1]

        try:
            self._api.update_status(status=message)
            logger.info(f"{channel_name} tweet sent successfully")
        except Forbidden:
            logger.error(f"Exception: {channel_name} tweet was already done")
