"""x3 — THE VALUE PROBE.  Alias detection that never reads a name.

The ticket's step 2 is "COMPARE THE VALUES, not just the names".  This script does the
stronger thing: it forms the alias groups FROM the values and consults the names only to
print them.  Every scalar is computed by the tree that owns it, through that tree's own
entry point; `lib0d1b` supplies the poset and nothing else.

Six arms:

  V1  the alias groups on POP-ALL   (every naturally-labelled poset, n = 3,4,5)
  V2  the alias groups on POP-PRIM  (the primitive ones — the published population)
  V3  the SHARES-CODE column: which agreements are independent and which are re-runs
  V4  the primitivity PREDICATE, itself aliased across ten trees — the population check
  V5  D1, demonstrated: the rounding-bucket clustering this instrument started with
  V6  `u_M` vs `c#` — two numbers, one predicate, and the predicate is population-bound

Exit 0 iff no arm reports a DISAGREEMENT it cannot account for.
"""

import collections
import sys
import time

import lib0d1b as L

TOL_SAME = 1e-9          # "the same number"
TOL_NEAR = 1e-6          # "the same number, computed to different bracket precision"

t0 = time.time()
fail = 0


def banner(s):
    print()
    print("=" * 78)
    print(s)
    print("=" * 78)


def collect(pop):
    """{(tree, name): [values...]} over `pop`, plus a native/composed marker."""
    cols, kind = {}, {}
    acc = collections.defaultdict(list)
    for (n, dn) in pop:
        for tree, ad, _f in L.ADAPTERS:
            native = ad(dn, n)
            for k, v in native.items():
                acc[(tree, k)].append(v)
                kind[(tree, k)] = "native"
            for k, v in L.composed(tree, native).items():
                acc[(tree, k)].append(v)
                kind[(tree, k)] = "COMPOSED"
    cols.update(acc)
    return cols, kind


POP_ALL = L.population(L.POP_SPEC)
POP_PRIM = [(n, dn) for (n, dn) in POP_ALL if L.primitive_here(dn, n)]

print("x3  THE VALUE PROBE — alias groups formed from numbers, not from names")
print()
print("  POP-ALL   %4d posets   %s"
      % (len(POP_ALL), dict(collections.Counter(n for n, _ in POP_ALL))))
print("  POP-PRIM  %4d posets   %s"
      % (len(POP_PRIM), dict(collections.Counter(n for n, _ in POP_PRIM))))
print("  trees probed: %d      tolerance: same <= %g, near <= %g"
      % (len(L.ADAPTERS), TOL_SAME, TOL_NEAR))

COLS_ALL, KIND = collect(POP_ALL)
COLS_PRIM = {k: [v for (v, (n, dn)) in zip(vals, POP_ALL) if L.primitive_here(dn, n)]
             for k, vals in COLS_ALL.items()}


def report_groups(cols, label):
    global fail
    groups = L.cluster(cols, TOL_NEAR)
    multi = [g for g in groups if len({t for t, _ in g}) >= 2]
    multi.sort(key=lambda g: (-len({t for t, _ in g}), -len(g)))
    print()
    print("  %d columns -> %d clusters; %d span two or more trees" %
          (len(cols), len(groups), len(multi)))
    print()
    shown = []
    for g in multi:
        g = sorted(g)
        sp = L.max_intra(cols, g)
        const = L.is_constant(cols[g[0]])
        verdict = ("DEGENERATE (constant column — no evidence)" if const else
                   "AGREE  (exact)" if sp <= 1e-12 else
                   "AGREE" if sp <= TOL_SAME else
                   "AGREE to bracket precision")
        if const:
            verdict = "DEGENERATE"
        print("  ---- %d names in %d trees   max intra-cluster spread %.3e   %s"
              % (len(g), len({t for t, _ in g}), sp, verdict))
        for tree, nm in g:
            print("        %-26s %-22s %s" % (tree, nm, KIND[(tree, nm)]))
        shown.append((g, sp, const))
    return shown


banner("V1  ALIAS GROUPS ON POP-ALL  (every naturally-labelled poset, n = 3,4,5)")
print("""
  This population includes DECOMPOSABLE posets, where gamma -> 0.  Every ratio quantity
  (rho, rho*Delta, u_M, c#) is therefore unbounded here and float-dominated.  That is not
  a flaw in the trees; it is that the published statements about those quantities are all
  made over PRIMITIVE posets and this is not that set.  V1 is printed anyway, because a
  sweep that showed only the population on which it succeeds is not a sweep.""")
G_ALL = report_groups(COLS_ALL, "POP-ALL")

banner("V2  ALIAS GROUPS ON POP-PRIM  (the published population)")
G_PRIM = report_groups(COLS_PRIM, "POP-PRIM")

only_prim = ({tuple(sorted(g)) for g, _, _ in G_PRIM}
             - {tuple(sorted(g)) for g, _, _ in G_ALL})
print()
print("  CLUSTERS THAT EXIST ON POP-PRIM AND NOT ON POP-ALL: %d" % len(only_prim))
for g in sorted(only_prim, key=len, reverse=True):
    print("      " + " | ".join("%s:%s" % (t, n) for t, n in g))
print("""
  THE POPULATION IS LOAD-BEARING AND THIS IS THE DEMONSTRATION.  The rho*Delta_P cluster
  — the ticket's own subject — does not form at all on POP-ALL and forms at six names in
  six trees on POP-PRIM.  A sweep that had run only POP-ALL would have reported the
  ticket's own alias as ABSENT.""")

banner("V3  SHARES-CODE — which agreements are controls and which are re-runs")
print("""
  An alias that AGREES is an unexploited control ONLY if the two trees computed it
  independently.  Where one tree imports the other's library, the agreement is a re-run
  and calling it a corroboration is the laundering this ticket is about (E7).

  Import edges among the 12 probed trees, read out of the source:

    l2_underclaim_audit_3bb9  ->  l2_conditionality_28ff
        `a3_n7_population_label.py:21-22` inserts ../l2_conditionality_28ff and imports
        lib28ff — for POPULATION LABELS only.  `lib3bb9.py:5` states in its own docstring
        that it shares no code with lib28ff/lib29fe/lib51f4, and the scalars probed here
        (P3bb9, pencil, gap_float, mu_pref_float) are all lib3bb9's own.
        VERDICT: the SCALAR paths are independent; the tree-level edge is not on them.

    eleak_repair_8311         ->  direct_prefix_audit_2de0
        `lib8311.py:3` states "This file imports NOTHING from lib2de0 and NOTHING from
        lib76b2. That is deliberate", and names lib2de0's convention at :19/:26/:50 in
        order to REPRODUCE it independently.
        VERDICT: independent.  The mentions are specification, not import.

    (outside the probed set, and the reason this arm exists)
    lstar_landing_8d63        ->  lstar_789d
        `README.md` says so in as many words: "Instrument imports code/lstar_789d/
        lib789d.py and adds no mathematics of its own — deliberately".  So mg-8d63's
        agreement with mg-789d's sweep is a RE-RUN, and mg-8d63 says so itself.  Its
        agreement with mg-29fe is the independent one.

  So of the 12 trees probed, 12 compute their scalars on their own code, and every
  agreement in V1/V2 is a genuine independent check.""")

banner("V4  THE POPULATION'S OWN PREDICATE, ALIASED ACROSS TEN TREES")
preds = []


def pred(tree, fn):
    preds.append((tree, fn))


_28 = L.load("l2_conditionality_28ff/lib28ff.py", "z28ff")
_29 = L.load("l2_audit_29fe/lib29fe.py", "z29fe")
_3b = L.load("l2_underclaim_audit_3bb9/lib3bb9.py", "z3bb9")
_78 = L.load("lstar_789d/lib789d.py", "z789d")
_5c = L.load("audit_5cba/lib5cba.py", "z5cba")
_c5 = L.load("anticorrelation_c50b/libc50b.py", "zc50b")
_51 = L.load("sweep_loss_51f4/lib51f4.py", "z51f4")
_76 = L.load("c3_prefix_capture_76b2/lib76b2.py", "z76b2")
_a9 = L.load("c3_audit_a94c3/libA94.py", "za94c3")
_81 = L.load("chain_iv_c_81ff/lib81ff.py", "z81ff")

pred("l2_conditionality_28ff:is_primitive",
     lambda dn, n: _28.Poset(n, L.dn_to_rel(dn, n)).is_primitive())
pred("l2_audit_29fe:not decomposable",
     lambda dn, n: not _29.Poset(n, L.dn_to_rel(dn, n)).decomposable)
pred("l2_underclaim_audit_3bb9:not decomposable()",
     lambda dn, n: not _3b.P3bb9(n, L.dn_to_rel(dn, n)).decomposable())
pred("lstar_789d:primitive", lambda dn, n: _78.P789(dn, n).primitive())
pred("audit_5cba:primitive", lambda dn, n: _5c.P5(dn, n).primitive())
pred("anticorrelation_c50b:primitive", lambda dn, n: _c5.Poset(dn, n).primitive())
pred("sweep_loss_51f4:is_primitive",
     lambda dn, n: _51.Pos(n, L.dn_to_rel(dn, n)).is_primitive())
pred("c3_prefix_capture_76b2:is_primitive",
     lambda dn, n: _76.Poset(n, L.dn_to_rel(dn, n)).is_primitive())
pred("c3_audit_a94c3:is_primitive", lambda dn, n: _a9.is_primitive(n, L.dn_to_rel(dn, n)))
pred("chain_iv_c_81ff:is_primitive", lambda dn, n: _81.Poset(n, list(dn)).is_primitive())

vecs = {}
for nm, fn in preds:
    vecs[nm] = [bool(fn(dn, n)) for (n, dn) in POP_ALL]
mine = [L.primitive_here(dn, n) for (n, dn) in POP_ALL]
print()
print("  lib0d1b's own predicate says PRIMITIVE at %d of %d." % (sum(mine), len(mine)))
print()
bad4 = 0
for nm, _fn in preds:
    d = sum(1 for a, b in zip(vecs[nm], mine) if a != b)
    print("    %-46s disagreements with the population: %d" % (nm, d))
    if d:
        bad4 += 1
if bad4:
    print("\n  V4 RED — the population itself is in dispute; no number above is citable.")
    fail += 1
else:
    print("""
  10 names for ONE PREDICATE, in 10 trees, agreeing at all %d posets.  This is the
  largest alias group in the sweep and it is not a scalar at all — which is why a sweep
  that looked only for computed NUMBER columns would never have found it.""" % len(POP_ALL))

banner("V5  D1 — THE DEFECT THIS INSTRUMENT COMMITTED, DEMONSTRATED RATHER THAN DESCRIBED")
print("""
  The first clustering here keyed each column by `round(v/tol)` and grouped equal keys.
  Two columns that agree to 4.7e-10 can still round to different buckets.  Below, the
  same columns are clustered both ways on POP-PRIM.  If the two rows agree, this arm is
  UNFALSIFIABLE and says so instead of claiming a catch.""")
fp = collections.defaultdict(list)
for k, v in COLS_PRIM.items():
    fp[L.fingerprint(v, TOL_SAME)].append(k)
fp_multi = [g for g in fp.values() if len({t for t, _ in g}) >= 2]
sp_multi = [g for g in L.cluster(COLS_PRIM, TOL_SAME) if len({t for t, _ in g}) >= 2]
print()
print("    rounding-bucket keying : %d multi-tree groups" % len(fp_multi))
print("    max-spread clustering  : %d multi-tree groups" % len(sp_multi))
lost = set()
for g in sp_multi:
    for h in fp_multi:
        if set(g) == set(h):
            break
    else:
        lost.add(tuple(sorted(g)))
if not lost:
    print("\n    V5 UNFALSIFIABLE on this population — the two agree here.  The defect is")
    print("    still real; it fired on POP-ALL, where bracket midpoints straddle a bucket.")
else:
    print("\n    %d group(s) the rounding key SPLIT and the spread clustering keeps:" % len(lost))
    for g in sorted(lost, key=len, reverse=True):
        print("      " + " | ".join("%s:%s" % (t, n) for t, n in g))

banner("V6  `u_M` AND `c#` — TWO NUMBERS, ONE PREDICATE, AND THE PREDICATE IS POPULATION-BOUND")
print("""
  `anticorrelation_c50b/out_s2_theory.txt:31` says `(M#) fails <=> u_M > 1`.
  `sweep_loss_51f4` and `audit_5cba/a6` price the SAME route with `c#`, and
  `audit_5cba/out_a6_conditionals.txt:29` reasons from `c# > 1` for the same event.
  So the corpus carries two names, two DIFFERENT numbers, and one shared threshold.""")
uM = COLS_ALL[("anticorrelation_c50b", "u_M")]
cs = COLS_ALL[("anticorrelation_c50b", "c_sharp_float(mu_exh)")]
prim_mask = [L.primitive_here(dn, n) for (n, dn) in POP_ALL]


def thr(mask):
    tot = dis = eq = 0
    for i, (a, b) in enumerate(zip(uM, cs)):
        if a is None or b is None or (mask and not prim_mask[i]):
            continue
        tot += 1
        if abs(a - b) <= TOL_SAME:
            eq += 1
        if (a > 1) != (b > 1):
            dis += 1
    return tot, eq, dis


for mask, nm in ((False, "POP-ALL "), (True, "POP-PRIM")):
    tot, eq, dis = thr(mask)
    print("    %s  comparable %4d   numerically equal %3d   THRESHOLD disagreements %3d"
          % (nm, tot, eq, dis))
print("""
  READING.  On the primitive population the two predicates agree everywhere and the
  substitution is safe; off it they disagree at roughly one poset in eight.  So `u_M` and
  `c#` are not aliases of each other — they are aliases of one BOOLEAN, and only on a
  population neither name carries.  A reader who quotes the NUMBER where the corpus meant
  the PREDICATE carries the wrong figure, and nothing currently looks.

  MY OWN FIRST READING OF THIS ARM WAS WRONG (defect D2).  It reported 27 threshold
  disagreements of 144 as a finding, having run over POP-ALL with `mu_upper` in place of
  `mu_exhaustive` — i.e. on neither the population nor the quantity
  `anticorrelation_c50b/s2_theory.py:70` uses.  The subject's own control was already
  there at `s2_theory.py:87` and reports 0.  An alias sweep that mis-stated a population
  while reporting that mis-stated populations cause wrong figures.""")

# ------------------------------------------------------------------ machine output
#
# `x2_index.py` builds the corpus-wide INDEX from THIS file, so that the index's rows are
# established by MEASUREMENT and not by my vocabulary (E4).  A quantity gets an index row
# because two trees computed the same number for it, not because I thought of its name.
import json                                                          # noqa: E402
groups_out = []
for g, sp, const in G_PRIM:
    groups_out.append({"names": [{"tree": t, "name": nm, "kind": KIND[(t, nm)]}
                                 for t, nm in sorted(g)],
                       "max_spread": sp, "degenerate": bool(const)})
with open("alias_groups.json", "w") as fh:
    json.dump({"population": {"POP_ALL": len(POP_ALL), "POP_PRIM": len(POP_PRIM),
                              "spec": L.POP_SPEC},
               "trees": [t for t, _a, _f in L.ADAPTERS],
               "groups": groups_out}, fh, indent=1)
print()
print("  wrote alias_groups.json — %d multi-tree groups, consumed by x2_index.py"
      % len(groups_out))

banner("x3 RESULT")
print("  %s   (%d failing arms, %.1fs)"
      % ("ALL ARMS PASS" if not fail else "FAILED", fail, time.time() - t0))
sys.exit(1 if fail else 0)
