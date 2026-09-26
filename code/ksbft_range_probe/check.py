"""check.py -- controls and exact re-derivation for probe.cpp (mg-2912).

  python3 check.py controls          # positive/negative controls (needs ./probe)
  python3 check.py rederive FILES..  # re-derive every record in probe .jsonl files

Exit status is non-zero on any disagreement.
"""
import json
import random
import subprocess
import sys
from fractions import Fraction
from math import factorial

import exact

HERE = __file__.rsplit("/", 1)[0] or "."
FAIL = []


def expect(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (("  " + detail) if detail else ""))
    if not ok:
        FAIL.append(name)


def closure(n, rel):
    down = [0] * n
    for (a, b) in rel:  # a < b
        down[b] |= 1 << a
    changed = True
    while changed:
        changed = False
        for v in range(n):
            new = down[v]
            for u in range(n):
                if down[v] >> u & 1:
                    new |= down[u]
            if new != down[v]:
                down[v] = new
                changed = True
    return down


def random_poset(n, p, rnd):
    rel = [(a, b) for a in range(n) for b in range(a + 1, n) if rnd.random() < p]
    down = closure(n, rel)
    perm = list(range(n))
    rnd.shuffle(perm)  # destroy the natural labelling
    inv = {perm[i]: i for i in range(n)}
    nd = [0] * n
    for v in range(n):
        m = 0
        for u in range(n):
            if down[v] >> u & 1:
                m |= 1 << inv[u]
        nd[inv[v]] = m
    return nd


def run_probe_one(posets):
    inp = "".join(f"{len(d)} " + " ".join(map(str, d)) + "\n" for d in posets)
    out = subprocess.run([HERE + "/probe", "one"], input=inp, capture_output=True, text=True, check=True)
    return [json.loads(l) for l in out.stdout.splitlines()]


def fib(k):
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def fib_poset(N):
    # elements 0..N-1, i < j iff j - i >= 2
    return [sum(1 << i for i in range(j - 1)) for j in range(N)]


def compare_record(rec, res, tag, quiet=False):
    e = int(rec["e"])
    ok = e == res["e"]
    ok &= Fraction(int(rec["delta_num"]), e) == res["delta"]
    ok &= Fraction(int(rec["M_num"]), e) == res["M"]
    ok &= rec["pi"] == res["pi"]
    ok &= [Fraction(int(s), e) for s in rec["S"]] == res["h"]
    x, y = rec["pair"]
    ok &= (x, y) in res["pairs"] and rec["npairs"] == len(res["pairs"])
    if not ok and not quiet:
        expect(tag, False, json.dumps(rec)[:300])
    return ok


def controls():
    # C0: the (2+1) poset: a<b, c incomparable to both.  delta = 1/3 exactly.
    r = exact.analyse(closure(3, [(0, 1)]), "brute")
    expect("C0 (2+1) delta = 1/3", r["delta"] == Fraction(1, 3), str(r["delta"]))
    expect("C0 (2+1) M = 1/3", r["M"] == Fraction(1, 3), str(r["M"]))
    # C1: antichain e = n!, delta = 1/2, M = (n-1)/2
    for n in range(1, 8):
        r = exact.analyse([0] * n, "dp")
        expect(f"C1 antichain n={n} e=n!", r["e"] == factorial(n))
        if n >= 2:
            expect(f"C1 antichain n={n} M=(n-1)/2", r["M"] == Fraction(n - 1, 2))
    # C2: KSBFT_v7 p.12 formula delta(F_m; x_i, x_{i+1}) = F_{m+i+1} F_{m-i} / F_{2m+2}
    for m in range(1, 8):
        N = 2 * m + 1
        down = fib_poset(N)
        r = exact.analyse(down, "dp")
        ok = True
        for i in range(-m, m):
            got = exact.bal(r, down, i + m, i + m + 1)
            want = Fraction(fib(m + i + 1) * fib(m - i), fib(2 * m + 2))
            ok &= got == want
        expect(f"C2 paper p.12 adjacent-pair formula F_{m} (all i)", ok)
    # C3: brute force vs DP vs probe.cpp on random unlabelled-order posets
    rnd = random.Random(2912)
    sample = [random_poset(rnd.randint(2, 8), rnd.choice([0.15, 0.3, 0.5]), rnd) for _ in range(300)]
    cres = run_probe_one(sample)
    agree_bd = agree_cp = 0
    for d, rec in zip(sample, cres):
        rb = exact.analyse(d, "brute")
        rd = exact.analyse(d, "dp")
        if all(rb[k] == rd[k] for k in ("e", "delta", "M", "h", "pi", "pairs")):
            agree_bd += 1
        if rb["delta"] is None:
            agree_cp += int(rec["delta_num"]) == -1
            continue
        if compare_record(rec, rb, "C3 probe vs brute"):
            agree_cp += 1
    expect("C3 brute == dp on 300 random posets", agree_bd == 300, f"{agree_bd}/300")
    expect("C3 probe.cpp == brute on 300 random posets", agree_cp == 300, f"{agree_cp}/300")
    # C4 NEGATIVE: the comparison must be able to fail -- perturb one record
    rec = dict(cres[0])
    rec["delta_num"] = str(int(rec["delta_num"]) + 1)
    rb = exact.analyse(sample[0], "brute")
    fired = not compare_record(rec, rb, "C4", quiet=True)
    expect("C4 NEGATIVE CONTROL: planted wrong delta (numerator + 1) " + ("CAUGHT" if fired else "MISSED"), fired)
    # C5: exact irrational comparison
    expect("C5 1/3 > C_BFT", exact.delta_minus_cbft_gt(Fraction(1, 3)))
    expect("C5 0.2763 < C_BFT", not exact.delta_minus_cbft_gt(Fraction(2763, 10000)))
    expect("C5 0.2764 > C_BFT", exact.delta_minus_cbft_gt(Fraction(2764, 10000)))

    # C6: ordinal-sum identity sum P_n x^n = 1/(1 - sum I_n x^n), I_n = #connected-G posets
    # (I_1 = 1, the singleton), against A000112, using the enumerator's own counts.
    import os, re
    f = os.path.join(HERE, "out", "summary_all_n11.txt")
    if os.path.exists(f):
        P, I = {0: 1}, {}
        for line in open(f):
            m = re.match(r"^n=(\d+) posets\(pi<=99\)=(\d+) OEIS_A000112=(\d+) connected-G=(\d+)", line)
            if m:
                n = int(m.group(1))
                expect(f"C6 n={n} count == OEIS A000112", m.group(2) == m.group(3))
                P[n] = int(m.group(2)); I[n] = 1 if n == 1 else int(m.group(4))
        ok = all(P[n] == sum(I[k] * P[n - k] for k in range(1, n + 1)) for n in I)
        expect(f"C6 ordinal-sum identity holds for n <= {max(I)}", ok)
    else:
        expect("C6 needs out/summary_all_n11.txt", False)


def rederive(files):
    n_ok = n = 0
    seen = set()
    for f in files:
        for line in open(f):
            o = json.loads(line)
            rec = o["rec"]
            key = tuple(rec["down"])
            if key in seen:
                continue
            seen.add(key)
            n += 1
            res = exact.analyse(rec["down"], "dp")
            if compare_record(rec, res, f"rederive {f}"):
                n_ok += 1
    expect(f"rederive: {n_ok}/{n} distinct extreme records agree exactly", n_ok == n)


if __name__ == "__main__":
    if sys.argv[1] == "controls":
        controls()
    else:
        rederive(sys.argv[2:])
    print("FAILURES:", len(FAIL))
    sys.exit(1 if FAIL else 0)
