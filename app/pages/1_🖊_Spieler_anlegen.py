import streamlit as st
from db.database import get_session
from services.player_service import create_player

st.set_page_config(page_title="Spieler anlegen", page_icon="🖊")

st.title("Kicker Ranking")
st.header("Neuen Spieler anlegen")

player_name = st.text_input("Vorname des Spielers")
player_surname = st.text_input("Nachname des Spielers")

if st.button("Spieler erstellen"):
    if player_name and player_surname:
        with get_session() as session:
            player = create_player(player_name, player_surname)
            if player is None:
                st.error("Ein Spieler mit diesem Namen existiert bereits.")
            else:
                st.success(f"Spieler {player_name} {player_surname} wurde erstellt!")
    else:
        st.error("Bitte sowohl Vorname als auch Nachname eingeben.")