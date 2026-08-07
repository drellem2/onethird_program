"""mg-200d V3 -- testing the (n-1)/3 conjecture past the brute-force horizon.

V2 computes the DISJUNCTIVE optimum exactly by visiting all `2^C(n,2)` branches.  That
stops at `n = 5` (1024 branches); `n = 6` is 32768 branches over 720 columns and is not run.

This script does the one thing that is still honest at `n = 6, 7`: it searches for a branch
that BEATS `(n-1)/3`.  Every value it prints is a LOWER bound on the disjunctive optimum, so

    * a value ABOVE (n-1)/3 would REFUTE the conjecture outright, and
    * a value equal to (n-1)/3 is only evidence, never a proof of the maximum.

That asymmetry is the whole point of the script and is printed with every line.

Two families, plus a randomised sweep:

  window w   -- x,y incomparable iff y - x <= w.  w = n-1 is the literal all-pairs form.
                This family contains the mechanism: an incomparable pair that is ALWAYS
                adjacent is forced by per-slot symmetry to have flip probability exactly
                1/2, which the 1/3 cap forbids -- so tight windows go infeasible.
  blocks b   -- consecutive blocks of size b, incomparable inside, comparable across.
"""

import sys
from fractions import Fraction as F

from lp200d import Infeasible, relaxation, measure_report, eps_spec, pairs_of

NS = [int(a) for a in sys.argv[1:]] or [4, 5, 6]
SEED, NRAND = 20260807, 60


def rng_stream(seed):
    """Deterministic LCG -- no Date/random dependence, so runs reproduce exactly."""
    s = seed
    while True:
        s = (1103515245 * s + 12345) % (2 ** 31)
        yield s


def evaluate(n, comp, label, target):
    try:
        val, mu = relaxation(n, "slot_eq", comparable=frozenset(comp))
    except Infeasible as e:
        print(f"    {label:26s} INFEASIBLE ({e})")
        return None
    rep = measure_report(n, mu)
    flag = "BEATS (n-1)/3" if val > target else ("= (n-1)/3" if val == target else "below")
    print(f"    {label:26s} E[inv] = {str(val):>8}  eps_spec = {str(eps_spec(n, val)):>7}"
          f"  |I| = {len(pairs_of(n)) - len(comp):>2}  atoms {len(mu):>3}"
          f"  max flip {rep['max_flip']}   {flag}")
    return val


print("=" * 78)
print("V3  LOWER-BOUND SEARCH for a branch beating (n-1)/3.  Every number below is a")
print("    LOWER bound on the disjunctive optimum -- it can refute the conjecture,")
print("    it can never confirm it.")
print("=" * 78)

for n in NS:
    prs = pairs_of(n)
    target = F(n - 1, 3)
    print(f"\n### n = {n}   (n-1)/3 = {target}   baseline C(n,2)/3 = {F(n * (n - 1), 6)}")
    best, best_lbl = None, None

    print("  window families:")
    for w in range(1, n):
        comp = [(x, y) for (x, y) in prs if y - x > w]
        v = evaluate(n, comp, f"window w={w}", target)
        if v is not None and (best is None or v > best):
            best, best_lbl = v, f"window w={w}"

    print("  block families:")
    for b in range(2, n + 1):
        comp = [(x, y) for (x, y) in prs if x // b != y // b]
        v = evaluate(n, comp, f"blocks b={b}", target)
        if v is not None and (best is None or v > best):
            best, best_lbl = v, f"blocks b={b}"

    print(f"  randomised sweep ({NRAND} branches, LCG seed {SEED}):")
    g = rng_stream(SEED + n)
    hits = []
    for t in range(NRAND):
        # bit 16, not bit 0 -- an LCG's low bit is periodic and gave 0/60 feasible at n=4
        comp = [pr for pr in prs if (next(g) >> 16) % 2 == 0]
        try:
            val, _ = relaxation(n, "slot_eq", comparable=frozenset(comp))
        except Infeasible:
            continue
        hits.append((val, tuple(sorted(comp))))
        if best is None or val > best:
            best, best_lbl = val, f"random #{t}"
    if hits:
        mx = max(v for v, _ in hits)
        print(f"    {len(hits)}/{NRAND} feasible, max E[inv] = {mx}"
              f"   {'BEATS (n-1)/3' if mx > target else '<= (n-1)/3'}")
    else:
        print(f"    0/{NRAND} feasible")

    verdict = "REFUTED" if (best is not None and best > target) else "not refuted"
    print(f"  ==> best found at n={n}: {best} on {best_lbl};  conjecture (n-1)/3 = {target}"
          f" is {verdict} by this search")
    sys.stdout.flush()


# ---------------------------------------------------------------------------------------
# THE LOWER BOUND, EXPLICIT AND FOR EVERY n.
#
# DEFECT OF THIS INSTRUMENT, LEFT IN THE FILE.  My first guess at the general construction
# was to 3-colour the n-1 consecutive pairs by index mod 3 and take the three products of
# transpositions.  It hits E[inv] = (n-1)/3 and the 1/3 cap at every n -- and it VIOLATES
# per-slot symmetry from n = 4 up.  This check caught it; the value and the cap agreeing is
# exactly the coincidence that would have let a construction with no symmetry check through.
#
#     def fence_atoms_WRONG(n):                        # kept as the refuted version
#         atoms = {}
#         for r in range(3):
#             p = list(range(n))
#             for i in range(r, n - 1, 3):
#                 p[i], p[i + 1] = p[i + 1], p[i]
#             atoms[tuple(p)] = atoms.get(tuple(p), F(0)) + F(1, 3)
#         return atoms
#
# The right shape is the one the LP itself returned at n = 3, 4 and 5, which I then read off
# rather than guessed: the IDENTITY, plus the two matchings of consecutive pairs (even
# indices, odd indices), mass 1/3 each.  Each consecutive pair is flipped in exactly one of
# the two matchings, so q = 1/3 for all n-1 of them and E[inv] = (n-1)/3; and at every slot k
# the identity supplies J_k(k,k+1) = 1/3 while whichever matching owns index k supplies
# J_k(k+1,k) = 1/3, which is the symmetry.  Every other adjacency it creates is at distance
# 3, hence on a COMPARABLE pair, which carries no constraint.
#
# Checked here DIRECTLY -- no LP -- so it is a construction, not a solver output.
# ---------------------------------------------------------------------------------------

def fence_atoms(n):
    atoms = {tuple(range(n)): F(1, 3)}
    for r in (0, 1):
        p = list(range(n))
        for i in range(r, n - 1, 2):
            p[i], p[i + 1] = p[i + 1], p[i]
        atoms[tuple(p)] = atoms.get(tuple(p), F(0)) + F(1, 3)
    return atoms


print()
print("=" * 78)
print("V3b  THE (n-1)/3 LOWER BOUND, CHECKED DIRECTLY AT EVERY n IN RANGE (no LP)")
print("     3 atoms: the identity, plus the even- and odd-index matchings of consecutive pairs.")
print("=" * 78)
allok = True
for n in range(3, 21):
    mu = fence_atoms(n)
    rep = measure_report(n, mu)
    I = {(i, i + 1) for i in range(n - 1)}
    tgt = F(n - 1, 3)
    ok_mass = rep["mass"] == 1
    ok_val = rep["E_inv"] == tgt
    ok_cap = rep["max_flip"] <= F(1, 3)
    ok_comp = all(pr in rep["zero_flip_pairs"] for pr in pairs_of(n) if pr not in I)
    ok_sym = all(pr not in I for (pr, _k) in rep["slot_eq_violations"])
    ok = ok_mass and ok_val and ok_cap and ok_comp and ok_sym
    allok = allok and ok
    print(f"  n={n:>2}  atoms {len(mu)}  E[inv] = {str(rep['E_inv']):>7} (target {str(tgt):>7})"
          f"  max flip {rep['max_flip']}"
          f"  comparable-never-flipped {ok_comp}  per-slot-symmetric on I {ok_sym}"
          f"   -> {'OK' if ok else 'FAILS'}")
print(f"  ==> lower bound (n-1)/3 {'HOLDS' if allok else 'FAILS'} on every n checked (3..20)")
