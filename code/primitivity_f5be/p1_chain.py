"""p1 -- pm-onethird's CHAIN, link by link, exactly.

THE CLAIM UNDER TEST, quoted from mg-f5be verbatim:

    alpha_S  <=  P(adjacent) / (4 p (1-p))  <=  1 / (2 max(p, 1-p))  <=  1

and the consequence he draws:

    on a FROZEN poset every incomparable pair has max(p,1-p) > 2/3, so alpha <= 3/4.

FIRST, THE THING THE TICKET ASKS TO BE CHECKED FIRST: this chain is NOT the proof in
mg-409a's deliverable.  Section 3 there proves alpha <= 1 by a two-case argument on
Ran Q_o -- an odd-fiber indicator in Case 1, and Pi_e = I in Case 2.  No pair bias appears
in it.  The chain IS however derivable from that document's section 2, links L1 + L2, and
this arm derives it and then measures every step.

  L1 (mg-409a):  R_M(f_xy) = ((n-1)/2) * E_BK(f_xy)/Var(f_xy)          [exact]
  A  (here):     E_BK(f_xy) = P(adj) / (2(n-1))     under lib409a's normalisation
  B  (here):     Var(f_xy)  = p (1-p)
  => R_M(f_xy) = P(adj) / (4 p (1-p))                                  = pm's TERM 1
  L2 (mg-409a):  alpha(P) <= R_M(f_xy)  at EVERY incomparable pair     [Rayleigh]
  C  (here):     P(adj) <= 2 min(p, 1-p)         [adjacent-swap involution]
  => TERM 1 <= 2 min(p,1-p) / (4 p (1-p)) = 1/(2 max(p,1-p))           = pm's TERM 2
  D:             max(p,1-p) >= 1/2  =>  TERM 2 <= 1                    = pm's TERM 3
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libf5be as F  # noqa: E402
import lib409a as L  # noqa: E402

ok = True

POPS = [(3, "exhaustive", F.posets_up_to_iso(3)),
        (4, "exhaustive", F.posets_up_to_iso(4)),
        (5, "exhaustive", F.posets_up_to_iso(5)),
        (6, "exhaustive", F.posets_up_to_iso(6))]

# --------------------------------------------------------------------------------------
F.banner("p1.0  IS THE CHAIN IN THE DELIVERABLE AT ALL?  (ticket step 1)")

doc = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "docs", "OneThird-Compression-W4-Rate-mg-409a.md")
text = open(doc).read()
for probe in ["4 p (1-p)", "4p(1-p)", "P(adjacent)", "adjacent", "max(p"]:
    print(f"      grep {probe!r:16s} in mg-409a deliverable: "
          f"{'FOUND' if probe in text else 'ABSENT'}")
ok &= F.verdict("4 p (1-p)" not in text and "4p(1-p)" not in text,
                "the chain as written is NOT in mg-409a's deliverable",
                "-> it is a re-derivation, and must be earned here")
ok &= F.verdict("R_M(f_xy)" in text and "Rayleigh at a test vector" in text,
                "but L1 and L2, which the chain needs, ARE in it (section 2)")

# --------------------------------------------------------------------------------------
F.banner("p1.1  LINK A + B -> TERM 1.  R_M(f_xy) = P(adj)/(4 p (1-p)) -- EXACT, EVERY PAIR")

tested = bad = 0
bad_ex = []
for n, label, posets in POPS:
    for lt in posets:
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        for (x, y) in L.incomparable(n, lt):
            p, padj = F.pair_stats(n, lt, LEs, x, y)
            f = L.pair_indicator(n, lt, LEs, x, y)
            rm = L.rayleigh_M(f, LEs, n)
            if rm is None:
                continue
            # B: Var(f_xy) = p(1-p)
            if L.variance(f) != p * (1 - p):
                bad += 1
                bad_ex.append(("var", n, sorted(lt), x, y))
                continue
            # A: E_BK(f_xy) = P(adj)/(2(n-1))
            if L.bk_energy(f, LEs, n, lt) != padj / (2 * (n - 1)):
                bad += 1
                bad_ex.append(("ebk", n, sorted(lt), x, y))
                continue
            tested += 1
            if rm != F.chain_term1(p, padj):
                bad += 1
                bad_ex.append(("term1", n, sorted(lt), x, y, rm, F.chain_term1(p, padj)))
ok &= F.verdict(bad == 0, f"TERM 1 exact at {tested} incomparable pairs, n<=6 EXHAUSTIVE",
                f"{bad} failures")
for e in bad_ex[:5]:
    print("      FAIL", e)

# --------------------------------------------------------------------------------------
F.banner("p1.2  LINK C -> TERM 2.  P(adj) <= 2 min(p,1-p), and it is an EQUALITY of halves")

# The involution: swapping an adjacent incomparable {x,y} is a bijection between
# {L : x,y adjacent, x before y} and {L : x,y adjacent, y before x}.  Hence
#   P(adj) = 2*P(adj & x before y) <= 2*p   and   = 2*P(adj & y before x) <= 2*(1-p).
tested = bad = 0
tight = 0
worst_slack = None
for n, label, posets in POPS:
    for lt in posets:
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        N = len(LEs)
        for (x, y) in L.incomparable(n, lt):
            p, padj = F.pair_stats(n, lt, LEs, x, y)
            fwd = sum(1 for Lx in LEs if Lx.index(y) - Lx.index(x) == 1)
            bwd = sum(1 for Lx in LEs if Lx.index(x) - Lx.index(y) == 1)
            tested += 1
            if Fraction(fwd, N) != Fraction(bwd, N):
                bad += 1
                bad_ex.append(("involution", n, sorted(lt), x, y, fwd, bwd))
                continue
            if padj > 2 * min(p, 1 - p):
                bad += 1
                bad_ex.append(("linkC", n, sorted(lt), x, y, padj, 2 * min(p, 1 - p)))
                continue
            if padj == 2 * min(p, 1 - p):
                tight += 1
            sl = 2 * min(p, 1 - p) - padj
            if worst_slack is None or sl > worst_slack:
                worst_slack = sl
ok &= F.verdict(bad == 0,
                f"P(adj)=2*P(adj & x<y) AND P(adj)<=2min(p,1-p) at {tested} pairs, n<=6 EXHAUSTIVE",
                f"{bad} failures")
print(f"      TIGHT (P(adj) = 2 min(p,1-p)) at {tight} / {tested} pairs; "
      f"worst slack {worst_slack} ({F.frac(worst_slack)})")
print("""
      The involution half is the load-bearing one and it is an EQUALITY, not an
      inequality: swapping an adjacent incomparable pair maps linear extensions to linear
      extensions bijectively.  The <= then comes for free from
      {adj & x before y} being a SUBSET of {x before y}.""")

# --------------------------------------------------------------------------------------
F.banner("p1.3  THE WHOLE CHAIN, all four terms, at every pair -- EXACT")

tested = bad = 0
for n, label, posets in POPS:
    for lt in posets:
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        st = F.all_pair_stats(n, lt, LEs)
        for (x, y), (p, padj) in st.items():
            t1 = F.chain_term1(p, padj)
            t2 = F.chain_term2(p)
            tested += 1
            if not (t1 <= t2 <= 1):
                bad += 1
                bad_ex.append(("chain", n, sorted(lt), x, y, t1, t2))
ok &= F.verdict(bad == 0, f"TERM1 <= TERM2 <= 1 at {tested} pairs, n<=6 EXHAUSTIVE",
                f"{bad} failures")

# --------------------------------------------------------------------------------------
F.banner("p1.4  L2 IS AVAILABLE AT EVERY PAIR -- the chain may choose the most extreme (ticket step 2)")

# alpha(P) <= R_M(f_xy) is a Rayleigh quotient at a test vector.  Nothing distinguishes a
# pair; every incomparable pair yields a valid bound, so the MINIMUM over pairs is a bound.
tested = bad = 0
tight_at = 0
for n, label, posets in POPS[:3]:          # n<=5: exact rational alpha bound vs float alpha
    for lt in posets:
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        st = F.all_pair_stats(n, lt, LEs)
        if not st:
            continue
        a = F.alpha_power(LEs, n)
        t1, t2 = F.chain_bound(st)
        tested += 1
        if a > float(t1) + 1e-9 or a > float(t2) + 1e-9:
            bad += 1
            bad_ex.append(("L2min", n, sorted(lt), a, float(t1), float(t2)))
        if abs(a - float(t1)) < 1e-9:
            tight_at += 1
ok &= F.verdict(bad == 0,
                f"alpha <= min-over-pairs of TERM1 and of TERM2 at {tested} posets (n<=5 exhaustive)",
                f"{bad} violations")
print(f"      the pair witness is TIGHT (alpha = min TERM1) at {tight_at} / {tested} posets")

# --------------------------------------------------------------------------------------
F.banner("p1.5  NEGATIVE CONTROL -- the arms above must be able to go red")

# Plant: drop P(adj) from TERM 1, i.e. use the shape 1/(4p(1-p)) that a careless reading of
# 'p bounded away from 1/2' suggests.  It must FAIL both as an identity and as a bound.
fails_ident = fails_bound = 0
checked = 0
for lt in F.posets_up_to_iso(5):
    LEs = L.linear_extensions(5, lt)
    if len(LEs) < 2:
        continue
    st = F.all_pair_stats(5, lt, LEs)
    if not st:
        continue
    a = F.alpha_power(LEs, 5)
    for (x, y), (p, padj) in st.items():
        checked += 1
        f = L.pair_indicator(5, lt, LEs, x, y)
        rm = L.rayleigh_M(f, LEs, 5)
        if rm != 1 / (4 * p * (1 - p)):
            fails_ident += 1
    # and the "bound" 2*min(p,1-p) >= P(adj) reversed must be violated somewhere
    for (x, y), (p, padj) in st.items():
        if padj < 2 * min(p, 1 - p):
            fails_bound += 1
ok &= F.verdict(fails_ident > 0, f"dropping P(adj) breaks the identity at {fails_ident}/{checked} pairs",
                "control FIRES")
ok &= F.verdict(fails_bound > 0, f"link C is a STRICT inequality at {fails_bound} pairs",
                "so it is not an identity in disguise")

# --------------------------------------------------------------------------------------
F.banner("p1.6  THE FROZEN CONSEQUENCE, as pure arithmetic (no poset needed)")

# If every incomparable pair has p outside [1/3, 2/3] then max(p,1-p) > 2/3 and TERM 2 < 3/4.
for p in [Fraction(1, 3), Fraction(3, 10), Fraction(1, 4), Fraction(1, 5),
          Fraction(276, 1000), Fraction(1, 2)]:
    print(f"      p = {str(p):10s} max(p,1-p) = {str(max(p,1-p)):10s} "
          f"TERM2 = 1/(2max) = {F.frac(F.chain_term2(p))}")
ok &= F.verdict(F.chain_term2(Fraction(1, 3)) == Fraction(3, 4),
                "at p = 1/3 exactly, TERM 2 = 3/4", "pm-onethird's number is right")
ok &= F.verdict(all(F.chain_term2(Fraction(a, 100)) < Fraction(3, 4) for a in range(1, 33)),
                "for every p < 1/3, TERM 2 < 3/4 STRICTLY")

print("""
      So the arithmetic of the ticket's frozen step is correct: delta(P) < 1/3 forces
      EVERY incomparable pair outside [1/3,2/3], hence mu(P) < 1/3, hence
      alpha(P) <= 1/(2(1-mu)) < 3/4.  Whether any such poset EXISTS is p3's question.""")

print()
print("=" * 88)
print("p1 OVERALL: " + ("PASS" if ok else "FAIL"))
print("=" * 88)
sys.exit(0 if ok else 1)
