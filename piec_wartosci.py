import streamlit as st
from pathlib import Path


def pobierz_liste_wartosci():
    """Wczytuje listę akceptowanych wartości z pliku tekstowego."""
    sciezka = Path("zyciowe_wartosci.txt")
    if not sciezka.exists():
        st.error("❌ Brakuje pliku: zyciowe_wartosci.txt")
        return []
    with open(sciezka, "r", encoding="utf-8") as f:
        return [linia.strip().lower() for linia in f.readlines() if linia.strip()]


def pobierz_wartosci_i_komentarze(openai_client, model="gpt-4o"):
    lista_dopuszczalnych = pobierz_liste_wartosci()

    if "user_values" not in st.session_state:
        st.session_state["user_values"] = []

    if "value_comments" not in st.session_state:
        st.session_state["value_comments"] = []

    if "last_entered_value" not in st.session_state:
        st.session_state["last_entered_value"] = ""
    if "last_generated_comment" not in st.session_state:
        st.session_state["last_generated_comment"] = ""

    if len(st.session_state["user_values"]) < 5:
        index = len(st.session_state["user_values"])
        st.subheader(f"🎯 Podaj wartość #{index+1} ze swoich 5 najważniejszych wartości")
        new_value = st.text_input("Twoja wartość", key="current_value_input")

        if st.button("✅ Zatwierdź wartość") and new_value.strip():
            cleaned_value = new_value.strip().lower()

            # 1. Czy wartość jest dokładnie w pliku?
            if cleaned_value in lista_dopuszczalnych:
                podobna = True
            else:
                # 2. Zapytaj OpenAI czy wartość ma zbliżone znaczenie do którejś z listy
                check_prompt = f"""
Sprawdź, czy wartość '{cleaned_value}' ma podobne znaczenie do którejkolwiek z poniższej listy wartości życiowych:
{', '.join(lista_dopuszczalnych)}

Odpowiedz tylko TAK lub NIE.
"""
                with st.spinner("🤖 Sprawdzam, czy wartość jest znana..."):
                    try:
                        response = openai_client.chat.completions.create(
                            model=model,
                            messages=[
                                {"role": "system", "content": "Jesteś ekspertem od języka i wartości. Odpowiadasz tylko TAK lub NIE."},
                                {"role": "user", "content": check_prompt},
                            ]
                        )
                        odpowiedz = response.choices[0].message.content.strip().lower()
                        podobna = "tak" in odpowiedz
                    except Exception as e:
                        podobna = True
                        st.warning(f"⚠️ Nie udało się sprawdzić podobieństwa: {e}")

            if not podobna:
                st.warning(f"🤔 Czy jesteś pewien, że wartość **{new_value.strip()}** jest poprawna?")
                if st.button("Tak, chcę ją dodać mimo wszystko", key="force_add"):
                    st.session_state["user_values"].append(new_value.strip())
                else:
                    st.stop()
            else:
                st.session_state["user_values"].append(new_value.strip())

            # Generuj komentarz
            with st.spinner("🧠 Generuję refleksję..."):
                try:
                    response = openai_client.chat.completions.create(
                        model=model,
                        messages=[
                            {
                                "role": "system",
                                "content": "Jesteś empatycznym mentorem wspierającym rozwój osobisty. Komentuj z czułością i inspiracją.",
                            },
                            {
                                "role": "user",
                                "content": f'Użytkownik wpisał wartość: "{new_value.strip()}". Skieruj do niego krótką refleksję lub zachętę, max 2 zdania.',
                            },
                        ]
                    )
                    comment = response.choices[0].message.content.strip()
                except Exception as e:
                    comment = f"Błąd pobierania komentarza: {e}"

            st.session_state["value_comments"].append(comment)
            st.session_state["last_entered_value"] = new_value.strip()
            st.session_state["last_generated_comment"] = comment

        # Pokaż ostatnio dodaną wartość
        if st.session_state["last_entered_value"]:
            st.markdown(f"**{len(st.session_state['user_values'])}. {st.session_state['last_entered_value']}**")
            st.caption(f"💬 {st.session_state['last_generated_comment']}")

        st.stop()

    else:
        st.success("✅ Podałeś wszystkie 5 wartości. Poniżej podsumowanie:")
        for i, val in enumerate(st.session_state["user_values"]):
            st.markdown(f"**{i+1}. {val}**")
            if i < len(st.session_state["value_comments"]):
                st.caption(f"💬 {st.session_state['value_comments'][i]}")
