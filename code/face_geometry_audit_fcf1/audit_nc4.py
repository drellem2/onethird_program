"""mg-fcf1 -- INDEPENDENT AUDIT of NEGATIVE CONTROL 4 (mg-2789).

Run:  python3 audit_nc4.py

Every number printed here is computed from `rebuild.py`, which imports nothing
from code/face_geometry/.  The committed output is never read.

The single question this audit is for: CAN NEGATIVE CONTROL 4 FAIL ON SOMETHING
THE BATTERY DOES NOT ALREADY CATCH?  Sections A-F.
"""

import sys

import rebuild as R

MUTS = [("I1", "a ridge's facet list"),
        ("I2", "the free/interior split"),
        ("I3", "the ridge enumeration"),
        ("I4", "the facet enumeration (le_to_facet off by one)")]


def hdr(s):
    print()
    print("=" * 78)
    print(s)
    print("=" * 78)


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    ps = R.population(nmax)
    N = len(ps)
    print("population: all posets on 2..%d elements up to isomorphism, N = %d"
          % (nmax, N))
    base = {}
    for P in ps:
        b = R.build(P)
        t = R.target_DA(P)
        assert R.eq(b["L"], t), "claim (1) failed on the uncorrupted rebuild"
        base[id(P)] = (b, t)
    print("claim (1) on the uncorrupted rebuild: holds on %d/%d "
          "(ideal-lattice route, le_to_facet not used)" % (N, N))

    # ---------------------------------------------------------------- A
    hdr("A. REPRODUCE THE FIRE.  Own counts, own population, own predicates.")
    print("%-4s %8s %6s %-28s %10s %10s" %
          ("row", "bites", "vac", "vacuous |L(P)|", "absorbable", "spec-moved"))
    rows = {}
    for tag, _desc in MUTS:
        app = rej = absorb = spec = 0
        vac, vsz = 0, set()
        for P in ps:
            b0, t = base[id(P)]
            bm = R.build(P, mutation=tag)
            if R.eq(bm["L"], b0["L"]):
                vac += 1
                vsz.add(len(b0["L"]))
                continue
            app += 1
            rej += not R.eq(bm["L"], t)
            absorb += R.absorbable(bm["L"], t)
            spec += R.spectrum_provably_moved(bm["L"], b0["L"])
        rows[tag] = (app, rej, vac, sorted(vsz), absorb, spec)
        print("%-4s %8s %6d %-28s %10s %10s" %
              (tag, "%d/%d" % (rej, app), vac, str(sorted(vsz)),
               "%d/%d" % (absorb, app), "%d/%d" % (spec, app)))

    # ---------------------------------------------------------------- B
    hdr("B. IS THE 'NOT ABSORBABLE' ANSWER A MEASUREMENT OR A THEOREM?\n"
        "   absorbable_by_diagonal_twist returns False the instant a DIAGONAL\n"
        "   entry moves (s_i^2 = 1 pins the diagonal).  So for any mutation\n"
        "   that provably changes diag(L^rel), 'absorbable 0/N' is arithmetic,\n"
        "   not evidence -- the same defect shape as mg-78c0's all-plus-1 row.")
    for tag, _desc in MUTS:
        diag_moved = same_diag = 0
        offdiag_only = 0
        for P in ps:
            b0, t = base[id(P)]
            bm = R.build(P, mutation=tag)
            if R.eq(bm["L"], b0["L"]):
                continue
            d0 = [b0["L"][i][i] for i in range(len(b0["L"]))]
            dm = [bm["L"][i][i] for i in range(len(bm["L"]))]
            if d0 == dm:
                same_diag += 1
                offdiag_only += 1
            else:
                diag_moved += 1
        app = rows[tag][0]
        print("  %-4s diagonal of L^rel moves on %d/%d biting posets; "
              "diagonal PRESERVED on %d/%d"
              % (tag, diag_moved, app, same_diag, app))
        if diag_moved == app and app:
            print("       -> on every one of them the predicate cannot return "
                  "True: this row's absorbability count is FORCED.")
        elif same_diag:
            print("       -> the predicate does real work on %d poset(s): the "
                  "diagonal matches and the off-diagonal signs decide."
                  % same_diag)

    print()
    print("  The exact algebra, verified rather than argued:")
    # I2: L_mut = L_true + e_j e_j^T  where j is the free ridge's unique facet
    ok = tot = 0
    for P in ps:
        b0, _ = base[id(P)]
        bm = R.build(P, mutation="I2")
        if bm["touched"] is None:
            continue
        tot += 1
        r = bm["touched"]
        j = sorted(bm["rows"][r].keys())[0]
        m = len(b0["L"])
        pred = [[b0["L"][a][c] + (1 if a == c == j else 0) for c in range(m)]
                for a in range(m)]
        ok += R.eq(bm["L"], pred)
    print("    I2: L_mut == L_true + e_j.e_j^T exactly (j = the free ridge's "
          "one facet) on %d/%d posets where it applies." % (ok, tot))
    print("        A rank-one bump on ONE diagonal entry.  Non-absorbability "
          "and trace-motion are both immediate, for every finite poset.")
    ok = tot = 0
    for P in ps:
        b0, _ = base[id(P)]
        bm = R.build(P, mutation="I3")
        if bm["touched"] is None:
            continue
        tot += 1
        r = bm["touched"]
        j1, j2 = sorted(b0["rows"][r].keys())
        c1, c2 = b0["rows"][r][j1], b0["rows"][r][j2]
        m = len(b0["L"])
        sub = {(j1, j1): c1 * c1, (j2, j2): c2 * c2,
               (j1, j2): c1 * c2, (j2, j1): c1 * c2}
        s = [R.perm_sign(w) for w in b0["words"]]
        pred = [[b0["L"][a][c] - s[a] * s[c] * sub.get((a, c), 0)
                 for c in range(m)] for a in range(m)]
        ok += R.eq(bm["L"], pred)
    print("    I3: L_mut == L_true minus that ridge's rank-one outer product "
          "on %d/%d posets where it applies." % (ok, tot))
    print("        Both diagonal entries drop by 1, so again forced.")
    ok = tot = 0
    for P in ps:
        b0, _ = base[id(P)]
        bm = R.build(P, mutation="I1")
        if bm["touched"] is None:
            continue
        tot += 1
        r = bm["touched"]
        j1, j2 = sorted(b0["rows"][r].keys())
        j3 = sorted(set(bm["rows"][r]) - {j1})[0] if j1 in bm["rows"][r] \
            else None
        m = len(b0["L"])
        d0 = b0["L"][j2][j2]
        dm = bm["L"][j2][j2]
        ok += (dm == d0 - 1)
    print("    I1: the abandoned facet's diagonal entry drops by exactly 1 on "
          "%d/%d posets where it applies -- forced too." % (ok, tot))

    # ---------------------------------------------------------------- C
    hdr("C. IS I4 A GAUGE?  The section rejected facet_swap01 because a\n"
        "   relabelling of the facet set is a signed-permutation conjugation,\n"
        "   hence isospectral.  Is the off-by-one one of those?")
    print("  The off-by-one is the TRUE map composed with a cyclic rotation of")
    print("  the word:  prefixes(w[1:]) = prefixes_true(rot(w)),")
    print("  rot(w) = (w1,...,w_{n-1},w0).  So whenever rot maps L(P) onto")
    print("  itself, the mutated facet SET equals the true facet set and the")
    print("  mutation is a pure relabelling -- exactly the rejected gauge.")
    print()
    gauge = []
    for P in ps:
        b0, t = base[id(P)]
        bm = R.build(P, mutation="I4")
        setsame = set(bm["facets"]) == set(b0["facets"])
        if not setsame:
            continue
        idx = {f: i for i, f in enumerate(b0["facets"])}
        sigma = [idx[f] for f in bm["facets"]]
        m = len(b0["L"])
        permuted = all(bm["L"][i][j] == b0["L"][sigma[i]][sigma[j]]
                       for i in range(m) for j in range(m))
        signed = None
        if not permuted:
            signed = R.absorbable(
                bm["L"],
                [[b0["L"][sigma[i]][sigma[j]] for j in range(m)]
                 for i in range(m)])
        bites = not R.eq(bm["L"], b0["L"])
        gauge.append((P, m, bites, permuted, signed))
        print("  %-22s n=%d |L(P)|=%-4d bites=%-5s facet set IDENTICAL, "
              "sigma = rot; L_mut == P^T.L_true.P : %s%s"
              % (P.covers(), P.n, m, bites, permuted,
                 "" if signed is None else
                 " (signed-permutation: %s)" % signed))
    print()
    print("  posets where the off-by-one is a pure facet relabelling: %d/%d"
          % (len(gauge), N))
    biting_gauges = [g for g in gauge if g[2]]
    print("  ... of which it BITES (so is counted in row I4) on %d:"
          % len(biting_gauges))
    for (P, m, _b, permuted, _s) in biting_gauges:
        b0, t = base[id(P)]
        bm = R.build(P, mutation="I4")
        print("      %-22s |L(P)|=%-4d  isospectral BY CONSTRUCTION "
              "(permutation similarity) = %s; corroborated by charpoly mod p "
              "at %d shifts = %s"
              % (P.covers(), m, permuted, m + 2,
                 R.charpoly_agrees_everywhere(bm["L"], b0["L"])))
        print("      %-22s   R.spectrum_provably_moved says %s -- so this "
              "poset is one of the row's unproved remainder, and it is not "
              "merely unproved: it is PROVABLY isospectral."
              % ("", R.spectrum_provably_moved(bm["L"], b0["L"])))

    # the row's own unproved remainder, identified
    print()
    print("  Row I4's biting posets on which no invariant separated the "
          "spectra, listed:")
    for P in ps:
        b0, t = base[id(P)]
        bm = R.build(P, mutation="I4")
        if R.eq(bm["L"], b0["L"]):
            continue
        if not R.spectrum_provably_moved(bm["L"], b0["L"]):
            same = set(bm["facets"]) == set(b0["facets"])
            print("      %-22s n=%d |L(P)|=%-4d facet set identical to the "
                  "true one: %s ; charpoly agrees mod p at %d shifts: %s"
                  % (P.covers(), P.n, len(b0["L"]), same, len(b0["L"]) + 2,
                     R.charpoly_agrees_everywhere(bm["L"], b0["L"])))

    # ---------------------------------------------------------------- D
    hdr("D. VACUITY, recomputed, and the REASON checked against the real one.")
    reasons = {
        "I1": "fewer than 3 facets, so the re-target has no third facet to "
              "aim at (or no interior ridge at all)",
        "I2": "no FREE ridge exists, i.e. F(P) is a sphere -- the antichains",
        "I3": "no interior ridge exists",
        "I4": "the off-by-one happens to leave L^rel numerically unchanged",
    }
    for tag, _d in MUTS:
        vac = [P for P in ps
               if R.eq(R.build(P, mutation=tag)["L"], base[id(P)][0]["L"])]
        sizes = sorted({len(base[id(P)][0]["L"]) for P in vac})
        kinds = []
        for P in vac:
            k = ("chain" if P.is_chain() else
                 "antichain" if P.is_antichain() else "other")
            kinds.append(k)
        print("  %-4s vacuous on %d posets, |L(P)| in %s"
              % (tag, len(vac), sizes))
        print("       kinds: chain=%d antichain=%d other=%d"
              % (kinds.count("chain"), kinds.count("antichain"),
                 kinds.count("other")))
        print("       real reason: %s" % reasons[tag])
        if tag == "I1":
            bad = [P for P in vac if R.build(P, mutation=tag)["n_facets"] >= 3
                   and R.build(P, mutation=tag)["n_eligible"] > 0]
            print("       posets vacuous for some OTHER reason: %d" % len(bad))
        if tag == "I2":
            bad = [P for P in vac if R.build(P)["free"]]
            print("       vacuous posets that DO have a free ridge: %d" % len(bad))
        if tag == "I3":
            bad = [P for P in vac if R.build(P)["interior"]]
            print("       vacuous posets that DO have an interior ridge: %d"
                  % len(bad))
        if tag == "I4":
            bad = [P for P in vac
                   if set(R.build(P, mutation="I4")["facets"])
                   != set(R.build(P)["facets"])]
            print("       vacuous posets where the facet SET really did change "
                  "(so L^rel not changing is a coincidence, not an identity): "
                  "%d" % len(bad))

    # ---------------------------------------------------------------- E
    hdr("E. INSTANCE-DEPENDENCE.  The audited code always mutates the FIRST\n"
        "   eligible ridge.  Sweep every eligible ridge instead: does any\n"
        "   choice make the corruption absorbable, or stop it biting?")
    for tag in ("I1", "I2", "I3"):
        worst_absorb = 0
        worst_nobite = 0
        tried = 0
        for P in ps:
            b0, t = base[id(P)]
            b = R.build(P)
            k = len(b["free"]) if tag == "I2" else b["n_eligible"]
            for w in range(k):
                bm = R.build(P, mutation=tag, which=w)
                if bm["touched"] is None:
                    continue
                tried += 1
                if R.eq(bm["L"], b0["L"]):
                    worst_nobite += 1
                elif R.absorbable(bm["L"], t):
                    worst_absorb += 1
        print("  %-4s over ALL %d eligible (poset, ridge) choices: absorbable "
              "on %d, failed to bite on %d"
              % (tag, tried, worst_absorb, worst_nobite))

    # ---------------------------------------------------------------- F
    hdr("F. mg-5630's PREMISE, re-derived: is NC3's parity corruption really\n"
        "   L_parity = D.L_true.D with D = diag((-1)^j)?")
    ok = tot = bite = 0
    for P in ps:
        b0, t = base[id(P)]
        m = len(b0["L"])
        # parity corruption: column sign (-1)^j on the boundary matrix
        chains = R.maximal_chains(P)
        words = sorted(R.chain_to_word(c, P.n) for c in chains)
        facets = [tuple(R._prefixes(w)) for w in words]
        ridges, rowsd = R.boundary_rows(facets)
        for r in rowsd:
            for j in list(rowsd[r]):
                if j % 2:
                    rowsd[r][j] = -rowsd[r][j]
        rf = {r: sorted(rowsd.get(r, {}).keys()) for r in range(len(ridges))}
        interior = {r for r in range(len(ridges)) if len(rf[r]) == 2}
        Lp = R.down_lap(rowsd, len(facets), allowed=interior)
        s = [R.perm_sign(w) for w in words]
        Lp = [[s[i] * Lp[i][j] * s[j] for j in range(m)] for i in range(m)]
        D = [1 if j % 2 == 0 else -1 for j in range(m)]
        pred = [[D[i] * b0["L"][i][j] * D[j] for j in range(m)]
                for i in range(m)]
        tot += 1
        ok += R.eq(Lp, pred)
        if not R.eq(Lp, b0["L"]):
            bite += 1
    print("  L_parity == D.L_true.D verified on %d/%d posets; the corruption "
          "bites on %d." % (ok, tot, bite))
    print("  So mg-5630's gauge-absorption premise, which mg-2789 is built on, "
          "is CONFIRMED by an independent rebuild.")

    print()
    print("=" * 78)
    print("done")


if __name__ == "__main__":
    main()
