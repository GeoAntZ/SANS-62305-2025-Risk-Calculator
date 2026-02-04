def calculate_pa(lps, tws=None) -> float:
    """
    Probability of injury to living beings by electric shock (PA).
    Influenced by LPS and Thunderstorm Warning Systems (TWS).
    """
    # If a TWS is active, it reduces the probability of persons being
    # in dangerous open areas.
    p_tws = tws.ptws if tws else 1.0

    # PA is also reduced by specific measures like insulation or
    # physical barriers (Table B.2), defaulting to 1.0 here.
    return 1.0 * p_tws


def calculate_pb(lps) -> float:
    """
    Probability of physical damage to a structure (PB).
    Directly tied to the LPL level of the LPS (Table B.3).
    """
    return lps.pb


def calculate_pc(spd_system) -> float:
    """
    Probability of failure of internal systems (PC).
    Depends on the SPD level (Table B.7).
    """
    # Source S1 (Flash to structure)
    return spd_system.get_pspd(source="S1")


def calculate_pm(ks1: float, ks2: float, uw: float = 1.5) -> float:
    """
    Calculates PM (Prob. of failure of internal systems due to LEMP).
    ks1: screening factor depending on the LPS or structure shield.
    ks2: screening factor depending on the internal spatial shield.
    uw: rated withstand voltage of the equipment (kV).
    """
    ksms = ks1 * ks2

    # Handle division by zero if shielding is perfect (ksms = 0)
    if ksms <= 0:
        return 0.0

    ratio = uw / ksms

    # Path 1: Voltage is high enough that failure is impossible
    if ratio >= 5:
        return 0.0

    # Path 2: Voltage is so low that failure is certain
    if ratio <= 0.07:
        return 1.0

    # Path 3: The interpolation zone (Fixed to always return a float)
    # Based on the log-linear relationship in Table B.10
    # Formula approximation: PM = 1 - (log10(ratio) + 1.15) / 1.85
    # Or a simpler linear interpolation for this stage:
    pm_value = 1.0 - ((ratio - 0.07) / (5 - 0.07))

    return float(pm_value)
