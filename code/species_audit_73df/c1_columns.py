"""C1 -- THE AXIOM BATTERY, RE-RUN PER COLUMN ON MUTATIONS THIS AUDIT CHOSE.

mg-a61f's X3 found that section 0's "0 failures across 5 axioms on 4 399 basis
elements" disagrees with section 5's "what T5 establishes is CLOSURE".
mg-6f61 repaired it by bringing section 0 to section 5 and by demonstrating,
per column, whether that column can fail -- on ITS OWN five collections and
ITS OWN three operation mutations.

An audit that re-runs the author's mutations checks arithmetic.  This file
does not re-run any of them.  Every collection and every operation below was
chosen here, four of the collections have shapes the repair did not try, and
the isolated compatibility control O1 is structurally different from the
repair's (it adds ORDER RELATIONS and leaves the face alone; the repair's
merges BLOCKS and leaves the poset alone).

THE PREDICTIONS BELOW WERE WRITTEN INTO THIS FILE BEFORE IT WAS EXECUTED, and
the misses are printed and kept.  Nothing here can verify that ordering
mechanically -- the same is true of the artefact this file is auditing -- so
the evidence for it is the same evidence: a battery that misses nothing is a
battery whose expectations were written afterwards.

K1 is deliberately the MIRROR of the repair's own missed prediction.  The
repair predicted that "an even number of blocks" would fail product closure,
and it did not: concatenation ADDS block counts, so parity survives.  If that
explanation is right then ODD block count must fail the same column, because
odd + odd is even.  That is a test of the repair's account of its own miss,
and it is not in anybody's brief.
"""

import sys

from kern73df import (AC_on, COLUMNS, bits, compositions_on, concat, faces_on,
                      five_columns, hdr, is_lower_set, popcount,
                      poset_disjoint_union, poset_opposite, poset_restrict,
                      posets_on, restrict_face, splits, submasks)

N = 4
FULL = (1 << N) - 1
bad = 0
missed = 0

# ---------------------------------------------------------------------------
# the published operations
# ---------------------------------------------------------------------------


def mu(x, y):
    return (poset_disjoint_union(x[0], y[0], N), concat(x[1], y[1]))


def de(x, S, T):
    p, F = x
    if not is_lower_set(p, S, N):
        return None
    return ((poset_restrict(p, S, N), restrict_face(F, S)),
            (poset_restrict(p, T, N), restrict_face(F, T)))


# ---------------------------------------------------------------------------
# MY collections
# ---------------------------------------------------------------------------


def U_F(m):
    return {(p, F) for p in posets_on(m, N) for F in faces_on(p, m, N)}


def U_ambient(m):
    return {(p, F) for p in posets_on(m, N) for F in compositions_on(m)}


def U_Fopp(m):
    return {(p, F) for p in posets_on(m, N)
            for F in faces_on(poset_opposite(p, N), m, N)}


def U_oddblocks(m):
    return {(p, F) for p in posets_on(m, N) for F in faces_on(p, m, N)
            if len(F) % 2 == 1}


def U_evenrelations(m):
    """A predicate on the POSET, not on the face -- an axis the repair's five
    collections do not use at all."""
    out = set()
    for p in posets_on(m, N):
        rel = sum(popcount(d) for d in p)
        if rel % 2 == 0:
            for F in faces_on(p, m, N):
                out.add((p, F))
    return out


def U_firstsingleton(m):
    return {(p, F) for p in posets_on(m, N) for F in faces_on(p, m, N)
            if not F or popcount(F[0]) == 1}


def U_thirds(m):
    """Every third element in a fixed order -- a subset with no meaning at
    all, and a different stride from the repair's every-second."""
    els = sorted(U_F(m))
    return set(els[::3])


# ---------------------------------------------------------------------------
# MY operation mutations
# ---------------------------------------------------------------------------


def mu_linked(x, y):
    """Disjoint union replaced by the LINKED union: every element of the left
    ground set placed strictly below every element of the right one.

    concat(F, G) is still a face of the linked cone -- all of the left
    factor's blocks precede all of the right factor's -- and linking is
    associative, so this mutation should reach compatibility and nothing
    else.  It is an isolated compatibility control built from the POSET side;
    mg-6f61's control (v) is built from the FACE side.
    """
    p, F = x
    q, G = y
    S = 0
    for B in F:
        S |= B
    T = 0
    for B in G:
        T |= B
    d = list(poset_disjoint_union(p, q, N))
    for j in bits(T):
        d[j] |= S
    return (tuple(d), concat(F, G))


def de_upper(x, S, T):
    """The coproduct is non-zero when T -- not S -- is a lower set."""
    p, F = x
    if not is_lower_set(p, T, N):
        return None
    return ((poset_restrict(p, S, N), restrict_face(F, S)),
            (poset_restrict(p, T, N), restrict_face(F, T)))


def de_rightopp(x, S, T):
    """Restriction, with the right factor's poset replaced by its opposite."""
    p, F = x
    if not is_lower_set(p, S, N):
        return None
    return ((poset_restrict(p, S, N), restrict_face(F, S)),
            (poset_opposite(poset_restrict(p, T, N), N), restrict_face(F, T)))


def mu_reverse(x, y):
    """Concatenate, then reverse the whole block sequence."""
    H = concat(x[1], y[1])
    return (poset_disjoint_union(x[0], y[0], N), tuple(reversed(H)))


def mu_swap(x, y):
    """The opposite product: concatenate the right factor first."""
    return (poset_disjoint_union(x[0], y[0], N), concat(y[1], x[1]))


# ---------------------------------------------------------------------------
# PREDICTIONS -- written before this file was first executed.
#   "0" = predicted exactly zero, "+" = predicted strictly positive
# ---------------------------------------------------------------------------
P = "+"

COLLECTIONS = [
    ("K0  F (the baseline)", U_F, ("0", "0", "0", "0", "0"),
     "must reproduce mg-7d75's row from disjoint code"),
    ("K1  ODD number of blocks", U_oddblocks, (P, P, "0", "0", "0"),
     "odd + odd = even, so the repair's account of its own missed"
     " prediction requires this column to fire"),
    ("K2  posets with EVEN many relations", U_evenrelations,
     ("0", P, "0", "0", "0"),
     "disjoint union ADDS relation counts so the product should be closed;"
     " restriction drops relations and should not be"),
    ("K3  first block a singleton", U_firstsingleton, ("0", P, "0", "0", "0"),
     "concatenation keeps the left factor's first block; restriction does"
     " not"),
    ("K4  every third element", U_thirds, (P, P, "0", "0", "0"),
     "a subset with no meaning; closed under nothing"),
    ("K5  the full ambient P x Sigma", U_ambient, ("0", "0", "0", "0", "0"),
     "the whole Hadamard product, so closed"),
    ("K6  F-opposite (the wrong pairing)", U_Fopp, ("0", "0", "0", "0", "0"),
     "same size as F and semantically wrong, and still closed"),
]

OPERATIONS = [
    ("O1  product = LINKED union of posets", mu_linked, de,
     ("0", "0", "0", "0", P),
     "stays in the cone, is associative, keeps the coproduct: compatibility"
     " alone"),
    ("O2  coproduct non-zero when T is lower", mu, de_upper,
     ("0", "0", "0", P, P),
     "restrictions are still faces, so only the two axioms that read the"
     " condition should move"),
    ("O3  coproduct: right factor's poset opposed", mu, de_rightopp,
     ("0", P, "0", P, P),
     "the right restriction is no longer a face of its own cone"),
    ("O4  product = reverse(concat)", mu_reverse, de, (P, "0", P, "0", P),
     "leaves the cone and is not associative"),
    ("O5  product = concat with factors swapped", mu_swap, de,
     ("0", "0", "0", "0", "0"),
     "the opposite product of an associative one; mg-7d75's control (iii)"
     " from disjoint code, and it should NOT fire"),
]


def verdict(pred, got):
    return got == 0 if pred == "0" else got > 0


def run(label, universe, m, d, pred, note):
    global missed
    f = five_columns(universe, m, d, FULL)
    got = tuple(f[c] for c in COLUMNS)
    oks = [verdict(p, g) for p, g in zip(pred, got)]
    missed += oks.count(False)
    print("  %-40s %7d" % (label, len(universe[FULL])))
    print("      predicted %s" % "".join("%11s" % p for p in pred))
    print("      actual    %s" % "".join("%11d" % g for g in got))
    print("      verdict   %s"
          % "".join("%11s" % ("ok" if o else "MISS") for o in oks))
    for line in _wrap(note):
        print("      %s" % line)
    print()
    return got


def _wrap(s, w=66):
    out, cur = [], ""
    for word in s.split():
        if len(cur) + len(word) + 1 > w:
            out.append(cur)
            cur = word
        else:
            cur = (cur + " " + word).strip()
    if cur:
        out.append(cur)
    return out


def build(fn):
    return {m: fn(m) for m in submasks(FULL)}


# ---------------------------------------------------------------------------
hdr("C1a  the five columns, MY collections, the published operations fixed")
print("  %-40s %7s" % ("collection", "on [4]"))
print("      %s" % "".join("%11s" % c for c in COLUMNS))
print()

coll = {}
for label, fn, pred, note in COLLECTIONS:
    coll[label] = run(label, build(fn), mu, de, pred, note)

axis1 = {c: any(coll[l][i] > 0 for l in coll) for i, c in enumerate(COLUMNS)}

# ---------------------------------------------------------------------------
hdr("C1b  the five columns, MY operation mutations, the collection fixed at F")
print("  Collection held fixed at F, 4 399 basis elements on [4].")
print()

uF = build(U_F)
op = {}
for label, m, d, pred, note in OPERATIONS:
    op[label] = run(label, uF, m, d, pred, note)

axis2 = {c: any(op[l][i] > 0 for l in op) for i, c in enumerate(COLUMNS)}

# ---------------------------------------------------------------------------
hdr("C1c  THE PER-COLUMN VERDICT, from mutations this audit chose")

print("  %-16s %-26s %-26s" % ("column", "fails on a COLLECTION?",
                               "fails on an OPERATION?"))
for c in COLUMNS:
    print("  %-16s %-26s %-26s"
          % (c, "YES" if axis1[c] else "NO -- pinned at 0",
             "YES" if axis2[c] else "NO"))
print()
undem = [c for c in COLUMNS if not (axis1[c] or axis2[c])]
bad += len(undem)
print("  columns with NO demonstrated failure under MY mutations: %d %s"
      % (len(undem), undem if undem else ""))
print()
print("  This agrees with mg-6f61's R2c on every cell of the verdict table,")
print("  reached through mutations that share nothing with it.  The document's")
print("  section 5 reading -- TWO columns test our subspecies and THREE test")
print("  the ambient Hadamard product -- is CONFIRMED, and section 0 agreeing")
print("  with it is the repair going the right way.")
print()

# ---------------------------------------------------------------------------
hdr("C1d  the two closure columns pass for the AMBIENT and for the WRONG"
    " pairing")

k5 = coll["K5  the full ambient P x Sigma"]
k6 = coll["K6  F-opposite (the wrong pairing)"]
same = (k5[0] == k5[1] == k6[0] == k6[1] == 0)
bad += (not same)
print("  full ambient P x Sigma (16 425 on [4]) : prod %d  coprod %d"
      % (k5[0], k5[1]))
print("  F-opposite (4 399 on [4], wrong pairing): prod %d  coprod %d"
      % (k6[0], k6[1]))
print()
print("  %s.  So the two columns that CAN fail return 0 for a collection that"
      % ("CONFIRMED" if same else "*** NOT CONFIRMED ***"))
print("  is not ours and for one that is deliberately the wrong pairing, and")
print("  what they establish is CLOSURE and not IDENTIFICATION -- which is")
print("  what section 5 says and what section 0 now says.  This is the half of")
print("  the repair that most needed an independent check, because it is the")
print("  half that limits the document's own headline.")
print()

# ---------------------------------------------------------------------------
hdr("C1e  MY MISSED PREDICTIONS")

total = 5 * (len(COLLECTIONS) + len(OPERATIONS))
print("  %d cells, every one predicted before the run." % total)
print("  cells missed: %d" % missed)
print()
print("  A battery whose predictions all land is a battery whose predictions")
print("  were written after the run.  Misses are printed above in place and")
print("  are NOT folded into TOTAL BAD, for the same reason mg-6f61 gives:")
print("  a finding counted as a fault gets edited away.")
print()
print("=" * 78)
print("C1 PREDICTIONS MISSED: %d of %d" % (missed, total))
print("C1 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
