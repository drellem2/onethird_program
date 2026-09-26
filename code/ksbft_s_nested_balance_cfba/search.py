"""search.py (mg-cfba): ADVERSARIAL counterexample search for Nested Balance (instrument, doc sec. 2.3).
Beam search over naturally labelled posets on n elements: minimise deltaN (best nested pair) + small
penalty-free tie-break on -#non-nested pairs.  deltaN < 1/3 would be an NB counterexample.
Mutations: toggle one comparability i<j (i<j in the labelling), then transitive closure; reject chains and
decomposable (incomparability graph disconnected) posets.  Batch-evaluated by nb.c."""
import random, sys
from fam import closure, run, connected, fmt, rng, parse

n = int(sys.argv[1]); seed = int(sys.argv[2]); gens = int(sys.argv[3]) if len(sys.argv) > 3 else 150
START = parse(sys.argv[4]) if len(sys.argv) > 4 else None  # optional start poset (then n = its size)
if START: n = len(START)
rnd = random.Random(seed)
BEAM, KIDS = 24, 12

def rand_start():
    while True:
        dn = [0] * n
        for j in range(n):
            for i in range(j):
                if rnd.random() < 0.4: dn[j] |= 1 << i
        dn = closure(dn)
        if connected(dn): return dn

def mutate(dn):
    dn = list(dn)
    for _ in range(rnd.choice([1, 1, 2, 3])):
        i, j = sorted(rnd.sample(range(n), 2))
        if dn[j] >> i & 1:
            # remove i<j: remove from j and everything above j that got it only... rebuild from covers minus (i,j)
            rel = [(a, b) for b in range(n) for a in range(n) if dn[b] >> a & 1 and (a, b) != (i, j)]
            # drop any relation implying i<j through a chain: keep only relations not of form (i,b),(b,j)
            new = [0] * n
            for a, b in rel:
                if a == i and dn[j] >> b & 1 and b != j: continue
                if b == j and dn[a] >> i & 1 and a != i: continue
                new[b] |= 1 << a
            dn = closure(new)
            if dn[j] >> i & 1: continue
        else:
            dn[j] |= 1 << i
            dn = closure(dn)
    return dn

beam = [list(START) for _ in range(BEAM)] if START else [rand_start() for _ in range(BEAM)]
seen = set()
best = None
for g in range(gens):
    cand = beam + [mutate(rnd.choice(beam)) for _ in range(BEAM * KIDS)]
    cand = [d for d in cand if connected(d)]
    uniq = []
    for d in cand:
        k = tuple(d)
        if k in seen and d not in beam: continue
        seen.add(k); uniq.append(d)
    res = run(uniq)
    scored = sorted(zip(uniq, res), key=lambda t: (t[1]["deltaN"], -t[1]["nnon"]))
    beam = [d for d, _ in scored[:BEAM // 2]] + [d for d, _ in rnd.sample(scored[:BEAM * 3], BEAM // 2)]
    d0, r0 = scored[0]
    if best is None or r0["deltaN"] < best[1]["deltaN"]:
        best = (d0, r0)
    if r0["flag"] != "NB":
        print("NB COUNTEREXAMPLE CANDIDATE:", fmt(d0), r0); sys.stdout.flush()
d, r = best
print(f"n={n} seed={seed} gens={gens}: best deltaN={r['deltaN']:.5f} delta={r['delta']:.5f} nnon={r['nnon']} "
      f"range={rng(d)} flag={r['flag']} poset: {fmt(d)}")
