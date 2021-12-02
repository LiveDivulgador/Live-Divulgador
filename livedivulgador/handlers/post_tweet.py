from logging import getLogger
from os import getenv
from typing import Union

from dotenv import load_dotenv

from livedivulgador.handlers.verify_online_streamers import (
    VerifyOnlineStreamers,
)
from livedivulgador.helpers.timeout import TimeoutValue
from livedivulgador.twitch.categories import LiveStreamCategories
from livedivulgador.twitch.tags import LiveStreamTags
from livedivulgador.twitter.client import (
    ClientKeys,
    TweetMetadata,
    TwitterClient,
)

load_dotenv()


CONSUMER_KEY_A = getenv("CONSUMER_KEY_A")
CONSUMER_SECRET_A = getenv("CONSUMER_SECRET_A")
ACCESS_TOKEN_A = getenv("ACCESS_TOKEN_A")
ACCESS_TOKEN_SECRET_A = getenv("ACCESS_TOKEN_SECRET_A")

TWITCH_CLIENT_ID = getenv("CLIENT_ID")
TWITCH_CLIENT_SECRET = getenv("CLIENT_SECRET")


logger = getLogger(__name__)


class PostTweet:
    cache: dict = {
        "tweeted": [],
    }

    client_keys = ClientKeys(
        CONSUMER_KEY_A, CONSUMER_SECRET_A, ACCESS_TOKEN_A, ACCESS_TOKEN_SECRET_A
    )

    enabled_categories = LiveStreamCategories("LiveDivulgador").enabled_categories

    twitter_client = TwitterClient(client_keys)

    @classmethod
    def handle(cls) -> None:
        try:
            data = VerifyOnlineStreamers.handle()
            cls.tweet(data)
        except Exception as e:
            logger.error(e)
            raise e

    @classmethod
    def generate_tweet_metadata(cls, data: dict) -> Union[TweetMetadata, None]:

        user_name = data["user_name"]
        live_title = data["title"]
        twitch_channel = f"https://twitch.tv/{data['user_name']}"
        category = data["game_name"]
        tags = LiveStreamTags(category).tags
        thumbnail = ""

        if category in cls.enabled_categories:
            tweet_metadata = TweetMetadata(
                twitter_display_name=user_name,
                twitch_channel=twitch_channel,
                twitch_stream_title=live_title,
                tags=tags,
                thumbnail=thumbnail,
                category=category,
            )

            return tweet_metadata

        logger.info(f"Skipping {user_name}: the category `{category}` is not enabled")

        return None

    @classmethod
    def update_tweeted(cls, data: dict) -> None:
        value = TimeoutValue(data["user_id"], 3600)
        cls.cache["tweeted"].append(value)

    @classmethod
    def ensure_cache_not_empty(cls) -> None:
        if cls.cache["tweeted"] == []:
            value = TimeoutValue("0", 15)
            cls.cache["tweeted"].append(value)

    @classmethod
    def refresh_tweeted_cache(cls) -> None:
        cls.ensure_cache_not_empty()

        for element in cls.cache["tweeted"]:
            if element.value == None:
                cls.cache["tweeted"].remove(element)

    @classmethod
    def remove_cached_from_tweet_list(cls, data) -> list[dict]:
        """Removes already tweeted users from the queue of incoming tweets"""
        cls.refresh_tweeted_cache()

        tweeted = cls.cache["tweeted"]
        tweeted_ids = [element.value for element in tweeted]

        online_streamer_not_cached = (
            lambda user: user if user["user_id"] not in tweeted_ids else None
        )

        online_streamer_to_tweet = list(filter(online_streamer_not_cached, data))

        return online_streamer_to_tweet

    @classmethod
    def handle_send_tweets(
        cls,
        not_cached_live_list: list[dict],
        live_tweet_metadata: list[TweetMetadata],
    ) -> None:
        if not_cached_live_list != []:
            logger.debug(f"Tweeting about streamers")
            list(map(cls.twitter_client.send_tweet, live_tweet_metadata))

            return None

        logger.info("No new live streamers to tweet")

    @classmethod
    def handle_update_cache(cls, not_cached_live_list: list) -> None:
        if not_cached_live_list != []:
            list(map(cls.update_tweeted, not_cached_live_list))
            logger.info("Updated tweeted streamers")

            return None

        logger.debug("No new live streamers to add to cache")

    @classmethod
    def handle_prepare_tweets(
        cls, live_list: list[dict]
    ) -> tuple[list[dict], list[TweetMetadata]]:
        """Defines streamers to receive new tweets and prepare the tweet list"""
        not_cached_streamers: list[dict] = cls.remove_cached_from_tweet_list(live_list)

        live_tweet_metadata: list[Union[TweetMetadata, None]] = list(
            map(cls.generate_tweet_metadata, not_cached_streamers)
        )

        filtered_live_tweet_metadata: list[TweetMetadata] = list(
            filter(None.__ne__, live_tweet_metadata)
        )

        return (not_cached_streamers, filtered_live_tweet_metadata)

    @classmethod
    def tweet(cls, live_list: list[dict]) -> None:
        not_cached_streamers, live_tweet_metadata = cls.handle_prepare_tweets(live_list)

        cls.handle_send_tweets(not_cached_streamers, live_tweet_metadata)

        cls.handle_update_cache(not_cached_streamers)
