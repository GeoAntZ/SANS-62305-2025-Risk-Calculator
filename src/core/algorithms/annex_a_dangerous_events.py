import math


def calculate_ng(td: float) -> float:
    """
    Calculates ground flash density (NG) from thunderstorm days (TD).
    As per Equation A.1: NG = 0.1 * TD
    Note: Some regions use local lightning mapping data instead.
    """
    return 0.1 * td


def calculate_nd(structure, ng: float) -> float:
    """
    Frequency of flashes to the structure (ND).
    Equation A.2: ND = NG * AD * CD * 10^-6
    """
    return ng * structure.ad * structure.CD * 1e-6


def calculate_nm(structure, ground_strike_density: float) -> float:
    """
    Frequency of flashes near the structure (NM).
    Now uses the structure's own AM and AD properties.
    """
    # Equation A.3: NM = Density * (AM - AD * CD) * 1e-6
    return ground_strike_density * (structure.am - (structure.ad * structure.CD)) * 1e-6


def calculate_nl(line, structure, ground_strike_density: float) -> float:
    """
    Frequency of flashes to a service line (NL).
    Equation A.4: NL = Density * AL * CI * CT * CE * 1e-6
    """
    total_nl = 0
    for section in line.sections:
        # We pass structure.H as 'hb' for the calculation
        al = section.calculate_al(structure.H)

        # CE is the environmental factor from Table A.4
        # For now, we assume a default or pass it as an attribute
        ce = getattr(section, "ce", 1.0)

        total_nl += (
            ground_strike_density * al * section.ci * line.line_type.value * ce * 1e-6
        )
    return total_nl


def _calculate_collection_area_m(structure):
    """Calculates AM: 250m perimeter area as per Annex A.2.2."""
    return (
        (structure.L * structure.W)
        + (2 * 250 * (structure.L + structure.W))
        + (math.pi * 250**2)
    )
