from typing import Dict

from src.core.algorithms import (
    annex_a_dangerous_events,
    annex_b_probability,
    annex_c_loss_logic,
)

# Moving up one level from 'engines' to 'core', then into 'models'
from src.core.models.structure import Structure


class RiskAggregator:
    def __init__(self, structure: Structure, ground_strike_density: float):
        self.structure = structure
        self.ng = ground_strike_density
        # Tolerable Risk for R1 as per Table 4
        self.RT_R1 = 1e-5

    def calculate_r1(self) -> Dict[str, float]:
        """
        Orchestrates the calculation of all R1 risk components.
        Returns a dictionary of individual components and the total risk.
        """
        results = {}

        # --- 1. Frequency of Dangerous Events (Annex A) ---
        nd = annex_a_dangerous_events.calculate_nd(self.structure, self.ng)
        nm = annex_a_dangerous_events.calculate_nm(self.structure, self.ng)

        # --- 2. Summing Risks across all Zones ---
        total_r1 = 0.0

        for zone in self.structure.zones:
            # Component RA: Injury to living beings (S1)
            # RA = ND * PA * LA
            pa = annex_b_probability.calculate_pa(
                self.structure.lps, getattr(self.structure, "tws", None)
            )
            la = annex_c_loss_logic.calculate_lo(zone.nz, zone.nt, zone.tz)  # Annex C.5
            ra = nd * pa * la

            # Component RB: Physical damage to structure (S1)
            # RB = ND * PB * LB
            pb = annex_b_probability.calculate_pb(self.structure.lps)
            lb = annex_c_loss_logic.calculate_lx(zone.loss_type, zone.rf.value, zone.rp)
            rb = nd * pb * lb

            # Initialize line risks
            ru = 0.0
            rv = 0.0
            rw = 0.0
            rz = 0.0

            lu = la # Loss of human life
            lv = lb # Loss of physical damage
            # LW/LZ uses Loss of Systems (LO). Assuming calculate_lx handles it or using LB as proxy for now.
            lw = lb
            lz = lw

            for line in self.structure.lines:
                nl_line = annex_a_dangerous_events.calculate_nl(line, self.structure, self.ng)
                ni_line = annex_a_dangerous_events.calculate_ni(line, self.ng)

                # Component RU: Injury to living beings (S3 - via Lines)
                # RU = NL * PU * LU
                pu = annex_b_probability.calculate_pu() # Should pass line info
                ru += nl_line * pu * lu

                # Component RV: Physical damage (S3 - via Lines)
                # RV = NL * PV * LV
                pv = annex_b_probability.calculate_pv()
                rv += nl_line * pv * lv

                # Component RW: Failure of internal systems (S3 - via Lines)
                # RW = NL * PW * LW
                pw = annex_b_probability.calculate_pw()
                rw += nl_line * pw * lw

                # Component RZ: Failure of internal systems (S4 - via Near Lines)
                # RZ = (NI - NL) * PZ * LZ
                # Note: NI is flashes near line. RZ driven by NI.
                pz = annex_b_probability.calculate_pz()
                rz += ni_line * pz * lz

            zone_total = ra + rb + ru + rv + rw + rz
            total_r1 += zone_total

            results[f"zone_{zone.name}_ra"] = ra
            results[f"zone_{zone.name}_rb"] = rb
            results[f"zone_{zone.name}_ru"] = ru
            results[f"zone_{zone.name}_rv"] = rv
            results[f"zone_{zone.name}_rw"] = rw
            results[f"zone_{zone.name}_rz"] = rz

        results["total_r1"] = total_r1
        results["is_safe"] = total_r1 <= self.RT_R1

        return results

    def get_summary_report(self):
        """Generates a human-readable verdict for the assessment."""
        res = self.calculate_r1()
        status = (
            "COMPLIANT" if res["is_safe"] else "NON-COMPLIANT - Protection Required"
        )
        print(f"Project: {self.structure.name}")
        print(f"Total Risk R1: {res['total_r1']:.2e}")
        print(f"Tolerable Risk RT: {self.RT_R1:.2e}")
        print(f"Verdict: {status}")
