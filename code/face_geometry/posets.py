"""Enumeration of all posets on n elements up to isomorphism.

Every poset on n elements is isomorphic to one whose strict order relation is a
subset of {(i,j) : 0 <= i < j <= n-1} (relabel by any linear extension).  So we
range over transitively closed subsets of that set and deduplicate by the
canonical key in face_complex.Poset.

Sanity check (used as a control in selftest.py): the counts must be
  n = 1,2,3,4,5,6  ->  1, 2, 5, 16, 63, 318
(OEIS A000112, the number of partially ordered sets on n unlabelled points).
"""

from itertools import combinations

from face_complex import Poset

POSET_COUNTS = {0: 1, 1: 1, 2: 2, 3: 5, 4: 16, 5: 63, 6: 318}


def _is_transitively_closed(rel):
    for (a, b) in rel:
        for (c, d) in rel:
            if b == c and (a, d) not in rel:
                return False
    return True


def all_posets(n):
    """All posets on n elements up to isomorphism, as Poset objects."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    seen = {}
    for k in range(len(pairs) + 1):
        for sub in combinations(pairs, k):
            rel = set(sub)
            if not _is_transitively_closed(rel):
                continue
            P = Poset(n, rel)
            key = P.canonical_key()
            if key not in seen:
                seen[key] = P
    return [seen[k] for k in sorted(seen)]


def describe(P):
    """A short human-readable tag for a poset, for tables."""
    bits = []
    if P.is_antichain():
        bits.append("antichain")
    if P.is_chain():
        bits.append("chain")
    if not P.is_connected():
        bits.append("disconnected")
    naut = len(P.automorphisms())
    if naut > 1:
        bits.append("|Aut|=%d" % naut)
    return ",".join(bits) if bits else "-"


def cover_string(P):
    """Cover relations, as a stable printable identifier of the poset."""
    covers = []
    for (a, b) in sorted(P.less):
        if not any((a, c) in P.less and (c, b) in P.less for c in range(P.n)):
            covers.append("%d<%d" % (a, b))
    return " ".join(covers) if covers else "(antichain)"
