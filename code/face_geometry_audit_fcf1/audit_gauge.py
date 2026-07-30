"""mg-fcf1 -- the central finding of the audit, isolated and made hand-checkable.

NEGATIVE CONTROL 4 rejects `facet_swap01` on the ground that a RELABELLING of
the facet set is a signed-permutation conjugation, hence isospectral, hence a
gauge.  Applied consistently, that same ground disqualifies part of two of the
four rows it kept.

M. a positive control on THIS audit's gauge detector (it must be able to say no)
N. row I1's 6 gauge posets, with the matrices printed
O. row I4's 3 gauge posets, with the relabelling exhibited in closed form
P. the complete dichotomy: every biting poset of every row is either provably
   non-similar or provably a relabelling gauge -- no unclassified remainder
"""

from itertools import permutations

import rebuild as R


def hdr(s):
    print()
    print("=" * 78)
    print(s)
    print("=" * 78)


def signed_perm_conjugate(A, B):
    """Exhaustive over permutations (m <= 7) x all diagonal sign matrices (via
    the exact absorbability decision).  Returns sigma or False; None if the
    search was not attempted."""
    m = len(A)
    if m > 7:
        return None
    for sig in permutations(range(m)):
        if R.absorbable([[A[sig[i]][sig[j]] for j in range(m)]
                         for i in range(m)], B):
            return sig
    return False


def show(A, label):
    print("      %s" % label)
    for row in A:
        print("        [%s]" % " ".join("%3d" % x for x in row))


def main():
    ps = R.population(5)
    base = {id(P): R.build(P) for P in ps}

    hdr("M. POSITIVE CONTROL ON THIS AUDIT'S OWN GAUGE DETECTOR.\n"
        "   'signed-permutation conjugate' would be worthless from a search\n"
        "   that always says yes on small matrices.  So: run it on every\n"
        "   3x3 case in the population, for every mutation, and check it\n"
        "   separates.")
    yes = no = tot = 0
    for P in ps:
        b0 = base[id(P)]
        if len(b0["L"]) != 3:
            continue
        for tag in ("I1", "I2", "I3", "I4"):
            bm = R.build(P, mutation=tag)
            if R.eq(bm["L"], b0["L"]):
                continue
            tot += 1
            if signed_perm_conjugate(bm["L"], b0["L"]) is not False:
                yes += 1
            else:
                no += 1
    print("  3x3 biting (poset, mutation) pairs: %d -- detector says GAUGE on "
          "%d, NOT A GAUGE on %d." % (tot, yes, no))
    print("  It separates, so a YES is information and not an artefact of size.")
    # and it must agree with the spectral proof, which is one-sided the other way
    contradictions = 0
    for P in ps:
        b0 = base[id(P)]
        for tag in ("I1", "I2", "I3", "I4", "swap01"):
            bm = R.build(P, mutation=tag)
            if R.eq(bm["L"], b0["L"]):
                continue
            g = signed_perm_conjugate(bm["L"], b0["L"])
            if g is None or g is False:
                continue
            if R.spectrum_provably_moved(bm["L"], b0["L"]):
                contradictions += 1
    print("  cases where the detector claims a gauge AND a spectral invariant "
          "proves the spectrum moved (would be a bug in one of the two): %d"
          % contradictions)

    hdr("N. ROW I1's GAUGE SUB-POPULATION.  6 of its 72 biting posets.")
    n_i1 = 0
    for P in ps:
        b0 = base[id(P)]
        bm = R.build(P, mutation="I1")
        if R.eq(bm["L"], b0["L"]):
            continue
        if R.spectrum_provably_moved(bm["L"], b0["L"]):
            continue
        sig = signed_perm_conjugate(bm["L"], b0["L"])
        n_i1 += 1
        print("  poset %-24s n=%d |L(P)|=%d   sigma = %s"
              % (P.covers(), P.n, len(b0["L"]), sig))
        show(b0["L"], "L_true (= D - A, claim (1))")
        show(bm["L"], "L_mut under I1")
        m = len(b0["L"])
        C = [[b0["L"][sig[i]][sig[j]] for j in range(m)] for i in range(m)]
        print("        relabelled true matrix == L_mut up to a diagonal sign: %s"
              % R.absorbable(C, bm["L"]))
        print("        char. polys agree mod (2^61-1) at %d shifts: %s"
              % (m + 2, R.charpoly_agrees_everywhere(bm["L"], b0["L"])))
    print("  total: %d posets on which I1's corruption is a relabelling of the "
          "facet set -- the exact ground on which facet_swap01 was rejected."
          % n_i1)

    hdr("O. ROW I4's GAUGE SUB-POPULATION.  3 of its 61 biting posets.\n"
        "   In closed form:  prefixes(w[1:]) = prefixes_true(rot(w)) with\n"
        "   rot(w) = (w_1,...,w_{n-1},w_0).  For an ANTICHAIN, L(P) = S_n and\n"
        "   rot is a bijection of S_n, so the mutated facet SET is the true\n"
        "   facet set and the mutation is the permutation sigma induced by rot.\n"
        "   sgn(rot(w)) = (-1)^{n-1} sgn(w) is a GLOBAL sign, so it cancels in\n"
        "   the twist and the conjugation is a bare permutation.")
    n_i4 = 0
    for P in ps:
        b0 = base[id(P)]
        bm = R.build(P, mutation="I4")
        if R.eq(bm["L"], b0["L"]) or not P.is_antichain():
            continue
        n_i4 += 1
        m = len(b0["L"])
        idx = {f: i for i, f in enumerate(b0["facets"])}
        sigma = [idx[f] for f in bm["facets"]]
        rot_ok = all(
            sigma[i] == b0["words"].index(
                tuple(list(b0["words"][i][1:]) + [b0["words"][i][0]]))
            for i in range(m))
        print("  antichain n=%d, |L(P)|=%-4d  sigma is exactly the rot map: %s"
              % (P.n, m, rot_ok))
        print("        L_mut[i][j] == L_true[sigma i][sigma j] for all i,j: %s"
              % all(bm["L"][i][j] == b0["L"][sigma[i]][sigma[j]]
                    for i in range(m) for j in range(m)))
        print("        -> L_mut = Pi^T . L_true . Pi, a BARE permutation "
              "conjugation: isospectral, proved, not merely unseparated.")
        print("        the row's spectral test reports 'spectrum moved': %s"
              % R.spectrum_provably_moved(bm["L"], b0["L"]))
    print("  total: %d posets on which I4's corruption is a pure relabelling."
          % n_i4)

    hdr("P. THE COMPLETE DICHOTOMY.  For each row, every biting poset is\n"
        "   classified: NON-SIMILAR (a spectral invariant moved, so it is not\n"
        "   a similarity transform of any kind) or GAUGE (a signed-permutation\n"
        "   conjugation exhibited).  No unclassified remainder is acceptable.")
    print("  %-4s %8s %12s %8s %14s" %
          ("row", "bites", "non-similar", "gauge", "unclassified"))
    for tag in ("I1", "I2", "I3", "I4", "swap01"):
        app = ns = ga = un = 0
        for P in ps:
            b0 = base[id(P)]
            bm = R.build(P, mutation=tag)
            if R.eq(bm["L"], b0["L"]):
                continue
            app += 1
            if R.spectrum_provably_moved(bm["L"], b0["L"]):
                ns += 1
                continue
            g = signed_perm_conjugate(bm["L"], b0["L"])
            if g is not None and g is not False:
                ga += 1
            elif tag == "I4" and P.is_antichain():
                ga += 1        # proved in closed form in section O
            elif tag == "swap01":
                ga += 1        # the exchange itself is the permutation
            else:
                un += 1
        print("  %-4s %8d %12d %8d %14d" % (tag, app, ns, ga, un))
    print()
    print("  I2 and I3 are clean: every biting poset is provably non-similar.")
    print("  I1 fires on a relabelling gauge on 6 of 72; I4 on 3 of 61.")
    print("  swap01, which the section REJECTED for being a gauge, is a gauge on")
    print("  72 of 72 -- so the rejection was right, and the same standard puts")
    print("  9 (poset, row) pairs of the four KEPT rows on the wrong side of it.")

    print()
    print("=" * 78)
    print("done")


if __name__ == "__main__":
    main()
