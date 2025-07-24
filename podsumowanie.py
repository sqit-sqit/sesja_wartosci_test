# podsumowanie.py

import streamlit as st
from openai import OpenAI

def pokaz_podsumowanie(api_key):
    st.title("📘 Podsumowanie Twojego procesu")

    user_values = st.session_state.get("user_values", [])[:3]  # ostatnie 3 najważniejsze wartości
    if not user_values:
        st.warning("Brak wystarczającej liczby wartości do podsumowania.")
        return

    st.markdown("#### 🌟 Twoje trzy najważniejsze wartości:")
    for val in user_values:
        st.markdown(f"- **{val}**")

    # System prompt do AI
    system_prompt = (
        "Jesteś doświadczonym coachem i mentorem. "
        "Użytkownik zakończył głęboki proces refleksji i odkrywania wartości. "
        f"Jego trzy najważniejsze wartości to: {', '.join(user_values)}.\n\n"
        "Napisz empatyczne i inspirujące podsumowanie, które wzmacnia jego wybory i dodaje otuchy. "
        "Zaproponuj konkretne działania (action items), które pomogą mu wdrożyć te wartości w codzienne życie."
    )

    # Inicjalizacja klienta
    client = OpenAI(api_key=api_key)

    with st.spinner("AI tworzy dla Ciebie podsumowanie..."):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Proszę o podsumowanie mojego procesu i konkretne działania."}
            ]
        )

    output = response.choices[0].message.content
    usage = response.usage

    # Zapis do historii i kosztów
    st.session_state["messages"].append({
        "role": "assistant",
        "content": output,
        "usage": {
            "completion_tokens": usage.completion_tokens,
            "prompt_tokens": usage.prompt_tokens,
            "total_tokens": usage.total_tokens
        }
    })

    # Wyświetlenie
    st.markdown("---")
    st.markdown(output)
