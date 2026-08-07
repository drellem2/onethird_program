# `code/pairbias_audit_a832f/` — mg-832f's instrument

INDEPENDENT AUDIT of `mg-6bc2`'s `eps_spec` derivation. Run `./run_all.sh` (~14 min).

**Independence.** Written from `STATE.md`'s statements of the definitions and from first
principles. `code/pairbias_sharpening_6bc2/`, `code/perslot_symmetry_200d/`,
`code/dual_certificate_131e/`, `code/pairbias_repair_ba78/` and `code/libweak_c3ca/` share
no line with this and **none of them was opened until after the runs above had produced
their outputs** — which is what makes §6.1 of the audit document a comparison rather than a
source. There is no `numpy` on this machine, so the two-phase simplex in `libA832.py` is
hand-written and uses Bland's rule; every arithmetic path is `fractions.Fraction`.

| file | what it is |
|---|---|
| `PREDICTIONS.md` | pre-registration, committed at `b9e6d19` before any script here existed and before the parent was read. **Do not edit** — it is a pre-registration artefact. |
| `libA832.py` | permutations, posets (naturally-labelled, generated bijectively), linear-extension DP, `delta`, the `>=2/3`-majority order with P15's guard, exact two-phase simplex |
| `selftesta832.py` | NC1 (three wrong closed forms must be REJECTED), NC2 (`delta` against two hand values), NC3 (the two-atom witness checked INTO `M_n`, not asserted), plus the simplex against hand-solved LPs |
| `a1_unitmap.py` | the unit map; Claim 3.1 by LP over all of `S_n`; attainment to `n = 1000`; Claim 4.1; the hypothesis-free bound; sec.3.1's identity; the `eta > 0` strictness |
| `a2_realizable.py` | the poset sweep both parents declared and refused. Argument = max `n`. |
| `a3_perslot.py` | `mg-131e`'s `n = 6` branch re-solved from scratch; three attempts to build what the negative forbids |
| `a4_boundary_structure.py` | primitivity of the boundary maximisers; the all-`n` ordinal-sum family; the nearest primitive population; a moving-count control on the sweep |

**Two defects of this instrument were found by reading its own output and are kept in the
audit document (§8), not fixed silently:** a printed `52/51` that should have been `52/52`,
and a summary sentence that contradicted the column printed beside it.

**`n <= 7` throughout.** Every emptiness and attainment figure here is finite-population.
