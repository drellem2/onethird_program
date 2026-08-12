# `compression_consumers_145f` — mg-145f's instrument

**Question.** Is there ANY target in this programme that an exact cube-foliation energy
identity can feed, given Theorem E caps the BK gap (mg-409a) and `λ_std` is provably
incomparable to `λ₂^BK` (mg-d1be, `STATE.md:78`)?

**Deliverable.** [`docs/OneThird-Compression-Consumers-mg-145f.md`](../../docs/OneThird-Compression-Consumers-mg-145f.md).

**Run.** `./run_all.sh` — **7.2 s measured on this host** (`time ./run_all.sh`, 6.99 s user;
`e5` is ~5 s of it, the isomorphism canonisation). Exit `0` iff every arm passes.

| arm | asks | output |
|---|---|---|
| `e0_selftest.py` | do my constructions agree with mg-409a's independent implementation? four positive controls that must fire | `out_e0_selftest.txt` |
| `e1_outputmap.py` | **THE OUTPUT MAP** — what does the identity actually emit? | `out_e1_outputmap.txt` |
| `e2_covariance.py` | can it feed **(B-cov)**, the residual `STATE.md:180` puts first? | `out_e2_covariance.txt` |
| `e3_density.py` | can it feed **(R)**, the one target whose deliverable is a crude constant? | `out_e3_density.txt` |
| `e4_adjacency.py` | the one candidate of the **right shape** — mg-92e6's adjacency fact | `out_e4_adjacency.txt` |
| `e5_collisions.py` | does the identity's output **determine** the programme's targets? | `out_e5_collisions.txt` |

## Exactness

**There is no float anywhere in this directory.** Unlike mg-409a's instrument there is no
eigenvalue path at all, because nothing here needs one: every arm is a `Fraction` comparison
or an exhibited bijection. mg-409a's D6 (*"the eigenvalue path is float"*) therefore does not
apply here, and that is a property of the question, not a virtue of the code.

## Independence

`lib409a` is imported by **`e0` only**, and only as a cross-check. `e1…e5` import `lib145f`
alone. Posets, linear extensions, the two checkerboard block systems, fibers, conditional
variances, the BK Dirichlet form and the adjacency probabilities are all rebuilt here from
the definitions in `docs/imports/compression.tex`. Same discipline mg-409a applied to
`lib8bc7`, for the reason its own D5 records: sharing one library makes downstream arms
non-independent witnesses of each other.

`e0.2` compares the two implementations on **702 (poset, statistic) pairs** at
`max |difference| = 0`, exact.

## The finding, in one line

> **The identity computes the NUMERATOR of the Rayleigh quotient exactly and the DENOMINATOR
> not at all** — and every open target in this programme lives in the denominator.

`E_BK(f) = (2/(n−1))(E Var(f|C_o) + E Var(f|C_e))` is exact for a degree-one statistic;
`Var(f) = E Var(f|C_o) + Var(Π_o f)` and the identity supplies only the first summand. The
ratio between what it computes and what it does not **is** `alpha`, which is why `alpha` is
its only output — and mg-409a priced `alpha` dead (ceiling `1`, bar `≥ 2`).

## The controls, and what each one would have caught

| control | plants | must |
|---|---|---|
| `e0` C1 | a perturbed `A_o` | break the identity — **fires** |
| `e0` C2 | `A_e` in `A_o`'s slot | break the identity — **fires** |
| `e0` C3 | a degree-two statistic | not be computed by the identity — **fires** |
| `e0` C4 | mg-409a's D1 (dropped trailing singleton) | leave the PARTITION identical, so the block LIST is what must be compared — **fires** |
| `e3.4` C | distance-2 for distance-1 | not give `n−1` — **fires** (`2` vs `3`) |
| `e5.0` C | my own D1's ordered-pair key | be shown NOT isomorphism-invariant — **fires**, 359 relabellings move it |

**And the suite as a whole goes red.** Swapping the two parity buckets inside
`lib145f.adjacency_probs` (one edit, the odd/even assignment) takes `e1.1` from
`0 failures / 1475` to **`1266 failures / 1475`** on both the `A^o` and the `A^e` row — while
the `E_BK` row stays green, because `E_BK` consumes only the **sum** `A^o + A^e` and a swap
preserves it. That asymmetry is worth stating: `e1`'s third row alone could not have caught
this, and the arm has three rows for that reason. `lib145f.py` was restored byte-identically
(`diff` clean) and `__pycache__` cleared — the stale `.pyc` after the restore turned five
arms red on unmutated source and is kept as **D2** below.

## Defects of my own, all kept

**D1 — I keyed an isomorphism-invariant question on an ordered-pair key and got a
"finding".** `e4.3`'s first version searched for two posets with equal `(A^o, A^e)` but
different per-slot `J`, and reported `P1 = [(2,3)]` against `P2 = [(3,2)]` — **one poset
relabelled**. The aggregate key was over unordered pairs and the per-slot key was over
ordered pairs, so the two sides were not comparable and the search found the relabelling
rather than an information loss. This is **mg-409a's own D2 recurring in the directory that
cites it**, which is the part worth recording: reading a predecessor's defect list is not the
same as applying it. Caught because a "collision" between a poset and its own relabelling is
absurd on its face, not because anything checked. Replaced by a direct demonstration
(`≥ 2` nonzero per-slot summands inside one parity class, at 70 of 921 incomparable pairs),
and the defective key is now armed as `e5.0`'s positive control.

**D2 — a restored library and a stale `__pycache__` sent five green arms red.** After the
mutation demonstration above I restored `lib145f.py` byte-identically (`diff` clean, sha256
recorded) and `run_all.sh` still failed five of six arms. The mutated bytecode was still
cached. Nothing mathematical was wrong and no committed output is affected, but a suite whose
result depends on a directory Python manages invisibly is a suite that can be green on
mutated source as easily as red on clean source. `run_all.sh` does **not** clear
`__pycache__` — adding that would hide the failure mode rather than record it, and the honest
statement is that **every output file here was produced by a run whose `__pycache__` I had
just deleted**.

**D3 — `e5`'s null rows have almost no power and must not be read as positives.** The
collision test compares **4 distinct-class pairs at `n = 4` and 10 at `n = 5`**. One target
(`max p_xy`) SPLITS, which is a hard negative for it. The other four come back "constant",
and that is a null over ten comparisons — it is **not** evidence that the identity determines
`δ`, `E[inv_e]`, `(B)`'s variance diagonal or `(EQ)`. The verdict does not rest on those
rows; it rests on `e1` (a theorem), `e2.3` (a theorem), `e3.3` (an equality at `d = 1`) and
`e4.4` (the ledger). The power number is printed beside the rows for exactly this reason.

**D4 — `e2.1`, `e2.2` and `e4.2` are `n ≤ 6` and partly SAMPLED.** `n = 3, 4` are exhaustive;
`n = 5` is `sample(50–60)` and `n = 6` is `sample(25–30)`, deterministic seeds, printed in
each arm's population line. The two statements that are **proved** rather than sampled are
`E Var(pos_x|C_o) ≤ 1/4` (`e2.3`, from `Σ_y A^o_xy ≤ 1`) and `Σ_{all pairs} A_xy = n−1`
(`e3.1`, slot counting). Everything else here is consistency, not warrant.

**D5 — the frozen class is empty at every `n` I can enumerate, and three of my six arms are
about frozen-conditional targets.** `1/3–2/3` is verified to `n = 14` (mg-33f5) and a minimal
counterexample needs `n ≥ 12` refereed / `n ≥ 15` preprint (`STATE.md:213`). So `e3`'s (R)
and every `δ < 1/3` statement is measured on a population that contains **no member of the
class**. mg-345e and mg-6bc2 declared and refused the same sweep; the refusal is kept, and
`e3.5` states it in the output rather than in this file only. What survives the emptiness is
the part that is about the *relation* rather than the *class* — `e3.3`'s equality at `d = 1`
holds at a poset that exists.

**D6 — I did not file a `PREDICTIONS.md` before writing the instrument.** mg-409a's D4 says
the same thing about itself and gives the same reason; I am not entitled to the reason twice.
The one place I had a prior it **lost**: I expected `e5` to split `E[inv_e]`, and it did not
(D3). That loss is reported where it happened rather than here only.
