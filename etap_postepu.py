import streamlit as st

def pokaz_pasek_postepu():
    ETAPY = [
        "Intro",
        "wybor_wartosci",
        "redukcja_do_10",
        "redukcja_do_3",
        "coaching",
        "podsumowanie"
    ]

    ETAP_OPIS = {
        "Intro": "Intro",
        "wybor_wartosci": "Wybór wartości",
        "redukcja_do_10": "Redukcja do 10",
        "redukcja_do_3": "Redukcja do 3",
        "coaching": "Coaching",
        "podsumowanie": "Podsumowanie"
    }

    aktualny = st.session_state.get("etap", "Intro")
    aktualny_index = ETAPY.index(aktualny)

    # Styl CSS
    st.markdown("""
    <style>
    .progress-container {
        display: flex;
        justify-content: space-between;
        margin: 20px 0 30px 0;
    }
    .step {
        flex-grow: 1;
        text-align: center;
        position: relative;
        font-size: 0.9rem;
        color: #bbb;
    }
    .step.active {
        color: #2d98da;
        font-weight: bold;
    }
    .step.done {
        color: #2ecc71;
        font-weight: bold;
    }
    .step::before {
        content: '';
        position: absolute;
        top: 14px;
        left: 50%;
        transform: translateX(-50%);
        height: 14px;
        width: 14px;
        border-radius: 50%;
        background-color: #ccc;
        z-index: 2;
    }
    .step.active::before {
        background-color: #2d98da;
    }
    .step.done::before {
        background-color: #2ecc71;
    }
    .step::after {
        content: '';
        position: absolute;
        top: 20px;
        left: 50%;
        height: 4px;
        width: 100%;
        background-color: #ccc;
        z-index: 1;
        transform: translateX(0%);
    }
    .step:last-child::after {
        display: none;
    }
    .step.done::after {
        background-color: #2ecc71;
    }
    </style>
    """, unsafe_allow_html=True)

    # Generowanie HTML paska
    html = '<div class="progress-container">'
    for i, etap in enumerate(ETAPY):
        class_name = ""
        if i < aktualny_index:
            class_name = "step done"
        elif i == aktualny_index:
            class_name = "step active"
        else:
            class_name = "step"

        html += f'<div class="{class_name}">{ETAP_OPIS[etap]}</div>'
    html += '</div>'

    st.markdown(html, unsafe_allow_html=True)
