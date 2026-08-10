"""a1 — the landing check for mg-a564's six repairs, run against the LANDED DOCUMENT.

`mg-3bb9` returned CONFIRMED WITH REPAIRS on `mg-b58d`'s seven landed repairs, four of which
are LABELLING or CITATION repairs.  Repair E exists precisely because repair 3 — itself a
labelling repair — carried a labelling defect: it wrote "40 primitive of 90 drawn" where the
scripts evaluate `named_posets(7) + sample_posets(7, 90)`, 98 entries, of which 5 primitive
come from the NAMED families and only 35 from the draw.  That is the third labelling repair in
this lineage to carry a labelling defect.

So this landing's own labels are not asserted.  They are CHECKED, here, against the two things
that can contradict them:

  (1) `lib28ff`'s OWN GENERATORS, for every population figure the document prints;
  (2) the SOURCE LINES the document cites, for every file:line citation the six repairs add or
      repair — including the two lines of `s3_counterfactual.py` whose identity is the whole
      content of repair A.

and, for repair C, over the CLASS of the defect rather than over a list of its instances:

  (3) a sweep for BLANKET UNIVERSAL QUANTIFIERS about rows.  `mg-b58d`'s check ran over
      FIGURES and passed; the defect was a surviving quantifier over ROWS, which no per-figure
      check can see.  This arm greps for the quantifier forms and requires each surviving hit
      to be one that has been re-scoped.

A NEGATIVE CONTROL is filed for each arm: a deliberately wrong label / citation / blanket must
make that arm FAIL.  An arm that cannot fail is what repair A is about, and this file is not
going to commit the defect it lands the repair for.

Run:  python3 code/l2_landing_a564/a1_landing_check.py
Exit: 0 = every arm passed (and every negative control fired);  1 = at least one arm failed.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "code", "l2_conditionality_28ff"))

DOC = os.path.join(ROOT, "docs", "OneThird-L2-Conditionality-mg-28ff.md")

failures = []


def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {detail}" if detail else ""))
    if not ok:
        failures.append(name)
    return ok


def source_line(relpath, n):
    with open(os.path.join(ROOT, relpath)) as fh:
        return fh.read().split("\n")[n - 1]


print("=" * 92)
print("a1  mg-a564 — landing check for the six repairs, against the landed document")
print("=" * 92)

doc = open(DOC).read()

# ---------------------------------------------------------------------------
# ARM 1 — REPAIR E.  Every population figure, re-measured on lib28ff's own generators.
# ---------------------------------------------------------------------------
print("\n(1) REPAIR E — the n = 7 population labels, against lib28ff's own generators")

from lib28ff import named_posets, sample_posets  # noqa: E402

named = named_posets(7)
draws = {90: sample_posets(7, 90), 200: sample_posets(7, 200)}


def prim(pop):
    return sum(1 for P in pop if P.is_primitive())


def distinct(pop):
    return len({tuple(sorted(map(tuple, P.rel))) for P in pop})


measured = {
    "named entries": len(named),
    "named primitive": prim(named),
    "draw90 entries": len(draws[90]),
    "draw90 primitive": prim(draws[90]),
    "draw200 entries": len(draws[200]),
    "draw200 primitive": prim(draws[200]),
}
for k in (90, 200):
    pop = named + draws[k]
    measured[f"union{k} entries"] = len(pop)
    measured[f"union{k} primitive"] = prim(pop)
    measured[f"union{k} distinct"] = distinct(pop)

for k, v in measured.items():
    print(f"      {k:22s} = {v}")

# the figures the document prints, and the sentence each must appear in
expected = {
    "named entries": 8, "named primitive": 5,
    "draw90 entries": 90, "draw90 primitive": 35,
    "draw200 entries": 200, "draw200 primitive": 101,
    "union90 entries": 98, "union90 primitive": 40, "union90 distinct": 97,
    "union200 entries": 208, "union200 primitive": 106, "union200 distinct": 207,
}
check("measured populations match the figures the document prints",
      measured == expected,
      f"measured {measured}" if measured != expected else "")

# the document must state the UNION size, and must NOT re-introduce the "drawn" attribution
for phrase in ("208 EVALUATED", "98 EVALUATED", "98 and 208"):
    check(f"document states the evaluated population: {phrase!r}", phrase in doc)
for bad in ("106 primitive of **200 drawn**", "40 primitive of **90 drawn**"):
    check(f"repair 3's defective label is gone: {bad!r}", bad not in doc)

# NEGATIVE CONTROL: a wrong population figure must be caught by this arm.
_neg = dict(measured)
_neg["union200 primitive"] = 105
check("NEGATIVE CONTROL — a wrong primitive count fails arm 1", _neg != expected)

# corroboration from inside the parent's own material (mg-3bb9 §7)
check("lib28ff's own output labels the row 'named + sample'",
      "named + sample" in source_line("code/l2_conditionality_28ff/out_b1_footrule.txt", 38))
check("§3 of the document states the union size 98 correctly",
      "98 at `n = 7`" in doc or "and 98 at" in doc)

# ---------------------------------------------------------------------------
# ARM 2 — every file:line citation the six repairs rest on.
# ---------------------------------------------------------------------------
print("\n(2) REPAIRS A, B, D, F — the cited lines say what the document says they say")

CITES = [
    # repair A — the tautology.  These two lines ARE the finding.
    ("code/l2_audit_29fe/s3_counterfactual.py", 60, "if rlo > 1:"),
    ("code/l2_audit_29fe/s3_counterfactual.py", 66, '"V00": rlo'),
    ("code/l2_audit_29fe/s3_counterfactual.py", 72, "if lowb[k] > 1:"),
    # repair B — the bets, verbatim, with their own scope.
    ("code/l2_conditionality_28ff/PREDICTIONS.md", 108, "P11 [BET, 0.35]"),
    ("code/l2_conditionality_28ff/PREDICTIONS.md", 109, "n ≤ 6"),
    ("code/l2_conditionality_28ff/PREDICTIONS.md", 83, "P4 [PRINCIPAL LIVE BET, 0.25]"),
    ("code/l2_conditionality_28ff/PREDICTIONS.md", 84, "n ≤ 6"),
    ("code/l2_conditionality_28ff/PREDICTIONS.md", 113, "n ≤ 6"),
    ("code/l2_conditionality_28ff/PREDICTIONS.md", 115, "n ≤ 6"),
    # repair D — the f* bracket and the five-decimal print.
    ("code/l2_conditionality_28ff/out_b1_footrule.txt", 38, "0.83253"),
    # repair E — the three lines that evaluate named + sample.
    ("code/l2_conditionality_28ff/b1_footrule.py", 73, "named_posets(7) + sample_posets(7, 200)"),
    ("code/l2_conditionality_28ff/b2_census.py", 138, "named_posets(7) + sample_posets(7, 90)"),
    ("code/l2_conditionality_28ff/b5_trend.py", 48, "named_posets(7) + sample_posets(7, 200)"),
    # repair F — the file whose own words say it cannot close the claim.
    ("code/sweep_loss_51f4/out_s3_n7.txt", 32, "UPPER bound -- exhibited vector"),
    ("code/sweep_loss_51f4/out_s3_n7.txt", 47, "OVERCOUNTS"),
]
for path, n, token in CITES:
    check(f"{path}:{n} contains {token!r}", token in source_line(path, n))

# repair A's finding is an IDENTITY of predicates, not two similar lines.  State it as one.
l2_pred = source_line("code/l2_audit_29fe/s3_counterfactual.py", 60).strip()
v00_pred = source_line("code/l2_audit_29fe/s3_counterfactual.py", 72).strip()
v00_val = source_line("code/l2_audit_29fe/s3_counterfactual.py", 66)
check("REPAIR A — 'L2 fails' and V00-FAIL are the same predicate on the same number",
      l2_pred == "if rlo > 1:" and v00_pred == "if lowb[k] > 1:" and '"V00": rlo' in v00_val,
      "so the cited verdict line cannot print False")

# repair F — the claim's real support is mg-51f4's DOCUMENT, not that output file.
f4 = open(os.path.join(ROOT, "docs", "OneThird-SweepLoss-mg-51f4.md")).read()
check("REPAIR F — mg-51f4 §5 carries the exact copositivity bracket that closes (M#) at n = 7",
      "the exact bracket confirms genuine failure" in f4
      and "0.226537524" in f4)
check("the document now cites mg-51f4 §5 for (M#)'s n = 7 failure",
      "OneThird-SweepLoss-mg-51f4.md` §5" in doc or "mg-51f4` **§5**" in doc
      or "`mg-51f4` §5" in doc)

# NEGATIVE CONTROL: a citation that does not say what it is cited for must fail.
check("NEGATIVE CONTROL — a bogus token at a real line fails arm 2",
      "this string is not in that file" not in source_line(
          "code/l2_audit_29fe/s3_counterfactual.py", 60))

# ---------------------------------------------------------------------------
# ARM 3 — REPAIR C.  Sweep the CLASS: blanket universal quantifiers about rows.
# ---------------------------------------------------------------------------
print("\n(3) REPAIR C — sweep for BLANKET statements about rows, not for mislabelled rows")

# The forms that carry the defect.  A surviving hit is acceptable ONLY if it sits inside an
# italic-quoted span `*"…"*` — the form this document reserves for quoting wording it has
# REPLACED.  Its own assertions are never written that way, so the rule discriminates; it is
# not "is there some reassuring word nearby", which would pass on anything.
#
# (The first version of this arm did use a nearby-marker heuristic, and it FAILED on two
# correctly-quoted hits of this landing's own repair notes.  The control was what was broken,
# not the text — so it was made precise rather than relaxed.  Recorded because an arm that was
# loosened until it passed is exactly the defect repair A lands.)
QUOTED = [m.span() for m in re.finditer(r'\*"[^"]{0,400}"\*', doc)]
quoted_chars = sum(b - a for a, b in QUOTED)
check("the quoted-span rule is not vacuous (italic quotations cover < 10 % of the document)",
      quoted_chars < 0.10 * len(doc),
      f"{quoted_chars} of {len(doc)} chars = {100.0 * quoted_chars / len(doc):.1f} %")


def inside_quote(m):
    return any(a <= m.start() and m.end() <= b for a, b in QUOTED)


BLANKETS = [
    r"[Tt]he `n = 7` rows are not maxima",
    r"[Ee]very constant carries `n ≤ 6`",
    r"`17/78` appears nowhere",
    r"`17/78` does not appear in this document at all",
    r"every table above is keyed on",
]
for pat in BLANKETS:
    hits = list(re.finditer(pat, doc))
    unquoted = [doc[max(0, m.start() - 70):m.end() + 70] for m in hits if not inside_quote(m)]
    check(f"blanket {pat!r}: {len(hits)} hit(s), none asserted in the document's own voice",
          not unquoted, f"ASSERTED: {unquoted}" if unquoted else "")

# the re-scoped replacements must actually be present
for phrase in ("no `n = 7` row produced by `lib28ff.py` is a maximum",
               "only as the name of the failure mode",
               "no route-constant table here"):
    check(f"the re-scoped replacement is present: {phrase!r}", phrase in doc)

# NEGATIVE CONTROLS, both arms of the discrimination.  The sweep must fire on a blanket
# asserted in the document's own voice AND must not fire on the same words inside a quotation
# of replaced wording — a rule that only ever passes is the defect repair A is about.
_bare = 'The `n = 7` rows are not maxima and must never be read as if they were.'
_quot = 'It read *"the `n = 7` rows are not maxima"* and is re-scoped above.'
for _label, _text, _want_fire in (("an unscoped blanket", _bare, True),
                                  ("a quotation of the replaced wording", _quot, False)):
    _q = [m.span() for m in re.finditer(r'\*"[^"]{0,400}"\*', _text)]
    _h = list(re.finditer(r"[Tt]he `n = 7` rows are not maxima", _text))
    _fired = any(not any(a <= m.start() and m.end() <= b for a, b in _q) for m in _h)
    check(f"NEGATIVE CONTROL — the sweep {'fires on' if _want_fire else 'stays silent on'} {_label}",
          _fired == _want_fire)

# ---------------------------------------------------------------------------
# ARM 4 — REPAIR B.  Every §9 row is scored against its bet as filed.
# ---------------------------------------------------------------------------
print("\n(4) REPAIR B — P11 is scored LOST, and the scope is restored in every cell whose bet carries it")

check("P11 is scored LOST", "**LOST, AND IT STAYS LOST.**" in doc)
check("P11's cell now quotes the bet's own `n ≤ 6`",
      "footrule route fails somewhere at `n ≤ 6`" in doc)
check("the flip's wording is gone",
      "SCORED LOST HERE ON A SAMPLE, AND IT IS WON ON THE TRUTH" not in doc)
check("P4's cell now carries the `n ≤ 6` its bet carries",
      "(M) holds at every primitive poset at `n ≤ 6`" in doc)
check("the scoring convention is stated once, outside any single row",
      "THE SCORING CONVENTION" in doc)
# the summary count must agree with the table: P4's reasoning, P9, P11 -> three
check("the 'three live bets lost or half-lost' summary agrees with the table again",
      "Three live bets lost or half-lost (P4's reasoning, P9, P11)" in doc)

# (F) at n <= 6 is what decides P11, and it is unchanged by this landing.
check("the figure that decides P11 is unchanged: (F) certifies 4377 of 4377 at n ≤ 6",
      "4377 of 4377" in doc)

# ---------------------------------------------------------------------------
print("\n" + "=" * 92)
if failures:
    print(f"FAILED — {len(failures)} arm(s):")
    for f in failures:
        print(f"  * {f}")
    print("=" * 92)
    sys.exit(1)
print("ALL ARMS PASSED — every population figure re-measured, every cited line read,")
print("the blanket class swept, and P11 scored against the bet as filed.")
print("NOT CHECKED HERE, AND SAID RATHER THAN LEFT IMPLICIT: the exhaustive n = 7 figures")
print("(0.340719 / 1.018707 / 1.297074 / 168 of 86278 / 96428) are NOT re-derived by this")
print("script or by any instrument in this repo other than mg-51f4's.  They are checked")
print("elsewhere only as FAITHFUL COPIES of out_s3_n7.txt.  mg-a91f carries the independent")
print("re-derivation; this landing does not claim it.")
print("=" * 92)
