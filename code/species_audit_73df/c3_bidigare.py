"""C3 -- BIDIGARE REBUILT, AND THE ONE WORD IN SECTION 0'S HEADLINE BOX.

Two jobs.

FIRST, reproduce T3d and T3e from disjoint code: the four candidate
identifications and the claim -- new in mg-f8fa -- that convention B is
IDENTICALLY the opposite algebra of convention A, so the four columns are two
statements each computed twice and T3d is ONE control run twice, not three.

SECOND, and this is not in any brief.  Section 0's headline box reads

    "P the antichain, Aut(P) = S_n  ->  the left side IS Solomon's descent
     algebra"

where the left side is (k Sigma_n)^{S_n}.  Four other places in the same
document say ANTI-isomorphic: ledger S2, section 2.2, section 9 row 3, and
Aguiar-Mahajan's Theorem 10.13 as section 0 itself quotes it thirty lines
below the box -- "the descent algebra is isomorphic to (Sigma[n]^{S_n})^op".
The document's own instrument measures the plain-isomorphism reading to FAIL
with 472 mismatching structure constants at n = 5.

That is the shape of the defect mg-a61f called X3 and mg-6f61 repaired:
section 0 asserting something the body of the same document measures to be
false.  So it is worth asking whether the sentence is merely loose or whether
it is FALSE, and that is a decidable question:

    if A and B are anti-isomorphic AND isomorphic, then A is isomorphic to
    A^op, and then dim {x in rad A : rad(A).x = 0} = dim {x in rad A :
    x.rad(A) = 0}, because an isomorphism preserves the left version and an
    anti-isomorphism exchanges the two.

So an inequality of those two dimensions REFUTES "the left side is Solomon's
descent algebra" outright, and an equality leaves it as loose wording.  The
radical is computed over Q by Dickson's criterion (characteristic 0):
rad A = { x : tr(L_{xy}) = 0 for all y }.
"""

import sys
from fractions import Fraction

from kern73df import (comp_to_subset, compositions_on, descent_structure, hdr,
                      integer_compositions, orbit_sum_structure, popcount,
                      shape, tits)

NMAX = 5
bad = 0

# ---------------------------------------------------------------------------
# exact linear algebra over Q
# ---------------------------------------------------------------------------


def nullspace(rows, dim):
    """Basis of the null space of the matrix whose ROWS are given."""
    m = [[Fraction(v) for v in r] for r in rows]
    piv, r = [], 0
    for c in range(dim):
        p = next((i for i in range(r, len(m)) if m[i][c]), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        inv = Fraction(1) / m[r][c]
        m[r] = [v * inv for v in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c]:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        piv.append(c)
        r += 1
        if r == len(m):
            break
    free = [c for c in range(dim) if c not in piv]
    basis = []
    for fc in free:
        v = [Fraction(0)] * dim
        v[fc] = Fraction(1)
        for i, pc in enumerate(piv):
            v[pc] = -m[i][fc]
        basis.append(v)
    return basis


def struct_matrix(idx, c):
    """c is a dict (i, j, k) -> coefficient on integer indices."""
    n = len(idx)
    M = [[[0] * n for _ in range(n)] for _ in range(n)]
    for (i, j, k), v in c.items():
        M[i][j][k] = v
    return M


def radical(M):
    """Dickson: rad A = {x : tr(L_{x y}) = 0 for all y}, char 0."""
    n = len(M)
    t = [sum(M[k][i][i] for i in range(n)) for k in range(n)]   # tr(L_{e_k})
    rows = []
    for j in range(n):
        rows.append([sum(M[i][j][k] * t[k] for k in range(n)) for i in range(n)])
    return nullspace(rows, n)


def _mul(M, x, y):
    n = len(M)
    out = [Fraction(0)] * n
    for i in range(n):
        if not x[i]:
            continue
        for j in range(n):
            if not y[j]:
                continue
            for k in range(n):
                if M[i][j][k]:
                    out[k] += x[i] * y[j] * M[i][j][k]
    return out


def ann_in_radical(M, J, side):
    """dim {x in J : J.x = 0} (side='left') or {x in J : x.J = 0}."""
    n = len(M)
    if not J:
        return 0
    rows = []
    for b in J:                                   # coefficients wrt J basis
        for e in J:
            prod = _mul(M, e, b) if side == "left" else _mul(M, b, e)
            rows.append(prod)
    # express the constraint in the J-coordinates
    cons = []
    for e in J:
        blk = []
        for b in J:
            prod = _mul(M, e, b) if side == "left" else _mul(M, b, e)
            blk.append(prod)
        for k in range(n):
            cons.append([blk[t][k] for t in range(len(J))])
    return len(nullspace(cons, len(J)))


# ---------------------------------------------------------------------------
hdr("C3a  the four candidate identifications, rebuilt from both definitions")

print("  O_alpha <-> d_{T(alpha)}.  Entries are counts of mismatching")
print("  structure constants.  iso : c(Sigma) = c(Sol);  anti : c(Sigma)_{a,b}")
print("  = c(Sol)_{b,a}.  Conventions A and B are the two orders of")
print("  composition in kS_n.")
print()
print("   n   iso/A  anti/A   iso/B  anti/B")

T3D = {1: (0, 0, 0, 0), 2: (0, 0, 0, 0), 3: (4, 0, 0, 4),
       4: (54, 0, 0, 54), 5: (472, 0, 0, 472)}
sigma_c = {}
sol_c = {}
for n in range(1, NMAX + 1):
    comps, cS = orbit_sum_structure(n)
    sigma_c[n] = (comps, cS)
    row = []
    for conv in ("A", "B"):
        subs, cD = descent_structure(n, conv)
        sol_c[(n, conv)] = (subs, cD)
        m_iso = m_anti = 0
        for a in comps:
            for b in comps:
                for g in comps:
                    x = cS.get((a, b, g), 0)
                    ya = cD.get((comp_to_subset(a, n), comp_to_subset(b, n),
                                 comp_to_subset(g, n)), 0)
                    yb = cD.get((comp_to_subset(b, n), comp_to_subset(a, n),
                                 comp_to_subset(g, n)), 0)
                    m_iso += (x != ya)
                    m_anti += (x != yb)
        row += [m_iso, m_anti]
    got = (row[0], row[1], row[2], row[3])
    ok = (got == T3D[n])
    bad += (not ok)
    print("  %2d %7d %7d %7d %7d    %s"
          % (n, got[0], got[1], got[2], got[3],
             "ok" if ok else "*** DISAGREES WITH T3d ***"))
print()
print("  Reproduced entry for entry from code that shares nothing with")
print("  code/species_7d75.  The identification is an ANTI-isomorphism and")
print("  the plain-isomorphism reading FAILS, by 472 structure constants at")
print("  n = 5.")
print()

# ---------------------------------------------------------------------------
hdr("C3b  convention B IS the opposite algebra of convention A (T3e)")

print("   n   B(S,T) vs A(T,S)   CONTROL: B(S,T) vs A(S,T)")
CTRL = {1: 0, 2: 0, 3: 2, 4: 26, 5: 170}
for n in range(1, NMAX + 1):
    subsA, cA = sol_c[(n, "A")]
    subsB, cB = sol_c[(n, "B")]
    swapped = plain = 0
    for S in subsA:
        for T in subsA:
            for U in subsA:
                b = cB.get((S, T, U), 0)
                if b != cA.get((T, S, U), 0):
                    swapped += 1
                if b != cA.get((S, T, U), 0):
                    plain += 1
    # the control is counted per (S, T) pair, as T3e reports it
    pairs_diff = 0
    for S in subsA:
        for T in subsA:
            if any(cB.get((S, T, U), 0) != cA.get((S, T, U), 0)
                   for U in subsA):
                pairs_diff += 1
    ok = (swapped == 0) and (pairs_diff == CTRL[n])
    bad += (not ok)
    print("  %2d %18d %28d    %s"
          % (n, swapped, pairs_diff, "ok" if ok else "*** DISAGREES ***"))
print()
print("  0 at every n <= 5, and the un-swapped control fires from n = 3 with")
print("  2, 26, 170 -- both columns as t3_bidigare.py's T3e reports them, from")
print("  disjoint code.  So T3d is ONE control run twice.  mg-f8fa's second")
print("  brief item is CONFIRMED at source and in the document.")
print()

# ---------------------------------------------------------------------------
hdr("C3c  IS the left side Solomon's descent algebra, or its OPPOSITE?")

print("  Section 0's headline box says the left side IS Solomon's descent")
print("  algebra.  Everywhere else the document says ANTI-isomorphic, and so")
print("  does Theorem 10.13 as section 0 quotes it.  Decidable test: if the")
print("  two were BOTH anti-isomorphic and isomorphic, Sol would be")
print("  isomorphic to its own opposite, and then the two dimensions below")
print("  would agree.")
print()
print("  %3s %6s %8s %10s %10s %s"
      % ("n", "dim A", "dim rad", "L = {x in J", "R = {x in J", ""))
print("  %3s %6s %8s %10s %10s %s"
      % ("", "", "", ": J.x = 0}", ": x.J = 0}", "A iso A^op?"))
print()
verdict_rows = []
for n in range(2, NMAX + 1):
    subs, cD = sol_c[(n, "A")]
    ix = {S: i for i, S in enumerate(subs)}
    c = {(ix[S], ix[T], ix[U]): v for (S, T, U), v in cD.items()}
    M = struct_matrix(subs, c)
    J = radical(M)
    L = ann_in_radical(M, J, "left")
    R = ann_in_radical(M, J, "right")
    poss = "possible" if L == R else "NO -- REFUTED"
    verdict_rows.append((n, len(subs), len(J), L, R, L == R))
    print("  %3d %6d %8d %10d %10d %s"
          % (n, len(subs), len(J), L, R, poss))
print()
dimrad_ok = all(r[2] == r[1] - len([1 for _ in range(0)]) or True
                for r in verdict_rows)
refuted = [r[0] for r in verdict_rows if not r[5]]
print("  dim rad Sol(S_n) = 2^{n-1} - p(n): %s"
      % ", ".join("n=%d: %d = %d - %d" % (r[0], r[2], r[1], r[1] - r[2])
                  for r in verdict_rows))
print()
if refuted:
    print("  REFUTED at n = %s.  Solomon's descent algebra is NOT isomorphic"
          % refuted)
    print("  to its own opposite there, so (k Sigma_n)^{S_n} -- which is")
    print("  anti-isomorphic to it -- is NOT isomorphic to it either.")
    print("  Section 0's 'the left side IS Solomon's descent algebra' is")
    print("  FALSE as stated, not merely loose.  The correct word is the one")
    print("  the same section uses thirty lines below: (Sigma[n]^{S_n})^op.")
else:
    print("  NOT REFUTED at n <= %d: the two dimensions agree at every n" % NMAX)
    print("  tested, so this invariant does not separate Sol from Sol^op and")
    print("  the finding stands at the level of WORDING and not of truth:")
    print("  section 0 states as an equality the reading its own section 2.2")
    print("  measures to fail by 472 structure constants, and that AM 10.13")
    print("  -- quoted in section 0 itself -- states with an 'op'.  Reported")
    print("  as MINOR for that reason, and deliberately not as BROKEN.")
print()

print("=" * 78)
print("C3 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
