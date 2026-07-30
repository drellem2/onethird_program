"""mg-1c80 -- the audit kernel.  A SECOND IMPLEMENTATION of everything mg-da45's
repair measures, written from the specifications rather than from its code.

WHY IT EXISTS.  mg-da45 repairs a control whose defect was a TRUE condition with a
FALSE printed reason.  The failure mode of that repair is a NEW plausible reason
that is also not what decides, so every number the repair prints has to be
recomputed by something that shares no code with it.

WHAT THIS SHARES WITH THE OBJECT UNDER AUDIT: nothing but `posets.all_posets`
(the population, itself A000112-checked) and `face_complex.Poset` (the data
type).  In particular this module does NOT call

  * `face_complex.top_laplacians`          -- facets, ridges, boundary and the
  * `face_complex.boundary_matrix`            relative Laplacian are rebuilt here
  * `face_complex.down_laplacian_from_boundary`  from the definitions,
  * `face_complex.at_laplacian`            -- the target is rebuilt here,
  * `face_complex.absorbable_by_diagonal_twist`  -- decided here by 2-colouring
                                              and, where feasible, brute force,
  * `controls.deciding_gate` / `controls.entry_mismatches`,
  * `controls.py` at all.

`a1_gates.py` cross-checks this rebuild against `face_complex` matrix-for-matrix
before using any number from it; a disagreement there is a finding either way.
"""

from itertools import permutations


# --------------------------------------------------------------------------
# population and words
# --------------------------------------------------------------------------

def my_linear_extensions(P):
    """Linear extensions of P as words, sorted.  Rebuilt from the definition."""
    n = P.n
    pred = {x: {a for a in range(n) if (a, x) in P.less} for x in range(n)}
    out = []

    def rec(placed, word):
        if len(word) == n:
            out.append(tuple(word))
            return
        for x in range(n):
            if x in placed:
                continue
            if pred[x] <= placed:
                rec(placed | {x}, word + [x])

    rec(frozenset(), [])
    out.sort()
    return out


def my_sign(w):
    """Sign of the word as a permutation, by inversion parity."""
    inv = 0
    for i in range(len(w)):
        for j in range(i + 1, len(w)):
            if w[i] > w[j]:
                inv += 1
    return -1 if inv % 2 else 1


# --------------------------------------------------------------------------
# the face complex, rebuilt
# --------------------------------------------------------------------------

def facets_true(w):
    """Prefixes w[:1], ..., w[:n-1] as bitmask chains -- `le_to_facet`'s rule."""
    chain, mask = [], 0
    for t in range(len(w) - 1):
        mask |= 1 << w[t]
        chain.append(mask)
    return tuple(chain)


def facets_offbyone(w):
    """Prefixes of w[1:] -- `le_to_facet_offbyone`'s rule, the I4 corruption."""
    chain, mask = [], 0
    for t in range(1, len(w)):
        mask |= 1 << w[t]
        chain.append(mask)
    return tuple(chain)


def rot(w):
    """Left cyclic rotation of POSITIONS: (w0,w1,...,w_{n-1}) -> (w1,...,w_{n-1},w0).

    The identity the repair's docstring asserts is
    `facets_offbyone(w) == facets_true(rot(w))`; `a2_antichain.py` checks it.
    """
    return tuple(w[1:]) + (w[0],)


def build(P, mode="true"):
    """(L_rel, m) for the poset P under incidence corruption `mode`, rebuilt from
    the mutation specifications in `face_complex.INCIDENCE_MODES`' docstring.

    Returns the UNTWISTED relative top Laplacian as a dense list of lists.
    """
    les = my_linear_extensions(P)
    m = len(les)
    if mode == "facet_offbyone":
        facets = [facets_offbyone(w) for w in les]
    else:
        facets = [facets_true(w) for w in les]
    if mode == "facet_swap01" and m >= 2:
        facets[0], facets[1] = facets[1], facets[0]

    ridge_set = set()
    for f in facets:
        for i in range(len(f)):
            ridge_set.add(f[:i] + f[i + 1:])
    ridges = sorted(ridge_set)
    ridx = {r: i for i, r in enumerate(ridges)}

    # standard simplicial boundary: d(v_0..v_d) = sum_i (-1)^i (v_0..^v_i..v_d)
    rows = {}
    for j, f in enumerate(facets):
        for i in range(len(f)):
            r = ridx[f[:i] + f[i + 1:]]
            rows.setdefault(r, {})
            rows[r][j] = rows[r].get(j, 0) + (-1) ** i

    incid = {r: sorted(rows.get(r, {}).keys()) for r in range(len(ridges))}

    if mode == "ridge_facets":
        for r in range(len(ridges)):
            if len(incid[r]) != 2:
                continue
            j1, j2 = incid[r]
            j3 = next((j for j in range(m) if j not in (j1, j2)), None)
            if j3 is None:
                break
            rows[r][j3] = rows[r].pop(j2)
            incid[r] = sorted(rows[r].keys())
            break
    elif mode == "ridge_drop":
        for r in range(len(ridges)):
            if len(incid[r]) == 2:
                del rows[r]
                incid[r] = []
                break

    interior = {r for r in range(len(ridges)) if len(incid[r]) == 2}
    if mode == "split_free_as_interior":
        free = {r for r in range(len(ridges)) if len(incid[r]) == 1}
        if free:
            interior = interior | {min(free)}

    L = [[0] * m for _ in range(m)]
    for r, row in rows.items():
        if r not in interior:
            continue
        items = list(row.items())
        for (j1, c1) in items:
            for (j2, c2) in items:
                L[j1][j2] += c1 * c2
    return L, m


def twisted(P, mode="true"):
    """E . L^rel . E with E = diag(sgn w) -- the left-hand side of claim (1)."""
    les = my_linear_extensions(P)
    L, m = build(P, mode)
    s = [my_sign(w) for w in les]
    return [[s[i] * L[i][j] * s[j] for j in range(m)] for i in range(m)]


def target(P):
    """D - A on the adjacent-transposition graph of L(P) -- claim (1)'s RHS,
    rebuilt from the words and never from the complex."""
    les = my_linear_extensions(P)
    idx = {w: i for i, w in enumerate(les)}
    m = len(les)
    A = [[0] * m for _ in range(m)]
    for w in les:
        i = idx[w]
        for t in range(P.n - 1):
            v = list(w)
            v[t], v[t + 1] = v[t + 1], v[t]
            v = tuple(v)
            if v in idx:
                A[i][idx[v]] = 1
    return [[(sum(A[i]) if i == j else 0) - A[i][j] for j in range(m)]
            for i in range(m)]


def parity_gauge(P):
    """NEGATIVE CONTROL 3's facet-parity corruption, rebuilt: the boundary's
    j-th column is globally negated for odd j, then twisted.  Built here as a
    CORRUPTED BOUNDARY, not as a conjugation, so that "it is D.L.D by
    construction" is a claim this module can test rather than assume."""
    les = my_linear_extensions(P)
    m = len(les)
    facets = [facets_true(w) for w in les]
    ridge_set = set()
    for f in facets:
        for i in range(len(f)):
            ridge_set.add(f[:i] + f[i + 1:])
    ridges = sorted(ridge_set)
    ridx = {r: i for i, r in enumerate(ridges)}
    rows = {}
    for j, f in enumerate(facets):
        col = 1 if j % 2 == 0 else -1
        for i in range(len(f)):
            r = ridx[f[:i] + f[i + 1:]]
            rows.setdefault(r, {})
            rows[r][j] = rows[r].get(j, 0) + (-1) ** i * col
    interior = {r for r in range(len(ridges)) if len(rows.get(r, {})) == 2}
    L = [[0] * m for _ in range(m)]
    for r, row in rows.items():
        if r not in interior:
            continue
        items = list(row.items())
        for (j1, c1) in items:
            for (j2, c2) in items:
                L[j1][j2] += c1 * c2
    s = [my_sign(w) for w in les]
    return [[s[i] * L[i][j] * s[j] for j in range(m)] for i in range(m)]


# --------------------------------------------------------------------------
# absorbability, decided twice, by neither of the author's routes
# --------------------------------------------------------------------------

def absorbable_2col(A, B):
    """Is there s in {+-1}^m with s_i A_ij s_j == B_ij for all i,j?

    Decided by 2-COLOURING the graph of nonzero off-diagonal entries with
    breadth-first search, not by the union-find `face_complex` uses.
    """
    m = len(A)
    if m != len(B):
        return False
    for i in range(m):
        if len(A[i]) != len(B[i]):
            return False
        for j in range(m):
            if abs(A[i][j]) != abs(B[i][j]):
                return False
        if A[i][i] != B[i][i]:
            return False
    colour = [None] * m
    for start in range(m):
        if colour[start] is not None:
            continue
        colour[start] = 0
        stack = [start]
        while stack:
            x = stack.pop()
            for y in range(m):
                if y == x or A[x][y] == 0:
                    continue
                need = 0 if B[x][y] == A[x][y] else 1
                c = colour[x] ^ need
                if colour[y] is None:
                    colour[y] = c
                    stack.append(y)
                elif colour[y] != c:
                    return False
    return True


def absorbable_brute(A, B):
    """The same question by exhaustive search over all 2^m sign vectors.  Only
    called for small m -- it exists to check `absorbable_2col`."""
    m = len(A)
    if m != len(B):
        return False
    for bits in range(1 << m):
        s = [1 if (bits >> i) & 1 == 0 else -1 for i in range(m)]
        if all(s[i] * A[i][j] * s[j] == B[i][j]
               for i in range(m) for j in range(m)):
            return True
    return False


# --------------------------------------------------------------------------
# gate attribution -- TWO definitions, deliberately
# --------------------------------------------------------------------------

def gate_execution(A, B):
    """The gate the predicate `absorbable_by_diagonal_twist` ACTUALLY reaches
    first, emulating its loop exactly (face_complex.py:767-775):

        for i:  check the DIAGONAL of row i
                for j:  check the MAGNITUDE of entry (i, j)

    The two gates are INTERLEAVED BY ROW.  A pair whose diagonal moves in row 4
    and whose magnitudes move in row 0 exits at the magnitude comparison, not
    the diagonal one.  This function reports where the predicate exits.
    """
    m = len(A)
    if m != len(B):
        return "shape"
    for i in range(m):
        if len(A[i]) != len(B[i]):
            return "shape"
        if A[i][i] != B[i][i]:
            return "diagonal"
        for j in range(m):
            if abs(A[i][j]) != abs(B[i][j]):
                return "magnitude"
    return "parity"


def gate_priority(A, B):
    """The gate `controls.deciding_gate` reports: ALL diagonals are tested
    before ANY magnitude.  A relabelling of the predicate's gates by priority,
    not a trace of the predicate."""
    m = len(A)
    if m != len(B) or any(len(A[i]) != len(B[i]) for i in range(m)):
        return "shape"
    if any(A[i][i] != B[i][i] for i in range(m)):
        return "diagonal"
    if any(abs(A[i][j]) != abs(B[i][j]) for i in range(m) for j in range(m)):
        return "magnitude"
    return "parity"


def census(A, B, offdiag_only=False):
    """(magnitude mismatches, sign-only mismatches) by ENTRY.

    `offdiag_only` exists because the repair prints its magnitude count as
    "off-diagonal magnitudes" while `controls.entry_mismatches` counts the whole
    matrix; both are computed here so the difference can be measured.
    """
    m = len(A)
    mag = sgn = 0
    for i in range(m):
        for j in range(m):
            if offdiag_only and i == j:
                continue
            if abs(A[i][j]) != abs(B[i][j]):
                mag += 1
            elif A[i][j] != B[i][j]:
                sgn += 1
    return mag, sgn


def eq(A, B):
    if len(A) != len(B):
        return False
    return all(len(a) == len(b) and all(x == y for x, y in zip(a, b))
               for a, b in zip(A, B))


SCORED_MUTATIONS = [
    ("I1", "ridge_facets"),
    ("I2", "split_free_as_interior"),
    ("I3", "ridge_drop"),
    ("I4", "facet_offbyone"),
]
