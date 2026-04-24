import streamlit as st

from components.trip_form import render_trip_form
from components.chat_interface import render_chat_interface
from services.mock_llm import generate_first_message


st.set_page_config(
    page_title="Scandinavia Travel Chatbot",
    page_icon="🧭",
    layout="wide"
)

st.title("🧭 Scandinavia Travel Chatbot")
st.write("Plan your trip through Sweden, Norway, and Denmark with a simple travel guide chatbot.")

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

        first_message = generate_first_message(city, days, budget)

        st.session_state.messages.append({
            "role": "assistant",
            "content": first_message
        })

        st.rerun()

else:
    col1, col2 = st.columns([1, 3])

    with col1:
        st.info(
            f"**Trip details**\n\n"
            f"Country: {st.session_state.country}\n\n"
            f"City: {st.session_state.city}\n\n"
            f"Days: {st.session_state.days}\n\n"
            f"Budget: {st.session_state.budget}"
        )

        if st.button("Start over"):
            st.session_state.clear()
            st.rerun()

    with col2:
        render_chat_interface()