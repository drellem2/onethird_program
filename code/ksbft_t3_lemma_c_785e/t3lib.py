"""t3lib.py (mg-785e): helpers for the Lemma C probes.

Generation, laws: read-only from ../ksbft_t_interval_orders_afa4/iolib.py (OEIS-certified, audited mg-5ecf).
Covers / typed separators / automaton DP: read-only from ../ksbft_t2_two_separator_561a/t2lib.py (audited mg-6c30).
New here: order_law(dn, X) = exact law of the relative order of the elements of X (dict tuple -> count).
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ksbft_t2_two_separator_561a'))
from t2lib import *            # noqa: F401,F403  (gen_fast, downmasks, laws, lt, inc, bal, covers, seps_typed, auto_count)
from fractions import Fraction as F


def order_law(dn, X):
    """exact counts of the relative order of the tuple X over all linear extensions."""
    X = tuple(X)
    def step(s, v):
        return s + (v,) if v in X else s
    return auto_count(dn, (), step)


def cont_pairs(iv, C=None):
    """strict containment pairs (a, a2) with a inside a2 (a first), S(a,a2) = A(a,a2) of size 2.
    yields (a, a2, s, t, Z) with Z = {z : r(a) < l(z) <= r(a2)}."""
    n = len(iv); C = C or covers(iv)
    for a in range(n):
        for a2 in range(n):
            (la, ra), (lb, rb) = iv[a], iv[a2]
            if not (lb < la and ra < rb): continue
            A, B = seps_typed(iv, C, a, a2)
            assert not B
            if len(A) != 2: continue
            Z = [z for z in range(n) if ra < iv[z][0] <= rb]
            yield a, a2, A[0], A[1], Z
