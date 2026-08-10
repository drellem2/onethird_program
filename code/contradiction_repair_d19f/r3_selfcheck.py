"""mg-d19f r3 — THE REPAIR CHECKED AGAINST THE DEFECT IT REPAIRS.

The defect: a BLANKET CLAIM about another document's labelling, published without having
read every appearance. This repair is an artifact of exactly that kind, so it can carry
exactly that defect -- and the way it would carry it is by asserting the OPPOSITE blanket
("mg-28ff's n = 7 figures were not correctly labelled"), which is also false: every n = 7
CELL does carry the word (sample). mg-29fe found THREE joints, and three is not "every".

Seven arms. Three must REFUSE something, and two of them fired on me first — D1/D1b and D2
below, both kept.
"""

import re
import subprocess
import sys

import libd19f as L

fails = []


def arm(name, ok, detail):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    for line in detail.split("\n"):
        print(f"         {line}")
    if not ok:
        fails.append(name)


L.banner("r3 — THE REPAIR, CHECKED AGAINST ITS OWN DEFECT CLASS")

doc = "\n".join(L.head_lines(L.DOC_51F4))
lines = L.head_lines(L.DOC_51F4)

# ---------------------------------------------------------------- C1
# STRUCK, NOT DELETED. Both false sentences must still be readable, inside ~~...~~.
struck = re.findall(r"~~(.+?)~~", doc, re.S)
s_all = " ".join(struck)
c1a = "correctly labelled as such at every appearance" in s_all
c1b = "was correctly labelled a sample at each" in s_all
arm("C1  both false sentences are STRUCK, and neither is DELETED",
    c1a and c1b,
    f"site A inside ~~...~~: {c1a}\n"
    f"site B inside ~~...~~: {c1b}\n"
    f"{len(struck)} strikethrough span(s) in the document")

# ---------------------------------------------------------------- C2
# NO OPPOSITE BLANKET. The repair must not claim mg-28ff's figures were uniformly
# mislabelled. Any sentence of MINE combining a universal with a labelling verdict is a
# candidate; the check is over the repair text only, with struck text excluded (the struck
# blanket is supposed to be there -- that is what a strikethrough is for).
unstruck = re.sub(r"~~.+?~~", " ", doc, flags=re.S)
UNIVERSAL = re.compile(
    r"(never (?:correctly )?labelled|nowhere labelled|none of (?:its|mg-28ff's) [^.]*labelled|"
    r"no `?n = 7`? (?:figure|row|cell)[^.]*labelled)", re.I)
bad = UNIVERSAL.findall(unstruck)
arm("C2  the repair asserts NO opposite blanket over mg-28ff's labelling",
    not bad,
    f"candidate opposite-blanket phrasings found: {bad if bad else 'none'}\n"
    "the repair says 'three joints' and names each; it never says 'nowhere' or 'never'.")

# ---------------------------------------------------------------- C3
# EVERY JOINT CARRIES A CITATION. A joint stated without a file:line is the same shape as
# the sentence being repaired: a characterisation the reader must take on trust.
sec = doc.split("## §0.0")[1].split("\n## §0.")[0]
cites = {
    "joint 1": "0.832530" in sec and "100 % at every enumerated" in sec,
    "joint 2": "NOT a maximum" in sec and "1 of 3" in sec,
    "joint 3": "b2_census.py:138" in sec and "b5_trend.py:48" in sec,
    "the measurement": "out_s3_n7.txt" in sec and "168 of 86278" in sec,
    "the reporter": "landing_audit_sweep_64cb" in sec,
    "the instrument": "code/contradiction_repair_d19f/" in sec,
}
arm("C3  every joint and every number in §0.0 carries a citation",
    all(cites.values()),
    "\n".join(f"{'ok ' if v else 'MISSING'}  {k}" for k, v in cites.items()))

# ---------------------------------------------------------------- C4
# NO HARMONISING. mg-28ff must not have been touched by this ticket -- the ticket's explicit
# instruction is to correct the false site and leave the true one alone.
# D1 (kept): this read `git diff --name-only main...HEAD` on its first run and reported
# NOTHING CHANGED while an edited working tree sat under it -- a committed-state probe
# answering a working-tree question, and it would have gone green at every moment before
# the commit, which is exactly when the arm is worth running.
#
# D1b (kept, and it is the arc's own recurring defect): the fix read `main`, and `main` in a
# polecat worktree is a LOCAL ref that nobody here updates. It sat 1 commit AHEAD of this
# branch's base, so the arm reported twelve files of mg-724a's as "changed by this ticket".
# A ref chosen for its name rather than for what it points at -- mg-f8e5's `c1_rebase.py:48`
# and mg-223d's pinned refs are the same shape. The baseline is now the BRANCH POINT,
# computed, and REFUSED if it does not resolve.
base = subprocess.run(["git", "-C", L.REPO, "merge-base", "origin/main", "HEAD"],
                      capture_output=True, text=True).stdout.strip()
if not base:
    print("  [FAIL] C4  cannot resolve the branch point (origin/main missing) -- REFUSED")
    sys.exit(1)
changed = subprocess.run(
    ["git", "-C", L.REPO, "diff", "--name-only", base],
    capture_output=True, text=True).stdout.split()
changed += subprocess.run(
    ["git", "-C", L.REPO, "ls-files", "--others", "--exclude-standard"],
    capture_output=True, text=True).stdout.split()
outside = sorted({f for f in changed
                  if not f.startswith("code/contradiction_repair_d19f/")})
arm("C4  mg-28ff is NOT edited; exactly one document outside this tree changed",
    outside == [L.DOC_51F4],
    f"changed outside this instrument: {outside}\n"
    f"expected exactly: ['{L.DOC_51F4}']")

# ---------------------------------------------------------------- C5
# NO FIGURE MOVED. This is a labelling repair; if any measured literal in the document
# changed, it is not the repair it says it is. Compared as a MULTISET against main.
MEASURED = re.compile(r"(?<![\w.])\d+\.\d{3,}(?![\w])")
before = sorted(MEASURED.findall(L.show(base, L.DOC_51F4)))
after = sorted(MEASURED.findall(doc))
added = [x for x in after if after.count(x) > before.count(x)]
dropped = [x for x in before if before.count(x) > after.count(x)]
# The repair legitimately ADDS quoted evidence (0.832530 from mg-28ff's row, and the
# literals it names in the residue paragraph). It must DROP nothing.
arm("C5  NO measured literal is DROPPED (added ones are the quoted evidence)",
    not dropped,
    f"dropped: {sorted(set(dropped)) if dropped else 'none'}\n"
    f"added  : {sorted(set(added))}")

# ---------------------------------------------------------------- C6
# NON-VACUITY OF C2. If the opposite-blanket detector cannot fire, C2 is worthless. Feed it
# a sentence this repair deliberately does not contain.
probe = "None of mg-28ff's n = 7 rows was correctly labelled anywhere in the document."
arm("C6  the opposite-blanket detector FIRES on a planted sentence",
    bool(UNIVERSAL.search(probe)),
    f"planted: {probe}\n"
    f"detector -> {UNIVERSAL.findall(probe)}")

# ---------------------------------------------------------------- C7
# D2 (kept, and it changed the work): C5's `added` list is what caught this. Quoting
# mg-28ff's f*(7) SAMPLE value 0.832530 as joint 1's evidence falsified §12's bullet
# "mg-28ff's n = 7 sample figures are not quoted anywhere ... the one place I mention one".
# Reading it out, that bullet was ALREADY false at 2f76a01 -- §11's table rows 2, 3 and 4
# quote all three sample values verbatim -- so it is a THIRD blanket of the same class,
# falsified by a table in this document rather than by another one. It is struck too.
# This arm is what keeps the repair from having created a fresh false sentence.
SAMPLES = {"0.176145": "c_true(7)", "0.850074": "c#(7)", "0.832530": "f*(7)"}
appear = {v: [i + 1 for i, ln in enumerate(lines) if v in ln] for v in SAMPLES}
bullet_struck = "sample figures are not quoted anywhere" in s_all
# The correction beside the strikethrough must NAME every value that actually appears --
# a correction that replaced one blanket with a shorter blanket would pass C1 and mean
# nothing. `corr` is the unstruck text of the §12 bullet only.
corr = unstruck.split("Struck and\n  corrected by `mg-d19f`")[-1][:1400]
named_in_repair = all(v in corr for v in SAMPLES)
c7 = bullet_struck and named_in_repair and all(appear[v] for v in SAMPLES)
arm("C7  §12's 'not quoted anywhere' bullet is struck, and every appearance is named",
    c7,
    "\n".join(f"{v} ({SAMPLES[v]:9s}) appears at lines {appear[v]}" for v in SAMPLES)
    + f"\n§12 bullet struck: {bullet_struck}   every value named in the correction: {named_in_repair}")

print()
if fails:
    print(f"SELFCHECK FAILED: {len(fails)} arm(s): {', '.join(fails)}")
    sys.exit(1)
print("SELFCHECK: 7 of 7 arms pass.")
