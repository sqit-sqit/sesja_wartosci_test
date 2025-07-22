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

    # Inicjalizacja session_state
    if "user_values" not in st.session_state:
        st.session_state["user_values"] = []
    if "losowe_wartosci" not in st.session_state:
        st.session_state["losowe_wartosci"] = random.sample(wszystkie, min(n, len(wszystkie)))
    if "dodano_wartosc" not in st.session_state:
        st.session_state["dodano_wartosc"] = False

    st.markdown("### ✨ Kliknij, aby dodać wartość")

    cols = st.columns(5)
    for i, val in enumerate(st.session_state["losowe_wartosci"]):
        col = cols[i % 5]
        with col:
            if st.button(val, key=f"suggestion_{val}_{i}"):
                if val not in st.session_state["user_values"]:
                    
                    if "just_added" not in st.session_state:
                          st.session_state["just_added"] = []
                    st.session_state["user_values"].append(val)
                    # st.session_state["just_added"].append(val)
                    st.rerun()                   
                    return  # przerywa dalsze wykonywanie po kliknięciu

    # Po rerunie resetujemy flagę
    if st.session_state.get("dodano_wartosc"):
        st.session_state["dodano_wartosc"] = False

    st.markdown("")

    # Przycisk: Pokaż inne propozycje
    if st.button("🔄 Pokaż inne propozycje", key="losuj_inne_propozycje"):
        st.session_state["losowe_wartosci"] = random.sample(wszystkie, min(n, len(wszystkie)))
        st.session_state["dodano_wartosc"] = False
        st.rerun()
