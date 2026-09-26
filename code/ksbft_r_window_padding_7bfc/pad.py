"""mg-7bfc (KSBFT-R): padding the thin witnesses of the delta-direct routes into the window.

INSTRUMENT ONLY (ticket rule): every poset here is a named witness or an explicit padding of one.
No case search. Exact integers / Fractions throughout. Section numbers match
docs/KSBFT-R-window-padding.md.
"""
import sys
from fractions import Fraction as Fr
from lib import (Exact, K_leak, antichain, attach_both, attach_low, hub, balanced, chain, closure, comp_connected,
                 disjoint_union, fib, from_dn, indecomposable, nontrivial_modules, ordinal_sum,
                 prime, rng)

FAIL = []


def check(cond, msg):
    print(("  ok    " if cond else "  FAIL  ") + msg)
    if not cond:
        FAIL.append(msg)


def F(k):
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def shape(P):
    return "n=%d range=%d G-conn=%s comp-conn=%s" % (P[0], rng(*P), indecomposable(*P),
                                                     comp_connected(*P))


def wstar_t(a, b, t):
    """mg-3af9/mg-b447 W*_t(a,b): A = C_{a-2} + {x,y} (ordinal), B = b_1<..<b_b,
    A below B except x not below b_1..b_t.  Same construction as ksbft_p1_walled_0b78."""
    n = a + b
    cs = list(range(a - 2))
    x, y = a - 2, a - 1
    bs = list(range(a, a + b))
    rel = [(cs[i], cs[i + 1]) for i in range(len(cs) - 1)]
    if cs:
        rel += [(cs[-1], x), (cs[-1], y)]
    rel += [(bs[i], bs[i + 1]) for i in range(b - 1)]
    rel += [(y, bs[0])]
    rel += [(x, bs[t])] if t < b else []
    return (n, closure(n, rel)), x, y


def substitute(Q, q, W):
    """lexicographic substitution Q[q <- W]: W becomes a module. W's elements come last."""
    nq, lq = Q
    nw, lw = W
    others = [i for i in range(nq) if i != q]
    n = len(others) + nw
    idx = {o: k for k, o in enumerate(others)}
    wi = [len(others) + k for k in range(nw)]
    lt = [[False] * n for _ in range(n)]
    for a in others:
        for b in others:
            lt[idx[a]][idx[b]] = lq[a][b]
        for w in wi:
            lt[idx[a]][w] = lq[a][q]
            lt[w][idx[a]] = lq[q][a]
    for i in range(nw):
        for j in range(nw):
            lt[wi[i]][wi[j]] = lw[i][j]
    return n, lt, wi


P9 = from_dn((0, 0, 2, 2, 3, 0xb, 0x2b, 0x2f, 0x7f))       # KSBFT-Q P_9 (range 5, self-dual)
PROBE_D_A = (6, closure(6, [(0, 1), (1, 2), (1, 4), (2, 3)]))            # mg-e2de pair A (P1 ranges2)
PROBE_D_B = (6, closure(6, [(0, 1), (0, 3), (1, 2), (2, 4), (3, 4)]))    # mg-e2de pair B


def sec1():
    print("§1 EXACT PADDINGS (Lemma 1.1): W-internal pair laws under +, ⊕, substitution")
    for name, W in (("F_7", fib(7)), ("P_9", P9), ("2+2", disjoint_union(chain(2), chain(2)))):
        EW = Exact(*W)
        pw = EW.pairs()
        n = W[0]
        pads = []
        pads.append(("W + C_8", disjoint_union(W, chain(8)), list(range(n))))
        pads.append(("W ⊕ A_9", ordinal_sum(W, antichain(9)), list(range(n))))
        # substitution into F_9 at its middle element (F_9 is prime, KSBFT-J Lemma 4.2 family)
        Q = fib(9)
        nS, lS, wi = substitute(Q, 4, W)
        pads.append(("F_9[x_4 <- W]", (nS, lS), wi))
        for pname, P, emb in pads:
            E = Exact(*P)
            same = all(E.before(emb[a], emb[b]) == p for (a, b), p in pw.items())
            check(same, "%-4s in %-14s %s : every W-pair law EXACTLY preserved" % (name, pname, shape(P)))
    # the three are decompositions: the witness is a proper non-chain module in each
    W = fib(7)
    for pname, P in (("F_7 + C_8", disjoint_union(W, chain(8))),
                     ("F_7 ⊕ A_9", ordinal_sum(W, antichain(9)))):
        mods = nontrivial_modules(*P)
        check(any(set(range(7)) <= set(m) and len(m) < P[0] and
                  not all(P[1][i][j] or P[1][j][i] or i == j for i in m for j in m) for m in mods),
              "%s has a proper NON-CHAIN module containing F_7 (so it is not a minimal-cex shape)" % pname)
    # CONTROL: a non-module padding does NOT preserve the law exactly (must differ)
    A = attach_low(fib(7), 3)
    EA, EW = Exact(*A), Exact(*fib(7))
    diff = [(a, b) for (a, b), p in EW.pairs().items() if EA.before(a, b) != p]
    check(len(diff) > 0, "NEGATIVE CONTROL: attach_low(F_7,3) (not a module embedding) changes %d of "
          "%d pair laws -> exactness claim CAUGHT when the hypothesis fails" % (len(diff), len(EW.pairs())))


def sec2():
    print("\n§2 FIBONACCI INSULATION (Thm 2.1): F_N with z || x_1..x_R, z < x_{R+1}..x_N")
    print("   centre pair B = {x_i,x_{i+1}}, i = N//2 (1-indexed); P(B) = F_i F_{N-i}/F_{N+1} in F_N")
    print("   %4s %3s %12s %14s %14s %9s  %s" % ("N", "R", "F_N", "padded", "closed form", "|diff|", "shape"))
    for N, R in ((14, 5), (20, 8), (30, 8), (41, 8), (41, 12), (61, 8), (81, 8), (81, 20)):
        P = attach_low(fib(N), R)
        E = Exact(*P)
        i = N // 2
        pB = Fr(F(i) * F(N - i), F(N + 1))
        pA = Fr(F(R) * F(N - R), F(N + 1))
        pAB = Fr(F(R) * F(i - R - 1) * F(N - i), F(N + 1))
        pred = pB + (pA * pB - pAB) / (R + 1 - pA)
        got = E.before(i, i - 1)       # 0-indexed: x_{i+1} before x_i  <=> domino at {i,i+1}
        u = Fr(382, 1000)              # rational upper bound for |q| = phi^-2 = 0.38197...
        a = i - R - 1
        bound = 4 * u ** a / ((1 - u ** a) ** 2 * R)
        ok = (got == pred) and abs(got - pB) <= bound
        pr = prime(*P) if N <= 30 else None
        print("   %4d %3d %12.9f %14.9f %14s %9.2e  %s prime=%s  |diff|<=4u^a/((1-u^a)^2 R)=%.1e %s" % (
            N, R, float(pB), float(got), "EQUAL" if got == pred else "DIFFERS", float(abs(got - pB)),
            shape(P), pr, float(bound), "ok" if ok else "FAIL"))
        if not ok:
            FAIL.append("fib insulation N=%d R=%d" % (N, R))
    cb = (5 - 5 ** 0.5) / 10
    print("   C_BFT = (5-sqrt5)/10 = %.9f; limit of F_i F_{N-i}/F_{N+1} is 1/(sqrt5*phi) = %.9f" % (
        cb, 1 / (5 ** 0.5 * (1 + 5 ** 0.5) / 2)))
    for N in (8, 12, 20, 30):
        for R in range(5, min(N - 2, 12)):
            P = attach_low(fib(N), R)
            if not prime(*P):
                check(False, "attach_low(F_%d,%d) prime" % (N, R))
    check(True, "attach_low(F_N,R) is prime for every N in {8,12,20,30}, 5 <= R < min(N-2,12) (EMPIRICAL)")
    # CONTROL: R=3 is NOT prime (module found) -- the primality test can say no
    mods = nontrivial_modules(*attach_low(fib(12), 3))
    check(len(mods) > 0, "CONTROL: attach_low(F_12,3) is NOT prime (module %s) -> primality test CAUGHT a module"
          % sorted(mods[0]))


def sec3():
    print("\n§3 W*, W*_t: the Step-6 witnesses are ordinal-DECOMPOSABLE")
    for (a, b, t) in ((4, 4, 2), (4, 8, 3), (9, 9, 7), (9, 10, 8)):
        (P, x, y) = wstar_t(a, b, t)
        E = Exact(*P)
        check(not indecomposable(*P), "W*_%d(%d,%d): %s  p_xy=%s  -> not in the minimal-cex class"
              % (t, a, b, shape(P), E.before(x, y)))
    # the indecomposable core of W*_t is the star C_1 + C_{t+1}
    (P, x, y) = wstar_t(4, 4, 2)
    core = [x, y, 4, 5]    # x, y, b_1, b_2
    n = len(core)
    sub = (n, [[P[1][core[i]][core[j]] for j in range(n)] for i in range(n)])
    E = Exact(*sub)
    check(E.before(0, 1) == Fr(1, 4) and indecomposable(*sub),
          "core {x,y,b_1,b_2} of W*(4,4,2) is the star C_1 + C_3 with p_xy = 1/4 (as in W*)")

    print("\n   (T_E) on INSULATED W*: base F_M replaces C_{a-2}; top F_s replaces the chain B")
    print("   f_0..f_{M-1} = F_M; x,y above f_0..f_{M-2}, || f_{M-1}; b_1..b_s = F_s above all f and y;")
    print("   x < b_j iff j >= t+2 (so x || b_1..b_{t+1}). Cut A = F_M + {x,y}.")
    for M, t, s in ((8, 2, 8), (12, 3, 12), (16, 6, 16)):
        n = M + 2 + s
        x, y = M, M + 1
        bs = list(range(M + 2, M + 2 + s))
        rel = [(i, j) for i in range(M) for j in range(M) if j - i >= 2]
        rel += [(i, x) for i in range(M - 1)] + [(i, y) for i in range(M - 1)]
        rel += [(bs[i], bs[j]) for i in range(s) for j in range(s) if j - i >= 2]
        rel += [(y, b) for b in bs] + [(i, b) for i in range(M) for b in bs]
        rel += [(x, bs[j - 1]) for j in range(t + 2, s + 1)]
        P = (n, closure(n, rel))
        A = list(range(M + 2))
        PA = (len(A), [[P[1][i][j] for j in A] for i in A])
        EP, EA = Exact(*P), Exact(*PA)
        d1 = K_leak(EP, A) / min(len(A), n - len(A))
        balA = [(a, b, p) for (a, b), p in EA.pairs().items() if balanced(p)]
        surv = [(a, b, EP.before(a, b)) for (a, b, p) in balA if balanced(EP.before(a, b))]
        pxy = EP.before(x, y)
        print("   M=%2d t=%d s=%2d %s prime=%s Delta_1=%.4f; P[A] balanced pairs %s; balanced in P too: %s" % (
            M, t, s, shape(P), prime(*P), float(d1), [(a, b, str(p)) for a, b, p in balA],
            [(a, b, str(q)) for a, b, q in surv]))
        check(len(surv) > 0 and not balanced(pxy),
              "insulated W* (M=%d,t=%d): p_xy = %s is unbalanced as in W*, but a base pair far from the cut "
              "survives -> (T_E) HOLDS on this indecomposable padding" % (M, t, pxy))


def probe_b_cert(E, x, y):
    Tx, Ty = E.slot_law(x), E.slot_law(y)
    best = Fr(0)
    for k in range(E.n - 1):
        s = Fr(Tx[k] + Tx[k + 1] + Ty[k] + Ty[k + 1], E.e) - 1
        best = max(best, s / 2)
    return best


def sec4():
    print("\n§4 PROBE B (diagonal capacity, mg-92e6): max over incomparable pairs and slots of")
    print("   1/2 (T[x,k]+T[x,k+1]+T[y,k]+T[y,k+1]-1)^+ ; certifies delta >= 1/3 iff >= 1/3")
    rows = [("F_12", fib(12)), ("attach_low(F_12,8)", attach_low(fib(12), 8)),
            ("attach_low(F_16,8)", attach_low(fib(16), 8)), ("attach_low(F_16,10)", attach_low(fib(16), 10)),
            ("attach_both(F_16,7)", attach_both(16, 7)), ("attach_both(F_20,8)", attach_both(20, 8)),
            ("attach_both(F_24,8)", attach_both(24, 8))]
    for name, P in rows:
        E = Exact(*P)
        cert = {}
        for (a, b) in E.pairs():
            cert[(a, b)] = probe_b_cert(E, a, b)
        best = max(cert.values())
        arg = max(cert, key=cert.get)
        pr = prime(*P) if P[0] <= 22 else None
        print("   %-20s %s prime=%s delta=%.4f  max cert=%.4f at %s  -> %s" % (
            name, shape(P), pr, float(E.delta()), float(best), arg,
            "CERTIFIES" if best >= Fr(1, 3) else "does NOT certify"))
        if name == "attach_both(F_20,8)":
            check(best < Fr(1, 3) and pr and rng(*P) == 8 and E.delta() >= Fr(1, 3),
                  "attach_both(F_20,8): prime, range 8, delta >= 1/3, and NO probe-B certificate "
                  "(max %s < 1/3) -> probe B incomplete on a prime window poset" % best)
    # soundness control on these posets: cert <= balance of its pair
    for name, P in rows[:2]:
        E = Exact(*P)
        ok = all(probe_b_cert(E, a, b) <= min(p, 1 - p) for (a, b), p in E.pairs().items())
        check(ok, "probe-B bound <= min(p,1-p) on every pair of %s (soundness, consistency check)" % name)


def sec5():
    print("\n§5 PROBE D blindness (mg-e2de n=6 pair, same incomparability graph, delta 4/9 vs 1/2)")
    EA, EB = Exact(*PROBE_D_A), Exact(*PROBE_D_B)
    print("   bare: delta(A)=%s delta(B)=%s  e=%d,%d" % (EA.delta(), EB.delta(), EA.e, EB.e))
    for k in (3, 4, 8):
        PA = disjoint_union(PROBE_D_A, chain(k))
        PB = disjoint_union(PROBE_D_B, chain(k))
        dA, dB = Exact(*PA).delta(), Exact(*PB).delta()
        print("   + C_%d: %s | delta(A+C)=%s=%.4f  delta(B+C)=%s=%.4f" % (
            k, shape(PA), dA, float(dA), dB, float(dB)))
    Q = attach_low(fib(20), 8)
    dQ = Exact(*Q).delta()
    for nm, W in (("A", PROBE_D_A), ("B", PROBE_D_B)):
        P = ordinal_sum(W, Q)
        print("   %s ⊕ attach_low(F_20,8): %s delta=%.4f" % (nm, shape(P), float(Exact(*P).delta())))
    check(dQ < Fr(1, 2) and dQ > Fr(4, 9),
          "delta(attach_low(F_20,8)) = %.4f lies in (4/9, 1/2): the two ⊕-paddings keep different delta" % float(dQ))


def codegree(n, lt, x, y):
    """number of elements comparable to exactly one of x, y"""
    c = 0
    for z in range(n):
        if z in (x, y):
            continue
        cx = lt[x][z] or lt[z][x]
        cy = lt[y][z] or lt[z][y]
        c += cx != cy
    return c


def sec6():
    print("\n§6 HUB PADDING (Lemma 1.3): W + C_k with c_k above a down-set U of W")
    W = disjoint_union(chain(2), chain(2))      # a1=0 < b1=1 ; a2=2 < b2=3
    x, y = 0, 3                                 # the pair (a1, b2): P[b2 before a1] = 1/6
    EW = Exact(*W)
    print("   2+2: P[b2 before a1] = %s, separating number (comparable to exactly one) = %d" % (
        EW.before(y, x), codegree(*W, x, y)))
    print("   single hub hub(2+2,{a1,a2,b2},k) leaves the NON-chain module {a2,b2,c_1..c_{k-1}}:")
    P1 = hub(W, [0, 2, 3], 8)
    bad = [sorted(M) for M in nontrivial_modules(*P1)
           if not all(P1[1][i][j] or P1[1][j][i] or i == j for i in M for j in M)]
    check(bad == [[2, 3] + list(range(4, 11))], "CONTROL: module test finds it: %s" % bad)
    print("   double hub: add a second chain d_1<..<d_k with d_k > a2 only (splits that module)")
    for k in (8, 16, 30):
        P = hub(hub(W, [0, 2, 3], k), [2], k)
        E = Exact(*P)
        q = E.before(y, x)
        mods = nontrivial_modules(*P)
        chain_mods = all(all(P[1][i][j] or P[1][j][i] or i == j for i in M for j in M) for M in mods)
        print("   k=%2d %s only chain modules=%s ; P[b2 before a1] = %s = %.5f ; separating number %d ;"
              " delta(P) = %.4f" % (k, shape(P), chain_mods, q, float(q), codegree(*P, x, y), float(E.delta())))
        check(q < Fr(1, 3) and chain_mods and comp_connected(*P) and indecomposable(*P)
              and codegree(*P, x, y) == 2 and rng(*P) >= 8,
              "double hub(2+2,k=%d): minimal-cex shape (G-conn, comp-conn, only chain modules), range %d, "
              "pair keeps separating number 2 and balance %.4f < 1/3" % (k, rng(*P), float(q)))
    # control: the weight bound is two-sided; a planted tighter bound (factor (2+k)/k) must be violated
    P = hub(W, [0, 2, 3], 8)
    q = Exact(*P).before(y, x)
    check(Fr(1, 6) * Fr(8, 12) <= q <= Fr(1, 6) * Fr(12, 8) and q != Fr(1, 6),
          "CONTROL: hub(2+2,8) law is NOT exactly the W law (%s != 1/6) -> padding is approximate, as stated" % q)


def sec7():
    print("\n§7 FINITE WITNESSES OF A28 (bitmasks as in ksbft_p1_walled_0b78/ranges2.py): already in the window?")
    W = [("(L*) n=9 #1 (mg-5cba)", (0, 1, 0, 4, 0, 0, 32, 96, 239)),
         ("(L*) n=9 #2 (mg-5cba)", (0, 0, 0, 0, 0, 16, 48, 16, 247)),
         ("(L*) n=10 (mg-789d)", (0, 1, 3, 0, 9, 0, 32, 96, 255, 239)),
         ("(L*) n=11 (mg-789d)", (0, 1, 3, 7, 0, 1, 1, 113, 1, 257, 257)),
         ("(F)&(M#) n=10 a", (0, 0, 0, 7, 15, 31, 15, 6, 135, 135)),
         ("(F)&(M#) n=12 (mg-5e82)", (0, 0, 3, 7, 15, 7, 63, 2, 135, 391, 7, 1159))]
    inwin = []
    for name, dn in W:
        P = from_dn(dn)
        mods = nontrivial_modules(*P)
        nonchain = [sorted(M) for M in mods
                    if not all(P[1][i][j] or P[1][j][i] or i == j for i in M for j in M)]
        print("   %-26s %s  non-chain proper modules: %d" % (name, shape(P), len(nonchain)))
        if rng(*P) >= 8 and indecomposable(*P):
            inwin.append(name)
    check(len(inwin) == 3, "exactly the three (L*) refuters n=9 #1, n=9 #2, n=11 have range >= 8 and "
          "connected G: %s" % inwin)


def main():
    sec1()
    sec2()
    sec3()
    sec4()
    sec5()
    sec6()
    sec7()
    print("\nSUMMARY: %d failed checks" % len(FAIL))
    for f in FAIL:
        print("  FAILED:", f)
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
