"""witnesses.py (audit mg-5ecf): named witnesses and Thm 2.1(b).

For T8, T13, T14, N12, P9, Q_m (m = 0, 4, 14), the mg-7bfc hosts (attach_both(F_20,8) = A14, attach_low(F_N,R),
the double hub of 2+2 = A16 shape), O9a, O9b and 400 random interval orders n = 10..24:
  - interval order? (2+2-free), semiorder? (also 3+1-free);
  - Thm 2.1(b) injection |Lambda_1| <= |Lambda_3| for EVERY ordered incomparable pair (a, a'), where
    Lambda_1 = {a before a', no element of S(a,a') strictly between}, Lambda_3 = {a' before a}.
    This inequality is unconditional (no counterexample hypothesis), so it can be tested on real posets.
    CONTROL: S replaced by above-separators only must produce violations somewhere.
  - delta, and whether the relation P[x<y] > 2/3 is transitive (Thm 2.1(a) only needs the no-balanced-pair
    hypothesis; here we just report delta).
Witness constructors are imported read-only from the author's-predecessor code (mg-ce69, mg-7bfc); every
computation is done by eng.py.
"""
import random, sys
from fractions import Fraction as F
import eng



def from_lt(n, lt):
    up = [0] * n
    for x in range(n):
        for y in range(n):
            if lt[x][y]:
                up[x] |= 1 << y
    return n, up


def parse(s):
    t = s.split()
    return eng.from_down([int(x, 16) for x in t[1:]])


def lam1(P, a, b, Smask):
    """#linear extensions with a before b and no element of Smask added while a in I and b not in I."""
    n, up = P
    dn = eng.downs(P)
    full = (1 << n) - 1
    f = {0: 1}
    layer = {0: 1}
    for _ in range(n):
        nxt = {}
        for I, c in layer.items():
            for x in range(n):
                if I >> x & 1 or dn[x] & ~I:
                    continue
                if x == b and not I >> a & 1:
                    continue
                if Smask >> x & 1 and I >> a & 1 and not I >> b & 1:
                    continue
                J = I | 1 << x
                nxt[J] = nxt.get(J, 0) + c
        layer = nxt
    return layer.get(full, 0)


def sep_masks(P, above_only=False):
    n, up = P
    cov = eng.covers(P)
    M = {}
    for a in range(n):
        for b in range(n):
            if eng.inc(P, a, b):
                m = 0
                for z in range(n):
                    if cov[a] >> z & 1 and eng.inc(P, z, b):
                        m |= 1 << z
                    if not above_only and cov[z] >> b & 1 and eng.inc(P, z, a):
                        m |= 1 << z
                M[a, b] = m
    return M


def check21b(P, above_only=False):
    e, N = eng.laws(P)
    viol = 0
    pairs = 0
    for (a, b), m in sep_masks(P, above_only).items():
        pairs += 1
        if lam1(P, a, b, m) > N[b][a]:
            viol += 1
    return pairs, viol, e, N


def build():
    W = []
    for name, s in [("T8", "8 0 0 2 6 3 e 17 5f"), ("T13", "13 0 1 0 3 5 17 3f b bf 1ff 7f 7ff 47f"),
                    ("T14", "14 0 0 153 12 2 1b 3 3b 53 15f 11ff 33ff bb 3ff"),
                    ("N12", "12 0 4 0 6 f 885 6 805 aff 5f 8af 5"), ("P9", "9 0 0 2 2 3 b 2b 2f 7f")]:
        W.append((name, parse(s)))
    import importlib
    sys.path.insert(0, "../ksbft_q2_both_ends_ce69")
    import longtail
    celib = importlib.import_module("lib")
    P9 = celib.parse("9 0 0 2 2 3 b 2b 2f 7f")
    for m in (0, 4, 14):
        lo = longtail.grow(P9, m, 1)
        W.append((f"Q_{m}", eng.from_down(longtail.glue(lo, longtail.dual(lo), 1))))
    sys.modules.pop("lib")
    sys.path.remove("../ksbft_q2_both_ends_ce69")
    sys.path.insert(0, "../ksbft_r_window_padding_7bfc")
    rlib = importlib.import_module("lib")
    assert hasattr(rlib, "attach_both")
    W.append(("A14 = attach_both(F_20,8)", from_lt(*rlib.attach_both(20, 8))))
    W.append(("attach_low(F_12,8)", from_lt(*rlib.attach_low(rlib.fib(12), 8))))
    W.append(("attach_low(F_16,10)", from_lt(*rlib.attach_low(rlib.fib(16), 10))))
    w22 = rlib.closure(4, [(0, 1), (2, 3)])
    W2 = (4, w22)
    for k in (4, 8):
        W.append((f"double hub(2+2,k={k}) (A16 shape)", from_lt(*rlib.hub(rlib.hub(W2, [0, 2, 3], k), [2], k))))
    W.append(("F_12", from_lt(*rlib.fib(12))))
    for name, iv in [("O9a", [(1, 1), (1, 2), (1, 5), (2, 3), (2, 6), (3, 4), (4, 5), (5, 6), (6, 6)]),
                     ("O9b", [(1, 1), (1, 2), (2, 3), (2, 6), (3, 4), (4, 5), (5, 6), (6, 7), (7, 7)])]:
        W.append((name, eng.from_intervals(iv)))
    return W


def rand_io(n, rng):
    """random interval order: random integer intervals, canonicalised via the poset."""
    iv = []
    for _ in range(n):
        a = rng.randint(1, 2 * n)
        L = rng.choice([0, 0, 1, 1, 2, 3, rng.randint(0, n)])
        iv.append((a, a + L))
    return eng.from_intervals(iv)


def run():
    tot_v = 0
    for name, P in build():
        n = P[0]
        io = not eng.has_2p2(P)
        so = io and not eng.has_3p1(P)
        pairs, v, e, N = check21b(P)
        d = eng.delta(P, (e, N))
        tot_v += v
        print(f"{name}: n={n} interval order={io} semiorder={so} delta={d} ({float(d):.5f}); "
              f"Thm2.1(b) injection: {pairs} ordered inc pairs, violations={v}")
        sys.stdout.flush()
    # O9a extra: P[[1,1] < [1,2]] and ([2,3],[1,5]) separators
    O9a = eng.from_intervals([(1, 1), (1, 2), (1, 5), (2, 3), (2, 6), (3, 4), (4, 5), (5, 6), (6, 6)])
    e, N = eng.laws(O9a)
    iv = [(1, 1), (1, 2), (1, 5), (2, 3), (2, 6), (3, 4), (4, 5), (5, 6), (6, 6)]
    print(f"O9a: P[[1,1]<[1,2]] = {F(N[0][1], e)} = {N[0][1] / e:.4f}; "
          f"S([2,3],[1,5]) = {[iv[z] for z in range(9) if sep_masks(O9a)[3, 2] >> z & 1]}")
    rng = random.Random(7)
    rv = 0
    rp = 0
    for t in range(400):
        P = rand_io(rng.randint(10, 24), rng)
        pairs, v, _, _ = check21b(P)
        rv += v
        rp += pairs
    print(f"random interval orders (400, n=10..24): {rp} ordered inc pairs, Thm2.1(b) violations = {rv}")
    tot_v += rv
    # control: above-only S
    cv = 0
    for n in range(3, 7):
        for iv in eng.gen(n):
            cv += check21b(eng.from_intervals(iv), above_only=True)[1]
    print(f"CONTROL (S = above-separators only), interval orders n=3..6: violations = {cv} (must be > 0)")
    print("RESULT", "Thm 2.1(b) never violated; control fires" if tot_v == 0 and cv > 0 else "FAILURE")


if __name__ == "__main__":
    run()
