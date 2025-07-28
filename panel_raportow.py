import streamlit as st
from pathlib import Path

def panel_raportow(folder_path="podsumowania"):
    st.title("📁 Panel Raportów z Sesji")
    st.markdown("Tutaj możesz przeglądać i pobierać zapisane raporty tekstowe z sesji coachingowych.")

    katalog = Path(folder_path)
    if not katalog.exists():
        st.warning(f"Katalog `{folder_path}` nie istnieje.")
        return

    pliki_txt = sorted(katalog.glob("*.txt"), reverse=True)

    if not pliki_txt:
        st.info("Brak dostępnych raportów.")
        return

    for plik in pliki_txt:
        with open(plik, "rb") as f:
            st.download_button(
                label=f"⬇️ Pobierz: {plik.name}",
                data=f,
                file_name=plik.name,
                mime="text/plain"  # ← zmieniony MIME
            )
