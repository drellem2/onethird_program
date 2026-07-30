# counterexample_audit_a7b4 — the instrument for the mg-a7b4 audit

Independent verification of `docs/OneThird-Counterexample-Under-The-Action.md`
(mg-24a3 / f5d3485). Findings are written up in
`docs/OneThird-Counterexample-Under-The-Action-IndependentAudit.md`.

**Shares no code with `code/counterexample_probe_24a3/`** (nor with `code/face_geometry/`,
`code/hodge_leverage/`, `code/semigroup_note/`). Every object is rebuilt from its definition in
exact rational arithmetic. Where a route was available, a different one from the target's was
taken on purpose, so that a shared bug cannot cancel:

| target | here |
|---|---|
| enumerate by adjoining a **maximal** element | adjoin a **minimal** element |
| canonical form certified against A000112 | **also** against A001035 (labelled posets) via `Σ n!/|Aut|`, which catches over- *and* under-merging |
| `p(x,y)` by splitting `L(P)` at `x`'s placement | `p(x,y) = e(P ∪ {x<y})/e(P)`, a DP on the augmented poset |
| quotient acyclicity by Kahn | by DFS three-colouring |
| moves at a level by a recursion | by a subset DP |

Run `./run_all.sh` (about 15 minutes, pure Python 3, no dependencies). `selfcheck.py` must end
in `ALL CONTROLS PASS` before any number here is quotable; it certifies the enumeration against
**A000112**, **A001035** and **A000670**, checks `e(P)` and `p(x,y)` against direct enumeration
of `L(P)`, checks the level description against brute force over all block orders, and checks
the predicted spectrum against `dim ker(M − λI)` in exact rationals on the actual transition
matrix.

Only `witness9.py` and `shrink_witness.py` use randomness, both seeded.
