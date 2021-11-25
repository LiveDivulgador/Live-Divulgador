class LiveStreamCategories:
    def __init__(self, bot_name: str):
        self.reflect_enabled_categories(bot_name)

    @property
    def enabled_categories(self):
        return self._enabled_categories

    def __set_enabled_categories(self, categories: list):
        self._enabled_categories = categories

    def reflect_enabled_categories(self, bot_name: str):
        categories = {
            "LiveDivulgador": [
                "Science & Technology",
                "Software and Game Development",
                "Talk Shows & Podcasts",
            ],
            "LiveDivulgador2": [
                "Art",
                "Makers & Crafting",
            ],
        }

        enabled_categories = categories.get(bot_name, [])
        self.__set_enabled_categories(enabled_categories)
