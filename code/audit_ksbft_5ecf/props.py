"""props.py (audit mg-5ecf): Prop 2.4, the n = 10 obstruction structure, and Claim K on bounded-range witnesses.

1. Prop 2.4, exhaustive over every interval order n <= 6 and every dominance-respecting linear extension L:
   (all down(z) are L-prefixes) <=> (no strict containment y > x with y before x), and dually for up-sets.
   CONTROL: the same test without the dominance restriction must find a failure of the '<=' direction.
2. n = 10 obstructions: every bad poset has 1..3 intervals with r - l >= 2 and ALL others with r - l <= 1.
3. Claim K (exists L with every consecutive incomparable step having >= 2 separators?) on the interval-order
   witnesses of this programme: P9, Q_0, Q_4, A14, attach_low(F_12,8), attach_low(F_16,10), F_12;
   and on a targeted family: the unit staircase [1,1][1,2][2,3]..[k,k] plus 1..3 long intervals, n = 10..13.
"""
import itertools, os, sys
from multiprocessing import Pool
import eng
import witnesses as W


def prefix_props(P, iv, perm):
    n = P[0]
    dn = eng.downs(P)
    up = P[1]
    pos = {v: i for i, v in enumerate(perm)}
    def is_prefix(mask):
        k = bin(mask).count("1")
        return all(mask >> perm[i] & 1 for i in range(k))
    def is_suffix(mask):
        k = bin(mask).count("1")
        return all(mask >> perm[n - 1 - i] & 1 for i in range(k))
    dpre = all(is_prefix(dn[z]) for z in range(n))
    usuf = all(is_suffix(up[z]) for z in range(n))
    strict = [(y, x) for y in range(n) for x in range(n)
              if iv[y][0] < iv[x][0] and iv[x][1] < iv[y][1]]
    cond_d = not any(pos[y] < pos[x] for y, x in strict)
    cond_u = not any(pos[x] < pos[y] for y, x in strict)
    return dpre == cond_d, usuf == cond_u


def part1():
    bad = 0
    ctrl = 0
    tested = 0
    for n in range(2, 7):
        for iv in eng.gen(n):
            P = eng.from_intervals(iv)
            pred = eng.dominance_pred(P)
            up = P[1]
            for perm in itertools.permutations(range(n)):
                pos = {v: i for i, v in enumerate(perm)}
                if any(pos[x] > pos[y] for x in range(n) for y in range(n) if up[x] >> y & 1):
                    continue
                dom = all(pos[x] < pos[y] for y in range(n) for x in range(n) if pred[y] >> x & 1)
                a, b = prefix_props(P, iv, perm)
                if dom:
                    tested += 1
                    bad += (not a) + (not b)
                else:
                    ctrl += (not a) + (not b)
    print(f"1. Prop 2.4: {tested} (poset, dominance-L) cases n <= 6, failures = {bad}; "
          f"CONTROL non-dominance L failures = {ctrl} (must be > 0)")
    return bad == 0 and ctrl > 0


def w10(iv):
    P = eng.from_intervals(iv)
    if all(not eng.inc(P, a, b) for a in range(10) for b in range(10)):
        return None                     # the 10-chain: K excludes chains
    if eng.badL(P):
        return iv
    return None


def part2():
    cores = int(os.environ.get("POGO_WORKER_CORES", "1"))
    with Pool(cores) as pool:
        res = [r for r in pool.map(w10, eng.gen(10), chunksize=256) if r]
    ok = True
    longs = set()
    for iv in res:
        k = sum(1 for l, r in iv if r - l >= 2)
        longs.add(k)
        if not 1 <= k <= 3:
            ok = False
    print(f"2. n=10 bad posets: {len(res)}; #intervals with r-l >= 2: {sorted(longs)}; "
          f"all others r-l <= 1 (tautological given the split) -> shape claim holds: {ok}")
    mx = max(max(r - l for l, r in iv) for iv in res)
    print(f"   max canonical length among them: {mx}")
    return ok


def part3():
    ok = True
    for name, P in W.build():
        if eng.has_2p2(P):
            continue
        r = eng.badL(P)
        rd = eng.badL(P, dominance=True) if r else None
        print(f"3. {name}: n={P[0]} bad L exists (Claim K fails) = {bool(r)}; dominance-respecting = {bool(rd)}")
        sys.stdout.flush()
    fam = 0
    badfam = 0
    for k in range(4, 12):
        stair = [(1, 1)] + [(i, i + 1) for i in range(1, k)] + [(k, k)]
        pts = range(1, k + 1)
        longs = [(a, b) for a in pts for b in pts if b - a >= 2]
        for t in (1, 2, 3):
            if len(stair) + t < 10 or len(stair) + t > 13:
                continue
            for extra in itertools.combinations(longs, t):
                iv = stair + list(extra)
                P = eng.from_intervals(iv)
                fam += 1
                if eng.badL(P, dominance=True):
                    badfam += 1
    print(f"3'. staircase + 1..3 long intervals, n = 10..13: {fam} posets, with a bad dominance-L: {badfam}")
    return ok


if __name__ == "__main__":
    a = part1()
    b = part2()
    part3()
    print("RESULT", "pass" if a and b else "FAILURE")
