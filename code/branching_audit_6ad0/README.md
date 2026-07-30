# `branching_audit_6ad0` — independent audit instrument for mg-af28 / 358beff

Built for mg-6ad0. **Shares no code with `code/branching_af28/`** or with any other
instrument in this repo. It re-derives every object it needs.

Deliberate representation differences from `core_af28.py`, so that agreement is evidence:

| object | `core_af28.py` | here |
|---|---|---|
| poset | tuple of up-set **bitmasks** | `(n, down)` with `down[i]` a **frozenset** of elements below |
| poset enumeration | one-point extension by a new **maximal** element | **naturally labelled** posets, choosing each element's down-set |
| canonical form | min over `n!` relabellings of a bitmask tuple | min over **colour-refined** relabellings of an adjacency **string** |
| order ideals | per-subset bitmask filter | **downward closure** of every subset |
| `f^lambda` | **hook length formula** | **branching recursion** |
| `[0, lambda]` | containment filter on partitions | generated from the **add-a-corner cover rule**, closed downwards |
| `dim kF(P)/rad` | rank of the **trace form** + Dickson's theorem | **characters + nilpotent kernel**, no cited theorem |

## Files

| file | what it does |
|---|---|
| `kern6ad0.py` | the kernel |
| `selftest6ad0.py` | **68 assertions** against A000112, A000110, A000670, `n!`, `sum (f^lam)^2 = n!`, M3, N5. Nothing else here is evidence if this does not pass |
| `a1_contact.py` | ledger **B1** re-tested as an equality, and strengthened to a **lattice** isomorphism |
| `a2_intervals.py` | **refutation by construction** of ledger **B2** and of §0 consequence 3's grid sentence; corrected counts |
| `a3_hypotheses.py` | **B3**, **B4**, **B6**, **B7** — including which of them can fail at all, and the 28 Young–Fibonacci intervals that Brown §4.3 does consume |
| `a4_algebra.py` | **B5** without the trace form; §5 item 5(a) and 5(b) |
| `a5_scan.py` | **B8** re-run with **ligature-aware** matching and ligature-bearing controls *(network)* |
| `a6_quotes.py` | the two verbatim quotations re-read from the PDFs *(network)* |

## Reproduce

```
./run_all.sh          # ~30 s of compute, plus two network fetches
SKEW8=1 python3 a2_intervals.py    # adds the n=8 row, ~4 min
```

## Caps, listed rather than hidden

* `a4_algebra.py` skips posets with `|F(P)| > 90` — **20 classes at n = 5**, each listed with
  its `|F(P)|` in `out_a4_algebra.txt`. Nothing is skipped at `n <= 4`.
* `a2_intervals.py` runs to `n = 7` by default; the `n = 8` row is behind `SKEW8=1`.
* `a3_hypotheses.py` runs Young–Fibonacci to rank 6, matching af28's T8 so the numbers
  are comparable.
* `a1_contact.py` runs all 44 partitions to `n <= 7`, the same range as af28's T1.
