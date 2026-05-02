import streamlit as st
from services.mock_llm import generate_mock_response


def render_chat_interface():
    st.subheader("Travel chat")

    city = st.session_state.get("city")
    days = st.session_state.get("days")
    budget = st.session_state.get("budget")
    messages = st.session_state.get("messages", [])

    if not city or not days or not budget:
        st.warning("Please start by entering your trip details.")
        return

    for message in messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_message = st.chat_input("Tell the chatbot what you want to do...")

    if user_message:
        st.session_state.messages.append({
            "role": "user",
            "content": user_message
        })

        with st.chat_message("user"):
            st.write(user_message)

        response = generate_mock_response(
            user_message=user_message,
            city=city,
            days=days,
            budget=budget
        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        with st.chat_message("assistant"):
            st.write(response)