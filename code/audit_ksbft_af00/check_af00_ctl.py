"""negative controls for check_af00.py §4 (run on exhaustive n<=5)"""
import itertools, sys, io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    sys.argv = ['x', '0']
    import check_af00 as C
fire51 = fire52 = tight_pz = 0
seen = set()
for n in range(2, 6):
    pairs = [(i, j) for i in range(n) for j in range(i+1, n)]
    for mask in range(1 << len(pairs)):
        lt = C.close(n, [pairs[k] for k in range(len(pairs)) if (mask >> k) & 1])
        key = tuple(map(tuple, lt))
        if key in seen: continue
        seen.add(key)
        N, e = C.pos_counts(n, lt)
        for x in range(n):
            I = C.inc(n, lt, x); d = sum(lt[y][x] for y in range(n)); Dn = [y for y in range(n) if lt[y][x]]
            for j in range(len(I)+1):  # planted: sum over ALL j-subsets, not only down-sets
                s = sum(C.e_of(n, lt, set(Dn) | set(J)) * C.e_of(n, lt, set(range(n)) - set(Dn) - set(J) - {x})
                        for J in itertools.combinations(I, j))
                if s != N[x][d+1+j]: fire51 += 1
            ds = C.ideals_of(n, lt, I)
            for J in ds:
                K = set(Dn) | J
                for z in I:
                    if z not in J and (J | {z}) in ds:
                        rL = C.Fr(C.e_of(n, lt, K | {z}), C.e_of(n, lt, K))
                        pz = len(C.inc(n, lt, z))
                        if rL > pz: tight_pz += 1   # does pi(z)+1 ever bind? (x is never in K)
                        if rL > pz - 1: fire52 += 1  # planted false: bound pi(z)-1
print(f"[control] Lemma 5.1 with ALL j-subsets (planted false) FIRES: {fire51}")
print(f"[control] Lemma 5.2 with bound pi(z)-1 (planted false) FIRES: {fire52}")
print(f"[observation] Lemma 5.2 ratio ever > pi(z) (n<=5 exhaustive): {tight_pz}  (x in inc(z) is never in K, so pi(z) suffices)")
