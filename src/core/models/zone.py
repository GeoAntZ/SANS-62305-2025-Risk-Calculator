from enum import Enum
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.core.models.structure import Structure


class FireRisk(Enum):
    """rf values as per Table B.6"""

    EXPLOSION = 1.0
    HIGH = 0.1
    ORDINARY = 0.01
    LOW = 0.001
    UNKNOWN = 0.0


class RiskZone:
    def __init__(self, name: str, structure, occupancy_hours: float = 0.0):
        self.name = name
        self.structure = structure
        self.tz = occupancy_hours  # Annual attendance hours

        # Physical factors
        self.rt = 1.0  # Reduction factor for type of surface (Table B.1)
        self.rf = FireRisk.ORDINARY  # Fire risk factor
        self.rp = 1.0  # Provisions to reduce fire consequences (Table B.4)

        self.internal_systems: List["InternalSystem"] = []

    @property
    def pp(self) -> float:
        """Probability of presence of persons (Eq. B.14)."""
        return self.tz / 8760.0

    def add_system(self, system: "InternalSystem"):
        """Adds an electrical/electronic system to the zone."""
        self.internal_systems.append(system)

    def get_aggregated_pc(self) -> float:
        """
        Implements Clause 8.5.1: Aggregated probability for failure
        of internal systems due to physical damage (PC).
        PC = 1 - PRODUCT(1 - PC_i)
        """
        if not self.internal_systems:
            return 0.0

        product_term = 1.0
        for sys in self.internal_systems:
            product_term *= 1.0 - sys.pc
        return 1.0 - product_term


class InternalSystem:
    def __init__(self, name: str, pc: float = 1.0, pm: float = 1.0):
        self.name = name
        self.pc = pc  # Prob. of failure due to physical damage (S1/S3)
        self.pm = pm  # Prob. of failure due to LEMP (S2/S4)


class Zone:  # Ensure this is exactly 'Zone'
    def __init__(
        self, name: str, structure: "Structure", loss_type: str = "residential"
    ):
        self.name = name
        self.structure = structure
        self.loss_type = loss_type

        # Occupancy attributes for Annex C
        self.nz = 1.0  # Persons in zone
        self.nt = 1.0  # Total persons in building
        self.tz = 8760.0  # Attendance hours

        # Fire attributes
        self.rf = FireRisk.ORDINARY
        self.rp = 1.0
