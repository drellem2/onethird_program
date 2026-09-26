"""bwrules.py (mg-afa4): which extremal rule picks a Brightwell-good consecutive pair, over all L of all interval orders."""
import sys
from collections import Counter
from iolib import *
from brightwell import covers, linexts, seps
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
rules = {
 'max r(a)':            lambda a, b, i, iv: (-iv[a][1],),
 'max r(a),then max l(b)': lambda a, b, i, iv: (-iv[a][1], -iv[b][0]),
 'min l(b)':            lambda a, b, i, iv: (iv[b][0],),
 'max l(b)':            lambda a, b, i, iv: (-iv[b][0],),
 'min r(a)':            lambda a, b, i, iv: (iv[a][1],),
 'max min(r(a),r(b))':  lambda a, b, i, iv: (-min(iv[a][1], iv[b][1]),),
 'min max(l(a),l(b))':  lambda a, b, i, iv: (max(iv[a][0], iv[b][0]),),
 'max r(a)-l(b)':       lambda a, b, i, iv: (-(iv[a][1] - iv[b][0]),),
 'max overlap':         lambda a, b, i, iv: (-(min(iv[a][1], iv[b][1]) - max(iv[a][0], iv[b][0])),),
}
for n in range(3, NMAX + 1):
    fails = Counter(); ex = {}
    for iv in gen(n):
        if all(not inc(iv, a, b) for a in range(n) for b in range(n)): continue
        C = covers(iv)
        for L in linexts(iv):
            prs = [(L[i], L[i + 1], i) for i in range(n - 1) if inc(iv, L[i], L[i + 1])]
            for name, key in rules.items():
                best = min(key(a, b, i, iv) for a, b, i in prs)
                tied = [(a, b, i) for a, b, i in prs if key(a, b, i, iv) == best]
                if not all(len(seps(iv, C, a, b)) <= 1 for a, b, i in tied):
                    fails[name] += 1; ex.setdefault(name, (iv, L))
    print(f"n={n}: " + ", ".join(f"[{k}] {fails[k]}" for k in rules))
    for k in rules:
        if fails[k] and n == NMAX: print("   ", k, ex[k])
