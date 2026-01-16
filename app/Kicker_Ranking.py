from db.database import init_db
import streamlit as st
from services.player_service import get_all_players
from services.match_service import create_match
from services.leaderboard import get_leaderboard_df

# Initalisiere die Datenbank
@st.cache_resource
def initialize_database():
    init_db()

@st.cache_data
def load_players():
    return get_all_players()

@st.cache_data(ttl=60)
def load_leaderboard():
    return get_leaderboard_df()


initialize_database()
st.set_page_config(page_title="Kicker Ranking", page_icon="🏆")

# Streamlit UI 
st.title("Kicker Ranking")
st.write("Bitte trage hier den Matchergebnis ein. Wenn dein Spieler noch nicht existiert, kannst du ihn unter 'Spieler anlegen' erstellen.")

players = load_players()

team_black = st.multiselect(
    "Spieler Team Schwarz",
    options=players,
    format_func=lambda p: f"{p.name} {p.surname}",
    max_selections=2
)

team_grey = st.multiselect(
    "Spieler Team Grau",
    options=players,
    format_func=lambda p: f"{p.name} {p.surname}",
    max_selections=2
)

winner = st.selectbox("Gewinner", ("Team Schwarz", "Team Grau"), index=None)
goals_looser = st.number_input("Tore Verlierer", min_value=0, step=1)

if st.button("Match speichern"):
    if winner is None:
        st.warning("Bitte Gewinner auswählen")
        st.stop()

    goals_black, goals_grey = (
        (10, goals_looser) if winner == "Team Schwarz"
        else (goals_looser, 10)
    )

    create_match(
        goals_schwarz=goals_black,
        goals_grau=goals_grey,
        team_schwarz_ids=[p.id for p in team_black],
        team_grau_ids=[p.id for p in team_grey],
    )

    st.success("Match gespeichert")

st.header("Leaderboard")
leaderboard_df = load_leaderboard()
st.dataframe(leaderboard_df)