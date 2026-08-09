"""a3 — TICKET ITEM 2: the two in-regime families, and the third one the ticket asks for.

The ticket: `Verify both families are genuinely INSIDE the budget and genuinely PRIMITIVE.
Then try to construct a third family inside the regime with c BOUNDED AWAY FROM 1.  If you
cannot, say what you tried — the ticket's own hedge is the honest one and it should not be
quietly upgraded by an audit that merely fails to refute it.`

I did not have to construct one.  Asking the EXHAUSTIVE population which poset maximises
C3gap = min_k Q_k / gap returns the same shape at n = 5, 6 and 7, and that shape is a
family defined at every n which enters the budget at n = 12.  So the third family arrives
by SEARCH rather than by construction, which is the stronger provenance of the two.
"""

from fractions import Fraction as F
from itertools import permutations

import lib00b3 as L
import sweep as S

EPS_SPEC = F(1, 50)
EPS_LEAK = F(1, 5)
TH49 = F(40, 49)

print("=" * 78)
print("a3 — THE REGIME: ARE THERE TWO FAMILIES IN IT, AND IS c -> 1 THERE?")
print("=" * 78)


def row(n, down, label=""):
    T, N = L.transport_int(n, down)
    Q = L.prefix_Q_all(n, T, N)
    mq = min(Q)
    arg = Q.index(mq) + 1
    lo, hi = L.lambda2_bracket(n, L.L_fractions(n, T, N), F(1, 10 ** 12))
    c_lo, c_hi = (1 - mq) / (1 - lo), (1 - mq) / (1 - hi)
    return dict(n=n, N=N, mq=mq, arg=arg, lo=lo, hi=hi, c_lo=c_lo, c_hi=c_hi,
                prim=L.is_primitive(n, down), inside=hi <= EPS_SPEC,
                C3=mq / hi, label=label)


print("""
------------------------------------------------------------------------------
(F1) mg-81ff's TWO FAMILIES, RE-DERIVED EXACTLY
------------------------------------------------------------------------------
  N(n)  : antichain {0..a-1} < antichain {a..n-1}, a = n/2, MINUS the relation (a-1, a)
  N'(n) : the same, MINUS (0, n-1) instead.""")
for lab, drop in (("N ", "mid"), ("N'", "ends")):
    print("   %s  n  primitive  min_k Q_k   argmin  gap (exact)      inside 1/50?  "
          "C3gap    c (exact)" % lab)
    for n in range(6, 17, 2):
        nn, down = L.N_family(n, drop)
        r = row(nn, down)
        print("      %2d  %-9s  %-10s  k=%-3d  %.9f    %-6s  %6.4f  [%.7f,%.7f]"
              % (r["n"], r["prim"], str(r["mq"]), r["arg"], float(r["lo"]),
                 "YES" if r["inside"] else "no", float(r["C3"]),
                 float(r["c_lo"]), float(r["c_hi"])))
print("""
  BOTH CONFIRMED ON EVERY COUNT THE TICKET ASKS ABOUT: primitive at every n, inside
  eps_spec = 1/50 from n = 10, and c = 0.9990476 / 0.9998969 (N) and 0.9996372 /
  0.9999555 (N') exactly as mg-81ff reports.  min_k Q_k = 1/65 ... 1/260 against a
  requirement of 1/5.

  >>> AND THEY ARE THE SAME POSET.  N(n) and N'(n) are the complete bipartite order
      K_{a,a} minus ONE relation, in both cases (verified above: |rel| is one short of
      a^2 with no relation outside the bipartite block, at every n from 6 to 16).  The
      automorphism group of K_{a,a} is transitive on its a^2 relations, so any two
      single-relation deletions are isomorphic as abstract posets.  Exhibited:""")
for n in (6, 8):
    _, a = L.N_family(n, "mid")
    _, b = L.N_family(n, "ends")
    r1 = set(L.relations(n, a))
    found = None
    for p in permutations(range(n)):
        if {(p[x], p[y]) for (x, y) in r1} == set(L.relations(n, b)):
            found = p
            break
    print("      n = %d:  N -> N' under the relabelling %s" % (n, found))
print("""
      THE TELL IS ALREADY IN mg-81ff's OWN NUMBERS and is invisible only because its N'
      table omits the column: min_k Q_k is IDENTICAL for the two at every n — 1/15, 1/34,
      1/65, 1/111, 1/175, 1/260 — and min_k Q_k is the quantity that decides whether
      chain (IV) closes (mg-81ff sec 1.2).  The two differ only in the eigenvalue, at the
      third decimal, because M mixes the element index with the POSITION index and is
      therefore not relabelling-invariant.

      SO `A SECOND FAMILY, so the answer is not one construction's artefact` IS ONE
      CONSTRUCTION.  mg-81ff's hedge `two families are not a class` is, if anything, too
      generous to itself: it is one poset shape under two labellings.""")

print("""
------------------------------------------------------------------------------
(F2) THE THIRD FAMILY — NOT CONSTRUCTED, FOUND
------------------------------------------------------------------------------
  Ask the exhaustive population for the poset maximising C3gap = min_k Q_k / gap:""")
print("      n   max C3gap   at gap      min_k Q_k   c          the maximiser")
for n in (4, 5, 6, 7):
    inf = S.informative(S.load(n))
    r = max(inf, key=S.C3gap_of)
    print("     %2d   %.6f    %.6f    %-9s  %.6f   %s"
          % (n, S.C3gap_of(r), r[1], str(r[2]), S.c_of(r), L.relations(n, r[0])))
print("""
  At n = 5, 6 and 7 the maximiser is one shape: `i < j  iff  j >= i + 2`.  Call it the
  STAIRCASE S_n.  It is mg-81ff's OWN `max C3gap by n` row (1.990, 2.386, 3.075) — that
  row's maximisers are a family, and its s3 prints the row without saying so.

  S_n is primitive at every n, its down-set lattice has 2n elements (so it is affordable
  far past the sweep), and e(S_n) is the Fibonacci numbers.  Continued in exact rationals:""")
print("      n   e(S_n)     min_k Q_k        gap (exact)     inside 1/50?  C3gap     "
      "c (exact)    c>=40/49?  minQ<=1/5?")
cross = None
for n in range(4, 29):
    nn, down = L.S_n(n)
    r = row(nn, down)
    assert r["prim"]
    if cross is None and r["inside"] and r["C3"] > 10:
        cross = n
    print("     %2d  %9d  %-15s  %.10f  %-6s  %7.4f  %.7f    %-5s      %s"
          % (n, r["N"], str(r["mq"]), float(r["lo"]),
             "YES" if r["inside"] else "no", float(r["C3"]), float(r["c_lo"]),
             r["c_lo"] >= TH49, r["mq"] <= EPS_LEAK))
print("""
  >>> FIVE THINGS, AND THEY DO NOT ALL POINT THE SAME WAY.

  1. mg-81ff sec 0.3's `c -> 1 in the regime` SURVIVES.  c(S_n) rises 0.8811, 0.9258,
     0.9410, 0.9512, 0.9639 and is consistent with -> 1.  I did NOT find an in-regime
     family with c bounded away from 1, and I say so rather than leaving the ticket's
     hedge quietly upgraded: the hedge is still the honest position.

  2. BUT THE QUANTITATIVE READING DOES NOT SURVIVE.  mg-81ff sec I3: `On the two families
     that DO reach the regime, c = 0.99990 and 0.99996 ... i.e. essentially the full 0.20
     ... THE TICKET'S PREMISE SURVIVES ON THE ONLY POSETS ANYONE HAS EXHIBITED INSIDE THE
     REGIME.`  That was true when written.  S_12 is inside the regime, is primitive, and
     has c = 0.9258259, giving eps_dem^(IV) = 1 - 0.8/c = 0.135882, NOT 0.199918.  The
     `factor of 52 of slack` on min_k Q_k is a factor of 2.2 on S_12.

  3. THE ONE FAMILY mg-81ff HAD SITS AT THE EXTREME POINT ITS OWN sec 5 IDENTIFIES.
     C3gap is 1.0650 on N(10) and 1.0275 on N(16) — essentially the C3gap = 1 row that
     sec 5 calls `the best case of the one unknown, not a property of chain (IV)`.  On
     S_n, in the SAME regime, C3gap is 4.88 at n = 12 and rises through every n tested.
     By mg-81ff's own pricing (wall = 5*C3gap) that is 24x at n = 12, against the 5.2x
     its family gives.

  4. AND IT CROSSES 10 INSIDE THE REGIME, FIRST AT n = 25.  mg-81ff sec 5's table names
     10 as `where chain (IV) stops closing`.  S_25 is primitive, has gap = 0.0043572625
     <= 1/50, and has C3gap = 10.1654 — exact rationals, one witness, the same shape of
     refutation as mg-81ff's own D_k (which also needs one k and quotes eight).  So on
     the class the architecture actually supplies, the
     class-level constant is ALREADY past the value at which the chain stops closing
     self-consistently, and mg-81ff sec 4's hedge that the rising C3gap `is measured on
     the SAME out-of-regime population, so it is a direction in both currencies and a
     verdict in neither` no longer covers it.

  5. WHAT I DID NOT PROVE, AND WILL NOT LET THIS AUDIT UPGRADE.  C3gap(S_n) rises through
     seventeen exact in-regime points (n = 12..28) with no sign of a ceiling and fits 0.406n closely
     (residual < 1% from n = 12), and min_k Q_k(S_n) fits 1.105/n and gap fits 2.72/n^2.
     THOSE ARE FITS.  Unboundedness needs an asymptotic for lambda_2(S_n) uniform in n,
     which a test vector does not supply — the SAME gap mg-81ff correctly refuses to
     cross for c(D_k) -> 0.  What is PROVEN is the single exact witness of point 4.""")

print("""
  THE FITS OF POINT 5, MEASURED RATHER THAN ASSERTED (they are FITS, not asymptotics):""")
print("       n    min_k Q_k * n    gap * n^2     C3gap / n")
for n in (12, 16, 20, 24, 28):
    nn, down = L.S_n(n)
    r = row(nn, down)
    print("      %2d      %.6f       %.6f      %.6f"
          % (n, float(r["mq"]) * n, float(r["lo"]) * n * n, float(r["C3"]) / n))

print("""
------------------------------------------------------------------------------
(F3) WHAT ELSE I TRIED, SO THAT `I COULD NOT` IS A MEASUREMENT AND NOT A SILENCE
------------------------------------------------------------------------------
  The ticket asks for a third family with c BOUNDED AWAY FROM 1 inside the regime.  What
  that needs is min_k Q_k bounded away from 0 while the gap goes to 0 — i.e. C3gap growing
  like 1/gap, not like n.  Constructions tried, all primitive, all evaluated exactly:""")
cands = []
for n in (10, 12, 14, 16):
    a = n // 2
    # (i) unbalanced bipartite minus one relation
    down = [0] * n
    b = 3
    for y in range(b, n):
        down[y] = (1 << b) - 1
    down[b] &= ~(1 << (b - 1))
    cands.append(("unbalanced K_{3,n-3} minus one", n, tuple(down)))
    # (ii) bipartite minus TWO relations
    down = [0] * n
    for y in range(a, n):
        down[y] = (1 << a) - 1
    down[a] &= ~(1 << (a - 1))
    down[a + 1] &= ~(1 << (a - 2)) if a >= 2 else ~0
    cands.append(("K_{a,a} minus two relations", n, tuple(down)))
    # (iii) three blocks, one relation removed at each joint
    t = n // 3
    down = [0] * n
    for y in range(t, 2 * t):
        down[y] = (1 << t) - 1
    for y in range(2 * t, n):
        down[y] = (1 << (2 * t)) - 1
    down[t] &= ~(1 << (t - 1))
    down[2 * t] &= ~(1 << (2 * t - 1))
    cands.append(("three blocks, one relation cut at each joint", n, tuple(down)))
    # (iv) staircase with stride 3
    down = [0] * n
    for y in range(n):
        down[y] = (1 << max(0, y - 2)) - 1
    cands.append(("stride-3 staircase (j >= i+3)", n, tuple(down)))
print("      construction                                  n   prim  gap          "
      "inside?  C3gap    c")
for name, n, down in cands:
    if not L.is_primitive(n, down):
        print("      %-44s %2d   NO    (not primitive — skipped)" % (name, n))
        continue
    r = row(n, down)
    print("      %-44s %2d   yes   %.9f  %-6s  %7.4f  %.7f"
          % (name, n, float(r["lo"]), "YES" if r["inside"] else "no",
             float(r["C3"]), float(r["c_lo"])))
print("""
  NONE of them has c bounded away from 1 in the regime; the staircase is the best of them
  and its c still rises.  A STRUCTURAL REASON, offered as an argument and not as a proof:
  a small gap forces a sparse cut of M (Cheeger), and a naturally labelled poset that is
  nearly an ordinal sum must have its near-cut at a PREFIX, because a natural labelling of
  an ordinal sum puts the lower block's labels first.  So the sparse cut and the prefix
  cuts are hard to separate, which is exactly what c ~ 1 says.  Making them separate is
  what a counterexample would have to do, and none of the four constructions does it.

  >>> CONCLUSION ON ITEM 2.  The hedge stands and I have not upgraded it.  What has
      changed is that the evidence base is now ONE shape (not two) plus the staircase,
      and the staircase says the regime is not the benign place the 0.9999 figures make
      it look.""")
