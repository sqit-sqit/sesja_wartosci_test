import streamlit as st

def redukuj_wartosci(limit, nastepny_etap, komunikat):
    
    with st.expander("👉 Kliknij, by schować lub rozwiniąć tę sekcję", expanded=True):
        st.markdown(f"""
        **Ogranicz liczbę wartości do {limit}**.  
        Teraz jest moment, by dokonać wyboru usuwając mniej istotne dla Ciebie wartości tak,
        by zostało ich nie więcej niż **{limit}**.
        Gdy zostanie **{limit}** lub mniej wartości, pojawi się przycis **Kontynuuj**, 
        który pozwoli przejść do następnego etapu

                    
        """)
    st.subheader("🎯 Wybór ważniejszych wartości")
    st.info(komunikat)

    if "user_values" not in st.session_state or not st.session_state["user_values"]:
        st.warning("Brak wartości do redukcji.")
        return

    wartosci = st.session_state["user_values"]

    # kol1, kol2 = st.columns(2)
    # for i, val in enumerate(wartosci.copy()):
    #     kol = kol1 if i % 2 == 0 else kol2
    #     with kol:
    #         usun = st.button(f"× {val}", key=f"usun_{val}")
    #         if usun:
    #             wartosci.remove(val)
    #             st.rerun()

    st.markdown("---")
    if len(wartosci) <= limit:
        st.warning(f"Ok, mozesz kontynuować i przejść do następnego etapu")
        st.session_state["kontynuuj_aktywny"] = True
     #   if st.button("✅ Kontynuuj"):
     #       st.session_state["user_values"] = wartosci
     #       st.session_state["etap"] = nastepny_etap
     #       st.rerun()
    else:
        st.warning(f"Usuń jeszcze {len(wartosci) - limit} wartości, by kontynuować.")
        st.session_state["kontynuuj_aktywny"] = False
