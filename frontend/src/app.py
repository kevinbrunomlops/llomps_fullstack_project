import streamlit as st

from frontend.src.components.trip_form import render_trip_form
from frontend.src.components.chat_interface import render_chat_interface
from backend.app.utils.localization import to_swedish_city, to_swedish_budget
import requests

import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
API_URL = f"{BACKEND_URL}/chat"

st.set_page_config(
    page_title="Nordic Travel Chatbot",
    page_icon="🧭",
    layout="wide"
)

st.title("🧭 Nordic Travel Chatbot")
st.write("Planera din resa genom Norden med en enkel svensk reseguide.")

if "chat_started" not in st.session_state:
    st.session_state.chat_started = False

if "messages" not in st.session_state:
    st.session_state.messages = []


if not st.session_state.chat_started:
    submitted, country, city, days, budget = render_trip_form()

    if submitted:
        st.session_state.country = country
        st.session_state.city = city
        st.session_state.days = days
        st.session_state.budget = budget
        st.session_state.chat_started = True

        try:
            api_response = requests.post(
                API_URL,
                json={
                    "message": "Ge mig ett personligt välkomstmeddelande och några första resetips baserat på mina reseuppgifter.",
                    "city": city,
                    "days": days,
                    "budget": budget.lower() if budget else None,
                    "use_google_maps": False
                },
                timeout=300
            )

            if api_response.status_code != 200:
                first_message = f"Backend error {api_response.status_code}: {api_response.text}"
            else:
                first_message = api_response.json()["answer"]

        except Exception as e:
            first_message = f"Kunde inte hämta ett personligt första svar från backend: {e}"

        st.session_state.messages.append({
            "role": "assistant",
            "content": first_message
        })

        st.rerun()

else:
    col1, col2 = st.columns([1, 3])

    with col1:
        swedish_city = to_swedish_city(st.session_state.city)
        swedish_budget = to_swedish_budget(st.session_state.budget)

        st.info(
            f"**Reseuppgifter**\n\n"
            f"Land: {st.session_state.country}\n\n"
            f"Stad: {swedish_city}\n\n"
            f"Dagar: {st.session_state.days}\n\n"
            f"Budget: {swedish_budget}"
        )

        if st.button("Börja om"):
            for key in ["chat_started", "messages", "country", "city", "days", "budget"]:
                st.session_state.pop(key, None)
            st.rerun()

    with col2:
        render_chat_interface()