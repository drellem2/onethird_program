# `pairbias_independence_345e` — is the pair-bias route to `ε_spec` independent of L4?

Instrument for `mg-345e`. Deliverable document:
[`docs/OneThird-PairBias-Independence-mg-345e.md`](../../docs/OneThird-PairBias-Independence-mg-345e.md).
Predictions committed at `eb1f4b9`, **before any script here existed**.

```
./run_all.sh          # all four probes, transcripts to out_*.txt; declared exit 0
```

| probe | what it measures | declared exit |
|---|---|---|
| `selftest345e.py` | that the detectors can produce the OTHER answer — two mutation arms plus regex and block-extraction controls | 0 |
| `p1_ledger_depgraph.py` | the **recorded** dependency closure of `mg-88bd`'s claim ledger: does the supply path reach claim 4 ("L4's `F` is `n`-free")? | 0 |
| `p2_architecture_graph.py` | reachability: can L4's *hypothesis* be reached without passing through L1b's *conclusion*? | 0 |
| `p3_algebra.py` | exact-rational check of **this ticket's own** algebra — nothing already proven is re-derived | 0 |

## What this instrument is not

`p1` measures **a document**, not the mathematics. A claim whose ledger label understates its
dependencies is scored independent here; that limit prints at the top of every run, and the
`residue` channel surfaces every integer in a label cell that the edge parser did not capture, so
a missed dependency is *visible* rather than dropped. It earned its keep: claim 28's label
mentions `L4` and `C₃` with no captured edge to either, because neither is a claim in this
ledger — adjudicated by hand in the document, §4.

`p2`'s `ARCH_EDGES` is a **hand transcription** of the stated architecture with per-edge
provenance printed. Nothing mechanical checks it against the source `.tex`.

**No poset enumeration anywhere.** The frozen class `δ(P) < 1/3` is empty at every `n` this
corpus can enumerate (1/3–2/3 verified to `n = 14`, `mg-33f5`), so the attractive cheap sweep
would be measuring a hypothetical population. Declared and refused, not overlooked.

## Defects of this instrument, kept

1. **The dependency parser under-read, and the selftest caught it, not my eye.** `DEP`'s
   quantifier was lazy, so `CONDITIONAL on 1, 4, 13, 16` parsed as `1, 4` and **silently dropped
   `17 ← 13`**. Construction S4 failed and named it. Fixed; the comment in `lib345e.py` records
   it; the construction is kept. It failed in the direction that **flatters this ticket's
   verdict** — an under-reading dependency parser makes things look more independent than they
   are.
2. `p1`'s supply/demand claim partitions are **hand-chosen** from `Op-Form`'s section structure.
   A claim assigned to the wrong side would be scored against the wrong expectation.

## Prediction P9 was refuted and is kept as written

I predicted 12–20 recorded dependency edges; the ledger has **11**. I over-estimated how much of
the document's dependency structure is *recorded* rather than implicit — the same over-trust in
the ledger that the claim-28 finding punishes.
