"""Player data model for fantasy football draft assistant."""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class Position(Enum):
    """Player position enumeration."""
    QB = "QB"
    RB = "RB" 
    WR = "WR"
    TE = "TE"
    K = "K"
    DEF = "DEF"


class InjuryStatus(Enum):
    """Player injury status enumeration."""
    HEALTHY = "Healthy"
    QUESTIONABLE = "Questionable"
    DOUBTFUL = "Doubtful" 
    OUT = "Out"
    IR = "IR"


@dataclass
class Player:
    """
    Represents a fantasy football player with all relevant draft information.
    
    Attributes:
        id: Unique player identifier
        name: Player's full name
        position: Player position (QB, RB, WR, TE, K, DEF)
        team: NFL team abbreviation
        bye_week: Week number for team's bye (1-18)
        consensus_rank: Overall consensus ranking
        adp: Average draft position from mock drafts
        ppg_projection: Projected points per game
        target_share: Expected target share (WRs/TEs/pass-catching RBs)
        receptions_2024: Receptions from previous season
        injury_status: Current injury status
        notes: Additional scouting notes
        handcuff: Name of player's primary handcuff
        is_drafted: Whether player has been drafted
    """
    
    id: Optional[int]
    name: str
    position: Position
    team: str
    bye_week: int
    consensus_rank: Optional[int] = None
    adp: Optional[float] = None
    ppg_projection: Optional[float] = None
    target_share: Optional[float] = None
    receptions_2024: Optional[int] = None
    injury_status: InjuryStatus = InjuryStatus.HEALTHY
    notes: Optional[str] = None
    handcuff: Optional[str] = None
    is_drafted: bool = False
    
    def __post_init__(self):
        """Validate player data after initialization."""
        if not isinstance(self.position, Position):
            self.position = Position(self.position)
        if not isinstance(self.injury_status, InjuryStatus):
            self.injury_status = InjuryStatus(self.injury_status)
        
        if not 1 <= self.bye_week <= 18:
            raise ValueError(f"bye_week must be between 1-18, got {self.bye_week}")
        
        if self.adp and self.adp < 1:
            raise ValueError(f"adp must be positive, got {self.adp}")
            
        if self.target_share and not 0 <= self.target_share <= 1:
            raise ValueError(f"target_share must be 0-1, got {self.target_share}")
    
    @property
    def is_injured(self) -> bool:
        """Check if player has any injury designation."""
        return self.injury_status != InjuryStatus.HEALTHY
    
    @property
    def is_available(self) -> bool:
        """Check if player is available for drafting."""
        return not self.is_drafted and self.injury_status != InjuryStatus.OUT
    
    @property
    def has_ppr_upside(self) -> bool:
        """Check if player has PPR upside (high target share or receptions)."""
        if self.position in [Position.K, Position.DEF]:
            return False
        if self.target_share and self.target_share > 0.15:
            return True
        if self.receptions_2024 and self.receptions_2024 > 40:
            return True
        return False
    
    @property
    def bye_week_risk(self) -> str:
        """Assess bye week risk level."""
        if self.bye_week == 8:
            return "HIGH"  # Byepocalypse week
        elif self.bye_week == 14:
            return "MEDIUM"  # Playoff week
        elif self.bye_week in [10]:
            return "MEDIUM"  # Heavy bye weeks
        else:
            return "LOW"
    
    def __str__(self) -> str:
        """String representation of player."""
        injury_indicator = "⚠️" if self.is_injured else ""
        drafted_indicator = "❌" if self.is_drafted else ""
        return f"{self.name} ({self.position.value}, {self.team}) {injury_indicator}{drafted_indicator}"
    
    def __repr__(self) -> str:
        """Developer representation of player."""
        return (f"Player(name='{self.name}', position={self.position.value}, "
                f"team='{self.team}', rank={self.consensus_rank}, "
                f"adp={self.adp}, drafted={self.is_drafted})")
    
    def to_dict(self) -> dict:
        """Convert player to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position.value,
            'team': self.team,
            'bye_week': self.bye_week,
            'consensus_rank': self.consensus_rank,
            'adp': self.adp,
            'ppg_projection': self.ppg_projection,
            'target_share': self.target_share,
            'receptions_2024': self.receptions_2024,
            'injury_status': self.injury_status.value,
            'notes': self.notes,
            'handcuff': self.handcuff,
            'is_drafted': self.is_drafted,
            'has_ppr_upside': self.has_ppr_upside,
            'bye_week_risk': self.bye_week_risk
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Player':
        """Create Player instance from dictionary."""
        return cls(
            id=data.get('id'),
            name=data['name'],
            position=Position(data['position']),
            team=data['team'],
            bye_week=data['bye_week'],
            consensus_rank=data.get('consensus_rank'),
            adp=data.get('adp'),
            ppg_projection=data.get('ppg_projection'),
            target_share=data.get('target_share'),
            receptions_2024=data.get('receptions_2024'),
            injury_status=InjuryStatus(data.get('injury_status', 'Healthy')),
            notes=data.get('notes'),
            handcuff=data.get('handcuff'),
            is_drafted=data.get('is_drafted', False)
        )