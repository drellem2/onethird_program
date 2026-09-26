"""t2lib.py (mg-561a): shared helpers for the two-separator probes.

Generation and exact pair laws are imported read-only from code/ksbft_t_interval_orders_afa4/iolib.py
(OEIS-certified generator; laws audited by mg-5ecf).  New here:
- seps_typed(): separators of an ordered incomparable pair (a,a'), split into above (a covered by z, z||a')
  and below (z covered by a', z||a) -- computed from the cover relation, not from the interval formula;
- auto_count(): exact number of linear extensions accepted by a small automaton run along the extension
  (DP over (ideal, state)); used for joint events such as Lambda_1, Lambda_2.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ksbft_t_interval_orders_afa4'))
from iolib import gen_fast, downmasks, laws, lt, inc, prob, bal, delta, A022493   # noqa: F401
from fractions import Fraction as F
from functools import lru_cache


def covers(iv):
    n = len(iv)
    return {(a, b) for a in range(n) for b in range(n) if lt(iv, a, b)
            and not any(lt(iv, a, c) and lt(iv, c, b) for c in range(n))}


def seps_typed(iv, C, a, a2):
    n = len(iv)
    A = [z for z in range(n) if (a, z) in C and inc(iv, z, a2)]
    B = [z for z in range(n) if (z, a2) in C and inc(iv, z, a)]
    return A, B


def auto_count(dn, start, step):
    """number of linear extensions (as sequences) accepted: state evolves by step(state, v); returns dict
    final_state -> count."""
    n = len(dn); full = (1 << n) - 1
    cur = {(0, start): 1}
    for _ in range(n):
        nxt = {}
        for (I, s), c in cur.items():
            for v in range(n):
                if not I >> v & 1 and dn[v] & ~I == 0:
                    t = step(s, v)
                    k = (I | 1 << v, t); nxt[k] = nxt.get(k, 0) + c
        cur = nxt
    out = {}
    for (I, s), c in cur.items():
        out[s] = out.get(s, 0) + c
    return out


def lambdas(dn, a, a2, S):
    """(|Lambda_1|, |Lambda_2|, |Lambda_3|) for the ordered pair (a,a') and separator set S."""
    S = frozenset(S)
    def step(s, v):
        # s: 0 = a not yet; 1 = a placed, no S since; 2 = a placed, some S since; 'L1','L2','L3' terminal
        if s in ('L1', 'L2', 'L3'): return s
        if v == a: return 1
        if v == a2: return 'L3' if s == 0 else ('L1' if s == 1 else 'L2')
        if v in S and s == 1: return 2
        return s
    out = auto_count(dn, 0, step)
    return out.get('L1', 0), out.get('L2', 0), out.get('L3', 0)
