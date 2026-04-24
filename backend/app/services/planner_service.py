"""Simple deterministic day-plan builder from recommendation result."""

from app.schemas.recommendations import RecommendationResponse


def _pick(items: list, index: int):
    if not items:
        return None
    return items[index % len(items)]


def build_day_plan(city: str, days: int, recommendations: RecommendationResponse) -> str:
    if not any([recommendations.attractions, recommendations.restaurants,recommendations.activities]):
        return f"No plan could be created for {city} yet."
    
    day_lines: list[str] = []
    for day in range(1, days + 1):
        attraction = _pick(recommendations.restaurants, day -1) 
        restaurant = _pick(recommendations.restaurants, day -1)
        activity = _pick(recommendations.activities, day - 1)

        parts = [f"Day {day} in {city}:"]
        if attraction:
            parts.append(f"start with {attraction.name}")
        if restaurant:
            parts.append(f"eat at {restaurant.name}")
        if activity:
            parts.append(f"finish with {activity.name}")
        day_lines.append(", ".join(parts) + ".")

    return "\n".join(day_lines)
