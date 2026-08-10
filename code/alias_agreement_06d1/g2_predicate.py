"""g2 — THE PREDICATE ARM.  Its own arm, because a boolean that agrees is quieter.

mg-0d1b's largest alias group is not a scalar at all: ten trees carry ten names for the
PRIMITIVITY PREDICATE, agreeing at all 404 posets, and it matters more than any float row
because it defines the population every published `6 of 275` is stated over.

A BOOLEAN THAT AGREES IS QUIETER THAN A FLOAT THAT AGREES.  A float column carries ~306
independent values and two of them matching by accident is not a thing that happens.  A
boolean column carries one bit per poset, and an equality check on it can pass for at
least four reasons a float check would not.  Each has its own arm below:

  P3  THE POPULATION HIDES IT.  Every one of these predicates is TRUE at every poset of
      POP-PRIM, by construction — that is what POP-PRIM is.  So a predicate replaced by
      `return True` agrees with all nine others on the published population and is caught
      only off it.  The arm plants exactly that and shows the same mutation GREEN on
      POP-PRIM and RED on POP-ALL.  This is why g2 runs on POP-ALL and g1 does not.

  P4  AGREEMENT IS INVARIANT UNDER THE POPULATION MOVING.  Ten predicates agreeing with
      EACH OTHER says nothing about which posets they were asked about.  If the poset
      generator changed, all ten would follow it and go on agreeing perfectly.  Only
      pinning the VECTOR — its digest, in BASELINE.json — catches that, and the arm plants
      a population shift in which pairwise disagreements stay at 0.

  P5  bool() COERCION.  A predicate that started returning a truthy non-boolean coerces to
      the same vector and goes on agreeing.  The baseline pins the returned TYPE, and the
      arm plants a predicate returning [1]/[] — identical under bool(), identical digest,
      caught only by the type record.

  P6  A PREDICATE THAT DOES NOT DISCRIMINATE CANNOT CORROBORATE.  If a column is constant,
      "it agrees" is a statement about nothing.  The live split is asserted, not assumed.

Cost: 0.1 s.  The whole arm is free next to g1's 30 s recompute, which is worth stating
plainly — it has been free the entire time nobody ran it.
"""

import sys
import time

import libagree as A
import predicates as PR

L = A.L
t0 = time.time()
BL = A.load_baseline()
PB = BL["predicate"]
REF = "lib0d1b:primitive_here"

POP_ALL = L.population(L.POP_SPEC)
PRIM_IDX = [i for i, (n, dn) in enumerate(POP_ALL) if L.primitive_here(dn, n)]

print("g2  THE PREDICATE ARM — one BOOLEAN, ten trees, ten names")
print()
print("  population POP-ALL   %d posets   (NOT POP-PRIM — see P3)" % len(POP_ALL))
print("  pinned     %d predicates + %s as the population's own" % (len(PB["names"]), REF))

if len(POP_ALL) != PB["n_posets"]:
    print("\n  REFUSED — population is %d posets, baseline pinned %d."
          % (len(POP_ALL), PB["n_posets"]))
    sys.exit(A.BROKEN)


# ------------------------------------------------------------------ the check

def digest(vec):
    import hashlib
    return hashlib.sha256(bytes(1 if v else 0 for v in vec)).hexdigest()[:16]


def check_pred(vecs, types, restrict=None, use_digest=True, use_types=True,
               use_discrim=True):
    """Problems with this set of predicate vectors.  `restrict` = index subset.

    The `use_*` flags are not options for the gate — the gate always runs with all of
    them on.  They exist so that arms P3/P4/P5 can run the WEAKER check somebody would
    plausibly have written ("do the ten booleans agree?") beside the real one, and show
    the input on which the weaker one is silent.  A design decision demonstrated is worth
    more than a design decision argued.

    DEFECT D1, RECORDED.  My first P3b left `use_discrim` on and called the result "the
    naive check", which it was not: the discrimination test is this gate's own addition.
    It reported 10 problems and the scoreboard scored the arm FALSE-POSITIVE, which is
    the scoreboard working.  The 10 were real and are printed by G2c below — on POP-PRIM
    every one of these predicates IS constant, which is the same fact P3 is about, read
    from the other end.
    """
    problems = []
    sel = (lambda v: [v[i] for i in restrict]) if restrict is not None else (lambda v: v)

    missing = [n for n in PB["names"] if n not in vecs]
    for m in missing:
        problems.append(("PREDICATE-LOST", m, "no longer computed by its tree"))

    ref = sel(vecs[REF])
    for name in PB["names"]:
        if name not in vecs:
            continue
        v = sel(vecs[name])
        d = sum(1 for a, b in zip(v, ref) if a != b)
        if d:
            first = next(i for i, (a, b) in enumerate(zip(v, ref)) if a != b)
            idx = restrict[first] if restrict is not None else first
            n, dn = POP_ALL[idx]
            problems.append(("PREDICATE-DISAGREE", name,
                             "%d of %d posets disagree with %s; first at poset #%d "
                             "(n=%d, dn=%s): %s says %s, %s says %s"
                             % (d, len(v), REF, idx, n, dn, name, v[first], REF,
                                ref[first])))
        if use_discrim and len(set(v)) < 2:
            problems.append(("NON-DISCRIMINATING", name,
                             "constant %s over all %d posets — a predicate that does not "
                             "discriminate cannot corroborate one that does"
                             % (v[0] if v else "?", len(v))))
        if use_types and types.get(name) != PB["return_types"].get(name):
            problems.append(("RETURN-TYPE", name,
                             "returns %s, baseline recorded %s — identical under bool(), "
                             "which is the point"
                             % (types.get(name), PB["return_types"].get(name))))

    if use_digest:
        for name in [REF] + PB["names"]:
            if name not in vecs:
                continue
            g = digest(vecs[name])
            if g != PB["vector_digest"]:
                problems.append(("VECTOR-MOVED", name,
                                 "digest %s, baseline pinned %s — the predicates may "
                                 "still agree with each other; they are agreeing about a "
                                 "different population" % (g, PB["vector_digest"])))
    return problems


# ------------------------------------------------------------------ P1  the live reading
A.banner("G2a  THE LIVE READING — ten predicates, and what they actually discriminate")
VECS, TYPES = PR.vectors(POP_ALL)
t_cap = time.time() - t0
print()
for name in [REF] + PB["names"]:
    v = VECS.get(name)
    if v is None:
        print("  %-46s ABSENT" % name)
        continue
    print("  %-46s True %3d  False %3d  types %s"
          % (name, sum(v), len(v) - sum(v), ",".join(TYPES[name])))
BASE = check_pred(VECS, TYPES)
print()
print("  captured in %.2fs   %d problem(s)" % (t_cap, len(BASE)))

if BASE:
    A.banner("g2 RESULT — RED.  THE POPULATION ITSELF IS IN DISPUTE.")
    A.report([{"label": "primitivity", "tolerance": 0.0, "spread": 0.0,
               "n_pinned": len(PB["names"]), "n_present": len(PB["names"]),
               "problems": BASE}])
    print("""
  No number in INDEX.md is citable while this is red: every MEASURED tolerance there is
  stated over POP-PRIM, and POP-PRIM is this predicate.  File a ticket naming both trees.
  Do not reconcile it by preferring either one, and do not re-cut the population to make
  it agree.  The planted worlds below are NOT RUN — see g1_values.py on mg-e331's D4.""")
    sys.exit(A.RED)

# ------------------------------------------------------------------ planted worlds
A.banner("G2b  POSITIVE CONTROL — five planted worlds on the captured vectors")
SB = A.Scoreboard(base_red=bool(BASE))
VICTIM = "chain_iv_c_81ff:is_primitive"


def clone(vecs, types):
    return {k: list(v) for k, v in vecs.items()}, {k: list(v) for k, v in types.items()}


# ---- P2  one bit.  The ordinary disagreement, and it must name both sides.
v2, t2 = clone(VECS, TYPES)
v2[VICTIM][0] = not v2[VICTIM][0]
p = check_pred(v2, t2)
SB.arm("P2 one bit flipped in %s" % VICTIM, True, bool(p),
       "reported as %s" % ", ".join(sorted({x[0] for x in p})))

# ---- P3  THE ARM THE TICKET ASKED FOR.  `return True` — and the population decides
#          whether anyone can see it.
v3, t3 = clone(VECS, TYPES)
v3[VICTIM] = [True] * len(POP_ALL)
p_all = check_pred(v3, t3)
p_prim = check_pred(v3, t3, restrict=PRIM_IDX, use_digest=False, use_types=False,
                    use_discrim=False)
SB.arm("P3 %s replaced by `return True`, checked on POP-ALL" % VICTIM, True, bool(p_all),
       "reported as %s" % ", ".join(sorted({x[0] for x in p_all})))
SB.arm("P3b the SAME mutation, checked on POP-PRIM by boolean agreement alone, is "
       "SILENT — %d problems" % len(p_prim), False, bool(p_prim),
       "this is the predicate gate somebody would have written; it agrees with all nine "
       "other trees at all %d primitive posets because that is what POP-PRIM IS"
       % len(PRIM_IDX))

# ---- P4  THE POPULATION MOVES AND EVERY PREDICATE FOLLOWS IT.  Pairwise agreement is
#          perfect; the pinned vector is not.
v4, t4 = clone(VECS, TYPES)
for k in v4:
    v4[k] = v4[k][1:] + v4[k][:1]                 # the same shift applied to all eleven
p_pair = check_pred(v4, t4, use_digest=False)
p_full = check_pred(v4, t4)
SB.arm("P4 the population shifts and ALL eleven vectors follow it", True, bool(p_full),
       "pairwise-agreement-only check reports %d problems; the pinned digest reports %s"
       % (len(p_pair), ", ".join(sorted({x[0] for x in p_full}))))

# ---- P5  bool() COERCION.  Same vector, same digest, different type.
v5, t5 = clone(VECS, TYPES)
t5[VICTIM] = ["list"]
p_notype = check_pred(v5, t5, use_types=False)
p_type = check_pred(v5, t5)
SB.arm("P5 %s starts returning [1]/[] — identical under bool()" % VICTIM,
       True, bool(p_type),
       "agreement-and-digest check reports %d problems; the pinned return type reports %s"
       % (len(p_notype), ", ".join(sorted({x[0] for x in p_type}))))

# ---- P6  NON-DISCRIMINATION.  A predicate gone constant-False agrees with nothing, but
#          the arm exists so the DISCRIMINATION test itself is falsified rather than
#          assumed: it must be the reported reason, not a side effect.
v6, t6 = clone(VECS, TYPES)
v6[VICTIM] = [False] * len(POP_ALL)
p6 = check_pred(v6, t6)
SB.arm("P6 %s goes constant-False" % VICTIM, True, bool(p6),
       "NON-DISCRIMINATING present: %s"
       % ("NON-DISCRIMINATING" in {x[0] for x in p6}))

# ---- P7  THE CARRIED TABLE vs THE RECORD.  predicates.py copies x3's V4 table rather
#          than importing it (that script costs 90 s and rewrites this gate's own input).
#          A copy nobody compares is this ticket's subject, so it is compared.
live = sorted(n for n in VECS if n != REF)
SB.arm("P7 predicates.py's ten trees are still mg-0d1b's ten trees",
       False, live != sorted(PB["names"]),
       "carried table %d names, baseline %d names" % (len(live), len(PB["names"])))

UNSAT = SB.print_and_score()

# ------------------------------------------------------------------ G2c
A.banner("G2c  WHY THIS ARM RUNS ON POP-ALL — the same fact, read from the other end")
const_prim = [n for n in [REF] + PB["names"]
              if len({VECS[n][i] for i in PRIM_IDX}) < 2]
print("""
  P3 shows a broken predicate hiding on POP-PRIM.  Here is the reason it can, stated as a
  count rather than as an argument: restricted to POP-PRIM, %d of the %d vectors are
  CONSTANT.  Not most of them — all of them, necessarily, because POP-PRIM is defined as
  the posets where this predicate is true.

  So on POP-PRIM these ten trees agree perfectly and carry ZERO bits of information about
  each other.  It is the one population on which this row of INDEX.md, the largest alias
  group in the corpus, cannot be cashed at all.  g1's tolerances are stated over POP-PRIM
  because that is where the FLOATS are published; g2 runs on POP-ALL because that is the
  only place the BOOLEAN says anything.  The two arms want different populations, and
  that is the substantive reason the predicate row needed an arm of its own.""" % (
    len(const_prim), len([REF] + PB["names"])))

A.banner("g2 RESULT")
print("  10 names for ONE predicate agree at all %d posets, discriminating %d/%d; "
      "%d arms unsatisfactory."
      % (len(POP_ALL), PB["true_count"], len(POP_ALL) - PB["true_count"], UNSAT))
print("  capture %.2fs · total %.2fs" % (t_cap, time.time() - t0))
sys.exit(A.BROKEN if UNSAT else A.GREEN)
