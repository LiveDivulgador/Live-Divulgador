from livedivulgador.twitch.categories import LiveStreamCategories
import pytest


@pytest.fixture
def lives_stream_categories():
    live_stream_categories = LiveStreamCategories()
    yield live_stream_categories
    del live_stream_categories


def test_twitch_live_stream_get_enabled_categories_should_return_none():
    live_stream_categories = LiveStreamCategories()
    assert live_stream_categories.get_enabled_categories() == None


def test_twitch_live_stream_reflect_enabled_categories_from_live_divulgador_should_change_enabled_categories():
    live_stream_categories = LiveStreamCategories()

    live_stream_categories.reflect_enabled_categories("LiveDivulgador")

    expected_response = [
        "Science & Technology",
        "Software and Game Development",
        "Talk Shows & Podcasts",
    ]

    assert live_stream_categories.get_enabled_categories() == expected_response


def test_twitch_live_stream_reflect_enabled_categories_from_live_divulgador2_should_change_enabled_categories():
    live_stream_categories = LiveStreamCategories()

    live_stream_categories.reflect_enabled_categories("LiveDivulgador2")

    expected_response = [
        "Art",
        "Makers & Crafting",
    ]

    assert live_stream_categories.get_enabled_categories() == expected_response
