import math
from enum import Enum
from typing import List


class LineType(Enum):
    """CT factors as per Table A.3"""

    POWER = 1.0
    TELECOM = 1.0
    DATA = 1.0  # Often treated same as telecom unless fiber


class InstallationType(Enum):
    """CI factors as per Table A.2"""

    AERIAL = 1.0
    BURIED = 0.5


class LineSection:
    def __init__(
        self,
        length: float = 1000.0,
        installation: InstallationType = InstallationType.AERIAL,
        line_height: float = 6.0,  # Ha
        rho_ground: float = 250.0,  # Added this to fix your error
    ):
        self.LL = length
        self.installation = installation
        self.Ha = line_height
        self.rho = rho_ground  # Now 'self.rho' is known to the class
        self.rs = 0.0  # Shield resistance

    def calculate_al(self, hb: float) -> float:
        """
        Calculates AL for a section (Annex A.3).
        hb: height of the structure connected to the line.
        """
        # Width of collection area (Dc)
        if self.installation == InstallationType.AERIAL:
            # For aerial lines, Dc = 3 * (Ha + Hb)
            dc = 3 * (self.Ha + hb)
        else:
            # For buried lines, Dc = sqrt(rho)
            dc = math.sqrt(self.rho)

        # AL = (LL - 3*(Ha + Hb)) * Dc
        # Note: 3*(Ha + Hb) represents the 'transition' zones at ends of the line
        return (self.LL - 3 * (self.Ha + hb)) * dc

    @property
    def ci(self) -> float:
        """Returns installation factor based on Table A.2."""
        return self.installation.value


class Line:
    def __init__(self, name: str, line_type: LineType = LineType.POWER):
        self.name = name
        self.line_type = line_type
        self.sections: List[LineSection] = []

    def add_section(self, section: LineSection):
        """Partitions the line into sections as per Clause 8.4."""
        self.sections.append(section)

    @property
    def total_length(self) -> float:
        """Calculates total line length. Defaults to 1000m if no sections exist."""
        if not self.sections:
            return 1000.0
        return sum(s.LL for s in self.sections)

    def get_worst_case_rho(self) -> float:
        """
        Implements Clause 8.4: If a parameter varies, the value
        leading to the highest risk is assumed.
        """
        if not self.sections:
            return 250.0  # Standard default
        return max(s.rho for s in self.sections)
