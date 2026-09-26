"""probe.py (mg-5f14) -- instrument for docs/KSBFT-Q-local-width2.md.

Reads isomorphism-class files written by `pcert onept gen` (line: n dn[0] .. dn[n-1], n decimal, dn = strict
down-set bitmask in HEX) and, for every poset whose incomparability graph is connected (indecomposable,
n >= 2), computes EXACTLY (Python ints / Fractions):

  e(P); B[x][y] = #extensions with x before y; for every minimal x the position law
  q_x(j) = #extensions with exactly j elements before x.

and tests the statements of the deliverable:

  LL   (Local Linial, Thm 2.1 of the doc, PROVEN) -- conclusion is checked as a positive control:
       if x is minimal, P(x first) <= 2/3, Inc(x) has chain bottom c_1<..<c_k and
       P(f(x) <= k) >= 1/3, then some (x, c_j), j <= k, is balanced.  A violation = a bug.
  MONO (Lemma 1.1, PROVEN): q_x non-increasing for minimal x.  A violation = a bug.
  classification of each P by which end-lemma fires:
       LLq_bot : exists minimal x satisfying LL's (quantitative) hypothesis
       LLs_bot : the STRUCTURAL corollary (Cor 2.3): P has exactly two minimal elements and
                 each has chain-bottom length k with 3k >= |Inc|+1
       same on the dual (top).
  for the posets where neither end fires: number of minimal/maximal elements, and whether a
  balanced pair exists among the minimal elements (candidate "3-antichain lemma") or among
  the minimal elements together with their incomparables.
Usage: python3 probe.py FILE [FILE ...]      (prints AGG lines and up to 5 witnesses per bucket)
Env MONOCTRL=1 applies the MONO test to non-minimal elements too: MONO_VIOLATION MUST then fire.
Env NEGCTRL=1 narrows 'balanced' to [0.34, 0.66] inside the LL check: the check MUST then fire
(LL is sharp at 1/3 on 2+1), proving the checker can fail.
"""
import os
import sys
from fractions import Fraction
from functools import lru_cache

LO = Fraction(34, 100) if os.environ.get("NEGCTRL") == "1" else Fraction(1, 3)


def balanced(p):
    return LO <= p <= 1 - LO


def analyse(dn):
    n = len(dn)
    up = [sum(1 << j for j in range(n) if dn[j] >> i & 1) for i in range(n)]
    full = (1 << n) - 1

    @lru_cache(maxsize=None)
    def N(I):  # extensions of ideal I
        if I == 0:
            return 1
        t = 0
        for x in range(n):
            if I >> x & 1 and not (up[x] & I):
                t += N(I & ~(1 << x))
        return t

    @lru_cache(maxsize=None)
    def Nc(F):  # extensions of filter F
        if F == 0:
            return 1
        t = 0
        for x in range(n):
            if F >> x & 1 and not (dn[x] & F):
                t += Nc(F & ~(1 << x))
        return t

    e = N(full)
    B = [[0] * n for _ in range(n)]
    pos = [[0] * n for _ in range(n)]  # pos[x][j] = #ext with j elements before x
    seen = {full}
    stack = [full]
    while stack:
        J = stack.pop()
        k = bin(J).count("1")
        for x in range(n):
            if J >> x & 1 and not (up[x] & J):
                I = J & ~(1 << x)
                c = N(I) * Nc(full & ~J)
                pos[x][k - 1] += c
                for w in range(n):
                    if I >> w & 1:
                        B[w][x] += c
                if I not in seen:
                    seen.add(I)
                    stack.append(I)
    return e, B, pos, up


def inc(dn, up, x, y):
    return x != y and not (dn[x] >> y & 1) and not (up[x] >> y & 1)


def chain_bottom(dn, S):
    """S = set (list) of elements forming an ideal. Return c_1..c_k: the longest chain bottom."""
    rest = set(S)
    out = []
    while rest:
        mins = [v for v in rest if not any(dn[v] >> u & 1 for u in rest)]
        if len(mins) != 1:
            break
        out.append(mins[0])
        rest.discard(mins[0])
    return out


def end_lemmas(n, dn, up, e, B, pos):
    """bottom end: returns (LLq, LLs, ll_violation, mono_violation, info)"""
    mins = [x for x in range(n) if dn[x] == 0]
    LLq = False
    viol = False
    mono = False
    structs = []
    if os.environ.get("MONOCTRL") == "1":  # firing control: the law of a NON-minimal element rises
        for x in range(n):
            if dn[x] and any(pos[x][j + 1] > pos[x][j] for j in range(n - 1)):
                mono = True
    for x in mins:
        q = pos[x]
        if any(q[j + 1] > q[j] for j in range(n - 1)):
            mono = True
        I = [y for y in range(n) if inc(dn, up, x, y)]
        cb = chain_bottom(dn, I)
        k, m = len(cb), len(I)
        structs.append(3 * k >= m + 1)
        first = Fraction(q[0], e)
        Sk = Fraction(sum(q[:k]), e)
        if first <= Fraction(2, 3) and k >= 1 and Sk >= Fraction(1, 3):
            LLq = True
            if not any(balanced(Fraction(B[x][c], e)) for c in cb):
                viol = True
    LLs = len(mins) == 2 and all(structs)
    return LLq, LLs, viol, mono, len(mins)


def window_tests(n, dn, up, e, B, pos):
    """Candidate bottom-end statements beyond LL (EMPIRICAL probes only).
    BR : x = a minimal element minimising P(x first); C = chain bottom of Inc(x); U = minimal
         elements of Inc(x) minus C.  Some pair inside {x} u C u U is balanced.
    WIN: for some minimal x, some pair inside {x} u Inc(x) is balanced (window of size <= D+1)."""
    mins = [x for x in range(n) if dn[x] == 0]
    bal = lambda a, b: inc(dn, up, a, b) and balanced(Fraction(B[a][b], e))
    x = min(mins, key=lambda v: pos[v][0])
    I = [y for y in range(n) if inc(dn, up, x, y)]
    C = chain_bottom(dn, I)
    rest = [y for y in I if y not in C]
    U = [v for v in rest if not any(dn[v] >> w & 1 for w in rest)]
    T = [x] + C + U
    br = any(bal(a, b) for a in T for b in T if a < b)
    win = False
    for x in mins:
        W = [x] + [y for y in range(n) if inc(dn, up, x, y)]
        if any(bal(a, b) for a in W for b in W if a < b):
            win = True
            break
    return br, win


def dual(dn):
    n = len(dn)
    return [sum(1 << j for j in range(n) if dn[j] >> i & 1) for i in range(n)]


def connected(n, dn, up):
    seen = 1
    stack = [0]
    while stack:
        v = stack.pop()
        for w in range(n):
            if not seen >> w & 1 and inc(dn, up, v, w):
                seen |= 1 << w
                stack.append(w)
    return seen == (1 << n) - 1


def main(files):
    for f in files:
        agg = {}
        wit = {}
        for line in open(f):
            a = line.split()
            n, dn = int(a[0]), [int(t, 16) for t in a[1:]]
            if n < 2:
                continue
            up = dual(dn)
            if not connected(n, dn, up):
                continue
            e, B, pos, _ = analyse(dn)
            # dual poset: up-sets become down-sets; B transposes; positions reverse
            Bd = [[B[y][x] for y in range(n)] for x in range(n)]
            posd = [[pos[x][n - 1 - j] for j in range(n)] for x in range(n)]
            b = end_lemmas(n, dn, up, e, B, pos)
            t = end_lemmas(n, up, dn, e, Bd, posd)
            rng = max(sum(inc(dn, up, x, y) for y in range(n)) for x in range(n))
            anybal = any(balanced(Fraction(B[x][y], e)) for x in range(n) for y in range(n) if inc(dn, up, x, y))
            mins = [x for x in range(n) if dn[x] == 0]
            maxs = [x for x in range(n) if up[x] == 0]
            balmin = any(balanced(Fraction(B[x][y], e)) for x in mins for y in mins if x != y)
            balmax = any(balanced(Fraction(B[x][y], e)) for x in maxs for y in maxs if x != y)
            # balanced pair with at least one element minimal (resp. maximal)
            balminX = any(balanced(Fraction(B[x][y], e)) for x in mins for y in range(n) if inc(dn, up, x, y))
            balmaxX = any(balanced(Fraction(B[x][y], e)) for x in maxs for y in range(n) if inc(dn, up, x, y))
            brb, winb = window_tests(n, dn, up, e, B, pos)
            brt, wint = window_tests(n, up, dn, e, Bd, posd)
            keys = [("ALL",)]
            keys.append(("BR_either_end", brb or brt))
            keys.append(("WIN_either_end", winb or wint))
            keys.append(("LL_or_BR_either_end", b[0] or t[0] or brb or brt))
            keys.append(("LLq_bottom", b[0]))
            keys.append(("BR_bottom", brb))
            iso = any(dn[x] == 0 and up[x] == 0 for x in range(n))
            if not (brb or brt):
                keys.append(("BR_fail_has_isolated", iso))
            if not brb:
                keys.append(("BR_bottom_fail_has_isolated", iso))
            if not (winb or wint):
                keys.append(("WIN_fail_has_isolated", iso))
            keys.append(("LLq_any", b[0] or t[0]))
            keys.append(("LLs_any", b[1] or t[1]))
            if b[2] or t[2]:
                keys.append(("LL_VIOLATION",))
            if b[3] or t[3]:
                keys.append(("MONO_VIOLATION",))
            if not anybal:
                keys.append(("NO_BALANCED_PAIR",))
            if not (b[0] or t[0]):
                keys.append(("noLL", "nmin>=3" if b[4] >= 3 else "nmin=2", "nmax>=3" if t[4] >= 3 else "nmax=2"))
                keys.append(("noLL_balmin_or_balmax", balmin or balmax))
                keys.append(("noLL_bal_touching_min_or_max", balminX or balmaxX))
                if b[4] >= 3:
                    keys.append(("nmin>=3_noLL_balmin", balmin))
            if b[4] >= 3:
                keys.append(("nmin>=3_balmin", balmin))
                keys.append(("nmin>=3_bal_touching_min", balminX))
            for k in keys:
                agg[k] = agg.get(k, 0) + 1
                if len(wit.setdefault(k, [])) < 3:
                    wit[k].append((rng, " ".join(a)))
        print("== file", os.path.basename(f), "LO", LO)
        for k in sorted(agg, key=str):
            print("AGG", " ".join(map(str, k)), agg[k])
        for k in sorted(wit, key=str):
            if k[0] in ("LL_VIOLATION", "MONO_VIOLATION", "NO_BALANCED_PAIR", "noLL") or (k[-1] is False and not k[0].startswith("LL")):
                for r, s in wit[k]:
                    print("WIT", " ".join(map(str, k)), "range", r, "|", s)
        sys.stdout.flush()


if __name__ == "__main__":
    main(sys.argv[1:])
