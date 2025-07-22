import streamlit as st
import random
from pathlib import Path

def pokaz_losowe_wartosci_animowane(n=30, plik="lista_wartosci.txt"):
    sciezka = Path(plik)
    if not sciezka.exists():
        st.warning("Nie znaleziono pliku lista_wartosci.txt")
        return

    with open(sciezka, "r", encoding="utf-8") as f:
        wszystkie = [linia.strip() for linia in f if linia.strip()]

    if not wszystkie:
        st.warning("Plik lista_wartosci.txt jest pusty.")
        return

    # Inicjalizacja
    if "user_values" not in st.session_state:
        st.session_state["user_values"] = []
    if "losowe_wartosci" not in st.session_state:
        st.session_state["losowe_wartosci"] = random.sample(wszystkie, min(n, len(wszystkie)))

    # 🔁 Odświeżenie listy wartości
    if st.button("🔄 Pokaż inne propozycje", key="shuffle_values"):
        st.session_state["losowe_wartosci"] = random.sample(wszystkie, min(n, len(wszystkie)))

    st.markdown("### ✨ Kliknij, by dodać wartość")

    # ✅ Interaktywne przyciski w kontenerze (nie formie!)
    container = st.container()
    cols = container.columns(5)

    for i, val in enumerate(st.session_state["losowe_wartosci"]):
        col = cols[i % 5]
        with col:
            if st.button(val, key=f"suggestion_{i}_{val}"):
                if val not in st.session_state["user_values"]:
                    st.session_state["user_values"].append(val)
