"""mg-244e audit of KSBFT-R (mg-7bfc). Independent recomputation of every padded exhibit.
Run: python3 audit.py > out_audit.txt   (exact Fractions; deterministic; ~1 min)"""
import random
from fractions import Fraction as Fr
from itertools import combinations, permutations
from math import sqrt
from indep import Poset, fibrel, F, chk, FAIL

third = Fr(1, 3)
bal = lambda p: third <= p <= 2 * third


def attach_low(N, R):
    # doc Thm 2.1: F_N, z || x_1..x_R, z < x_{R+1..N}   (0-indexed x_0..x_{N-1}, z = N)
    return Poset(N + 1, fibrel(N) + [(N, j) for j in range(R, N)])


print("§A  Thm 2.1 closed form vs exact count, every admissible i (not only the centre)")
phi = (1 + sqrt(5)) / 2; u = phi ** -2
for N, R in ((12, 4), (14, 5), (20, 8), (26, 8), (30, 11)):
    P = attach_low(N, R)
    worst = 0
    for i in range(R + 2, N):            # 1-indexed i, a = i-R-1 >= 1, pair x_i,x_{i+1}
        a = i - R - 1
        PB = Fr(F(i) * F(N - i), F(N + 1)); PA = Fr(F(R) * F(N - R), F(N + 1))
        PAB = Fr(F(R) * F(a) * F(N - i), F(N + 1))
        closed = PB + (PA * PB - PAB) / (R + 1 - PA)
        exact = P.before(i, i - 1)        # x_{i+1} (0-idx i) before x_i (0-idx i-1)
        assert exact == closed, (N, R, i)
        bound = 4 * u ** a / ((1 - u ** a) ** 2 * R)
        assert abs(float(exact - PB)) <= bound + 1e-15, (N, R, i)
        worst = max(worst, abs(float(exact - PB)))
    chk(P.rng() == max(R, 3) and P.g_conn() and P.g_conn(True),
        "attach_low(F_%d,%d): closed form EXACT at all %d admissible i, bound (3) holds, range=%d, both graphs connected"
        % (N, R, N - R - 2, P.rng()))

print("\n§A' primality of attach_low(F_N,R): the audit's hand proof says prime iff R>=4 (N>=R+2, N>=4)")
bad = []
for N in range(6, 41, 2):
    for R in range(3, min(N - 2, 14) + 1):
        m = attach_low(N, R).proper_nonchain_module()
        if (R >= 4) != (m is None):
            bad.append((N, R, m))
chk(not bad, "attach_low(F_N,R) prime for all R>=4, and has a module for R=3, N=6..40 even, R<=14  %s" % bad[:3])
print("   R=3 module (control):", attach_low(12, 3).proper_nonchain_module())

print("\n§B  probe B on attach_both(F_N,R), built from the doc's words")
def attach_both(N, R):
    z, zp = N, N + 1
    rel = fibrel(N) + [(z, j) for j in range(R, N)] + [(j, zp) for j in range(N - R)]
    return Poset(N + 2, rel)

def cert(P):
    lev = P.ideals_by_size()
    T = [P.slot_law(x, lev) for x in range(P.n)]
    best, arg = Fr(0), None
    for x, y in combinations(range(P.n), 2):
        if P.comp(x, y):
            continue
        for k in range(P.n - 1):
            s = (T[x][k] + T[x][k + 1] + T[y][k] + T[y][k + 1] - 1) / 2
            if s > best:
                best, arg = s, (x, y, k)
    return best, arg

for name, P in (("attach_low(F_16,8)", attach_low(16, 8)), ("attach_both(F_20,8)", attach_both(20, 8)),
                ("attach_both(F_26,8)", attach_both(26, 8)), ("attach_both(F_20,10)", attach_both(20, 10))):
    b, arg = cert(P)
    mod = P.proper_nonchain_module()
    mins, maxs = P.minimal(), P.maximal()
    print("   %-20s n=%d range=%d prime=%s Gconn=%s Cconn=%s delta=%.4f maxcert=%s=%.4f at %s  #min=%d #max=%d"
          % (name, P.n, P.rng(), mod is None, P.g_conn(), P.g_conn(True), float(P.delta()), b, float(b), arg,
             len(mins), len(maxs)))
    if name == "attach_both(F_20,8)":
        chk(b == Fr(13627, 46282) and P.rng() == 8 and mod is None and P.g_conn() and P.g_conn(True),
            "attach_both(F_20,8): max certificate 13627/46282 < 1/3 reproduced; prime; range 8")
        chk(len(mins) >= 3 and len(maxs) >= 3,
            "attach_both(F_20,8) also has >=3 minimal and >=3 maximal elements (KSBFT-Q O1 at BOTH ends; (M4) satisfied)")

print("\n§C  probe D double hub, built from Lemma 1.3's words; W = 2+2 with a1<b1, a2<b2 (a's bottoms)")
a1, b1, a2, b2 = 0, 1, 2, 3
def hub_rel(m, k, U, off):
    ch = [off + i for i in range(k)]
    return [(ch[i], ch[i + 1]) for i in range(k - 1)] + [(uu, ch[-1]) for uu in U]
W = [(a1, b1), (a2, b2)]
W0 = Poset(4, W)
chk(W0.before(b2, a1) == Fr(1, 6), "2+2: P[b2 before a1] = 1/6")
for k in (8, 16):
    P = Poset(4 + 2 * k, W + hub_rel(4, k, [a1, a2, b2], 4) + hub_rel(4, k, [a2], 4 + k))
    q = P.before(b2, a1)
    sep = sum(1 for z in range(P.n) if z not in (a1, b2) and P.comp(z, a1) != P.comp(z, b2))
    mod = P.proper_nonchain_module()
    print("   k=%d n=%d range=%d Gconn=%s Cconn=%s module=%s P[b2<a1]=%s=%.5f sep=%d #min=%d #max=%d delta=%.4f"
          % (k, P.n, P.rng(), P.g_conn(), P.g_conn(True), mod, q, float(q), sep, len(P.minimal()),
             len(P.maximal()), float(P.delta())))
    if k == 8:
        chk(q == Fr(5336, 27441) and P.rng() == 18 and sep == 2 and (mod is None or mod[0] == "chain")
            and P.g_conn() and P.g_conn(True), "double hub k=8 reproduced: 5336/27441, range 18, sep 2, only chain modules")
# single hub: Lemma 1.3(1) ext formula, every tau in L(W)
k = 8
H = Poset(4 + k, W + hub_rel(4, k, [a1, a2, b2], 4))
Wl = [t for t in permutations(range(4)) if all(t.index(x) < t.index(y) for x, y in W)]
okf = True
from math import comb
for t in Wl:
    ext = Poset(H.n, W + hub_rel(4, k, [a1, a2, b2], 4) + [(t[i], t[i + 1]) for i in range(3)]).e()
    p = 1 + max(t.index(x) for x in (a1, a2, b2))
    okf &= ext == comb(4 + k, k) - comb(p - 1 + k, k)
chk(okf, "Lemma 1.3(1): ext(tau) = C(m+k,k) - C(p_tau-1+k,k) exactly for all 6 tau (single hub, k=8)")
print("   single hub: P[b2<a1] =", H.before(b2, a1), " module:", H.proper_nonchain_module())
HU = Poset(4 + k, W + hub_rel(4, k, [0, 1, 2, 3], 4))
chk(not HU.g_conn(), "Lemma 1.3(2) FAILS for U = W: hub with U = all of 2+2 has DISCONNECTED incomparability graph (c_k isolated)")

print("\n§D  Step 6: W*_t from mg-b447 Thm 4.1's text, and insulated W* from the doc's text")
def wstar(a, b, t):
    cs = list(range(a - 2)); x, y = a - 2, a - 1; bs = list(range(a, a + b))
    rel = [(cs[i], cs[i + 1]) for i in range(len(cs) - 1)] + [(cs[-1], x), (cs[-1], y)]
    rel += [(bs[i], bs[i + 1]) for i in range(b - 1)] + [(y, bs[0])] + [(x, bs[t])]
    return Poset(a + b, rel), x, y
for a, b, t in ((4, 4, 2), (4, 8, 3), (9, 9, 7)):
    P, x, y = wstar(a, b, t)
    # ordinal-sum check: C_{a-2} below everything else, b_{t+1}.. above everything else
    lowok = all(P.lt(c, z) for c in range(a - 2) for z in range(P.n) if z > c)
    hiok = all(P.lt(z, bb) for bb in range(a + t, a + b) for z in range(P.n) if z < bb)
    chk(lowok and hiok and not P.g_conn() and P.before(x, y) == Fr(1, t + 2),
        "W*_%d(%d,%d) = C_%d ⊕ ({x}+C_%d) ⊕ C_%d, p_xy=1/%d" % (t, a, b, a - 2, t + 1, b - t, t + 2))
    # the only incomparable pairs of the sides P[A], P[B]: A = C + {x,y}, B = chain
    incA = [(u, v) for u, v in combinations(range(a), 2) if not P.comp(u, v)]
    chk(incA == [(x, y)], "   sides have exactly one incomparable pair {x,y}: W* refutes the EXISTENTIAL (T), not only a modulus form")

def insulated(M, t, s):
    x, y = M, M + 1; bs = list(range(M + 2, M + 2 + s))
    rel = fibrel(M) + [(i, x) for i in range(M - 1)] + [(i, y) for i in range(M - 1)]
    rel += fibrel(s, M + 2) + [(y, bb) for bb in bs] + [(i, bb) for i in range(M) for bb in bs]
    rel += [(x, bs[j - 1]) for j in range(t + 2, s + 1)]
    return Poset(M + 2 + s, rel), x, y

for M, t, s in ((8, 2, 8), (16, 6, 16), (20, 6, 20), (24, 6, 24), (30, 6, 30)):
    P, x, y = insulated(M, t, s)
    A = list(range(M + 2)); nA = len(A)
    PA = Poset(nA, [(i, j) for i in A for j in A if P.lt(i, j)])
    lev = P.ideals_by_size()
    EK = sum(sum(P.slot_law(z, lev)[nA:]) for z in A)
    d1 = EK / min(nA, P.n - nA)
    balA = [(i, j, PA.before(i, j)) for i, j in combinations(A, 2) if not PA.comp(i, j) and bal(PA.before(i, j))]
    surv = [(i, j) for i, j, _ in balA if bal(P.before(i, j))]
    pxy = P.before(x, y)
    mod = P.proper_nonchain_module() if P.n <= 40 else "skip"
    print("   (M,t,s)=(%d,%d,%d) n=%d range=%d module=%s Gconn=%s Cconn=%s Delta1=%.4f p_xy: %s -> %.4f ; bal(P[A])=%s surviving=%s"
          % (M, t, s, P.n, P.rng(), mod, P.g_conn(), P.g_conn(True), float(d1), PA.before(x, y), float(pxy),
             [(i, j) for i, j, _ in balA], surv))
    if (M, t, s) == (16, 6, 16):
        chk(pxy == Fr(5702887, 39150182) and P.rng() == 9 and abs(float(d1) - 0.0443) < 5e-5 and surv,
            "insulated W* (16,6,16) reproduced: p_xy 5702887/39150182, range 9, Delta1 0.0443, (T∃) holds")

print("\n§E  'exactly three exact paddings': a NON-module embedding with exactly uniform law in a PRIME host")
# z1<u, z2<v, z1<w, z2<w : automorphism swaps (z1,z2),(u,v); W={u,v} antichain, not a module
P = Poset(5, [(0, 2), (1, 3), (0, 4), (1, 4)])
chk(P.proper_nonchain_module() is None and not P.is_module({2, 3}) and P.before(2, 3) == Fr(1, 2),
    "prime 5-poset, W={u,v} is not a module, yet P[u<v]=1/2 = W's law exactly")
# small instrument search: an induced 2+2 with EXACTLY uniform law (1/6 each) in a prime host, n<=8
random.seed(244)
found = None
for trial in range(4000):
    n = random.choice((6, 7, 8)); pr = random.choice((0.2, 0.3, 0.4))
    perm = list(range(n)); random.shuffle(perm)
    rel = [(perm[i], perm[j]) for i in range(n) for j in range(i + 1, n) if random.random() < pr]
    Q = Poset(n, rel)
    if Q.proper_nonchain_module() is not None or not Q.g_conn():
        continue
    for a, b, c, d in permutations(range(n), 4):
        if not (Q.lt(a, b) and Q.lt(c, d) and a < c) or any(Q.comp(p_, q_) for p_ in (a, b) for q_ in (c, d)):
            continue
        ws = [(a, b), (c, d)]
        taus = [t for t in permutations((a, b, c, d)) if all(t.index(p_) < t.index(q_) for p_, q_ in ws)]
        base = [(p_, q_) for p_ in range(n) for q_ in Q.above[p_]]
        exts = {Poset(n, base + [(t[i], t[i + 1]) for i in range(3)]).e() for t in taus}
        if len(exts) == 1:
            found = (n, sorted(base), (a, b, c, d)); break
    if found:
        break
print("   uniform-law 2+2 in a prime host:", found if found else "none found in 4000 random prime hosts, n<=8 (EMPIRICAL negative)")

print("\n§F  A28 finite witnesses (bitmasks as quoted by mg-0b78 ranges2.py)")
def from_dn(dn):
    return Poset(len(dn), [(j, i) for i in range(len(dn)) for j in range(len(dn)) if (dn[i] >> j) & 1])
for nm, dn in (("n=9 #1", (0, 1, 0, 4, 0, 0, 32, 96, 239)), ("n=9 #2", (0, 0, 0, 0, 0, 16, 48, 16, 247)),
               ("n=11", (0, 1, 3, 7, 0, 1, 1, 113, 1, 257, 257))):
    P = from_dn(dn)
    print("   %s range=%d Gconn=%s Cconn=%s module=%s" % (nm, P.rng(), P.g_conn(), P.g_conn(True), P.proper_nonchain_module()))

print("\n§G  CONTROLS (each must FIRE)")
P = attach_low(20, 8); N, R, i = 20, 8, 14; a = i - R - 1
PB = Fr(F(i) * F(N - i), F(N + 1)); PA = Fr(F(R) * F(N - R), F(N + 1))
wrong = PB + (PA * PB - PA * PB) / (R + 1 - PA)
chk(P.before(i, i - 1) != wrong, "NEGATIVE CONTROL: closed form with P(A∩B) replaced by P(A)P(B) is REJECTED by the exact count -> CAUGHT")
b, _ = cert(Poset(12, fibrel(12)))
chk(b >= third, "CONTROL: probe-B certificate on bare F_12 CERTIFIES (%s) -> the no-certificate negative is not an instrument artefact" % b)
Q = Poset(6, [(0, 1), (2, 3), (4, 5)])   # 2+2 + C_2: W={0,1,2,3} is a module
taus = [t for t in permutations((0, 1, 2, 3)) if t.index(0) < t.index(1) and t.index(2) < t.index(3)]
base = [(p_, q_) for p_ in range(6) for q_ in Q.above[p_]]
chk(len({Poset(6, base + [(t[j], t[j + 1]) for j in range(3)]).e() for t in taus}) == 1,
    "CONTROL: the uniform-law detector FIRES on 2+2 inside 2+2+C_2 (module embedding)")
Hn = Poset(4 + 8, W + hub_rel(4, 8, [a1, a2, b2], 4))
chk(Hn.proper_nonchain_module() is not None and Hn.proper_nonchain_module()[0] == "nonchain",
    "CONTROL: module detector finds the single hub's non-chain module")

print("\nSUMMARY: %d failed checks %s" % (len(FAIL), FAIL))
