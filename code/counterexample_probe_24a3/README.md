# mg-24a3 — a 1/3–2/3 counterexample under the semigroup action

Instrument for `docs/OneThird-Counterexample-Under-The-Action.md`.

    ./run_all.sh            # regenerates selftest_output.txt and probe_output.txt
    python3 check_doc.py    # verifies every figure quoted in the deliverable

Self-contained: no imports from `code/face_geometry/`, `code/hodge_leverage/` or
`code/semigroup_note/`. Every object is rebuilt from its definition in exact rational
arithmetic, so the numbers are independent of the pipeline they are about.

| file | what it is |
|---|---|
| `core.py` | posets, linear extensions, `delta`, the partition lattice, commitment levels, multiplicities, moves, the action |
| `bridge.py` | the majority relation, `L*`, `E[inv(L,L*)]`, the concentration ratio `R`, `L*`'s chain in `Q(P)`, named families |
| `selftest.py` | 10 controls; every derived route checked against a brute-force route sharing no code with it |
| `probe.py` | the seven sections of the deliverable |
| `check_doc.py` | the prose-vs-instrument check: 53 quoted figures, plus guards against unconditional counterexample claims |

Controls worth knowing about, because they are what makes the rest trustworthy:

* **C1** poset counts against A000112 (1, 2, 5, 16, 63, 318, 2045) by **two** independent
  enumeration routes, agreeing set-for-set to `n = 6`.
* **C6** the predicted spectrum against `dim ker(M − λI)` on the actual transition matrix in
  exact rationals, multiplicities matched and dimensions summing to `|L(P)|`.
* **C8** the stationary pair marginal `π = q/(q+q')` against the exact stationary vector of `M`.
* **C10** the worked example of `docs/OneThird-Semigroup-Walk-Family-Note.md` reproduced from
  scratch (6 extensions, 26 moves, 14 of 15 partitions are levels, and the missing one is
  `{a,d}|{b,c}`).

Determinism: seeded PRNG (`SEED = 20260730`) and sorted iteration throughout; both output
files reproduce byte-identically.
