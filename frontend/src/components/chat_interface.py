import streamlit as st
import requests

import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
API_URL = f"{BACKEND_URL}/chat"


def render_chat_interface():
    st.subheader("Resechatt")

    city = st.session_state.get("city")
    days = st.session_state.get("days")
    budget = st.session_state.get("budget")
    messages = st.session_state.get("messages", [])

    if not city or not days or not budget:
        st.warning("Börja med att fylla i dina reseuppgifter.")
        return

    for message in messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_message = st.chat_input("Berätta vad du vill ha hjälp med...")

    if user_message:
        st.session_state.messages.append({
            "role": "user",
            "content": user_message
        })

        with st.chat_message("user"):
            st.write(user_message)

        try:
            response = requests.post(
                API_URL,
                json={
                    "message": user_message,
                    "city": city,
                    "days": days,
                    "budget": budget.lower() if budget else None,
                    "use_google_maps": False
                },
                timeout=300
            )

            if response.status_code != 200:
                st.error(response.text)
                answer = f"Backend svarade med felkod {response.status_code}"
            else:
                data = response.json()
                answer = data["answer"]

        except Exception as e:
            answer = f"Något gick fel när appen kontaktade backend: {e}"

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        with st.chat_message("assistant"):
            st.write(answer)