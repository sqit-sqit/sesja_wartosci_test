import streamlit as st
from openai import OpenAI
from pathlib import Path


def wczytaj_szablony(plik="szablony_coachingowe.txt"):
    sciezka = Path(plik)
    if not sciezka.exists():
        return []
    with open(sciezka, "r", encoding="utf-8") as f:
        return [linia.strip() for linia in f if linia.strip()]
    
def wczytaj_osobowosc(path="chatbot_personality_coach.txt", wartosc="", prompt_szablonowy=""):
    if not Path(path).exists():
        return "Jesteś empatycznym coachem."  # fallback

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        return content.format(wartosc=wartosc, prompt_szablonowy=prompt_szablonowy)

def coaching_dla_wartosci(api_key: str):
    client = OpenAI(api_key=api_key)

    with st.expander("👉 Kliknij, by schować lub rozwiniąć tę sekcję", expanded=True):
        st.markdown(f"""
        Pozwól sobie teraz na głębszą reflekeję nad wybraną wartością.
        Dlaczego została wybrana?
        Jak wpływa na Twoje wybory i decyzjie?
        Na ile możesz ją realizować w swoim życiu?  
        Gdy poczujesz, że refleksja na temat danej wartości już się wyczerpała,
        możesz przejść do podsumowania.
        """)
    # st.title("🧭 Porozmawiajmy o Twoich wartościach")
    wartosci = st.session_state.get("user_values", [])
    if len(wartosci) == 0:
        st.warning("Ten etap wymaga przynajmniej jednej wybranej wartości.")
        return
    if "coaching_index" not in st.session_state:
        st.session_state["coaching_index"] = 0
        st.session_state["coaching_chat"] = {}
    index = st.session_state["coaching_index"]
    wartosc = wartosci[index]
    st.subheader(f"🌀 Wartość #{index+1}:   **{wartosc}**")

    # Przejście do kolejnej wartości
    st.markdown("---")
    # if index < 2:
    if index < len(wartosci)-1:
        st.session_state["kontynuuj_aktywny"] = False
        if st.button("➡️ Przejdź do kolejnej wartości"):
           st.session_state["coaching_index"] += 1
           st.rerun()
    else:
        st.session_state["kontynuuj_aktywny"] = True
        # if st.button("📋 Zakończ proces i przejdź do podsumowania"):
        #     st.session_state["etap"] = "podsumowanie"
        #     st.rerun()


    # Inicjalizacja historii czatu
    if wartosc not in st.session_state["coaching_chat"]:
        szablony = wczytaj_szablony()
        prompt_szablonowy = "\n".join(szablony) if szablony else ""

        osobowosc = wczytaj_osobowosc(
            path="chatbot_personality_coach.txt",
            wartosc=wartosc,
            prompt_szablonowy=prompt_szablonowy
        )




        st.session_state["coaching_chat"][wartosc] = [
            {
                "role": "system",
                "content": osobowosc
                # "content": (
                #     f"Jesteś empatycznym i pogłębiającym coachem. "
                #     f"Pomagasz użytkownikowi odkrywać znaczenie jego wartości: **{wartosc}**.\n"
                #     f"Stosuj pytania podobne do poniższych (ale nie dosłownie):\n{prompt_szablonowy}\n"
                #     f"Pytaj, pogłębiaj, zachęcaj do refleksji. Unikaj ocen. "
                #     f"Skup się na tym, co jest naprawdę ważne dla użytkownika."
                #     f"Zacznij od dociekania, dlaczego taka wartosść została wybrana."
                #     f"Zmierzaj do pytań, jakie kroki uytkownik chciałbym podjąć by wzmocnić lub utrzymać realizację wdanej wartości w zyciu."
                #     f"Jeśli wyczujesz, e uytkownik zdawkowo odpowiada na pytania i nie chce dalej pogłębiać wartości, spytaj, czy chce przejść do kolejnej wartości."
                # )
            }
        ]
        # AI zadaje pierwsze pytanie automatycznie
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state["coaching_chat"][wartosc]
        )
        first_question = response.choices[0].message.content.strip()
        st.session_state["coaching_chat"][wartosc].append({"role": "assistant", "content": first_question})
        # Zapisz tylko usage (do liczenia kosztu)
        if "messages" not in st.session_state:
            st.session_state["messages"] = []
        if response.usage:
            st.session_state["messages"].append({
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            })
    # Wyświetlenie historii czatu
    for msg in st.session_state["coaching_chat"][wartosc]:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    # Input użytkownika
    user_input = st.chat_input(f"Rozmawiaj o wartości: {wartosc}")
    if user_input:
        st.session_state["coaching_chat"][wartosc].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state["coaching_chat"][wartosc]
            )
            ai_msg = response.choices[0].message.content.strip()
            st.markdown(ai_msg)
        # Zapisz w historii tej wartości
        st.session_state["coaching_chat"][wartosc].append({"role": "assistant", "content": ai_msg})
        # Zapisz tylko usage (do licznika kosztów)
        if "messages" not in st.session_state:
            st.session_state["messages"] = []
        if response.usage:
            st.session_state["messages"].append({
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            })
