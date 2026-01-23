import pandas as pd
from sqlmodel import select
from sqlalchemy.sql import func, case
from db.database import get_session
from streamlit import cache_data

from db.models import Player, MatchPlayer, Matches, TeamEnum

@cache_data(ttl=60)
def get_leaderboard_df() -> pd.DataFrame:
    with get_session() as session:

        # -----------------------------
        # Tore FÜR Spieler
        # -----------------------------
        goals_for = case(
            (MatchPlayer.team == TeamEnum.TEAM_SCHWARZ, Matches.goals_schwarz),
            else_=Matches.goals_grau,
        )

        # -----------------------------
        # Tore GEGEN Spieler
        # -----------------------------
        goals_against = case(
            (MatchPlayer.team == TeamEnum.TEAM_SCHWARZ, Matches.goals_grau),
            else_=Matches.goals_schwarz,
        )

        # -----------------------------
        # Sieg (1 = gewonnen, 0 = verloren)
        # -----------------------------
        wins = case(
            (
                (MatchPlayer.team == TeamEnum.TEAM_SCHWARZ)
                & (Matches.goals_schwarz > Matches.goals_grau),
                1,
            ),
            (
                (MatchPlayer.team == TeamEnum.TEAM_GRAU)
                & (Matches.goals_grau > Matches.goals_schwarz),
                1,
            ),
            else_=0,
        )
        # -----------------------------
        # Spiel gezählt (immer 1)
        # -----------------------------

        games_played = func.count(Matches.id)

        # -----------------------------
        # SQLModel Select
        # -----------------------------
        stmt = (
            select(
                Player.name.label("Vorname"),
                Player.surname.label("Nachname"),
                games_played.label("Spiele"),
                func.sum(wins).label("Siege"),
                func.sum(goals_for).label("Tore"),
                func.sum(goals_against).label("Gegentore"),
            )
            .join(MatchPlayer, MatchPlayer.player_id == Player.id)
            .join(Matches, Matches.id == MatchPlayer.match_id)
            .group_by(Player.id, Player.name, Player.surname)
            .order_by(func.sum(wins).desc())
        )

        rows = session.exec(stmt).all()

    df = pd.DataFrame(rows)

    # -----------------------------
    # Gewinnrate berechnen
    # -----------------------------
    df["Gewinnrate"] = (df["Siege"] / df["Spiele"] * 100).round(1)
    
    df_sorted = (
        df.sort_values(by=["Siege","Gewinnrate", "Tore", "Gegentore"], ascending=[False, False, False, True]).reset_index(drop=True)
    )
    df_sorted.index = df_sorted.index + 1
    df_sorted.index.name = "Platz"



    return df_sorted
