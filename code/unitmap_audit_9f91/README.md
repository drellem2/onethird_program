# `mg-9f91` — instrument for the independent audit of `mg-9adf`

Audits `21ee93f` (the `ε_spec`/`ε_c3ca` unit-map landing into `STATE.md:15` and `:115`).
Full record: [`docs/OneThird-UnitMap-mg-9f91-IndependentAudit.md`](../../docs/OneThird-UnitMap-mg-9f91-IndependentAudit.md).

Run from the repo root. Python 3, stdlib only, no arguments.

    python3 code/unitmap_audit_9f91/m1_map.py          # step 1  re-derive the map
    python3 code/unitmap_audit_9f91/m2_survival.py     # step 5  did the other landings survive
    python3 code/unitmap_audit_9f91/m3_attainment.py   # step 4  is the n-range split right
    python3 code/unitmap_audit_9f91/m4_landing.py      # steps 2, 3, 6

Committed outputs: `out_m1_map.txt`, `out_m2_survival.txt`, `out_m3_attainment.txt`,
`out_m4_landing.txt`. `m2` and `m4` read `72a6e33` and `21ee93f` out of git, so they reproduce
regardless of what `STATE.md` looks like later; `m1` and `m3` depend on nothing in the repo at all.

**`PREDICTIONS.md` was committed at `440cb05`, before any diff of `21ee93f` was read.** `H1`–`H7`
in it are hand measurements disclosed as such and are not scored.

## What each script establishes

**`m1_map.py`** — exact `Fraction` arithmetic, `77/77`. `ε_c3ca = (n−1)/(6n) → 1/6`,
`ε_spec = n/(n+1) → 1`, ratio `= 6n²/(n²−1) → 6`, all three **strict at every finite `n`**, and
`ε_spec` at the bound is identically the `n/(n+1)` closure value. Also prints what a flat factor of
6 gets wrong at small `n` (`n=3`: `2/3` against the true `3/4`).

**`m2_survival.py`** — **never looks at the diff.** Row 8 is one 5 245-character cell that three
tickets edited on 2026-08-07, so any edit renders as *"the whole line changed"* and a diff-driven
check would report reflow as loss. Instead it extracts 13 guarded spans (`mg-d1a2`'s literature
guard, `mg-5ce3`'s N₀ text) by **string search** from parent and landed file and compares bytes.
`13/13 INTACT` at both `21ee93f` and `HEAD`. This guard was written into `PREDICTIONS.md` as `P13`,
my own most likely error, before the diff was opened.

**`m3_attainment.py`** — the load-bearing one, and it **inverts the brief**. My ticket said
attainment is finite-population `n ∈ {3,4,5,6,8}`. It is not: that set is `mg-6bc2` **Claim 4.1**'s
(footrule), while **Claim 3.1** (inversion) is attained at every `n` by the **two-atom law**
`μ = (2/3+η)δ_e + (1/3−η)δ_{rev e}` — two permutations. Brute-forces the flip probabilities over
`S_n` directly, **no LP and nothing inherited from `mg-6bc2`'s tableau**: `192/192` exact-rational
over `n ∈ {2,3,4,5,6,7,8,9,11,20,50,137} × η ∈ {0, 1/100, 1/12, 1/6}`, seven of those `n` outside
the ticket's set. `mg-9adf`'s split is correct and both tickets' paraphrase was wrong.

**`m4_landing.py`** — scans the inserted text only. Confirms the reserved question is **not**
decided (3 reserving phrases per site), the closure travelled to **both** sites (6/6 markers each),
`:415` and `:172` are both cited at both sites, the doubled `λ_std→1` sentence is **pre-existing**
(2 → 2), and scope is clean (only `:15`/`:115` changed, row 11 at `:118` untouched, `ε_dem`/`C₃`
counts unchanged). Its `S4` block is the audit's one finding: the landed all-`n` attainment claim is
correct but `mg-6bc2:450` says the opposite, and neither the page nor the commit message says so.

## Defects of this instrument, kept in the source

- **`m4_landing.py` S1 reads a DENIAL as an ASSERTION.** The regex
  `conjecture is (confirmed|refuted|…)` fires on `:15`, matching *"nothing in it says the conjecture
  is confirmed or refuted"* — the sentence that **reserves** the question. Trusting the headline
  would have reported the site that best obeys the brief as the one that violates it. Kept as
  written, with surrounding context printed so the false positive is visible. A misreading detector
  that misreads, inside an audit about misreadings.
- **`m3_attainment.py`'s exhaustive `≤` cross-check is thin.** It enumerates only *single-atom*
  measures at `n ≤ 6` (4 feasible). The real `≤` is one line of linearity of expectation and needs
  no enumeration; the scan is not independent verification of that direction.
- **`m2_survival.py`'s span list is hand-chosen.** 13 needles I selected by reading row 8 at the
  parent. A claim deleted from a region I did not pick a needle for would not be detected. The
  pure-insertion result (`m4`, S6 / the audit doc §5) is what actually rules that out, and it is a
  stronger check than the needle list.
