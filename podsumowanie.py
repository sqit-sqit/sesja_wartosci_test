import streamlit as st
from openai import OpenAI
from datetime import datetime
from pathlib import Path

def pokaz_podsumowanie(api_key, pricing, usd_to_pln):
    st.header("📄 Podsumowanie Twojej sesji")

    user_values = st.session_state.get("user_values", [])
    top_10 = st.session_state.get("top_10", [])
    top_3 = st.session_state.get("top_3", [])
    coaching_messages = st.session_state.get("coaching_messages", [])
    podsumowanie_messages = st.session_state.get("podsumowanie_messages", [])

    # Oblicz koszt
    koszt_usd = 0.0
    for m in coaching_messages + podsumowanie_messages:
        if "usage" in m:
            koszt_usd += m["usage"]["prompt_tokens"] * pricing["input_tokens"]
            koszt_usd += m["usage"]["completion_tokens"] * pricing["output_tokens"]

    # Stwórz podsumowanie z AI
    client = OpenAI(api_key=api_key)

    prompt = (
        f"Użytkownik zdefiniował następujące wartości: {', '.join(top_3)}.\n"
        f"Na podstawie wcześniejszej rozmowy wygeneruj podsumowanie sesji coachingowej: \n"
        f"- Co było ważne dla użytkownika\n"
        f"- Jakie wartości się ujawniły\n"
        f"- Jakie działania użytkownik może podjąć dalej\n"
        f"Zakończ inspirującym przesłaniem."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Jesteś doświadczonym coachem piszącym podsumowanie sesji rozwojowej."},
            {"role": "user", "content": prompt}
        ]
    )

    summary = response.choices[0].message.content
    usage = response.usage
    podsumowanie_messages.append({"role": "assistant", "content": summary, "usage": usage})

    st.markdown("### 🧾 Podsumowanie wygenerowane przez AI")
    st.markdown(summary)

    # Zapisz wszystko do pliku
    lines = []
    lines.append("🟢 Wszystkie wartości wybrane przez użytkownika:\n" + ", ".join(user_values) + "\n")
    lines.append("🔟 Wybrane 10 najważniejszych wartości:\n" + ", ".join(top_10) + "\n")
    lines.append("🔴 Wybrane 3 kluczowe wartości:\n" + ", ".join(top_3) + "\n")

    lines.append("\n📚 Historia rozmów coachingowych:\n")
    for msg in coaching_messages:
        if "content" in msg:
            lines.append(f"{msg['role'].upper()}: {msg['content']}\n")

    lines.append("\n📄 Podsumowanie AI:\n" + summary + "\n")
    lines.append(f"💰 Koszt sesji: {koszt_usd:.4f} USD ({koszt_usd * usd_to_pln:.2f} PLN)\n")

    filename = f"podsumowanie_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = Path("podsumowania") / filename
    filepath.parent.mkdir(exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    st.success(f"✅ Podsumowanie zapisane jako `{filename}` w folderze `podsumowania/`.")
