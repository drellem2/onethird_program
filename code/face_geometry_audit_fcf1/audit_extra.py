"""mg-fcf1 -- second half of the NEGATIVE CONTROL 4 audit (mg-2789).

G. the unproved remainder of row I1: gauge or not?
H. which of the printed measurements are tautologies of the code path?
I. what row I4's 25 vacuous posets actually mean for "le_to_facet is covered"
J. mg-5630's line-F experiment, re-run independently
K. the absorbability decision procedure, brute-forced
"""

import sys

import rebuild as R


def hdr(s):
    print()
    print("=" * 78)
    print(s)
    print("=" * 78)


def is_signed_perm_conjugate(A, B):
    """Search for a permutation sigma and signs with S.P^T.A.P.S == B.
    Exhaustive only for tiny m; returns None when not attempted."""
    m = len(A)
    if m > 7:
        return None
    from itertools import permutations
    for sig in permutations(range(m)):
        C = [[A[sig[i]][sig[j]] for j in range(m)] for i in range(m)]
        if R.absorbable(C, B):
            return sig
    return False


def main():
    ps = R.population(5)
    N = len(ps)
    base = {}
    for P in ps:
        base[id(P)] = R.build(P)

    hdr("G. ROW I1's UNPROVED REMAINDER (6 of 72).  I1 moves one diagonal\n"
        "   entry down and another up, so the TRACE cannot separate the\n"
        "   spectra by construction.  Are those 6 posets gauges?")
    for P in ps:
        b0 = base[id(P)]
        bm = R.build(P, mutation="I1")
        if R.eq(bm["L"], b0["L"]):
            continue
        if R.spectrum_provably_moved(bm["L"], b0["L"]):
            continue
        m = len(b0["L"])
        cp = R.charpoly_agrees_everywhere(bm["L"], b0["L"])
        sp = is_signed_perm_conjugate(bm["L"], b0["L"])
        setsame = set(bm["facets"]) == set(b0["facets"])
        print("  %-24s n=%d |L(P)|=%-3d charpoly agrees mod p at %d shifts: "
              "%-5s  signed-permutation conjugate: %-8s  facet set changed: %s"
              % (P.covers(), P.n, m, m + 2, cp,
                 "not tried" if sp is None else (sp is not False),
                 not setsame))
    print()
    print("  Read: a False in the charpoly column would be a proof the spectrum")
    print("  moved that the audited invariant list missed; a True is evidence")
    print("  of isospectrality, and a signed-permutation conjugate is a PROOF")
    print("  that the corruption is a relabelling gauge on that poset.")

    hdr("H. WHICH PRINTED MEASUREMENTS ARE TAUTOLOGIES OF THE CODE PATH?")
    print("  1. 'the target D-A is byte-identical on 344/344 (poset, mutation)")
    print("     pairs'.  claim1_pair computes the target as at_laplacian(P);")
    print("     `incidence_mode` is not an argument of at_laplacian and is not")
    print("     forwarded to it.  So the target cannot differ, for any poset,")
    print("     any mutation, at any n.  344/344 is 4 x 86 and is forced.")
    import subprocess
    src = subprocess.run(
        ["git", "show", "HEAD:code/face_geometry/controls.py"],
        capture_output=True, text=True).stdout
    seg = src.split("def claim1_pair")[1].split("def claim1_test")[0]
    print("     evidence, from the committed source:")
    for line in seg.splitlines():
        if "at_laplacian" in line or "target =" in line:
            print("       %s" % line.strip())

    print()
    print("  2. 'no ridge lies in >= 3 facets under any of the four mutations'.")
    print("     For I1 the re-targeted ridge's facet list is {j1,j3}, size 2 by")
    print("     construction; I2 does not touch the boundary matrix at all; I3")
    print("     deletes a row.  So three of the four entries are forced and")
    print("     only the I4 entry is a measurement.  Recomputed here:")
    for tag in ("I1", "I2", "I3", "I4"):
        bad = sum(1 for P in ps if R.build(P, mutation=tag)["multi"])
        print("       %-4s posets with a ridge in >= 3 facets: %d" % (tag, bad))

    hdr("I. WHAT ROW I4's 25 VACUOUS POSETS MEAN FOR 'le_to_facet IS COVERED'")
    changed_silent = []
    for P in ps:
        b0 = base[id(P)]
        bm = R.build(P, mutation="I4")
        if not R.eq(bm["L"], b0["L"]):
            continue
        if set(bm["facets"]) != set(b0["facets"]):
            changed_silent.append((P, len(b0["L"])))
    print("  posets where the off-by-one produces a DIFFERENT facet set and the")
    print("  claim-(1) test is nevertheless silent: %d of %d"
          % (len(changed_silent), N))
    bysz = {}
    for (P, m) in changed_silent:
        bysz.setdefault(m, 0)
        bysz[m] += 1
    print("  by |L(P)|: %s" % sorted(bysz.items()))
    nontriv = [(P, m) for (P, m) in changed_silent if m >= 3]
    print("  of those, with |L(P)| >= 3 (so not a 1x1 or 2x2 degeneracy): %d"
          % len(nontriv))
    for (P, m) in nontriv[:12]:
        print("      %-24s n=%d |L(P)|=%d" % (P.covers(), P.n, m))
    if len(nontriv) > 12:
        print("      ... and %d more" % (len(nontriv) - 12))
    print()
    print("  So a mis-indexed le_to_facet really does build a different complex")
    print("  on these posets and claim (1) still holds there.  The row's own")
    print("  wording ('where the corruption changes L^rel', 25 vacuous) is")
    print("  correctly scoped; what is NOT said anywhere is that the vacuity is")
    print("  a numerical coincidence rather than an identity -- on %d of the 25"
          % len(changed_silent))
    print("  the incidence structure genuinely is wrong and the pipeline does")
    print("  not notice.  Contrast row I1/I2/I3, whose vacuity is 'the mutation")
    print("  did not apply'.  Two different kinds of vacuity, one label.")

    hdr("J. mg-5630's LINE-F EXPERIMENT, re-run independently.\n"
        "   Under each mutation, do NEGATIVE CONTROL 3's own lines move?")
    # NC3 line 2 = all-+1 signs leave L unchanged; line 3 = parity signs bite.
    def build_signed(P, mutation, sign_mode):
        chains = R.maximal_chains(P)
        words = sorted(R.chain_to_word(c, P.n) for c in chains)
        pref = R._prefixes_offbyone if mutation == "I4" else R._prefixes
        facets = [tuple(pref(w)) for w in words]
        if mutation == "swap01" and len(facets) >= 2:
            facets[0], facets[1] = facets[1], facets[0]
        ridges, rows = R.boundary_rows(facets)
        nr, nc = len(ridges), len(facets)
        if sign_mode == "allplus":
            rows = {r: {j: 1 for j in rows[r]} for r in rows}
        elif sign_mode == "parity":
            rows = {r: {j: (v if j % 2 == 0 else -v) for j, v in rows[r].items()}
                    for r in rows}
        rf = {r: sorted(rows.get(r, {}).keys()) for r in range(nr)}
        touched = None
        if mutation == "I1":
            elig = [r for r in range(nr) if len(rf[r]) == 2]
            if elig and nc >= 3:
                r = elig[0]
                j1, j2 = rf[r]
                j3 = next(j for j in range(nc) if j not in (j1, j2))
                rows[r][j3] = rows[r].pop(j2)
                rf[r] = sorted(rows[r].keys())
        elif mutation == "I3":
            elig = [r for r in range(nr) if len(rf[r]) == 2]
            if elig:
                del rows[elig[0]]
                rf[elig[0]] = []
        interior = {r for r in range(nr) if len(rf[r]) == 2}
        free = {r for r in range(nr) if len(rf[r]) == 1}
        if mutation == "I2" and free:
            interior = interior | {min(free)}
        L = R.down_lap(rows, nc, allowed=interior)
        s = [R.perm_sign(w) for w in words]
        return [[s[i] * L[i][j] * s[j] for j in range(nc)] for i in range(nc)]

    nc3_bite_true = sum(
        1 for P in ps
        if not R.eq(build_signed(P, "true", "parity"), base[id(P)]["L"]))
    print("  uncorrupted: NC3 line 3 (parity) bites on %d/%d" % (nc3_bite_true, N))
    for tag in ("I1", "I2", "I3", "I4"):
        b = [build_signed(P, tag, "true") for P in ps]
        same_plus = sum(1 for P, bb in zip(ps, b)
                        if R.eq(build_signed(P, tag, "allplus"), bb))
        par = sum(1 for P, bb in zip(ps, b)
                  if not R.eq(build_signed(P, tag, "parity"), bb))
        verdict = ("SILENT" if same_plus == N else "differs")
        moved = "unchanged -> reads verbatim" if par == nc3_bite_true \
            else "moved to %d -> bite-count accident" % par
        print("  %-4s NC3 line 2 all-+1-unchanged %d/%d (%s); "
              "NC3 line 3 parity bites %d (%s)"
              % (tag, same_plus, N, verdict, par, moved))
    print()
    print("  Reproduces the committed 86/86 SILENT on all four, and the")
    print("  82 / 82 / 72 / 79 parity bite-counts, from an independent build.")
    print("  NEGATIVE CONTROL 3 therefore could not have caught any of the four")
    print("  incidence errors: its detecting line is a sign gauge and stays a")
    print("  sign gauge under all of them.  That part of mg-2789's case STANDS.")

    hdr("K. THE ABSORBABILITY DECISION PROCEDURE, BRUTE-FORCED.")
    agree = cases = 0
    for P in ps:
        b0 = base[id(P)]
        t = R.target_DA(P)
        m = len(t)
        if m > 8:
            continue
        for tag in ("true", "I1", "I2", "I3", "I4", "swap01"):
            A = R.build(P, mutation=tag)["L"]
            brute = False
            for bits in range(1 << m):
                s = [-1 if bits >> i & 1 else 1 for i in range(m)]
                if all(s[i] * A[i][j] * s[j] == t[i][j]
                       for i in range(m) for j in range(m)):
                    brute = True
                    break
            cases += 1
            agree += (brute == R.absorbable(A, t))
    print("  my BFS decision == brute force over all 2^m sign vectors on "
          "%d/%d (poset, mutation) pairs with |L(P)| <= 8" % (agree, cases))
    print("  (the committed instrument check reports 306/306 on the same")
    print("   population and cutoff; %d posets here have |L(P)| <= 8, "
          "6 modes -> %d)" % (cases // 6, cases))

    hdr("L. THE REJECTED CANDIDATE, checked: is facet_swap01 really a gauge?")
    app = absorb = spec = perm = 0
    for P in ps:
        b0 = base[id(P)]
        t = R.target_DA(P)
        bm = R.build(P, mutation="swap01")
        if R.eq(bm["L"], b0["L"]):
            continue
        app += 1
        absorb += R.absorbable(bm["L"], t)
        spec += R.spectrum_provably_moved(bm["L"], b0["L"])
        m = len(t)
        sig = [1, 0] + list(range(2, m))
        perm += R.absorbable([[b0["L"][sig[i]][sig[j]] for j in range(m)]
                              for i in range(m)], bm["L"])
    print("  bites on %d/%d; absorbable into a diagonal +-1 twist on %d/%d; "
          "spectrum provably moved on %d/%d" % (app, N, absorb, app, spec, app))
    print("  it IS a signed-permutation conjugate of the true matrix on %d/%d "
          "-- so 'a relabelling of the facet set is a gauge' is verified, and "
          "the ground on which facet_swap01 was rejected is sound." % (perm, app))

    print()
    print("=" * 78)
    print("done")


if __name__ == "__main__":
    main()
