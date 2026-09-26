"""goodpair.py (audit mg-ebbe): own detector of a FIRING full-chain good pair: an incomparable ordered (a,b) with
D(a) <= D(b), U(b)\\U(a) a chain (possibly empty) and P[a<b] <= 2/3, or the same in the dual (U(a) <= U(b),
D(b)\\D(a) a chain, P[b<a] <= 2/3).  Checks the doc's N12 claim (none) with T8 as positive control."""
import subprocess, sys
from census import parse, ups
def chain(dn, S):
    v = [i for i in range(len(dn)) if S >> i & 1]
    return all(dn[a] >> b & 1 or dn[b] >> a & 1 for a in v for b in v if a < b)
def firing(s):
    dn = parse(s); up = ups(dn); n = len(dn)
    out = subprocess.run(["./aud", "-v"], input=s + "\n", capture_output=True, text=True).stdout.splitlines()
    e = int(out[-1].split("e=")[1].split()[0]); B = {}
    for l in out[:-1]:
        t = l.split(); a, b, x = int(t[1]), int(t[2]), int(t[3][2:]); B[a, b] = x; B[b, a] = e - x
    hits = []
    for (a, b), x in B.items():
        if not dn[a] & ~dn[b] and chain(dn, up[b] & ~up[a]) and 3 * x <= 2 * e: hits.append(("primal", a, b))
        if not up[a] & ~up[b] and chain(dn, dn[b] & ~dn[a]) and 3 * B[b, a] <= 2 * e: hits.append(("dual", a, b))
    return hits
n12 = firing("12 0 4 0 6 f 885 6 805 aff 5f 8af 5"); t8 = firing("8 0 0 2 6 3 e 17 5f")
print(f"N12 firing full-chain good pairs: {len(n12)} {n12}")
print(f"CONTROL T8 firing full-chain good pairs: {len(t8)} ({'FIRES' if t8 else 'DID NOT FIRE'})")
sys.exit(0 if not n12 and t8 else 1)
