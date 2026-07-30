"""mg-66a6 AUDIT, target 1: every number in the worked example of
docs/OneThird-Semigroup-Walk-Family-Note.md, recomputed from the definitions.

P = {a<b, c<d} on {a,b,c,d}.  Nothing here reads note_check.py; the note's
claimed values are hard-coded below as EXPECTATIONS and compared at the end.
"""

import sys
from fractions import Fraction

from audit_lib import (poset, orderings, moves, act, product, level, levels,
                       lstr, mstr, multiplicities, eigenvalue,
                       transition_matrix, nullity, sub_scalar, induced,
                       n_orderings, refines, acyclic_partitions,
                       set_partitions, _lkey, at_laplacian, at_graph,
                       sgn, inversions, connected, mat_vec, rank_Q)

FAIL = []
CHECKS = [0]


def check(label, got, want):
    CHECKS[0] += 1
    ok = got == want
    print("  [%s] %s" % ("OK " if ok else "FAIL", label))
    if not ok:
        print("        note says : %r" % (want,))
        print("        recomputed: %r" % (got,))
        FAIL.append(label)
    return ok


A, B, C, D = 0, 1, 2, 3          # a, b, c, d
P = poset(4, [(A, B), (C, D)])
NAMES = "abcd"


def w(word):
    """'abcd' -> the ordering tuple."""
    return tuple(NAMES.index(ch) for ch in word)


def mv(spec):
    """'ac|bd' -> the move tuple."""
    return tuple(frozenset(NAMES.index(ch) for ch in blk)
                 for blk in spec.split("|"))


def lv(spec):
    return frozenset(mv(spec))


print(__doc__)
print("=" * 78)
print("SECTION A -- the orderings and the moves (note section 3)")
print("=" * 78)

ords = orderings(P)
print("  orderings:", " ".join("".join(NAMES[e] for e in c) for c in ords))
check("6 orderings", len(ords), 6)
check("the orderings are the note's list",
      sorted("".join(NAMES[e] for e in c) for c in ords),
      sorted(["abcd", "acbd", "acdb", "cabd", "cadb", "cdab"]))

MV = moves(P)
allosp = list(__import__("audit_lib").ordered_set_partitions(range(4)))
check("75 ordered set partitions of a 4-set", len(allosp), 75)
check("26 of them are P-compatible", len(MV), 26)

byk = {}
for x in MV:
    byk.setdefault(len(x), []).append(x)
print("  block-count profile:", {k: len(v) for k, v in sorted(byk.items())})
check("block-count profile 1/7/12/6",
      [len(byk[k]) for k in (1, 2, 3, 4)], [1, 7, 12, 6])

note_moves = {
    1: ["abcd"],
    2: ["abc|d", "ab|cd", "acd|b", "ac|bd", "a|bcd", "cd|ab", "c|abd"],
    3: ["ab|c|d", "ac|b|d", "a|bc|d", "a|b|cd", "ac|d|b", "a|cd|b", "a|c|bd",
        "c|ab|d", "cd|a|b", "c|ad|b", "c|a|bd", "c|d|ab"],
    4: ["a|b|c|d", "a|c|b|d", "a|c|d|b", "c|a|b|d", "c|a|d|b", "c|d|a|b"],
}
for k in (1, 2, 3, 4):
    got = sorted(mstr(x) for x in byk[k])
    want = sorted("(" + s + ")" for s in note_moves[k])
    check("the %d-block moves are exactly the note's list" % k, got, want)

check("(b|acd) is not a move", mv("b|acd") in MV, False)
check("(ad|b|c) is not a move", mv("ad|b|c") in MV, False)

print()
print("  one step under x = (ac|bd):")
x = mv("ac|bd")
step = {}
for c in ords:
    step["".join(NAMES[e] for e in c)] = "".join(NAMES[e] for e in act(x, c))
    print("    %s -> %s" % ("".join(NAMES[e] for e in c),
                            "".join(NAMES[e] for e in act(x, c))))
check("the whole (ac|bd) step table", step,
      {"abcd": "acbd", "acbd": "acbd", "acdb": "acdb",
       "cabd": "cabd", "cadb": "cadb", "cdab": "cadb"})

print()
print("  the four-line commitment-destroyed trace:")
c0 = w("abcd")
c1 = act(mv("a|c|bd"), c0)
c2 = act(mv("cd|ab"), c1)
c3 = act(mv("a|c|bd"), c2)
trace = ["".join(NAMES[e] for e in c) for c in (c0, c1, c2, c3)]
print("    " + " -> ".join(trace))
check("trace abcd -(a|c|bd)-> acbd -(cd|ab)-> cdab -(a|c|bd)-> acdb",
      trace, ["abcd", "acbd", "cdab", "acdb"])
check("(a|c|bd) sends every ordering to one with a before c",
      all(list(act(mv("a|c|bd"), c)).index(A) <
          list(act(mv("a|c|bd"), c)).index(C) for c in ords), True)
check("(cd|ab) sends every ordering to one with c before a",
      all(list(act(mv("cd|ab"), c)).index(C) <
          list(act(mv("cd|ab"), c)).index(A) for c in ords), True)

# reachability in the digraph of all moves
idx = {c: i for i, c in enumerate(ords)}
reach = [[False] * 6 for _ in range(6)]
for i in range(6):
    reach[i][i] = True
for x in MV:
    for c in ords:
        reach[idx[c]][idx[act(x, c)]] = True
for _ in range(8):
    for i in range(6):
        for j in range(6):
            if reach[i][j]:
                for k in range(6):
                    if reach[j][k]:
                        reach[i][k] = True
check("every ordering reachable from every ordering",
      all(all(r) for r in reach), True)
fixall = [x for x in MV if all(act(x, c) == c for c in ords)]
check("exactly one move fixes all six orderings", len(fixall), 1)
check("and it is the do-nothing move (abcd)", mstr(fixall[0]), "(abcd)")
absorbing = [c for c in ords if all(act(x, c) == c for x in MV)]
check("zero absorbing orderings", len(absorbing), 0)

# action well-definedness and the ordering-as-move fact (note section 1)
bad = sum(1 for x in MV for c in ords if act(x, c) not in idx)
check("action lands in L(P): 0 failures of 156",
      (bad, len(MV) * len(ords)), (0, 156))
bad2 = sum(1 for x in MV for c in ords
           if act(x, c) != act(product(x, tuple(frozenset([e]) for e in c)),
                               c))
# "treating the ordering itself as a move and multiplying":  x . c  vs  x*c_move
def as_move(c):
    return tuple(frozenset([e]) for e in c)
bad2 = 0
for x in MV:
    for c in ords:
        prod = product(x, as_move(c))
        got = tuple(sorted(Bl)[0] for Bl in prod)
        if got != act(x, c):
            bad2 += 1
check("x.c agrees with the product x*(c as a move): 0 mismatches of 156",
      (bad2, len(MV) * len(ords)), (0, 156))

print()
print("=" * 78)
print("SECTION B -- the band identities on this poset (note section 2)")
print("=" * 78)
n_xx = sum(1 for x in MV if product(x, x) != x)
check("x.x = x on 26 of 26", (len(MV) - n_xx, len(MV)), (26, 26))
n_pairs = 0
n_xyx = 0
n_clos = 0
for x in MV:
    for y in MV:
        n_pairs += 1
        xy = product(x, y)
        if product(product(x, y), x) == xy:
            n_xyx += 1
        if xy in set(MV):
            n_clos += 1
check("x.y.x = x.y on 676 of 676", (n_xyx, n_pairs), (676, 676))
check("closure on 676 of 676", (n_clos, n_pairs), (676, 676))
n_assoc = 0
n_tri = 0
MVs = MV
for x in MVs:
    for y in MVs:
        xy = product(x, y)
        for z in MVs:
            n_tri += 1
            if product(xy, z) == product(x, product(y, z)):
                n_assoc += 1
check("associativity on 17576 of 17576", (n_assoc, n_tri), (17576, 17576))

print()
print("=" * 78)
print("SECTION C -- the commitment levels (note section 4)")
print("=" * 78)
LV = levels(P)
allparts = sorted(set_partitions(range(4)), key=_lkey)
check("15 partitions of a 4-set", len(allparts), 15)
check("14 distinct commitment levels", len(LV), 14)
missing = [X for X in allparts if X not in set(LV)]
check("exactly one partition is not a level", len(missing), 1)
check("and it is {a,d}|{b,c}", lstr(missing[0]), "ad|bc")

AC = acyclic_partitions(P)
check("levels == acyclic quotients on this poset (14 = 14)",
      sorted(map(lstr, LV)), sorted(map(lstr, AC)))
check("{a,d}|{b,c} has a cyclic quotient",
      __import__("audit_lib").quotient_acyclic(P, lv("ad|bc")), False)

bylevel = {}
for x in MV:
    bylevel.setdefault(level(x), []).append(x)
print("  the 14 levels and the moves at each:")
note_table = {
    "abcd": ["(abcd)"],
    "a|bcd": ["(a|bcd)"],
    "acd|b": ["(acd|b)"],
    "ab|cd": ["(ab|cd)", "(cd|ab)"],
    "abd|c": ["(c|abd)"],
    "ac|bd": ["(ac|bd)"],
    "abc|d": ["(abc|d)"],
    "a|b|cd": ["(a|b|cd)", "(a|cd|b)", "(cd|a|b)"],
    "a|bd|c": ["(a|c|bd)", "(c|a|bd)"],
    "a|bc|d": ["(a|bc|d)"],
    "ad|b|c": ["(c|ad|b)"],
    "ac|b|d": ["(ac|b|d)", "(ac|d|b)"],
    "ab|c|d": ["(ab|c|d)", "(c|ab|d)", "(c|d|ab)"],
    "a|b|c|d": ["(a|b|c|d)", "(a|c|b|d)", "(a|c|d|b)", "(c|a|b|d)",
                "(c|a|d|b)", "(c|d|a|b)"],
}
got_table = {}
for X in LV:
    ms = sorted(mstr(x) for x in bylevel[X])
    got_table[lstr(X)] = ms
    print("    %-9s <- %s" % (lstr(X), " ".join(ms)))
check("the level -> moves table is exactly the note's",
      got_table, {k: sorted(v) for k, v in note_table.items()})
check("the finest level's moves are the six orderings read as moves",
      sorted(got_table["a|b|c|d"]),
      sorted(mstr(as_move(c)) for c in ords))

print()
print("=" * 78)
print("SECTION D -- the multiplicities from P alone (note section 5a)")
print("=" * 78)
M = multiplicities(P, LV)
print("  |L| of the induced subposets used in the note:")
for S, want in ((("a", "b"), 1), (("a", "c"), 2), (("a", "b", "c"), 3),
                (("a", "b", "c", "d"), 6)):
    got = n_orderings(induced(P, {NAMES.index(s) for s in S}))
    check("|L(P|{%s})| = %d" % (",".join(S), want), got, want)

note_mult = {
    "a|b|c|d": (1, 1), "ac|b|d": (2, 1), "ad|b|c": (2, 1), "a|bc|d": (2, 1),
    "a|bd|c": (2, 1), "ab|c|d": (1, 0), "a|b|cd": (1, 0), "ac|bd": (4, 1),
    "ab|cd": (1, 0), "abc|d": (3, 0), "abd|c": (3, 0), "acd|b": (3, 0),
    "a|bcd": (3, 0), "abcd": (6, 0),
}
note_refiners = {
    "a|b|c|d": ["a|b|c|d"],
    "ac|b|d": ["ac|b|d", "a|b|c|d"],
    "ad|b|c": ["ad|b|c", "a|b|c|d"],
    "a|bc|d": ["a|bc|d", "a|b|c|d"],
    "a|bd|c": ["a|bd|c", "a|b|c|d"],
    "ab|c|d": ["ab|c|d", "a|b|c|d"],
    "a|b|cd": ["a|b|cd", "a|b|c|d"],
    "ac|bd": ["ac|bd", "ac|b|d", "a|bd|c", "a|b|c|d"],
    "ab|cd": ["ab|cd", "ab|c|d", "a|b|cd", "a|b|c|d"],
    "abc|d": ["abc|d", "ab|c|d", "ac|b|d", "a|bc|d", "a|b|c|d"],
    "abd|c": ["abd|c", "ab|c|d", "ad|b|c", "a|bd|c", "a|b|c|d"],
    "acd|b": ["acd|b", "ac|b|d", "ad|b|c", "a|b|cd", "a|b|c|d"],
    "a|bcd": ["a|bcd", "a|bc|d", "a|bd|c", "a|b|cd", "a|b|c|d"],
    "abcd": [lstr(X) for X in LV],
}
print("  %-9s %6s  %-4s  %s" % ("level", "prod", "m_X", "levels refining it"))
got_mult, got_ref = {}, {}
for X in LV:
    rhs = 1
    for Bk in X:
        rhs *= n_orderings(induced(P, Bk))
    refs = sorted(lstr(Y) for Y in LV if refines(Y, X))
    got_mult[lstr(X)] = (rhs, M[X])
    got_ref[lstr(X)] = refs
    print("  %-9s %6d  %-4d  %s" % (lstr(X), rhs, M[X], ", ".join(refs)))
check("the (product, multiplicity) column of the section-5a table",
      got_mult, note_mult)
check("the 'levels refining it' column of the section-5a table",
      got_ref, {k: sorted(v) for k, v in note_refiners.items()})
check("multiplicities sum to |L(P)| = 6", sum(M.values()), 6)
check("all 14 levels refine the coarsest level",
      len(got_ref["abcd"]), 14)
nonzero = sorted(lstr(X) for X in LV if M[X])
check("six levels carry nonzero multiplicity", len(nonzero), 6)
check("and they are the note's six", nonzero,
      sorted(["ac|bd", "a|bd|c", "a|bc|d", "ad|b|c", "ac|b|d", "a|b|c|d"]))
check("hand-worked row ac|bd: 2*2 = 4, three proper refiners, so m = 1",
      (4, len(got_ref["ac|bd"]) - 1, M[lv("ac|bd")]), (4, 3, 1))

print()
print("=" * 78)
print("SECTION E -- the spectrum under three weightings (note section 5b/5c)")
print("=" * 78)
WCOL = {
    "abcd":    (4, 8, 2),
    "a|bcd":   (6, 4, 3),
    "ac|bd":   (2, 3, 5),
    "ac|b|d":  (3, 2, 1),
    "a|bc|d":  (5, 6, 6),
    "c|ad|b":  (7, 3, 7),
    "a|c|bd":  (1, 2, 4),
    "a|b|c|d": (4, 4, 4),
}
for k, spec in enumerate(("w1", "w2", "w3")):
    tot = sum(v[k] for v in WCOL.values())
    check("%s sums to 1 (32/32)" % spec, tot, 32)

WS = []
for k in range(3):
    d = {}
    for spec, trip in WCOL.items():
        m_ = mv(spec)
        assert m_ in set(MV), spec
        d[m_] = Fraction(trip[k], 32)
    WS.append(d)

note_eigs = {
    "ac|bd":   ("6/32", "11/32", "7/32"),
    "ac|b|d":  ("9/32", "13/32", "8/32"),
    "ad|b|c":  ("11/32", "11/32", "9/32"),
    "a|bd|c":  ("13/32", "17/32", "14/32"),
    "a|bc|d":  ("15/32", "18/32", "11/32"),
    "a|b|c|d": ("1", "1", "1"),
}
got_eigs = {}
for X in LV:
    if M[X] == 0:
        continue
    row = tuple(str(eigenvalue(P, WS[k], X, MV)) for k in range(3))
    got_eigs[lstr(X)] = row
print("  level (mult)   w1        w2        w3")
for kk in sorted(got_eigs, key=lambda s: -len(s)):
    print("  %-9s (%d)  %-9s %-9s %-9s"
          % (kk, M[lv(kk)], *got_eigs[kk]))
want_eigs = {}
for kk, trip in note_eigs.items():
    want_eigs[kk] = tuple(str(Fraction(t)) for t in trip)
check("the six-row eigenvalue table under w1/w2/w3", got_eigs, want_eigs)

# the hand-worked lambda(a|bd|c) under w1
contrib = sorted(mstr(y) for y in MV
                 if WS[0].get(y) and refines(lv("a|bd|c"), level(y)))
check("under w1, exactly four weighted moves contribute to level a|bd|c",
      contrib, sorted(["(abcd)", "(a|bcd)", "(ac|bd)", "(a|c|bd)"]))
check("lambda(a|bd|c) under w1 = 13/32",
      str(eigenvalue(P, WS[0], lv("a|bd|c"), MV)), "13/32")

# against the actual 6x6 matrix
print()
print("  exact rank check against the 6x6 transition matrix:")
for k, spec in enumerate(("w1", "w2", "w3")):
    T = transition_matrix(P, WS[k], ords, MV)
    for j in range(6):
        assert sum(T[i][j] for i in range(6)) == 1, "not stochastic"
    lams = sorted({eigenvalue(P, WS[k], X, MV) for X in LV if M[X]})
    dims = [nullity(sub_scalar(T, lam)) for lam in lams]
    print("     %s: predicted lambdas %s -> dim ker %s, total %d of 6"
          % (spec, [str(l) for l in lams], dims, sum(dims)))
    want = {"w1": [1, 1, 1, 1, 1, 1], "w2": [1, 1, 1, 2],
            "w3": [1, 1, 1, 1, 1, 1]}[spec]
    if spec == "w2":
        print("     *** FINDING F1.  The note's section 5b says of w2:")
        print("     ***   \"Under `w2`: `1,1,1,2` summing to 6 of 6.\"")
        print("     *** There are FIVE distinct eigenvalues under w2, not")
        print("     *** four, and the four numbers printed sum to 5, not 6.")
        print("     *** The instrument itself prints five dim-ker lines")
        print("     *** (1,1,1,1,2 -> 6); the PROSE dropped one.  The")
        print("     *** mathematics is right; the sentence is not, and it is")
        print("     *** the sentence that certifies section 5 against the")
        print("     *** matrix.  The FAIL below is that finding, recorded.")
    check("%s: dim ker multiset is the note's %s summing to 6"
          % (spec, want), sorted(dims), sorted(want))
    check("%s: predicted multiplicities sum to 6 = |L(P)| (diagonalisable)"
          % spec, sum(dims), 6)
    # the multiplicity of each NUMBER = sum of m_X over levels landing on it
    for lam, dim in zip(lams, dims):
        pred = sum(M[X] for X in LV if M[X] and
                   eigenvalue(P, WS[k], X, MV) == lam)
        check("%s: multiplicity of %s predicted %d, dim ker %d"
              % (spec, lam, pred, dim), pred, dim)

# w(abcd) is never an eigenvalue
print()
for k, spec in enumerate(("w1", "w2", "w3")):
    val = WS[k][mv("abcd")]
    lams = {eigenvalue(P, WS[k], X, MV) for X in LV if M[X]}
    T = transition_matrix(P, WS[k], ords, MV)
    landing = sorted(lstr(X) for X in LV
                     if eigenvalue(P, WS[k], X, MV) == val)
    check("%s: w(abcd) = %s is NOT a predicted eigenvalue"
          % (spec, val), val in lams, False)
    check("%s: and dim ker(M - w(abcd) I) = 0 in the actual matrix" % spec,
          nullity(sub_scalar(T, val)), 0)
    if spec in ("w1", "w2"):
        check("%s: the six levels landing on w(abcd) all have m_X = 0"
              % spec,
              sorted(landing), sorted(["abcd", "acd|b", "ab|cd", "abd|c",
                                       "abc|d", "ab|c|d"]))
        check("%s: w(abcd) = %s" % (spec, {"w1": "1/8", "w2": "1/4"}[spec]),
              str(val), {"w1": "1/8", "w2": "1/4"}[spec])

# the level collision under w2
coll = {}
for X in LV:
    if M[X]:
        coll.setdefault(eigenvalue(P, WS[1], X, MV), []).append(lstr(X))
dupes = {str(k): sorted(v) for k, v in coll.items() if len(v) > 1}
check("under w2 exactly one eigenvalue is hit by two levels, 11/32 by "
      "ac|bd and ad|b|c", dupes, {"11/32": ["ac|bd", "ad|b|c"]})
for k, spec in enumerate(("w1", "w3")):
    kk = 0 if spec == "w1" else 2
    vals = [eigenvalue(P, WS[kk], X, MV) for X in LV if M[X]]
    check("under %s all six level-eigenvalues are distinct" % spec,
          len(set(vals)), 6)

print()
print("=" * 78)
print("SECTION F -- the level->multiplicity table is w-independent (5c)")
print("=" * 78)
note_5c = {"abcd": 0, "a|bcd": 0, "acd|b": 0, "ab|cd": 0, "abd|c": 0,
           "ac|bd": 1, "abc|d": 0, "a|b|cd": 0, "a|bd|c": 1, "a|bc|d": 1,
           "ad|b|c": 1, "ac|b|d": 1, "ab|c|d": 0, "a|b|c|d": 1}
check("the section-5c level:multiplicity line",
      {lstr(X): M[X] for X in LV}, note_5c)
# the multiplicity solve genuinely never sees w: recompute with a random-ish
# 4th weighting and confirm the table is byte-identical, and confirm the
# spectrum still checks out.
W4 = {}
vals = [1, 5, 2, 9, 3, 7, 4, 1, 6, 2, 8, 3, 1, 5, 2, 4, 7, 1, 3, 9, 2, 5, 1,
        6, 3, 8]
tot = sum(vals)
for x, v in zip(MV, vals):
    W4[x] = Fraction(v, tot)
check("a fourth weighting (support = ALL 26 moves) sums to 1",
      sum(W4.values()), 1)
T4 = transition_matrix(P, W4, ords, MV)
lams4 = sorted({eigenvalue(P, W4, X, MV) for X in LV if M[X]})
dims4 = [nullity(sub_scalar(T4, l)) for l in lams4]
print("  w4 (all 26 moves weighted): lambdas %s"
      % [str(l) for l in lams4])
print("  w4 dim ker %s, total %d of 6" % (dims4, sum(dims4)))
check("w4: the level->multiplicity table is unchanged",
      {lstr(X): M[X] for X in LV}, note_5c)
check("w4: predicted spectrum accounts for all 6 dimensions", sum(dims4), 6)
for lam, dim in zip(lams4, dims4):
    pred = sum(M[X] for X in LV if M[X] and eigenvalue(P, W4, X, MV) == lam)
    check("w4: multiplicity of %s predicted %d = dim ker %d"
          % (lam, pred, dim), pred, dim)

print()
print("=" * 78)
print("SECTION G -- section 6 (R6): the twist, ONE and SGN")
print("=" * 78)
note_inv = {"abcd": 0, "acbd": 1, "acdb": 2, "cabd": 2, "cadb": 3, "cdab": 4}
got_inv = {"".join(NAMES[e] for e in c): inversions(c) for c in ords}
check("the inversion counts of the six orderings", got_inv, note_inv)
S = [sgn(c) for c in ords]
check("the signs +1 -1 +1 +1 -1 +1", S, [1, -1, 1, 1, -1, 1])
check("sign imbalance of P = +2", sum(S), 2)

Lat = at_laplacian(P, ords)
ONE = [1] * 6
SGN = list(S)
Erel = [[S[i] * Lat[i][j] * S[j] for j in range(6)] for i in range(6)]  # E.Lat.E
# note's identity: Delta_AT = E . L^rel . E, E involutive, so L^rel = E.Delta.E
Lrel = Erel
check("E . ONE = SGN", [S[i] * ONE[i] for i in range(6)], SGN)
check("E . SGN = ONE", [S[i] * SGN[i] for i in range(6)], ONE)
check("Delta_AT . ONE = 0", mat_vec(Lat, ONE), [0] * 6)
check("Delta_AT . SGN = (2,-6,4,4,-6,2)", mat_vec(Lat, SGN),
      [2, -6, 4, 4, -6, 2])
check("L^rel . SGN = 0", mat_vec(Lrel, SGN), [0] * 6)
check("L^rel . ONE = (2,6,4,4,6,2)", mat_vec(Lrel, ONE), [2, 6, 4, 4, 6, 2])
check("dim ker Delta_AT = 1", 6 - rank_Q(Lat), 1)
check("dim ker L^rel = 1", 6 - rank_Q(Lrel), 1)
check("the AT graph on L(P) is connected", connected(at_graph(P, ords)), True)
check("<ONE,SGN> = sum of signs = 2", sum(ONE[i] * SGN[i] for i in range(6)), 2)
check("projection of ONE onto span(SGN) is (1/3) SGN",
      Fraction(sum(ONE[i] * SGN[i] for i in range(6)),
               sum(SGN[i] * SGN[i] for i in range(6))), Fraction(1, 3))
print("  AT degrees:", [sum(1 for j in range(6) if at_graph(P, ords)[i][j])
                        for i in range(6)])

print()
print("=" * 78)
print("%d checks, %d FAILURES" % (CHECKS[0], len(FAIL)))
for f in FAIL:
    print("  FAILED: %s" % f)
print("=" * 78)
sys.exit(1 if FAIL else 0)
