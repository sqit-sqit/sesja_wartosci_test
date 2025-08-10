import streamlit as st
from openai import OpenAI
from utils import wczytaj_osobowosc
from pathlib import Path


def wczytaj_szablony(plik="pytania_poglebiajace.txt"):
    sciezka = Path(plik)
    if not sciezka.exists():
        return []
    with open(sciezka, "r", encoding="utf-8") as f:
        return [linia.strip() for linia in f if linia.strip()]


def wybor_top_3(api_key: str, model: str):
    # st.title("🏅 Wybierz 3 Najważniejsze Wartości")
    st.subheader("🎯 Wybierz 3 Najważniejsze Wartości")

    with st.expander("👉 Kliknij, by schować lub rozwiniąć tę sekcję", expanded=True):
        st.markdown(f"""
        A gdyby teraz miałyby zostać tylko 3 wartości? Te wartości, które stanowią esencję Twojej istoty?
        To które zaznaczysz?
                    
        Spośród tych, które zostały wybieraj kolejno te, które w tym momencie wydają się najbliższe Tobie.
        I daj się zaprosić na chwilę reflekcji nad nimi.
        Co one mówią o Tobie? Kim jesteś? Jak definiują Twoją tożsamość? 
        Znowu weź głębszy oddech, to zawsze pomaga mieć lepszy kontakt ze sobą.
                    
        Jeśli poczujesz, że rozmowa na temat danej wartości przeciąga się i że chcesz przejść dalej
        daj o tym znać w czacie.
                     
        """)

    # if "user_values" not in st.session_state or len(st.session_state["user_values"]) != 10:
    #     st.error("Nie można przejść do tego etapu. Najpierw wybierz dokładnie 10 wartości.")
    #     return

    if "top_3" not in st.session_state:
        st.session_state["top_3"] = []

    if "aktywny_chat_top3" not in st.session_state:
        st.session_state["aktywny_chat_top3"] = None

    client = OpenAI(api_key=api_key)

    top_10 = st.session_state["user_values"]

 
    if st.session_state["top_3"]:
        st.markdown("### ✅ Twoje wybrane wartości:")

        kol1, kol2 = st.columns(2)
        for i, val in enumerate(st.session_state["top_3"].copy()):
            kol = kol1 if i % 2 == 0 else kol2
            with kol:
                usun = st.button(f"× {val}", key=f"usun_top3_main_{val}")
                if usun:
                    st.session_state["top_3"].remove(val)
                    if st.session_state["aktywny_chat_top3"] == val:
                        st.session_state["aktywny_chat_top3"] = None
                    st.rerun()



    wybrana = st.session_state.get("aktywny_chat_top3")

    if wybrana:
        st.markdown("---")
        st.subheader(f"🌀 Porozmawiajmy o  wartości: **{wybrana}**")

        if "coaching_top_3" not in st.session_state:
            st.session_state["coaching_top_3"] = {}

        if wybrana not in st.session_state["coaching_top_3"]:
            szablony = wczytaj_szablony()
            prompt_szablonowy = "\n".join(szablony) if szablony else ""
            osobowosc = wczytaj_osobowosc(
                path="chatbot_personality_coach.txt",
                wartosc=wybrana,
                prompt_szablonowy=prompt_szablonowy
            )

            st.session_state["coaching_top_3"][wybrana] = [
                {"role": "system", "content": osobowosc}
            ]

            # AI zadaje pierwsze pytanie
            response = client.chat.completions.create(
                model=model,
                messages=st.session_state["coaching_top_3"][wybrana],
                temperature=0.9,
                top_p=0.95,
                presence_penalty=0.6,
                frequency_penalty=0.2,
            )
            first_msg = response.choices[0].message.content.strip()
            st.session_state["coaching_top_3"][wybrana].append(
                {"role": "assistant", "content": first_msg}
            )

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

        # Wyświetl historię czatu (pomijając "system")
        for msg in st.session_state["coaching_top_3"][wybrana]:
            if msg["role"] != "system":
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        # Wprowadź odpowiedź użytkownika
        user_input = st.chat_input("Napisz swoją odpowiedź...")
        if user_input:
            st.session_state["coaching_top_3"][wybrana].append(
                {"role": "user", "content": user_input}
            )
            with st.chat_message("user"):
                st.markdown(user_input)

        # spinner
            thinking = st.empty()
            thinking.info("⏳ Daj mi chwilę... zbieram myśli :)")
            with st.spinner("Daj mi chwilę... zbieram myśli..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=st.session_state["coaching_top_3"][wybrana]
                )
            thinking.empty()

            with st.chat_message("assistant"):
                response = client.chat.completions.create(
                    model=model,
                    messages=st.session_state["coaching_top_3"][wybrana]
                )
                ai_reply = response.choices[0].message.content.strip()
                st.markdown(ai_reply)

            st.session_state["coaching_top_3"][wybrana].append(
                {"role": "assistant", "content": ai_reply}
            )
            if response.usage:
                st.session_state["messages"].append({
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    }
                })
        st.session_state["kontynuuj_aktywny"] = True