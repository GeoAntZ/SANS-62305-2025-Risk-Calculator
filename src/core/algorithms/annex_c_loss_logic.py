# Base loss values (LT) from Table C.2 for Loss of Life (L1)
BASE_LOSSES = {
    "hospital": 1e-2,
    "industrial": 1e-2,
    "public_entertainment": 1e-2,
    "residential": 1e-3,
    "commercial": 1e-3,
}


def calculate_lx(loss_type: str, rf: float, rp: float, h_factor: float = 1.0) -> float:
    """
    Calculates the relative loss (LX) for a zone.
    loss_type: e.g., 'hospital', 'industrial', 'residential'
    rf: fire risk factor (from Table B.6)
    rp: provisions against fire (from Table B.4)
    h_factor: increases loss if a special hazard is present (Table C.1)
    """
    lt = BASE_LOSSES.get(loss_type, 1e-3)

    # Equation C.1: LX = LT * rf * rp * h_factor
    return lt * rf * rp * h_factor


def calculate_lo(nz: float, nt: float, tz: float) -> float:
    """
    Calculates loss due to injury (LO) as per Equation C.5.
    nz: number of persons in the zone
    nt: total number of persons in the structure
    tz: time in hours per year spent in the zone
    """
    # Relative number of persons affected weighted by time
    return (nz / nt) * (tz / 8760.0)
