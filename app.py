
import streamlit as st
from openai import OpenAI
from dotenv import dotenv_values
import os

# import modułów
from pokaz_losowe_wartosci import pokaz_losowe_wartosci_animowane
from redukcja import redukuj_wartosci
from etap_postepu import pokaz_pasek_postepu
from coaching_dla_wartosci import coaching_dla_wartosci
from intro import pokaz_intro
from podsumowanie import pokaz_podsumowanie

#raporty
from panel_raportow import panel_raportow

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
MODEL = "gpt-4o"
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
    redukuj_wartosci(limit=10, nastepny_etap="redukcja_do_3", komunikat="Usuń wartości, aż zostanie ich tylko 10.")

elif st.session_state["etap"] == "redukcja_do_3":
    redukuj_wartosci(limit=3, nastepny_etap="coaching", komunikat="Usuń wartości, aż zostaną tylko 3.")

elif st.session_state["etap"] == "coaching":
    coaching_dla_wartosci(api_key=st.session_state["openai_api_key"])


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
    st.markdown(
        f"<div style='font-size: 1.1rem; margin-bottom: 1rem;'>🔢 Wybranych wartości: <b>{liczba_wartosci}</b></div>",
        unsafe_allow_html=True
    )

    wartosci = st.session_state["user_values"]
    kol1, kol2 = st.columns(2)
    for i, val in enumerate(wartosci.copy()):
        kol = kol1 if i % 2 == 0 else kol2
        with kol:
            usun = st.button(f"× {val}", key=f"usun_sidebar_{val}")
            if usun:
                wartosci.remove(val)
                st.session_state["last_deleted"] = val
                st.rerun()


# poprzedni wygląd wybranych wartości

    # col1, col2 = st.columns(2)
    # for i, val in enumerate(st.session_state["user_values"]):
    #     col = col1 if i % 2 == 0 else col2
    #     with col:
    #         inner_cols = st.columns([5, 1])
    #         with inner_cols[0]:
    #             st.markdown(f"<div style='padding: 4px 0px;'>✅ <b>{val}</b></div>", unsafe_allow_html=True)
    #         with inner_cols[1]:
    #             if st.button("×", key=f"delete_{val}", help=f"Usuń wartość: {val}"):
    #                 st.session_state["last_deleted"] = val
    #                 st.session_state["user_values"].remove(val)
    #                 st.rerun()

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

    # c0, c1 = st.columns(2)
    # with c0:
    #     st.metric("Koszt rozmowy (USD)", f"${total_cost:.4f}")
    # with c1:
    #     st.metric("Koszt rozmowy (PLN)", f"{total_cost * USD_TO_PLN:.4f}")

#     default_personality = f"""
# Jesteś ciepłym, empatycznym i wspierającym agentem rozwojowym.
# Pomagasz użytkownikowi kierować się jego wartościami: {', '.join(st.session_state.get('user_values', []))}.
# Odpowiadasz jasno, inspirująco i z szacunkiem. Pomagasz działać zgodnie z tym, co ważne.
# """.strip()
#     st.session_state["chatbot_personality"] = st.text_area(
#         "🧠 Osobowość chatbota",
#         max_chars=1000,
#         height=200,
#         value=default_personality
#     )

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
                st.session_state["etap"] = "redukcja_do_3"
                st.session_state["kontynuuj_aktywny"] = False
                st.rerun()
            

        elif st.session_state["etap"] == "redukcja_do_3":
            if st.button("✅ Kontunuuj"):
                st.session_state["etap"] = "coaching"
                st.session_state["kontynuuj_aktywny"] = False
                st.rerun()
  

        elif st.session_state["etap"] == "coaching":
            if st.button("📋 Zakończ proces i przejdź do podsumowania"):
                st.session_state["kontynuuj_aktywny"] = False
                st.session_state["etap"] = "podsumowanie"
                st.rerun()


    if st.session_state["etap"] == "redukcja_do_10":
        if st.button(" ↩  Wróc"):
                st.session_state["etap"] = "wybor_wartosci"
                st.session_state["kontynuuj_aktywny"] = True
                st.rerun()

    if st.session_state["etap"] == "redukcja_do_3":
        if st.button(" ↩  Wróc"):
                st.session_state["etap"] = "redukcja_do_10"
                st.session_state["kontynuuj_aktywny"] = True
                st.rerun()

    if st.session_state["etap"] == "coaching":
            if st.button(" ↩  Wróc"):
                    st.session_state["etap"] = "redukcja_do_3"
                    st.session_state["coaching_index"]=0
                    st.session_state["kontynuuj_aktywny"] = True
                    st.rerun()

    # st.subheader( st.session_state["kontynuuj_aktywny"])
    # st.subheader(st.session_state["coaching_index"])

    st.markdown("---")
    st.markdown("---")

    
    # if st.button(" Logi"):
    if "raport_autoryzowany" not in st.session_state:
        st.session_state["raport_autoryzowany"] = False

    autoryzacja_do_raportow()

    if st.session_state["raport_autoryzowany"]:
        panel_raportow()
    else:
        st.warning("🔒 Wprowadź poprawne dane logowania, aby uzyskać dostęp do raportów.")


    # if st.button(" 🧾  Logs"):
    #     panel_raportow()
