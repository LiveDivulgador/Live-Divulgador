from logging import getLogger


logger = getLogger(__name__)


class LiveStreamTags:
    def __init__(self, category: str) -> None:
        self._category = category
        self._tags = "#twitch #live"

        self.reflect_tags()

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, tags: str):
        self._tags = tags

    def reflect_tags(self) -> None:
        tags = {
            "Science & Technology": "#ciencia #tecnologia",
            "Software and Game Development": "#livecoding #dev",
            "Talk Shows & Podcasts": "#talk #podcast",
            "Art": "#arte #criar",
            "Makers & Crafting": "#maker #DIY",
        }

        generic_tags = "#twitch #live"
        enabled_tags = tags.get(self._category, None)

        if enabled_tags:
            self.tags = enabled_tags + " " + generic_tags
            return None

        logger.info(f"Using generic bot tags for category `{self._category}`")
