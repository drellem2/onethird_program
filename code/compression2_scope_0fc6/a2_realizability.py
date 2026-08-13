"""a2 — THE CRUX.  Does compression2's construction inject REALIZABILITY, or only appear to?

The ticket's addendum names this the question the whole note should be priced against:

    "Does 'design them via poset structure' actually inject realizability, or does it only
     appear to?  A compression parameterised by the poset still has to CONSTRAIN something an
     abstract frozen measure could not satisfy.  If it does, that is the first realizability
     lever this programme has had.  If it does not, say exactly where the poset-dependence
     washes out."

The test is operational, not rhetorical.  A REALIZABILITY ORACLE decides whether a measure on
`S_n` is the uniform linear-extension measure of some poset; it is exact and it is controlled.
Then the note's entire chain is run on measures the oracle says are NOT realizable.  If every
step still holds, the chain cannot distinguish a poset from a frozen measure, and it injects
nothing.
"""
import sys
from fractions import Fraction
from itertools import combinations, permutations

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import lib0fc6 as L  # noqa: E402


# ------------------------------------------------------------------ the realizability oracle

def realizable(mu, n):
    """Is `mu` the UNIFORM measure on `L(P)` for some poset `P` on n elements?

    EXACT and constructive.  If `S = supp(mu)` is `L(P)` for some `P`, then that `P` is forced:
    it is the intersection of the orders in `S` (`x < y` iff x precedes y in EVERY member).
    So the test is: (i) `mu` uniform on `S`; (ii) `L(intersection of S) == S`.  No search over
    posets is needed, and no poset can be missed.
    """
    S = [Lx for Lx, w in mu.items() if w > 0]
    if not S:
        return False, "empty support"
    w0 = mu[S[0]]
    if any(mu[Lx] != w0 for Lx in S):
        return False, "not uniform on its support"
    lt = [[True] * n for _ in range(n)]
    for i in range(n):
        lt[i][i] = False
    for Lx in S:
        pos = [0] * n
        for t, x in enumerate(Lx):
            pos[x] = t
        for x in range(n):
            for y in range(n):
                if x != y and pos[x] > pos[y]:
                    lt[x][y] = False
    got = set(L.linear_extensions(n, lt))
    if got != set(S):
        return False, f"support is not L(P): |L(P)|={len(got)} vs |supp|={len(S)}"
    return True, "uniform on L(P)"


L.banner("a2.1  CONTROL — the realizability oracle on cases whose answer is known")
ok = True
for n in (3, 4, 5):
    for lt in L.all_posets(n):
        LEs = L.linear_extensions(n, lt)
        mu = {Lx: Fraction(1, len(LEs)) for Lx in LEs}
        r, why = realizable(mu, n)
        if not r:
            ok = False
            print(f"    MISS: a genuine LE measure at n={n} was rejected ({why})")
L.verdict(ok, "every uniform linear-extension measure at n <= 5 is accepted",
          f"{len(L.all_posets(3))+len(L.all_posets(4))+len(L.all_posets(5))} posets")

# and it must REJECT things.  Three planted non-realizable measures.
n = 4
perms = list(permutations(range(n)))
bad_cases = []
# (i) non-uniform on a genuine L(P)
LEs = L.linear_extensions(n, L.tclose(n, [(0, 1)]))
mu = {Lx: Fraction(1, len(LEs)) for Lx in LEs}
mu[LEs[0]] = mu[LEs[0]] + Fraction(1, 100)
mu[LEs[1]] = mu[LEs[1]] - Fraction(1, 100)
bad_cases.append(("non-uniform on a genuine L(P)", mu))
# (ii) a support that is not any poset's L(P)
mu2 = {Lx: Fraction(0) for Lx in perms}
mu2[(0, 1, 2, 3)] = Fraction(1, 2)
mu2[(3, 2, 1, 0)] = Fraction(1, 2)
bad_cases.append(("two antipodal atoms (the corpus's two-atom law)", mu2))
# (iii) the mixture witness
bad_cases.append(("(2/3)Unif + (1/3)delta_L*", L.mixture_witness(n, Fraction(2, 3))))
for label, m in bad_cases:
    r, why = realizable(m, n)
    L.verdict(not r, f"REJECTED: {label}", why)

# ------------------------------------------------------------------ the note's chain on a fake

L.banner("a2.2  THE NOTE'S ENTIRE CHAIN, RUN ON A MEASURE THAT IS NOT A POSET'S")


def run_note_chain(mu, n, star):
    """Every step of compression2.tex, evaluated on an arbitrary measure `mu` on `S_n`.

    Returns a dict of the note's own quantities.  NOTHING in here reads a poset: the only
    inputs are `mu` and `L*`.  That is the finding, stated as code.
    """
    nodes = L.dyadic_nodes(n)
    pp = L.pair_probs_measure(mu, n)
    hyp = L.max_flip_against(pp, star)                       # (1)
    # (2): inv_{L*} = sum_B K_B, pointwise
    id2 = all(L.inv_against(Lx, star) == sum(L.word_inv(w)
                                             for w in L.merge_words(Lx, star, nodes))
              for Lx, w in mu.items() if w > 0)
    # (3): K_B = prefix area, pointwise
    id3 = all(L.word_inv(w) == L.word_prefix_area(w)
              for Lx, wt in mu.items() if wt > 0
              for w in L.merge_words(Lx, star, nodes))
    # (4): E K_B <= |A||C|/3 at every node
    ek = {}
    for nd in nodes:
        tot = Fraction(0)
        for Lx, wt in mu.items():
            if wt > 0:
                tot += wt * L.word_inv(L.merge_words(Lx, star, [nd])[0])
        ek[nd] = tot
    id4 = all(ek[(lo, mid, hi)] <= Fraction((mid - lo) * (hi - mid), 3)
              for (lo, mid, hi) in nodes)
    # (5): H(W_B) <= note bound, at every BALANCED node
    id5 = True
    for (lo, mid, hi) in nodes:
        if mid - lo != hi - mid:
            continue
        dist = {}
        for Lx, wt in mu.items():
            if wt > 0:
                w = L.merge_words(Lx, star, [(lo, mid, hi)])[0]
                dist[w] = dist.get(w, Fraction(0)) + wt
        if L.entropy_bits(dist.values()) > L.note_word_bound(mid - lo) + 1e-12:
            id5 = False
    # (6): H(mu) <= 0.9399 n log2 n
    Hmu = L.entropy_bits([w for w in mu.values() if w > 0])
    id6 = Hmu <= L.note_headline_bound(n) + 1e-12
    return {"(1) max flip": hyp, "(2)": id2, "(3)": id3, "(4)": id4, "(5)": id5,
            "(6)": id6, "H": Hmu}


for n in (4, 6, 8):
    star = tuple(range(n))
    mu = L.mixture_witness(n, Fraction(2, 3))
    r, why = realizable(mu, n)
    res = run_note_chain(mu, n, star)
    L.verdict(not r, f"n={n}: the witness is NOT a linear-extension measure", why)
    L.verdict(res["(1) max flip"] <= Fraction(1, 3),
              f"n={n}: it SATISFIES hypothesis (1)", f"max flip = {res['(1) max flip']}")
    for k in ("(2)", "(3)", "(4)", "(5)", "(6)"):
        L.verdict(res[k], f"n={n}: compression2 {k} holds on it verbatim")
    print(f"       H(mu) = {res['H']:.4f} bits   note bound (6) = "
          f"{L.note_headline_bound(n):.4f}   log2 n! = {L.log2_factorial(n):.4f}")

print()
print("       [finding] every step of the note holds for a measure that is not any poset's.")
print("                 The chain reads P through (1) ALONE, and (1) is a statement about the")
print("                 measure's PAIR MARGINALS.  That is the corpus's information set M_n")
print("                 (STATE.md:21), not a realizability fact.")

# ------------------------------------------------------- the note cannot even SEE the difference

L.banner("a2.3  TWO MEASURES WITH IDENTICAL PAIR MARGINALS — one realizable, one not")
# If a realizable mu1 and a non-realizable mu2 have the SAME pair-marginal vector, then every
# quantity the note's chain bounds is bounded by the SAME number for both, because (1) is the
# only input.  The stronger statement is that the note's OUTPUT is identical; that is what is
# measured here.
n = 4
perms = list(permutations(range(n)))
pairs = list(combinations(range(n), 2))


def flagvec(Lx):
    pos = [0] * n
    for t, x in enumerate(Lx):
        pos[x] = t
    return tuple(1 if pos[i] < pos[j] else 0 for (i, j) in pairs)


# The base measure is a member of the HYPOTHESIS POPULATION — a poset that actually satisfies
# (1) — not the antichain, whose max flip is 1/2 and which therefore sits outside the note's
# standing assumption.  D4 KEPT: my first version used the antichain and demonstrated the point
# on a measure the note's own hypothesis excludes.
def find_kernel(LEs, n, lt):
    """A COMMUTING SQUARE: `L`, `L·s`, `L·t`, `L·s·t` for two DISJOINT legal adjacent swaps.

    `s` flips exactly one incomparable pair and `t` another, and the two pairs are disjoint, so
    `flag(L) + flag(L·s·t) = flag(L·s) + flag(L·t)` COORDINATE BY COORDINATE — an exact kernel
    direction of the pair-marginal map, with all four orders inside `L(P)`.
    """
    for Lx in LEs:
        ps = L_bk(Lx, n, lt)
        for p in ps:
            for q in ps:
                if q < p + 2:
                    continue
                A = Lx
                B = L.swap(L.swap(Lx, p), q)
                C = L.swap(Lx, p)
                D = L.swap(Lx, q)
                if len({A, B, C, D}) == 4 and all(x in set(LEs) for x in (A, B, C, D)):
                    return (A, B, C, D)
    return None


L_bk = L.bk_edges

base = None
kernel = None
for nn in (4, 5, 6):
    for lt0 in L.all_posets(nn):
        LE0 = L.linear_extensions(nn, lt0)
        if len(LE0) < 4:
            continue
        s0 = L.coherent_order(LE0, nn)
        if s0 is None:
            continue
        if L.max_flip_against(L.pair_probs(LE0, nn), s0) > Fraction(1, 3):
            continue
        k0 = find_kernel(LE0, nn, lt0)
        if k0 is not None:
            base = (nn, lt0, LE0, s0)
            kernel = k0
            break
    if base is not None:
        break
L.verdict(base is not None, "a hypothesis-population poset with a kernel square exists",
          f"n = {base[0] if base else '-'}, e(P) = {len(base[2]) if base else '-'}")
n, lt, LEs, star_h = base
perms = list(permutations(range(n)))
pairs = list(combinations(range(n), 2))
L.verdict(kernel is not None, "a pair-marginal kernel direction exists over that support",
          str(kernel))
mu1 = {Lx: Fraction(1, len(LEs)) for Lx in LEs}
eps = Fraction(1, 4 * len(LEs))
mu2 = dict(mu1)
a, b, c, d = kernel
mu2[a] = mu2.get(a, Fraction(0)) + eps
mu2[b] = mu2.get(b, Fraction(0)) + eps
mu2[c] -= eps
mu2[d] -= eps
same = L.pair_probs_measure(mu1, n) == L.pair_probs_measure(mu2, n)
r1, _ = realizable(mu1, n)
r2, why2 = realizable(mu2, n)
L.verdict(same, "mu1 and mu2 have IDENTICAL pair marginals")
L.verdict(r1, "mu1 IS a linear-extension measure")
L.verdict(not r2, "mu2 is NOT a linear-extension measure", why2)
star = star_h
res1 = run_note_chain(mu1, n, star)
res2 = run_note_chain(mu2, n, star)
L.verdict(res1["(1) max flip"] <= Fraction(1, 3),
          "BOTH sit inside hypothesis (1)", f"max flip = {res1['(1) max flip']}")
L.verdict(res1["(1) max flip"] == res2["(1) max flip"],
          "the note's ONLY input, (1), takes the same value on both",
          f"{res1['(1) max flip']}")
L.verdict(all(res1[k] == res2[k] for k in ("(2)", "(3)", "(4)", "(5)", "(6)")),
          "every step of the note returns the same verdict on both")
print(f"       H(mu1) = {res1['H']:.6f}   H(mu2) = {res2['H']:.6f}  "
      f"— the MEASURES differ; the note's INPUT does not.")

print()
print("       [finding] P5 CONFIRMED.  The poset-dependence washes out at exactly one place:")
print("                 L* and (1) are both functions of the PAIR MARGINALS, and the dyadic")
print("                 tree is a function of L*.  Nothing downstream reads P again.")

sys.exit(L.finish())
