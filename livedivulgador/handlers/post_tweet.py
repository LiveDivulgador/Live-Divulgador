from logging import getLogger
from os import getenv
from typing import Union

from dotenv import load_dotenv

from livedivulgador.handlers.verify_online_streamers import (
    VerifyOnlineStreamers,
)
from livedivulgador.helpers.timeout import TimeoutValue
from livedivulgador.twitch.categories import LiveStreamCategories
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

CLIENT_KEYS_A = ClientKeys(
    CONSUMER_KEY_A, CONSUMER_SECRET_A, ACCESS_TOKEN_A, ACCESS_TOKEN_SECRET_A
)

TWITCH_CLIENT_ID = getenv("CLIENT_ID")
TWITCH_CLIENT_SECRET = getenv("CLIENT_SECRET")


logger = getLogger(__name__)


class PostTweet:
    def __init__(
        self,
        client_keys: ClientKeys = CLIENT_KEYS_A,
        bot_name: str = "LiveDivulgador",
    ):
        live_stream_categories = LiveStreamCategories()
        live_stream_categories.reflect_enabled_categories(bot_name)

        self.enabled_categories = (
            live_stream_categories.get_enabled_categories()
        )
        self.twitter_client = TwitterClient(client_keys)
        self.cache: dict = {
            "tweeted": [],
        }

    def handle(self) -> None:
        try:
            data = VerifyOnlineStreamers.handle()
            self.tweet(data)
        except Exception as e:
            logger.error(e)
            raise e

    def generate_tweet_metadata(
        self, data: dict
    ) -> Union[TweetMetadata, None]:

        user_name = data["user_name"]
        live_title = data["title"]
        twitch_channel = f"https://twitch.tv/{data['user_name']}"
        category = data["game_name"]
        tags = "#Twitch #live"
        thumbnail = ""

        if category in self.enabled_categories:
            tweet_metadata = TweetMetadata(
                twitter_display_name=user_name,
                twitch_channel=twitch_channel,
                twitch_stream_title=live_title,
                tags=tags,
                thumbnail=thumbnail,
                category=category,
            )

            return tweet_metadata

        logger.info(
            f"Skipping {user_name}: the category `{category}` is not enabled"
        )

        return None

    def update_tweeted(self, data: dict) -> None:
        value = TimeoutValue(data["user_id"], 3600)
        self.cache["tweeted"].append(value)

    def ensure_cache_not_empty(self) -> None:
        if self.cache["tweeted"] == []:
            value = TimeoutValue("0", 15)
            self.cache["tweeted"].append(value)

    def refresh_tweeted_cache(self) -> None:
        self.ensure_cache_not_empty()

        for element in self.cache["tweeted"]:
            if element.value == None:
                self.cache["tweeted"].remove(element)

    def remove_cached_from_tweet_list(self, data) -> list[dict]:
        """Removes already tweeted users from the queue of incoming tweets"""
        self.refresh_tweeted_cache()

        tweeted = self.cache["tweeted"]
        tweeted_ids = [element.value for element in tweeted]

        online_streamer_not_cached = (
            lambda user: user if user["user_id"] not in tweeted_ids else None
        )

        online_streamer_to_tweet = list(
            filter(online_streamer_not_cached, data)
        )

        return online_streamer_to_tweet

    def handle_send_tweets(
        self,
        not_cached_live_list: list[dict],
        live_tweet_metadata: list[TweetMetadata],
    ) -> None:
        if not_cached_live_list != []:
            logger.debug(f"Tweeting about streamers")
            list(map(self.twitter_client.send_tweet, live_tweet_metadata))

            return None

        logger.info("No new live streamers to tweet")

    def handle_update_cache(self, not_cached_live_list: list) -> None:
        if not_cached_live_list != []:
            list(map(self.update_tweeted, not_cached_live_list))
            logger.info("Updated tweeted streamers")

            return None

        logger.debug("No new live streamers to add to cache")

    def handle_prepare_tweets(
        self, live_list: list[dict]
    ) -> tuple[list[dict], list[TweetMetadata]]:
        """Defines streamers to receive new tweets and prepare the tweet list"""
        not_cached_streamers: list[dict] = self.remove_cached_from_tweet_list(
            live_list
        )

        live_tweet_metadata: list[Union[TweetMetadata, None]] = list(
            map(self.generate_tweet_metadata, not_cached_streamers)
        )

        filtered_live_tweet_metadata: list[TweetMetadata] = list(
            filter(None.__ne__, live_tweet_metadata)
        )

        return (not_cached_streamers, filtered_live_tweet_metadata)

    def tweet(self, live_list: list[dict]) -> None:
        not_cached_streamers, live_tweet_metadata = self.handle_prepare_tweets(
            live_list
        )

        self.handle_send_tweets(not_cached_streamers, live_tweet_metadata)

        self.handle_update_cache(not_cached_streamers)
