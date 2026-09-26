"""randprime.py (mg-cfba): Nested Balance on random PRIME, indecomposable posets of range >= 8 (doc sec. 2.2).
Sampler: natural labelling 0..n-1; i<j forced when j-i > w; for 0 < j-i <= w the relation is added with prob q;
transitive closure; keep if range >= 8, incomparability graph connected, prime (no module of size 2..n-1).
Reports the NB flag, delta, deltaN and the gap delta - deltaN (the 'price of nesting')."""
import random, sys
from fam import closure, run, rng, connected, is_prime, fmt

rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
NS = int(sys.argv[2]) if len(sys.argv) > 2 else 300
kept = []
tries = 0
while len(kept) < NS:
    tries += 1
    n = rnd.randint(14, 26); w = rnd.randint(6, 12); q = rnd.choice([0.2, 0.35, 0.5, 0.65])
    dn = [0] * n
    for j in range(n):
        for i in range(j):
            if j - i > w or rnd.random() < q:
                dn[j] |= 1 << i
    dn = closure(dn)
    if rng(dn) < 8 or rng(dn) > 14 or not connected(dn) or not is_prime(dn):
        continue
    kept.append(dn)
res = run(kept)
fails = [d for d, r in zip(kept, res) if r["flag"] != "NB"]
withnon = sum(1 for r in res if r["nnon"] > 0)
gaps = sorted(r["delta"] - r["deltaN"] for r in res)
print(f"seed={sys.argv[1] if len(sys.argv) > 1 else 1}: sampled {len(kept)} prime indecomposable range 8..14 posets (n 14..26) from {tries} draws")
print(f"  with >=1 non-nested incomparable pair: {withnon}; NB failures: {len(fails)}; 1/3-2/3 failures: {sum(r['flag']=='CEX_1323' for r in res)}")
print(f"  min deltaN = {min(r['deltaN'] for r in res):.5f}; min delta = {min(r['delta'] for r in res):.5f}")
print(f"  price of nesting delta-deltaN: max {gaps[-1]:.5f}, #>0: {sum(g > 1e-12 for g in gaps)}")
print(f"  mean fraction of balanced pairs that are nested: {sum(r['nbalN']/max(1,r['nbal']) for r in res)/len(res):.4f}")
for d in fails[:5]:
    print("  NB-FAIL:", fmt(d))
