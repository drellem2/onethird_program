"""lib_c4f5 — the audit instrument for mg-c4f5.

INDEPENDENT OF `code/libweak_c3ca/`: nothing here imports lib_c3ca, and the poset
representation, the linear-extension counting and the pair probabilities are all built
from scratch. The one deliberate overlap is the POPULATION definition (naturally
labelled posets on [n]) — sharing the population is the point of a reproduction; sharing
the parser would defeat it.

Exact arithmetic everywhere except the eigenvalue step, which is float by necessity and
is the ONLY place a tolerance appears. It is declared at its call sites.

Representation
--------------
A poset on [0..n-1] is `(n, up)` where `up[x]` is a bitmask of the elements STRICTLY
above `x`, and the labelling is natural: `x <_P y` implies `x < y` as integers.
`down[x]` is the mirror.

Everything below runs off ORDER IDEALS (down-sets), not off enumerated linear
extensions.  For an ideal `S` (bitmask), `nin[S]` = number of ways to build `S` as a
prefix of a linear extension, and `nout[S]` = number of linear extensions of the
complement.  Then for every ideal `S` and every `x` with `S u {x}` an ideal,

    #{ linear extensions placing x at position |S| }  contributed by S
        = nin[S] * nout[S | bit(x)]

and summing over the relevant `S` gives positions, pair orders and the footrule with no
enumeration of L(P) at all.  This is what makes n = 7 reachable.
"""

from itertools import combinations
from fractions import Fraction
import math


# --------------------------------------------------------------------------- posets

def poset_from_pairs(n, pairs):
    """Build (n, up, down) from a set of covering-or-not pairs; transitively closes."""
    up = [0] * n
    for (a, b) in pairs:
        if a == b:
            raise ValueError("reflexive pair")
        if a > b:
            raise ValueError("not naturally labelled: %d < %d required" % (a, b))
        up[a] |= 1 << b
    # transitive closure (Floyd-Warshall on bitmasks; labels are topologically sorted)
    for k in range(n - 1, -1, -1):
        for x in range(n):
            if up[x] >> k & 1:
                up[x] |= up[k]
    down = [0] * n
    for x in range(n):
        for y in range(n):
            if up[x] >> y & 1:
                down[y] |= 1 << x
    return (n, tuple(up), tuple(down))


def is_transitively_closed(n, up):
    for x in range(n):
        for y in range(n):
            if up[x] >> y & 1 and (up[x] & up[y]) != up[y]:
                return False
    return True


def gen_natural_posets(n):
    """Every naturally labelled poset on [0..n-1], i.e. every transitively closed
    subset of {(i,j) : i < j}.

    Built by the ideal recursion: a naturally labelled poset on [n] is a naturally
    labelled poset Q on [n-1] plus an order ideal D of Q (the set below the new top
    label n-1).  This is a bijection, and it is why the counts are
    1, 1, 2, 7, 40, 357, 4824, 96428 (A006455) rather than the labelled-poset counts.
    """
    if n == 0:
        yield (0, (), ())
        return
    for (m, up, down) in gen_natural_posets(n - 1):
        assert m == n - 1
        for D in ideals(m, up, down):
            nup = list(up) + [0]
            for x in range(m):
                if D >> x & 1:
                    nup[x] |= 1 << m
            ndown = list(down) + [D]
            for x in range(m):
                if D >> x & 1:
                    pass
            # ndown[m] = D is already the full down-set (D is an ideal, so closed down)
            yield (n, tuple(nup), tuple(ndown))


def ideals(n, up, down):
    """All order ideals (down-sets) as bitmasks, in increasing popcount order."""
    out = []
    for S in range(1 << n):
        ok = True
        for x in range(n):
            if S >> x & 1 and (down[x] & S) != down[x]:
                ok = False
                break
        if ok:
            out.append(S)
    out.sort(key=lambda s: (bin(s).count("1"), s))
    return out


# ------------------------------------------------------- linear extensions by ideals

def ideal_dp(n, up, down):
    """Return (ideal_list, nin, nout, e_of_P).

    nin[S]  = # chains  0 = S_0 < S_1 < ... < S_k = S  of ideals adding one element
    nout[S] = # chains  S = T_0 < ... < T_m = [n]      of ideals adding one element
    e_of_P  = nin[full] = nout[0]
    """
    ids = ideals(n, up, down)
    idx = {S: i for i, S in enumerate(ids)}
    full = (1 << n) - 1
    nin = {S: 0 for S in ids}
    nin[0] = 1
    for S in ids:                      # increasing popcount => predecessors done
        if nin[S] == 0 and S != 0:
            continue
        for x in range(n):
            if S >> x & 1:
                continue
            if (down[x] & S) != down[x]:
                continue
            nin[S | (1 << x)] = nin.get(S | (1 << x), 0) + nin[S]
    nout = {S: 0 for S in ids}
    nout[full] = 1
    for S in reversed(ids):
        if S == full:
            continue
        tot = 0
        for x in range(n):
            if S >> x & 1:
                continue
            if (down[x] & S) != down[x]:
                continue
            tot += nout[S | (1 << x)]
        nout[S] = tot
    return ids, nin, nout, nin[full]


def analyse(P):
    """The full exact readout for one poset.

    Returns a dict with EXACT Fractions:
      eP       number of linear extensions
      T[x][i]  Pr[ pos(x) = i ]           (0-indexed positions)
      q[(x,y)] Pr[ y before x ]  for x<y INCOMPARABLE  (= an inversion vs the labelling)
      inv      E[ inv_L ]  = sum of q over incomparable pairs
      footrule E[ sum_x |pos(x) - x| ]
      m[x]     per-element inversion mass = sum over incomparable y of Pr[y on the wrong
               side of x], i.e. sum_{y>x} q[(x,y)] + sum_{y<x} q[(y,x)]
      delta    max over incomparable pairs of min(p, 1-p), or None if a chain
      inc      list of incomparable pairs (x<y)
      primitive  True iff the incomparability graph is connected (and n>=2 with >=1 edge)
    """
    n, up, down = P
    ids, nin, nout, eP = ideal_dp(n, up, down)
    if eP == 0:
        raise AssertionError("no linear extensions")

    T = [[0] * n for _ in range(n)]        # integer counts, divided by eP at the end
    # pair counts: cnt_before[y][x] = # LEs with y before x
    before = [[0] * n for _ in range(n)]

    for S in ids:
        w_in = nin[S]
        if w_in == 0:
            continue
        pos = bin(S).count("1")
        for x in range(n):
            if S >> x & 1:
                continue
            if (down[x] & S) != down[x]:
                continue
            w = w_in * nout[S | (1 << x)]
            if w == 0:
                continue
            T[x][pos] += w
            # every y already in S is before x
            Sy = S
            while Sy:
                y = (Sy & -Sy).bit_length() - 1
                Sy &= Sy - 1
                before[y][x] += w

    inc = []
    for x in range(n):
        for y in range(x + 1, n):
            if not (up[x] >> y & 1) and not (up[y] >> x & 1):
                inc.append((x, y))

    q = {}
    for (x, y) in inc:
        q[(x, y)] = Fraction(before[y][x], eP)     # Pr[y before x] = inversion vs L

    inv = sum(q.values()) if q else Fraction(0)

    Tf = [[Fraction(T[x][i], eP) for i in range(n)] for x in range(n)]
    footrule = sum(Tf[x][i] * abs(i - x) for x in range(n) for i in range(n))

    m = [Fraction(0)] * n
    m = list(m)
    for (x, y) in inc:
        m[x] += q[(x, y)]
        m[y] += q[(x, y)]

    if inc:
        delta = max(min(q[(x, y)], 1 - q[(x, y)]) for (x, y) in inc)
    else:
        delta = None

    # primitivity: incomparability graph connected on all n vertices
    prim = _connected(n, inc) if n >= 2 else False

    return dict(n=n, eP=eP, T=Tf, Tint=T, q=q, inv=inv, footrule=footrule,
                m=m, delta=delta, inc=inc, primitive=prim, up=up, down=down)


def p_before(a, u, v):
    """Pr[ u before v ] for an incomparable pair, from the natural-labelling readout."""
    if u < v:
        return 1 - a["q"][(u, v)]     # q[(u,v)] = Pr[v before u]
    return a["q"][(v, u)]


def E_maj(a):
    """sum over incomparable pairs of min(p, 1-p).

    This is REFERENCE-FREE.  It equals E[inv_r] for the reference order r that orients
    every pair with its majority — and it is a LOWER BOUND on E[inv_r] for every other
    r, since min(p,1-p) <= p and <= 1-p pairwise.  It is what mg-c3ca's instrument
    prints, and it is NOT the same number as E[inv_L] for the natural labelling L.
    """
    return sum(min(v, 1 - v) for v in a["q"].values()) if a["q"] else Fraction(0)


def E_inv_wrt(a, order):
    """E[inv_r] for an arbitrary total order r given as a list of elements in order."""
    rank = {x: i for i, x in enumerate(order)}
    tot = Fraction(0)
    for (x, y) in a["inc"]:
        u, v = (x, y) if rank[x] < rank[y] else (y, x)
        tot += p_before(a, v, u)          # inversion = the r-later one comes first
    return tot


def majority_order(a):
    """The >1/2-majority tournament as a total order, or None if it has a 3-cycle.

    Under `frozen` this is always a linear order AND a linear extension of P
    (STATE.md:384's 3-cycle argument; not re-derived here, used as a definition).
    Off `frozen` it can cycle, and then `e` — hence `inv_e` — does not exist.
    """
    n = a["n"]
    up = a["up"]
    beats = [[False] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if x == y:
                continue
            if up[x] >> y & 1:
                beats[x][y] = True
            elif up[y] >> x & 1:
                beats[x][y] = False
            else:
                beats[x][y] = p_before(a, x, y) > Fraction(1, 2)
                if p_before(a, x, y) == Fraction(1, 2):
                    return None            # a tie: no strict majority order
    score = [sum(1 for y in range(n) if y != x and beats[x][y]) for x in range(n)]
    if sorted(score) != list(range(n)):
        return None                        # not a transitive tournament
    order = sorted(range(n), key=lambda x: -score[x])
    for i in range(n):
        for j in range(i + 1, n):
            if not beats[order[i]][order[j]]:
                return None
    return order


def is_linear_extension(P, order):
    n, up, down = P
    rank = {x: i for i, x in enumerate(order)}
    for x in range(n):
        for y in range(n):
            if up[x] >> y & 1 and rank[x] > rank[y]:
                return False
    return True


def _connected(n, inc):
    if n == 0:
        return False
    adj = [[] for _ in range(n)]
    for (x, y) in inc:
        adj[x].append(y)
        adj[y].append(x)
    seen = [False] * n
    stack = [0]
    seen[0] = True
    c = 1
    while stack:
        v = stack.pop()
        for w in adj[v]:
            if not seen[w]:
                seen[w] = True
                c += 1
                stack.append(w)
    return c == n


# ------------------------------------------------------------------- lambda_std

def jacobi_eigenvalues(A, sweeps=200, tol=1e-14):
    """Eigenvalues of a real symmetric matrix by cyclic Jacobi rotations.

    Written here rather than taken from a library because there is no numpy in this
    environment AND because an independent audit that shares its linear algebra with
    nothing is a stronger control.  Validated in selftest_c4f5.py against three matrices
    with hand-known spectra and against the characteristic polynomial at n <= 3.
    """
    n = len(A)
    a = [row[:] for row in A]
    for _ in range(sweeps):
        off = 0.0
        for p in range(n):
            for qq in range(p + 1, n):
                off += a[p][qq] * a[p][qq]
        if off <= tol * tol:
            break
        for p in range(n):
            for qq in range(p + 1, n):
                if abs(a[p][qq]) < 1e-300:
                    continue
                theta = (a[qq][qq] - a[p][p]) / (2.0 * a[p][qq])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][qq]
                    a[k][p] = c * akp - s * akq
                    a[k][qq] = s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[qq][k]
                    a[p][k] = c * apk - s * aqk
                    a[qq][k] = s * apk + c * aqk
    return sorted(a[i][i] for i in range(n))


def lambda_std_from_T(Tf):
    """lambda_std = max spec(S | 1-perp) where S = (T + T^T)/2.

    S is symmetric and doubly stochastic, so S1 = 1 and 1 is always an eigenvalue.
    spec(S) = {that 1} u spec(S|1perp); so lambda_std is spec(S) with ONE copy of the
    top eigenvalue removed.  (When the poset is an ordinal sum, 1 has multiplicity >= 2
    and lambda_std = 1 — which is exactly ledger row 1.)
    """
    n = len(Tf)
    S = [[float(Tf[x][i] + Tf[i][x]) / 2.0 for i in range(n)] for x in range(n)]
    ev = jacobi_eigenvalues(S)
    return ev[-2] if n >= 2 else 0.0, ev


def relabel(P, perm):
    """Relabel a poset by `perm` (perm[i] = new label of old element i).  Returns the
    poset in the new labelling.  Used to change the reference linear extension."""
    n, up, down = P
    nup = [0] * n
    ndown = [0] * n
    for x in range(n):
        for y in range(n):
            if up[x] >> y & 1:
                nup[perm[x]] |= 1 << perm[y]
                ndown[perm[y]] |= 1 << perm[x]
    return (n, tuple(nup), tuple(ndown))


def linear_extensions(P):
    """All linear extensions as tuples (element at position 0, 1, ...).  Only used for
    small controls and for the reference-order sweep; the DP is what does the work."""
    n, up, down = P
    out = []
    def rec(S, acc):
        if S == (1 << n) - 1:
            out.append(tuple(acc))
            return
        for x in range(n):
            if S >> x & 1:
                continue
            if (down[x] & S) != down[x]:
                continue
            acc.append(x)
            rec(S | (1 << x), acc)
            acc.pop()
    rec(0, [])
    return out


# ------------------------------------------------------------------ named families

def chain(n):
    return poset_from_pairs(n, [(i, j) for i in range(n) for j in range(i + 1, n)])


def antichain(n):
    return poset_from_pairs(n, [])


def chain_plus_antichain(p, q):
    """C_p (labels 0..p-1, a chain) DISJOINT UNION A_q (labels p..p+q-1, free).

    This is the object P8 asks for: q elements each incomparable to the whole p-chain
    AND to each other, i.e. q elements of mobility Theta(p) sharing ONE chain.
    """
    return poset_from_pairs(p + q, [(i, j) for i in range(p) for j in range(i + 1, p)])


def W(m):
    """W_m = C_m (labels 0..m-1) disjoint-union one free point (label m).
    STATE.md:102's separator."""
    return chain_plus_antichain(m, 1)


def V_poset():
    """the 3-element V: 0 < 1, 0 < 2.  delta = 1/3 exactly."""
    return poset_from_pairs(3, [(0, 1), (0, 2)])


def m_maj(a):
    """Per-element inversion mass in the MAJORITY orientation:
    m_x = sum over z incomparable to x of min(p_{xz}, 1-p_{xz}).

    This is mg-c3ca Sec.1's `m_x` (it is the one for which sum_x m_x = 2 E[inv_e]),
    and it is NOT `analyse()["m"]`, which is the natural-labelling mass.
    """
    n = a["n"]
    out = [Fraction(0)] * n
    for (x, y) in a["inc"]:
        v = a["q"][(x, y)]
        w = min(v, 1 - v)
        out[x] += w
        out[y] += w
    return out


def two_chains(p, q):
    """C_p (labels 0..p-1) disjoint-union C_q (labels p..p+q-1).  Every element of the
    shorter chain is incomparable to the whole of the longer one: Theta(n) elements of
    Theta(n) mobility with NO mutually-incomparable free pair to force delta = 1/2."""
    e = [(i, j) for i in range(p) for j in range(i + 1, p)]
    e += [(p + i, p + j) for i in range(q) for j in range(i + 1, q)]
    return poset_from_pairs(p + q, e)
