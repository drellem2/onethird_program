"""A4 -- X4: the Young-Fibonacci re-scoping, and the NEW claim it derives.

mg-41aa keeps mg-af28's measurement (33 intervals to rank 6, 5 non-distributive,
witness w = 221) and rewrites the reading.  In doing so it derives something
mg-6ad0's brief did not ask for, in §2's heading note and in §3 row 10:

    "Row 10 therefore has the SAME index-set contact this document headlines
     for Young's, on 28 of its 33 intervals."

That is new material produced while repairing a defect that came from new
material.  So this probe checks three things:

  1. the measurement: 33 / 5 / 28, and the witness, on a fourth Young-Fibonacci
     implementation (mine), controlled by DU - UD = I;
  2. the negative inside it: "5 are NOT distributive" -- attacked by trying to
     verify distributivity of each of the 5 directly, and by exhibiting the
     forbidden sublattice;
  3. the NEW claim: is the YF contact really "the same" as the Young one?
     Measured by asking WHICH posets P arise, which is the question the Young
     headline answers and the YF sentence does not.

Also here: "no differential poset is finite", which mg-41aa uses as the reason
X4's old reading is vacuous.  The document licenses it by definition (locally
finite, infinitely many ranks).  There is a stronger, definition-free reason,
and it is checked.
"""
import sys
from kern5800 import (bits, canon, decode, down_of, enumerate_posets,
                      ideal_lattice, induced, is_distributive, is_lattice,
                      join_irreducibles, interval_poset, meet_join_tables,
                      skew_cell_poset, skew_shapes, straight_shapes,
                      shape_to_mu_lam, yf_poset, yf_down_covers, yf_words)

print("=" * 78)
print("A4  X4 -- YOUNG-FIBONACCI, AND THE NEW CLAIM THE REPAIR DERIVES")
print("=" * 78)

RANK = 6
m, up, els, idx, cov = yf_poset(RANK)
sel = [i for i, w in enumerate(els) if sum(w) <= RANK]
print("\nwords with rank <= %d: %d   (Fibonacci 1+1+2+3+5+8+13)" % (RANK, len(sel)))

# ---------------------------------------------- the measurement, redone

print("\n[R6] EVERY INTERVAL [0,w], rank(w) <= 6")
dist = []
nondist = []
for i in sel:
    sub = [j for j in range(m) if j == i or ((up[j] >> i) & 1)]
    sub = [j for j in sub if sum(els[j]) <= sum(els[i])]
    k, kup = induced(m, up, sub)
    if not is_lattice(k, kup):
        print("   NOT A LATTICE: w=%s" % (els[i],))
        continue
    (dist if is_distributive(k, kup) else nondist).append((els[i], k, kup))
print("  intervals: %d;  distributive: %d;  NOT distributive: %d"
      % (len(sel), len(dist), len(nondist)))
print("  non-distributive words: %s" % [w for w, _, _ in nondist])
smallest = min((w for w, _, _ in nondist), key=lambda w: (sum(w), w))
print("  smallest non-distributive witness: w = %s  (rank %d)"
      % ("".join(str(d) for d in smallest), sum(smallest)))

# attack the negative: try to make each of the 5 come out distributive
print("\n  ATTACKING '5 ARE NOT DISTRIBUTIVE' -- each one re-checked by exhibiting")
print("  the failing triple a, b, c with a^(bvc) != (a^b)v(a^c):")
for w, k, kup in nondist:
    meet, join = meet_join_tables(k, kup)
    found = None
    for a in range(k):
        for b in range(k):
            for c in range(k):
                if meet[a][join[b][c]] != join[meet[a][b]][meet[a][c]]:
                    found = (a, b, c)
                    break
            if found:
                break
        if found:
            break
    print("    w=%-6s |interval|=%-3d failing triple %s"
          % ("".join(str(d) for d in w), k, found))

# ---------------------------------------- Birkhoff reconstruction of the 28

print("\n  RECONSTRUCTION: each distributive interval as J(P) from its")
print("  join-irreducibles, rebuilt and compared as a lattice:")
bad = 0
arising = {}
for w, k, kup in dist:
    r, rup = join_irreducibles(k, kup)
    jm, jup, _ = ideal_lattice(r, rup)
    if canon(jm, jup) != canon(k, kup):
        bad += 1
        print("    BAD w=%s" % (w,))
    arising.setdefault(r, set()).add(canon(r, rup))
print("    reconstructions: %d, bad: %d" % (len(dist), bad))

# ------------------- the Young side, for the comparison the new claim makes

print("\n  THE YOUNG SIDE: all intervals [0,lam] with |lam| <= 6")
ylams = [()] + [tuple(b for a, b in s) for n in range(1, 7) for s in straight_shapes(n)]
ybad = 0
for lam in ylams:
    k, kup, _ = interval_poset((), lam)
    if not is_distributive(k, kup):
        ybad += 1
print("    %d intervals, non-distributive: %d" % (len(ylams), ybad))

# ------------------------------------- IS IT THE SAME CONTACT?  measured

print("\n[NEW CLAIM] 'Row 10 has the SAME index-set contact ... on 28 of 33'")
print("  The Young headline is not just 'the intervals are J(P)' -- it NAMES the")
print("  P: the skew cell posets.  So the comparable question for YF is which P")
print("  arise there.  Measured:")
allskew = {0: {canon(0, ())}}       # the empty shape: [0,0] is a single point
for n in range(1, RANK + 1):
    allskew[n] = {canon(*skew_cell_poset(s)) for s in skew_shapes(n, n)}
tot = 0
inskew = 0
sizes = {}
for r, codes in sorted(arising.items()):
    tot += len(codes)
    hit = len(codes & allskew.get(r, set())) if r in allskew else 0
    inskew += hit
    sizes[r] = (len(codes), hit)
    print("    |P|=%d: %d distinct P arise from YF intervals; %d of them are skew cell posets"
          % (r, len(codes), hit))
print("    total distinct P from YF intervals to rank 6: %d; skew cell posets"
      " among them: %d; NOT skew: %d" % (tot, inskew, tot - inskew))
print("    For Young's lattice the answer to the same question is: ALL of them,")
print("    and the class is CLOSED and NAMED (the skew cell posets).  For")
print("    Young-Fibonacci no class is named by anyone in this arc.")

# --------------------------------- 'no differential poset is finite'

print("\n[N3] 'NO DIFFERENTIAL POSET IS FINITE' -- the reason mg-41aa gives is")
print("  definitional (locally finite, infinitely many ranks).  A stronger one:")
print("  on a FINITE poset U and D are finite matrices, so tr(DU) = tr(UD) and")
print("  tr(DU - UD) = 0, while tr(r.I) = r.|P| > 0.  No finite non-empty poset")
print("  is r-differential for any r >= 1, whatever else it satisfies.")
print("  The trace argument is a PROOF, not a measurement: with U the cover")
print("  matrix and D = U^T, tr(DU) = tr(U^T U) = tr(U U^T) = tr(UD) for every")
print("  finite poset whatsoever.  Running it over examples would be a")
print("  restatement (the defect mg-3b51 flagged in this repo as R1d), so it")
print("  is booked here as an ARGUMENT and not as evidence.")
print("\n  What IS a measurement, and is reported as FORCED anyway: DU - UD")
print("  built as a full matrix on every poset to n <= 6, counting how many")
print("  satisfy DU - UD = I.  The answer cannot be anything but 0, by the")
print("  line above; it is here only as a check that the matrices are the")
print("  matrices the argument is about.")
ps = enumerate_posets(6)
checked = 0
hits = 0
maxdiag = 0
for n in range(1, 7):
    for code in ps[n]:
        u = decode(n, code)
        dn = down_of(n, u)
        cov2 = [[y for y in bits(u[x]) if not (u[x] & dn[y])] for x in range(n)]
        U = [[1 if y in cov2[x] else 0 for y in range(n)] for x in range(n)]
        DU = [[sum(U[x][t] * U[y][t] for t in range(n)) for y in range(n)]
              for x in range(n)]
        UD = [[sum(U[t][x] * U[t][y] for t in range(n)) for y in range(n)]
              for x in range(n)]
        M = [[DU[x][y] - UD[x][y] for y in range(n)] for x in range(n)]
        checked += 1
        if all(M[x][y] == (1 if x == y else 0) for x in range(n) for y in range(n)):
            hits += 1
        maxdiag = max(maxdiag, sum(M[x][x] for x in range(n)))
print("  posets checked: %d;  satisfying DU - UD = I: %d;  max tr(DU - UD): %d"
      % (checked, hits, maxdiag))
worst = maxdiag
diffposets = hits

print("\nSUMMARY a4_yf: intervals %d, distributive %d, non-distributive %d, "
      "witness %s; reconstructions bad %d; Young intervals %d non-distributive %d; "
      "distinct P from YF %d of which skew %d; posets to n<=6 with DU-UD=I: %d "
      "of %d (FORCED)"
      % (len(sel), len(dist), len(nondist),
         "".join(str(d) for d in smallest), bad, len(ylams), ybad,
         tot, inskew, diffposets, checked))
