import streamlit as st
from openai import OpenAI
from dotenv import dotenv_values

# import modułów

from pokaz_losowe_wartosci import pokaz_losowe_wartosci_animowane
from redukcja import redukuj_wartosci
from etap_postepu import pokaz_pasek_postepu

# from coaching_dla_wartosci import coaching_dla_wartosci
# from podsumowanie import pokaz_podsumowanie


model_pricings = {
    "gpt-4o": {
        "input_tokens": 5.00 / 1_000_000,  # per token
        "output_tokens": 15.00 / 1_000_000,  # per token
    },
    "gpt-4o-mini": {
        "input_tokens": 0.150 / 1_000_000,  # per token
        "output_tokens": 0.600 / 1_000_000,  # per token
    }
}
MODEL = "gpt-4o"
USD_TO_PLN = 3.97
PRICING = model_pricings[MODEL]
LICZBA_WARTOSCI = 10  # <-- możesz tu ustawić dowolną wartość


env = dotenv_values(".env")

# openai_client = OpenAI(api_key=env["OPENAI_API_KEY"])

def get_openai_client():
    return OpenAI(api_key=st.session_state["openai_api_key"])

# new chatbot reply
def chatbot_reply(user_prompt, memory):
    # Dołącz wartości użytkownika do system promptu
    user_values = st.session_state.get("user_values", [])
    values_text = ", ".join(user_values) if user_values else "nieokreślone wartości"
    system_prompt = (
        st.session_state["chatbot_personality"].strip()
        + f"\n\nWartości użytkownika to: {values_text}. "
        + "Zawsze odpowiadaj w sposób wspierający, uwzględniający te wartości."
    )

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
    ]
    
    for message in memory:
        messages.append({"role": message["role"], "content": message["content"]})

    messages.append({"role": "user", "content": user_prompt})

    client = get_openai_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    usage = {}
    if response.usage:
        usage = {
            "completion_tokens": response.usage.completion_tokens,
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        }

    return {
        "role": "assistant",
        "content": response.choices[0].message.content,
        "usage": usage,
    }



# OpenAI API key protection
if not st.session_state.get("openai_api_key"):
    if "OPENAI_API_KEY" in env:
        st.session_state["openai_api_key"] = env["OPENAI_API_KEY"]

    else:
        st.info("Dodaj swój klucz API OpenAI aby móc korzystać z tej aplikacji")
        st.session_state["openai_api_key"] = st.text_input("Klucz API", type="password")
        if st.session_state["openai_api_key"]:
            st.rerun()

if not st.session_state.get("openai_api_key"):
    st.stop()

openai_client = get_openai_client()


# Ustawienie domyślnego etapu
if "etap" not in st.session_state:
    st.session_state["etap"] = "wybor_wartosci"

st.title(":classical_building: Moje Osobiste Wartości")
pokaz_pasek_postepu()

# Główna logika krok po kroku
if st.session_state["etap"] == "wybor_wartosci":
    pokaz_losowe_wartosci_animowane()
    if st.button("✅ Mam już wystarczająco wartości"):
        st.session_state["etap"] = "redukcja_do_10"
        st.rerun()

elif st.session_state["etap"] == "redukcja_do_10":
    # pokaz_losowe_wartosci_animowane()
    # print("drugi")
    # if st.button("✅ To jest tych 10 wartości"):
    #     st.session_state["etap"] = "top_3"
    #     st.rerun()
    redukuj_wartosci(limit=10, nastepny_etap="redukcja_do_3", komunikat="Usuń wartości, aż zostanie ich tylko 10.")

elif st.session_state["etap"] == "redukcja_do_3":
    # pokaz_losowe_wartosci_animowane()
    # if st.button("✅ To są moje 3 najwaniejsze wartości"):
    #     st.session_state["etap"] = "redukcja_do_10"
    #     st.rerun()
    redukuj_wartosci(limit=3, nastepny_etap="coaching", komunikat="Usuń wartości, aż zostaną tylko 3.")




if st.session_state.get("rerun"):
    st.session_state["rerun"] = False
    st.rerun()


if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("O co chcesz spytać?")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        response = chatbot_reply(prompt, memory=st.session_state["messages"][-10:])
        st.markdown(response["content"])

    st.session_state["messages"].append({"role": "assistant", "content": response["content"], "usage": response["usage"]})




with st.sidebar:
    st.header("🎯 Twoje wartości")

    # Inicjalizacja listy
    if "user_values" not in st.session_state:
        st.session_state["user_values"] = []

    liczba_wartosci = len(st.session_state["user_values"])

    # 🔢 Licznik wybranych wartości
    st.markdown(
        f"<div style='font-size: 1.1rem; margin-bottom: 1rem;'>🔢 Wybranych wartości: <b>{liczba_wartosci}</b></div>",
        unsafe_allow_html=True
    )

    # Układ wartości w dwóch kolumnach z przyciskiem usuwania
    col1, col2 = st.columns(2)
    for i, val in enumerate(st.session_state["user_values"]):
        col = col1 if i % 2 == 0 else col2
        with col:
            inner_cols = st.columns([5, 1])
            with inner_cols[0]:
                st.markdown(f"<div style='padding: 4px 0px;'>✅ <b>{val}</b></div>", unsafe_allow_html=True)
            with inner_cols[1]:
                if st.button("×", key=f"delete_{val}", help=f"Usuń wartość: {val}"):
                    st.session_state["last_deleted"] = val
                    st.session_state["user_values"].remove(val)
                    st.rerun()

    # 🔁 Przywrócenie ostatnio usuniętej wartości
    if "last_deleted" in st.session_state:
        if st.button("↩️ Przywróć ostatnio usuniętą"):
            val = st.session_state.pop("last_deleted")
            if val not in st.session_state["user_values"]:
                st.session_state["user_values"].append(val)
                st.rerun()

    st.markdown("---")

    # Koszty tokenów
    total_cost = 0
    for message in st.session_state.get("messages") or []:
        if "usage" in message:
            total_cost += message["usage"]["prompt_tokens"] * PRICING["input_tokens"]
            total_cost += message["usage"]["completion_tokens"] * PRICING["output_tokens"]

    c0, c1 = st.columns(2)
    with c0:
        st.metric("Koszt rozmowy (USD)", f"${total_cost:.4f}")
    with c1:
        st.metric("Koszt rozmowy (PLN)", f"{total_cost * USD_TO_PLN:.4f}")

    # Edytowalna osobowość chatbota
    default_personality = f"""
Jesteś ciepłym, empatycznym i wspierającym agentem rozwojowym.
Pomagasz użytkownikowi kierować się jego wartościami: {', '.join(st.session_state.get('user_values', []))}.
Odpowiadasz jasno, inspirująco i z szacunkiem. Pomagasz działać zgodnie z tym, co ważne.
""".strip()

    st.session_state["chatbot_personality"] = st.text_area(
        "🧠 Osobowość chatbota",
        max_chars=1000,
        height=200,
        value=default_personality
    )
