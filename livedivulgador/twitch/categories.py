class LiveStreamCategories:
    def __init__(self):
        self.categories = {
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

        self._enabled_categories = None

    def get_enabled_categories(self):
        return self._enabled_categories

    def set_enabled_categories(self, categories: list):
        self._enabled_categories = categories

    def reflect_enabled_categories(self, bot_name: str):
        self.set_enabled_categories(self.categories[bot_name])
