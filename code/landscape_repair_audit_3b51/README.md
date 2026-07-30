# `landscape_repair_audit_3b51` — mg-3b51's instrument

Independent audit of **mg-1953 / `6b1eacf`**, the repair of mg-ebd8's derivations in
`docs/OneThird-Landscape-Where-This-Lives.md`.

Pure Python 3, exact integer arithmetic, no third-party imports. `./run_all.sh`, ~5 min.

**Shares no code with** `code/landscape_ebd8/` (the original), `code/landscape_audit_d673/`
(the first audit), `code/landscape_repair_1953/` (the target of this audit),
`code/semigroup_note/`, `code/face_geometry/`, `code/unified_gate_8fd1/` or
`code/hodge_leverage/`. **No output committed by mg-1953 is read by anything here**, and
none of mg-1953's scripts is executed.

Where mg-1953 makes a representation or algorithm choice, `core3b51.py` makes the other
one, so agreement is evidence rather than a shared bug:

| step | mg-1953 | here |
|---|---|---|
| poset carrier | frozenset of strict pairs | packed reachability bitmasks |
| poset enumeration | filter the `2^C(n,2)` transitively closed upper-triangle subsets | extension by a new **maximal element** over an order ideal |
| "does flat `X` meet the open cone `U`?" | exhaustive search over the `|X|!` block orderings | **numeric construction with a certificate both ways** — longest-path potentials verified against the defining equations/inequalities on the YES side, an exhibited directed block cycle on the NO side |
| linear extensions | filter all `n!` permutations | DP over order ideals |
| multiplicities | — | the repo's triangular identity, rebuilt from the identity |

Both decision procedures for "`X` meets `U`" are implemented and **cross-validated flat by
flat** in `selftest.py`; the run fails loudly if they ever disagree.

| file | what it establishes |
|---|---|
| `core3b51.py` | the shared machinery above |
| `audit_r1_offAC.py` | R1: the acyclicity repair checked over **all flats**; where the defect lives; mg-1953's own control R1d examined for power to fail; a four-way mutation panel |
| `audit_r1_n7.py` | the same, at **n = 7**, one order past the range mg-1953 repaired in |
| `audit_r3_r4.py` | R3 ("sharper" → "more informative") as a two-sided comparison; the true gain counted; every R4 population; the Möbius step mg-1953 does not re-derive |
| `audit_r2_e8.py` | R2: the E8 replacement — band axioms, homomorphism, image, properness, injectivity, antichain cardinalities |
| `audit_scope_text.py` | scope: the bound word, the adoption argument, re-opening, over-correcting, row Q's candidate space, material beyond the brief |
| `selftest.py` | 139 assertions — external sequences, the cross-validation, and every number this audit's document carries |

Verdict and reasoning: `docs/OneThird-Landscape-Repair-IndependentAudit.md`.
