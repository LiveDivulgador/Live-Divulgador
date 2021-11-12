class LiveStreamCategories:
    def __init__(self):
        self._enabled_categories = [
            "Art",
            "Makers & Crafting",
            "Science & Technology",
            "Software and Game Development",
            "Talk Shows & Podcasts",
        ]

    @property
    def enabled_categories(self):
        return self._enabled_categories

    @enabled_categories.setter
    def enabled_categories(self, categories: list):
        self._enabled_categories = categories
