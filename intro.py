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
    co nazywamy naszym systemem wartości. 
    A to już możemy ogarnąć na poziomie świadomym.
                
    
    Zrozumienie swojego systemu wartości to pierwszy krok do zrozumienia siebie.
    Co mną kieruje. Co dla mnie jest ważne w życiu. Jak to wpływa na moje życiowe priorytety.
    Jeśli to dla Ciebie ważne, wygospodaruj siebie do pół godziny czasu, tylko dla siebie.  
    Kliknij przycisk **Zaczynamy** i wejdź w proces refleksji nad własnymi wartościami, 
    przez który ta aplikacja Ciebie poprowadzi.


    # """, unsafe_allow_html=True)

    st.session_state["kontynuuj_aktywny"] = True

    # if st.button("➡️ Kontynuuj"):
    #     st.session_state["etap"] = "wybor_wartosci"
    #     st.rerun()
