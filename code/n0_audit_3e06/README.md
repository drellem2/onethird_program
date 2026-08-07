# mg-3e06 — independent audit instrument for mg-5ce3's landing of mg-c4f5 §5.3

Two scripts, no dependencies beyond the standard library, no network, no float on
any decision path.

| file | what it does |
|---|---|
| `PREDICTIONS.md` | committed at `e186067`, before the diff / STATE.md / the audit doc were opened. Discloses an unusually large exposure (H1) rather than laundering it. |
| `a1_violator.py` | CHECK 1. Re-derives §5.3 from the definitions and **builds the violator** — 4 prefixes × 5 tails, both renderings of (LIB-const), five `N₀`. Exact `Fraction`/big-int arithmetic; `log₂` is never evaluated numerically. Also: the realizability ceiling, the repaired ceiling-respecting witness, both §5.3 figures in exact integers, and the conditional frozen-class `N₀`. |
| `a2_page.py` | CHECKS 2–4. Byte-substring tests over STATE.md (never line numbers), the site census pre/post/now, the blanket-replace test, the overshoot test, the mg-d1a2 guard, and mermaid edge integrity. |
| `out_*.txt` | committed output of each. |

Run: `python3 code/n0_audit_3e06/a1_violator.py` and
`python3 code/n0_audit_3e06/a2_page.py` from the repo root. `a2_page.py` shells out to
`git show 4ef64d7^:STATE.md`, so it must run inside the worktree.

**Six defects of my own fired against correct claims and are kept in the source rather
than tuned away** — see §7 of `docs/OneThird-N0-StateLanding-mg-3e06-IndependentAudit.md`.
The fourth is the load-bearing one: no finite ladder can establish unboundedness, so the
`o(n²)` verdict rests on an analytic reduction that is *stated*, with the ladder deciding
only the part it can (strict increase, which is what kills the constant-divisor controls).
