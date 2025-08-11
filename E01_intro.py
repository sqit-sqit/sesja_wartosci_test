# intro.py
import streamlit as st

def pokaz_intro():
    # st.title("👋 Witaj w aplikacji Odkrywania Wartości")

    st.markdown("""
    
    ### Droga Osobo testująca :)
    Dziękuję za Twój czas poświęcony na przejście przez tę aplikację.
    Efekty tego posłużą jej udoskonalaniu po to, by w niedalekiej przyszłości inni
    mogli z niej czerpać wartość.
    Jak z tym pracować? Wyobraź sobie, że bierzesz udział w sesji coachingowej.
    Postaraj się na odpowiedzi jak najbardziej naturalne i szczere tak, 
    jakby to była rozmowa z innym człowiekiem. Jeśli coś Cię zirytuje, napisz o tym.
                
    Sesje w pewnym fragmencie prowadzi AI. On(a) czasem potrzebuje czasu na odpowiedź.
    Wykaż się proszę cierpliwością, jeśli nic przez dłuzszy momen nie będzie się działo
    na ekranie. Niech Cię też nie razi skronmy interfejs. On z casem wypięknieje :)
    
    I podziel się w bezpośrednim kontakcie ze mną swoimi wrażeniami z tej sesji.
    To bardzo dla mnie ważne, 
                
    pozdrawiam, Adam
                
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
                
    Jeśli to dla Ciebie ważne, wygospodaruj sobie do pół godziny czasu, tylko dla siebie
    i poeksploruj, co Ciebie napędza. 

    Kliknij przycisk **Zaczynamy** i wejdź w proces refleksji nad własnymi wartościami,
                

    **UWAGA:** 
                
    Dane z tej sesji są logowane. Zostaną zapisane wartości, które wybierzesz, 
    treść refleksji z formie dialogu z Agentem oraz treść podsumowania. 
    Wszystko po to, by Agenta można było udoskonalać, by lepiej służył kolejnym użytkownikom.
    Nie będą logowane żadne dane, które umożliwiłyby zidentifikowanie Ciebie.
    Natomiast jeśli nie wyrażasz zgody na logowanie Twojej sesji, po prostu przerwij proces.


    # """, unsafe_allow_html=True)

    st.session_state["kontynuuj_aktywny"] = True

    # if st.button("➡️ Kontynuuj"):
    #     st.session_state["etap"] = "wybor_wartosci"
    #     st.rerun()
