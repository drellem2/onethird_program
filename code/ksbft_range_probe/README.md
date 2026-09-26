# `code/ksbft_range_probe/` — KSBFT-A: bounded-range posets computed exactly (mg-2912)

Deliverable: [`docs/KSBFT-A-range-probe.md`](../../docs/KSBFT-A-range-probe.md).
Subject: KSBFT_v7 (Aires–Chan–Pak–Panova, 2026-09-25), read from
`/Users/daniel/files/KSBFT_v7.pdf` (not in this repo). **Everything reported here is
EMPIRICAL (exact arithmetic over a stated finite population) unless marked PROVEN, and the
proofs of the PROVEN items are in §4 below.**

## 1. The instrument

| file | what it does |
|---|---|
| `probe.cpp` | C++ enumerator + exact analyser. `probe enum NMAX DMAX PREFIX`: every poset on `n ≤ NMAX` elements with range `π ≤ DMAX` up to isomorphism (DMAX=99 means all), analysed when its incomparability graph `G(P)` is connected. `probe one`: analyse posets read from stdin. `probe search N1 N2 D OBJ SEED ITERS RESTARTS`: simulated annealing for small `M` or small `δ` (HEURISTIC). |
| `exact.py` | an independent exact analyser in Python, sharing no code with `probe.cpp`: brute force over all `n!` permutations (`n ≤ 8`) and a second DP over order ideals that removes MAXIMAL elements (probe.cpp adds minimal ones). |
| `check.py` | `controls`: positive/negative controls (§3). `rederive FILES`: recompute every extreme record the enumerator kept, exactly, in Python, and require agreement on `e`, `δ`, the attaining pair, the count of attaining pairs, every height `h(x)`, `M` and `π`. |
| `report.py` | collates the per-`(n, π)` buckets of several runs into the tables of the deliverable. **Refuses** if two runs disagree on a bucket they both enumerated. |
| `fib.py` | the finite Fibonacci posets `F_N`, `N = 3..81`, exactly, including the paper's p.13 height formula as printed and a sign-corrected version. |
| `d1bound.py` | numerical check of P4 below (`M ≥ d_1 ≥ 1/(π+1)`): every labelled connected-`G` poset on `n ≤ 6` plus every kept record, with a planted false bound as its negative control. |
| `structure.py`, `describe.py`, `searchtab.py` | readers: structure of the low-`δ` records, human-readable dumps, annealing table. |
| `run_all.sh` | rebuilds, runs the controls, and regenerates every `out/` file (≈ 3.5 CPU-hours, ≈ 1.5 h wall at 3 cores; §5). |
| `out/` | committed transcripts. `summary_*.txt` per run; `<run>_n<k>.jsonl` the extreme records (top-K by `δ`, by `M`, by `(δ−C)/M²`, by the structured-triple ratio) per `(n, π)`; `report.txt`, `fib.txt`, `structure.txt`, `search_*.jsonl`, `searchtab.txt`, `controls.txt`, `rederive.txt`, `d1bound.txt`. |

**What is computed, exactly, for each poset with connected `G(P)`** (integers throughout;
`e(P)` fits in `__int128`): `e(P)` by a forward/backward DP over order ideals; for every
ordered pair the count `B[x][y]` of extensions with `x` before `y`; `h(x) = S[x]/e` with `S[x]`
the sum of positions; `δ(P) = max over incomparable x,y of min(B[x][y],B[y][x])/e` and the
attaining pairs; the height order `v_1..v_n` (ties broken by label — `M` does not depend on the
tie-break, since tied elements have equal `h`); `d_i = h(v_i) − i`; `M = max|d_i|`; width
(Dilworth via bipartite matching); every Lemma-4.1 candidate `k` (`d_k = M`, `k ≤ n−2`, or
`d_{k+2} = −M`) with `max(δ(v_k,v_{k+1}), δ(v_{k+1},v_{k+2}))`, and whether it is a BFT
triple; and every consecutive triple with the **Lemma 3.2 shape** (x ≺ z a cover, y
incomparable to exactly x and z, span `h(z) − h(x) ≤ 2`, and (3.4)–(3.5)).

**Isomorphism.** Canonical form by exhaustive individualisation–refinement (colour refinement
on down/up colour counts, first non-singleton cell, minimum adjacency code over all leaves).
Branches on TWINS (equal down-set and up-set) are pruned: the transposition of two twins not
yet individualised is an automorphism fixing every individualised vertex, so it preserves
the refined colouring and the two subtrees give the same minimum. Correctness is not argued
from the code alone: the level counts reproduce OEIS A000112 exactly for every `n ≤ 11`
(`1, 2, 5, 16, 63, 318, 2045, 16999, 183231, 2567284, 46749427`) — a canonical form that
merged non-isomorphic posets would undercount and one that failed to merge isomorphic ones
would overcount.

## 2. The population

| run | posets | n range | time |
|---|---|---|---|
| `all` (every poset) | 46 749 427 at `n = 11` | `n ≤ 11` exhaustive | 18 min |
| `d3` (`π ≤ 3`) | 34 677 549 at `n = 18` | `n ≤ 18` exhaustive | 14 min |
| `d4` (`π ≤ 4`) | 34 593 068 at `n = 15` | `n ≤ 15` exhaustive | 10 min |
| `d5` (`π ≤ 5`) | 24 861 893 at `n = 13` | `n ≤ 13` exhaustive | 6.5 min |
| `d6` (`π ≤ 6`) | 31 723 092 at `n = 12` | `n ≤ 12` exhaustive | 8 min |
| annealing, `π ≤ D`, `D ∈ {3,4,5,6,8}` | best witness per `(D, n)`; `M` with two seeds (11, 29), `δ` with one (13) | `12 ≤ n ≤ 24`, HEURISTIC | ≈ 50 min each, three runs in parallel |

The per-`(n, π)` buckets of the restricted runs coincide EXACTLY with the same buckets of
the unrestricted run wherever both exist (`report.py` refuses otherwise) — a check on the
completeness argument §4.P2, since pruning that lost a poset would lose it from a bucket.

## 3. Controls (`python3 check.py controls`, transcript `out/controls.txt`)

- **C0 positive:** the (2+1) poset has `δ = 1/3` and `M = 1/3`.
- **C1 positive:** the antichain on `n ≤ 7` has `e = n!` and `M = (n−1)/2`.
- **C2 positive, taken from the paper:** KSBFT_v7 p.12, `δ(F_m; x_i, x_{i+1}) = F_{m+i+1}F_{m−i}/F_{2m+2}`,
  checked for every `i` and `m = 1..7`. (The paper's p.13 height formula fails in sign — §D4 of the deliverable.)
- **C3 three-way agreement:** brute force over permutations = ideal DP = `probe.cpp` on 300
  random posets (`n ≤ 8`, labels shuffled).
- **C4 NEGATIVE:** a record with `δ` numerator +1 is detected as a disagreement (the
  comparison can fail).
- **C5:** the exact test against the irrational `C_BFT` places 1/3 and 0.2764 above it and 0.2763 below.
- **C6 (in `report.py`/deliverable):** the counts of connected-`G` posets satisfy the
  ordinal-sum identity `Σ P_n xⁿ = 1/(1 − Σ I_n xⁿ)` against A000112 for `n ≤ 10`.
- **Annealing control:** from a Fibonacci start the annealer re-finds the exhaustive minima
  (`M = 56/187` at n=10 and `13/45` at n=11 for `π ≤ 5`; `δ = 37/106`, `20/57`; and every
  `π ≤ 3` minimum of `M` and `δ` for `12 ≤ n ≤ 18`). Where it is below exhaustive range, a
  failure to find a smaller value **proves nothing**; a witness it finds is an exact
  certificate.

`python3 check.py rederive out/*_n*.jsonl out/search_*.jsonl` re-derives every kept extreme record
together with every annealing witness in `out/search_*.jsonl` (2 535 distinct posets, `out/rederive.txt`).

## 4. PROVEN (small facts the tables rely on)

**P1 (components).** Let the components of `G(P)` be `C_1,…,C_r`; then `P` is the ordinal sum
`C_1 ⊕ … ⊕ C_r` (in some order), and `δ(P) = max_j δ(C_j)`, `π(P) = max_j π(C_j)`,
`M(P) = max_j M(C_j)`. *Proof.* Elements of different components are comparable, and
transitivity orders whole components, so `P` is an ordinal sum and every linear extension is
a concatenation of extensions of the `C_j`. Incomparable pairs lie inside one component, and
`P[f(x)<f(y)]` for them is computed inside it. For `x ∈ C_j`, `h_P(x) = o_j + h_{C_j}(x)` with
`o_j` the size of the earlier blocks. If `|C_j| ≥ 2`, every `x ∈ C_j` has an incomparable
partner inside `C_j`, so it is neither always first nor always last there, and
`o_j + 1 < h_P(x) < o_j + |C_j|`; a singleton has `h = o_j + 1` exactly. Hence sorting by
`h` lists the blocks in order, the rank of `x` is `o_j` plus its rank in `C_j`, and
`d_P(x) = d_{C_j}(x)`. ∎ *Consequence:* the minimum of `δ` (or `M`) over non-chain posets on
`≤ n` elements with `π ≤ D` equals the minimum over connected-`G` posets on `2..n` elements
with `π ≤ D` (pad with a chain). This is why only connected-`G` posets are analysed.

**P2 (completeness of the restricted generation).** Deleting a maximal element leaves an
induced subposet in which no element gains an incomparable, so `π` does not increase; every
poset on `n` elements is its `(n−1)`-element subposet plus a maximal element whose down-set
is an order ideal. So generating level `n` from all of level `n−1` with `π ≤ D`, keeping only
`π ≤ D`, is complete. ∎

**P3 (the unconditional form of (4.1) is false; the hypothesis is doing work).** The
antichain `A_n` has `δ = 1/2`, all heights `(n+1)/2`, hence `M = (n−1)/2`. The inequality
`δ ≥ C_BFT + M²/441` then needs `(n−1)² ≤ 1764(1/2 − C_BFT) ≈ 394.5`, i.e. fails for every
`n ≥ 21`. So Lemma 4.2 cannot be tested as an unconditional statement, and its hypothesis
`δ(P) ≤ C_BFT + η_D` is met by NO poset in this population (all have `δ ≥ 1/3`), which makes
any check of the lemma as stated vacuous. What is tested instead is in the deliverable §3.

**P4 (displacement floor).** If `G(P)` is connected, `n ≥ 2` and `π(P) ≤ D`, then
`M ≥ d_1 ≥ P[v_1 not first] ≥ 1/(D+1)`. The proof is in the deliverable §3.1. It is checked by
`d1bound.py` (`out/d1bound.txt`).

## 5. Reproduce

```
sh run_all.sh          # ≈ 3.5 CPU-hours, ≈ 1.5 h wall at 3 cores; writes out/
```
Single pieces: `clang++ -O2 -std=c++17 -o probe probe.cpp`, `python3 check.py controls`,
`./probe enum 11 99 out/all`, `python3 report.py out/summary_*.txt`, `python3 fib.py 81`.
Memory: the `n = 11` level and the `π ≤ 3, n = 18` level each hold ≈ 35–47 M canonical codes
(≈ 4 GB resident). `probe` is single-threaded.

## 6. NOT done

- `n = 12` exhaustively over ALL ranges (1 104 891 746 posets) — out of the time budget.
- `π ≤ 7, 8` exhaustively beyond `n = 11`; `π ≤ 4` beyond 15; `π ≤ 5` beyond 13; `π ≤ 6` beyond 12.
  Beyond those, only annealing, which is a HEURISTIC and can miss the minimum.
- No proof of anything in the deliverable's EMPIRICAL or CONJECTURED items.
- Lemma 4.2 was not checked under its own hypothesis because no poset satisfies it (P3).
