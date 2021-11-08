from pytest import fixture
from live_divulgator.plugins.twitter import TwitterPlugin
from live_divulgator.bots.bases import Bot


@fixture
def bot():
    class MockBot(Bot):
        ...

    bot = MockBot()

    yield bot

    del bot


def test_twitter_plugin(bot: Bot):
    bot.add_plugin(TwitterPlugin)

    bot.run()
