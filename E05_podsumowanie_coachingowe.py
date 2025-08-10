import streamlit as st
from openai import OpenAI
from pathlib import Path
from utils import wczytaj_szablony, wczytaj_osobowosc

def podsumowanie_coachingowe(api_key: str, model: str):
    client = OpenAI(api_key=api_key)
    st.subheader("🧠 Zatrzymajmy się jeszcze na chwilę i podsumujmy to nasze spotkanie")

    if "podsumowanie_chat" not in st.session_state:
        st.session_state["podsumowanie_chat"] = []

        # Wczytaj pytania z pliku jako inspirację
        szablony = wczytaj_szablony("pytania_podsumowujace.txt")
        prompt_szablonowy = "\n".join(szablony) if szablony else ""

        # Wczytaj osobowość z pliku i dodaj pytania jako inspirację
        system_prompt = wczytaj_osobowosc(
            path="chatbot_personality_podsumowanie.txt",
            wartosc="wartości użytkownika",  # można zostawić jako placeholder
            prompt_szablonowy=prompt_szablonowy
        )

        # spinner
        # thinking = st.empty()
        # thinking.info("⏳ Coach AI przygotowuje pytanie na start...")
        # with st.spinner("AI myśli..."):
        #     response = client.chat.completions.create(
        #         model= model,
        #         messages=st.session_state["podsumowanie_chat"]
        #     )
        # thinking.empty()


        st.session_state["podsumowanie_chat"].append({
            "role": "system",
            "content": system_prompt
        })

        # Zainicjuj sesję pytaniem od AI
        response = client.chat.completions.create(
            model= model,
            messages=st.session_state["podsumowanie_chat"]
        )
        first_message = response.choices[0].message.content.strip()
        st.session_state["podsumowanie_chat"].append({"role": "assistant", "content": first_message})

        if "messages" not in st.session_state:
            st.session_state["messages"] = []
        if response.usage:
            st.session_state["messages"].append({
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            })

    # Wyświetlenie historii czatu
    for msg in st.session_state["podsumowanie_chat"]:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Input użytkownika
    user_input = st.chat_input("Co chciałbyś/chciałabyś powiedzieć?")
    if user_input:
        st.session_state["podsumowanie_chat"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # spinner
        thinking = st.empty()
        # thinking.info("⏳ Coach AI formułuje odpowiedź...")
        with st.spinner("Daj mi chwilę..."):
            response = client.chat.completions.create(
                model= model,
                messages=st.session_state["podsumowanie_chat"]
            )
        thinking.empty()


        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model= model,
                messages=st.session_state["podsumowanie_chat"]
            )
            ai_msg = response.choices[0].message.content.strip()
            st.markdown(ai_msg)
        st.session_state["podsumowanie_chat"].append({"role": "assistant", "content": ai_msg})

        if "messages" not in st.session_state:
            st.session_state["messages"] = []
        if response.usage:
            st.session_state["messages"].append({
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            })

        st.session_state["kontynuuj_aktywny"] = True
