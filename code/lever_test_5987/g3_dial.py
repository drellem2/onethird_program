#!/usr/bin/env python3
"""mg-5987 `g3` — STEP 3: *if it is a graded family, what does the WHOLE dial do?*

`mg-9b6b`'s finding was that the `(1_D)` dial was worth pricing away from the one point anybody had
evaluated, because the provable end and the useful end are what show the shape.  Both residuals
here are graded families in exactly the same way — the constant is the dial — so step 3 applies
verbatim, and this arm runs it.

WHAT IT TAKES TO RUN IT, AND WHY THIS ARM IS SHORTER THAN mg-9b6b's.  Pricing a dial END TO END
needs the primitive floor at EVERY `n`, not at the ones a census reaches.  `mg-9b6b` had one:
`floor_d(n) = 2/n` is a THEOREM (a primitive poset has an incomparable pair at every element, so
`m ≥ n/2`), which is what let it write `forbids up to n = 98` and count 84 UNREACHED orders.
Neither residual here has such a theorem, and `g2` measured the floor only to `n = 8` — every one
of them already verified.  So this arm pins the two ENDS of each dial, which is what can be done
without one:

    the far end   — an EXPLICIT PRIMITIVE FAMILY caps the floor at every `n`, so above the cap the
                    price is 0 orders at every order, not merely at the swept ones;
    the near end  — below `g2`'s measured floor the price is every order the census can see.

and reports the gap between them as the gap it is.
"""

import json
import os
import sys
from fractions import Fraction

import lib5987 as M
import lib6ff4 as L

# g2's measured floors, READ rather than copied.  A figure typed into two files goes stale in one
# of them (mg-2959), and this arm's whole near-end column is g2's measurement.  If the file is not
# there this arm says so and prints no number, which is the only honest alternative to a stale one.
FLOORS = None
_fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "floors.json")
if os.path.exists(_fp):
    _raw = json.load(open(_fp))
    FLOORS = {k: {int(n): Fraction(v) for n, v in d.items()} for k, d in _raw.items()}


def near_end(key):
    """The largest `C` at which g2's swept orders are ALL delivered: `C < min_n floor(n)`."""
    if FLOORS is None:
        return "NOT AVAILABLE — run g2_step2.py first (floors.json absent)"
    m = min(FLOORS[key].values())
    return f"C < {m} = {float(m):.6f}"

print("=" * 96)
print("mg-5987  g3 — STEP 3: THE WHOLE DIAL, BOTH RESIDUALS")
print("=" * 96)

print("""
§1. THE FAMILY THAT CARRIES BOTH DIALS PAST THE CENSUS.  `Z_n`: `x_i < x_j` iff `j − i ≥ 2`, so
    the incomparable pairs are exactly the consecutive ones and `L(Z_n)` is in bijection with the
    MATCHINGS of a path.  Everything below is closed form; `g0` checks it term for term against the
    general machinery at n = 3…11.

        |L(Z_n)| = F_{n+1}        q_i = Pr[(i,i+1) transposed] = F_i F_{n−i} / F_{n+1}
        h(x_i) − i = q_i − q_{i−1}          C_{x_i} = 2 q_i q_{i−1}          E[inv_e] = Σ q_i

    ⚠️  `Z_n` IS PRIMITIVE AT EVERY `n` — its incomparability graph is a path — which is the whole
    reason it can carry a verdict where mg-9b6b's ordinal-sum family could not: mg-f5be's
    primitivity objection lapsed that refutation above n = 3 and does not touch this one.
""")
print("      n |     |L(Z_n)| | max_x |h − rank_e| | Σ C_x / E[inv_e]")
print("   -----+--------------+--------------------+------------------")
for n in (3, 4, 5, 8, 14, 15, 20, 50, 100, 300):
    cf = M.zigzag_closed_form(n)
    b, r = cf["bias"], cf["rho"]
    ext = str(cf["ext"]) if cf["ext"] < 10 ** 10 else f"F_{n + 1}, {len(str(cf['ext']))} digits"
    print(f"   {n:4d} | {ext:>12s} | {str(b) if n <= 8 else '':7s} {float(b):.6f} |"
          f" {str(r) if n <= 5 else '':6s} {float(r):.6f}")
print(f"""
    Both columns CONVERGE and neither runs away:

        max_x |h − rank_e| = F_{{n−1}}/F_{{n+1}} → 1/φ² = (3−√5)/2 = {(3 - 5 ** 0.5) / 2:.6f}
        Σ C_x / E[inv_e]                    → 1 − 1/√5      = {1 - 5 ** -0.5:.6f}

    and the first is EXACTLY `q_1`, attained at the end of the path: `b_1 = q_1 − q_0 = q_1`.
""")

print("""
§2. AND THE CAP IS A THEOREM, NOT A LIMIT.  A limit says what happens eventually; the price needs
    a bound at EVERY n.  Both come from one Fibonacci identity, checked below rather than cited:

        F_{a+b−1} = F_a F_b + F_{a−1} F_{b−1}   ⟹   F_i F_{n−i} ≤ F_{n−1}   ⟹   q_i ≤ q_1

    so    max_x |h − rank_e| = q_1 = F_{n−1}/F_{n+1} ≤ 2/5           at every n ≥ 3
    and   Σ C_x / E[inv_e]   = 2 Σ q_i q_{i−1} / Σ q_i ≤ 2 q_1 ≤ 4/5  at every n ≥ 3
""")
bad_id = [(a, b) for a in range(1, 40) for b in range(1, 40)
          if M.fib(a + b - 1) != M.fib(a) * M.fib(b) + M.fib(a - 1) * M.fib(b - 1)]
bad_q = [(n, i) for n in range(3, 200) for i in range(1, n)
         if M.fib(i) * M.fib(n - i) > M.fib(n - 1)]
bad_cap = [n for n in range(3, 400)
           if M.zigzag_closed_form(n)["bias"] > Fraction(2, 5)
           or M.zigzag_closed_form(n)["rho"] > Fraction(4, 5)]
sup_b = max(M.zigzag_closed_form(n)["bias"] for n in range(3, 400))
sup_r = max(M.zigzag_closed_form(n)["rho"] for n in range(3, 400))
print(f"    identity F_{{a+b−1}} = F_a F_b + F_{{a−1}} F_{{b−1}}, a,b ≤ 39 ....... {len(bad_id)} failures")
print(f"    q_i ≤ q_1 at every n ≤ 199 and every i .......................... {len(bad_q)} failures")
print(f"    both caps hold at every n ≤ 399 ................................ {len(bad_cap)} failures")
print(f"    sup over n ≤ 399:  bias = {sup_b} (at n = 4),  ρ = {float(sup_r):.6f}")

print("""
§3. THE DIAL, IN mg-9b6b's OWN TABLE SHAPE.  `D`/`C` from the end nothing consumes to the end
    everything does.  ⚠️  THE `unreached` COLUMN IS THE ONE TO READ AND FOR TWO OF THE THREE ROWS
    IT CANNOT BE FILLED: it counts orders above the census frontier of 14, and that needs the floor
    at n > 14, which for (R) is the theorem `2/n` and for these two is nothing at all.
""")
rd = [n for n in range(3, 400) if M.V.primitive_floor(n) > M.V.d_needed(n)]
print("    residual   | setting                     | delivers            | unreached (n > 14)")
print("   ------------+-----------------------------+---------------------+--------------------")
print(f"    (R)        | F26, PROVEN                 | nothing             | 0")
print(f"    (R)        | ε_dem·(n+1)/n  — row 8      | n = 3…{max(rd):<14d}| {len([n for n in rd if n > 14])}")
print(f"    (R)        | F23's 4⌊n/3⌋/(n(n−1))       | every n ≥ 4         | all of them")
print( "    (EQ)       | C ≥ 2/5      — the cap      | NOTHING, at every n | 0, at every n")
print(f"    (EQ)       | {near_end('bias'):27s} | every n = 3…8       | NOT COMPUTABLE HERE")
print( "    (B-cov)    | C ≥ 4/5      — the cap      | NOTHING, at every n | 0, at every n")
print(f"    (B-cov)    | {near_end('rho'):27s} | every n = 3…8       | NOT COMPUTABLE HERE")
print("""
    THE TWO `NOT COMPUTABLE` CELLS ARE THE FINDING, NOT A GAP IN THE SWEEP.  mg-9b6b's currency is
    unreached orders; unreached orders are a function of the primitive floor above n = 14; and the
    floor above n = 14 is a THEOREM for `d` and an open question for both of these.  No amount of
    census closes that cell — a sweep to n = 12 would still be inside the verified range.
""")

print("""
§4. WHERE THE ANSWER FLIPS, AND WHAT SITS THERE.  The two ends disagree, so there is a crossing,
    and the whole verdict is a question of which side the architecture's own constant is on.
""")
print( "    (EQ):     0 orders at every n for  C ≥ 2/5 = 0.400000        (theorem, §2)")
print(f"              every swept order for   {near_end('bias'):28s} (census to n = 8, g2)")
print( "    (B-cov):  0 orders at every n for  C ≥ 4/5 = 0.800000        (theorem, §2)")
print(f"              every swept order for   {near_end('rho'):28s} (census to n = 8, g2)")
print(f"""
    Against them, what the architecture names: ε_dem = {M.EPS_DEM} = {float(M.EPS_DEM):.4f}, and
    STATE.md records the constant that SUFFICES as unpinned by ~2 orders of magnitude (audit F5).

        the flip for (EQ)     sits at   ≈ 0.3 – 0.4   =  15× – 20× ε_dem
        the flip for (B-cov)  sits at   ≈ 0.4 – 0.8   =  20× – 40× ε_dem

    A 2-orders-of-magnitude window on the required constant spans BOTH flips.  So the record as it
    stands cannot say which side either residual is on, and *"is it a lever?"* is not answerable
    from the mathematics of the residual alone — it is answerable from a constant nobody has
    computed end to end.
""")

print("""
§5. WHAT WOULD MAKE THE TEST RETURN AN ANSWER — one object, named so it can be looked for.

    A THEOREM ABOUT `floor_Q(n)` — the analogue of `d ≥ 2/n` for either quantity.  Two shapes and
    they answer opposite ways, which is what makes it worth doing:

      (a) `floor_Q(n) ≥ c > 0` at every n.  Then every C < c delivers EVERY order — the whole
          conjecture in one step, mg-9b6b's data end — and the residual is dead at every setting
          below c, with no cutoff at all.  Note this is WORSE than (R): (R)'s delivery STOPS at
          n = 2/D precisely because its floor decays past D.  A floor that does not decay never
          gets overtaken, so the initial segment is everything.

      (b) `floor_Q(n) → 0`.  Then each fixed C has a cutoff `n_C` and the price is finite and
          computable, exactly as for (R) — and the number of UNREACHED orders it buys becomes a
          figure somebody can put in this table instead of `NOT COMPUTABLE HERE`.

    The measured floors are consistent with both and settle neither.  They are NOT monotone, which
    is reported rather than smoothed — and they are read from g2 rather than copied:
""")
if FLOORS is None:
    print("    NOT AVAILABLE — run g2_step2.py first (floors.json absent).")
else:
    for key, name in (("bias", "(EQ)   "), ("rho", "(B-cov)")):
        row = "  ".join(f"{str(FLOORS[key][n]):>7s}" for n in sorted(FLOORS[key]))
        dec = "  ".join(f"{float(FLOORS[key][n]):7.4f}" for n in sorted(FLOORS[key]))
        print(f"    {name} floor, n = 3…8:  {row}")
        print(f"                           {dec}")
sys.exit(0)
