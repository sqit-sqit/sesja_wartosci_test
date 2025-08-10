
from pathlib import Path


def wczytaj_osobowosc(path="chatbot_personality_coach.txt", wartosc="", prompt_szablonowy=""):
    if not Path(path).exists():
        return "Jesteś empatycznym coachem."
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        return content.format(wartosc=wartosc, prompt_szablonowy=prompt_szablonowy)

def wczytaj_szablony(plik="pytania_poglebiajace.txt"):
    sciezka = Path(plik)
    if not sciezka.exists():
        return []
    with open(sciezka, "r", encoding="utf-8") as f:
        return [linia.strip() for linia in f if linia.strip()]
    

