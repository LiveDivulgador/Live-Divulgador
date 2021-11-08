from collections import deque
from logging import getLogger
from os import getenv

from dotenv import load_dotenv

from live_divulgator.handlers.verify_online_streamers import VerifyOnlineStreamers
from live_divulgator.helpers.timeout import TimeoutValue
from live_divulgator.twitter.client import ClientKeys, TweetMetadata, TwitterClient

load_dotenv()


CONSUMER_KEY_A = getenv("CONSUMER_KEY_A")
CONSUMER_SECRET_A = getenv("CONSUMER_SECRET_A")
ACCESS_TOKEN_A = getenv("ACCESS_TOKEN_A")
ACCESS_TOKEN_SECRET_A = getenv("ACCESS_TOKEN_SECRET_A")

TWITCH_CLIENT_ID = getenv("CLIENT_ID")
TWITCH_CLIENT_SECRET = getenv("CLIENT_SECRET")


logger = getLogger(__name__)


class PostTweet:
    client_keys = ClientKeys(
        CONSUMER_KEY_A, CONSUMER_SECRET_A, ACCESS_TOKEN_A, ACCESS_TOKEN_SECRET_A
    )

    twitter_client = TwitterClient(client_keys)

    cache: dict = {
        "tweeted": [],
    }

    @classmethod
    def handle(cls) -> None:
        try:
            data = VerifyOnlineStreamers.handle()
            logger.info("Tweeting about `data`")
            cls.tweet(data)
        except Exception as e:
            logger.error(e)
            raise e

    @classmethod
    def generate_tweet_metadata(cls, data: dict) -> TweetMetadata:
        user_name = data["user_name"]
        live_title = data["title"]
        twitch_channel = f"https://twitch.tv/{data['user_name']}"
        tags = "#Twitch #live"
        thumbnail = ""

        tweet_metadata = TweetMetadata(
            twitter_display_name=user_name,
            twitch_channel=twitch_channel,
            twitch_stream_title=live_title,
            tags=tags,
            thumbnail=thumbnail,
        )

        return tweet_metadata

    @classmethod
    def update_tweeted(cls, data: dict) -> None:
        value = TimeoutValue(data["user_id"], 3600)
        cls.cache["tweeted"].append(value)

    @classmethod
    def ensure_cache_not_empty(cls):
        if cls.cache["tweeted"] == []:
            value = TimeoutValue("0", 15)
            cls.cache["tweeted"].append(value)

    @classmethod
    def refresh_tweeted_cache(cls):
        cls.ensure_cache_not_empty()

        for element in cls.cache["tweeted"]:
            if element.value == None:
                cls.cache["tweeted"].remove(element)

    @classmethod
    def remove_cached_from_tweet_list(cls, data):
        cls.refresh_tweeted_cache()

        tweeted = cls.cache["tweeted"]
        tweeted_ids = [element.value for element in tweeted]

        online_streamer_not_cached = (
            lambda user: user if user["user_id"] not in tweeted_ids else None
        )

        online_streamer_to_tweet = list(filter(online_streamer_not_cached, data))

        return online_streamer_to_tweet

    @classmethod
    def tweet(cls, live_list: list[dict]) -> None:
        not_cached_live_list = cls.remove_cached_from_tweet_list(live_list)

        live_tweet_metadata: list[TweetMetadata] = list(
            map(cls.generate_tweet_metadata, not_cached_live_list)
        )

        if not_cached_live_list == []:
            logger.info("No new live streamers to tweet")

        logger.info(f"Tweeting about streamers")
        deque(map(cls.twitter_client.send_tweet, live_tweet_metadata))

        deque(map(cls.update_tweeted, not_cached_live_list))
        logger.info("Updated tweeted streamers")
