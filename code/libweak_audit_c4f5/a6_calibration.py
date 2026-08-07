#!/usr/bin/env python3
"""a6_calibration — AUDIT TARGET 4 ((LIB-weak) vs (LIB-const)) plus the standing targets.

Four things, all cheap and all checkable, none of which needs a poset:

  C1  the eps_spec arithmetic, at BOTH calibrations, so the `~50` and the `~5x10^3`
      are the same computation with one input changed
  C2  the class chain `(LIB) c (LIB-weak) c (LIB-const)` -- FALSIFIED BY CONSTRUCTION
      as a statement about the objects satisfying the conditions, by exhibiting an
      explicit o(n^2) function that violates (LIB-const) at its own constant
  C3  the Delta_AT / Theorem G drift check (P15) -- a target reported even though it
      does not fire, because a target that never fires and is never reported cannot be
      distinguished from a target never run
  C4  bound words and the superseded-calibration figures, counted in the parent doc
"""
import re
import os
import subprocess
from fractions import Fraction

DOC = "../../docs/OneThird-LIBweak-mg-c3ca.md"
STATE = "../../STATE.md"

print("=" * 78)
print("a6_calibration -- target 4 and the standing targets")
print("=" * 78)

print()
print("-" * 78)
print("C1. THE (LIB-weak) vs (LIB-const) GAP, PRICED AT BOTH CALIBRATIONS")
print("-" * 78)
print("(LIB-const) is   E[inv_e] <= (eps_spec/6)(n^2-1).")
print("E_unif[inv]  is  C(n,2)/2 = n(n-1)/4.")
print("Freezing gives unconditionally (mg-88bd Claim 6.1)  E[inv_e] < m/3 <= n(n-1)/6,")
print("i.e. (2/3) of the uniform value, i.e. eps_spec = n/(n+1) -> 1.")
print()
print("%10s %16s %20s %18s %14s"
      % ("eps_spec", "as frac of unif", "held (frac of unif)", "gap factor", "source"))
for eps, src in ((2e-4, "mg-88bd Sec.6.4 / mg-c3ca Sec.2.3"),
                 (2e-2, "mg-e35c F5 (audited) / STATE.md")):
    need = (eps / 6.0) / 0.25            # (eps/6)n^2 as a fraction of n^2/4
    held = 2.0 / 3.0
    print("%10.1e %16.6g %20.6g %18.6g %14s" % (eps, need, held, held / need, ""))
    print("%10s %16s %20s %18s %s" % ("", "", "", "", "   " + src))
print()
print("  So the SAME arithmetic gives ~5x10^3 at 2e-4 and ~50 at 2e-2, and the gap")
print("  factor is exactly 1/eps_spec (times n/(n+1)):  1/2e-4 = %g, 1/2e-2 = %g."
      % (1 / 2e-4, 1 / 2e-2))
print("  mg-c3ca Sec.2.3 prints the 2e-4 branch. STATE.md, at the commit mg-c3ca was")
print("  written against, says in bold: `do not carry 2x10^-4 or the n = 10^5 crossover")
print("  as flat text`.  Both appear in Sec.2.3 as flat text.")

print()
print("-" * 78)
print("C2. THE CLASS CHAIN, FALSIFIED BY CONSTRUCTION")
print("-" * 78)
print("mg-c3ca Sec.2.3 bullet 1 (quoting mg-88bd Sec.6.2):")
print("    `(LIB) O(n) c (LIB-weak) o(n^2) c (LIB-const) <= c n^2`")
print("An inclusion of classes IS an implication.  Bullet 2 then says `neither implies")
print("the other outright`.  Both cannot be read literally.  Which is right:")
print()
print("Construction: f(n) = n^2 / log2(n)  for n >= 2, f(n) = 10^6 for n < 2.")
print("f is o(n^2).  Is f <= c n^2 at EVERY n for the architecture's c = eps_spec/6?")
c_needed = 2e-2 / 6
print("  c = eps_spec/6 = %.6g   (at the repaired eps_spec = 2e-2)" % c_needed)
import math
# DEFECT 5 OF THIS INSTRUMENT, kept: this was first written as a search loop capped at
# n = 10^6.  It found nothing and PRINTED `None` as though None were the answer -- a
# cap reported as a measurement, which is the exact shape this audit criticises in
# others.  Replaced by the closed form, which is why the number below is enormous.
# f(n) = n^2/log2(n) <= c n^2  <=>  log2(n) >= 1/c  <=>  n >= 2^(1/c).
first_ok = 2.0 ** (1.0 / c_needed)
print("  f(n) <= c n^2  <=>  log2(n) >= 1/c = %.0f  <=>  n >= 2^%.0f ~ 10^%.0f"
      % (1 / c_needed, 1 / c_needed, math.log10(2) * (1 / c_needed)))
print("  So f is o(n^2) and VIOLATES (LIB-const) at EVERY n below about 10^%.0f."
      % (math.log10(2) * (1 / c_needed)))
print("  (At the SUPERSEDED eps_spec = 2e-4 the same construction runs to 10^%.0f.)"
      % (math.log10(2) * 6 / 2e-4))
print()
print("  AND THE THRESHOLD IS UNBOUNDED, not merely large: for ANY N0 whatsoever,")
print("  g(n) := n^2 for n < N0 and n^2/log2(n) for n >= N0 is o(n^2) and violates")
print("  (LIB-const) below N0.  So `N0 unspecified` is not a technicality about an")
print("  unknown constant -- NO N0 EXISTS that works for all of (LIB-weak).")
print()
print("  VERDICT C2: as a statement about GROWTH-RATE CLASSES with (LIB-const) read as")
print("  O(n^2), the chain is correct.  As a statement about the OBJECTS satisfying the")
print("  three conditions at the architecture's own constant, `(LIB-weak) c (LIB-const)`")
print("  IS FALSE, and the failure interval is unbounded over the class.")
print("  Bullet 2 is right and bullet 1 needs the rider AT ITS OWN SITE.  This is the")
print("  same defect mg-325c repaired in STATE.md at four sites, surviving in the doc.")
print()
print("  AND THE TWO GAPS ARE NOT COMPETITORS.  C1's factor (50) and C2's quantifier")
print("  are different objects:")
print("    C1 = (what freezing gives free) vs (what the architecture needs) : a CONSTANT")
print("    C2 = (LIB-weak) vs (LIB-const)                                  : a QUANTIFIER")
print("  A relay that says `the residual is a constant (~50) RATHER THAN a quantifier`")
print("  has set two true statements about different pairs against each other.")

print()
print("-" * 78)
print("C3. DELTA_AT / THEOREM G DRIFT CHECK (P15) -- REPORTED EVEN THOUGH IT DOES NOT FIRE")
print("-" * 78)
if not os.path.exists(DOC):
    print("  DOC NOT FOUND at %s -- THIS CHECK DID NOT RUN." % DOC)
else:
    txt = open(DOC).read()
    lines = txt.splitlines()
    terms = ["Delta_AT", "Δ_AT", "Hodge", "Theorem G", "Garland", "Kaufman", "ALOV",
             "Alev", "link bound", "Coxeter"]
    hits = []
    for i, ln in enumerate(lines, 1):
        for t in terms:
            if t in ln:
                hits.append((i, t, ln.strip()[:90]))
    print("  terms searched: %s" % ", ".join(terms))
    print("  total occurrences: %d" % len(hits))
    for i, t, ln in hits:
        print("    line %d  [%s]  %s" % (i, t, ln))
    # NON-VACUITY: the same search on a document that DOES discuss the axis must hit.
    ctl = "../../STATE.md"
    ctxt = open(ctl).read() if os.path.exists(ctl) else ""
    cn = sum(ctxt.count(t) for t in terms)
    print()
    print("  NON-VACUITY CONTROL: the same term list over STATE.md hits %d times." % cn)
    print("  If that were 0 the `0 hits` above would be a broken search, not a clean doc.")
    print("  VERDICT: %s" % ("NO DRIFT -- the axis is absent from the deliverable."
                             if len(hits) == 0 else
                             "occurrences present; adjudicate each line above by hand."))

print()
print("-" * 78)
print("C4. BOUND WORDS AND SUPERSEDED FIGURES IN THE PARENT DOC")
print("-" * 78)
if os.path.exists(DOC):
    txt = open(DOC).read()
    lines = txt.splitlines()
    print("  superseded-calibration figures (STATE.md says do not carry as flat text):")
    for pat in ["2×10⁻⁴", "5×10³", "10⁵"]:
        ns = [i for i, ln in enumerate(lines, 1) if pat in ln]
        print("    %-8s : %d occurrence(s) at line(s) %s" % (pat, len(ns), ns))
    print()
    print("  bound words:")
    for w in ["closes", "cannot", "suffices", "strictly", "never", "not blocked",
              "is FALSE", "IN KIND"]:
        ns = [i for i, ln in enumerate(lines, 1) if re.search(w, ln)]
        print("    %-12s : %2d occurrence(s) at line(s) %s" % (w, len(ns), ns[:12]))

print()
print("-" * 78)
print("C5. THE PREMISE'S SECOND HALF -- `NEVER ATTACKED BY ANY ARC` (P3)")
print("-" * 78)
print("This is a claim about the corpus's history and it is checkable.  Two searches:")
print("  (a) which mg items mention (LIB-weak) or `o(n^2)` as a target at all")
print("  (b) which merged docs do")
try:
    out = subprocess.run(["mg", "list", "--all"], capture_output=True, text=True,
                         timeout=120).stdout
    ids = re.findall(r"(mg-[0-9a-f]{4})", out)
    print("  mg items visible to `mg list --all`: %d" % len(set(ids)))
except Exception as e:
    print("  mg list failed: %s -- THIS HALF DID NOT RUN." % e)
print()
print("  (the substantive search is done in a7_history.sh, which greps the item store")
print("   and the merged docs; this section only records that the claim is checkable")
print("   and where it is checked.)")

print()
print("=" * 78)
print("a6_calibration done.")
print("=" * 78)
