# ksbft_r_window_padding_7bfc — instrument for KSBFT-R (mg-7bfc)

Instrument for [`docs/KSBFT-R-window-padding.md`](../../docs/KSBFT-R-window-padding.md).
Computation here is an INSTRUMENT only (ticket rule). Every poset is a named witness from the record
or an explicit padding of one. There is no census and no search.

```
sh run_all.sh     # ~1 s, one process, exact integers / Fractions, deterministic; asserts every control
```

| file | what |
|---|---|
| `lib.py` | Exact linear-extension statistics from one pass over the ideal lattice: pair laws, slot laws, δ. Also range, both connectivities, modules/primality, and the paddings `attach_low`, `attach_both` and `hub`. |
| `pad.py` → `out_pad.txt` | §1 exact paddings (+, ⊕, substitution), with a NEGATIVE CONTROL: a non-module embedding must change the law. §2 Fibonacci insulation: the closed form of Thm 2.1 against the DP, exact equality; primality, with a control that must find a module. §3 `W*_t` decomposable; insulated `W*`: (T∃) holds and `Δ₁` is small. §4 probe-B certificate on padded `F_N`, including the prime range-8 poset with no certificate. §5 probe-D G-blindness padded. §6 hub / double-hub padding of `2+2`; the control catches the single hub's non-chain module. §7 whether the A28 finite witnesses already lie in the window. |

Controls that must fire (asserted by `run_all.sh`):
- NEGATIVE CONTROL: `attach_low(F_7,3)` changes 6/6 pair laws, so the exactness claim is CAUGHT when the module hypothesis fails.
- `attach_low(F_12,3)` is NOT prime, so the primality test CAUGHT a module.
- The single hub `hub(2+2,{a1,a2,b2},8)` has the non-chain module `{a2,b2,c_1..c_7}`, and the module test finds it.
- Probe-B soundness: on every pair, the bound is at most `min(p,1−p)`. This is a consistency check.
