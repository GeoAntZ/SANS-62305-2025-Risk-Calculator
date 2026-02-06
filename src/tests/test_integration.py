import sys
import os

# Ensure src is in pythonpath
sys.path.append(os.getcwd())

from src.core.models.structure import Structure, LocationFactor
from src.core.models.zone import RiskZone
from src.core.models.line import Line, LineType, LineSection, InstallationType
from src.core.engines.risk_aggregator import RiskAggregator
from src.core.models.protection import LPS

def main():
    print("Starting Integration Test...")

    # 1. Create Structure
    struct = Structure("Test House", length=10, width=10, height=5, location=LocationFactor.ISOLATED)
    print("Structure created.")

    # 2. Add LPS
    lps = LPS(level=None) # No LPS
    struct.set_lps(lps)
    print("LPS set.")

    # 3. Add Zone
    zone = RiskZone("Z1", struct, loss_type="residential", occupancy_hours=8760)
    struct.zones.append(zone)
    print("Zone added.")

    # 4. Add Line
    line = Line("Power Line", LineType.POWER)
    section = LineSection(length=500, installation=InstallationType.AERIAL)
    line.add_section(section)
    struct.add_line(line)
    print("Line added.")

    # 5. Run Aggregator
    aggregator = RiskAggregator(struct, ground_strike_density=4.0)
    results = aggregator.calculate_r1()

    print("\n--- Results ---")
    print(f"Total Risk: {results['total_r1']:.2e}")
    print(f"Is Safe: {results['is_safe']}")
    print("Detailed components:")
    for k, v in results.items():
        if k not in ["total_r1", "is_safe"]:
            print(f"  {k}: {v:.2e}")

    if results['total_r1'] > 0:
        print("\nSUCCESS: Risk calculated.")
    else:
        print("\nFAILURE: Risk is zero (unexpected for this test case).")

if __name__ == "__main__":
    main()
