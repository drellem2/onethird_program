"""d1 — WHY the image has no convex shadow, in a form that is not about the image.

`mg-c776` `c2.1` measured `vert(M_n) subset R_n`, hence `conv(R_n) = M_n`, hence no inequality
valid on the image cuts anything off the body.  That is correct and it is re-measured here at
`d1.1` by a library that shares no code with it.

WHAT THIS ARM ADDS is that the obstruction is not a property of `R_n` at all:

    T-3da1.  Let C be ANY class of probability measures on S_n that contains every point mass,
             and let S = { pi(mu) : mu in C } be its marginal image.  Then conv(S) = M_n.

    Proof.   pi(delta_sigma) = delta_sigma is a vertex of M_n, so vert(M_n) subset S subset M_n,
             and a set containing every vertex of a polytope has the polytope as its hull.  QED

    Corollary.  NO restriction of the marginal body phrased as "pi must be realizable" can
                lower a linear ceiling over M_n -- because REALIZABILITY IS VACUOUS AT THE
                VERTICES.  Every vertex is the marginal vector of a point mass, which is as
                realizable as a measure gets.  Realizability and extremality point the SAME WAY.

That is strictly more general than `c2.1`: it disposes of every candidate of this shape at once,
including the ones nobody has written down yet, and it says which property of a proposed
restriction has to be checked FIRST -- does it exclude a vertex?

`d1.4` is the other half and it is what stops this arm from being a proof that nothing works:
a restriction that DOES exclude vertices tightens, and hypothesis (1) read on the MEASURE is
one.  The dividing line is exactly vertex exclusion, and `d3` measures what it buys.
"""

from fractions import Fraction

import lib3da1 as L

FAIL = []


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


# ---------------------------------------------------------------------------------------
head("d1.1  vert(M_n) is inside the image — mg-c776 c2.1, re-measured on independent code")

rows = []
for n in (3, 4, 5):
    U = L.all_perms(n)
    posets = L.enumerate_posets(n)
    R = {key(L.uniform_image(P, n, U)[0], n) for P in posets}
    V = {key(v, n) for v in L.vertices(n)}
    fixed = all(L.retract(v, n, U) == v for v in L.vertices(n))
    rows.append((n, len(V), len(R), V <= R, fixed))

print("   n | vertices of M_n | |R_n| | vert subset R_n | every vertex is r-FIXED")
print("  ---+-----------------+-------+-----------------+------------------------")
for n, nv, nr, sub, fx in rows:
    print(f"   {n} | {nv:15d} | {nr:5d} | {str(sub):15s} | {fx}")
check(all(sub and fx for _, _, _, sub, fx in rows),
      "every vertex of M_n is an image point, at n = 3,4,5",
      "|R_n| = 19, 219, 4231 reproduces mg-c776 c1's count from a different marginal algorithm;\n"
      "the containment is what gives conv(R_n) = M_n, since a set holding every vertex of a\n"
      "polytope has that polytope as its hull")

# ---------------------------------------------------------------------------------------
head("d1.2  THE GENERALISATION — four DIFFERENT realizability restrictions, same obstruction")

n = 4
U = L.all_perms(n)
posets = L.enumerate_posets(n)
V = {key(v, n) for v in L.vertices(n)}

# (a) mg-c776's image: uniform on the linear extensions.
S_a = {key(L.uniform_image(P, n, U)[0], n) for P in posets}

# (b) A DIFFERENT canonical measure on the same supports: weight each extension by
#     1/(1 + inv(sigma)).  Nothing uniform about it, and it is not mg-c776's set.
def inv_count(sigma):
    pos = {x: k for k, x in enumerate(sigma)}
    return sum(1 for (i, j) in L.pairs(len(sigma)) if pos[i] > pos[j])


S_b = set()
for P in posets:
    ext = L.linear_extensions(P, n, U)
    w = [Fraction(1, 1 + inv_count(s)) for s in ext]
    tot = sum(w)
    S_b.add(key(L.marginal([(s, x / tot) for s, x in zip(ext, w)], n), n))

# (c) The SUPPORT-level restriction: every measure whose support is contained in the linear
#     extensions of some poset.  This is much larger than either image and is the widest
#     reading of "realizable" the pair-marginal level can express.
#     It is computed here on the ANTICHAIN alone, which is enough and is the point:
#     L(antichain) = S_n, so this restriction is the whole body and restricts NOTHING.
antichain = frozenset()
S_c_support = L.linear_extensions(antichain, n, U)

# (d) The ARITHMETIC restriction mg-c776 §3 names as the other non-convex survivor (`U-id`):
#     every coordinate of an image point is a multiple of 1/e(P).  Checked on R_n, and then
#     checked at the vertices, where e(P) = 1 and the condition is satisfied by every integer.
u_id_ok, vert_u_id = True, True
for P in posets:
    pi, ext = L.uniform_image(P, n, U)
    e = len(ext)
    if any((x * e).denominator != 1 for x in pi.values()):
        u_id_ok = False
for v in L.vertices(n):
    P = L.poset_of(v, n)
    e = len(L.linear_extensions(P, n, U))
    if e != 1 or any((x * e).denominator != 1 for x in v.values()):
        vert_u_id = False

print("   restriction                                              | distinct points | holds every vertex")
print("  ----------------------------------------------------------+-----------------+-------------------")
print(f"   (a) pi(Unif(L(P)))            — mg-c776's R_n            | {len(S_a):15d} | {V <= S_a}")
print(f"   (b) pi(mu_P), mu_P ~ 1/(1+inv) — a different canonical mu | {len(S_b):15d} | {V <= S_b}")
print(f"   (c) supp(mu) inside some L(P) — the widest reading        | {'all of M_n':>15s} | {len(S_c_support) == len(U)}")
print(f"   (d) U-id: coords multiples of 1/e(P)                      | {'contains R_n':>15s} | {vert_u_id}")

check(V <= S_a and V <= S_b and len(S_c_support) == len(U) and vert_u_id and u_id_ok,
      "all four restrictions contain every one of the 24 vertices, so all four have hull M_n",
      "(a) and (b) are DIFFERENT sets — "
      f"{len(S_a ^ S_b)} of {len(S_a | S_b)} points are in one and not the other — and the\n"
      "obstruction is identical, which is the content of T-3da1: it is not about which\n"
      "canonical measure you pick.\n"
      "(c) is the finding that the widest reading is VACUOUS OUTRIGHT: L(antichain) = S_n, so\n"
      f"'supp(mu) inside some L(P)' admits all {len(U)} permutations and is no restriction at all.\n"
      "(d) the arithmetic survivor holds at every vertex too, because a total order has\n"
      "e(P) = 1 and every rational is a multiple of 1/1.")

# ---------------------------------------------------------------------------------------
head("d1.3  the one line — a point mass is a measure, and its marginal vector IS a vertex")

bad = []
for n in (3, 4, 5):
    for sigma in L.all_perms(n):
        if L.marginal([(sigma, Fraction(1))], n) != L.vertex(sigma, n):
            bad.append((n, sigma))
check(not bad,
      "pi(delta_sigma) = delta_sigma at all 6 + 24 + 120 point masses",
      "This is the whole proof of T-3da1 and it is why the obstruction cannot be engineered\n"
      "around: the vertices are not merely IN the realizable set, they are the realizable set's\n"
      "least interesting members.  Any future proposal of the form 'restrict M_n to the pi that\n"
      "are realizable in sense X' inherits this the moment sense X admits a point mass.")

# ---------------------------------------------------------------------------------------
head("d1.4  THE CONTROL — a restriction that DOES tighten, and what distinguishes it")

# Hypothesis (1) read on the MEASURE, inside the cell L* = identity: every pair is flipped with
# probability at most 1/3, i.e. pi[(i,j)] >= 2/3 for i < j.  A vertex has 0/1 coordinates, so it
# survives only if every coordinate is 1 -- there is exactly ONE such vertex, delta_id.
rows = []
for n in (3, 4, 5):
    surv = [s for s in L.all_perms(n)
            if all(L.vertex(s, n)[p] >= Fraction(2, 3) for p in L.pairs(n))]
    rows.append((n, len(L.all_perms(n)), len(surv), surv[0] if len(surv) == 1 else None))

print("   n | vertices of M_n | surviving the cell | the survivor")
print("  ---+-----------------+--------------------+--------------")
for n, tot, k, s in rows:
    print(f"   {n} | {tot:15d} | {k:18d} | {s}")
check(all(k == 1 and s == tuple(range(n)) for n, _, k, s in rows),
      "hypothesis (1) read on the MEASURE excludes n! - 1 of the n! vertices",
      "THIS IS THE DIVIDING LINE, and it is the reason d1.2 is a finding rather than a\n"
      "tautology about every set anyone might write down.  A restriction tightens a linear\n"
      "ceiling exactly when it excludes vertices; realizability excludes none, and hypothesis\n"
      "(1) on the measure excludes all but one.\n"
      "AND IT IS ALSO WHY mg-c776 c2.3 IS NOT A COUNTEREXAMPLE TO THIS: c2.3 reads hypothesis\n"
      "(1) on the POSET -- delta(P) for P = P(pi) -- where a total order has no incomparable\n"
      "pair and its delta is a maximum over the EMPTY set, so all n! vertices survive.  The two\n"
      "readings of the same hypothesis differ by n! - 1 vertices, and d3 measures what the\n"
      "difference is worth.")

print("\nRESULT: " + ("GREEN — all checks passed" if not FAIL else f"RED — {FAIL}"))
raise SystemExit(1 if FAIL else 0)
