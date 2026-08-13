"""a0 — CONTROLS.  Nothing below this file's exit status is worth reading.

Four planted-wrong worlds and a set of plug-backs.  The point of the planted worlds is that
this ticket's headline is a NEGATIVE (`the note is realizability-blind`), and a detector that
cannot distinguish "no separation exists" from "my detector is broken" would return that
headline on a broken detector.  So the separation detector is tested on a population where the
answer it wants is NOT the one it gets.
"""
import sys
from fractions import Fraction
from itertools import permutations

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import lib0fc6 as L  # noqa: E402

L.banner("a0.1  poset enumeration plugs back to published counts")
# Labelled strict orders on n elements: 1, 1, 3, 19, 219, 4231, 130023 (OEIS A001035).
PUBLISHED = {1: 1, 2: 3, 3: 19, 4: 219, 5: 4231, 6: 130023}
for n in (1, 2, 3, 4, 5, 6):
    got = len(L.all_posets(n))
    L.verdict(got == PUBLISHED[n], f"labelled posets n={n}", f"{got} (published {PUBLISHED[n]})")

L.banner("a0.2  linear-extension counts plug back to known values")
for n in range(1, 7):
    ch = L.chain(n)
    ac = L.antichain(n)
    ne_ch = len(L.linear_extensions(n, ch))
    ne_ac = len(L.linear_extensions(n, ac))
    fact = 1
    for k in range(2, n + 1):
        fact *= k
    L.verdict(ne_ch == 1, f"e(chain_{n}) = 1", str(ne_ch))
    L.verdict(ne_ac == fact, f"e(antichain_{n}) = {n}!", str(ne_ac))

L.banner("a0.3  word statistics: inv and the prefix area agree, and both are right by hand")
HAND = {"CA": 1, "AC": 0, "ACCA": 2, "AACC": 0, "CCAA": 4, "CACA": 3}
for w, want in HAND.items():
    gi = L.word_inv(w)
    ga = L.word_prefix_area(w)
    L.verdict(gi == want, f"inv({w}) = {want}", str(gi))
    L.verdict(ga == want, f"prefix-area({w}) = {want}  [compression2 (3)]", str(ga))

L.banner("a0.4  the note's own numbers reproduce")
L.verdict(abs(1 / (24 * 2.718281828459045 ** 0 * __import__("math").log(2)) - 0.06011) < 5e-5,
          "1/(24 ln 2) = 0.06011...", f"{1/(24*__import__('math').log(2)):.5f}")
L.verdict(abs(L.NOTE_CONST - 0.9399) < 5e-5, "1 - 1/(24 ln 2) = 0.9399 (note line 113)",
          f"{L.NOTE_CONST:.5f}")

L.banner("a0.5  PLANTED WORLD 1 — a wrong decoder must be caught")
# If the decoder ignored one node's word the round trip would break somewhere.
n = 6
lt = L.antichain(n)
star = tuple(range(n))
nodes = L.dyadic_nodes(n)
LEs = L.linear_extensions(n, lt)
bad = 0
for Lx in LEs:
    w = list(L.merge_words(Lx, star, nodes))
    w[0] = "A" * w[0].count("A") + "C" * w[0].count("C")  # clobber the ROOT word
    if L.decode_merge_words(tuple(w), star, nodes) != Lx:
        bad += 1
L.verdict(bad > 0, "clobbering the root word breaks the round trip (detector is alive)",
          f"{bad} of {len(LEs)} broken")

L.banner("a0.6  PLANTED WORLD 2 — the separation detector on a population where it SHOULD fire")
# The detector in a3 asks: does any step of the note's chain distinguish a linear-extension
# measure from a non-realizable measure?  Here it is handed two measures a statistic DOES
# separate, and it must say so.  D1 KEPT: my first version of this control compared the
# ANTICHAIN's measure with the mixture witness, and both have full support 720 — a control
# that could not fire, planted inside the arm whose subject is whether a detector can fire.
lt_rel = L.tclose(4, [(0, 1)])
LE_rel = L.linear_extensions(4, lt_rel)
mu_real = {Lx: Fraction(1, len(LE_rel)) for Lx in LE_rel}
mu_fake = L.mixture_witness(4, Fraction(2, 3))
s_real = len([w for w in mu_real.values() if w > 0])
s_fake = len([w for w in mu_fake.values() if w > 0])
L.verdict(s_real != s_fake, "a genuinely separating statistic IS detected as separating",
          f"|supp| {s_real} (poset 0<1, n=4) vs {s_fake} (mixture)")

L.banner("a0.7  PLANTED WORLD 3 — a wrong-direction world for the entropy lemma")
# If the constraint ran the WRONG way (E inv >= m^2/3 instead of <=) the lemma must not hold.
# Uniform words have E inv = m^2/2 > m^2/3 and entropy exactly log2 C(2m, m), which EXCEEDS
# the note's bound.  If it did not, the lemma would be vacuous.
import math  # noqa: E402
# D2 KEPT: my first version of this block read `verdict(a > b - 1e-9 or a <= b, ...)` — A ROW
# THAT CANNOT FAIL, planted inside the gate, which is mg-8d66's own D2 reproduced.  Replaced by
# the check that actually has content.
for m in (32, 64, 128):
    unif = math.log2(math.comb(2 * m, m))
    L.verdict(unif > L.note_word_bound(m),
              f"m={m}: the UNCONSTRAINED word EXCEEDS the note's bound (the bound has content)",
              f"H_unif={unif:.4f} > bound={L.note_word_bound(m):.4f}")
cross = next(m for m in range(2, 400) if math.log2(math.comb(2 * m, m)) > L.note_word_bound(m))
print(f"       [note] the crossover is m = {cross}: below it the note's per-node bound is "
      f"WEAKER than the free bound log2 C(2m,m), i.e. it says nothing at small blocks")
for m in (8, 16, 32):
    L.verdict(L.note_word_bound(m) < 2 * m, f"m={m}: note bound < 2m (non-vacuous vs 2m bits)",
              f"{L.note_word_bound(m):.4f} < {2*m}")

L.banner("a0.8  PLANTED WORLD 4 — max-entropy solver on a problem with a known answer")
# With cap = 1/2 every measure on S_n satisfies the constraint (uniform is feasible and is the
# unconstrained maximiser), so the answer must be exactly log2(n!).
for n2 in (3, 4):
    H, mu, worst = L.max_entropy_in_Mn(n2, cap=Fraction(1, 2), iters=3000)
    want = L.log2_factorial(n2)
    L.verdict(abs(H - want) < 1e-6, f"cap=1/2 at n={n2} recovers log2({n2}!)",
              f"{H:.9f} vs {want:.9f}")
# and with cap = 0 the only feasible measure is the point mass on L*, entropy 0.  The dual
# optimum there is at theta = infinity, so convergence is asymptotic and the tolerance is
# stated rather than hidden: 1e-2 bits, reached in 40 000 iterations.
H0, _, _ = L.max_entropy_in_Mn(3, cap=Fraction(0), iters=40000, lr=8.0)
L.verdict(H0 < 1e-2, "cap=0 at n=3 collapses to the point mass (H -> 0, tol 1e-2 bits)",
          f"{H0:.6f}")

sys.exit(L.finish())
