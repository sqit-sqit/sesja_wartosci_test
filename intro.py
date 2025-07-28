# intro.py
import streamlit as st

def pokaz_intro():
    # st.title("👋 Witaj w aplikacji Odkrywania Wartości")

    st.markdown("""
    ### 🔍 Moje Osobiste Wartości? O co tu chodzi?
    Jakie według mnie jest jedno z najważniejszych pytań, które sam sobie zadaję? 
    To pytanie to "Dlaczego?"
    
    1. **Dlaczego robię to, co robię?**
    2. **Dlaczego podejmuję takie a nie inne decyzje?**
    3. **Dlaczego dokonuję takich a nie innych wyborów**

  
    Nie tak prosto na to odpowiedzieć, bo te najgłębsze przyczyny, 
    które o tym decydują są często poukrywane w naszej podświadomości, 
    ukształtowane przez naszą przeszłość, doświadczenia, i przeżycia.
    Natomiast te  poukrywane dynamiki kształtują coś, 
    co nazywamy naszym systemem wartości, czyli zestawu wartości, 
    które są tak ważne w życiu, że określają nasze postępowanie. 
    A to już możemy rozpoznać na poziomie świadomym.
                
    
    Zrozumienie swojego systemu wartości to pierwszy krok do zrozumienia siebie.
    Co mną kieruje. Co dla mnie jest ważne w życiu. Jak to wpływa na moje życiowe priorytety.
                
    Jeśli to dla Ciebie ważne, wygospodaruj siebie do pół godziny czasu, tylko dla siebie
    i poeksploruj, co Ciebie napędza. 
                

    **UWAGA:** 
                
    Dane z tej sesji są logowane. Zostaną zapisane wartości, które wybierzesz, 
    treść refleksji z formie dialogu z Agentem oraz treść podsumowania. Nie będą logowane  
    Kliknij przycisk **Zaczynamy** i wejdź w proces refleksji nad własnymi wartościami,
    przez który ta aplikacja Ciebie poprowadzi. Wszystko po to, by Agenta można było udoskonalać,
    by lepiej służył kolejnym użytkownikom.
    Nie będą logowane żadne dane, które umożliwiłyby zidentifikowanie Ciebie.
    Natomiast jeśli nie wyrażasz zgody na logowanie Twojej sesji, po prostu przerwij proces.


    # """, unsafe_allow_html=True)

    st.session_state["kontynuuj_aktywny"] = True

    # if st.button("➡️ Kontynuuj"):
    #     st.session_state["etap"] = "wybor_wartosci"
    #     st.rerun()
