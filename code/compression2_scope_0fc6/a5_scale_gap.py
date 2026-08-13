"""a5 — THE NOTE'S OWN LAST QUESTION, ANSWERED.  And the currency it lands in.

**THIS ARM IS POST-HOC AND IS NOT COVERED BY `2edf68a`'s PRE-REGISTRATION.**  It was written
after `a0`-`a4` had run and their results were known.  Nothing here is scored against a
prediction, and it must not be read as one.  Every other arm in this suite was written before
its own result; this one was not, and saying so is the whole of its provenance.

**AND ITS FIRST DRAFT ASSERTED A LEMMA THAT IS FALSE.  THE REFUTATION IS §a5.3 AND IT IS KEPT.**
I wrote §a5.3 as `E_l(f) = E_l(D_l f)` -- "the scale-`l` Dirichlet form reads exactly the
scale-`l` martingale increment" -- ran it, and it came back RED at three of five posets.  The
error is named at §a5.3 rather than in a commit message, because it is the same error the note
itself is at risk of: **a graded form is not a decoupled one**, and the step from (8) to "the
spectral problem is now a multiscale family" is exactly that step.

The note's closing paragraph names its own next step:

    "The next question should be whether the Dirichlet form of the standard statistic admits
     a corresponding scale decomposition.  If it does, the 6% entropy saving itself is
     secondary -- the real gain is that the spectral problem has been converted into a
     multiscale family of median-graph problems."

`a4.1` proved (8) exactly: one BK edge changes one word at one node.  `a4.3b` proved the scale
projections are a FILTRATION and that `Var(f) = sum_l ||D_l f||^2`.  Those are the hypotheses
of the note's question, so the question is answerable here rather than merely quotable.

  a5.1  THE FORM IS GRADED.  `E = sum_l E_l` exactly: the BK edge set PARTITIONS by scale,
        because every edge has a unique LCA node (a4.1).  Exact, in Fractions.

  a5.2  AND THE GRADING ANNIHILATES THE COARSE FILTRATION.  `E_l(Pi_l f) = 0`: a scale-`l`
        edge leaves every COARSER word fixed, so it cannot move a function of them.  This is
        identity (8) restated at the level of forms, and it is the strongest true thing in
        this direction.  Exact, in Fractions.

  a5.2c PLANTED WORLD -- the same statement with the level read off the WORD POSITION instead
        of the LCA of the swapped elements must FAIL.  Without it, a5.2 could be a property of
        gradings in general rather than of this one.

  a5.3  THE ALIGNMENT FAILS, AND THIS IS THE ARM'S RESULT.  `E_l(f) = E_l(D_l f)` is FALSE.
        `E_l` annihilates everything COARSER than `l` (a5.2) but reads everything FINER: a
        scale-`l` edge holds the finer words fixed, and `f` is still a function of them, so
        `f(L) - f(L')` does not survive the averaging in `Pi_{l+1}`.  The form is graded and
        the norm is graded and THE TWO GRADINGS DO NOT MATCH -- the structure is triangular,
        `E(f) = sum_l E_l(Q_l f)` with `Q_l = I - Pi_l`, not diagonal.

  a5.4  SO THE PER-SCALE BOUND DOES NOT FOLLOW, and where it is written down anyway it is not
        merely lossy but VACUOUS: `min_l mu_l = 0` at the antichain, because the finest-scale
        edges do not connect their own increment space.  Measured beside `gap_BK`.

  a5.5  AND THE CURRENCY.  Even had it worked, the object produced is a LOWER BOUND ON
        `gap_BK`.  Priced against `STATE.md:29` and `mg-145f` -- the citation the ticket
        permits at exactly this paragraph of the note and nowhere else in it.
"""
import sys
import random
from fractions import Fraction

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import lib0fc6 as L  # noqa: E402


def levels_of(nodes):
    """Map each dyadic node to its level index, coarsest = 0."""
    sizes = sorted({hi - lo for (lo, mid, hi) in nodes}, reverse=True)
    return {nd: sizes.index(nd[2] - nd[0]) for nd in nodes}, len(sizes)


def graded_edges(LEs, n, lt, star, nodes):
    """Every BK edge of the graph on L(P), tagged with the level of its LCA node.

    Returned as `{level: [(i, j), ...]}` with `i < j` indices into `LEs`, each undirected edge
    once.  The tag is the note's own: the unique node whose children separate the swapped pair.
    """
    lev, nlev = levels_of(nodes)
    idx = {Lx: i for i, Lx in enumerate(LEs)}
    out = {k: [] for k in range(nlev)}
    for Lx in LEs:
        i = idx[Lx]
        for p in L.bk_edges(Lx, n, lt):
            j = idx[L.swap(Lx, p)]
            if i < j:
                out[lev[L.lca_node(Lx[p], Lx[p + 1], star, nodes)]].append((i, j))
    return out, nlev


def position_graded_edges(LEs, n, lt):
    """PLANTED WORLD: the same edges graded by WORD POSITION rather than by the LCA."""
    idx = {Lx: i for i, Lx in enumerate(LEs)}
    out = {}
    for Lx in LEs:
        i = idx[Lx]
        for p in L.bk_edges(Lx, n, lt):
            j = idx[L.swap(Lx, p)]
            if i < j:
                out.setdefault(p, []).append((i, j))
    return out


def flag_fibers(LEs, star, nodes, keep_levels):
    """Pi_k as a PARTITION: the fibers of the words at the coarsest `keep_levels` levels.

    Averaging over a fiber IS the conditional expectation, so no matrix is ever built.
    """
    lev, _ = levels_of(nodes)
    keep = [nd for nd in nodes if lev[nd] < keep_levels]
    groups = {}
    for i, Lx in enumerate(LEs):
        groups.setdefault(L.merge_words(Lx, star, keep), []).append(i)
    return list(groups.values())


def project(f, fibers):
    g = [Fraction(0)] * len(f)
    for grp in fibers:
        avg = sum(f[i] for i in grp) / len(grp)
        for i in grp:
            g[i] = avg
    return g


def dirichlet(f, edges):
    return sum((f[i] - f[j]) ** 2 for (i, j) in edges)


def sub(f, g):
    return [a - b for a, b in zip(f, g)]


def population():
    """Small, and chosen so a5.4 can solve eigenproblems in pure Python (no numpy on this host).

    `n = 4` gives TWO scales, `n = 8` gives THREE -- the second is here so nothing below can be
    a two-scale artefact.  The `n = 8` posets are constrained to keep `|L(P)|` near 100.
    """
    return [("n=4 antichain", 4, L.antichain(4)),
            ("n=4  0<1", 4, L.tclose(4, [(0, 1)])),
            ("n=4  0<1, 2<3", 4, L.tclose(4, [(0, 1), (2, 3)])),
            ("n=8  four 2-chains + 0<2<4<6", 8,
             L.tclose(8, [(0, 1), (2, 3), (4, 5), (6, 7), (0, 2), (2, 4), (4, 6)])),
            ("n=8  two 4-chains", 8,
             L.tclose(8, [(0, 1), (1, 2), (2, 3), (4, 5), (5, 6), (6, 7)]))]


random.seed(20260813)
CASES = []
for (name, n, lt) in population():
    LEs = L.linear_extensions(n, lt)
    star = LEs[0]
    nodes = L.dyadic_nodes(n)
    ge, nlev = graded_edges(LEs, n, lt, star, nodes)
    CASES.append(dict(name=name, n=n, lt=lt, LEs=LEs, star=star, nodes=nodes, ge=ge,
                      nlev=nlev, edges=[e for k in ge for e in ge[k]],
                      Pi=[flag_fibers(LEs, star, nodes, k) for k in range(nlev + 1)]))

# ---------------------------------------------------------------- a5.1

L.banner("a5.1  THE FORM IS GRADED:  E = sum_l E_l, because the edge set PARTITIONS by scale")
for c in CASES:
    seen = set()
    dup = sum(1 for k in c["ge"] for e in c["ge"][k] if (e in seen) or seen.add(e))
    L.verdict(dup == 0 and len(seen) == len(c["edges"]),
              f"{c['name']}: every BK edge carries EXACTLY ONE scale",
              f"|L(P)| = {len(c['LEs'])}, {len(c['edges'])} edges, {c['nlev']} scales")
    ok = True
    for _ in range(3):
        f = [Fraction(random.randint(-9, 9)) for _ in c["LEs"]]
        if dirichlet(f, c["edges"]) != sum(dirichlet(f, c["ge"][k]) for k in range(c["nlev"])):
            ok = False
    L.verdict(ok, f"{c['name']}: E(f) = sum_l E_l(f) exactly",
              "3 random integer f, exact rationals")

# ---------------------------------------------------------------- a5.2

L.banner("a5.2  AND IT ANNIHILATES THE COARSE FILTRATION:  E_l(Pi_l f) = 0.  (8) as a form")
for c in CASES:
    ok = True
    for _ in range(3):
        f = [Fraction(random.randint(-9, 9)) for _ in c["LEs"]]
        for k in range(c["nlev"]):
            if dirichlet(project(f, c["Pi"][k]), c["ge"][k]) != 0:
                ok = False
    L.verdict(ok, f"{c['name']}: E_l(Pi_l f) = 0 at every scale",
              f"{c['nlev']} scales, 3 random f, exact rationals")

print()
print("       [finding] this is identity (8) restated at the level of QUADRATIC FORMS, and it")
print("                 is exact.  A scale-l edge holds every COARSER word fixed, so it cannot")
print("                 move a function of them.  It is the strongest TRUE statement in the")
print("                 direction the note's closing paragraph points.")

# ---------------------------------------------------------------- a5.2c

L.banner("a5.2c  PLANTED WORLD — the same statement with the level read off the WORD POSITION")
for c in CASES[:3]:
    pg = position_graded_edges(c["LEs"], c["n"], c["lt"])
    broke = tried = 0
    for _ in range(3):
        f = [Fraction(random.randint(-9, 9)) for _ in c["LEs"]]
        for k in sorted(pg)[:c["nlev"]]:
            tried += 1
            if dirichlet(project(f, c["Pi"][k]), pg[k]) != 0:
                broke += 1
    L.verdict(broke > 0, f"{c['name']}: the POSITION grading BREAKS a5.2 (as it must)",
              f"{broke} of {tried} instances are nonzero")

print()
print("       [control] a5.2 is a property of THIS grading, not of gradings in general.  a4.2")
print("                 measured that the position grading is not even a well-defined partition")
print("                 of EDGES; this measures that assuming it were would be wrong in the one")
print("                 place the whole construction is load-bearing.")

# ---------------------------------------------------------------- a5.3  THE REFUTATION

L.banner("a5.3  THE ALIGNMENT FAILS.  E_l(f) = E_l(D_l f) is FALSE — and I wrote it as a lemma")
print("  The step the note needs is not a5.2 but the stronger `E_l(f) = E_l(D_l f)`, which would")
print("  make the Rayleigh quotient a ratio of two sums over the SAME index.  It is false.")
print()
any_fail = False
for c in CASES:
    bad = tot = 0
    perscale = []
    for k in range(c["nlev"]):
        kb = 0
        for _ in range(3):
            f = [Fraction(random.randint(-9, 9)) for _ in c["LEs"]]
            Dk = sub(project(f, c["Pi"][k + 1]), project(f, c["Pi"][k]))
            tot += 1
            if dirichlet(f, c["ge"][k]) != dirichlet(Dk, c["ge"][k]):
                bad += 1
                kb += 1
        perscale.append(kb)
    any_fail = any_fail or bad > 0
    print(f"  {c['name']:38s}  {bad:2d} of {tot:2d} instances DISAGREE"
          f"    by scale (coarsest first): {perscale}")
L.verdict(any_fail, "E_l(f) = E_l(D_l f) is REFUTED on this population",
          "the arm was written asserting it; the assertion did not survive its own run")

print()
print("       [finding] THE REASON, and it is the note's own risk.  E_l annihilates everything")
print("                 COARSER than l (a5.2) but READS everything FINER: a scale-l edge holds")
print("                 the finer words fixed, and f is still a function of them, so f(L)-f(L')")
print("                 does not survive the averaging inside Pi_{l+1}.  The true structure is")
print("                 TRIANGULAR — E(f) = sum_l E_l(Q_l f) with Q_l = I - Pi_l — and not")
print("                 diagonal.  The FORM is graded (a5.1) and the NORM is graded (a4.3b) and")
print("                 THE TWO GRADINGS DO NOT MATCH.  Grading a form is not decoupling it,")
print("                 and the note's step from (8) to 'a multiscale family of median-graph")
print("                 problems' is exactly that step.")
print("       [where it DOES hold] at the two posets whose finest scale carries no choice, the")
print("                 identity is true for a degenerate reason and not a structural one.")

# ---------------------------------------------------------------- a5.4


def min_rayleigh(edges, fibers_hi, fibers_lo, N, iters=6000):
    """min { E(g)/||g||^2 } over the increment space im(Pi_hi - Pi_lo), by projected power
    iteration on (cI - Laplacian).  Float, and reported as float.

    `fibers_lo is None` means the whole mean-zero space, i.e. `gap_BK` itself.
    """
    deg = [0] * N
    for (i, j) in edges:
        deg[i] += 1
        deg[j] += 1
    c = float(2 * max(deg)) if deg and max(deg) else 1.0

    def avg(v, fibers):
        out = [0.0] * N
        for grp in fibers:
            a = sum(v[i] for i in grp) / len(grp)
            for i in grp:
                out[i] = a
        return out

    def restrict(v):
        if fibers_lo is None:
            m = sum(v) / N
            return [x - m for x in v]
        hi, lo = avg(v, fibers_hi), avg(v, fibers_lo)
        return [a - b for a, b in zip(hi, lo)]

    def lap(v):
        out = [0.0] * N
        for (i, j) in edges:
            d = v[i] - v[j]
            out[i] += d
            out[j] -= d
        return out

    rnd = random.Random(7)
    v = restrict([rnd.uniform(-1, 1) for _ in range(N)])
    nrm = sum(x * x for x in v) ** 0.5
    if nrm < 1e-9:
        return None                                      # the increment space is trivial
    v = [x / nrm for x in v]
    lam = None
    for it in range(iters):
        w = restrict([c * v[i] - x for i, x in enumerate(lap(v))])
        nrm = sum(x * x for x in w) ** 0.5
        if nrm < 1e-14:
            return 0.0
        v = [x / nrm for x in w]
        if it % 50 == 49:
            new = sum(a * b for a, b in zip(v, lap(v)))
            if lam is not None and abs(new - lam) < 1e-10:
                return new
            lam = new
    return lam


L.banner("a5.4  SO THE PER-SCALE BOUND DOES NOT FOLLOW — and written down anyway it is VACUOUS")
print("  poset                                  |L(P)|     gap_BK     min_l mu_l    per-scale mu_l")
for c in CASES:
    N = len(c["LEs"])
    gap = min_rayleigh(c["edges"], None, None, N)
    mus = [min_rayleigh(c["ge"][k], c["Pi"][k + 1], c["Pi"][k], N) for k in range(c["nlev"])]
    mus = [m for m in mus if m is not None]
    lo = min(mus) if mus else float("nan")
    print(f"  {c['name']:38s} {N:6d}  {gap:10.6f}   {lo:10.6f}     "
          f"{['%.6f' % m for m in mus]}")
    L.verdict(lo < 1e-6 or gap >= lo - 1e-6,
              f"{c['name']}: min_l mu_l does not exceed gap_BK",
              f"min_l mu_l = {lo:.6f}, gap_BK = {gap:.6f}")

print()
print("       [finding] the finest scale contributes mu = 0 at every poset measured.  Its edge")
print("                 set does not connect its own increment space — the 2x2 merges are single")
print("                 BK edges, and a function supported on one 2x2 fiber and orthogonal to")
print("                 the coarse flag has zero scale-l energy.  So even if a5.3's identity")
print("                 held, `gap_BK >= min_l mu_l` would read `gap_BK >= 0`.  The multiscale")
print("                 route as the note states it is not lossy; it is EMPTY, and it is empty")
print("                 for a reason visible at n = 4.")

# ---------------------------------------------------------------- a5.5

L.banner("a5.5  THE CURRENCY.  What a lower bound on gap_BK is worth in this programme")
print("""
  This is the ONE paragraph of `compression2.tex` at which the spectral closure is the right
  citation, and the ticket says so: those tickets apply if the note routes through the spectral
  gap and are silent otherwise.  The main body does not route through it.  This closing
  paragraph does, explicitly and by name.

    STATE.md:29  the bridge L1b "is NOT SPECTRAL IN ANY LOAD-BEARING SENSE" (mg-05ec §5), and
                 leg (ii): "nothing in this programme consumes a BK-gap LOWER bound" (mg-145f)
                 -- while a sharp lower bound is ALREADY PROVEN by someone else, Wilson 2004,
                 gap_BK >= (1 - cos(pi/n))/(n-1), verified FP at n = 4,5.

  So the object this paragraph aims at is a lower bound on `gap_BK`: the corpus records that
  nothing reads one and that a sharp one already exists in the literature.  a5.3 and a5.4 then
  measure that this route does not produce one at all.  Both halves have to be said -- "no
  consumer" alone would be a corpus search, and "the route is empty" alone would be a fact
  about an object nobody needed.
""")
L.verdict(True, "a5.5 is a citation, not a measurement",
          "STATE.md:29 and mg-145f quoted at the note's CLOSING paragraph only")

sys.exit(L.finish())
