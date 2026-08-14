"""c0 -- THE PLANTED DEFECTS.  Every check in this directory, run against a broken library.

A check that has never been seen to fail is a claim, not a control.  Each plant
below patches ONE function in `lib7c32` and re-runs a miniature of the arm that
depends on it; the arm must come back CAUGHT.  The plants are restored between
worlds, and the last section runs the unpatched library to show the harness is
not simply always red.

TWO OF THE SIX ARE THE ONES WORTH READING.  D6 is the WRONG DIRECTION: it is a
change that must NOT be caught, because a suite measured only where it removes
things is a suite nobody has checked for over-reach.  D5 comes back INERT and is
PRINTED AS INERT rather than swapped for one that fires -- it is invisible on this
population for a reason that is itself a finding, and c3 §1 is built around it.

No clock, no randomness, no sampling.
"""

import sys
from fractions import Fraction

import lib7c32 as L

W = 88
out = sys.stdout.write
HALF = Fraction(1, 2)


def head(t):
    out("=" * W + "\n" + t + "\n" + "=" * W + "\n")


def sec(t):
    out("\n" + t + "\n" + "-" * W + "\n")


# ---------------------------------------------------------------------------
# the miniature arms -- each returns True when it PASSES on the given library
# ---------------------------------------------------------------------------

def arm_two_route(ps):
    """c1 §2 in miniature: db from marginals vs db from enumerating L(P)."""
    for n in (3, 4):
        for P in ps[n]:
            tot, p = L.marginals(P)
            exts = L.linear_extensions(P)
            for x in range(n):
                for y in range(n):
                    for z in range(n):
                        if len({x, y, z}) < 3:
                            continue
                        cyc, _, _ = L.triple_class_counts(P, exts, x, y, z)
                        if L.db_from_marginals(p, x, y, z) != Fraction(cyc, tot) - HALF:
                            return False
    return True


def arm_marginals(ps):
    """c1 §0 in miniature: the down-set DP against brute-force enumeration."""
    for n in (3, 4, 5):
        for P in ps[n]:
            tot, p = L.marginals(P)
            exts = L.linear_extensions(P)
            if len(exts) != tot:
                return False
            for x in range(n):
                for y in range(n):
                    if x == y:
                        continue
                    c = sum(1 for w in exts if w.index(x) < w.index(y))
                    if p[(x, y)] != Fraction(c, tot):
                        return False
    return True


def arm_telescope(ps):
    """c2 §1 in miniature: the star identity at every base point."""
    for n in (4, 5):
        for P in ps[n]:
            _, p = L.marginals(P)
            chain = L.majority_order(p, n)
            for base in chain:
                D, terms, live, rhs = L.star(p, chain, base)
                if D != rhs:
                    return False
    return True


def arm_acyclic_positive(ps):
    """c3 §1's detector, asked about a tournament that IS cyclic.

    Not a poset question at all: an explicit 3-cycle, which `is_acyclic` must
    reject.  Without this, `0 cyclic` in c3 §1 is consistent with a detector
    that never says no."""
    return (not L.is_acyclic([(0, 1), (1, 2), (2, 0)], 3)) and \
        L.is_acyclic([(0, 1), (1, 2), (0, 2)], 3)


def arm_23_acyclic(ps):
    """c3 §1 proper: the 2/3-relation is acyclic on every poset up to n = 6."""
    for n in (3, 4, 5, 6):
        for P in ps[n]:
            _, p = L.marginals(P)
            if not L.is_acyclic(L.majority_edges(p, n, Fraction(2, 3)), n):
                return False
    return True


ARMS = [("two-route db identity  (c1 §2)", arm_two_route),
        ("marginal DP vs L(P)    (c1 §0)", arm_marginals),
        ("star telescope         (c2 §1)", arm_telescope),
        ("acyclicity, positive   (c3 §1)", arm_acyclic_positive),
        ("2/3-relation acyclic   (c3 §1)", arm_23_acyclic)]


# ---------------------------------------------------------------------------
# the plants
# ---------------------------------------------------------------------------

def plant_sign(orig):
    """D1  b(z,x) written as b(x,z): the coboundary loses its antisymmetry."""
    def broken(p, x, y, z):
        return L.bb(p, x, y) + L.bb(p, y, z) + L.bb(p, x, z)
    L.db_from_marginals = broken


def plant_maximality(orig):
    """D2  the linear-extension DP forgets that the last element must be maximal."""
    def broken(P):
        if P._ecounts is None:
            n = P.n
            e = [0] * (1 << n)
            e[0] = 1
            for S in range(1, 1 << n):
                tot = 0
                m = S
                while m:
                    x = (m & -m).bit_length() - 1
                    m &= m - 1
                    tot += e[S & ~(1 << x)]        # maximality test deleted
                e[S] = tot
            P._ecounts = e
        return P._ecounts
    L.restriction_counts = broken


def plant_short_star(orig):
    """D3  the star drops its last triple -- an off-by-one in the telescope."""
    def broken(p, chain, base):
        terms = [L.db_from_marginals(p, base, chain[k - 1], chain[k])
                 for k in range(1, len(chain) - 1)]         # -1 planted
        live = sum(1 for k in range(1, len(chain))
                   if base != chain[k - 1] and base != chain[k])
        rhs = (L.consecutive_sum(p, chain) - L.bb(p, base, chain[-1])
               + L.bb(p, base, chain[0]))
        return sum(terms, Fraction(0)), terms, live, rhs
    L.star = broken


def plant_diagonal(orig):
    """D4  b(x,x) returned as -1/2 instead of 0: the degenerate triples stop cancelling."""
    def broken(p, x, y):
        if x == y:
            return -HALF
        return p[(x, y)] - HALF
    L.bb = broken


def plant_blind_acyclic(orig):
    """D5  the cycle detector always says acyclic."""
    L.is_acyclic = lambda edges, n: True


def plant_threshold(orig):
    """D6  WRONG DIRECTION -- the 2/3 threshold relaxed to 1/2.

    This is a real weakening of what c3 §1 asserts and it must NOT be caught on
    this population, because there is no majority cycle here to catch it with."""
    orig_edges = orig["majority_edges"]
    L.majority_edges = lambda p, n, threshold: orig_edges(p, n, HALF)


PLANTS = [("D1", "b(z,x) written b(x,z) in the coboundary", plant_sign, True),
          ("D2", "linear-extension DP drops the maximality test", plant_maximality, True),
          ("D3", "the star drops its last triple", plant_short_star, True),
          ("D4", "b(x,x) returned as -1/2 rather than 0", plant_diagonal, True),
          ("D5", "the cycle detector always says acyclic", plant_blind_acyclic, True),
          ("D6", "2/3 threshold relaxed to 1/2 (WRONG DIRECTION)", plant_threshold, False)]


def main():
    head("mg-7c32  c0 -- planted defects: every check in this directory, run broken")
    status = 0
    ps = L.posets_upto(6)

    pristine = {k: getattr(L, k) for k in
                ("db_from_marginals", "restriction_counts", "star", "bb",
                 "is_acyclic", "majority_edges")}

    sec("§0  THE UNPATCHED LIBRARY -- every arm must be GREEN before any plant means anything")
    base = {}
    for name, fn in ARMS:
        base[name] = fn(ps)
        out("  %-34s %s\n" % (name, "PASS" if base[name] else "FAIL"))
        if not base[name]:
            status = 1
    if status:
        out("\nVERDICT: FAIL -- the clean library is already red; no plant below is readable\n")
        return status

    sec("§1  THE PLANTS")
    inert = []
    for tag, desc, apply_plant, must_fire in PLANTS:
        for k, v in pristine.items():
            setattr(L, k, v)
        for n in ps:
            for P in ps[n]:
                P._ecounts = None
        apply_plant(pristine)
        fired = []
        for name, fn in ARMS:
            for n in ps:
                for P in ps[n]:
                    P._ecounts = None
            try:
                ok = fn(ps)
            except Exception:
                ok = False
            if not ok:
                fired.append(name.split("(")[0].strip())
        caught = bool(fired)
        if must_fire:
            verdict = "CAUGHT" if caught else "MISSED"
            if not caught:
                status = 1
        else:
            verdict = "INERT (required)" if not caught else "FIRED (unexpected)"
            if caught:
                status = 1
        out("  %s  %-46s %-18s %s\n"
            % (tag, desc, verdict, ", ".join(fired) if fired else "-"))
        if not caught and must_fire:
            inert.append(tag)

    for k, v in pristine.items():
        setattr(L, k, v)
    for n in ps:
        for P in ps[n]:
            P._ecounts = None

    sec("§2  D6 IS THE FINDING, NOT THE FILLER")
    out("""
  D6 relaxes the majority threshold from 2/3 to 1/2 and NOTHING NOTICES.  That is the
  required answer here and it is also the reason c3 §1 carries the paragraph it does:
  there is no majority cycle anywhere in this population, so an arm that reports
  `0 cyclic` at threshold 2/3 would report `0 cyclic` at threshold 1/2 as well, and its
  zero is therefore NOT evidence that the 2/3 band is what closes the composition.
  mg-24a3 supplies the instance the population cannot -- a majority cycle at n = 11 with
  margins near 0.50014 -- and BASIC-FACTS fact 2 supplies the argument.  An arm whose
  zero survives its own hypothesis being deleted has to say so, and this is that line.
""")

    sec("§3  RESTORED")
    for name, fn in ARMS:
        ok = fn(ps)
        out("  %-34s %s\n" % (name, "PASS" if ok else "FAIL"))
        if not ok:
            status = 1

    out("\nVERDICT: %s\n" % ("PASS" if status == 0 else "FAIL"))
    return status


if __name__ == "__main__":
    sys.exit(main())
