"""general.py (mg-561a): does the interval-order reduction (Thm 2.1 + Lemma C) have a general-poset analogue?

General-poset version of the step classes (they reduce to the interval ones on interval orders):
  DOM  : a dominates a' (down(a) <= down(a'), up(a) >= up(a')): S(a',a) is empty, exact identity.
  NEST : a' is freer than a (down(a') <= down(a), up(a') <= up(a)) = interval containment.
  TRAP : neither (a 2+2-trapped pair; impossible in an interval order).
A counterexample's L puts a before a' whenever a dominates a' (Zaguia Lemma 7).  Rules (forbidden steps):
  K   : |S| <= 1                                  (Thm 2.1, PROVEN)
  KC  : K + NEST steps with |S| = 2               (Lemma C, general form)
  KCT : KC + TRAP steps with |S| = 2              (what a general two-separator lemma would also need)
  KALL: K + every step with |S| = 2               (the strongest two-separator lemma)
Population: random labelled posets (random DAG + transitive closure), n = 7..11 (chains excluded), plus the mg-afa4 control
{0<1,0<5,0<6,1<6,2<5,3<4,3<6}.  Prints the first survivors per rule.
usage: python3 general.py COUNT"""
import sys, os, random
from multiprocessing import Pool

def closure(n, LT):
    for k in range(n):
        for x in range(n):
            if LT[x][k]:
                for y in range(n):
                    if LT[k][y]: LT[x][y] = True
    return LT

def analyse(n, LT):
    INC = [[x != y and not LT[x][y] and not LT[y][x] for y in range(n)] for x in range(n)]
    COV = [[LT[x][y] and not any(LT[x][c] and LT[c][y] for c in range(n)) for y in range(n)] for x in range(n)]
    dn = [frozenset(w for w in range(n) if LT[w][v]) for v in range(n)]
    up = [frozenset(w for w in range(n) if LT[v][w]) for v in range(n)]
    cls = {}; ns = {}
    for a in range(n):
        for b in range(n):
            if not INC[a][b]: continue
            ns[(a, b)] = sum(1 for z in range(n) if (COV[a][z] and INC[z][b]) or (COV[z][b] and INC[z][a]))
            if dn[a] <= dn[b] and up[a] >= up[b]: cls[(a, b)] = 'DOM'
            elif dn[b] <= dn[a] and up[b] <= up[a]: cls[(a, b)] = 'NEST'
            else: cls[(a, b)] = 'TRAP'
    need = [sum(1 << w for w in range(n) if LT[w][v] or (INC[w][v] and cls[(w, v)] == 'DOM' and not
               (dn[w] == dn[v] and up[w] == up[v]))) for v in range(n)]
    def forb(rule, a, b):
        k = ns[(a, b)]; c = cls[(a, b)]
        if k <= 1: return True
        if rule == 'KC': return k == 2 and c == 'NEST'
        if rule == 'KCT': return k == 2 and c in ('NEST', 'TRAP')
        if rule == 'KALL': return k == 2
        return False
    res = {}
    for rule in ('K', 'KC', 'KCT', 'KALL'):
        layer = {1 << x: {x: None} for x in range(n) if need[x] == 0}; back = [layer]
        for _ in range(n - 1):
            nxt = {}
            for I, lasts in layer.items():
                for x in range(n):
                    if I >> x & 1 or need[x] & ~I: continue
                    for a in lasts:
                        if LT[a][x] or not forb(rule, a, x):
                            nxt.setdefault(I | 1 << x, {})[x] = (I, a); break
            layer = nxt; back.append(layer)
        full = (1 << n) - 1
        if full in layer:
            x = next(iter(layer[full])); I = full; seq = []
            for k in range(n - 1, -1, -1):
                seq.append(x); par = back[k][I][x]
                if par is None: break
                I, x = par
            L = list(reversed(seq))
            res[rule] = (L, [(cls[(L[i], L[i + 1])], ns[(L[i], L[i + 1])]) for i in range(n - 1) if INC[L[i]][L[i + 1]]])
        else: res[rule] = None
    return res

def job(seed):
    rnd = random.Random(seed); n = 7 + seed % 5; p = rnd.choice((0.15, 0.25, 0.35))
    LT = closure(n, [[x < y and rnd.random() < p for y in range(n)] for x in range(n)])
    if all(LT[x][y] or LT[y][x] for x in range(n) for y in range(n) if x != y): return None   # chains excluded
    return n, [(x, y) for x in range(n) for y in range(n) if LT[x][y]], analyse(n, LT)

if __name__ == '__main__':
    COUNT = int(sys.argv[1])
    n = 7; rel = [(0, 1), (0, 5), (0, 6), (1, 6), (2, 5), (3, 4), (3, 6)]
    LT = closure(n, [[(x, y) in rel for y in range(n)] for x in range(n)])
    r = analyse(n, LT)
    print("mg-afa4 control poset:", {k: (v[0] if v else None) for k, v in r.items()})
    with Pool(int(os.environ.get('POGO_WORKER_CORES', '3'))) as pool:
        out = [o for o in pool.map(job, range(COUNT), chunksize=32) if o]
    for rule in ('K', 'KC', 'KCT', 'KALL'):
        surv = [(n, rel, r[rule]) for n, rel, r in out if r[rule]]
        print(f"rule {rule}: {len(surv)} of {COUNT} random non-chain posets (n=7..11) have a surviving dominance-L")
        for n, rel, (L, st) in surv[:2]:
            print(f"   n={n} rel={rel}\n     L={L} steps(class,|S|)={st}")
