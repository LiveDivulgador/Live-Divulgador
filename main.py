import warnings
from datetime import timedelta
from logging import DEBUG, INFO, basicConfig, captureWarnings, getLogger
from time import sleep

import click
from timeloop import Timeloop

from livedivulgador.bots.livedivulgador import LiveDivulgador
from livedivulgador.handlers.create_streamer import CreateStreamerFromUsername
from livedivulgador.plugins.plugin import Plugin
from livedivulgador.plugins.twitter import TwitterPlugin
from livedivulgador.plugins.twitter_alternative import TwitterAlternativePlugin
from livedivulgador.service.streamers_service import StreamersService

logger = getLogger(__name__)


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("--debug", "-d", help="Enable debug logging", is_flag=True, default=False)
def main(debug):
    basicConfig(
        format="%(asctime)s [%(levelname)8s] [%(threadName)20s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=DEBUG if debug else INFO,
    )

    def custom_formatwarning(msg, *args, **kwargs):
        return str(msg)

    warnings.formatwarning = custom_formatwarning
    warnings.simplefilter("default")
    captureWarnings(True)

    logger.warning("Starting Live Divulgador bot")


def create_bots(_class, plugins: list[Plugin]):
    bots = [create_bot(_class, plugin) for plugin in plugins]

    return bots


def create_bot(_class, plugin: Plugin):
    bot = _class()
    bot.add_plugin(plugin)

    return bot


@main.command("run")
def run():
    tl = Timeloop()
    tl.logger = logger
    execute = True
    plugins = [TwitterPlugin, TwitterAlternativePlugin]
    bots = create_bots(LiveDivulgador, plugins)

    def exec_bots(bots: list[LiveDivulgador]) -> None:
        [create_bot_routine(bot) for bot in bots]

    def create_bot_routine(bot: LiveDivulgador) -> None:
        @tl.job(interval=timedelta(seconds=300))
        def start_loop():
            bot.run()

    exec_bots(bots)

    tl.start()

    while execute:
        try:
            sleep(1)
        except KeyboardInterrupt:
            logger.warning("Stopping Live Divulgador bot")
            tl.stop()
            execute = False


@main.command()
@click.option("twitch_username", "-u", help="Twitch username")
@click.option("twitter_username", "-t", help="Twitter username", default=None)
def add(twitch_username, twitter_username):
    logger.info(f"Trying to add `{twitch_username}`")
    CreateStreamerFromUsername.handle(twitch_username, twitter_username)


@main.command()
@click.option("twitch_username", "-u", help="Twitch username")
def rm(twitch_username):
    logger.info(f"Deleting streamer `{twitch_username}`")
    StreamersService.delete_streamer_by_name(twitch_username)


if __name__ == "__main__":
    main()
