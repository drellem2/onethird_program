"""mg-fcb2 SELFTEST -- this audit's own instruments, against answers known in
advance, BEFORE either is pointed at the tree under audit.

The findings below rest on two instruments written from scratch: an exact integer
characteristic polynomial and a signed-permutation search over all of S_m.  An
audit that reports "the shipped detector is wrong" on the word of an unchecked
detector of its own has done nothing.  So each is checked here against a source
that shares no line with it:

  charpoly_exact      vs a cofactor expansion of det(x.I - A) over polynomials,
                      enumerated over all m! permutation terms
  signed_perm_witness vs brute force over all m! permutations x 2^m sign vectors
  the two together    against the identity that a signed-permutation conjugation
                      PRESERVES the characteristic polynomial -- so a pair that
                      is both witnessed and spectrally separated is impossible,
                      and finding one would mean one of the two is broken

PREDICTED EXIT: 0.
"""

import itertools
import random
import sys

import lib_fcb2 as L


def naive_charpoly(A):
    """det(x.I - A) by the Leibniz formula over polynomials.  Exponential and
    obviously correct; that is the whole point of it."""
    m = len(A)
    coeffs = [0] * (m + 1)
    for perm in itertools.permutations(range(m)):
        s, p = 1, list(perm)
        for i in range(m):
            for j in range(i + 1, m):
                if p[i] > p[j]:
                    s = -s
        poly = [1]
        for i in range(m):
            f = [-A[i][perm[i]], 1] if i == perm[i] else [-A[i][perm[i]]]
            new = [0] * (len(poly) + len(f) - 1)
            for a, ca in enumerate(poly):
                for b, cb in enumerate(f):
                    new[a + b] += ca * cb
            poly = new
        for d, c in enumerate(poly):
            coeffs[d] += s * c
    return coeffs


def rand_sym(rng, m, lo=-4, hi=4):
    A = [[rng.randint(lo, hi) for _ in range(m)] for _ in range(m)]
    for i in range(m):
        for j in range(i):
            A[i][j] = A[j][i]
    return A


def main():
    print("== mg-fcb2 SELFTEST: this audit's instruments, before they are used ==")
    fc, po = L.import_face_geometry()
    sys.path.insert(0, L.FACE_GEOMETRY)
    from controls import claim1_pair
    from posets import all_posets

    rng = random.Random(20260805)

    # ---- S1: the exact characteristic polynomial -------------------------
    ok = tot = 0
    for _ in range(240):
        m = rng.randint(1, 5)
        A = rand_sym(rng, m)
        want = naive_charpoly(A)
        got = L.charpoly_exact(A)
        tot += 1
        ok += got == want
    L.check("S1a exact charpoly agrees with a Leibniz cofactor expansion over "
            "polynomials on %d/%d random symmetric integer matrices with m <= 5, "
            "entries in [-4, 4]" % (ok, tot), ok == tot and tot > 0)

    # ... and on the matrices this audit will actually judge, against the same
    # naive expansion wherever m is small enough to enumerate m! terms.
    ps = [P for n in range(2, 6) for P in all_posets(n)]
    ok = tot = 0
    for P in ps:
        A, _ = claim1_pair(P)
        if len(A) > 6:
            continue
        tot += 1
        ok += L.charpoly_exact(A) == naive_charpoly(A)
    L.check("S1b ... and on %d/%d of THIS BATTERY'S OWN L^rel matrices with "
            "|L(P)| <= 6, not just random ones" % (ok, tot), ok == tot and tot > 0)

    # The bound has to be a bound.  A lift under a too-small modulus is the way
    # this instrument would fail silently, so it is checked rather than trusted.
    ok = tot = 0
    for _ in range(60):
        m = rng.randint(1, 5)
        A = rand_sym(rng, m, -9, 9)
        cp = naive_charpoly(A)
        tot += 1
        ok += max(abs(c) for c in cp) <= L.charpoly_bound(A)
    L.check("S1c the Hadamard coefficient bound really bounds every coefficient "
            "of the true polynomial on %d/%d matrices (a lift under a modulus "
            "smaller than 2*bound is how this instrument would fail SILENTLY)"
            % (ok, tot), ok == tot and tot > 0)

    # ---- S2: the signed-permutation search -------------------------------
    agree = tot = built = found = witnessed = 0
    for _ in range(300):
        m = rng.randint(1, 4)
        A = rand_sym(rng, m, -2, 2)
        if rng.random() < 0.6:                 # a pair built to BE a conjugate
            sig = list(range(m))
            rng.shuffle(sig)
            s = [rng.choice([1, -1]) for _ in range(m)]
            B = L.reconstruct(A, sig, s)
            built += 1
        else:
            B = rand_sym(rng, m, -2, 2)
        w = L.signed_perm_witness(A, B)
        bf = L.brute_signed_perm(A, B)
        assert w != "BUDGET", "budget exhausted at m <= 4, which should not happen"
        tot += 1
        agree += (w is not None) == (bf is not None)
        if w is not None:
            witnessed += 1
            found += L.reconstruct(A, w[0], w[1]) == B
    L.check("S2a the pruned search over S_m agrees with BRUTE FORCE over all m! "
            "permutations x 2^m sign vectors on %d/%d random pairs with m <= 4 "
            "(%d of them built to be conjugates)" % (agree, tot, built),
            agree == tot and tot > 0)
    L.check("S2b every witness it returned reconstructs to the target ENTRY BY "
            "ENTRY (%d/%d), so a bug in the search cannot return a false gauge"
            % (found, witnessed), found == witnessed and witnessed > 0)

    # A search that says YES to everything would make every gauge row green.  A
    # search that says NO to everything would make them all red.  Both ends are
    # pinned, on pairs whose answer is known before the search runs.
    yes = no = 0
    for _ in range(120):
        m = rng.randint(2, 5)
        A = rand_sym(rng, m, -3, 3)
        sig = list(range(m))
        rng.shuffle(sig)
        s = [rng.choice([1, -1]) for _ in range(m)]
        yes += L.signed_perm_witness(A, L.reconstruct(A, sig, s)) is not None
        B = [row[:] for row in A]
        B[0][0] += 1                            # moves the diagonal: s_i^2 = 1
        no += L.signed_perm_witness(A, B) is None
    L.check("S2c positive control on the search: a genuine signed-permutation "
            "conjugate is found on %d/120; negative control: A with one DIAGONAL "
            "entry moved by 1 is rejected on %d/120" % (yes, no),
            yes == 120 and no == 120)

    # ---- S3: the two instruments against each other ----------------------
    # A signed-permutation conjugation is a similarity, so it preserves the
    # characteristic polynomial exactly.  If the search ever witnesses a pair
    # whose exact charpolys differ, one of the two instruments is broken -- and
    # this is the identity every "no pair is both" claim below rests on.
    bad = tot = 0
    for _ in range(200):
        m = rng.randint(1, 5)
        A = rand_sym(rng, m, -3, 3)
        sig = list(range(m))
        rng.shuffle(sig)
        s = [rng.choice([1, -1]) for _ in range(m)]
        B = L.reconstruct(A, sig, s)
        tot += 1
        bad += L.charpoly_exact(A) != L.charpoly_exact(B)
    L.check("S3 a conjugate pair has EQUAL exact characteristic polynomials on "
            "%d/%d constructed pairs (%d violations) -- the identity that makes "
            "'spectrally separated' and 'gauge' mutually exclusive, and the "
            "reason a contradiction between them would be a BUG REPORT and not a "
            "finding about the repair" % (tot - bad, tot, bad), bad == 0)

    # ---- S4: the budget is reported, not swallowed -----------------------
    # "searched and found nothing" must never be printed as "no witness exists".
    m = 9
    A = [[1 if i != j else 0 for j in range(m)] for i in range(m)]
    B = [row[:] for row in A]
    B[0][1] = B[1][0] = -1
    r = L.signed_perm_witness(A, B, node_budget=3)
    L.check("S4 with the node budget set to 3 the search returns the sentinel "
            "'BUDGET' rather than None, so an exhausted search can never be read "
            "as a proof that no witness exists (got %r)" % (r,), r == "BUDGET")

    return L.finish("selftest_fcb2")


if __name__ == "__main__":
    sys.exit(main())
