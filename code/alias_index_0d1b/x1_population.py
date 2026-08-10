"""x1 — THE POPULATION.  What this sweep examined, and what it did not.

The ticket's step 4: "STATE THE POPULATION YOU SEARCHED, on a clean result as well as a
dirty one.  If the sweep finds only V10, that is a real and useful answer ONLY if it names
what it examined."

This arm exists because the defect the ticket is about — the smallest `n` an instrument
looked at, published as the smallest `n` where the thing happens — is a POPULATION defect.
`mg-789d` reported `n = 6` because `n = 6` was the floor of its sweep.  A sweep that
reported "12 trees examined, 12 alias groups found" without saying which 12 of 184, and
what the other 172 are, would be the same defect in a different coat.

Exit 0 always: this arm counts, it does not judge.
"""

import collections
import os
import re
import sys
import time

import lib0d1b as L

t0 = time.time()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(ROOT)
SELF = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

PROBED = {t for t, _a, _f in L.ADAPTERS}

# The screen for "this tree does poset mathematics at all".  It is a LEXICAL screen and
# it is stated as one: a tree that enumerates linear extensions, order ideals or
# downsets, or that builds a transport matrix, is doing the arc's mathematics; a tree
# that greps transcripts is not.  A tree can defeat this screen by computing a poset
# scalar without any of these tokens, and if one does, it is in the "no idiom" bucket
# wrongly.  Nothing here detects that, and saying so is cheaper than pretending.
IDIOM = re.compile(r"linear_extension|order_ideal|downsets|def transport|"
                   r"permutations\(range")

# The name-forms the value probe ESTABLISHED (x3's clusters), used to ask which unprobed
# trees compute one of the already-indexed quantities.  Derived from the adapters rather
# than typed, so it cannot drift from what x3 measured.
MEASURED_NAMES = set()
for _t, _ad, _f in L.ADAPTERS:
    for k in _ad((0, 1, 3), 3):
        MEASURED_NAMES.add(k.split("(")[0].split("[")[0])


def banner(s):
    print()
    print("=" * 78)
    print(s)
    print("=" * 78)


trees = sorted(d for d in os.listdir(ROOT)
               if os.path.isdir(os.path.join(ROOT, d)) and not d.startswith("."))
files = collections.Counter()
per_tree = {}
for t in trees:
    d = os.path.join(ROOT, t)
    py, txt, md, blob = [], [], [], []
    for dp, dn, fns in os.walk(d):
        for fn in fns:
            p = os.path.join(dp, fn)
            if fn.endswith(".py"):
                py.append(p)
            elif fn.endswith(".txt"):
                txt.append(p)
            elif fn.endswith(".md"):
                md.append(p)
    for p in py:
        with open(p, encoding="utf8", errors="replace") as fh:
            blob.append(fh.read())
    per_tree[t] = {"py": py, "txt": txt, "md": md, "src": "\n".join(blob)}
    if t != SELF:
        files["py"] += len(py)
        files["txt"] += len(txt)
        files["md"] += len(md)

docs = [f for f in os.listdir(os.path.join(REPO, "docs")) if f.endswith(".md")]

print("x1  THE POPULATION THIS SWEEP EXAMINED")
print()
print("  NAME LAYER — every tracked file under code/ and docs/, this instrument excluded")
print("    trees under code/ .............. %d  (+1, this instrument, excluded below)"
      % (len(trees) - 1))
print("    .py files ...................... %d" % files["py"])
print("    transcripts (*.txt) ............ %d" % files["txt"])
print("    .md under code/ ................ %d" % files["md"])
print("    canonical documents in docs/ ... %d" % len(docs))
print("    STATE.md ....................... %d lines"
      % len(open(os.path.join(REPO, "STATE.md"), encoding="utf8").read().splitlines()))
print()
print("  VALUE LAYER — where a number could actually be produced and compared")
print("    posets in POP-ALL .............. %d   (every naturally-labelled poset, n=3,4,5)"
      % len(L.population(L.POP_SPEC)))
print("    of those, primitive (POP-PRIM) . %d"
      % sum(1 for (n, dn) in L.population(L.POP_SPEC) if L.primitive_here(dn, n)))
print("    trees with an adapter .......... %d" % len(PROBED))
print("    scalar columns compared ........ %d"
      % sum(len(ad((0, 1, 3), 3)) for _t, ad, _f in L.ADAPTERS))

banner("WHY 172 TREES ARE NOT IN THE VALUE LAYER — the classification, by machine")

buckets = collections.defaultdict(list)
for t in trees:
    if t == SELF:
        continue
    if t in PROBED:
        buckets["probed"].append(t)
    elif not per_tree[t]["py"]:
        buckets["no python at all"].append(t)
    elif not IDIOM.search(per_tree[t]["src"]):
        buckets["no poset idiom — a META tree (transcripts, pins, gates, provenance)"]\
            .append(t)
    else:
        buckets["POSET MATHEMATICS, NO ADAPTER WRITTEN — the residue"].append(t)

for k in ("probed",
          "POSET MATHEMATICS, NO ADAPTER WRITTEN — the residue",
          "no poset idiom — a META tree (transcripts, pins, gates, provenance)",
          "no python at all"):
    v = buckets[k]
    print()
    print("  %-4d %s" % (len(v), k))
    if k.startswith("no poset idiom"):
        print("       (not listed individually — %d trees; these compute nothing this "
              "sweep could compare)" % len(v))
        continue
    for i in range(0, len(v), 3):
        print("       " + "  ".join("%-30s" % x for x in v[i:i + 3]))

banner("THE RESIDUE, RANKED — which unswept trees define an ALREADY-INDEXED name")
print("""
  The %d trees above do the arc's mathematics and have no adapter here.  The question
  that matters is not how many there are, it is which of them compute a quantity this
  index already has a row for — because those are the free controls this sweep has NOT
  cashed.  A tree is listed below if its `.py` DEFINES a symbol whose name is one the
  value layer established.""" % len(buckets["POSET MATHEMATICS, NO ADAPTER WRITTEN — the residue"]))
defined_in = collections.defaultdict(set)
for t in trees:
    if t == SELF:
        continue
    for ln in per_tree[t]["src"].splitlines():
        m = re.match(r"\s*(?:def\s+(\w+)\s*\(|(\w+)\s*=[^=])", ln)
        if m:
            nm = m.group(1) or m.group(2)
            if nm in MEASURED_NAMES:
                defined_in[nm].add(t)

AMBIG_AT = 8
ambiguous = {nm for nm, ts in defined_in.items() if len(ts) > AMBIG_AT}
print()
print("    AMBIGUOUS TOKENS, EXCLUDED FROM THE RANKING AND NAMED INSTEAD (rule: a name")
print("    defined in more than %d trees is not evidence of anything):" % AMBIG_AT)
for nm in sorted(ambiguous, key=lambda x: -len(defined_in[x])):
    print("      `%s` is defined in %d trees.  In `lstar_789d`, `audit_5cba`, "
          "`anticorrelation_c50b`" % (nm, len(defined_in[nm])))
    print("      and `sweep_loss_51f4` it is route (F)'s mean and the four AGREE exactly")
    print("      (x3 V2).  Elsewhere it is a matrix, a multiplicity or a loop variable,")
    print("      and NOTHING IN THIS INDEX CAN TELL WHICH — the name carries no type.")
    print("      That is a finding about the name, not a gap in the sweep.")
rows = []
for t in buckets["POSET MATHEMATICS, NO ADAPTER WRITTEN — the residue"]:
    hits = {nm for nm in MEASURED_NAMES
            if nm not in ambiguous and t in defined_in.get(nm, ())}
    if hits:
        rows.append((len(hits), t, sorted(hits)))
rows.sort(reverse=True)
print()
for k, t, hits in rows:
    print("    %-32s %d: %s" % (t, k, ", ".join(hits)))
print()
print("    %d of %d residue trees define at least one already-indexed, UNAMBIGUOUS name."
      % (len(rows), len(buckets["POSET MATHEMATICS, NO ADAPTER WRITTEN — the residue"])))
print("""
    THESE ARE THE NEXT TICKET, AND THEY ARE NAMED RATHER THAN COUNTED.  Each is a place
    where an alias probably exists and this sweep did not check it.  Reporting the sweep
    as complete without this list would be the ticket's own defect: the smallest set an
    instrument looked at, published as the set where the thing happens.""")

banner("WHAT THE VALUE LAYER CANNOT SEE EVEN WHERE IT RUNS")
print("""
  * `n <= 5`.  Two scalars that agree over 306 primitive posets at n = 3,4,5 can differ
    at n = 8.  Nothing here bears on that, and no row of INDEX.md claims otherwise.

  * FAMILIES.  Every published statement about `rho*Delta` at n >= 6 is about a FAMILY
    (chain(n-1)+point, near-ordinal antichains), not about a sweep.  This instrument
    compares per-poset scalars and has no family arm.

  * numpy.  `l2_audit_29fe.mu_pref_float` imports numpy at `lib29fe.py:347` and numpy is
    NOT INSTALLED in this environment, so that entry point cannot run here at all.  The
    29fe column in the value layer is its EXACT path (`bracket_mu_pref`, copositivity by
    bisection) instead.  Recorded because a reader who assumes the transcripts of
    `l2_audit_29fe` can be reproduced on this machine is wrong, and that is a fact about
    the corpus, not about this ticket.""")

banner("x1 RESULT")
print("  population stated: %d trees, %d .py, %d transcripts, %d docs; value layer %d "
      "trees / %d posets   (%.1fs)"
      % (len(trees) - 1, files["py"], files["txt"], len(docs), len(PROBED),
         len(L.population(L.POP_SPEC)), time.time() - t0))
sys.exit(0)
