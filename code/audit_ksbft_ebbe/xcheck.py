"""xcheck.py (audit mg-ebbe): aud.c vs explicit enumeration of linear extensions (itertools.permutations),
on every poset n<=6 and 400 random census posets n=7, comparing e, d, dN, dP, dD, nn.  Exit 1 on mismatch.
CONTROL: a planted classifier (primal := down-sets EQUAL) must produce mismatches in dP.
Usage: python3 xcheck.py p1.txt .. p7.txt  (census files); needs ./aud built."""
import sys, random, subprocess
from itertools import permutations
from census import parse, ups

def brute(dn, planted=False):
    n = len(dn); up = ups(dn); e = 0; B = {}
    for perm in permutations(range(n)):
        pos = [0] * n
        for i, v in enumerate(perm): pos[v] = i
        if any(pos[j] < pos[i] for i in range(n) for j in range(n) if dn[i] >> j & 1): continue
        e += 1
        for a in range(n):
            for b in range(a + 1, n):
                if pos[a] < pos[b]: B[a, b] = B.get((a, b), 0) + 1
    d = dN = dP = dD = nn = 0
    for a in range(n):
        for b in range(a + 1, n):
            if dn[a] >> b & 1 or dn[b] >> a & 1: continue
            x = B.get((a, b), 0); m = min(x, e - x)
            prim = (dn[a] == dn[b]) if planted else (dn[a] & ~dn[b] == 0 or dn[b] & ~dn[a] == 0)
            dual = up[a] & ~up[b] == 0 or up[b] & ~up[a] == 0
            d = max(d, m)
            if prim or dual: dN = max(dN, m)
            else: nn += 1
            if prim: dP = max(dP, m)
            if dual: dD = max(dD, m)
    return dict(e=e, d=d, dN=dN, dP=dP, dD=dD, nn=nn)

pos = []
for f in sys.argv[1:]:
    L = [l.strip() for l in open(f) if l.strip()]
    if L and int(L[0].split()[0]) == 7:
        random.seed(20260926); L = random.sample(L, 400)
    pos += L
out = subprocess.run(["./aud"], input="\n".join(pos) + "\n", capture_output=True, text=True).stdout.splitlines()
bad = ctl = 0
for s, line in zip(pos, out):
    kv = dict(t.split("=") for t in line.split(" | ")[1].split())
    dn = parse(s); b = brute(dn)
    if any(int(kv[k]) != b[k] for k in b): bad += 1; print("MISMATCH", s, kv, b)
    if brute(dn, planted=True)["dP"] != int(kv["dP"]): ctl += 1
print(f"xcheck: {len(pos)} posets, {bad} mismatches; CONTROL planted primal-classifier differs on {ctl} posets "
      f"({'FIRES' if ctl else 'DID NOT FIRE'})")
sys.exit(1 if bad or not ctl or len(out) != len(pos) else 0)
