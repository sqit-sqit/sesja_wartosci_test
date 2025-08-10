
import streamlit as st
from openai import OpenAI
from dotenv import dotenv_values
import os

# import modułów
from pokaz_losowe_wartosci import pokaz_losowe_wartosci_animowane
from redukcja import redukuj_wartosci
from etap_postepu import pokaz_pasek_postepu
from podsumowanie_coachingowe import podsumowanie_coachingowe
from intro import pokaz_intro
from podsumowanie import pokaz_podsumowanie
from wybor_top_3 import wybor_top_3

#raporty
from panel_raportow import panel_raportow, usun_raporty

model_pricings = {
    "gpt-4o": {
        "input_tokens": 5.00 / 1_000_000,
        "output_tokens": 15.00 / 1_000_000,
    },
    "gpt-4o-mini": {
        "input_tokens": 0.150 / 1_000_000,
        "output_tokens": 0.600 / 1_000_000,
    }
}
MODEL = "gpt-4o-mini"
USD_TO_PLN = 3.97
PRICING = model_pricings[MODEL]
LICZBA_WARTOSCI = 10

env = dotenv_values(".env")

def autoryzacja_do_raportow():
    with st.sidebar:
        st.markdown("## 🔐 Dostęp do raportów")

        # login = st.text_input("Login", key="raport_login")
        password = st.text_input("Hasło", type="password", key="raport_password")
        if os.environ.get('APP_ENV') != 'production':
            if password == env.get("RAPORT_PASSWORD"):
                st.session_state["raport_autoryzowany"] = True
            else:
                st.session_state["raport_autoryzowany"] = False
        elif os.environ.get('APP_ENV') == 'production':
            if password == os.environ["RAPORT_PASSWORD"]:
                st.session_state["raport_autoryzowany"] = True
            else:
                st.session_state["raport_autoryzowany"] = False


# # OpenAI API key
# if not st.session_state.get("openai_api_key"):
#     if "OPENAI_API_KEY" in env:
#         st.session_state["openai_api_key"] = env["OPENAI_API_KEY"]
#     else:
#         st.info("Dodaj swój klucz API OpenAI aby móc korzystać z tej aplikacji")
#         st.session_state["openai_api_key"] = st.text_input("Klucz API", type="password")
#         if st.session_state["openai_api_key"]:
#             st.rerun()

# if not st.session_state.get("openai_api_key"):
#     st.stop()


if not st.session_state.get("openai_api_key"):
    if os.environ.get('APP_ENV') != 'production':
        if "OPENAI_API_KEY" in env:
            st.session_state["openai_api_key"] = env["OPENAI_API_KEY"]
    elif os.environ.get("OPENAI_API_KEY"):
        st.session_state["openai_api_key"] = os.environ["OPENAI_API_KEY"]
    else:
        st.info("Dodaj swój klucz API OpenAI aby móc korzystać z tej aplikacji")
        st.session_state["openai_api_key"] = st.text_input("Klucz API", type="password")
        if st.session_state["openai_api_key"]:
            st.rerun()

if not st.session_state.get("openai_api_key"):
    st.stop()



# Initiation
if "etap" not in st.session_state:
    st.session_state["etap"] = "Intro"

if "wybrana_wartosc" not in st.session_state:
    st.session_state["wybrana_wartosc"] = []

if "kontynuuj_aktywny" not in st.session_state:
    st.session_state["kontynuuj_aktywny"] = True

if "coaching_index" not in st.session_state:
        st.session_state["coaching_index"] = 0
        st.session_state["coaching_chat"] = {}

st.title(":classical_building: Moje Osobiste Wartości")
# pokaz_pasek_postepu()

# Etapy
if st.session_state["etap"] == "Intro":
    pokaz_intro()
 #   if st.button("✅ Zaczynamy"):
 #       st.session_state["etap"] = "wybor_wartosci"
 #       st.rerun()

elif st.session_state["etap"] == "wybor_wartosci":
    pokaz_losowe_wartosci_animowane()
#    if st.button("✅ Kontunuuj"):
#        st.session_state["etap"] = "redukcja_do_10"
#        st.rerun()

elif st.session_state["etap"] == "redukcja_do_10":
    redukuj_wartosci(limit=10, nastepny_etap="wybor_top_3", komunikat="Usuń wartości, aż zostanie ich tylko 10.")

elif st.session_state["etap"] == "wybor_top_3":
    wybor_top_3(api_key=st.session_state["openai_api_key"])

elif st.session_state["etap"] == "podsumowanie_coachingowe":
    podsumowanie_coachingowe(api_key=st.session_state["openai_api_key"])

elif st.session_state["etap"] == "podsumowanie":
    pokaz_podsumowanie(
        api_key=st.session_state["openai_api_key"], 
        model=MODEL,
        pricing=PRICING,
        usd_to_pln=USD_TO_PLN
    )

if st.session_state.get("rerun"):
    st.session_state["rerun"] = False
    st.rerun()

# Sidebar
with st.sidebar:
    st.header("🎯 Twoje wartości")
    if "user_values" not in st.session_state:
        st.session_state["user_values"] = []

    liczba_wartosci = len(st.session_state["user_values"])
    etap = st.session_state["etap"]



    wartosci = st.session_state["user_values"]
    
    if (
        st.session_state["etap"] == "Intro"
        or st.session_state["etap"] == "wybor_wartosci"
        or st.session_state["etap"] == "redukcja_do_10"
    ):    
        st.markdown(
            f"<div style='font-size: 1.1rem; margin-bottom: 1rem;'>🔢 Wybranych wartości: <b>{liczba_wartosci}</b></div>",
            unsafe_allow_html=True
        )        
        
        kol1, kol2 = st.columns(2)
        for i, val in enumerate(wartosci.copy()):
            kol = kol1 if i % 2 == 0 else kol2
            with kol:
                usun = st.button(f"× {val}", key=f"usun_sidebar_{val}")
                if usun:
                    wartosci.remove(val)
                    st.session_state["last_deleted"] = val
                    st.rerun()



    if st.session_state["etap"] == "wybor_top_3":
        # st.subheader("🧩 Wybierz 3 najważniejsze wartości")

        # if "top_3" not in st.session_state:
        #     st.session_state["top_3"] = []

        # if "wybrana_wartosc" not in st.session_state:
        #     st.session_state["wybrana_wartosc"] = None

        # kol1, kol2 = st.columns(2)
        # top_10 = st.session_state["user_values"]  # założenie: wcześniej zredukowano do 10

        # for i, val in enumerate(top_10):
        #     kol = kol1 if i % 2 == 0 else kol2
        #     with kol:
        #         if st.button(val, key=f"top3_sidebar_{val}"):
        #             if val not in st.session_state["top_3"] and len(st.session_state["top_3"]) < 3:
        #                 st.session_state["top_3"].append(val)
        #                 st.session_state["wybrana_wartosc"] = val
        st.markdown("### 🔘 Wybierz 3 kluczowe wartości:")
        top_10 = st.session_state["user_values"]
        kol1, kol2 = st.columns(2)
        for i, val in enumerate(top_10):
            kol = kol1 if i % 2 == 0 else kol2
            with kol:
                if st.button(val, key=f"top3_{val}"):
                    if val not in st.session_state["top_3"]:
                        if len(st.session_state["top_3"]) < 3:
                            st.session_state["top_3"].append(val)
                            st.session_state["aktywny_chat_top3"] = val
                            st.rerun()
                    else:
                        st.session_state["top_3"].remove(val)
                        if st.session_state["aktywny_chat_top3"] == val:
                            st.session_state["aktywny_chat_top3"] = None
                        st.rerun()

    if (
        st.session_state["etap"] == "podsumowanie_coachingowe"
        or st.session_state["etap"] == "podsumowanie"
    ):
        # st.markdown("### 🔘 Twoje 3 kluczowe wartości:")
        top3 = st.session_state.get("top_3", [])

        if not top3:
            st.info("Brak wybranych wartości TOP 3.")
        else:
            for val in top3:
                st.markdown(
                    f"""
                    <div style='
                        border: 1px solid #ddd;
                        border-radius: 8px;
                        padding: 6px 10px;
                        margin-bottom: 6px;
                        background-color: #f9f9f9;
                        font-size: 1rem;
                        font-weight: 500;
                        text-align: center;
                    '>{val}</div>
                    """,
                    unsafe_allow_html=True
                )



    st.markdown("---")
    if "last_deleted" in st.session_state:
        if st.button("↩️ Przywróć ostatnio usuniętą"):
            val = st.session_state.pop("last_deleted")
            if val not in st.session_state["user_values"]:
                st.session_state["user_values"].append(val)
                st.rerun()

    st.markdown("---")

    total_cost = 0
    for message in st.session_state.get("messages", []):
        if "usage" in message:
            total_cost += message["usage"]["prompt_tokens"] * PRICING["input_tokens"]
            total_cost += message["usage"]["completion_tokens"] * PRICING["output_tokens"]



# NAWIGACJA

    if st.session_state.get("kontynuuj_aktywny"):
        if st.session_state["etap"] == "Intro":
            if st.button("✅ Zaczynamy"):
                st.session_state["etap"] = "wybor_wartosci"
                st.session_state["kontynuuj_aktywny"] = False
                st.rerun()

        elif st.session_state["etap"] == "wybor_wartosci":
            if st.button("✅ Kontunuuj"):
                st.session_state["etap"] = "redukcja_do_10"
                st.session_state["kontynuuj_aktywny"] = False
                st.rerun()

        elif st.session_state["etap"] == "redukcja_do_10":
            if st.button("✅ Kontunuuj"):
                st.session_state["etap"] = "wybor_top_3"
                st.session_state["kontynuuj_aktywny"] = False
                st.rerun()
            

        elif st.session_state["etap"] == "wybor_top_3":
            if st.button("✅ Kontunuuj"):
                st.session_state["etap"] = "podsumowanie_coachingowe"
                st.session_state["kontynuuj_aktywny"] = False
                st.rerun()
  

        elif st.session_state["etap"] == "podsumowanie_coachingowe":
            if st.button("📋 Zakończ proces i przejdź do podsumowania"):
                st.session_state["kontynuuj_aktywny"] = False
                st.session_state["etap"] = "podsumowanie"
                st.rerun()


    if st.session_state["etap"] == "redukcja_do_10":
        if st.button(" ↩  Wróc"):
                st.session_state["etap"] = "wybor_wartosci"
                st.session_state["kontynuuj_aktywny"] = True
                st.rerun()

    if st.session_state["etap"] == "wybor_top_3":
        if st.button(" ↩  Wróc"):
                st.session_state["etap"] = "redukcja_do_10"
                st.session_state["kontynuuj_aktywny"] = True
                st.rerun()

    if st.session_state["etap"] == "coaching":
            if st.button(" ↩  Wróc"):
                    st.session_state["etap"] = "wybor_top_3"
                    st.session_state["coaching_index"]=0
                    st.session_state["kontynuuj_aktywny"] = True
                    st.rerun()

    st.markdown("---")
    st.markdown("---")



    if st.session_state["etap"] == "Intro":
        if "pokaz_logi" not in st.session_state:
            st.session_state["pokaz_logi"] = False

        
        if st.button(" Logi"):
        #    st.session_state["pokaz_logi"] = True
            st.session_state["pokaz_logi"] = not st.session_state.get("pokaz_logi", False)

        if st.session_state["pokaz_logi"]:

            if "raport_autoryzowany" not in st.session_state:
                st.session_state["raport_autoryzowany"] = False
            autoryzacja_do_raportow()
            if st.session_state["raport_autoryzowany"]:
                usun_raporty()
                panel_raportow()
                

            else:
                st.warning("🔒 Wprowadź poprawne dane logowania, aby uzyskać dostęp do raportów.")
