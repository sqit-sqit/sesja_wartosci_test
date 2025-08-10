import streamlit as st

def redukuj_wartosci(limit, nastepny_etap, komunikat):
    

    st.subheader("🎯 Wybór ważniejszych wartości")

    with st.expander("👉 Kliknij, by schować lub rozwiniąć tę sekcję", expanded=True):
        st.markdown(f"""
        Przyjrzyj się tym wartościom, które zostały wybrane. Co one mówią o Tobie? Kim jesteś? Jak definiują Twoją tożsamość? Weź głębszy oddech, jeśli pomoże to lepiej poczuć.
 
        Jeśli w poprzednim kroku zostało wybranych więcej niż **{limit}** wartości, to teraz jest moment, by zastanowić się, które z nich mają dla Ciebie większe znaczenie. Usuń te mniej istotne wartości tak, by zostało ich nie więcej niż właśnie **{limit}**.
        

        Klikając na daną wartość w oknie po lewej stronie powodujesz jej usunięcie. Gdy zostanie **{limit}** lub mniej wartości, pojawi się przycisk **Kontynuuj**, 
        który pozwoli przejść do następnego etapu.

                    
        """)

    # st.info(komunikat)

    if "user_values" not in st.session_state or not st.session_state["user_values"]:
        st.warning("Brak wartości do redukcji.")
        return

    wartosci = st.session_state["user_values"]



    st.markdown("---")
    if len(wartosci) <= limit:
        st.warning(f"Ok, możesz kontynuować usuwanie tych mniej istotnych wartości a gdy skończysz, mozesz przejść do następnego etapu")
        st.session_state["kontynuuj_aktywny"] = True
     #   if st.button("✅ Kontynuuj"):
     #       st.session_state["user_values"] = wartosci
     #       st.session_state["etap"] = nastepny_etap
     #       st.rerun()
    else:
        st.warning(f"Usuń jeszcze {len(wartosci) - limit} wartości, by móc kontynuować.")
        st.session_state["kontynuuj_aktywny"] = False
