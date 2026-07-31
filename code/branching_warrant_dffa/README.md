# `code/branching_warrant_dffa/` — the evidence for mg-dffa

**Work item:** mg-dffa. **Lands:** the four MINOR findings of
`docs/OneThird-Audit-mg-41aa-Repair.md` (mg-5800, `8ce78fb`) on
`docs/OneThird-Branching-Graphs-Where-This-Lives.md` and
`code/branching_repair_41aa/check_doc.py`. **Account:**
`docs/OneThird-Warrant-Repair-mg-dffa.md`.

**All four findings are about WARRANT.** Nothing in the target was wrong; four statements
were wider — or, for two ledger cells, narrower — than the evidence under them. **No number
moves.** This directory exists because a repair whose entire content is rewriting claim
statements is precisely where a wrong new statement is likeliest, so every sentence written
into the target was measured or located here first.

## Independence

Imports nothing from `branching_af28/`, `branching_audit_6ad0/`,
`branching_repair_41aa/` or `branching_audit_5800/`. Where a probe cites one of those it
reads the committed **output** file and says in its own output that it located a result
rather than reproducing one.

## Files

| file | what it settles |
|---|---|
| `kerndffa.py` | posets, canonical form, ideals, lattices, Young's lattice, Young–Fibonacci, skew shapes |
| `selftestdffa.py` | 42 assertions, every one that matters checked in **both** directions |
| `w1_ledger.py` | **F1** — B1 as a lattice isomorphism, re-measured; B5's two derivations, located |
| `w2_family.py` | **F2** — 33/5/28, 17 distinct `P`, 5 not skew cell posets; 30 of 30 on the Young side |
| `w3_brown.py` | **F4** — Brown `§4.3` read, located by position (needs network) |
| `w4_control.py` | **F3** — the new `check_doc.py` line fired in four configurations |
| `w5_doc.py` | the edited document read off disk: narrowings present, wide phrasings gone, mg-41aa's strikes undisturbed |
| `run_all.sh` | all of the above, ~5 s |

## The two controls that decide whether anything here is worth reading

**1. The canonical form is the definition, not a shortcut.** `canon` is the plain minimum
over all `n!` relabellings. mg-5800 recorded a control firing on its own canonical form — a
colour class chosen by dict-insertion order, which split two isomorphic 20-element lattices
**while A000112 came out exactly to 16 999**. A counting sequence is not a control on a
canonical form. Random relabelling is, and it is assertions 10–13 here.

**2. The Fibonacci rank sizes are not a control on the Young–Fibonacci cover rule.** Two
wrong cover rules were written for `yf_down_covers` before the right one. **Both returned
1, 1, 2, 3, 5, 8, 13.** They failed `DU − UD = I` by 10 and by 22 elements. The self-test
asserts that a wrong rule passes the rank-size check and fails the operator check, so the
distinction cannot rot back out. mg-5800 recorded the identical failure on its own
instrument, which is why the assertion is written that way and not merely "the rule is
right".

## Reproduce

```
./run_all.sh                                          # ~5 s, pure Python 3
cd ../branching_repair_41aa && python3 check_doc.py   # 31 checks, 0 failed
```

Committed outputs: `out_selftest.txt`, `out_w1_ledger.txt`, `out_w2_family.txt`,
`out_w3_brown.txt`, `out_w4_control.txt`, `out_w5_doc.txt`.
