import streamlit as st

def zapytaj_wartosci(liczba_wartosci: int):
    """Pobiera określoną liczbę wartości od użytkownika i zapisuje je do session_state."""
    if "user_values" not in st.session_state:
        st.session_state["user_values"] = []

    if len(st.session_state["user_values"]) < liczba_wartosci:
        index = len(st.session_state["user_values"])
        st.subheader("🎯 Jakie są Twoje najważniejsze wartości?")
        value_input = st.text_input(
            f"Podaj wartość #{index + 1}",
            key=f"value_input_{index}"
        )

        if value_input and value_input.strip():
            st.session_state["user_values"].append(value_input.strip())
            st.rerun()
        st.stop()
    else:
        st.success("✅ Dziękuję! Twoje wartości zostały zapisane.")
        st.write("Twoje wartości:", ", ".join(st.session_state["user_values"]))
