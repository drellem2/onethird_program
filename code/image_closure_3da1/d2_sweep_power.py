"""d2 — how much a direction sweep over the image can actually see.

`mg-c776` `c2.2` reports `max over R_n = max over M_n for every sampled linear functional,
300 seeded integer directions at n = 3,4, 0 separations found`, and labels it in the deliverable
as `a vacuity guard rather than a second proof`.  That label is correct and this arm is not a
correction of it.  What this arm adds is the MEASUREMENT the label implies and does not carry:
a guard is only worth reading if it can go red, so how often does it?

Two findings, and the second is the one worth keeping.

  d2.2  The sweep CANNOT find a separation, as a matter of logic and not of sampling.  Once
        `vert(M_n) subset R_n` is known (`d1.1`, `c2.1`), `max over R_n = max over M_n` holds
        for EVERY direction, because the maximum of a linear functional over a polytope is
        attained at a vertex and every vertex is in R_n.  `0 separations` is therefore not
        evidence about R_n -- it is c2.1 restated, and it would read the same against a sweep
        of 3 directions or 3 million.

  d2.3  Put to a world where a separation DOES exist -- the same image with ONE vertex removed
        -- the sweep detects it at a rate of about 1/n!, because a single missing vertex is
        invisible unless the sampled direction happens to be maximised UNIQUELY there.
        Measured below.  At n = 5 that is 1 direction in 120; the estate should not read a
        clean direction sweep as evidence that a set is convexly large.

Neither finding weakens `mg-c776`'s conclusion, which never rested on the sweep: `conv(R_n) = M_n`
is a one-line theorem and `d1` re-proves it.  What they bound is what a sweep of this shape is
worth as evidence ANYWHERE in this estate, which is why this arm is here rather than in a footnote.
"""

from fractions import Fraction

import lib3da1 as L

FAIL = []
N_DIRECTIONS = 300          # mg-c776 c2.2's own sample size, taken deliberately
SEED = 0x3DA1


def check(ok, name, detail):
    print(f"  [{'GREEN' if ok else 'RED  '}] {name}")
    for line in detail.split("\n"):
        print(f"       {line}")
    if not ok:
        FAIL.append(name)


def head(t):
    print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


def key(pi, n):
    return tuple(pi[p] for p in L.pairs(n))


def build(n):
    U = L.all_perms(n)
    R = [L.uniform_image(P, n, U)[0] for P in L.enumerate_posets(n)]
    return U, R, L.vertices(n)


# ---------------------------------------------------------------------------------------
head("d2.1  the sweep as mg-c776 ran it — reproduced on independent code")

rows = []
for n in (3, 4):
    U, R, V = build(n)
    rng = L.Lcg(SEED)
    seps = 0
    for _ in range(N_DIRECTIONS):
        c = rng.direction(n)
        if L.maximise(c, R, n) != L.maximise(c, V, n):
            seps += 1
    rows.append((n, seps))
print("   n | directions | separations found")
print("  ---+------------+------------------")
for n, s in rows:
    print(f"   {n} | {N_DIRECTIONS:10d} | {s:17d}")
check(all(s == 0 for _, s in rows),
      f"0 separations over {N_DIRECTIONS} integer directions at n = 3,4",
      "the same reading mg-c776 c2.2 reports, from a different library and a different PRNG")

# ---------------------------------------------------------------------------------------
head("d2.2  and it could not have been otherwise — the sweep tests nothing beyond c2.1")

n = 4
U, R, V = build(n)
rng = L.Lcg(SEED)
attained_at_vertex = 0
for _ in range(N_DIRECTIONS):
    c = rng.direction(n)
    mv = L.maximise(c, V, n)
    # The maximum over R_n is attained at a VERTEX every time, because the vertices are in R_n
    # and nothing in M_n beats a vertex on a linear functional.
    if L.maximise(c, R, n) == mv and max(L.dot(c, pi, n) for pi in R) == mv:
        attained_at_vertex += 1
check(attained_at_vertex == N_DIRECTIONS,
      "every one of the 300 maxima over R_n is attained at a vertex of M_n",
      "So `0 separations` is a RESTATEMENT of vert(M_n) subset R_n, not independent evidence for\n"
      "it.  A linear functional is maximised over a polytope at a vertex; every vertex is in the\n"
      "image; therefore no direction can separate, at any sample size.  The sweep has no power\n"
      "against its own hypothesis -- which is what `vacuity guard` should be read to mean.")

# ---------------------------------------------------------------------------------------
head("d2.3  THE POWER MEASUREMENT — the same sweep put to a world with a real separation")

print("   Plant: the image with ONE vertex removed.  Its hull is strictly smaller than M_n, so a")
print("   separation EXISTS.  The question is how often 300 random directions notice.\n")
print("   n | n! | directions with a UNIQUE argmax | detects delta_id removed | pooled rate | 1/n!")
print("  ---+----+---------------------------------+--------------------------+-------------+-------")
power_rows = []
for n in (3, 4, 5):
    U, R, V = build(n)
    rng = L.Lcg(SEED)
    uniq, hit_id = 0, 0
    id_key = key(L.vertex(tuple(range(n)), n), n)
    for _ in range(N_DIRECTIONS):
        c = rng.direction(n)
        vals = [L.dot(c, v, n) for v in V]
        best = max(vals)
        arg = [i for i, x in enumerate(vals) if x == best]
        if len(arg) == 1:
            uniq += 1
            if key(V[arg[0]], n) == id_key:
                hit_id += 1
    pooled = Fraction(uniq, N_DIRECTIONS * len(U))
    power_rows.append((n, len(U), uniq, hit_id, pooled))
    print(f"   {n} | {len(U):2d} | {uniq:31d} | {hit_id:24d} | "
          f"{float(pooled):11.4f} | {1/len(U):.4f}")

check(all(h < N_DIRECTIONS // 4 for _, _, _, h, _ in power_rows),
      "a single removed vertex is invisible to the overwhelming majority of directions",
      "The pooled rate is the chance that a uniformly chosen one of the n! single-vertex\n"
      "removals is caught by a uniformly chosen direction, and it tracks 1/n! -- a direction\n"
      "catches a removal only when it is maximised UNIQUELY at the removed point.\n"
      "CONSEQUENCE FOR THE ESTATE, and it is the reason this arm is not a footnote: a direction\n"
      "sweep returning 0 separations is near-zero evidence that a subset of M_n is convexly\n"
      "large.  Where a claim of that shape is load-bearing it needs the containment argument,\n"
      "which is what mg-c776 has and what this directory re-proves at d1.")

# ---------------------------------------------------------------------------------------
head("d2.4  the separation IS there — a chosen direction finds it every time")

rows = []
for n in (3, 4, 5):
    U, R, V = build(n)
    # c = all ones.  <c, pi> = sum of coordinates, maximised over M_n UNIQUELY at delta_id
    # (every coordinate 1).  So dropping delta_id must drop the maximum.
    c = {p: 1 for p in L.pairs(n)}
    full = L.maximise(c, V, n)
    id_key = key(L.vertex(tuple(range(n)), n), n)
    without = max(L.dot(c, pi, n) for pi in R if key(pi, n) != id_key)
    rows.append((n, full, without, without < full))
print("   n | max over M_n | max over R_n minus delta_id | strictly smaller")
print("  ---+--------------+-----------------------------+-----------------")
for n, f, w, ok in rows:
    print(f"   {n} | {L.fmt(f):12s} | {L.fmt(w):27s} | {ok}")
check(all(ok for _, _, _, ok in rows),
      "the all-ones direction separates the planted set at every n, exactly",
      "So d2.3's low rate is a property of the SWEEP and not of the planted world: the\n"
      "separation is real, exact, and found instantly by one direction chosen with the\n"
      "removed point in mind.  Random directions are the wrong instrument for this question,\n"
      "and that is the finding rather than a caveat about sample size.")

print("\nRESULT: " + ("GREEN — all checks passed" if not FAIL else f"RED — {FAIL}"))
raise SystemExit(1 if FAIL else 0)
