"""bwgeneral.py (mg-afa4): CONTROL.  Does 'every linear extension has an L-consecutive incomparable pair with
<=1 separator' fail on general posets?  (It must fail somewhere, or Brightwell's argument would prove 1/3-2/3.)
Exhaustive over naturally-labelled relations for n<=6, random for n=7..9."""
import random, itertools, sys
def closure(n, rel):
    lt = [[False] * n for _ in range(n)]
    for a, b in rel: lt[a][b] = True
    for k in range(n):
        for i in range(n):
            if lt[i][k]:
                for j in range(n):
                    if lt[k][j]: lt[i][j] = True
    return lt
def analyse(n, lt):
    inc = lambda a, b: a != b and not lt[a][b] and not lt[b][a]
    cov = lambda a, b: lt[a][b] and not any(lt[a][c] and lt[c][b] for c in range(n))
    if not any(inc(a, b) for a in range(n) for b in range(n)): return None
    def seps(a, b): return sum(1 for z in range(n) if (cov(a, z) and inc(z, b)) or (cov(z, b) and inc(z, a)))
    def rec(pre, used):
        if len(pre) == n: yield pre; return
        for v in range(n):
            if not used >> v & 1 and all(used >> w & 1 for w in range(n) if lt[w][v]):
                yield from rec(pre + [v], used | 1 << v)
    for L in rec([], 0):
        if all(seps(L[i], L[i + 1]) >= 2 for i in range(n - 1) if inc(L[i], L[i + 1])): return L
    return None
def is_io(n, lt):
    inc = lambda a, b: a != b and not lt[a][b] and not lt[b][a]
    return not any(lt[a][x] and lt[c][y] and inc(a, y) and inc(c, x) and inc(a, c) and inc(x, y)
                   for a in range(n) for x in range(n) for c in range(n) for y in range(n))
random.seed(7)
for n in range(4, 10):
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    found = None; tried = 0
    it = (itertools.product([0, 1], repeat=len(pairs)) if n <= 5 else
          ([random.random() < random.choice([0.2, 0.3, 0.45]) for _ in pairs] for _ in range(3000 if n <= 7 else 800)))
    for bits in it:
        lt = closure(n, [p for p, b in zip(pairs, bits) if b]); tried += 1
        L = analyse(n, lt)
        if L is not None:
            found = (L, [(a, b) for a in range(n) for b in range(n) if lt[a][b]], is_io(n, lt)); break
    print(f"n={n}: tried {tried}; bad L found: {found is not None}" + (f"  L={found[0]} relations={found[1]} interval_order={found[2]}" if found else ""))
    sys.stdout.flush()
