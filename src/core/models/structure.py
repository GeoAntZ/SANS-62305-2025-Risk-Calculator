import math
from enum import Enum
from typing import TYPE_CHECKING, List, Optional


class LocationFactor(Enum):
    """CD values as per Table A.1 of SANS 62305-2:2025"""

    ISOLATED_TALLER = 2.0  # Structure at the hilltop
    ISOLATED = 1.0  # No other structures around
    SURROUNDED_SIMILAR = 0.5  # Objects of similar height
    SURROUNDED_TALLER = 0.25  # Objects taller than structure


# This block only runs during static analysis (Type checking)
# It prevents circular import errors at runtime
if TYPE_CHECKING:
    from src.core.models.protection import LPS, TWS
    from src.core.models.zone import Zone


class Structure:
    def __init__(
        self,
        name: str,
        length: float,
        width: float,
        height: float,
        location: LocationFactor = LocationFactor.ISOLATED,
    ):
        self.name = name
        self.L = length
        self.W = width
        self.H = height
        self.CD = location.value

        self._manual_ad: Optional[float] = None
        self.protrusions: List[float] = []  # List of heights of protrusions
        self.zones = []

    def set_lps(self, lps_system: LPS):
        """Attaches an LPS system to the structure."""
        self.lps = lps_system

    def set_tws(self, tws_system: TWS):
        """Attaches a Thunderstorm Warning System to the structure."""
        self.tws = tws_system

    @property
    def ad(self) -> float:
        """
        Calculates AD. Implements the 'Conservative Risk Profile' by selecting
        the maximum area between the base height and all protrusion heights.
        """
        if self._manual_ad is not None:
            return self._manual_ad

        # Start with the collection area of the base structure
        max_area = self._calculate_area_from_height(self.H)

        # Check all protrusions and take the highest resulting area
        for p_height in self.protrusions:
            p_area = self._calculate_area_from_height(p_height)
            if p_area > max_area:
                max_area = p_area

        return max_area

    def _calculate_area_from_height(self, h: float) -> float:
        """Standard Annex A formula for a rectangular structure footprint."""
        return (
            (self.L * self.W) + (6 * h * (self.L + self.W)) + (math.pi * (3 * h) ** 2)
        )

    def set_graphical_area(self, area_value: float):
        """Override for AutoCAD-derived graphical analysis results."""
        self._manual_ad = area_value

    def add_protrusion(self, height: float):
        """Adds a roof protrusion to the calculation stack."""
        if height > 0:
            self.protrusions.append(height)

    def am(self) -> float:
        """
        Calculates AM (area for flashes near structure).
        Defaults to the 250m perimeter formula unless manually overridden.
        """
        if self._manual_am is not None:
            return self._manual_am

        # Standard formula for rectangular footprint with 250m buffer
        return (self.L * self.W) + (2 * 250 * (self.L + self.W)) + (math.pi * 250**2)

    def set_graphical_am(self, area_value: float):
        """Input for AM results derived from AutoCAD analysis."""
        self._manual_am = area_value
