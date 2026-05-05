import streamlit as st
from data.city_data import COUNTRIES_AND_CITIES, BUDGET_OPTIONS, CITY_MAPPING


def render_trip_form():
    st.subheader("Planera din resa")

    country = st.selectbox(
        "Välj ett land",
        list(COUNTRIES_AND_CITIES.keys())
    )

    city_label = st.selectbox(
        "Välj en stad",
        COUNTRIES_AND_CITIES[country]
    )

    city = CITY_MAPPING[city_label]

    days = st.slider(
        "Hur många dagar planerar du att resa?",
        min_value=1,
        max_value=14,
        value=4
    )

    budget_label = st.selectbox(
        "Välj din budget",
        list(BUDGET_OPTIONS.keys())
    )

    budget = BUDGET_OPTIONS[budget_label]

    submitted = st.button("Börja resechatt")

    return submitted, country, city, days, budget