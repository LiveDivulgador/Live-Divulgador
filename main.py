import warnings
from datetime import timedelta
from logging import DEBUG, INFO, basicConfig, captureWarnings, getLogger
from time import sleep

import click
from timeloop import Timeloop

from livedivulgador.bots.livedivulgador import LiveDivulgador
from livedivulgador.plugins.twitter import TwitterPlugin

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


@main.command("run")
def run():
    tl = Timeloop()
    tl.logger = logger
    execute = True
    divulgador = LiveDivulgador()
    divulgador.add_plugin(TwitterPlugin)

    @tl.job(interval=timedelta(seconds=30))
    def start_loop():
        divulgador.run()

    tl.start()

    while execute:
        try:
            sleep(1)
        except KeyboardInterrupt:
            logger.warning("Stopping Live Divulgador bot")
            tl.stop()
            execute = False


if __name__ == "__main__":
    main()
