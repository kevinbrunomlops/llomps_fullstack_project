def generate_first_message(city, days, budget):
    return (
        f"Great! You're going to {city} for {days} days with a {budget.lower()} budget. "
        f"Here are some ideas to get started:\n\n"
        f"- Explore the city center\n"
        f"- Visit popular cultural spots\n"
        f"- Try local food\n"
        f"- Take time to walk around and discover hidden places\n\n"
        f"What kind of activities are you most interested in?"
    )


def generate_mock_response(user_message, city, days, budget):
    return (
        f"That sounds interesting! Since you're visiting {city} for {days} days "
        f"with a {budget.lower()} budget, I would suggest choosing activities that match your style. "
        f"You mentioned: '{user_message}'.\n\n"
        f"A good next step could be to plan one main activity per day and leave space for food, walking, and relaxing."
    )