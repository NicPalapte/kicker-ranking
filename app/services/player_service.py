from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from db.database import get_session
from db.models import Player

def create_player(first_name: str, last_name: str):
    with get_session() as session:
        player = Player(
            name=first_name.strip(),
            surname=last_name.strip()
        )
        session.add(player)

        try:
            session.commit()
            session.refresh(player)
            return player

        except IntegrityError:
            session.rollback()
            return None
        
def get_all_players():
    with get_session() as session:
        players = session.exec(
            select(Player).order_by(Player.name, Player.surname)
        ).all()
        return players
    
def get_player_by_name_and_surname(name: str, surname: str):
    with get_session() as session:
        player = session.exec(
            select(Player).where(
                Player.name == name,
                Player.surname == surname
            )
        ).first()
        return player