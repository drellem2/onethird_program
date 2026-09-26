"""misc.py (audit mg-5ecf): two small checks.

1. KSBFT-T sec. 4 'down-twin classes': for l(x) = l(y), r(x) < r(y), if Z = {z : r(x) < l(z) <= r(y)} has a unique
   minimal element b1, then P[y < b1] = 2 P[y < x]. Every interval order n <= 8, exact.
   CONTROL: the same identity for pairs with l(x) < l(y) (not down-twins) must fail somewhere.
2. KSBFT-T sec. 0 item 2 says the semiorder count 'each element separates at most one pair from above' is
   EQUIVALENT to 'every down(z) is an L-prefix'. Test, for every linear extension L of every interval order
   n <= 6: (A) every z separates <= 1 L-consecutive pair from above; (B) every down(z) is an L-prefix.
   B => A is immediate; report counterexamples to A => B.
"""
import itertools
import eng


def part1():
    tested = viol = ctrl = 0
    for n in range(2, 9):
        for iv in eng.gen(n):
            P = eng.from_intervals(iv)
            e, N = eng.laws(P)
            dn = eng.downs(P)
            for x in range(n):
                for y in range(n):
                    if x == y or not eng.inc(P, x, y) or not iv[x][0] <= iv[y][0] or not iv[x][1] < iv[y][1]:
                        continue
                    Z = [z for z in range(n) if iv[x][1] < iv[z][0] <= iv[y][1]]
                    Zm = sum(1 << z for z in Z)
                    mins = [z for z in Z if not dn[z] & Zm]
                    if len(mins) != 1:
                        continue
                    b1 = mins[0]
                    holds = N[y][b1] == 2 * N[y][x]
                    if iv[x][0] == iv[y][0]:
                        tested += 1
                        viol += not holds
                    else:
                        ctrl += not holds
    print(f"1. Doubling in interval form: {tested} down-twin pairs n <= 8, violations = {viol}; "
          f"CONTROL (l(x) < l(y)) failures = {ctrl} (must be > 0)")


def part2():
    AnotB = 0
    tot = 0
    ex = None
    domAnotB = 0
    exd = None
    for n in range(2, 7):
        for iv in eng.gen(n):
            P = eng.from_intervals(iv)
            dn = eng.downs(P)
            up = P[1]
            cov = eng.covers(P)
            pred = eng.dominance_pred(P)
            for perm in itertools.permutations(range(n)):
                pos = {v: i for i, v in enumerate(perm)}
                if any(pos[a] > pos[b] for a in range(n) for b in range(n) if up[a] >> b & 1):
                    continue
                tot += 1
                A = all(sum(1 for a, b in zip(perm, perm[1:]) if eng.inc(P, a, b) and cov[a] >> z & 1 and eng.inc(P, z, b)) <= 1
                        for z in range(n))
                B = all(all(dn[z] >> perm[i] & 1 for i in range(bin(dn[z]).count("1"))) for z in range(n))
                if A and not B:
                    AnotB += 1
                    if ex is None:
                        ex = (iv, [iv[v] for v in perm])
                    if all(pos[a] < pos[b] for b in range(n) for a in range(n) if pred[b] >> a & 1):
                        domAnotB += 1
                        if exd is None:
                            exd = (iv, [iv[v] for v in perm])
    print(f"2. separation-count vs prefix: {tot} (P, L) with n <= 6; A holds but B fails in {AnotB}; example {ex}")
    print(f"   restricted to dominance-respecting L: A holds but B fails in {domAnotB}; example {exd}")


if __name__ == "__main__":
    part1()
    part2()
