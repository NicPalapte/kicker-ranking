from db.database import get_session
from db.models import Matches, MatchPlayer, TeamEnum

def create_match(goals_schwarz: int, goals_grau: int, team_schwarz_ids: list, team_grau_ids: list) -> Matches:
    with get_session() as session:
        match = Matches(
            goals_schwarz=goals_schwarz,
            goals_grau=goals_grau
        )
        session.add(match)
        session.commit()
        session.refresh(match)

        for player_id in team_schwarz_ids:
            match_player = MatchPlayer(
                match_id=match.id,
                player_id=player_id,
                team=TeamEnum.TEAM_SCHWARZ
            )
            session.add(match_player)
        for player_id in team_grau_ids:
            match_player = MatchPlayer(
                match_id=match.id,
                player_id=player_id,
                team=TeamEnum.TEAM_GRAU
            )
            session.add(match_player) 
        session.commit()
        return match