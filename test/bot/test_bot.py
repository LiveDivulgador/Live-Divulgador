from pytest import fixture
from livedivulgador.bots.livedivulgador import LiveDivulgador
from livedivulgador.plugins.twitter import TwitterPlugin


@fixture
def livedivulgador():
    plugins_list = [TwitterPlugin]

    bot = LiveDivulgador()

    bot.add_plugins(plugins_list)

    yield bot

    del bot


def test_livedivulgador_init(livedivulgador):
    livedivulgador.run()
