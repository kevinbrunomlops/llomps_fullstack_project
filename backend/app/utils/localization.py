def to_swedish_city(city: str | None) -> str:
    city_map = {
        # Sweden
        "Stockholm": "Stockholm",
        "Göteborg": "Göteborg",
        "Gothenburg": "Göteborg",
        "Malmö": "Malmö",

        # Norway
        "Oslo": "Oslo",
        "Bergen": "Bergen",
        "Tromso": "Tromsø",
        "Tromsø": "Tromsø",

        # Denmark
        "Copenhagen": "Köpenhamn",
        "København": "Köpenhamn",
        "Kobenhavn": "Köpenhamn",
        "Aarhus": "Århus",
        "Odense": "Odense",

        # Finland
        "Helsinki": "Helsingfors",
        "Turku": "Åbo",
        "Rovaniemi": "Rovaniemi",

        # Iceland
        "Reykjavik": "Reykjavík",
        "Reykjavík": "Reykjavík",

        # Regions
        "Golden Circle": "Gyllene cirkeln",
        "South Coast": "Sydkusten",
    }

    return city_map.get(city or "", city or "Okänd stad")


def to_swedish_budget(budget: str | None) -> str | None:
    budget_map = {
        "low": "låg",
        "medium": "medel",
        "high": "hög",

        "Low": "låg",
        "Medium": "medel",
        "High": "hög",
    }

    return budget_map.get(budget, budget)


def to_swedish_category(category: str | None) -> str | None:
    category_map = {
        "attraction": "sevärdhet",
        "activity": "aktivitet",
        "restaurant": "restaurang",
    }

    return category_map.get(category, category)


def to_swedish_environment(environment: str | None) -> str | None:
    environment_map = {
        "indoors": "inomhus",
        "outdoors": "utomhus",
        "mixed": "blandad miljö",
    }

    return environment_map.get(environment, environment)


def to_swedish_season(season: str | None) -> str | None:
    season_map = {
        "spring": "vår",
        "summer": "sommar",
        "autumn": "höst",
        "winter": "vinter",
        "all_year": "året runt",
    }

    return season_map.get(season, season)


def to_swedish_travel_style(style: str | None) -> str | None:
    style_map = {
        "solo": "solo",
        "couple": "par",
        "family": "familj",
        "friends": "vänner",
    }

    return style_map.get(style, style)