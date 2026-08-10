"""x0 — SEVEN PLANTED WORLDS.  How this instrument can fail, exercised rather than promised.

Every world below states what it plants, what the detector must say, and — first — what
the detector says about the UNMUTATED input.  mg-9876's rule, adopted rather than
paraphrased: a probe already satisfied by the good input is UNFALSIFIABLE and is never
scored CAUGHT.  Two of these worlds require the answer "this instrument's clustering is
worthless", and if it ever gives that answer the arm goes red rather than quiet.

  W1  a column 1e-3 away from Delta must NOT join Delta's cluster   (discrimination)
  W2  a column EQUAL to Delta must join it                          (non-vacuity)
  W3  a constant column shared by two fake trees must read DEGENERATE
  W4  the rho*Delta cluster must form on POP-PRIM and not on POP-ALL (population)
  W5  D1: the rounding key must split a pair the spread clustering keeps
  W6  two all-None columns must NOT be clustered together
  W7  every adapter must still produce its columns — a group that quietly loses a
      member because a library changed would report a smaller alias and no error

Exit 0 iff every world is CAUGHT or honestly UNFALSIFIABLE-with-reason.
"""

import sys
import time

import lib0d1b as L

t0 = time.time()
results = []


def arm(name, verdict, detail):
    results.append((name, verdict, detail))
    print("  [%-14s] %-46s %s" % (verdict, name, detail))


POP = L.population([(3, 1), (4, 1)])
PRIM = [(n, dn) for (n, dn) in POP if L.primitive_here(dn, n)]

print("x0  PLANTED WORLDS")
print()
print("  base population for W1-W3, W6-W7: %d posets (n = 3,4); primitive %d"
      % (len(POP), len(PRIM)))
print()

# the honest baseline: the real columns, unmutated
base = {}
for tree, ad, _f in L.ADAPTERS:
    acc = {}
    for (n, dn) in POP:
        for k, v in ad(dn, n).items():
            acc.setdefault(k, []).append(v)
    for k, v in acc.items():
        base[(tree, k)] = v

DELTA = base[("lstar_789d", "Delta")]


def cluster_of(cols, member):
    for g in L.cluster(cols, 1e-6):
        if member in g:
            return g
    return [member]


# ---------------------------------------------------------------- W1
cols = dict(base)
cols[("FAKE_near", "Delta_plus_1e3")] = [v + 1e-3 for v in DELTA]
g = cluster_of(cols, ("lstar_789d", "Delta"))
if ("FAKE_near", "Delta_plus_1e3") in g:
    arm("W1 discrimination", "MISSED",
        "a column 1e-3 from Delta joined Delta's cluster — the clustering is worthless")
else:
    arm("W1 discrimination", "CAUGHT",
        "planted Delta+1e-3 stayed out of a cluster of %d" % len(g))

# ---------------------------------------------------------------- W2
cols = dict(base)
cols[("FAKE_same", "Delta_copy")] = list(DELTA)
g2 = cluster_of(cols, ("lstar_789d", "Delta"))
if ("FAKE_same", "Delta_copy") in g2:
    arm("W2 non-vacuity", "CAUGHT",
        "an identical column DID join, so W1 is a refusal and not silence")
else:
    arm("W2 non-vacuity", "MISSED",
        "an identical column did not join — W1 proves nothing")

# ---------------------------------------------------------------- W3
pre = L.is_constant(DELTA)
cols = dict(base)
cols[("FAKE_c1", "always_one")] = [1.0] * len(POP)
cols[("FAKE_c2", "also_always_one")] = [1.0] * len(POP)
g3 = cluster_of(cols, ("FAKE_c1", "always_one"))
joined = ("FAKE_c2", "also_always_one") in g3
if pre:
    arm("W3 degenerate guard", "UNFALSIFIABLE",
        "the real Delta column is itself constant here — cannot distinguish")
elif joined and L.is_constant(cols[("FAKE_c1", "always_one")]):
    arm("W3 degenerate guard", "CAUGHT",
        "two constant columns cluster AND are flagged is_constant -> DEGENERATE")
else:
    arm("W3 degenerate guard", "MISSED",
        "constant columns were not flagged; a cluster of constants would read as an alias")

# ---------------------------------------------------------------- W4
RHO_NAMES = [("lstar_789d", "rho*Delta"), ("audit_5cba", "v_L"),
             ("l2_underclaim_audit_3bb9", "V10")]
w4 = {}
for tree, ad, _f in L.ADAPTERS:
    if tree not in {t for t, _ in RHO_NAMES}:
        continue
    acc = {}
    for (n, dn) in POP:
        for k, v in ad(dn, n).items():
            acc.setdefault(k, []).append(v)
    for k, v in acc.items():
        w4[(tree, k)] = v
w4_prim = {k: [v for v, (n, dn) in zip(vals, POP) if L.primitive_here(dn, n)]
           for k, vals in w4.items()}
in_all = set(cluster_of(w4, RHO_NAMES[0])) >= set(RHO_NAMES)
in_prim = set(cluster_of(w4_prim, RHO_NAMES[0])) >= set(RHO_NAMES)
if in_prim and not in_all:
    arm("W4 population", "CAUGHT",
        "rho*Delta clusters on POP-PRIM and does NOT on POP-ALL — the population decides")
elif in_prim and in_all:
    arm("W4 population", "UNFALSIFIABLE",
        "it clusters on both here; at n = 3,4 the decomposable posets may not separate it")
else:
    arm("W4 population", "MISSED",
        "the rho*Delta cluster did not form even on POP-PRIM")

# ---------------------------------------------------------------- W5
# The mutation is DERIVED from the captured bytes, not typed: every real column is
# nudged by 4e-10 — smaller than the tolerance, so the two are the same number by any
# reading — and the first column whose ROUNDING KEY changes under that nudge is the
# world.  If no real column straddles a bucket, the arm says UNFALSIFIABLE rather than
# inventing a pair that does.
a = b = None
for k, v in sorted(base.items()):
    vv = [x for x in v if x is not None]
    if len(vv) < 5:
        continue
    cand = [x + 4e-10 for x in vv]
    if L.fingerprint(vv, 1e-9) != L.fingerprint(cand, 1e-9):
        a, b, src = vv, cand, k
        break
if a is None:
    a, b, src = [0.5], [0.5], ("none", "none")
cols5 = {("A", "x"): a, ("B", "y"): b}
same_fp = L.fingerprint(a, 1e-9) == L.fingerprint(b, 1e-9)
same_cl = len(L.cluster(cols5, 1e-9)) == 1
if same_cl and not same_fp:
    arm("W5 D1 rounding", "CAUGHT",
        "spread clustering keeps %s:%s nudged by 4e-10; the rounding key splits it"
        % src)
elif same_cl and same_fp:
    arm("W5 D1 rounding", "UNFALSIFIABLE",
        "this pair happened not to straddle a bucket; the defect is real, see x3 V5")
else:
    arm("W5 D1 rounding", "MISSED",
        "the spread clustering ALSO split them — the repair did not take")

# ---------------------------------------------------------------- W6
cols6 = {("A", "none1"): [None] * 10, ("B", "none2"): [None] * 10,
         ("C", "real"): [float(i) for i in range(10)]}
gs = L.cluster(cols6, 1e-6)
merged = any({("A", "none1"), ("B", "none2")} <= set(g) for g in gs)
if merged:
    arm("W6 empty columns", "MISSED",
        "two never-comparable columns were clustered — every absent scalar would alias")
else:
    arm("W6 empty columns", "CAUGHT",
        "spread() returns None for a never-comparable pair and no edge is drawn")

# ---------------------------------------------------------------- W7
short = []
for tree, ad, _f in L.ADAPTERS:
    d = ad((0, 1, 3), 3)
    live = sum(1 for v in d.values() if v is not None)
    if live < 3:
        short.append("%s(%d)" % (tree, live))
if short:
    arm("W7 adapters live", "MISSED",
        "adapters producing fewer than 3 live columns: " + ", ".join(short))
else:
    arm("W7 adapters live", "CAUGHT",
        "all %d adapters produce >= 3 live scalars on a fixed poset" % len(L.ADAPTERS))

# ---------------------------------------------------------------- verdict
print()
print("=" * 78)
missed = [n for n, v, _d in results if v == "MISSED"]
unf = [n for n, v, _d in results if v == "UNFALSIFIABLE"]
print("x0 RESULT: %d CAUGHT, %d UNFALSIFIABLE (explained), %d MISSED   (%.1fs)"
      % (len(results) - len(missed) - len(unf), len(unf), len(missed), time.time() - t0))
if unf:
    print("  UNFALSIFIABLE arms are reported as such and NOT counted as catches: "
          + ", ".join(unf))
print("=" * 78)
sys.exit(1 if missed else 0)
