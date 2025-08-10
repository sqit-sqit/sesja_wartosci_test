import streamlit as st
from openai import OpenAI
from datetime import datetime
from pathlib import Path

def pokaz_podsumowanie(api_key: str, model: str, pricing=None, usd_to_pln=4.0):
    
    
    st.title("📘 Podsumowanie sesji")

    top_3 = st.session_state.get("top_3", [])
    coaching_top_3 = st.session_state.get("coaching_top_3", {})
    podsumowanie_chat = st.session_state.get("podsumowanie_chat", [])

    if not top_3 or not coaching_top_3 or not podsumowanie_chat:
        st.warning("Brakuje danych do wygenerowania pełnego podsumowania.")
        return

    # Połączenie dialogów
    tresc_rozmowy_top3 = ""
    for wartosc in top_3:
        messages = coaching_top_3.get(wartosc, [])
        tresc_rozmowy_top3 += f"\n🌀 Wartość: {wartosc}\n"
        for m in messages:
            if m["role"] in ["user", "assistant"]:
                rola = "Ty" if m["role"] == "user" else "Coach AI"
                tresc_rozmowy_top3 += f"{rola}: {m['content']}\n"

    tresc_podsumowanie_chat = "\n🧠 Sesja podsumowująca:\n"
    for m in podsumowanie_chat:
        if m["role"] in ["user", "assistant"]:
            rola = "Ty" if m["role"] == "user" else "Coach AI"
            tresc_podsumowanie_chat += f"{rola}: {m['content']}\n"

    # Prompt
    prompt = (
        f"Użytkownik wybrał trzy kluczowe wartości: {', '.join(top_3)}.\n\n"
        f"Poniżej znajduje się zapis rozmów coachingowych dla każdej z wartości:\n"
        f"{tresc_rozmowy_top3}\n\n"
        f"Oraz zapis sesji podsumowującej:\n{tresc_podsumowanie_chat}\n\n"
        f"Na podstawie tych rozmów wygeneruj:\n"
        f"- Krótkie przypomnienie 3 wartości,\n"
        f"- skieruj do użytkownika Osobne podsumowanie rozmowy dla każdej wartości,\n"
        f"- Skieruj do użytkownika syntetyczną listę możliwych działań wypowiedzianych lub sugerowanych przez użytkownika,\n"
        f"- skieruj do użytkownika Refleksje i przesłanie końcowe dla użytkownika.\n\n"
        f"Zachowaj wspierający, ciepły i inspirujący ton."
    )

    client = OpenAI(api_key=api_key)
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

    st.session_state["podsumowanie"] = podsumowanie
    if "podsumowanie_messages" not in st.session_state:
        st.session_state["podsumowanie_messages"] = []
    st.session_state["podsumowanie_messages"].append({
        "role": "assistant",
        "content": podsumowanie,
        "usage": usage
    })

    # Wyświetl
    st.markdown("### ✨ Podsumowanie naszej sesji")
    st.markdown(podsumowanie)

    # Koszt sesji
    total_cost_usd = 0.0
    for message in st.session_state.get("messages", []):
        if "usage" in message:
            u = message["usage"]
            total_cost_usd += u["prompt_tokens"] * pricing["input_tokens"]
            total_cost_usd += u["completion_tokens"] * pricing["output_tokens"]
    total_cost_pln = total_cost_usd * usd_to_pln

    st.markdown(f"💰 **Koszt sesji:** `{total_cost_usd:.4f} USD` (`{total_cost_pln:.2f} PLN`)")

    # Zapisz do pliku
    folder = Path("podsumowania")
    folder.mkdir(exist_ok=True)
    filename = f"podsumowanie_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = folder / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("🔴 Trzy najważniejsze wartości:\n")
        f.write(", ".join(top_3) + "\n\n")
        f.write("📚 Rozmowy coachingowe:\n")
        f.write(tresc_rozmowy_top3 + "\n")
        f.write("🧠 Sesja podsumowująca:\n")
        f.write(tresc_podsumowanie_chat + "\n")
        f.write("✨ Podsumowanie AI:\n")
        f.write(podsumowanie + "\n")
        f.write(f"💰 Koszt sesji: {total_cost_usd:.4f} USD ({total_cost_pln:.2f} PLN)\n")
        f.write(f"🔴 Model: {model}\n")

    st.success(f"✅ Podsumowanie zapisane jako `{filename}` w folderze `podsumowania/`.")
