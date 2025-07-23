import streamlit as st

def redukuj_wartosci(limit, nastepny_etap, komunikat):
    st.subheader("🎯 Redukcja wartości")
    st.info(komunikat)

    if "user_values" not in st.session_state or not st.session_state["user_values"]:
        st.warning("Brak wartości do redukcji.")
        return

    wartosci = st.session_state["user_values"]

    kol1, kol2 = st.columns(2)
    for i, val in enumerate(wartosci.copy()):
        kol = kol1 if i % 2 == 0 else kol2
        with kol:
            usun = st.button(f"× {val}", key=f"usun_{val}")
            if usun:
                wartosci.remove(val)
                st.rerun()

    st.markdown("---")
    if len(wartosci) <= limit:
        if st.button("✅ Kontynuuj"):
            st.session_state["user_values"] = wartosci
            st.session_state["etap"] = nastepny_etap
            st.rerun()
    else:
        st.warning(f"Usuń jeszcze {len(wartosci) - limit} wartości, by kontynuować.")
