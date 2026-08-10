"""a5 -- STEP E.  What this counterexample reaches, and what it does not.

A dramatic negative is exactly the condition under which this arc has shipped
over-claims, so the scope is established CLAUSE BY CLAUSE and the clauses that were
NOT re-run here are named as not re-run rather than passed over.

  E1  n <= 8 is untouched.  Re-derived here EXHAUSTIVELY at n <= 6; DECLARED
      UNVERIFIED at n = 7 and n = 8, with the reason and the cost.
  E2  n = 9, 10, 11 are NOT settled by this.
  E3  Nothing here bears on C_3 = 1 itself.

E1's n <= 6 half is also a control on this instrument.  If these devices manufactured
route failures, they would manufacture them at small n too, where the corpus has an
exhaustive census to disagree with.
"""
import sys
import time
from fractions import Fraction as Fr
from common5e82 import banner
import lib5e82 as L

ok = True


def check(label, got, want):
    global ok
    good = got == want
    ok = ok and good
    print("  [%s] %-58s got=%s want=%s" % ("ok " if good else "FAIL", label, got, want))


def gen_posets(n):
    if n == 0:
        yield ()
        return
    for dn in gen_posets(n - 1):
        for D in range(1 << (n - 1)):
            m, good = D, True
            while m:
                i = (m & -m).bit_length() - 1
                m &= m - 1
                if dn[i] & ~D:
                    good = False
                    break
            if good:
                yield dn + (D,)


banner("a5  STEP E -- THE SCOPE CLAIMS, EACH SEPARATELY")
print("""
E1  'n <= 8 is untouched: both routes fail at 0 of 2600369, c_or(8) = 0.943649'

    Re-derived here at n <= 6, exhaustively.  BOTH routes failing requires (F) to
    fail first, so it is enough -- and much cheaper -- to show (F) holds everywhere:
    (F) holds  <=>  gamma >= M^2/2  <=>  R(M^2/2) is PSD.  One exact PSD test per
    primitive poset, no bisection.
""")
EXPECT_PRIM = {3: 4, 4: 27, 5: 275, 6: 4070}
for n in range(3, 7):
    t0 = time.time()
    tot = prim = ffail = 0
    for dn in gen_posets(n):
        tot += 1
        P = L.Poset(dn, n)
        if not P.primitive:
            continue
        prim += 1
        t = P.M * P.M / 2
        if not L.is_psd(P.R(t.numerator, t.denominator)):
            ffail += 1
    print("    n=%d  naturally labelled=%-5d primitive=%-5d  (F) FAILS at %d   [%.1fs]"
          % (n, tot, prim, ffail, time.time() - t0))
    check("  n=%d primitive count matches the corpus" % n, prim, EXPECT_PRIM[n])
    check("  n=%d: (F) fails nowhere, so BOTH routes fail at 0" % n, ffail, 0)

print("""
    So the (F)-failing set is EMPTY at every n <= 6, which is what the corpus says
    ('the (F)-failing set is empty below n = 7', mg-789d s2 §2.4), and 'both routes
    fail at 0' holds there for a reason stronger than the census: the conjunction has
    no candidates at all.

    NOT RE-RUN HERE, AND DECLARED UNVERIFIED:
      * n = 7, 96428 posets / 86278 primitive.  mg-a0d6 recomputed this independently
        (168 route-(F) failures, both routes at 0) in 1443 s.  This audit does not
        repeat it; it was not asked to and it would not test the claim under audit.
      * n = 8, 2800472 / 2600369, and c_or(8) = 0.943649.  NOT recomputed here by
        anybody in this ticket.  I am asserting nothing about it.
    Both figures are quoted in STATE.md and both are OUTSIDE what this audit measured.
""")

print("""
E2  'n = 9, 10, 11 are NOT settled by this'

    Correct, and in both directions:
      * This witness is at n = 12.  It says nothing about smaller n.
      * The four certified counterexamples at n = 9, 9, 10, 11 have u_M =
        0.943486 / 0.947534 / 0.981830 / 0.958326, all < 1, so (M#) HOLDS at each and
        the disjunction survives at each.  Those four are unaffected by this verdict
        and a refutation of it would not have disturbed them either.
      * Whether some OTHER poset at n = 9, 10 or 11 also has both routes failing is
        NOT ANSWERED HERE.  No search was run at those n in this ticket.  'The onset
        is n = 12' is NOT a claim this audit supports -- what is supported is 'both
        routes fail at THIS poset, which has n = 12'.  The distinction is the same one
        mg-5cba's own R1 records: the smallest n an instrument LOOKED AT, published as
        the smallest n where the thing happens.
""")

print("""
E3  'nothing here bears on C_3 = 1 itself'

    Correct.  (F) and (M#) are two SUFFICIENT routes to C_3^(III) = 1; their
    disjunction is what the dependency diagram consumes.  A poset where both fail
    removes the route AT THAT POSET.  It does not refute C_3 = 1, which is not an
    implication of the disjunction but a consequence of it.  What dies is
    'the disjunction is a theorem uniform in n' -- and that is the same thing (L*)'s
    refutation cost, one level up: (L*) died as a route to the disjunction, and now
    the disjunction dies as a route to C_3 = 1 uniformly in n.  n <= 8 remains
    enumerated and Theorem A remains proved; neither is touched here.
""")
# E2 and E3 are STATEMENTS OF SCOPE, not measurements, and they are deliberately not
# dressed as scored arms: a check(True, True) cannot fail, and three of them sat here
# in my first draft.  What is scored in this arm is E1's n <= 6 half, which is the
# only part of the scope that an instrument can be wrong about.
print()
banner("a5 VERDICT: %s" % ("ALL ARMS SATISFACTORY" if ok else "*** AN ARM FAILED ***"))
sys.exit(0 if ok else 1)
