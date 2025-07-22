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

    # Dodajemy stan do przechowywania wartości losowych
    if "losowe_wartosci" not in st.session_state:
        st.session_state["losowe_wartosci"] = random.sample(wszystkie, min(n, len(wszystkie)))

    # Przycisk do zmiany listy
    # if st.button("🔄 Pokaż inne propozycje"):
    #    st.session_state["losowe_wartosci"] = random.sample(wszystkie, min(n, len(wszystkie)))

    # Styl + wyświetlenie wartości
    st.markdown("""
    <style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
        gap: 12px;
        margin-top: 1rem;
        padding: 1rem;
    }
    .grid-item {
        background-color: #ffeaa7;
        border-radius: 12px;
        padding: 10px 15px;
        text-align: center;
        font-size: 1rem;
        font-weight: 500;
        animation: fadeInUp 0.6s ease;
        transition: transform 0.2s;
    }
    .grid-item:hover {
        transform: scale(1.05);
        background-color: #fab1a0;
    }
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("### ✨ Na początku podaj 10 wartości, które są wazne w Twoim zyciu. Mozesz się inspirować przykładami ponizej")

    html = "<div class='grid-container'>"
    for val in st.session_state["losowe_wartosci"]:
        html += f"<div class='grid-item'>{val}</div>"
    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

       # Przycisk do zmiany listy
    if st.button("🔄 Pokaż inne propozycje"):
        st.session_state["losowe_wartosci"] = random.sample(wszystkie, min(n, len(wszystkie)))
