"""props.py (audit mg-6c30): exact tests of the PROVEN statements of mg-561a on random interval orders
(n = 9..14, not canonical-restricted) and random general posets, each with a firing control.
  T1.1  |L1(a,a')| = |L1(a',a)|   (every ordered incomparable pair)      control: above-separators only
  T3.1  sum of counted pair laws >= (P[a<c]-P[c<a]) + (P[c<b]-P[b<c])  (every a||c||b triple, no L needed)
                                                                        control: also cancel A(a,c) entirely
  P2.2  a strictly inside a', Z = S = {s,t}: |L2^(1)| <= |L1| and |L2^(2)| <= |L1|     control: Z != S
  P2.4  a strictly inside a', s in A(a,a'), r(s) <= r(a'), a unique maximal of D_s: P[a<a'] <= 2 P[s<a']
                                                                        control: a maximal but NOT unique
usage: python3 props.py SEED NIO NGEN"""
import sys, os, random
from fractions import Fraction as Fr
from multiprocessing import Pool
from eng import Poset, lambdas


def rand_io(rnd):
    n = rnd.randint(9, 13); h = rnd.randint(4, 9)
    iv = []
    for _ in range(n):
        l = rnd.randint(1, h); r = min(h, l + int(rnd.expovariate(0.6)))
        iv.append((l, r))
    return tuple(sorted(iv))


def rand_gen(rnd):
    n = rnd.randint(7, 10); p = rnd.choice((0.2, 0.3, 0.4))
    lt = [[x < y and rnd.random() < p for y in range(n)] for x in range(n)]
    for c in range(n):
        for x in range(n):
            if lt[x][c]:
                for y in range(n):
                    if lt[c][y]: lt[x][y] = True
    perm = list(range(n)); rnd.shuffle(perm)
    lt2 = [[lt[perm[x]][perm[y]] for y in range(n)] for x in range(n)]
    return Poset(n, lt2)


def test(P, is_io):
    n = P.n; st = dict(t11=0, t11_bad=0, t11_ctrl=0, t31=0, t31_bad=0, t31_ctrl=0,
                       p22=0, p22_bad=0, p22_ctrl=0, p22_ctrl_bad=0, p24=0, p24_bad=0, p24_ctrl=0, p24_ctrl_bad=0)
    M, e = P.before_counts()
    pr = lambda x, y: Fr(M[x][y], e)
    I = [(x, y) for x in range(n) for y in range(n) if P.inc[x][y]]
    for (a, a2) in I:
        if a > a2: continue
        l1, l2, l3 = lambdas(P, a, a2); m1, m2, m3 = lambdas(P, a2, a)
        st['t11'] += 1; st['t11_bad'] += (l1 != m1) or (l1 + l2 != M[a][a2]) or (m1 + m2 != M[a2][a])
        c1, _, _ = lambdas(P, a, a2, P.A(a, a2)); c2, _, _ = lambdas(P, a2, a, P.A(a2, a))
        st['t11_ctrl'] += (c1 != c2)
    for (a, c) in I:
        for b in range(n):
            if b == a or not P.inc[c][b]: continue
            lhs = sum(pr(z, c) for z in P.A(a, c) - P.A(b, c)) + sum(pr(a, w) for w in P.B(a, c)) \
                + sum(pr(c, w) for w in P.B(c, b) - P.B(c, a)) + sum(pr(z, b) for z in P.A(c, b))
            rhs = (pr(a, c) - pr(c, a)) + (pr(c, b) - pr(b, c))
            st['t31'] += 1; st['t31_bad'] += lhs < rhs
            ctrl = lhs - sum(pr(z, c) for z in P.A(a, c) - P.A(b, c))
            st['t31_ctrl'] += ctrl < rhs
    if is_io:
        iv = P.iv
        for (a, a2) in I:
            (la, ra), (lb, rb) = iv[a], iv[a2]
            if not (lb < la and ra < rb): continue          # a strictly inside a'
            Z = frozenset(z for z in range(n) if ra < iv[z][0] <= rb)
            S = P.A(a, a2)
            assert not P.B(a, a2)
            if len(S) == 2:
                s, t = sorted(S)
                def step(q, v):
                    # q = (phase, k): phase 0 a not yet, 1 a placed; k = # of s,t placed since a
                    if isinstance(q, str): return q
                    ph, k = q
                    if v == a: return (1, 0)
                    if v == a2: return 'L3' if ph == 0 else f"L2_{k}"
                    if ph == 1 and v in (s, t): return (1, k + 1)
                    return q
                r = P.count(step, start=(0, 0))
                L1, L21, L22 = r.get('L2_0', 0), r.get('L2_1', 0), r.get('L2_2', 0)
                viol = L21 > L1 or L22 > L1
                if Z == S: st['p22'] += 1; st['p22_bad'] += viol
                else: st['p22_ctrl'] += 1; st['p22_ctrl_bad'] += viol
            for s in S:
                if iv[s][1] > rb: continue
                Ds = [z for z in range(n) if lb <= iv[z][1] < iv[s][0]]
                maxi = [z for z in Ds if not any(P.lt[z][u] for u in Ds)]
                assert a in maxi
                ineq = pr(a, a2) <= 2 * pr(s, a2)
                if maxi == [a]: st['p24'] += 1; st['p24_bad'] += not ineq
                else: st['p24_ctrl'] += 1; st['p24_ctrl_bad'] += not ineq
    return st


def job(arg):
    kind, seed = arg; rnd = random.Random(seed)
    if kind == 'io':
        iv = rand_io(rnd); P = Poset.from_iv(iv)
    else:
        P = rand_gen(rnd)
    return kind, test(P, kind == 'io')


if __name__ == '__main__':
    seed, nio, ngen = map(int, sys.argv[1:4])
    jobs = [('io', seed * 10 ** 6 + i) for i in range(nio)] + [('gen', seed * 10 ** 6 + 500000 + i) for i in range(ngen)]
    tot = {'io': {}, 'gen': {}}
    with Pool(int(os.environ.get('POGO_WORKER_CORES', '3'))) as pool:
        for kind, st in pool.imap_unordered(job, jobs, chunksize=2):
            for k, v in st.items(): tot[kind][k] = tot[kind].get(k, 0) + int(v)
    for kind in ('io', 'gen'):
        print(kind, dict(sorted(tot[kind].items())))
