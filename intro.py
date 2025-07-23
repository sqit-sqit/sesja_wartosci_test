# intro.py
import streamlit as st

def pokaz_intro():
    st.title("👋 Witaj w aplikacji Odkrywania Wartości")

    st.markdown("""
    ### 🔍 Cel aplikacji:
    Ta aplikacja pomoże Ci odkryć, uporządkować i pogłębić refleksję nad Twoimi osobistymi wartościami.

    ### 🛤 Etapy pracy:
    1. **Wybór wartości** – wybierzesz lub wpiszesz ważne dla siebie wartości.
    2. **Redukcja do 10** – ograniczysz swój wybór do 10 kluczowych wartości.
    3. **Redukcja do 3** – wybierzesz 3 najważniejsze wartości w obecnym etapie życia.
    4. **Coaching wokół wartości** – wejdziesz w dialog coachingowy wokół wybranych wartości.
    5. **Podsumowanie** – otrzymasz podsumowanie procesu.

    ### 🤝 Jak korzystać:
    - Dodawaj wartości klikając na proponowane kafelki lub wpisując własne.
    - Usuwaj i edytuj wartości w panelu bocznym.
    - Postępuj zgodnie z komunikatami aplikacji krok po kroku.
    """, unsafe_allow_html=True)

    # if st.button("➡️ Kontynuuj"):
    #     st.session_state["etap"] = "wybor_wartosci"
    #     st.rerun()
