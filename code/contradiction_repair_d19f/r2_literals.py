"""mg-d19f r2 — THE OTHER ELEVEN.

mg-64cb's s4 screen intersected the MEASURED literals (decimals with >= 3 fraction digits)
on mg-51f4's added canonical lines with those on mg-29fe's correction lines, and got twelve:

  0.019169 0.176 0.250000 0.306250 0.308339 0.327508 0.341 0.550747 0.923894 0.943649
  0.968818 1.078

mg-64cb hand-read one of them and said so: 'a shared literal is a NECESSARY condition and
not a finding'. This arm reads the rest. It does not re-open anybody's mathematics -- the
ticket forbids that and mg-29fe's own verdict already records that mg-51f4's handling of
mg-28ff's n = 7 figures is 'carried and not used, which is the correct handling'. What it
asks of each literal is only: WHICH COMMIT PUT IT THERE, and does mg-51f4's document
actually publish it.

THE ANSWER IS NOT WHAT THE SCREEN'S NAME SUGGESTS, and the cause is one line of mg-64cb's
index. lib64cb attributes a commit to EVERY work-item id that appears anywhere in it, which
is right for 'which items does this commit concern' and wrong for 'which item wrote it'.
mg-51f4's 'canonical' commit list therefore contains three commits, and only one of them is
mg-51f4's landing. The other two are a later ticket that cites mg-51f4 and -- this is the
sharp one -- mg-29fe's OWN AUDIT COMMIT, so for three of the twelve literals the screen
intersected the audit with itself.

This is reported as a property of the SCREEN, not as a defect of mg-64cb's report, which
says in its own words that the screen is a screen. What it changes is the size of the
residue a successor has to hand-read: it is five, not eleven, and all five are mg-51f4's
own independently recomputed n <= 6 values.
"""

import os
import re
import subprocess
import sys

import libd19f as L

sys.path.insert(0, os.path.join(L.REPO, "code", "landing_audit_sweep_64cb"))
import lib64cb as L64  # noqa: E402

TWELVE = ["0.019169", "0.176", "0.250000", "0.306250", "0.308339", "0.327508",
          "0.341", "0.550747", "0.923894", "0.943649", "0.968818", "1.078"]
MEASURED = re.compile(r"(?<![\w.])\d+\.\d{3,}(?![\w])")

L.banner("r2 — THE OTHER ELEVEN, READ")

idx = L64.build()["idx"]
canon = idx["mg-51f4"]["canonical"]

print("""
STEP 1 -- WHOSE COMMITS ARE ON THE 'LANDING SIDE' OF THE SCREEN?
""")
print(f"  lib64cb's idx['mg-51f4']['canonical'] = {canon}")
print()
print(f"  {'commit':9s} {'wrote it':9s} {'authored':26s} subject")
for h in canon:
    print(f"  {h:9s} {L.item_of(h):9s} {L.author_date(h):26s} {L.subject(h)[:66]}")
print("""
  ONE of the three is mg-51f4's landing. lib64cb's index is built by MENTION, so a commit
  that names mg-51f4 joins mg-51f4's list -- including the audit's own commit.
""")

print("""
STEP 2 -- EACH OF THE TWELVE, ATTRIBUTED TO THE COMMIT THAT ADDED IT
""")
where = {v: [] for v in TWELVE}
lines = {}
for h in canon:
    d = subprocess.run(["git", "-C", L.REPO, "show", h, "--unified=0", "--",
                        "STATE.md", "docs", "README.md"],
                       capture_output=True, text=True).stdout
    for line in d.split("\n"):
        if line.startswith("+") and not line.startswith("+++"):
            for m in MEASURED.findall(line):
                if m in where and h not in where[m]:
                    where[m].append(h)
                    lines.setdefault((m, h), line[1:].strip())

print(f"  {'literal':10s} {'added by':9s} {'i.e.':9s} the added line")
for v in TWELVE:
    if not where[v]:
        print(f"  {v:10s} {'-':9s} {'-':9s} (not added by any of the three)")
    for h in where[v]:
        print(f"  {v:10s} {h:9s} {L.item_of(h):9s} {lines[(v, h)][:96]}")

by_item = {}
for v in TWELVE:
    owners = {L.item_of(h) for h in where[v]}
    by_item.setdefault(tuple(sorted(owners)), []).append(v)

print("""

STEP 3 -- THE RESIDUE THAT IS ACTUALLY mg-51f4's
""")
for owners, vs in sorted(by_item.items(), key=lambda kv: -len(kv[1])):
    print(f"  {', '.join(owners) or '(none)':22s} {len(vs):2d}   {' '.join(vs)}")

mine = [v for v in TWELVE if "mg-51f4" in {L.item_of(h) for h in where[v]}]
print(f"""
  Published by mg-51f4's OWN landing ({L.C_51F4_LANDING}): {len(mine)} of 12 -- {' '.join(mine)}
""")

print("""
STEP 4 -- THE READ. Each of mg-51f4's five, in its own document, with the question asked.
""")
head51 = L.head_lines(L.DOC_51F4)
for v in mine:
    hits = L.find(head51, v)
    print(f"  {v}")
    for ln in hits:
        print(f"     {L.DOC_51F4}:{ln}  {head51[ln - 1].strip()[:110]}")

print("""
  ALL FIVE ARE n <= 6 CELLS OF mg-51f4's OWN EXHAUSTIVE TABLE (§4), and none is carried
  from mg-28ff: mg-51f4 recomputes the n <= 6 population on an instrument that shares no
  source line with lib28ff and computes the transport by a down-set dynamic program rather
  than by filtering n! permutations (§4, and the colophon). Its P12 records the agreement as
  a FORMALITY it had to earn: '5230 / 4377, 1,4,27,275,4070, c_true(6) = 0.327508,
  c#(6) = 0.943151'.

  AND mg-29fe WITHDREW NO FIGURE. Its verdict is CONFIRMED WITH REPAIRS over four
  falsification arms; the repairs landed by mg-b58d and mg-3bb9 are labels, a diagnosis, an
  over-claim, an under-claim and a citation -- and both landing commits say NO FIGURE
  WITHDRAWN in their own subjects. So there is no superseded n <= 6 value for any of the
  five to be.

  THE ONE DISAGREEMENT mg-51f4 DID RECORD is f*(6): mg-28ff prints 0.811654, mg-51f4 gets
  0.8116489. It is NOT in the twelve (neither spelling appears on a correction line of the
  audit under the screen's regex), mg-51f4 records it rather than smoothing it, and mg-29fe
  found the cause -- 20 bisection steps over [0,4], the sixth decimal being the upper
  bracket end. Conservative, not wrong. NOT re-opened here.

  ONE LITERAL NEEDS ITS SPELLING SAID OUT LOUD. `0.176` is mg-29fe's rounding of mg-28ff's
  n = 7 sample c_true; mg-51f4 writes the same quantity as `0.176145`, which the screen's
  regex tokenises separately, so `0.176` is NOT evidence that mg-51f4 published it. mg-51f4
  DOES quote that one figure, once, at :150, and its §12 says so in advance and says why:
  'The one place I mention one -- its c_true(7) = 0.176145 in §4 -- is to record that the
  enumerated maximum is 1.93x larger, and it carries the word *sample* in the same
  sentence.' That is mg-29fe's 'carried and not used, which is the correct handling', and it
  is not what this ticket repairs.

  RESIDUE AFTER THIS ARM: 0. The other eleven are read. Five are mg-51f4's own recomputed
  n <= 6 values and carry nothing; three (0.019169, 0.176, 0.341) were contributed by
  mg-29fe's own audit commit and are the screen intersecting the audit with itself; four
  (0.923894, 0.943649, 0.968818, 1.078) were contributed by mg-c50b's later landing, which
  is a different ticket and post-dates both documents.
""")

print("""
WHAT THIS ARM CANNOT SAY
""")
print("""  It cannot say mg-51f4 carried nothing WRONG from mg-28ff in prose that shares no literal
  with the audit's correction lines. The screen is a literal intersection and so is this
  arm; the labelling claim -- the thing this ticket actually repairs -- carries NO literal
  at all and would never have been found by either. That is the honest limit, and it is the
  same limit mg-64cb states: a shared literal is a necessary condition, not a finding, and
  the absence of one is not an absence of defect.
""")
