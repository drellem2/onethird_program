# `counterexample_audit_c6bc` — the independent audit of mg-a893 (`90db267`)

Write-up: `docs/OneThird-Counterexample-Under-The-Action-IndependentAudit-mgc6bc.md`.

**What this is.** A fourth independent implementation of the objects in
`docs/OneThird-Counterexample-Under-The-Action.md`, built to check mg-a893's repair of the statistical
inference in `docs/OneThird-Counterexample-Under-The-Action-Repair.md`. `kern6bc.py` imports **nothing**
from `counterexample_repair_dea5/` (the subject), `counterexample_probe_24a3/` (the target) or
`counterexample_audit_0a11/` (the previous audit). Its definitions are rebuilt from the sentences of the
documents:

| object | definition taken from |
|---|---|
| `e(P)`, `p(x,y)`, `Inc(P)`, `δ(P)` | target §1 |
| `L*` (the majority order) | target §2 |
| move, `P`-compatibility, level, `Q(P)`, `m_X` | `OneThird-Semigroup-Walk-Family-Note.md` §1 |
| `qfrac`, `qmass` | target §4 |
| cut element, cut extension, core | repair §3.4 |
| `δ`-extremal | `δ(P) = 1/3` — target §3, "min 3δ = 1 says the conjecture is tight" |

**Run it.** `sh run_all.sh` — pure Python 3, no dependencies, about 4 minutes. Exact integer and rational
arithmetic throughout. Every output reproduces byte-identically. The last step re-runs
`../counterexample_audit_0a11/check_locator.py` **unmodified** and diffs it against mg-a893's committed
`out_battery_0a11_rerun.txt`; it does not re-commit that file.

| file | what it does | output |
|---|---|---|
| `kern6bc.py` | posets up to isomorphism, `e`, `p(x,y)`, `δ`, levels, `m_X`, `qmass`, cores, duals | — |
| `selftest6bc.py` | controls on the instrument, labelled positive / theorem / **negative** | `out_selftest.txt` |
| `a1_recount.py` | every figure mg-a893 added, recounted | `out_a1_recount.txt` |
| `a2_theorem.py` | the cut-element theorem re-derived; NC1 re-run as the control it is | `out_a2_theorem.txt` |
| `a3_duality.py` | **BROKEN 2** — order duality collapses the five cores to three | `out_a3_duality.txt` |
| `a4_extend.py` | **BROKEN 1** — the `e ≤ 9` family to `n = 12`; the sixth core | `out_a4_extend.txt` |
| `a5_battery.py` | six probes mg-a893's author never saw, plus the mg-4acd composition test | `out_a5_battery.txt` |

**Three negative controls, and they fire** (`out_selftest.txt`): breaking the level test changes `qmass`;
the duality loop run on `#minimal elements` — a statistic that is *not* dual-invariant — differs on 50 of
88; a mean-instead-of-max `δ` changes which posets are extremal. The confluence-style checks are labelled
**THEOREM WITH AN IMPLEMENTATION CHECK** rather than controls, per mg-3b51.

**The completeness of `a4_extend.py`'s enumeration is an argument, not a search.** Deleting a maximal
element cannot increase `e`, because `L(Q) → L(Q − x)` is onto. So `{P : e(P) ≤ 9}` is closed under that
deletion and building `n` from `n − 1` with an `e ≤ 9` prune reaches every member up to isomorphism. The
control on it is in `out_selftest.txt`: the pruned and the full enumerations agree exactly at
`n = 5 … 8`.

**What this instrument does not do.** It does not re-derive Theorem 4, the cycle search, or §5–§6 of the
target — mg-0a11 covered those and nothing in `90db267` touches them. It computes `qmass` directly up to
`n = 10`; beyond that only the cores are checked.
