import streamlit as st

def zapytaj_wartosci():
    """Pobiera 5 wartości od użytkownika i zapisuje je do session_state."""
    if "user_values" not in st.session_state:
        st.session_state["user_values"] = []

    if len(st.session_state["user_values"]) < 5:
        st.subheader("🎯 Jakie są Twoje 5 najważniejszych wartości?")
        value_input = st.text_input(
            f"Podaj wartość #{len(st.session_state['user_values']) + 1}",
            key="value_input"
        )

        if value_input and value_input.strip():
            st.session_state["user_values"].append(value_input.strip())
            st.rerun()
        st.stop()
    else:
        st.success("✅ Dziękuję! Twoje wartości zostały zapisane.")
        st.write("Twoje wartości:", ", ".join(st.session_state["user_values"]))
