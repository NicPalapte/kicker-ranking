from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint

from datetime import datetime, timezone
from enum import Enum
from uuid import UUID, uuid4

def utc_now():
    """Hilfsfunktion für konsistente UTC-Zeitpunkte."""
    return datetime.now(timezone.utc)

class Player(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    surname: str
    matches: list["MatchPlayer"] = Relationship(back_populates="player")
    __table_args__ = (UniqueConstraint("name", "surname", name="uq_player_name"),)


class Matches(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    goals_schwarz: int
    goals_grau: int
    date: datetime = Field(default_factory=utc_now)

    players: list["MatchPlayer"] = Relationship(back_populates="match")

class TeamEnum(str, Enum):
    TEAM_SCHWARZ = "Team_SCHWARZ"
    TEAM_GRAU = "Team_GRAU"

class MatchPlayer(SQLModel, table=True):
    match_id: UUID = Field(foreign_key="matches.id", primary_key=True)
    player_id: UUID = Field(foreign_key="player.id", primary_key=True)
    team: TeamEnum

    match: Matches = Relationship(back_populates="players")
    player: Player = Relationship(back_populates="matches")

