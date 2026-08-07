"""mg-8311 R4 — THE CONSEQUENCES. This is the actual deliverable.

The ticket: "A repair that fixes the function and does not re-run what depended on it has
done the easy half." So this script re-runs what depended on it, BEFORE and AFTER, side by
side, on mg-2de0's OWN population.

How the population is obtained, and why: `named_posets` and `all_posets` are imported from
`lib2de0` itself. They are not the defective code -- the defect is in `E_leak` alone (R3.2
established that by parsing) -- and importing them is the only way to be certain the
population is mg-2de0's 431 posets and not a lookalike of mine that happens to have 431
members. The LEAK ARITHMETIC is mine: each of mg-2de0's Poset objects is re-wrapped as a
P8311 carrying the same (n, rel), and both conventions are evaluated by lib8311. So the
population is theirs and the measurement is mine.

Every figure below is printed in TWO columns, `convention` and `definition`. The convention
column is a REPRODUCTION of what mg-2de0 published; where it fails to reproduce, that is
reported as a failure of this script to reproduce, not as a new finding about mg-2de0.

OPERATOR SCOPE: Phi_P / Phi* / Delta_1 only. No eigenvalue. Transport axis.
"""

import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                os.pardir, "direct_prefix_audit_2de0"))
from lib2de0 import named_posets, all_posets            # POPULATION ONLY -- see docstring

from lib8311 import P8311, antichain, Tally

T = Tally()

print("=" * 78)
print("R4 — THE CONSEQUENCES: every Phi figure mg-2de0 published, before and after")
print("=" * 78)

# ---------------------------------------------------------------------------
print()
print("R4.1  mg-2de0's OWN population, imported from lib2de0 and re-wrapped so that the")
print("      leak arithmetic is this instrument's and the poset list is theirs:")
raw = named_posets(7) + all_posets(4) + all_posets(5)
POP = [P8311(P.n, P.rel, P.name) for P in raw]
cuts = sum(2 ** P.n - 2 for P in POP)
print(f"       posets: {len(POP)}   (mg-2de0's a3_nonvacuity.py prints 431)")
print(f"       cuts:   {cuts}   (mg-2de0's a3_nonvacuity.py prints 12702)")
T.report("population reproduces mg-2de0's 431 posets / 12702 cuts",
         (0 if len(POP) == 431 else 1) + (0 if cuts == 12702 else 1), 2,
         "two integer equalities against the counts printed in out_a3_nonvacuity.txt",
         "named_posets(7) + all_posets(4) + all_posets(5), all 2^n-2 proper cuts each")

# ---------------------------------------------------------------------------
print()
print("R4.2  A3.2 / P9 FIRST HALF — `Phi_P(A) <= 1 for every cut`, published `0 / 12702`.")
b = {"conv": 0, "def": 0}
for P in POP:
    for A in P.cuts():
        for w in ("conv", "def"):
            if P.phi(A, w) > 1:
                b[w] += 1
print(f"       convention: {b['conv']} / {cuts}      definition: {b['def']} / {cuts}")
T.report("A3.2 reproduces under the convention (0 / 12702)", b["conv"], cuts,
         "per-(poset, cut), exact Fraction comparison against 1",
         "mg-2de0's 431 posets x all 12702 proper cuts")
T.report("A3.2 STILL HOLDS under the definition", b["def"], cuts,
         "per-(poset, cut), exact Fraction comparison against 1",
         "the same 12702 pairs")
print("       => P9's FIRST HALF DOES NOT MOVE. `0 / 12702` is correct as published and")
print("          stays correct after the repair. Forced by PREDICTIONS.md H6, which proved")
print("          it by hand for both conventions before this script existed: the")
print("          convention's leak is |A\\P| = |P\\A| with |P| = |A|, hence <= |A^c|.")

# ---------------------------------------------------------------------------
print()
print("R4.3  A3.4 / P9 SECOND HALF — `Phi* <= min_k Delta_1(A_k)`, published `0 / 431`,")
print("      AND the figure inside it: `strictly smaller on 65 of 431 posets`.")
viol = {"conv": 0, "def": 0}
strict = {"conv": 0, "def": 0}
moved_strict = []
for P in POP:
    m = P.prefix_min()
    s = {}
    for w in ("conv", "def"):
        ps = P.phi_star(w)
        if ps > m:
            viol[w] += 1
        s[w] = ps < m
        if s[w]:
            strict[w] += 1
    if s["conv"] != s["def"]:
        moved_strict.append((P.name, P.phi_star("conv"), P.phi_star("def"), m,
                             s["conv"], s["def"]))
print(f"       violations of Phi* <= m_pre:  convention {viol['conv']} / {len(POP)}      "
      f"definition {viol['def']} / {len(POP)}")
T.report("A3.4's `0 / 431` reproduces under the convention", viol["conv"], len(POP),
         "per-poset, exact Fraction comparison", "mg-2de0's 431 posets")
T.report("A3.4's `0 / 431` STILL HOLDS under the definition", viol["def"], len(POP),
         "per-poset, exact Fraction comparison", "the same 431 posets")
print("       => P9's SECOND HALF DOES NOT MOVE either. Forced by H7: Phi* is a minimum")
print("          over a family containing the prefixes, and R1.4 measured the two")
print("          conventions agreeing on every prefix of e.")
print()
print(f"       STRICT count:  convention {strict['conv']} / {len(POP)}      "
      f"definition {strict['def']} / {len(POP)}")
T.report("the published `strictly smaller on 65 of 431` reproduces under the convention",
         0 if strict["conv"] == 65 else 1, 1,
         "integer equality against the figure in out_a3_nonvacuity.txt:80 and "
         "docs/OneThird-Direct-Prefix-Route-mg-2de0-Audit.md:202",
         "mg-2de0's 431 posets")
print()
if strict["def"] != strict["conv"]:
    print("       *** THIS FIGURE MOVES. ***")
    print(f"       `strictly smaller on 65 of 431` becomes "
          f"`strictly smaller on {strict['def']} of 431`.")
    print(f"       {len(moved_strict)} posets change side. Direction of each:")
    up = sum(1 for r in moved_strict if r[5] and not r[4])
    dn = sum(1 for r in moved_strict if r[4] and not r[5])
    print(f"         became strict (Phi* fell below m_pre after repair): {up}")
    print(f"         became equal  (Phi* rose to m_pre after repair):    {dn}")
    print(f"       {'poset':>26s} {'Phi*_conv':>10s} {'Phi*_def':>10s} {'m_pre':>8s}  side change")
    for nm, pc, pd, m, sc, sd in moved_strict[:12]:
        print(f"       {nm:>26s} {str(pc):>10s} {str(pd):>10s} {str(m):>8s}  "
              f"{'equal->strict' if sd else 'strict->equal'}")
    if len(moved_strict) > 12:
        print(f"       ... and {len(moved_strict) - 12} more (full list is deterministic "
              f"and re-derivable by re-running this script)")
else:
    print(f"       this figure DOES NOT move: {strict['def']} of 431 both ways.")
T.report("PREDICTIONS.md P8 -- `65 of 431` moves",
         0 if strict["def"] != strict["conv"] else 1, 1,
         "integer inequality between the two columns",
         "mg-2de0's 431 posets", fatal=False)

# ---------------------------------------------------------------------------
print()
print("R4.4  A3.5 — `Phi* == min_k Delta_1(A_k) at the antichain`, published `0 / 6`.")
b = {"conv": 0, "def": 0}
tot = 0
for P in POP:
    if not P.name.startswith("antichain"):
        continue
    tot += 1
    m = P.prefix_min()
    for w in ("conv", "def"):
        if P.phi_star(w) != m:
            b[w] += 1
print(f"       convention: {b['conv']} / {tot}      definition: {b['def']} / {tot}")
T.report("A3.5 holds under BOTH conventions", b["conv"] + b["def"], 2 * tot,
         "per-antichain, exact Fraction equality",
         f"the {tot} antichains in mg-2de0's population (n=2..7)")
print("       => DOES NOT MOVE. Forced by H5: over all n! permutations both sigma(A) and")
print("          set(p[:a]) are uniform random a-subsets, so both leaks equal a(n-a)/n and")
print("          the two conventions COINCIDE at every antichain cut. Verified directly:")
bad = tt = 0
for P in POP:
    if not P.name.startswith("antichain"):
        continue
    for A in P.cuts():
        tt += 1
        if P.E_leak(A, "conv") != P.E_leak(A, "def"):
            bad += 1
T.report("the two conventions COINCIDE at every antichain cut", bad, tt,
         "per-(antichain, cut), exact Fraction equality of the two expectations",
         f"antichains n=2..7, all 2^n-2 cuts each = {tt} pairs")
print("       => so mg-2de0's 1/2, 2/3, sqrt(2) and 4/3 arithmetic -- ALL of it evaluated")
print("          at the antichain -- is untouched by this repair. A3.1, A3.3 and A3.6 do")
print("          not move, and neither does anything A4 or A5 reports.")

# ---------------------------------------------------------------------------
print()
print("R4.5  HOW FAR the underlying Phi* actually moved, which is the honest measure of")
print("      the blast radius even where no published verdict changed:")
moved = lower = higher = 0
worst = None
for P in POP:
    pc, pd = P.phi_star("conv"), P.phi_star("def")
    if pc != pd:
        moved += 1
        if pd < pc:
            lower += 1
        else:
            higher += 1
        d = pc - pd
        if worst is None or abs(d) > abs(worst[1]):
            worst = (P.name, d, pc, pd)
print(f"       Phi* changed on {moved} of {len(POP)} posets "
      f"({100.0 * moved / len(POP):.1f}%)")
print(f"         repaired Phi* is LOWER on  {lower}")
print(f"         repaired Phi* is HIGHER on {higher}")
if worst:
    print(f"       largest change: {worst[0]}  {worst[2]} -> {worst[3]}  "
          f"(delta {worst[1]})")
T.report("PREDICTIONS.md P10 -- the moved count lands in [150, 350]",
         0 if 150 <= moved <= 350 else 1, 1,
         "integer range test on the count above", "mg-2de0's 431 posets", fatal=False)
print("       and per-cut, on mg-2de0's own 12702 pairs rather than R2's 11316:")
d = 0
for P in POP:
    for A in P.cuts():
        if P.E_leak(A, "conv") != P.E_leak(A, "def"):
            d += 1
print(f"       E_leak differs on {d} of {cuts} (poset, cut) pairs "
      f"({100.0 * d / cuts:.1f}%)")
print()
print("       the set of posets whose Phi* MOVES and the set mg-2de0 published as")
print("       STRICTLY SMALLER are the SAME SET, which is why both counts read 65:")
mv = {P.name for P in POP if P.phi_star("conv") != P.phi_star("def")}
st = {P.name for P in POP if P.phi_star("conv") < P.prefix_min()}
T.report("{Phi* moves} == {strict under the convention}", 0 if mv == st else 1, 1,
         "set equality on poset names", f"mg-2de0's {len(POP)} posets")
print("       => forced, once the direction is known: Phi*_def >= Phi*_conv and")
print("          Phi*_def <= m_pre, so Phi* moving implies Phi*_conv < m_pre. The")
print("          repair acts on EXACTLY the posets A3.4's figure counts, and on no others.")

# ---------------------------------------------------------------------------
print()
print("R4.5b WHY PREDICTIONS.md P9 LOST, measured rather than explained away. P9 bet the")
print("      convention only ever OVER-charges, and inferred that the repair would LOWER")
print("      Phi* and RAISE the strict count. R2.4 refuted the pointwise claim (2122 of")
print("      11316 under-charges) and R4.3/R4.5 refuted the direction too: Phi* rose on")
print("      all 65 movers and the count FELL, 65 -> 16. The two facts are not in tension,")
print("      and here is the reason, as a measurement:")
pop_over = pop_under = pop_eq = 0
arg_over = arg_under = arg_eq = 0
for P in POP:
    best = None
    for A in P.cuts():
        c, dd = P.E_leak(A, "conv"), P.E_leak(A, "def")
        if c > dd:
            pop_over += 1
        elif c < dd:
            pop_under += 1
        else:
            pop_eq += 1
        v = P.phi(A, "conv")
        if best is None or v < best[0]:
            best = (v, c, dd)
    _, c, dd = best
    if c > dd:
        arg_over += 1
    elif c < dd:
        arg_under += 1
    else:
        arg_eq += 1
print(f"       over ALL {cuts} cuts:              conv > def on {pop_over}, "
      f"< on {pop_under}, == on {pop_eq}")
print(f"       at the {len(POP)} cuts ATTAINING Phi*_conv: conv > def on {arg_over}, "
      f"< on {arg_under}, == on {arg_eq}")
print("       => the convention over-charges on the MAJORITY of cuts and under-charges at")
print("          the cuts that attain the MINIMUM. Phi* is an extremal statistic, so the")
print("          population sign carries no information about it -- the minimum is attained")
print("          exactly where the error runs the other way. That is the whole content of")
print("          P9's loss, and it is a caution worth more than the prediction was: an")
print("          aggregate sign is not a bound on an extremum.")

# ---------------------------------------------------------------------------
print()
print("R4.6  the SELFTEST drills that reach Phi, each evaluated under both conventions,")
print("      so the repair's effect on mg-2de0's own red-team file is known in advance:")
A4 = antichain(4)
rows = [
    ("S7 Phi(antichain n=4, A={0}) == 3/4",
     A4.phi(frozenset({0}), "conv"), A4.phi(frozenset({0}), "def"), F(3, 4)),
    ("S7 Phi* (antichain n=4) == 1/2",
     A4.phi_star("conv"), A4.phi_star("def"), F(1, 2)),
    ("S7 Phi* == min over prefixes at antichain n=4",
     A4.phi_star("conv"), A4.phi_star("def"), A4.prefix_min()),
]
print(f"       {'drill':>44s} {'conv':>8s} {'def':>8s} {'expects':>8s}  verdict")
bad = 0
for label, c, dd, exp in rows:
    ok = (c == exp and dd == exp)
    if not ok:
        bad += 1
    print(f"       {label:>44s} {str(c):>8s} {str(dd):>8s} {str(exp):>8s}  "
          f"{'both pass' if ok else 'CHANGES'}")
T.report("all three antichain Phi drills pass under BOTH conventions", bad, len(rows),
         "per-drill, exact Fraction equality in both columns",
         "selftest2de0.py's S7 drills at lines 139, 144, 145")
n4 = [P8311(P.n, P.rel, P.name) for P in all_posets(4)]
ex = {w: sum(1 for P in n4 if P.phi_star(w) < P.prefix_min()) for w in ("conv", "def")}
print(f"       S7 `at least one n=4 poset has Phi* < prefix minimum`: "
      f"conv {ex['conv']} of 40, def {ex['def']} of 40")
T.report("selftest line 148's existence drill survives the repair",
         0 if ex["def"] > 0 else 1, 1, "integer positivity",
         "all 40 labelled posets on 4 elements")
print("       => the drill SURVIVES, but its comment cites `A3.4's strictly smaller on")
print("          65 of 431` by number, so that comment must be retargeted with the figure.")

# ---------------------------------------------------------------------------
print()
print("R4.7  THE LEDGER OF PUBLISHED FIGURES. Every site that carries a Phi number from")
print("      mg-2de0, and whether the repair moves it. Sites located by grep and READ.")
LEDGER = [
    ("docs/OneThird-Direct-Prefix-Route-mg-2de0-Audit.md:183",
     "`Phi_P(A) <= 1` on all 12702 (poset, cut) pairs", "NO"),
    ("docs/OneThird-Direct-Prefix-Route-mg-2de0-Audit.md:202",
     "`Phi* <= min_k Delta_1(A_k)`, 0 exceptions / 431 posets", "NO"),
    ("docs/OneThird-Direct-Prefix-Route-mg-2de0-Audit.md:202",
     "`strict on 65 of them`", "YES"),
    ("docs/OneThird-Direct-Prefix-Route-mg-2de0-Audit.md:204",
     "`Phi* = min_k Delta_1(A_k)` at the antichain, exactly", "NO"),
    ("code/direct_prefix_audit_2de0/README.md:60",
     "P9 HIT (0 / 12702; 0 / 431)", "NO"),
    ("code/direct_prefix_audit_2de0/out_a3_nonvacuity.txt:34",
     "Phi_P(A) <= 1 for every cut: 0 / 12702", "NO"),
    ("code/direct_prefix_audit_2de0/out_a3_nonvacuity.txt:77",
     "Phi* <= min over prefixes: 0 / 431", "NO"),
    ("code/direct_prefix_audit_2de0/out_a3_nonvacuity.txt:80",
     "strictly smaller on 65 of 431 posets; EQUAL on 366", "YES"),
    ("code/direct_prefix_audit_2de0/out_a3_nonvacuity.txt:88",
     "Phi* == min over prefixes at the antichain: 0 / 6", "NO"),
    ("code/direct_prefix_audit_2de0/out_selftest_2de0.txt:73",
     "cites `A3.4's strictly smaller on 65 of 431`", "YES"),
    ("code/direct_prefix_audit_2de0/selftest2de0.py:147",
     "the same citation, in a source comment", "YES"),
]
print(f"       {'site':>62s}  moves?")
for site, what, mv in LEDGER:
    print(f"       {site:>62s}  {mv:>4s}   {what}")
movers = [s for s, _, m in LEDGER if m == "YES"]
print()
print(f"       => {len(movers)} sites carry a figure that MOVES, and all of them carry the")
print("          SAME figure: A3.4's strict count. Every other published Phi figure of")
print("          mg-2de0 is correct as published and stays correct.")
print("       => and NOTHING outside code/direct_prefix_audit_2de0/ and")
print("          docs/OneThird-Direct-Prefix-Route-mg-2de0-Audit.md carries a Phi figure")
print("          sourced from mg-2de0. STATE.md's mg-2de0 row carries no Phi number;")
print("          checked by grep, reported in the README as PREDICTIONS.md P12.")

print()
print("=" * 78)
print(f"R4 TOTAL BAD: {T.bad}")
print("=" * 78)
sys.exit(0 if T.bad == 0 else 1)
