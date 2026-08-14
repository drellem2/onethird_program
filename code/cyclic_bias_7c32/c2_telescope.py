"""c2 -- STEP 3: THE TELESCOPE, AT EVERY BASE POINT AND UNDER TWO BRACKETINGS.

    b(x_1, x_n) = SUM_i b(x_i, x_{i+1})  -  D,      D = SUM_k (db)(x_1, x_{k-1}, x_k)

The identity itself is algebra and cannot fail; what this arm is for is the two
things around it that CAN.  (1) The ticket spends the lazy bracketing -- a star of
triples through `x_1` -- and names the BASE POINT and the BRACKETING as its two
unspent resources, so both are exercised here rather than described.  (2) The
ticket's own caveat asks that the degenerate cases be checked before the telescope
is built on: `n < 4`, `P` a chain, `P` an antichain.  They are, in §3.

The one non-obvious invariant, and it is not in the ticket: EVERY bracketing of the
telescope spends exactly `n - 2` triples, because a binary tree with `n - 1` leaves
has `n - 2` internal nodes.  So the bracketing freedom cannot buy a shorter sum --
it can only change WHICH triples the sum runs over.  §2 measures that it does.

No clock, no randomness, no sampling.
"""

import sys
from fractions import Fraction
from itertools import permutations

import lib7c32 as L

NMAX = 8          # exhaustive: majority chain, every base point
NMAX_ALLPERM = 5  # exhaustive: EVERY chain, every base point

W = 88
out = sys.stdout.write


def head(t):
    out("=" * W + "\n" + t + "\n" + "=" * W + "\n")


def sec(t):
    out("\n" + t + "\n" + "-" * W + "\n")


def bracket_balanced(p, chain, lo, hi, terms):
    """`b(chain[lo], chain[hi])` reduced by repeated MIDPOINT splits.

    b(x,z) = b(x,y) + b(y,z) - (db)(x,y,z) applied at y = the midpoint, then
    recursively.  Returns the value; appends each `db` used to `terms`.  This is
    a different bracketing from the star and it visits a different set of triples;
    both are exact, which is the point."""
    if hi - lo <= 1:
        return L.bb(p, chain[lo], chain[hi]) if hi > lo else Fraction(0)
    mid = (lo + hi) // 2
    left = bracket_balanced(p, chain, lo, mid, terms)
    right = bracket_balanced(p, chain, mid, hi, terms)
    terms.append(L.db_from_marginals(p, chain[lo], chain[mid], chain[hi]))
    return left + right - terms[-1]


def main():
    head("mg-7c32  c2 -- the step-3 telescope: every base point, two bracketings, "
         "degenerate cases")
    status = 0
    ps = L.posets_upto(NMAX)
    half = Fraction(1, 2)

    # -- SS1 ----------------------------------------------------------------
    sec("§1  THE IDENTITY, EXHAUSTIVE OVER EVERY BASE POINT (majority chain, n = 3..%d)" % NMAX)
    bad_id = 0
    bad_ticket = 0
    bad_live = 0
    checked = 0
    for n in range(3, NMAX + 1):
        for P in ps[n]:
            _, p = L.marginals(P)
            chain = L.majority_order(p, n)
            consec = L.consecutive_sum(p, chain)
            for base in chain:
                D, terms, live, rhs = L.star(p, chain, base)
                checked += 1
                if D != rhs:
                    bad_id += 1
                want_live = n - 2 if base in (chain[0], chain[-1]) else n - 3
                if live != want_live:
                    bad_live += 1
                if base == chain[0]:
                    # the ticket's own form: b(x_1,x_n) = consec - D
                    if L.bb(p, chain[0], chain[-1]) != consec - D:
                        bad_ticket += 1
    out("  (poset, base point) telescopes checked: %d\n" % checked)
    out("  D  ==  SUM consec  -  b(base, x_n)  +  b(base, x_1)    disagreements: %d   [%s]\n"
        % (bad_id, "PASS" if bad_id == 0 else "FAIL"))
    out("  live (non-degenerate) term count == n-2 at an END point, n-3 inside: %d wrong   [%s]\n"
        % (bad_live, "PASS" if bad_live == 0 else "FAIL"))
    out("  the ticket's form  b(x_1,x_n) = SUM consec - D  at base = x_1: %d wrong   [%s]\n"
        % (bad_ticket, "PASS" if bad_ticket == 0 else "FAIL"))
    status |= 0 if (bad_id == 0 and bad_live == 0 and bad_ticket == 0) else 1
    out("""
  AN END POINT IS THE RIGHT BASE FOR THE LOWER BOUND, AND IT IS NOT A CONVENTION.
  The identity at a general base reads  D = SUM consec - b(base,x_n) + b(base,x_1),
  so with base = x_1 the second correction VANISHES and only one bias is spent:
  D > (n-1)/6 - 1/2 = (n-4)/6.  An interior base spends TWO, giving only (n-7)/6 over
  one fewer term.  The base point is free but it is not free in this direction.
""")

    # -- SS2 ----------------------------------------------------------------
    sec("§2  BRACKETING -- the star against the balanced tree, and what the freedom buys")
    bad = 0
    diff_terms = 0
    same_D = 0
    tot = 0
    for n in range(4, NMAX + 1):
        for P in ps[n]:
            _, p = L.marginals(P)
            chain = L.majority_order(p, n)
            terms_b = []
            val = bracket_balanced(p, chain, 0, n - 1, terms_b)
            D_star, terms_s, live, _ = L.star(p, chain, chain[0])
            tot += 1
            if val != L.bb(p, chain[0], chain[-1]):
                bad += 1
            if len(terms_b) != n - 2:
                bad += 1
            if sum(terms_b, Fraction(0)) != D_star:
                same_D += 0
            else:
                same_D += 1
            if sorted(terms_b) != sorted(t for t in terms_s if t != 0):
                diff_terms += 1
    out("  posets n = 4..%d with both bracketings run: %d\n" % (NMAX, tot))
    out("  balanced tree reproduces b(x_1,x_n) and spends exactly n-2 triples: %d failures"
        "   [%s]\n" % (bad, "PASS" if bad == 0 else "FAIL"))
    status |= 0 if bad == 0 else 1
    out("  the two bracketings visit a DIFFERENT multiset of db values on %d of %d posets,\n"
        "  and nonetheless reach the same total D on %d of %d.\n"
        % (diff_terms, tot, same_D, tot))
    out("""
  BOTH HALVES ARE THE FINDING AND THE SECOND IS THE ONE THAT COSTS SOMETHING.
  D is b(x_1,x_n) subtracted from a sum that does not mention the bracketing, so D is
  bracketing-INVARIANT by construction -- rebracketing redistributes the defect over
  different triples and cannot change its total.  So the ticket's "bracketing is free"
  is free for choosing WHICH triples an argument must bound, and buys NOTHING at all
  against the aggregate D.  Only the BASE POINT moves D, and §1 says which way.
""")

    # -- SS3 ----------------------------------------------------------------
    sec("§3  THE DEGENERATE CASES THE TICKET ASKS ABOUT, RUN RATHER THAN REASONED")
    # n = 3: the bound (n-4)/6 is negative, so step 3 says nothing
    why = {3: "NEGATIVE -- step 3 says nothing, and there is no triple to bound anyway",
           4: "ZERO -- the bound is D > 0, true of the star's two live terms for free",
           5: "the first n at which (n-4)/6 exceeds a single db's own floor of -1/6"}
    for n in (3, 4, 5):
        out("  n = %d:  the step-3 bound (n-4)/6 = %-6s  -- %s\n"
            % (n, Fraction(n - 4, 6), why[n]))
    chain5 = L.Poset(5, [(i, j) for i in range(5) for j in range(i + 1, 5)])
    anti5 = L.Poset(5, [])
    for name, P in (("chain_5", chain5), ("antichain_5", anti5)):
        _, p = L.marginals(P)
        ch = L.majority_order(p, 5)
        D, terms, live, rhs = L.star(p, ch, ch[0])
        consec = L.consecutive_sum(p, ch)
        delta, _ = L.delta_of(P, p)
        out("  %-12s e(P) = %-4d  delta(P) = %-6s  SUM consec = %-6s  D = %-6s  "
            "avg db = %s\n"
            % (name, len(L.linear_extensions(P)),
               "n/a" if delta is None else str(delta), consec, D,
               Fraction(D, live) if live else "n/a"))
        out("               identity holds: %s   b(x_1,x_5) = %s\n"
            % (D == rhs, L.bb(p, ch[0], ch[-1])))
        status |= 0 if D == rhs else 1
    out("""
  NEITHER DEGENERATE CASE BREAKS THE TELESCOPE AND NEITHER IS A COUNTEREXAMPLE.
  The CHAIN has no incomparable pair, so the counterexample hypothesis is vacuously
  true of it and step 3's conclusion D > (n-4)/6 is CORRECT for it -- D = 3/2 > 1/6 at
  n = 5 -- with average db = 1/2.  It is excluded as a counterexample by the conjecture's
  own statement (it has no incomparable pair to balance), NOT by anything in step 3.
  The ANTICHAIN has b == 0 at every pair, so it fails the hypothesis at every pair, and
  D = 0 with every db = 0: it is the exact case where the bias IS a coboundary, which
  BASIC-FACTS fact 3 says forces the conjecture -- and it satisfies it.
""")

    # -- SS4 ----------------------------------------------------------------
    sec("§4  EVERY CHAIN, NOT ONLY THE MAJORITY ONE (exhaustive, n <= %d)" % NMAX_ALLPERM)
    bad = 0
    checked = 0
    for n in range(3, NMAX_ALLPERM + 1):
        for P in ps[n]:
            _, p = L.marginals(P)
            for chain in permutations(range(n)):
                chain = list(chain)
                for base in chain:
                    D, terms, live, rhs = L.star(p, chain, base)
                    checked += 1
                    if D != rhs:
                        bad += 1
    out("  (poset, chain, base) telescopes checked: %d   disagreements: %d   [%s]\n"
        % (checked, bad, "PASS" if bad == 0 else "FAIL"))
    out("  The identity is an algebraic tautology in `b` and does NOT use that the chain is\n"
        "  a linear extension, or even that it is sorted by anything.  What step 3 needs the\n"
        "  MAJORITY chain for is only the per-step bound b(x_i, x_{i+1}) >= 1/6 -- that is a\n"
        "  property of the chain, not of the identity, and c3 is where it is measured.\n")
    status |= 0 if bad == 0 else 1

    out("\nVERDICT: %s\n" % ("PASS" if status == 0 else "FAIL"))
    return status


if __name__ == "__main__":
    sys.exit(main())
