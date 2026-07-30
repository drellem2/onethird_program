"""Per-poset records for n = 3..8, and the population section 4 is stated over.

The population of the target's section 4: the TIE-FREE NON-CHAIN posets, on which
the majority relation is a linear order L* and both quotient statistics are
canonical.  Tie-freeness alone is not enough for L* to exist -- the majority
relation also has to be acyclic -- so that is checked rather than assumed, and
the count of posets excluded for each reason is reported.
"""

import sys
from fractions import Fraction

from poset import (all_posets, pair_probs, delta_of, tie_free, lstar,
                   e_all_subsets, majority_edges, find_cycle)
from levels import m_table, qmass, qfrac, interval_partitions_are_levels


class Rec:
    __slots__ = ("n", "cover", "e", "delta", "tie_free", "cyclic", "order",
                 "qmass", "qfrac")


_CACHE = {}
_MCACHE = {}


def build(n, want_qfrac=True, verbose=True):
    """Records for every non-chain poset on n elements, up to isomorphism."""
    key = (n, want_qfrac)
    if key in _CACHE:
        return _CACHE[key]
    if (n, True) in _CACHE:
        return _CACHE[(n, True)]
    # warm the isomorphism cache for M from the bottom up: M depends only on the
    # isomorphism class of the induced subposet, so smaller n pays for larger n
    for k in range(1, min(n, 7) + 1):
        if k not in _MCACHE:
            for P in all_posets(k):
                m_table(P, _MCACHE.setdefault("c", {}))
            _MCACHE[k] = True
    cache = _MCACHE.setdefault("c", {})
    out = []
    posets = all_posets(n)
    for idx, P in enumerate(posets):
        if verbose and idx % 2000 == 0:
            print("    [records n=%d: %d/%d]" % (n, idx, len(posets)),
                  file=sys.stderr, flush=True)
        probs = pair_probs(P)
        if not probs:
            continue                                  # chain
        r = Rec()
        r.n = n
        r.cover = P.cover_string()
        e = e_all_subsets(P)
        r.e = e[(1 << n) - 1]
        r.delta = delta_of(probs)
        r.tie_free = tie_free(probs)
        r.cyclic = find_cycle(n, majority_edges(P, probs)) is not None
        r.order = None
        r.qmass = None
        r.qfrac = None
        if r.tie_free and not r.cyclic:
            r.order = lstar(P, probs)
            assert interval_partitions_are_levels(P, r.order), \
                "interval partitions of L* must all be levels"
            Mm, _ = m_table(P, cache, e)
            r.qmass = qmass(P, r.order, Mm, r.e)
            if want_qfrac:
                r.qfrac = qfrac(P, r.order)
        out.append(r)
    _CACHE[key] = out
    return out


def population(recs):
    """The tie-free, acyclic-majority non-chains: where section 4 is defined."""
    return [r for r in recs if r.qmass is not None]


def extremal(pop):
    dmin = min(r.delta for r in pop)
    return dmin, [r for r in pop if r.delta == dmin]
