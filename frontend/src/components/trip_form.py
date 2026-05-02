import streamlit as st
from data.city_data import COUNTRIES_AND_CITIES, BUDGET_OPTIONS


def render_trip_form():
    st.subheader("Plan your trip")

    country = st.selectbox(
        "Choose a country",
        list(COUNTRIES_AND_CITIES.keys())
    )

    city = st.selectbox(
        "Choose a city",
        COUNTRIES_AND_CITIES[country]
    )

    days = st.slider(
        "How many days are you staying?",
        min_value=1,
        max_value=14,
        value=4
    )

    budget = st.selectbox(
        "Choose your budget",
        BUDGET_OPTIONS
    )

    submitted = st.button("Start travel chat")

    return submitted, country, city, days, budget