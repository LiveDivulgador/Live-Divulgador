from dataclasses import dataclass

from livedivulgador.twitter.message import Message


@dataclass
class ClientKeys:
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str


@dataclass
class TweetMetadata:
    twitter_display_name: str
    twitch_channel: str
    twitch_stream_title: str
    tags: str = Message.TAGS
    thumbnail: str = ""
