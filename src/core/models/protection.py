from enum import Enum
from typing import Optional


class LPL(Enum):
    """Lightning Protection Levels I through IV."""

    LEVEL_I = 1
    LEVEL_II = 2
    LEVEL_III = 3
    LEVEL_IV = 4


class LPS:
    def __init__(self, level: Optional[LPL] = None, is_mesh: bool = False):
        self.level = level
        self.is_mesh = is_mesh

    @property
    def pb(self) -> float:
        """
        Returns PB (Probability of physical damage) based on LPL.
        Values derived from Table B.3.
        """
        if self.level is None:
            return 1.0

        # Mapping LPL to standard PB values
        mapping = {
            LPL.LEVEL_I: 0.02,
            LPL.LEVEL_II: 0.05,
            LPL.LEVEL_III: 0.10,
            LPL.LEVEL_IV: 0.20,
        }
        return mapping.get(self.level, 1.0)


class SPDSystem:
    def __init__(self, level: LPL, coordinated: bool = True):
        self.level = level
        self.coordinated = coordinated

    def get_pspd(self, source: str) -> float:
        """
        Returns PSPD based on Table B.7 for Power Lines.
        Requires coordinated systems for values < 1.0.
        """
        if not self.coordinated:
            return 1.0

        # Simplified lookup for S1 (flashes to structure)
        mapping = {
            LPL.LEVEL_I: 0.01,
            LPL.LEVEL_II: 0.02,
            LPL.LEVEL_III: 0.03,  # Note: III and IV are often 0.05
            LPL.LEVEL_IV: 0.05,
        }
        return mapping.get(self.level, 1.0)


class TWS:
    """
    Thunderstorm Warning System as per IEC 62793
    (Integrated into SANS 62305-2:2025).
    """

    def __init__(self, active: bool = False, ftwr: float = 1.0):
        self.active = active
        self.ftwr = ftwr  # Failure to Warn Ratio

    @property
    def ptws(self) -> float:
        """Reduction factor for risks to persons in open areas (Equation B.45)."""
        return self.ftwr if self.active else 1.0
