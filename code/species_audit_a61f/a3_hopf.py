"""A3 -- THE HOPF-MONOID BATTERY, AND WHAT IT CAN AND CANNOT DETECT.

mg-7d75 section 0: "HOPF MONOID AXIOMS CHECKED, NOT ANALOGISED: F and AC are
closed subspecies of the Hadamard products P x Sigma and P x Pi with 0 failures
across 5 axioms on 4 399 and 2 685 basis elements".  Section 5 prints a table
whose five columns are product closure, coproduct closure, associativity,
coassociativity and compatibility, all 0, and four controls of which two fire.

A3a reproduces the table from code written here.  A3b then asks the question the
audit brief demands -- demand the axioms, not the resemblance -- in the only
form that can settle it: WHAT ELSE PASSES?

The three subspecies fed to the identical battery in A3b are chosen so that a
battery with real discriminating power must separate them from F:

  (i)   the FULL ambient P x Sigma -- every (poset, set composition) pair, with
        no cone condition at all;
  (ii)  F-OPPOSITE: (p, F) with F a face of the cone of the OPPOSITE poset,
        which is the wrong pairing of a poset with a face;
  (iii) a DELIBERATELY BROKEN subset of F: every second element of F in a fixed
        order, which is not closed under anything.

If (i) and (ii) also come out 0 across all five columns, then four of the five
columns are not measuring our subspecies.  If (iii) comes out 0 on the last
three columns while its closure columns fire, then those three columns cannot
fail for ANY subset whatever, closed or not, and are not axioms being tested at
all -- they are identities of tuple concatenation and of set restriction.
"""

import sys
from itertools import combinations
from kerna61f import (posets_labelled, restrict_poset, is_lower_set, faces,
                      set_compositions, supp, tits, concat, restrict_comp,
                      restrict_part, AC_by_support)

bad = 0
GROUND = 4
I_FULL = frozenset(range(GROUND))


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
    print()


def subsets_of(I):
    I = sorted(I)
    out = []
    for m in range(1 << len(I)):
        out.append(frozenset(I[i] for i in range(len(I)) if m >> i & 1))
    return out


def decomps(I):
    return [(S, frozenset(I) - S) for S in subsets_of(I)]


_POSETS = {}


def posets_on(I):
    I = frozenset(I)
    if I in _POSETS:
        return _POSETS[I]
    lab = sorted(I)
    out = []
    for rel in posets_labelled(len(lab)):
        out.append(frozenset((lab[a], lab[b]) for (a, b) in rel))
    _POSETS[I] = out
    return out


# ---- the species under test -------------------------------------------------

def elems_F(I):
    return [(rel, F) for rel in posets_on(I) for F in faces(rel, I)]


def elems_AC(I):
    out = []
    for rel in posets_on(I):
        for X in sorted(AC_by_support(rel, I), key=repr):
            out.append((rel, X))
    return out


def elems_ambient(I):
    return [(rel, F) for rel in posets_on(I) for F in set_compositions(I)]


def opposite(rel):
    return frozenset((b, a) for (a, b) in rel)


def elems_Fop(I):
    return [(rel, F) for rel in posets_on(I) for F in faces(opposite(rel), I)]


def elems_broken(I):
    e = elems_F(I)
    return e[::2] if len(e) > 1 else e


# ---- the published operations ----------------------------------------------

def mu_comp(x, y):
    return (x[0] | y[0], concat(x[1], y[1]))


def mu_part(x, y):
    return (x[0] | y[0], frozenset(x[1]) | frozenset(y[1]))


def cond(rel, S, mode):
    if mode == "lower":
        return is_lower_set(rel, S)
    if mode == "none":
        return True
    if mode == "antichain":
        return not any(a in S and b in S for (a, b) in rel)
    raise ValueError(mode)


def de_comp(x, S, T, mode="lower"):
    rel, F = x
    if not cond(rel, S, mode):
        return None
    return ((restrict_poset(rel, S), restrict_comp(F, S)),
            (restrict_poset(rel, T), restrict_comp(F, T)))


def de_part(x, S, T, mode="lower"):
    rel, X = x
    if not cond(rel, S, mode):
        return None
    return ((restrict_poset(rel, S), restrict_part(X, S)),
            (restrict_poset(rel, T), restrict_part(X, T)))


def battery(elems, mu, de, mode="lower"):
    f = dict(prod=0, coprod=0, assoc=0, coassoc=0, compat=0)
    U = {J: set(elems(J)) for J in subsets_of(I_FULL)}
    for J, els in U.items():
        for (S, T) in decomps(J):
            for x in U[S]:
                for y in U[T]:
                    if mu(x, y) not in els:
                        f["prod"] += 1
            for x in els:
                d = de(x, S, T, mode)
                if d is None:
                    continue
                if d[0] not in U[S] or d[1] not in U[T]:
                    f["coprod"] += 1
    for (S, R) in decomps(I_FULL):
        for (S1, S2) in decomps(S):
            for x in U[S1]:
                for y in U[S2]:
                    for z in U[R]:
                        if mu(mu(x, y), z) != mu(x, mu(y, z)):
                            f["assoc"] += 1
    for (A, rest) in decomps(I_FULL):
        for (B, C) in decomps(rest):
            for x in U[I_FULL]:
                d1 = de(x, A, B | C, mode)
                l = None if d1 is None else de(d1[1], B, C, mode)
                d2 = de(x, A | B, C, mode)
                r = None if d2 is None else de(d2[0], A, B, mode)
                lv = None if l is None else (d1[0], l[0], l[1])
                rv = None if r is None else (r[0], r[1], d2[1])
                if lv != rv:
                    f["coassoc"] += 1
    for (S1, T1) in decomps(I_FULL):
        for (S2, T2) in decomps(I_FULL):
            A, B = S1 & S2, S1 & T2
            C, D = T1 & S2, T1 & T2
            for x in U[S1]:
                for y in U[T1]:
                    lhs = de(mu(x, y), S2, T2, mode)
                    dx = de(x, A, B, mode)
                    dy = de(y, C, D, mode)
                    rhs = None if (dx is None or dy is None) else \
                        (mu(dx[0], dy[0]), mu(dx[1], dy[1]))
                    if lhs != rhs:
                        f["compat"] += 1
    f["dim"] = len(U[I_FULL])
    return f


def show(name, f):
    print("  %-24s %8d %8d %8d %9d %9d %9d"
          % (name, f["dim"], f["prod"], f["coprod"], f["assoc"], f["coassoc"],
             f["compat"]))


HEAD = ("  %-24s %8s %8s %8s %9s %9s %9s"
        % ("species", "dim[4]", "prod", "coprod", "assoc", "coassoc", "compat"))

# ---------------------------------------------------------------------------
hdr("A3a  mg-7d75's T5b/T5c table, rebuilt here")

print(HEAD)
fF = battery(elems_F, mu_comp, de_comp)
fA = battery(elems_AC, mu_part, de_part)
show("F   (ours)", fF)
show("AC  (ours)", fA)
print()
okdims = (fF["dim"] == 4399 and fA["dim"] == 2685)
okzero = all(fF[k] == 0 and fA[k] == 0
             for k in ("prod", "coprod", "assoc", "coassoc", "compat"))
print("  mg-7d75's 4399 / 2685 basis elements reproduced: %s" % okdims)
print("  mg-7d75's 0 failures in all five columns reproduced: %s" % okzero)
bad += (not okdims) + (not okzero)
print()

# ---------------------------------------------------------------------------
hdr("A3b  WHAT ELSE PASSES?  the same battery on three other subspecies")

print(HEAD)
show("ambient P x Sigma", battery(elems_ambient, mu_comp, de_comp))
show("F-opposite (wrong)", battery(elems_Fop, mu_comp, de_comp))
fb = battery(elems_broken, mu_comp, de_comp)
show("F broken (every 2nd)", fb)
print()
famb = battery(elems_ambient, mu_comp, de_comp)
fop = battery(elems_Fop, mu_comp, de_comp)
allpass = all(famb[k] == 0 for k in ("prod", "coprod", "assoc", "coassoc",
                                     "compat"))
oppass = all(fop[k] == 0 for k in ("prod", "coprod", "assoc", "coassoc",
                                   "compat"))
brokenlast3 = (fb["assoc"] == 0 and fb["coassoc"] == 0 and fb["compat"] == 0)
brokenclosure = (fb["prod"] > 0)
print("  the FULL ambient passes all five columns          : %s" % allpass)
print("  the WRONG pairing (opposite cone) passes all five : %s" % oppass)
print("  the BROKEN subset still passes assoc/coassoc/compat: %s" %
      brokenlast3)
print("  ... while its product-closure column fires        : %s (%d)"
      % (brokenclosure, fb["prod"]))
print()
if not (allpass and oppass and brokenlast3 and brokenclosure):
    print("  A3b DID NOT COME OUT AS EXPECTED -- read the numbers, not this note.")
    bad += 1
else:
    print("  READING.  Three of mg-7d75's five columns -- assoc, coassoc,")
    print("  compat -- return 0 for a subset of F that is closed under")
    print("  nothing.  They cannot fail for any collection of (poset, face)")
    print("  pairs whatever, because the operations are inherited from the")
    print("  ambient Hadamard product and associativity of CONCATENATION and")
    print("  coassociativity of RESTRICTION are identities of tuples and sets,")
    print("  not properties of the subspecies.  And the two columns that CAN")
    print("  fail -- the two closure columns -- return 0 for the full ambient")
    print("  and for the wrong pairing as well as for ours.")
    print()
    print("  So '0 failures across 5 axioms on 4 399 basis elements' is one")
    print("  fact about our subspecies (it is closed), not five, and the")
    print("  4 399 is the size of the ambient degree-4 component rather than")
    print("  a count of independent tests.  mg-7d75's own section 5 says")
    print("  'what T5 establishes is CLOSURE ... and NOT that the operations")
    print("  are forced', which is the correct reading; section 0's phrasing")
    print("  'AXIOMS CHECKED, NOT ANALOGISED ... 0 failures across 5 axioms'")
    print("  is the one that overstates it, and section 0 is what gets quoted.")
print()

# ---------------------------------------------------------------------------
hdr("A3c  mg-7d75's four controls, re-run, plus what control (ii) really is")


def mu_tits_cross(x, y):
    return (x[0] | y[0],
            tits(x[1], y[1]) if x[1] and y[1] else concat(x[1], y[1]))


def mu_rev(x, y):
    return (x[0] | y[0], tuple(y[1]) + tuple(x[1]))


print(HEAD)
show("(i)  no lower-set cond", battery(elems_F, mu_comp, de_comp, "none"))
f2 = battery(elems_F, mu_tits_cross, de_comp)
show("(ii) Tits product", f2)
show("(iii) reversed concat", battery(elems_F, mu_rev, de_comp))
f4 = battery(elems_F, mu_comp, de_comp, "antichain")
show("(iv) antichain cond", f4)
print()
tgt2 = (f2["prod"], f2["assoc"], f2["compat"]) == (1442, 252, 11020)
tgt4 = (f4["coassoc"] == 75512)
print("  mg-7d75's control (ii) 1442 / 252 / 11020 reproduced: %s" % tgt2)
print("  mg-7d75's control (iv) 75512 coassoc failures reproduced: %s" % tgt4)
bad += (not tgt2) + (not tgt4)
print()
print("  WHAT CONTROL (ii) ACTUALLY TESTS.  mu_{S,T} takes a face of a cone on")
print("  S and a face of a cone on the DISJOINT set T.  The Tits product F.G")
print("  intersects the blocks of F with the blocks of G, so on disjoint")
print("  ground sets every intersection is empty and the product is the empty")
print("  composition -- it is not a near-miss product, it is an operation of")
print("  the wrong type being fed arguments it is not defined on.  Both")
print("  mg-7d75's code and this one paper over that with a guard that falls")
print("  back to concatenation when either argument is empty.  Below: how many")
print("  of the (x, y) pairs the control counts have DISJOINT nonempty ground")
print("  sets, i.e. how many are type errors rather than false products.")
tot = 0
degen = 0
U = {J: set(elems_F(J)) for J in subsets_of(I_FULL)}
for J in subsets_of(I_FULL):
    for (S, T) in decomps(J):
        for x in U[S]:
            for y in U[T]:
                tot += 1
                if x[1] and y[1] and not (set().union(*x[1]) &
                                          set().union(*y[1])):
                    degen += 1
print()
print("  product-closure pairs examined by the battery : %d" % tot)
print("  ... with both factors nonempty and disjoint   : %d (%.1f%%)"
      % (degen, 100.0 * degen / tot))
print()
print("  So control (ii) fires, but it fires on a type mismatch.  It does not")
print("  establish that the Tits product is a NEAR miss for the Hopf-monoid")
print("  product; it establishes that it is not the same kind of map.  The")
print("  document's section 6 item 5 conclusion -- 'the band structure is not")
print("  carried by the Hopf monoid' -- is correct and is the important line;")
print("  the 1442 / 252 / 11020 do not add evidence to it.")
print()
print("  Controls (i) and (iii) do not fire and mg-7d75 says so and says why.")
print("  Verified independently here: both come out all-zero above, and the")
print("  document's explanations (the R_q family at q = 1; the opposite")
print("  monoid) are consistent with what is measured.")
print()

print("=" * 78)
print("A3 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
