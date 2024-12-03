from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional
from decimal import Decimal

class TournamentType(Enum):
    REGULAR = "Regular"
    PKO = "Progressive Knockout"

@dataclass
class BlindLevel:
    small_blind: int
    big_blind: int
    ante: int
    duration_minutes: int

@dataclass
class Player:
    id: int
    name: str
    bounty: Optional[Decimal] = None
    eliminated: bool = False
    position: Optional[int] = None

@dataclass
class PayoutStructure:
    positions: Dict[int, Decimal]  # position -> percentage of prize pool
    min_players: int  # minimum number of players for this structure

@dataclass
class MultiwayAllInResult:
    players: List[Player]
    finishing_positions: Dict[int, int]  # player_id -> position