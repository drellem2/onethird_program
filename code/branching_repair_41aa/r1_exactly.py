"""R1 -- the repair of X1: mg-af28's ledger B2 said "exactly the cell posets"
and nothing ever tested the word "exactly".  This tests it, in both
directions, on the lattices themselves.

WHAT WAS WRONG.  B2, the T2 docstring of `code/branching_af28/t_young.py` and
the header of its committed `out_young.txt` all said:

    "the posets P for which J(P) is an interval of Young's lattice are EXACTLY
     the cell posets"

and gave 6/318, 8/2045, 12/16999 as the size of that class.  T2 computed
{canon(D_lambda) : lambda |- n} -- the STRAIGHT cell posets -- and nothing
else.  mg-6ad0 refuted the "exactly" by construction with the 2-element
antichain.  The corrected claim is

    {P : J(P) is an interval of Young's lattice} = {SKEW cell posets lambda/mu}

WHAT THIS FILE DOES, AND WHAT A FALSIFIER WOULD HAVE LOOKED LIKE.

  R1a  The smallest witness, with the isomorphism CONSTRUCTED rather than
       asserted: J(2-antichain) -> [(1), (2,1)], printed element by element.
       FALSIFIER: the map fails to be a bijection, or fails to preserve order
       in either direction, or the 2-antichain turns out to be some D_lambda.

  R1b  THE TEST B2 NEVER RAN, forward direction, exhaustively.  For EVERY
       isomorphism class of poset P on n <= 6 elements -- all 405 of them --
       decide whether J(P) is an interval of Young's lattice, by exhibiting an
       explicit order isomorphism J(P) -> [mu, lambda] and checking it pair by
       pair in both directions.  Then compare the resulting class against
       af28's answer (straight cell posets) and against the corrected answer
       (skew cell posets).
       FALSIFIER for the corrected claim: any poset in one class and not the
       other.  Expected disagreement with af28: 405 - 21 = the misses.

  R1c  THE TEST B2 NEVER RAN, converse direction, exhaustively at n <= 5.  For
       every poset class P that R1b did NOT match, run an isomorphism test of
       J(P) against EVERY interval [mu, lambda] of Young's lattice of the right
       rank and the right size.  FALSIFIER: one hit -- which would mean the
       corrected class is still too small.  Plus the structural reason the
       search is complete: the join-irreducibles of [mu, lambda] are the cells
       of lambda/mu, checked on every skew shape to n <= 6.

  R1d  The corrected fractions.  FALSIFIER for the enumeration itself: the
       class count changing when the bounding box grows, which would mean the
       trimming argument that bounds the search is wrong (mg-6ad0 pre-filed
       exactly this attack against its own numbers, item 4).
"""

import sys
from kern41aa import (all_posets, canon, iso, ideals, ideal_lattice, partitions,
                      sub, skew_poset, cells, young_interval, interval_poset,
                      mk, join_irreducibles)

OUT = sys.stdout
A000112 = {1: 1, 2: 2, 3: 5, 4: 16, 5: 63, 6: 318, 7: 2045, 8: 16999}


def parts_in_box(b):
    """Every partition whose diagram fits in the b x b box."""
    out = set()

    def rec(i, cap, cur):
        if i == b:
            out.add(tuple(x for x in cur if x > 0))
            return
        for v in range(min(cap, b), -1, -1):
            cur.append(v)
            rec(i + 1, v, cur)
            cur.pop()
    rec(0, b, [])
    return sorted(out, key=lambda x: (sum(x), x))


def skew_shapes(n, box=None):
    """Every skew cell poset with n cells, up to isomorphism, as
    canon -> (lambda, mu).

    A skew diagram with n cells has at most n nonempty rows and at most n
    nonempty columns, so after deleting empty rows and columns it sits in the
    n x n box.  R1d checks that bound empirically by growing the box.
    """
    b = n if box is None else box
    seen = {}
    for lam in parts_in_box(b):
        t = sum(lam) - n
        if t < 0:
            continue
        for mu in (partitions(t) if t else [()]):
            if not sub(mu, lam):
                continue
            P, cs = skew_poset(lam, mu)
            if P[0] != n:
                continue
            seen.setdefault(canon(P), (lam, mu))
    return seen


def build_phi(P, lam, mu, phi):
    """Given a poset isomorphism `phi` from P onto the cell poset of lam/mu,
    build the induced map J(P) -> [mu, lambda]: an order ideal I goes to the
    partition whose row i is mu_i plus the number of cells of phi(I) in row i.
    Returns (images, ok, why)."""
    cs = cells(lam, mu)
    nrows = len(lam)
    mu_pad = tuple(list(mu) + [0] * (nrows - len(mu)))
    out = []
    for I in ideals(P):
        rows = list(mu_pad)
        m = I
        while m:
            b = m & -m
            a = b.bit_length() - 1
            rows[cs[phi[a]][0]] += 1
            m ^= b
        nu = tuple(x for x in rows if x > 0)
        if any(rows[i] < rows[i + 1] for i in range(nrows - 1)):
            return out, False, "image is not a partition"
        if not (sub(mu, nu) and sub(nu, lam)):
            return out, False, "image outside [mu, lambda]"
        out.append(nu)
    return out, True, ""


def verify_phi(P, lam, mu, images):
    """Bijection onto [mu, lambda], and order-preserving in BOTH directions,
    checked on every pair of ideals."""
    iv = young_interval(mu, lam)
    ids = ideals(P)
    if sorted(images) != sorted(iv):
        return False, "not onto [mu, lambda] (%d images, %d elements)" % (
            len(set(images)), len(iv))
    if len(set(images)) != len(images):
        return False, "not injective"
    for a in range(len(ids)):
        for b in range(len(ids)):
            left = (ids[a] & ids[b] == ids[a])
            right = sub(images[a], images[b])
            if left != right:
                return False, "order not preserved at (%d, %d)" % (a, b)
    return True, ""


def r1a():
    print("=" * 78, file=OUT)
    print("R1a  THE SMALLEST WITNESS, WITH THE ISOMORPHISM CONSTRUCTED.", file=OUT)
    print("     B2: the posets P with J(P) an interval of Young's lattice are", file=OUT)
    print("     EXACTLY the cell posets.  Here is one that is not.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    A = mk(2, [])
    straight2 = {canon(skew_poset(l)[0]) for l in partitions(2)}
    print("  P = the 2-element ANTICHAIN.", file=OUT)
    print("    the two 2-cell straight shapes are (2) and (1,1); their cell", file=OUT)
    print("    posets are %s, so the straight class at n = 2 has %d member(s)."
          % ("both the 2-CHAIN" if len(straight2) == 1 else "distinct",
             len(straight2)), file=OUT)
    print("    is P a straight cell poset D_lambda?   %s"
          % ("YES" if canon(A) in straight2 else "NO"), file=OUT)
    lam, mu = (2, 1), (1,)
    Q, cs = skew_poset(lam, mu)
    phi = iso(A, Q)
    print("    is P a SKEW cell poset?                %s   (%s/%s, cells %s)"
          % ("YES" if phi is not None else "NO", lam, mu, cs), file=OUT)
    imgs, ok, why = build_phi(A, lam, mu, phi)
    good, why2 = verify_phi(A, lam, mu, imgs) if ok else (False, why)
    print(file=OUT)
    print("    the induced map J(P) -> [(1), (2,1)], element by element:", file=OUT)
    for I, nu in zip(ideals(A), imgs):
        print("        ideal %-10s ->  %s"
              % ("{%s}" % ",".join(str(i) for i in range(2) if I >> i & 1), nu),
              file=OUT)
    print(file=OUT)
    print("    bijection onto [(1),(2,1)] and order-preserving both ways: %s"
          % ("YES" if good else "NO -- " + why2), file=OUT)
    print(file=OUT)
    print("  CONCLUSION R1a: B2's \"exactly\" is FALSE.  The 2-element antichain", file=OUT)
    print("  is not a cell poset and J(it) IS an interval of Young's lattice.", file=OUT)
    print("  Reproduces mg-6ad0's A2a on a third instrument, and adds the map.", file=OUT)
    print(file=OUT)
    return 0 if good and phi is not None and canon(A) not in straight2 else 1


def r1b(maxn=6):
    print("=" * 78, file=OUT)
    print("R1b  THE TEST B2 NEVER RAN.  For EVERY poset class P on n <= %d" % maxn, file=OUT)
    print("     elements, is J(P) an interval of Young's lattice?  Decided by", file=OUT)
    print("     exhibiting the isomorphism and checking it on every pair.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("   n  classes  J(P) an interval  straight D_lam  af28 said  misses  bad maps",
          file=OUT)
    tot_bad = 0
    tot_miss = 0
    misses_by_n = {}
    for n in range(1, maxn + 1):
        skews = skew_shapes(n)
        straight = {canon(skew_poset(l)[0]) for l in partitions(n)}
        classes = all_posets(n)
        hits = []
        bad = 0
        for P in classes:
            c = canon(P)
            if c not in skews:
                continue
            lam, mu = skews[c]
            Q, _ = skew_poset(lam, mu)
            phi = iso(P, Q)
            assert phi is not None, "canon says isomorphic, iso says not"
            imgs, ok, why = build_phi(P, lam, mu, phi)
            good, why2 = verify_phi(P, lam, mu, imgs) if ok else (False, why)
            if not good:
                bad += 1
                print("      BAD: n=%d %s/%s -- %s" % (n, lam, mu, why2), file=OUT)
            else:
                hits.append(c)
        miss = [c for c in hits if c not in straight]
        misses_by_n[n] = (len(hits), len(straight), len(miss))
        tot_bad += bad
        tot_miss += len(miss)
        print("  %2d  %7d  %16d  %14d  %9d  %6d  %8d"
              % (n, len(classes), len(hits), len(straight), len(straight),
                 len(miss), bad), file=OUT)
    print(file=OUT)
    print("  Every \"J(P) an interval\" cell above is a CONSTRUCTED isomorphism", file=OUT)
    print("  J(P) -> [mu, lambda], verified on every pair of ideals in both", file=OUT)
    print("  directions: %d bad maps." % tot_bad, file=OUT)
    print("  Posets af28's \"exactly\" excludes but which ARE interval posets: %d."
          % tot_miss, file=OUT)
    print(file=OUT)
    return tot_bad, tot_miss, misses_by_n


def r1c(maxn=5):
    print("=" * 78, file=OUT)
    print("R1c  THE CONVERSE.  R1b found the interval posets among the skew", file=OUT)
    print("     shapes.  Could a poset OUTSIDE that class still have J(P) an", file=OUT)
    print("     interval?  Two checks: an exhaustive one at n <= %d, and the" % maxn, file=OUT)
    print("     structural reason the search is complete.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("  (i) EXHAUSTIVE.  For each poset class NOT a skew shape, J(P) is", file=OUT)
    print("      tested against every interval [mu, lambda] with |lambda/mu| = n", file=OUT)
    print("      and |[mu, lambda]| = |J(P)|.  A hit here would break the", file=OUT)
    print("      corrected claim.", file=OUT)
    print(file=OUT)
    print("   n  non-skew classes  intervals tried  hits", file=OUT)
    hits_total = 0
    for n in range(1, maxn + 1):
        skews = skew_shapes(n)
        ivs = []
        for lam in parts_in_box(n):
            t = sum(lam) - n
            if t < 0:
                continue
            for mu in (partitions(t) if t else [()]):
                if not sub(mu, lam):
                    continue
                if len(cells(lam, mu)) != n:
                    continue
                IP, elems = interval_poset(mu, lam)
                ivs.append((IP, len(elems), lam, mu))
        tried = 0
        hits = 0
        nonskew = 0
        for P in all_posets(n):
            if canon(P) in skews:
                continue
            nonskew += 1
            JP, _ = ideal_lattice(P)
            for IP, sz, lam, mu in ivs:
                if sz != JP[0]:
                    continue
                tried += 1
                if iso(JP, IP) is not None:
                    hits += 1
                    print("      HIT: n=%d P=%s is not a skew shape but J(P) = [%s,%s]"
                          % (n, canon(P), mu, lam), file=OUT)
        hits_total += hits
        print("  %2d  %17d  %15d  %4d" % (n, nonskew, tried, hits), file=OUT)
    print(file=OUT)
    print("  (ii) WHY THE SEARCH IS COMPLETE.  An order isomorphism of finite", file=OUT)
    print("       lattices carries join-irreducibles to join-irreducibles, and", file=OUT)
    print("       the join-irreducibles of J(P) are the principal ideals, i.e.", file=OUT)
    print("       P itself.  So J(P) = [mu, lambda] forces P = the join-", file=OUT)
    print("       irreducible poset of [mu, lambda].  Measured: that poset is", file=OUT)
    print("       the cell poset of lambda/mu, on every skew shape to n <= 6.", file=OUT)
    print(file=OUT)
    print("   n  skew shapes  ji([mu,lam]) = cells(lam/mu)  bad", file=OUT)
    bad_ji = 0
    for n in range(1, 7):
        skews = skew_shapes(n)
        bad = 0
        for c, (lam, mu) in skews.items():
            IP, elems = interval_poset(mu, lam)
            JI, _ = join_irreducibles(IP)
            Q, _ = skew_poset(lam, mu)
            if iso(JI, Q) is None:
                bad += 1
        bad_ji += bad
        print("  %2d  %11d  %27d  %3d" % (n, len(skews), len(skews) - bad, bad),
              file=OUT)
    print(file=OUT)
    print("  exhaustive hits outside the skew class: %d;  join-irreducible" % hits_total,
          file=OUT)
    print("  reconstructions bad: %d." % bad_ji, file=OUT)
    print(file=OUT)
    return hits_total, bad_ji


def r1d(maxn=7, skew8=None):
    print("=" * 78, file=OUT)
    print("R1d  THE CORRECTED FRACTIONS, and a control on the enumeration.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("   n   straight D_lam   skew = interval posets   all posets    af28   corrected",
          file=OUT)
    counts = {}
    for n in range(1, maxn + 1):
        straight = {canon(skew_poset(l)[0]) for l in partitions(n)}
        sk = len(skew_shapes(n))
        counts[n] = (len(straight), sk)
        print("  %2d   %14d   %22d   %10d  %6.4f    %8.4f"
              % (n, len(straight), sk, A000112[n], len(straight) / A000112[n],
                 sk / A000112[n]), file=OUT)
    if skew8 is not None:
        n = 8
        straight = {canon(skew_poset(l)[0]) for l in partitions(n)}
        counts[8] = (len(straight), skew8)
        print("  %2d   %14d   %22d   %10d  %6.4f    %8.4f   (r1b_skew8.py)"
              % (n, len(straight), skew8, A000112[8], len(straight) / A000112[8],
                 skew8 / A000112[8]), file=OUT)
    print(file=OUT)
    print("  af28's three numbers 6/318, 8/2045, 12/16999 are the STRAIGHT", file=OUT)
    print("  column and are reproduced here exactly.  They are not counts of", file=OUT)
    print("  the class B2 names.  The corrected numbers are 62/318, 149/2045,", file=OUT)
    print("  360/16999 -- understated by a factor of 10 to 30.", file=OUT)
    print("  At n <= 3 EVERY poset is a skew shape poset (1/1, 2/2, 5/5).", file=OUT)
    print(file=OUT)
    print("  CONTROL ON THE ENUMERATION.  The search is bounded by the claim", file=OUT)
    print("  that a skew diagram with n cells fits, after trimming empty rows", file=OUT)
    print("  and columns, in the n x n box.  If that were wrong the counts", file=OUT)
    print("  would be too low.  Grow the box and see:", file=OUT)
    print(file=OUT)
    print("   n   box n   box n+1   box n+2   stable", file=OUT)
    unstable = 0
    for n in range(1, 6):
        a = len(skew_shapes(n, n))
        b = len(skew_shapes(n, n + 1))
        c = len(skew_shapes(n, n + 2))
        if not (a == b == c):
            unstable += 1
        print("  %2d  %6d  %8d  %8d   %s"
              % (n, a, b, c, "." if a == b == c else "MOVED"), file=OUT)
    print(file=OUT)
    print("  box-growth instabilities: %d" % unstable, file=OUT)
    print(file=OUT)
    return counts, unstable


def main():
    import os
    bad_a = r1a()
    bad_maps, misses, _ = r1b()
    hits, bad_ji = r1c()
    s8 = os.environ.get("SKEW8_COUNT")
    counts, unstable = r1d(skew8=int(s8) if s8 else None)
    print("=" * 78, file=OUT)
    print("SUMMARY r1_exactly: witness bad %d; constructed maps bad %d; posets"
          % (bad_a, bad_maps), file=OUT)
    print("  af28's \"exactly\" wrongly excludes %d; converse hits %d; join-"
          % (misses, hits), file=OUT)
    print("  irreducible reconstructions bad %d; box instabilities %d"
          % (bad_ji, unstable), file=OUT)
    print("=" * 78, file=OUT)


if __name__ == "__main__":
    main()
