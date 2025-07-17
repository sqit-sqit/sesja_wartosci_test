import streamlit as st
from openai import OpenAI
from dotenv import dotenv_values


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

env = dotenv_values(".env")

# openai_client = OpenAI(api_key=env["OPENAI_API_KEY"])

def get_openai_client():
    return OpenAI(api_key=st.session_state["openai_api_key"])



def chatbot_reply(user_prompt, memory):
    # dodaj system message
    messages = [
        {
            "role": "system",
            "content": st.session_state["chatbot_personality"],
        },
    ]
    # dodaj wszystkie wiadomości z pamięci
    for message in memory:
        messages.append({"role": message["role"], "content": message["content"]})

    # dodaj wiadomość użytkownika
    messages.append({"role": "user", "content": user_prompt})

    response = openai_client.chat.completions.create(   # laczymy sie z open ai, z jego modelami zwiazanymi z czatem, dokladnie to z modelami ktore potrafia odpowiadac
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
        "content": response.choices[0].message.content,   # instrukcja ktorej trzeba uzyc by faktycznie wyciagnac te wiadomosc
        "usage": usage,
    }


def get_openai_client():
    return OpenAI(api_key=st.session_state["openai_api_key"])



# Main

st.title(":classical_building: Jakie są Twoje wartości zyciowe")

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


# --- Nowa sekcja: wartości użytkownika ---
if "user_values" not in st.session_state:
    st.session_state["user_values"] = []

if len(st.session_state["user_values"]) < 5:
    st.subheader("🎯 Jakie są Twoje 5 najważniejszych wartości?")
    value_input = st.text_input(f"Podaj wartość #{len(st.session_state['user_values']) + 1}")
    if value_input and value_input.strip():
        st.session_state["user_values"].append(value_input.strip())
        st.rerun()
    st.stop()
else:
    st.success("✅ Dziękuję! Twoje wartości zostały zapisane.")
    st.write("Twoje wartości:", ", ".join(st.session_state["user_values"]))

if "messages" not in st.session_state:   # sprawdzamy, czy lancuch messages nie jest w session state i jesli nie jest, to go dodajemy
    st.session_state["messages"] = []

for message in st.session_state["messages"]:    # wyswietla wszystkie messages dodane do session state wczesniej. Przeiteruj mi po wszystkich wiadomosciach ktore mamy w session state
    with st.chat_message(message["role"]):      # dodaj mi komponent chat_message 
        st.markdown(message["content"])         # tresc tej wiadomosci to ma byc cntent tego message



prompt = st.chat_input("O co chcesz spytać?")  # miejsce gdzie uzytkownicy moga wpisac pytanie
if prompt:                                         # jesli "prompt niepusty"
    with st.chat_message("user"):                   # to wyswietl go w okienku u gory, chat_message to komponent, "user" oznacza awatara
        st.markdown(prompt)

    st.session_state["messages"].append({"role": "user", "content": prompt})  # zbieramy te wiadomosci, tworzymy slownik, role - okresla kto stworzyl te wiadomosc

    with st.chat_message("assistant"):          # wyswietlanie okienka z wiadomoscia
        response = chatbot_reply(prompt, memory=st.session_state["messages"][-10:])
        st.markdown(response["content"])

    st.session_state["messages"].append({"role": "assistant", "content": response["content"], "usage": response["usage"]})  # tu dodajemy do session state response z chata


# Sidebar
with st.sidebar:
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

    st.session_state["chatbot_personality"] = st.text_area(
        "Opisz osobowość chatbota",
        max_chars=1000,
        height=200,
        value="""
Jesteś pomocnikiem, który odpowiada na wszystkie pytania użytkownika.
Odpowiadaj na pytania w sposób zwięzły i zrozumiały.
        """.strip()
    )
