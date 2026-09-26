"""sl.py (audit mg-5ecf): KSBFT-T sec. 3.4 -- do the Brightwell-bad dominance-respecting L survive the Swap-Ladder
constraints? Own implementation from the mg-ce69 Thm 1.4 statement:
  nested (x; b): x || b, D(x) <= D(b). W = up-closure of b minus up-closure of x (b included).
  chain bottom b_0 = b, b_{i+1} = the unique minimal element of W - {b_0..b_i} (stop if not unique / none).
  (SL1) b before x  =>  b_m before x.     (SL2) W a chain (chain bottom exhausts W)  =>  x before b.
  Duals: the same in the dual poset with L reversed.
Every bad dominance-respecting L of every bad interval order at n = 9, 10 is enumerated and filtered.
Author's figures: n = 9: 2 of 2 posets survive; n = 10: 16 of 24 posets, 20 of 29 L survive.
CONTROL: on the n=9 obstructions, a planted violating order (move x after b for an SL2 pair) must be rejected.
"""
import os, sys
from multiprocessing import Pool
import eng


def dual(P):
    return P[0], eng.downs(P)


def constraints(P):
    """returns list of (kind, x, b, bm) in P's orientation."""
    n, up = P
    dn = eng.downs(P)
    out = []
    for x in range(n):
        for b in range(n):
            if not eng.inc(P, x, b) or dn[x] & ~dn[b]:
                continue
            W = (up[b] | 1 << b) & ~(up[x] | 1 << x)
            chain = [b]
            rest = W & ~(1 << b)
            while rest:
                mins = [z for z in range(n) if rest >> z & 1 and not (eng.downs(P)[z] & rest)]
                if len(mins) != 1:
                    break
                chain.append(mins[0])
                rest &= ~(1 << mins[0])
            out.append(("SL1", x, b, chain[-1]))
            if rest == 0:
                out.append(("SL2", x, b, None))
    return out


def ok(cons, pos, rev):
    for kind, x, b, bm in cons:
        before = (lambda u, v: pos[u] > pos[v]) if rev else (lambda u, v: pos[u] < pos[v])
        if kind == "SL1" and before(b, x) and not before(bm, x):
            return False
        if kind == "SL2" and not before(x, b):
            return False
    return True


def all_bad_dom(P):
    n, up = P
    dn = eng.downs(P)
    S = eng.seps(P)
    pred = eng.dominance_pred(P)
    need = [dn[x] | pred[x] for x in range(n)]
    out = []

    def rec(I, seq):
        if len(seq) == n:
            out.append(tuple(seq))
            return
        for x in range(n):
            if I >> x & 1 or need[x] & ~I:
                continue
            if seq and not eng.lt(P, seq[-1], x) and S[seq[-1]][x] < 2:
                continue
            rec(I | 1 << x, seq + [x])
    rec(0, [])
    return out


def work(iv):
    P = eng.from_intervals(iv)
    if all(not eng.inc(P, a, b) for a in range(P[0]) for b in range(P[0])):
        return None
    if not eng.badL(P, dominance=True):
        return None
    Ls = all_bad_dom(P)
    cp = constraints(P)
    cd = constraints(dual(P))
    surv = [L for L in Ls if ok(cp, {v: i for i, v in enumerate(L)}, False)
            and ok(cd, {v: i for i, v in enumerate(L)}, True)]
    return iv, len(Ls), len(surv), surv[:1], cp


def main():
    cores = int(os.environ.get("POGO_WORKER_CORES", "1"))
    with Pool(cores) as pool:
        for n in (9, 10):
            R = [r for r in pool.map(work, eng.gen(n), chunksize=256) if r]
            nl = sum(r[1] for r in R)
            sp = sum(1 for r in R if r[2])
            sl = sum(r[2] for r in R)
            print(f"n={n}: posets with a bad dominance-L: {len(R)}, bad dominance-L total: {nl}; "
                  f"surviving SL1/SL2 + duals: {sp} posets, {sl} L")
            if n == 9:
                for iv, a, b, s, cp in R:
                    L = s[0] if s else None
                    print(f"   {''.join(f'[{l},{r}]' for l, r in iv)}: bad L {a}, surviving {b}; "
                          f"e.g. {' '.join(f'[{iv[x][0]},{iv[x][1]}]' for x in L) if L else '-'}")
                    # control: violate one SL2 constraint
                    sl2 = [c for c in cp if c[0] == "SL2"]
                    if L and sl2:
                        _, x, bb, _ = sl2[0]
                        pos = {v: i for i, v in enumerate(L)}
                        pos[x], pos[bb] = max(pos[x], pos[bb]) + 0.5, min(pos[x], pos[bb])
                        print(f"      CONTROL planted SL2 violation rejected: {not ok(cp, pos, False)}")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
