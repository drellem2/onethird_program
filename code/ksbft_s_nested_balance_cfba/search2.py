"""search2.py (mg-cfba): second adversarial NB search (instrument).  Objective (lexicographic):
(deltaN > 1/3 ?, soft, deltaN) where soft = sum of excess of nested pairs above 1/3-0.02 (nb.c col 9): pushes ALL
near-balanced nested pairs out at once.  Mutations: toggle relations (+closure), add a random element (random
down-ideal below, random filter above, consistent), delete an element.  n kept in [NMIN, NMAX].
Rejects disconnected incomparability graphs.  Prints any poset with deltaN < 1/3 (an NB counterexample)."""
import random, sys
from fam import closure, run, connected, fmt, rng, parse, upmasks, chain_pairs, pair_laws, firing_full_pairs

seed = int(sys.argv[1]); gens = int(sys.argv[2]); NMIN, NMAX = int(sys.argv[3]), int(sys.argv[4])
starts = [parse(s) for s in sys.argv[5:]]
rnd = random.Random(seed)
BEAM, KIDS = 30, 10

def rand_poset(n):
    while True:
        dn = [0] * n
        for j in range(n):
            for i in range(j):
                if rnd.random() < 0.4: dn[j] |= 1 << i
        dn = closure(dn)
        if connected(dn): return dn

def toggle(dn):
    n = len(dn); dn = list(dn)
    i, j = sorted(rnd.sample(range(n), 2))
    if dn[j] >> i & 1:
        new = [0] * n
        for b in range(n):
            for a in range(n):
                if dn[b] >> a & 1 and (a, b) != (i, j):
                    if a == i and dn[j] >> b & 1: continue
                    if b == j and dn[a] >> i & 1: continue
                    new[b] |= 1 << a
        return closure(new)
    if rnd.random() < 0.5: i, j = j, i
    dn[j] |= 1 << i
    try:
        return closure(dn)
    except AssertionError:
        return None

def add_elem(dn):
    n = len(dn); up = upmasks(dn)
    # pick a random down-set D (union of down-closures) and put new element above D, below a random filter disjoint from D
    D = 0
    for v in range(n):
        if rnd.random() < 0.3: D |= dn[v] | 1 << v
    U = 0
    for v in range(n):
        if not (D >> v & 1) and rnd.random() < 0.3:
            U |= up[v] | 1 << v
    U &= ~D
    # U must be a filter disjoint from D; D is down-closed; need nothing of U below something of D: ok since D down-closed & U∩D=∅ ... check
    for v in range(n):
        if U >> v & 1 and dn[v] & ~D & ~U and False: pass
    new = list(dn) + [D]
    for v in range(n):
        if U >> v & 1: new[v] |= 1 << n | D
    try:
        return closure(new)
    except AssertionError:
        return None

def del_elem(dn):
    n = len(dn); k = rnd.randrange(n)
    keep = [v for v in range(n) if v != k]
    idx = {v: i for i, v in enumerate(keep)}
    return [sum(1 << idx[w] for w in keep if dn[v] >> w & 1) for v in keep]

def mutate(dn):
    r = rnd.random()
    if r < 0.12 and len(dn) < NMAX: return add_elem(dn)
    if r < 0.2 and len(dn) > NMIN: return del_elem(dn)
    for _ in range(rnd.choice([1, 1, 2])):
        dn = toggle(dn)
        if dn is None: return None
    return dn

beam = [list(s) for s in starts for _ in range(BEAM // max(1, len(starts)))] or [rand_poset(rnd.randint(NMIN, NMAX)) for _ in range(BEAM)]
MODE = __import__("os").environ.get("NBKEY", "soft")
key = (lambda r: (r["pflag"] == "PNB", round(r["deltaP"], 6))) if MODE == "dP" else (lambda r: (r["flag"] == "NB", r["soft"], r["deltaN"])) if MODE == "soft" else (lambda r: (r["flag"] == "NB", round(r["deltaN"], 6), r["soft"])) if MODE == "dN" else (lambda r: (r["flag"] == "NB", r["cp"], round(r["deltaN"], 6), r["soft"]))  # flag is the EXACT test
best = None; found = 0
for g in range(gens):
    cand = beam + [mutate(rnd.choice(beam)) for _ in range(BEAM * KIDS)]
    cand = [d for d in cand if d is not None and NMIN <= len(d) <= NMAX and connected(d)]
    uniq = list({tuple(d): d for d in cand}.values())
    res = run(uniq)
    if MODE == "cp":
        for d, r, pl in zip(uniq, res, pair_laws(uniq)): r["cp"] = firing_full_pairs(d, pl)
    else:
        for r in res: r["cp"] = -1
    scored = sorted(zip(uniq, res), key=lambda t: key(t[1]))
    beam = [d for d, _ in scored[:BEAM // 2]] + [d for d, _ in rnd.sample(scored[:BEAM * 4], BEAM // 2)]
    for d, r in scored:
        if (r["flag"] == "NB_FAILS" or (MODE == "dP" and r["pflag"] == "PNB_FAILS")) and found < 3:
            found += 1; print("NB COUNTEREXAMPLE:", fmt(d), r); sys.stdout.flush()
    if best is None or key(scored[0][1]) < key(best[1]): best = scored[0]
d, r = best
print(f"seed={seed} gens={gens} n in [{NMIN},{NMAX}]: best deltaN={r["deltaN"]:.6f} deltaP={r["deltaP"]:.6f} pflag={r["pflag"]} soft={r['soft']:.4f} delta={r['delta']:.5f} "
      f"nnon={r['nnon']} chainpairs={r['cp']} n={len(d)} range={rng(d)} flag={r['flag']} poset: {fmt(d)}")
