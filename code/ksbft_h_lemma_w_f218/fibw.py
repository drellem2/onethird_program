"""fibw.py (mg-f218) -- does the 1/(D+1) of Lemma W survive near C_BFT?

Family G(m, a, b): the Fibonacci poset F_m on x_{-m..m} (x_i < x_j iff
j - i >= 2) plus ONE element w with
    down(w) = {x_i : i <= -a},   up(w) = {x_i : i >= b},
so w is incomparable to x_{-a+1}, ..., x_{b-1}.  With b >= 2 and a >= 0 the
element w lies in N(x, y) for the central triple (x, y, z) = (x_0, x_1, x_2)
(w is not below y = x_1 and x = x_0 is not below w).  Transitivity holds
because j - i >= a + b >= 2 for i <= -a < b <= j.

For each member it prints, EXACTLY (fractions.Fraction, DP over order ideals):
  whether (x_0, x_1, x_2) is still a BFT triple (heights compared exactly),
  p = P[y < x], p' = P[z < y], ratio = P[f(x)-f(y) >= 2] / p, the range pi,
  and pi * ratio.  Lemma W (PROVEN) says ratio >= 1/(pi(w)+1).
POSITIVE CONTROL: with w removed (plain F_m) P[f(x)-f(y) >= 2] must be 0
(N(x,y) is empty in F_m: Lemma 3.2(iii) holds there), and p must equal the
paper's delta(F_m; x_0, x_1) = F_{m+1} F_m / F_{2m+2} (p.12)."""
from fractions import Fraction as Fr
import sys

def analyse(n, down):
    full = (1 << n) - 1
    up = [0] * n
    for j in range(n):
        for i in range(n):
            if down[j] >> i & 1: up[i] |= 1 << j
    inc = [full & ~(down[i] | up[i] | (1 << i)) for i in range(n)]
    pi = max(bin(v).count('1') for v in inc)
    # forward counts N and backward counts S over reachable ideals
    order, N = [0], {0: 1}
    q = 0
    while q < len(order):
        I = order[q]; q += 1
        for x in range(n):
            if not I >> x & 1 and down[x] & ~I == 0:
                J = I | 1 << x
                if J not in N: N[J] = 0; order.append(J)
                N[J] += N[I]
    S = {full: 1}
    for I in reversed(order):
        if I == full: continue
        S[I] = sum(S[I | 1 << x] for x in range(n) if not I >> x & 1 and down[x] & ~I == 0)
    e = N[full]
    def avail(I):
        return [x for x in range(n) if not I >> x & 1 and down[x] & ~I == 0]
    h = [Fr(0)] * n
    before = {}   # before[(a,b)] = #ext with a before b
    adj = {}      # adj[(a,b)] = #ext with b immediately after a
    for I in order:
        if I == full: continue
        k = bin(I).count('1') + 1
        for a in avail(I):
            J = I | 1 << a
            cnt = N[I] * S[J]
            h[a] += Fr(cnt * k, e)
            rest = inc[a] & ~I
            for b in range(n):
                if rest >> b & 1:
                    before[(a, b)] = before.get((a, b), 0) + cnt
            for b in avail(J):
                if inc[a] >> b & 1:
                    adj[(a, b)] = adj.get((a, b), 0) + N[I] * S[J | 1 << b]
    return e, h, before, adj, pi, inc

def fib(k):
    a, b = 0, 1
    for _ in range(k): a, b = b, a + b
    return a

def build(m, a, b, with_w=True):
    idx = {i: i + m for i in range(-m, m + 1)}
    n = 2 * m + 1 + (1 if with_w else 0)
    down = [0] * n
    for j in range(-m, m + 1):
        for i in range(-m, m + 1):
            if j - i >= 2: down[idx[j]] |= 1 << idx[i]
    if with_w:
        W = n - 1
        for i in range(-m, m + 1):
            if i <= -a: down[W] |= 1 << idx[i]
            if i >= b: down[idx[i]] |= 1 << W
        # transitive closure (w's down-set is already an ideal)
        for _ in range(n):
            for j in range(n):
                s = down[j]
                for i in range(n):
                    if s >> i & 1: s |= down[i]
                down[j] = s
    return n, down, idx

def report(m, a, b, with_w=True):
    n, down, idx = build(m, a, b, with_w)
    e, h, before, adj, pi, inc = analyse(n, down)
    x, y, z = idx[0], idx[1], idx[2]
    p = Fr(before.get((y, x), 0), e)
    pp = Fr(before.get((z, y), 0), e)
    gap2 = Fr(before.get((y, x), 0) - adj.get((y, x), 0), e)
    bft = h[x] <= h[y] <= h[z] <= h[x] + 2
    ratio = gap2 / p
    piw = bin(inc[n - 1]).count('1') if with_w else 0
    delta = max(min(Fr(v, e), 1 - Fr(v, e)) for (u, t), v in before.items() if u < t)
    return dict(n=n, pi=pi, piw=piw, bft=bft, p=p, pp=pp, gap2=gap2, ratio=ratio, delta=delta)

def _main():
    print("== positive control: plain F_m, central pair (x_0, x_1)")
    for m in (2, 4, 6):
        r = report(m, 0, 0, with_w=False)
        paper = Fr(fib(m + 1) * fib(m), fib(2 * m + 2))
        print(f"m={m} P[gap>=2]={r['gap2']} p={r['p']} paper={paper} match={r['p']==paper} bft={r['bft']}")
    print("== G(m,a,b): F_m plus w with down(w)={x_i: i<=-a}, up(w)={x_i: i>=b}")
    print("m a b | pi pi(w) BFT(x0,x1,x2) | p p' max(p,p') | ratio=P[gap>=2]/p  (pi(w)+1)*ratio | delta(P)")
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    for a in range(0, m):
        for b in range(2, m):
            r = report(m, a, b)
            print(f"{m} {a} {b} | {r['pi']} {r['piw']} {r['bft']} | {float(r['p']):.4f} {float(r['pp']):.4f} {float(max(r['p'],r['pp'])):.4f}"
                  f" | {float(r['ratio']):.4f} {float((r['piw']+1)*r['ratio']):.4f} | {float(r['delta']):.4f}")

def scan(m, a, b):
    """All Case-D BFT triples (x,y,z) of G(m,a,b) with N(x,y) nonempty;
    returns the one minimising ratio, and the one minimising max(p,p')."""
    n, down, idx = build(m, a, b)
    e, h, before, adj, pi, inc = analyse(n, down)
    up = [0] * n
    for j in range(n):
        for i in range(n):
            if down[j] >> i & 1: up[i] |= 1 << j
    best = None
    for x in range(n):
        for y in range(n):
            if not inc[x] >> y & 1: continue
            Nxy = [w for w in range(n) if w not in (x, y) and not down[y] >> w & 1 and not up[x] >> w & 1]
            if not Nxy: continue
            piN = max(bin(inc[w]).count('1') for w in Nxy)
            for z in range(n):
                if not (up[x] >> z & 1 and inc[y] >> z & 1): continue
                if not (h[x] <= h[y] <= h[z] <= h[x] + 2): continue
                p = Fr(before[(y, x)], e); pp = Fr(before[(z, y)], e)
                g2 = Fr(before[(y, x)] - adj.get((y, x), 0), e)
                r = g2 / p
                key = (r * (piN + 1), max(p, pp))
                if best is None or key < best[0]:
                    best = (key, (x, y, z), piN, p, pp, r)
    return pi, best

def scan_main(m):
    print(f"== scan: every Case-D BFT triple with N(x,y) nonempty in G({m},a,b); the one minimising (pi_N+1)*ratio")
    print("a b | pi | triple(labels; w = last) pi_N | p p' max | ratio (pi_N+1)*ratio")
    for a in range(1, m):
        for b in range(2, m):
            pi, best = scan(m, a, b)
            if best is None: print(f"{a} {b} | {pi} | none"); continue
            (k, mx), t, piN, p, pp, r = best
            print(f"{a} {b} | {pi} | {t} {piN} | {float(p):.4f} {float(pp):.4f} {float(mx):.4f} | {float(r):.4f} {float(k):.4f}")

if __name__ == '__main__':
    _main()
    scan_main(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
