from live_divulgator.bots.live_divulgator import LiveDivulgator
from logging import getLogger, basicConfig, DEBUG, INFO, captureWarnings
from live_divulgator.plugins.twitter import TwitterPlugin
import warnings
import click

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

    logger.warning("Starting Live Divulgator bot")


@main.command("run")
def run():
    config = TwitterPlugin

    live_divulgator = LiveDivulgator()

    live_divulgator.add_plugin(config)
    live_divulgator.run()


if __name__ == "__main__":
    main()
