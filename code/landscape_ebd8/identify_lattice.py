#!/usr/bin/env python3
"""
IDENTIFICATION CHECK, not new mathematics.

The programme's support lattice AC(P) -- partitions of a finite poset P whose
quotient has no directed cycle among distinct blocks -- is claimed in the
accompanying landscape document to be an already-named object: the lattice
O(P) of ORDER-PRESERVING PARTITIONS (= order congruences) of P, studied by
Sturm (1971-77), Czedli-Lenkehegyi (1983), Koertesi-Radeleczki-Szilagyi (2005)
and Jenca-Sarkoci (JCTA 2014).

This script tests that identification against published statements about O(P)
that were derived with no reference to this programme.  Every predicted number
below is READ OFF A PAPER; nothing here is fitted.

  JS = Jenca & Sarkoci, "Linear extensions and order-preserving poset
       partitions", J. Combin. Theory Ser. A 122 (2014) 28-38, arXiv:1112.5782.

Predictions tested
------------------
  P1  (JS Def. 3.1, after Koertesi-Radeleczki-Szilagyi)
        AC(P) computed by the programme's own acyclic-quotient test coincides
        setwise with O(P) computed by JS's rho-cycle definition.
  P2  (JS Thm. 3.8 + abstract)  THE SHARP ONE.
        mu_{AC(P)}(0hat, 1hat) = (-1)^(n-1) * s, where s = e(P) (number of
        linear extensions) when P is connected, and s = eC(P) (number of
        cyclic classes of linear extensions) in general.
  P3  (JS Ex. 3.5)   P an antichain  =>  AC(P) = Pi_n.
  P4  (JS Ex. 3.6)   P an n-chain    =>  |AC(P)| = 2^(n-1), blocks convex,
                     and AC(P) is a Boolean lattice.
  P5  (JS Sec. 3)    AC(P) is ranked by n - |pi|: every covering pair merges
                     exactly two blocks.
  P6  (JS Sec. 3)    the atoms are exactly the pi_{a,b} with a covered-by b or
                     a incomparable to b.
  P7  (JS Sec. 3)    meet = common refinement (blockwise intersection), i.e.
                     AC(P) is closed under the Pi_n-meet.
  P8  (JS Ex. 3.7)   O(B_2) for B_2 the 4-element Boolean lattice has 11
                     elements and 2 spheres.

Self-contained: shares no code with code/hodge_leverage, code/face_geometry,
code/unified_gate_8fd1 or code/semigroup_note.  Pure Python 3, exact integer
arithmetic throughout.
"""

import itertools
import sys
from functools import lru_cache


# ---------------------------------------------------------------- posets ----

def transitive_closure(n, rel):
    """rel: set of (i,j) meaning i < j.  Return its transitive closure."""
    r = set(rel)
    changed = True
    while changed:
        changed = False
        for (a, b) in list(r):
            for (c, d) in list(r):
                if b == c and (a, d) not in r:
                    r.add((a, d))
                    changed = True
    return r


def enumerate_posets(n):
    """All labelled posets on [n] admitting 0<1<...<n-1 as a linear extension,
    i.e. every strict relation goes from a smaller to a larger label.  Every
    isomorphism class is hit at least once.  Returns list of frozensets."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    out = set()
    for mask in range(1 << len(pairs)):
        rel = {pairs[k] for k in range(len(pairs)) if mask >> k & 1}
        if transitive_closure(n, rel) == rel:
            out.add(frozenset(rel))
    return sorted(out, key=lambda s: (len(s), sorted(s)))


def canonical(n, rel):
    """Canonical form of a labelled poset under S_n relabelling."""
    best = None
    for p in itertools.permutations(range(n)):
        img = frozenset((p[a], p[b]) for (a, b) in rel)
        key = tuple(sorted(img))
        if best is None or key < best:
            best = key
    return best


def iso_classes(n):
    seen = {}
    for rel in enumerate_posets(n):
        c = canonical(n, rel)
        if c not in seen:
            seen[c] = rel
    return list(seen.values())


def is_connected(n, rel):
    """Connectivity of the comparability graph."""
    if n == 0:
        return True
    adj = {i: set() for i in range(n)}
    for (a, b) in rel:
        adj[a].add(b)
        adj[b].add(a)
    seen = {0}
    stack = [0]
    while stack:
        v = stack.pop()
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == n


def linear_extensions(n, rel):
    """All linear extensions as tuples (words) over [n]."""
    below = {j: {i for (i, jj) in rel if jj == j} for j in range(n)}
    out = []

    def rec(prefix, remaining):
        if not remaining:
            out.append(tuple(prefix))
            return
        for x in sorted(remaining):
            if below[x] <= set(prefix):
                rec(prefix + [x], remaining - {x})

    rec([], set(range(n)))
    return out


# ------------------------------------------------------------ partitions ----

def set_partitions(n):
    """All partitions of [n] as tuples of frozensets, canonically ordered."""
    if n == 0:
        yield ()
        return
    parts = [[[0]]]
    for x in range(1, n):
        new = []
        for p in parts:
            for i in range(len(p)):
                q = [list(b) for b in p]
                q[i].append(x)
                new.append(q)
            new.append([list(b) for b in p] + [[x]])
        parts = new
    for p in parts:
        yield tuple(sorted((frozenset(b) for b in p), key=lambda b: min(b)))


def block_of(pi):
    m = {}
    for idx, b in enumerate(pi):
        for x in b:
            m[x] = idx
    return m


# ------- route A: the programme's definition (acyclic quotient) -------------

def acyclic_quotient(n, rel, pi):
    """True iff the quotient P/pi has no directed cycle among DISTINCT blocks.
    This is the programme's definition of a commitment level / support."""
    bo = block_of(pi)
    k = len(pi)
    adj = [set() for _ in range(k)]
    for (a, b) in rel:
        if bo[a] != bo[b]:
            adj[bo[a]].add(bo[b])
    # cycle detection by DFS three-colouring
    colour = [0] * k

    def dfs(v):
        colour[v] = 1
        for w in adj[v]:
            if colour[w] == 1:
                return False
            if colour[w] == 0 and not dfs(w):
                return False
        colour[v] = 2
        return True

    for v in range(k):
        if colour[v] == 0 and not dfs(v):
            return False
    return True


# ------- route B: Jenca-Sarkoci Definition 3.1 (rho-cycles) ----------------

def js_order_preserving(n, rel, pi):
    """True iff pi is an order-preserving partition in the sense of
    Jenca-Sarkoci Def. 3.1(ii)-(iii): for every rho-cycle x_0,...,x_m (each
    step either rho-equivalent or strictly less), all x_i lie in ONE block.

    Implemented literally: build the digraph on ELEMENTS with edges x->y when
    (x,y) in rho (same block) or x < y, and demand that every directed cycle
    stays inside a single block.  Equivalently: in the condensation, no strong
    component may meet two blocks."""
    bo = block_of(pi)
    adj = [set() for _ in range(n)]
    for b in pi:
        for x in b:
            for y in b:
                if x != y:
                    adj[x].add(y)
    for (a, b) in rel:
        adj[a].add(b)

    # Tarjan strongly connected components
    index = [None] * n
    low = [0] * n
    onstack = [False] * n
    stack = []
    counter = [0]
    comps = []

    def strong(v):
        # iterative to avoid recursion limits
        work = [(v, iter(sorted(adj[v])))]
        index[v] = low[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        onstack[v] = True
        while work:
            u, it = work[-1]
            advanced = False
            for w in it:
                if index[w] is None:
                    index[w] = low[w] = counter[0]
                    counter[0] += 1
                    stack.append(w)
                    onstack[w] = True
                    work.append((w, iter(sorted(adj[w]))))
                    advanced = True
                    break
                elif onstack[w]:
                    low[u] = min(low[u], index[w])
            if advanced:
                continue
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[u])
            if low[u] == index[u]:
                comp = []
                while True:
                    w = stack.pop()
                    onstack[w] = False
                    comp.append(w)
                    if w == u:
                        break
                comps.append(comp)

    for v in range(n):
        if index[v] is None:
            strong(v)

    for comp in comps:
        if len({bo[x] for x in comp}) > 1:
            return False
    return True


# ------------------------------------------------------- lattice machinery --

def refines(pi, sigma):
    """pi <= sigma in the refinement order: every block of pi inside a block
    of sigma."""
    return all(any(b <= c for c in sigma) for b in pi)


def mobius_bottom_top(elts, leq):
    """mu(0hat, 1hat) for a poset given as a list with a <= test.  Assumes a
    unique minimum and maximum, both present."""
    # order elements so that leq-smaller come first
    order = sorted(range(len(elts)), key=lambda i: sum(1 for j in range(len(elts)) if leq(elts[j], elts[i])))
    pos = {i: k for k, i in enumerate(order)}
    bot = min(range(len(elts)), key=lambda i: sum(1 for j in range(len(elts)) if leq(elts[j], elts[i])))
    top = max(range(len(elts)), key=lambda i: sum(1 for j in range(len(elts)) if leq(elts[j], elts[i])))
    mu = {}
    for i in order:
        if i == bot:
            mu[i] = 1
        else:
            s = 0
            for j in order:
                if j != i and leq(elts[j], elts[i]):
                    s += mu[j]
            mu[i] = -s
    return mu[top], bot, top


def cyclic_classes(n, les):
    """Jenca-Sarkoci Def. 4.1: f ~ g iff f = w w' and g = w' w as words.
    Count equivalence classes among the linear extensions."""
    les = [tuple(f) for f in les]
    idx = {f: i for i, f in enumerate(les)}
    parent = list(range(len(les)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for f in les:
        for k in range(1, n):
            g = f[k:] + f[:k]
            if g in idx:
                union(idx[f], idx[g])
    return len({find(i) for i in range(len(les))})


# ------------------------------------------------------------------ main ----

def analyse(n, verbose=False):
    parts = list(set_partitions(n))
    results = {
        'classes': 0,
        'P1_mismatch': 0, 'P1_checked': 0,
        'P2_mismatch': 0, 'P2_checked': 0,
        'P5_mismatch': 0, 'P5_checked': 0,
        'P6_mismatch': 0, 'P6_checked': 0,
        'P7_mismatch': 0, 'P7_checked': 0,
        'connected': 0,
    }
    for rel in iso_classes(n):
        results['classes'] += 1
        conn = is_connected(n, rel)
        if conn:
            results['connected'] += 1

        # ---- P1: the two definitions agree, setwise
        A = [pi for pi in parts if acyclic_quotient(n, rel, pi)]
        B = [pi for pi in parts if js_order_preserving(n, rel, pi)]
        results['P1_checked'] += 1
        if set(A) != set(B):
            results['P1_mismatch'] += 1
            print("  P1 FAIL", sorted(rel), file=sys.stderr)

        les = linear_extensions(n, rel)
        e = len(les)
        eC = cyclic_classes(n, les)

        # ---- P2: Mobius vs sphere count  (needs n >= 3 for JS Thm 3.8)
        if n >= 3:
            mu, bot, top = mobius_bottom_top(A, refines)
            predicted_s = e if conn else eC
            predicted_mu = ((-1) ** (n - 1)) * predicted_s
            results['P2_checked'] += 1
            if mu != predicted_mu:
                results['P2_mismatch'] += 1
                print("  P2 FAIL n=%d rel=%s mu=%d predicted=%d e=%d eC=%d conn=%s"
                      % (n, sorted(rel), mu, predicted_mu, e, eC, conn), file=sys.stderr)

        # ---- covers of the lattice AC(P), by bitmask transitive reduction
        Aset = set(A)
        m = len(A)
        aidx = {pi: i for i, pi in enumerate(A)}
        above = [0] * m           # strictly above, as a bitmask over A
        for i, x in enumerate(A):
            for j, y in enumerate(A):
                if i != j and refines(x, y):
                    above[i] |= 1 << j
        cov = [0] * m
        for i in range(m):
            reach2 = 0
            b = above[i]
            while b:
                j = (b & -b).bit_length() - 1
                b &= b - 1
                reach2 |= above[j]
            cov[i] = above[i] & ~reach2

        # ---- P5: every cover merges exactly two blocks (rank = n - |pi|)
        results['P5_checked'] += 1
        bad5 = False
        for i, x in enumerate(A):
            b = cov[i]
            while b:
                j = (b & -b).bit_length() - 1
                b &= b - 1
                if len(x) - len(A[j]) != 1:
                    bad5 = True
        if bad5:
            results['P5_mismatch'] += 1

        # ---- P6: atoms are exactly pi_{a,b} with a<.b (cover) or a || b
        bottom = tuple(sorted((frozenset([i]) for i in range(n)), key=lambda b: min(b)))
        bi = aidx[bottom]
        true_atoms = set()
        b = cov[bi]
        while b:
            j = (b & -b).bit_length() - 1
            b &= b - 1
            true_atoms.add(A[j])
        # predicted
        covers = set()
        for (a, b) in rel:
            if not any((a, c) in rel and (c, b) in rel for c in range(n)):
                covers.add((a, b))
        incomp = {(a, b) for a in range(n) for b in range(n)
                  if a < b and (a, b) not in rel and (b, a) not in rel}
        pred_atoms = set()
        for (a, b) in list(covers) + list(incomp):
            blocks = [frozenset([a, b])] + [frozenset([x]) for x in range(n) if x not in (a, b)]
            pred_atoms.add(tuple(sorted(blocks, key=lambda s: min(s))))
        results['P6_checked'] += 1
        if true_atoms != pred_atoms:
            results['P6_mismatch'] += 1
            print("  P6 FAIL", sorted(rel), file=sys.stderr)

        # ---- P7: closed under blockwise intersection (the Pi_n meet)
        results['P7_checked'] += 1
        bad7 = False
        for x in A:
            for y in A:
                inter = set()
                for bx in x:
                    for by in y:
                        c = bx & by
                        if c:
                            inter.add(frozenset(c))
                m = tuple(sorted(inter, key=lambda s: min(s)))
                if m not in Aset:
                    bad7 = True
        if bad7:
            results['P7_mismatch'] += 1

    return results


def special_cases(nmax):
    print()
    print("P3 / P4 -- the two named degenerate ends (JS Ex. 3.5, Ex. 3.6)")
    print("  %-4s %-10s %-24s %-24s" % ("n", "|Pi_n|", "antichain |AC|", "chain |AC| (pred 2^(n-1))"))
    for n in range(2, nmax + 1):
        parts = list(set_partitions(n))
        anti = frozenset()
        chain = transitive_closure(n, {(i, j) for i in range(n) for j in range(i + 1, n)})
        a_ac = [pi for pi in parts if acyclic_quotient(n, anti, pi)]
        c_ac = [pi for pi in parts if acyclic_quotient(n, chain, pi)]
        # chain: are all blocks convex intervals?
        conv = all(all(max(b) - min(b) + 1 == len(b) for b in pi) for pi in c_ac)
        ok3 = (len(a_ac) == len(parts))
        ok4 = (len(c_ac) == 2 ** (n - 1)) and conv
        print("  %-4d %-10d %-24s %-24s" % (
            n, len(parts),
            "%d  %s" % (len(a_ac), "= Pi_n OK" if ok3 else "MISMATCH"),
            "%d  %s" % (len(c_ac), "OK, all convex" if ok4 else "MISMATCH")))


def boolean_b2():
    """JS Example 3.7: P = B_2, the 4-element Boolean lattice 0 < a,b < 1.
    Predicted |O(P)| = 11 and 2 spheres of dimension 1."""
    n = 4
    # 0 = bottom, 1 = a, 2 = b, 3 = top
    rel = transitive_closure(n, {(0, 1), (0, 2), (1, 3), (2, 3)})
    parts = list(set_partitions(n))
    A = [pi for pi in parts if acyclic_quotient(n, rel, pi)]
    B = [pi for pi in parts if js_order_preserving(n, rel, pi)]
    mu, _, _ = mobius_bottom_top(A, refines)
    les = linear_extensions(n, rel)
    print()
    print("P8 -- JS Example 3.7, P = B_2 (4-element Boolean lattice)")
    print("  |AC(P)| by acyclic-quotient   = %d   (JS says 11)  %s" % (len(A), "OK" if len(A) == 11 else "MISMATCH"))
    print("  |O(P)|  by JS rho-cycle def   = %d                 %s" % (len(B), "OK" if set(A) == set(B) else "MISMATCH"))
    print("  mu(0,1)                       = %d" % mu)
    print("  spheres = |mu|                = %d   (JS says 2, dim n-3 = 1)  %s"
          % (abs(mu), "OK" if abs(mu) == 2 else "MISMATCH"))
    print("  e(P) = %d, connected = %s" % (len(les), is_connected(n, rel)))


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    print("=" * 78)
    print("IDENTIFICATION CHECK: is AC(P) the order-congruence lattice O(P)?")
    print("Predictions read off Jenca & Sarkoci, JCTA 122 (2014) 28-38")
    print("(arXiv:1112.5782), and Koertesi-Radeleczki-Szilagyi, Math. Pannon.")
    print("16 (2005) 39-55.  Nothing below is fitted.")
    print("=" * 78)
    print()
    print("%-4s %-9s %-11s %-34s %-9s %-9s %-9s" %
          ("n", "classes", "connected", "P2  mu = (-1)^(n-1) * spheres",
           "P1 defs", "P5 rank", "P6 atoms"))
    grand = {}
    for n in range(2, nmax + 1):
        r = analyse(n)
        grand[n] = r
        p2 = ("%d bad of %d" % (r['P2_mismatch'], r['P2_checked'])) if r['P2_checked'] else "n/a (n<3)"
        print("%-4d %-9d %-11d %-34s %-9s %-9s %-9s" % (
            n, r['classes'], r['connected'], p2,
            "%d bad of %d" % (r['P1_mismatch'], r['P1_checked']),
            "%d bad of %d" % (r['P5_mismatch'], r['P5_checked']),
            "%d bad of %d" % (r['P6_mismatch'], r['P6_checked'])))
    print()
    print("P7 (meet = common refinement, i.e. closed under the Pi_n-meet):")
    for n in range(2, nmax + 1):
        print("  n=%d: %d bad of %d" % (n, grand[n]['P7_mismatch'], grand[n]['P7_checked']))

    special_cases(min(nmax, 7))
    boolean_b2()

    total_bad = sum(grand[n]['P1_mismatch'] + grand[n]['P2_mismatch'] +
                    grand[n]['P5_mismatch'] + grand[n]['P6_mismatch'] +
                    grand[n]['P7_mismatch'] for n in grand)
    print()
    print("=" * 78)
    print("TOTAL DISAGREEMENTS WITH THE PUBLISHED DESCRIPTION OF O(P): %d" % total_bad)
    print("=" * 78)


if __name__ == '__main__':
    main()
