# ksbft_one_pt — exact census of (ONE-PT) for KSBFT-J (mg-eedd)

Instrument for [`docs/KSBFT-J-one-pt.md`](../../docs/KSBFT-J-one-pt.md).

```
sh run_all.sh      # ~11 min, <= 3 processes, deterministic; poset lists live in a temp dir
```

| file | what it is |
|---|---|
| `onept.c` | generator of isomorphism classes (add a maximal element + canonical form), exact `__int128` linear-extension counter, per-poset (ONE-PT) analysis with 18 rules, margins, Lemma R check |
| `merge.py` | merges the `AGG` lines of the 3 stride-processes into one table (exact `Fraction`s) |
| `out_gen_all.txt` | class counts n=1..10 — **positive control**: equals OEIS A000112 |
| `out_gen_range.txt` | range <= 3 classes to n=16, range <= 4 to n=13 |
| `out_controls.txt` | Fibonacci closed form (n<=20), brute-force permutation cross-check, `W*(4,4,2)` every-v failure (firing) |
| `out_census_all.txt` | every non-chain class, n=3..10 |
| `out_census_indec.txt` | indecomposable (G(P) connected) classes, n=3..10 |
| `out_census_range.txt` | indecomposable range <= 3 (n=11..16) and range <= 4 (n=11..13) |
| `out_control_narrow.txt` | **firing control**: interval narrowed to [2/5,3/5]; exists-v must fail, and does |

Every table also prints `reweighting lemma R: ... violations=0` with its own firing control (`r -> r-1`
must be violated, and prints `FIRES`), and the "every v" row, which must be nonzero in every
exhaustive range (it is: the known W*-type failures).

Poset format: `n` then the strict down-sets as hex bitmasks, element i = bit i.
