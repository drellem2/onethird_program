# audit_ksbft_6e7c — independent audit of mg-ce69 (KSBFT-Q2)

Instrument for [`docs/AUDIT-mg-6e7c.md`](../../docs/AUDIT-mg-6e7c.md). Pure Python, exact integers/Fractions, no
code shared with `../ksbft_q2_both_ends_ce69/`. `sh run_all.sh` (~3 min, ≤ 3 processes) regenerates every
transcript and exits 1 if any figure the audit relies on changes (`check.py`) or a control is missed.

| file | role |
|---|---|
| `aud.py` | three probability engines (ideal DP, added-relation count e(P+{a<b})/e(P), explicit enumeration); ladders; |Aut| |
| `gencheck.py` | census files complete and duplicate-free: Σ n!/|Aut| = OEIS A001035 for n ≤ 9 → `out_gencheck.txt` |
| `witnesses.py` | every witness number of mg-ce69; Q_m rebuilt from the prose; B7 tail sensitivity; my B7-glued both-ends family → `out_witnesses.txt` |
| `census.py` | Thm 1.4 / Lemma 1.5 / Pinch / C-prefix checks, SL ⟺ nested-balanced equivalence, Zaguia and Cor 1.6 counts, 5 firing controls → `out_census_*.txt` |
| `pinch.py`, `release.py`, `reduction.py` | Lemma 1.2, Lemma 1.3 (explicit enumeration), P-vs-R twin balance |
| `negative_control.py` | planted falsehoods, all must print CAUGHT → `out_negative_control.txt` |
| `check.py` | asserts the audit's figures → `out_check.txt` |

Census posets come from mg-eedd's generator (`../ksbft_m_margin_6b81/pcert.c`, `onept gen`), certified by `gencheck.py`.
