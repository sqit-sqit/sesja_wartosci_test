import streamlit as st
from openai import OpenAI
from datetime import datetime
from pathlib import Path


def pokaz_podsumowanie(api_key: str, model: str = "gpt-4o"):
    st.title("📘 Podsumowanie sesji")

    top_3 = st.session_state.get("user_values", [])
    coaching_chat = st.session_state.get("coaching_chat", {})

    if len(top_3) != 3 or not coaching_chat:
        st.warning("Brakuje danych do wygenerowania podsumowania. Upewnij się, że ukończyłeś etap coachingu.")
        return

    client = OpenAI(api_key=api_key)

    # Kompilacja rozmów coachingowych
    tresc_rozmowy = ""
    for wartosc in top_3:
        messages = coaching_chat.get(wartosc, [])
        tresc_rozmowy += f"\n🌀 Wartość: {wartosc}\n"
        for m in messages:
            if m["role"] in ["user", "assistant"]:
                rola = "Ty" if m["role"] == "user" else "Coach AI"
                tresc_rozmowy += f"{rola}: {m['content']}\n"
                # st.info(tresc_rozmowy)

    # Prompt do AI podsumowujący sesję
    prompt = (
        f"Użytkownik wybrał trzy kluczowe wartości: {', '.join(top_3)}.\n\n"
        f"Poniżej znajduje się zapis rozmów coachingowych dla każdej z wartości:\n{tresc_rozmowy}\n\n"
        f"Na podstawie tych rozmów wygeneruj:\n"
        f"- Krótkie przypomnienie 3 wartości,\n"
        f"- Osobne podsumowanie rozmowy dla każdej wartości,\n"
        f"- Syntetyczną listę możliwych działań („action items”) wypowiedzianych lub sugerowanych przez użytkownika,\n"
        f"- Refleksje i przesłanie końcowe dla użytkownika, które pomoże mu dalej kroczyć drogą zgodną z wartościami.\n\n"
        f"Zachowaj wspierający, ciepły i inspirujący ton wypowiedzi."
    )

    # Wygeneruj podsumowanie
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Jesteś doświadczonym coachem, który potrafi podsumować sesję coachingową w sposób klarowny i inspirujący."
            },
            {"role": "user", "content": prompt}
        ]
    )

    podsumowanie = response.choices[0].message.content.strip()
    usage = response.usage

    # Zapisz do sesji
    if "podsumowanie_messages" not in st.session_state:
        st.session_state["podsumowanie_messages"] = []
    st.session_state["podsumowanie_messages"].append({
        "role": "assistant",
        "content": podsumowanie,
        "usage": usage
    })
    st.session_state["podsumowanie"] = podsumowanie

    # Wyświetlenie na ekranie
    st.markdown("### ✨ Podsumowanie AI")
    st.markdown(podsumowanie)

    # Zapisz do pliku tekstowego
    folder = Path("podsumowania")
    folder.mkdir(exist_ok=True)
    filename = f"podsumowanie_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = folder / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("🔴 Trzy najważniejsze wartości:\n")
        f.write(", ".join(top_3) + "\n\n")
        f.write("📚 Rozmowy coachingowe:\n")
        f.write(tresc_rozmowy + "\n")
        f.write("🧠 Podsumowanie AI:\n")
        f.write(podsumowanie + "\n")

    st.success(f"✅ Podsumowanie zapisane jako `{filename}` w folderze `podsumowania/`.")
