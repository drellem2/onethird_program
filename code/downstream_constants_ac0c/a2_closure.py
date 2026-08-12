"""mg-ac0c `a2` — THE CLOSURE ARITHMETIC.  Does the chain close with the coarse constants in?

Every constant on the chain has a proved or a pinned value EXCEPT `ε₀` (rows 13–15) and L2's
second-disjunct constant (row 05).  So the closure question reduces to: **sweep `ε₀` over its
whole admissible range and ask, at each value, whether what L1b would have to deliver is
something the corpus can supply.**

The supply benchmark is `ε_sup(n) = n/(n+1)` — what pair bias PROVES today, and an EQUALITY
for the information it consumes (`mg-6bc2` Claim 3.1), so it cannot be improved without adding
a realizability fact.  Reading a *does not close* below as *the architecture is broken* is
wrong: it says how much better than pair bias L1b must be.  That distinction is §D.
"""

from fractions import Fraction as F
import libac0c as L

print("=" * 100)
print("a2 §A — THE LADDER: ε_dem at every value ε₀ can take, on every enumerated chain")
print("=" * 100)
print()

PINS = [
    (F(1),        "ε₀ = 1 — the LARGEST admissible value: above it Step 5's conclusion is\n"
                  "                vacuous. And it is the value at which mg-3969 Claim 5.1 finds the\n"
                  "                consumable statement trivially TRUE on every exhibitable poset."),
    (F(17, 78),   "17/78 — PROVED ceiling on the (i)-free surrogate, RESTRICTED scope\n"
                  "                (both sides non-chain), which is NOT the scope Step 6 must survive."),
    (F(1, 5),     "1/5 — the corpus's EMPIRICAL calibration. FP; says nothing above n = 7."),
    (F(1, 7),     "1/7 — PROVED ceiling on the surrogate in the REQUIRED scope at n ≤ 7."),
    (L.d3c7_leak(50), "51/5050 — mg-d3c7's family at k = 50, i.e. n = 101. PROVED, required scope."),
    (F(0),        "0 — the surrogate's UNIFORM value in the required scope. PROVED (refuted,\n"
                  "                not capped): mg-d3c7's family drives Δ₁ → 0 with every pair evicted."),
]

hdr = f"  {'ε₀':>12} | {'(I)≡(III) C₃=1':>16} | {'(II) C₃ᵍᵃᵖ=10.1654':>18} | {'(IV) c→1':>10} | {'CAP 2ε₀':>10}"
print(hdr)
print("  " + "-" * (len(hdr) - 2))
for e0, _ in PINS:
    i3 = L.chain_I_III(e0)
    ii = L.chain_II(e0, F(101654, 10000)) if e0 else F(0)
    iv = L.chain_IV(e0, F(1))
    cp = L.cap(e0)

    def f(x):
        return "—" if x is None else (f"{float(x):.6g}" if x else "0")
    print(f"  {float(e0):>12.6g} | {f(i3):>16} | {f(ii):>18} | {f(iv):>10} | {f(cp):>10}")
print()
for e0, note in PINS:
    print(f"  ε₀ = {e0}: {note}")

print()
print("=" * 100)
print("a2 §B — DOES IT CLOSE?  Each ε_dem above, against the PROVED supply ε_sup(n) = n/(n+1)")
print("=" * 100)
print()
print("  The chain closes at n iff  ε_sup(n) ≤ ε_dem.  ε_sup rises with n toward 1, so if it")
print("  fails at large n it fails where a minimal counterexample would live.")
print()
NS = [2, 7, 15, 100, 900, 10**6]
for e0, _ in PINS:
    print(f"  ── ε₀ = {e0} ─────────────────────────────────────────────────────────")
    for name, dem in [("(I)≡(III) C₃=1", L.chain_I_III(e0)),
                      ("(IV) at c→1", L.chain_IV(e0, F(1))),
                      ("CAP  2ε₀ (any chain)", L.cap(e0))]:
        verdicts = []
        for n in NS:
            c = L.closes(L.eps_sup(n), dem)
            verdicts.append("—" if c is None else ("CLOSES" if c else "no"))
        w = L.wall(L.eps_sup(10**6), dem)
        wtxt = "∞" if w is None else f"{float(w):.4g}×"
        dtxt = "— (chain absent)" if dem is None else f"{float(dem):.6g}"
        print(f"     {name:<22} ε_dem={dtxt:<16} "
              f"n={NS}: {verdicts}   wall at large n: {wtxt}")
    print()

print("=" * 100)
print("a2 §C — THE COARSE PIN ON ROW 05 (L2's second disjunct), taken at its only PROVED value")
print("=" * 100)
print()
print("  The source never names the constant in `low-conductance` (mg-fa70 §12: 5 occurrences,")
print("  0 quantified).  The ONLY universal statement available about the delivered prefix is")
print("  the trivial one:  Δ₁(A,B) ≤ 1  for 0 < |A| ≤ n/2, since |A ∖ σ(A)| ≤ |A| = min(|A|,|B|).")
print()
print("  Pinned there, the second disjunct delivers Φ_pref ≤ 1, and Step 5's conclusion needs")
print("  Φ_pref ≤ ε₀.  So the pin licenses the chain only when ε₀ ≥ 1 — the vacuous end.")
print()
for e0 in [F(1, 5), F(1, 7), F(1, 2), F(1)]:
    ok = F(1) <= e0
    print(f"     ε₀ = {e0}: trivial pin Δ₁ ≤ 1 meets Δ₁ ≤ ε₀ ?  {'YES' if ok else 'NO'}")
print()
print("  ⭐ SO THE PIN IS REAL, COARSE, AND IT MAKES THE CHAIN VACUOUS — which is the ticket's")
print("     own third option: *a value that makes the chain absurd. Take it anyway.*")
print("     In C₃ units the pin is C₃ ≤ 1/(2 ε_spec), i.e. ε_dem = ε_leak²·ε_spec, i.e. the")
print("     demand becomes ε_spec ≤ ε_leak²·ε_spec, i.e. ε_leak ≥ 1.  Same conclusion.")

print()
print("=" * 100)
print("a2 §D — THE CLOSURE REQUIREMENT, SOLVED FOR ε₀ RATHER THAN CHECKED AT PINS")
print("=" * 100)
print()
print("  mg-7564's cap is chain-free: ε_dem ≤ 2ε₀ for ANY derivation of Step 5's conclusion,")
print("  including a chain nobody has written.  So the pair-bias supply suffices only if")
print()
print("        n/(n+1)  ≤  ε_dem  ≤  2 ε₀        i.e.        ε₀  ≥  n/(2(n+1)).")
print()
for n in [2, 7, 15, 100, 900, 10**6]:
    req = F(n, 2 * (n + 1))
    print(f"     n = {n:>8}:  ε₀ must be ≥ {req} = {float(req):.6f}")
print(f"     n → ∞    :  ε₀ must be ≥ 1/2")
print()
print("  AND EVERY PROVED CEILING ON THE (i)-FREE SURROGATE IS BELOW THAT:")
REQ = F(1, 2)
for label, val in [("17/78 (restricted scope, n ≤ 7)", F(17, 78)),
                   ("1/7   (required scope, n ≤ 7)", F(1, 7)),
                   ("51/5050 (required scope, n = 101)", L.d3c7_leak(50)),
                   ("0     (required scope, uniform)", F(0))]:
    short = "∞" if val == 0 else f"{float(REQ / val):.4g}×"
    print(f"     {label:<36} {float(val):>10.6f}   short of 1/2 by {short}")
print()
print("  ⚠️ THOSE CEILINGS ARE ON THE SURROGATE `U_either`, NOT ON `ε₀^cons`.  They do not say")
print("     ε₀^cons is small — ε₀^cons is UNMEASURABLE (row 13).  What they say is that no")
print("     (i)-free UNIVERSAL argument can ever deliver the ε₀ ≥ 1/2 the closure needs.")

print()
print("=" * 100)
print("a2 §D2 — THE SAME QUESTION IN THE DENSITY CURRENCY (mg-0e8c, landed at STATE.md row 8)")
print("=" * 100)
print()
print("  ⚠️ THIS SECTION IS A CORRECTION TO §B's SCOPE, LANDED HERE RATHER THAN BY REWRITING §B.")
print("  mg-0e8c proved the supply is `ε_sup = d·n/(n+1)`, LINEAR in the incomparability")
print("  density `d = m/C(n,2)`. §B quotes it at `d = 1`, the WORST case. At small `d` the")
print("  wall is already DOWN — proven, all n, L4-free — so §B's `no` is a statement about")
print("  the DENSE regime and must be read as one.")
print()
print("  Each demand becomes meetable by pair bias exactly at `d ≤ ε_dem·(n+1)/n`:")
print()
print(f"  {'ε₀':>12} | {'chain (I)≡(III) ε_dem':>22} | {'closes at density d ≤ (n→∞)':>28}")
print("  " + "-" * 68)
for e0, _ in PINS:
    dem = L.chain_I_III(e0)
    dt = L.d_threshold(dem, 10**6)
    print(f"  {float(e0):>12.6g} | {float(dem):>22.6g} | "
          f"{'— never —' if dt is None else f'{float(dt):>28.6g}'}")
print()
print("  ⭐ EVEN AT THE VACUOUS `ε₀ = 1`, chain (I)≡(III) closes only at `d ≲ 1/2`.")
print("     So for the architecture's own chain to close on pair bias at ANY `ε₀`, residual")
print("     (R) — STATE.md's own *do frozen posets have a density ceiling `d ≤ D < 1`?* —")
print("     would have to be answered at `D ≲ 1/2`. That is a NEW consumer for (R), which")
print("     STATE.md lists as elementary and open, and it prices it: `D ≲ 1/2` at the most")
print("     generous `ε₀` conceivable, `D ≲ 2×10⁻²` at the live calibration — which is")
print("     mg-0e8c's own dense-regime figure, reached from the demand side.")

print()
print("=" * 100)
print("a2 §E — THE DIAL: the two open lemmas pull OPPOSITE WAYS in ε₀")
print("=" * 100)
print()
print(f"  {'ε₀':>10} | {'L1b must deliver ε_spec ≤ (chain I/III)':>40} | what L4 must then be")
print("  " + "-" * 96)
for e0, tag in [(F(1, 50), "the superseded 2×10⁻⁴ calibration"),
                (F(1, 7), "already ABOVE the required-scope n ≤ 7 ceiling"),
                (F(1, 5), "the live calibration — 40% above that ceiling"),
                (F(17, 78), "above the restricted-scope ceiling too"),
                (F(1, 2), "the value the CAP needs for closure at pair bias"),
                (F(1), "L4 at Δ₁ ≤ 1 — i.e. EVERY cut — i.e. the conjecture")]:
    dem = L.chain_I_III(e0)
    factor = L.eps_sup(10**6) / dem
    print(f"  {str(e0):>10} | ε_spec ≤ {float(dem):<12.6g} "
          f"({float(factor):>8.4g}× better than pair bias) | {tag}")
print()
print("  ⭐ THERE IS NO SETTING OF ε₀ AT WHICH BOTH HALVES ARE CHEAP. Raising ε₀ relaxes L1b")
print("     and strengthens L4 — and L4 passes the point where its own (i)-free surrogate is")
print("     already refuted (1/7 in the required scope at n ≤ 7) BEFORE L1b's demand becomes")
print("     anything pair bias can meet (ε₀ ≥ 1/2 at the cap; ε₀ > 1 on chain (I)/(III)).")
