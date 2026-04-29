from app.services.content_service import filter_places, get_supported_cities, load_places


def test_load_places():
    places = load_places()
    assert len(places) > 0
    assert "Stockholm" in get_supported_cities()


def test_filer_stockholm_attraction():
    places = filter_places(city="Stockholm", category="attraction")
    assert places
    assert all(place.city == "Stockholm" for place in places)
    assert all(place.category == "attraction" for place in places)


def test_filter_budget_family_environment():
    places = filter_places(
        city="Copenhagen",
        budget="low",
        family_friendly=True,
        environment="outdoors"
        )
    assert places