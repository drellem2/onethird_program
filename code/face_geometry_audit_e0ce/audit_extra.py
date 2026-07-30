#!/usr/bin/env python3
"""mg-e0ce extra audit checks.

  X1  PURITY: is every element of Sur_iso(P,[n-1]) a face of some facet?
      (their L3 claims F(P) is PURE of dimension n-2; their PC3 only checks
      the whole complex at n<=4.  Checked here independently for n<=6.)

  X2  The left/value action: is the antichain a witness against claim (2) at
      EVERY n >= 3?  Section 0 asserts this for all n; ledger row D2 labels it
      PROVEN-by-computation on n <= 5 only.  Checked here to n = 8, and the
      one-line proof is exhibited: s_1 s_2 is a right-neighbour of s_1 but is
      not of the form s_j s_1.

  X3  Construction-side negative control the deliverable lacks: perturb the
      SIMPLICIAL SIGNS of the boundary in a facet-dependent way; the identity
      must be rejected.  (All-+1 signs do NOT get rejected -- see audit_rebuild.)
"""
from itertools import permutations
from audit_rebuild import (posets_upto_iso, sur_iso, linear_extensions, merge,
                           _claim1_with_signs)


def purity(nmax=6):
    print("X1 -- PURITY of F(P): every Sur_iso(P,[n-1]) face lies in a facet?")
    bad = []
    tot = 0
    for n in range(2, nmax + 1):
        for rel in posets_upto_iso(n):
            tot += 1
            facets = sur_iso(rel, n, n)
            ridges = set(sur_iso(rel, n, n - 1))
            covered = set()
            for f in facets:
                for t in range(1, n):
                    covered.add(merge(f, t))
            if covered != ridges:
                bad.append((n, sorted(rel), len(ridges - covered)))
    print(f"   {tot - len(bad)}/{tot} posets (2<=n<={nmax}) PURE; "
          f"violations: {bad[:5] if bad else 'none'}")


def left_vs_right(nmax=8):
    print("X2 -- antichain as a witness against the LEFT/value reading of claim (2)")
    for n in range(2, nmax + 1):
        Sn = list(permutations(range(n)))
        sidx = {w: i for i, w in enumerate(Sn)}
        differs = None
        for w in Sn:
            R = set()
            Lf = set()
            for t in range(n - 1):
                v = list(w); v[t], v[t + 1] = v[t + 1], v[t]
                R.add(tuple(v))
                Lf.add(tuple((t + 1) if x == t else (t if x == t + 1 else x) for x in w))
            if R != Lf:
                differs = (w, sorted(R - Lf)[:1])
                break
        print(f"   n={n}: right- and left-Cayley neighbourhoods differ? "
              f"{'YES' if differs else 'NO '}   first witness w={differs[0] if differs else '-'}")
    print("   proof for all n>=3: take w = s_1.  Right-neighbours of s_1 include")
    print("   s_1 s_2; left-neighbours are {s_j s_1}.  s_1 s_2 != s_2 s_1, and for")
    print("   j>=3, s_j s_1 = s_1 s_j != s_1 s_2.  So the neighbourhoods differ,")
    print("   and on the antichain the compression is the whole matrix. QED")


def construction_side_control():
    print("X3 -- construction-side negative control (missing from the deliverable)")
    rows = []
    for n in (3, 4, 5):
        for rel in posets_upto_iso(n)[:20]:
            rows.append((n, _claim1_with_signs(rel, n, "true"),
                         _claim1_with_signs(rel, n, "allplus"),
                         _claim1_with_signs(rel, n, "parity"),
                         len(linear_extensions(rel, n))))
    ok_true = sum(1 for r in rows if r[1])
    surv_plus = sum(1 for r in rows if r[2])
    rej_par = sum(1 for r in rows if not r[3])
    bites = sum(1 for r in rows if r[4] >= 2)
    print(f"   {len(rows)} posets: true signs pass {ok_true}; "
          f"all-+1 signs STILL pass {surv_plus} (control cannot fire); "
          f"facet-parity signs rejected {rej_par} of {bites} where |L|>=2")


if __name__ == "__main__":
    purity()
    print()
    left_vs_right()
    print()
    construction_side_control()
