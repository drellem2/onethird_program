"""INDEPENDENT REBUILD of the face-geometry machinery, for the mg-fcf1 audit of
NEGATIVE CONTROL 4 (mg-2789).

Nothing here imports face_complex.py, controls.py or posets.py.  Everything is
rebuilt from the definitions, by a DIFFERENT route where a different route
exists:

  * facets are built as the maximal chains of the proper part of the ideal
    lattice J(P) (the definition of F(P) as an order complex), NOT as the
    prefix words of a linear extension.  `le_to_facet` is exactly one of the
    sites under audit, so the audit must not use it.
  * the word attached to a facet is recovered from the chain afterwards, and is
    used only for the ORDERING of the facet index set and for the orientation
    twist sgn(w).
  * poset enumeration up to isomorphism is done by canonical relabelling.

The four NEGATIVE CONTROL 4 mutations are re-implemented here from their prose
descriptions in controls.py, not by calling `top_laplacians(incidence_mode=...)`.
"""

from itertools import combinations, permutations


# --------------------------------------------------------------------------
# posets
# --------------------------------------------------------------------------

def tclose(n, rel):
    rel = set(rel)
    changed = True
    while changed:
        changed = False
        for (a, b) in list(rel):
            for (c, d) in list(rel):
                if b == c and (a, d) not in rel:
                    rel.add((a, d))
                    changed = True
    return frozenset(rel)


class Pos:
    __slots__ = ("n", "less")

    def __init__(self, n, rel):
        self.n = n
        self.less = tclose(n, rel)

    def key(self):
        best = None
        for g in permutations(range(self.n)):
            r = tuple(sorted((g[a], g[b]) for (a, b) in self.less))
            if best is None or r < best:
                best = r
        return (self.n, best)

    def is_antichain(self):
        return not self.less

    def is_chain(self):
        return len(self.less) == self.n * (self.n - 1) // 2

    def covers(self):
        out = []
        for (a, b) in sorted(self.less):
            if not any((a, c) in self.less and (c, b) in self.less
                       for c in range(self.n)):
                out.append("%d<%d" % (a, b))
        return " ".join(out) if out else "(antichain)"


def posets(n):
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    seen = {}
    for k in range(len(pairs) + 1):
        for sub in combinations(pairs, k):
            ok = all(not (b == c and (a, d) not in set(sub))
                     for (a, b) in sub for (c, d) in sub)
            if not ok:
                continue
            P = Pos(n, sub)
            kk = P.key()
            if kk not in seen:
                seen[kk] = P
    return [seen[k] for k in sorted(seen)]


def population(nmax=5, nmin=2):
    return [P for n in range(nmin, nmax + 1) for P in posets(n)]


# --------------------------------------------------------------------------
# the face complex, built as the order complex of the proper part of J(P)
# --------------------------------------------------------------------------

def ideals(P):
    """Order ideals of P as bitmasks."""
    out = []
    for m in range(1 << P.n):
        if all(not ((m >> b) & 1) or ((m >> a) & 1)
               for (a, b) in P.less):
            out.append(m)
    return out


def proper_ideals(P):
    full = (1 << P.n) - 1
    return [m for m in ideals(P) if m != 0 and m != full]


def maximal_chains(P):
    """Facets of F(P) = maximal chains of proper nonempty ideals, each as a
    tuple of masks increasing by inclusion.  Built from the lattice, not from
    words.  A maximal chain has n-1 elements (one of each cardinality)."""
    V = proper_ideals(P)
    bysize = {}
    for m in V:
        bysize.setdefault(bin(m).count("1"), []).append(m)
    out = []

    def rec(chain, size):
        if size == P.n:
            out.append(tuple(chain))
            return
        for m in bysize.get(size, []):
            if not chain or (chain[-1] & m) == chain[-1]:
                rec(chain + [m], size + 1)
    rec([], 1)
    return out


def chain_to_word(chain, n):
    """The word whose prefixes are `chain`.  Only used for ordering and signs."""
    w, prev = [], 0
    for m in list(chain) + [(1 << n) - 1]:
        d = m & ~prev
        assert d and (d & (d - 1)) == 0, "not a maximal chain"
        w.append(d.bit_length() - 1)
        prev = m
    return tuple(w)


def linexts(P):
    """Linear extensions, built by repeated minimal-element choice."""
    out = []

    def rec(mask, w):
        if len(w) == P.n:
            out.append(tuple(w))
            return
        for x in range(P.n):
            if (mask >> x) & 1:
                continue
            if all((mask >> a) & 1 for a in range(P.n) if (a, x) in P.less):
                rec(mask | (1 << x), w + [x])
    rec(0, [])
    return sorted(out)


def perm_sign(w):
    inv = sum(1 for i in range(len(w)) for j in range(i + 1, len(w))
              if w[i] > w[j])
    return -1 if inv % 2 else 1


# --------------------------------------------------------------------------
# boundary, Laplacians
# --------------------------------------------------------------------------

def boundary_rows(facets):
    """rows[ridge] = {facet index: coefficient}, standard simplicial signs.

    Facet vertices are listed in increasing order (by inclusion for a chain);
    the boundary of (v_0,...,v_d) is sum_i (-1)^i (v_0,..,^v_i,..,v_d).
    """
    ridge_index, rows = {}, {}
    for j, f in enumerate(facets):
        for i in range(len(f)):
            g = f[:i] + f[i + 1:]
            if g not in ridge_index:
                ridge_index[g] = None
    ridges = sorted(ridge_index)
    ridge_index = {g: r for r, g in enumerate(ridges)}
    for j, f in enumerate(facets):
        for i in range(len(f)):
            g = f[:i] + f[i + 1:]
            r = ridge_index[g]
            rows.setdefault(r, {})
            rows[r][j] = rows[r].get(j, 0) + (-1) ** i
    return ridges, rows


def down_lap(rows, ncols, allowed=None):
    L = [[0] * ncols for _ in range(ncols)]
    for r, row in rows.items():
        if allowed is not None and r not in allowed:
            continue
        it = list(row.items())
        for (j1, c1) in it:
            for (j2, c2) in it:
                L[j1][j2] += c1 * c2
    return L


def build(P, mutation="true", which=0):
    """The audited object, rebuilt.  Returns a dict with L_rel (twisted) and
    the bookkeeping the audit needs.

    `mutation` re-implements NEGATIVE CONTROL 4's four sites from their prose:
      "true"        no mutation
      "I1"          one interior ridge's second incidence re-targeted onto a
                    facet it does not meet
      "I2"          one free ridge counted as interior
      "I3"          one interior ridge deleted from the complex
      "I4"          facets built from the prefixes of w[1:] (the off-by-one)
      "swap01"      facets 0 and 1 exchanged
    `which` selects WHICH eligible ridge is mutated (0 = the first, as the
    audited code does); the audit sweeps it to test instance-dependence.
    """
    n = P.n
    chains = maximal_chains(P)
    words = sorted(chain_to_word(c, n) for c in chains)
    assert words == linexts(P), "the two routes to L(P) disagree"
    if mutation == "I4":
        facets = [tuple(_prefixes_offbyone(w)) for w in words]
    else:
        facets = [tuple(_prefixes(w)) for w in words]
    if mutation == "swap01" and len(facets) >= 2:
        facets[0], facets[1] = facets[1], facets[0]

    ridges, rows = boundary_rows(facets)
    nr, nc = len(ridges), len(facets)
    rf = {r: sorted(rows.get(r, {}).keys()) for r in range(nr)}

    touched = None
    if mutation == "I1":
        elig = [r for r in range(nr) if len(rf[r]) == 2]
        if elig and nc >= 3:
            r = elig[which % len(elig)]
            j1, j2 = rf[r]
            j3 = next(j for j in range(nc) if j not in (j1, j2))
            rows[r][j3] = rows[r].pop(j2)
            rf[r] = sorted(rows[r].keys())
            touched = r
    elif mutation == "I3":
        elig = [r for r in range(nr) if len(rf[r]) == 2]
        if elig:
            r = elig[which % len(elig)]
            del rows[r]
            rf[r] = []
            touched = r

    interior = {r for r in range(nr) if len(rf[r]) == 2}
    free = {r for r in range(nr) if len(rf[r]) == 1}
    multi = {r for r in range(nr) if len(rf[r]) >= 3}
    if mutation == "true":
        assert interior | free == set(range(nr))
    if mutation == "I2":
        elig = sorted(free)
        if elig:
            touched = elig[which % len(elig)]
            interior = interior | {touched}

    L = down_lap(rows, nc, allowed=interior)
    s = [perm_sign(w) for w in words]
    Lt = [[s[i] * L[i][j] * s[j] for j in range(nc)] for i in range(nc)]
    return {
        "P": P, "words": words, "facets": facets, "ridges": ridges,
        "rows": rows, "interior": interior, "free": free, "multi": multi,
        "L_raw": L, "L": Lt, "touched": touched, "n_facets": nc,
        "n_eligible": len([r for r in range(nr) if len(rf[r]) == 2]),
    }


def _prefixes(w):
    out, m = [], 0
    for t in range(len(w) - 1):
        m |= 1 << w[t]
        out.append(m)
    return out


def _prefixes_offbyone(w):
    out, m = [], 0
    for t in range(1, len(w)):
        m |= 1 << w[t]
        out.append(m)
    return out


def target_DA(P):
    """D - A of the adjacent-transposition graph on L(P), built from the words."""
    w = linexts(P)
    idx = {x: i for i, x in enumerate(w)}
    m = len(w)
    A = [[0] * m for _ in range(m)]
    for x in w:
        i = idx[x]
        for t in range(P.n - 1):
            y = list(x)
            y[t], y[t + 1] = y[t + 1], y[t]
            y = tuple(y)
            if y in idx:
                A[i][idx[y]] = 1
    return [[(sum(A[i]) if i == j else 0) - A[i][j] for j in range(m)]
            for i in range(m)]


# --------------------------------------------------------------------------
# the two predicates the audited row is scored on, re-implemented
# --------------------------------------------------------------------------

def eq(A, B):
    return len(A) == len(B) and all(a == b for ra, rb in zip(A, B)
                                   for a, b in zip(ra, rb))


def absorbable(A, B):
    """Exists a diagonal sign matrix S with S.A.S == B?

    Independent implementation: BFS over the components of the off-diagonal
    support graph, then EXPLICIT RECONSTRUCTION of S and a direct matrix
    comparison, so a True answer is self-certifying.  A False answer is exact
    too: within a component the signs are forced up to a global flip, and a
    global flip per component leaves S.A.S unchanged.
    """
    m = len(A)
    if m != len(B):
        return False
    for i in range(m):
        if A[i][i] != B[i][i]:
            return False
        for j in range(m):
            if abs(A[i][j]) != abs(B[i][j]):
                return False
    s = [None] * m
    for root in range(m):
        if s[root] is not None:
            continue
        s[root] = 1
        stack = [root]
        while stack:
            i = stack.pop()
            for j in range(m):
                if i == j or A[i][j] == 0:
                    continue
                want = s[i] * (1 if B[i][j] == A[i][j] else -1)
                if s[j] is None:
                    s[j] = want
                    stack.append(j)
                elif s[j] != want:
                    return False
    return all(s[i] * A[i][j] * s[j] == B[i][j]
               for i in range(m) for j in range(m))


def _mat_mul_trace(A, k):
    """trace(A^k) for small k, by repeated multiplication of the rows needed."""
    m = len(A)
    if k == 1:
        return sum(A[i][i] for i in range(m))
    if k == 2:
        return sum(A[i][j] * A[j][i] for i in range(m) for j in range(m))
    B = [row[:] for row in A]
    for _ in range(k - 2):
        B = [[sum(B[i][t] * A[t][j] for t in range(m)) for j in range(m)]
             for i in range(m)]
    return sum(sum(B[i][t] * A[t][i] for t in range(m)) for i in range(m))


def det_shift_mod(A, k, p=(1 << 61) - 1):
    """det(A - k.I) mod p by elimination over F_p."""
    m = len(A)
    B = [[(A[i][j] - (k if i == j else 0)) % p for j in range(m)]
         for i in range(m)]
    det = 1
    for c in range(m):
        piv = next((r for r in range(c, m) if B[r][c]), None)
        if piv is None:
            return 0
        if piv != c:
            B[c], B[piv] = B[piv], B[c]
            det = -det
        det = det * B[c][c] % p
        inv = pow(B[c][c], p - 2, p)
        for r in range(c + 1, m):
            f = B[r][c] * inv % p
            if f:
                Bc, Br = B[c], B[r]
                for t in range(c, m):
                    Br[t] = (Br[t] - f * Bc[t]) % p
    return det % p


def spectrum_provably_moved(A, B, shifts=(3, 5, 7, 11, 13)):
    """One-sided: True means the characteristic polynomials PROVABLY differ."""
    for k in (1, 2, 3):
        if _mat_mul_trace(A, k) != _mat_mul_trace(B, k):
            return True
    for k in shifts:
        if det_shift_mod(A, k) != det_shift_mod(B, k):
            return True
    return False


def charpoly_agrees_everywhere(A, B, npts=None):
    """Strong isospectrality evidence: det(.-kI) mod a 61-bit prime at more
    distinct shifts than the degree, so the two characteristic polynomials
    agree mod p as polynomials.  Used only to CORROBORATE a structural proof of
    isospectrality, never as one."""
    m = len(A)
    npts = npts if npts is not None else m + 2
    return all(det_shift_mod(A, k) == det_shift_mod(B, k)
               for k in range(1, npts + 1))
