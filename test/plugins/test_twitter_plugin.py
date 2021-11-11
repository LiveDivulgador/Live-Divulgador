from pytest import fixture
from livedivulgador.plugins.twitter import TwitterPlugin
from livedivulgador.bots.bases import Bot


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
