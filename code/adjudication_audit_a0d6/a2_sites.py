"""a2 — THE THREE SITES, THE SURVIVING SITE, AND WHAT WAS STRUCK.

Four questions, one arm each:

  (1) IS `mg-28ff:21` TRUE?  It is a positive claim the landing makes and leaves standing,
      and it is the one nobody re-checked.  Every one of its three components is resolved
      here against `mg-28ff` AT `cb496e9` — the text `mg-51f4` actually read — and against
      `a1`'s re-derivation, never against either document's prose about the other.
  (2) ARE ALL THREE SITES HANDLED, and are they the SAME claim?
  (3) WAS ANYTHING TRUE STRUCK?  Each strikethrough is split into clauses and each clause
      resolved separately, because a sentence being wrong at one clause does not make the
      sentence wrong.
  (4) WAS ANYTHING HARMONISED?  A repair that edits the OTHER document into agreement, or
      that deletes rather than strikes, would make the disagreement unreadable.
"""

import re
import subprocess
import sys

D51 = "docs/OneThird-SweepLoss-mg-51f4.md"
D28 = "docs/OneThird-L2-Conditionality-mg-28ff.md"
LANDING = "095260c"          # the commit under audit
BASE51 = "2f76a01"           # mg-51f4's landing — the text before the repair
READ28 = "cb496e9"           # mg-28ff as mg-51f4 read it

FAILS = []
FINDINGS = []


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True).stdout


def blob(rev, path):
    return sh("git", "show", "%s:%s" % (rev, path)).split("\n")


def arm(name, ok, detail=""):
    print("  [%s] %s" % ("CONFIRMED" if ok else "REFUTED  ", name))
    if detail:
        for line in detail.split("\n"):
            print("        " + line)
    if not ok:
        FAILS.append(name)


head51 = blob("HEAD", D51)
head28 = blob("HEAD", D28)
base51 = blob(BASE51, D51)
read28 = blob(READ28, D28)
H51, B51, R28, H28 = "\n".join(head51), "\n".join(base51), "\n".join(read28), "\n".join(head28)

print("=" * 96)
print("a2 — THE ADJUDICATION'S FOUR CLAIMS, RESOLVED ONE AT A TIME")
print("=" * 96)
print()
print("  %s@%s : %d lines      %s@%s : %d lines" % (D51, BASE51, len(base51), D51, "HEAD", len(head51)))
print("  %s@%s : %d lines      %s@%s : %d lines" % (D28, READ28, len(read28), D28, "HEAD", len(head28)))
print()

# ======================================================================== (1)
print("-" * 96)
print("(1)  THE SURVIVING SITE — IS mg-28ff:21 TRUE?   [nobody re-checked this]")
print("-" * 96)
print()
line21 = head28[20]
print("  %s@HEAD:21" % D28)
print("      " + line21[:180] + (" ..." if len(line21) > 180 else ""))
print()
arm("(1a) line 21 IS the row the landing names — SS4.3 summary, sample-as-enumeration",
    "§4.3 summary" in line21 and "enumerated" in line21 and "sample" in line21
    and "false of the truth" in line21)

# component 1: the sentence exists at cb496e9 and says ENUMERATED
hits247 = [(i + 1, l) for i, l in enumerate(read28)
           if "100 %" in l and "enumerated" in l and "eigenvector" in l]
arm("(1b) component 1 — the SENTENCE exists in mg-28ff as mg-51f4 read it, and says 'enumerated'",
    len(hits247) == 1 and hits247[0][0] == 247,
    "%s@%s:%d\n    %s" % (D28, READ28, hits247[0][0], hits247[0][1]) if hits247 else "NOT FOUND")

# component 2: the n=7 row two lines above is a SAMPLE
row245 = read28[244]
arm("(1c) component 2 — the n = 7 row it summarises IS a sample, two lines above",
    row245.strip().startswith("| 7 |") and "(sample)" in row245 and "106 / 106" in row245,
    "%s@%s:245\n    %s" % (D28, READ28, row245))

# component 3: the number, from a1 — never from either document
a1 = open("out_a1_ground_truth.txt").read() if True else ""
got168 = "(F) FAILS at n = 7          : 168 of 86278" in a1 and "REPRODUCED EXACTLY" in a1
arm("(1d) component 3 — '168 of 86278' RE-DERIVED here, not read from mg-51f4's transcript",
    got168,
    "a1 enumerated all 96428 naturally labelled posets on [7], found 86278 primitive,\n"
    "and CERTIFIED 168 route-(F) failures by exhibited rational vectors.\n"
    "a1 also finds (F) failing at NO n <= 6 — so 'every ENUMERATED n' is true of n <= 6\n"
    "and false ONLY at n = 7, which is exactly the scope mg-28ff:21 claims.")

arm("(1e) mg-28ff:21 IS TRUE — all three components hold",
    len(FAILS) == 0)
print()

# ======================================================================== (2)
print("-" * 96)
print("(2)  ALL THREE SITES — FOUND, HANDLED, AND THE SAME CLAIM?")
print("-" * 96)
print()

SITES = [
    ("1", "SS4, the n = 7 paragraph",
     "correctly labelled as such at every appearance in its document",
     "named by the TICKET (mg-64cb reported it)"),
    ("2", "SS11, above the repair table",
     "None of these is a labelling failure",
     "found by the LANDING — not in the ticket"),
    ("3", "SS12, NOT DONE",
     "sample figures are not quoted anywhere",
     "found by the LANDING — not in the ticket"),
]
for num, where, needle, prov in SITES:
    at_base = [i + 1 for i, l in enumerate(base51) if needle in l]
    at_head = [i + 1 for i, l in enumerate(head51) if needle in l]
    print("  SITE %s — %s   (%s)" % (num, where, prov))
    print("      needle : %r" % needle)
    print("      @%s : lines %s        @HEAD : lines %s" % (BASE51, at_base, at_head))
    arm("(2.%s) the sentence was PRESENT at mg-51f4's own landing" % num, len(at_base) >= 1)
    arm("(2.%s') it is STILL PRESENT at HEAD — struck, not deleted" % num, len(at_head) >= 1)
    print()


def strike_spans(lines):
    """Every ~~...~~ span in the document, as (startline, text). Markdown strikethrough may
    wrap lines, so the whole blob is scanned and spans mapped back to a line number."""
    blob_ = "\n".join(lines)
    out = []
    for m in re.finditer(r"~~(.+?)~~", blob_, re.S):
        ln = blob_[:m.start()].count("\n") + 1
        out.append((ln, m.group(1)))
    return out


spans_head = strike_spans(head51)
spans_base = strike_spans(base51)
print("  STRIKETHROUGH SPANS IN mg-51f4")
print("      @%s : %d      @HEAD : %d      ADDED BY THE LANDING : %d"
      % (BASE51, len(spans_base), len(spans_head), len(spans_head) - len(spans_base)))
for ln, txt in spans_head:
    flat = " ".join(txt.split())
    print("      :%-4d %s" % (ln, flat[:150] + (" ..." if len(flat) > 150 else "")))
print()
# D1 (MINE, KEPT): my first form of this arm asserted ONE strike span per site and went
# RED at 4 of 3.  It was my rule that was wrong, not the landing: SITE 1's paragraph
# carries TWO false clauses and both are struck separately — and the second of them,
# 'I do not quote any of them', is SITE 3's blanket a second time, which is exactly what
# the landing's own SS0.0 row 1 says of it.  The arm now COUNTS the mapping instead of
# assuming it.
site_of_span = []
for ln, txt in spans_head:
    site_of_span.append(1 if ln < 400 else (2 if ln < 500 else 3))
print("      span -> site mapping : %s" % site_of_span)
arm("(2d) the landing struck FOUR spans across THREE sites — SITE 1 carries two false clauses",
    len(spans_base) == 0 and len(spans_head) == 4 and sorted(set(site_of_span)) == [1, 2, 3],
    "the ticket named ONE site (mg-51f4 doc:148). The landing struck three sites and four\n"
    "clauses. The extra clause is SS4's 'I do not quote any of them' — SITE 3's blanket\n"
    "stated a second time in a different section, which is what makes 'all three are ONE\n"
    "defect' a finding rather than a slogan.")

# are they the same claim? each struck span must quantify over LABELLING or QUOTING
LABEL = ("label", "quote", "quoted", "mention", "appearance", "sample")
QUANT = ("every", "each", "all ", "none", "not ", "any", "one place")
same = [(ln, t) for ln, t in spans_head
        if any(w in t.lower() for w in LABEL) and any(w in t.lower() for w in QUANT)]
arm("(2e) EVERY struck span is the SAME class — a QUANTIFIER over how n = 7 figures are\n"
    "       LABELLED or QUOTED.  Nothing of another class was struck alongside them.",
    len(same) == len(spans_head) and len(spans_head) > 0,
    "%d of %d struck spans carry both a quantifier word and a labelling word" % (len(same), len(spans_head)))
print()

# ======================================================================== (3)
print("-" * 96)
print("(3)  WAS ANYTHING TRUE STRUCK?  — clause by clause")
print("-" * 96)
print()

# --- site 1, clause A: 'correctly labelled ... at every appearance'
arm("(3a) SITE 1 clause 'correctly labelled at every appearance' is FALSE",
    len(hits247) == 1,
    "mg-28ff@%s:247 is an APPEARANCE of the n = 7 figure '100 %%' that reads ENUMERATED,\n"
    "two lines under the row at :245 that reads (sample). FALSE, on mg-28ff's own text\n"
    "at the state mg-51f4 read." % READ28)

# --- site 1, clause B: '40-200 posets' mixes units  (PREDICTIONS P9)
src = {}
for f in ("b1_footrule.py", "b2_census.py", "b5_trend.py"):
    src[f] = sh("git", "show", "%s:code/l2_conditionality_28ff/%s" % (READ28, f))
draws = sorted({m.group(1) for f in src for m in re.finditer(r"sample_posets\(7,\s*(\d+)\)", src[f])})
print("      every sample_posets(7, k) in mg-28ff's instrument at %s : k in %s" % (READ28, draws))
arm("(3b) SITE 1 clause 'samples of 40-200 posets' MIXES UNITS — FALSE as written",
    "40" not in draws and "200" in draws,
    "no draw of size 40 exists: the draws are %s.  '40' is a PRIMITIVE COUNT (mg-28ff SS4.2)\n"
    "and '200' is a DRAW SIZE (SS4.1/SS4.3), so the range has no unit.  P9 CONFIRMED." % draws)

# --- site 1, clause C: what was RETAINED
retained = [
    ("deterministic\nsamples", "the figures ARE deterministic samples"),
    ("0.176145", "its n = 7 sample reads c_true = 0.176145"),
    ("0.340719", "the maximum over the enumerated population is 0.340719"),
    ("low by a factor of `1.93`", "the sample was low by a factor of 1.93"),
]
ok = True
for needle, what in retained:
    inb, inh = needle in B51, needle in H51
    print("      RETAINED: %-52s @%s %s  @HEAD %s"
          % (what, BASE51, "y" if inb else "n", "y" if inh else "n"))
    ok = ok and inb and inh
arm("(3c) SITE 1's TRUE clauses all survive — the strike is scoped to the false ones", ok,
    "and a1 re-derives 0.340719 and 0.340719/0.176145 = 1.9343 independently.")

# --- site 2: is it false, and is it false from INSIDE the document?
tbl_row1 = [l for l in head51 if l.startswith("| **1** | **247**")]
arm("(3d) SITE 2 'None of these is a labelling failure' is FALSE — and self-falsifying",
    len(tbl_row1) == 1
    and "sat over a table whose `n = 7` row was a sample" in tbl_row1[0]
    and "is false there" in tbl_row1[0],
    "SS11's own row 1, three lines BELOW the struck sentence, says in mg-51f4's words:\n"
    "  'The word *enumerated* sat over a table whose n = 7 row was a sample, so the\n"
    "   sentence reads as covering n = 7 and is false there.'\n"
    "That is a labelling failure. No second document is needed to refute this sentence.")

# --- site 3: the figures ARE quoted, and they ARE mg-28ff's n=7 sample figures
FIGS = ["0.176145", "0.850074", "0.832530"]
print()
print("      ARE THEY mg-28ff's n = 7 SAMPLE FIGURES?  (checked in mg-28ff@%s, not in mg-51f4)" % READ28)
allsample = True
for v in FIGS:
    # D2 (MINE, KEPT): this probe first required the row to START with '| 7 |' and could
    # not read mg-28ff@cb496e9:200, which is the SAME ROW inside a markdown BLOCKQUOTE.
    # A probe for 'is this figure labelled' that cannot see a quoted table is a probe that
    # would have reported a labelling defect as absent.
    rows = [(i + 1, l) for i, l in enumerate(read28)
            if v in l and l.strip().lstrip("> ").startswith("| 7 |")]
    lab = rows and "sample" in rows[0][1]
    allsample = allsample and bool(lab)
    print("        %s -> %s:%s  labelled '(sample)': %s"
          % (v, D28, rows[0][0] if rows else "NOT FOUND", "yes" if lab else "NO"))
arm("(3e) all three ARE n = 7 sample rows of mg-28ff", allsample)

print()
print("      WERE THEY QUOTED IN mg-51f4 AT ITS OWN LANDING?  (site 3 says 'not anywhere')")
tot_base = 0
for v in FIGS:
    at = [i + 1 for i, l in enumerate(base51) if v in l]
    tot_base += len(at)
    print("        %s @%s : lines %s" % (v, BASE51, at))
arm("(3f) SITE 3 'not quoted anywhere / the one place' is FALSE — and was false ON THE DAY",
    tot_base >= 4,
    "%d occurrences of the three figures at %s, mg-51f4's OWN landing commit.\n"
    "Two of the three figures (0.850074, 0.832530) are quoted in SS11's table and are not\n"
    "the 'one place' the bullet names. Nothing in mg-28ff is needed to see this." % (tot_base, BASE51))

# --- the REPLACEMENT for site 3 must itself be true: 'I do not USE any of them'
print()
print("      THE REPLACEMENT CLAUSE 'I do not USE any of them' — is IT true?")
own_tables = []
for i, l in enumerate(head51):
    if l.strip().startswith("| ") and any(v in l for v in FIGS):
        own_tables.append((i + 1, l))
quoting = [(ln, l) for ln, l in own_tables if "**247**" in l or "**245**" in l
           or "**217**" in l or "**200**" in l]
arm("(3g) every table row carrying one of the three figures is a SS11 REPAIR-PROPOSAL row,\n"
    "       i.e. a QUOTATION of mg-28ff's own cell, not a cell of mg-51f4's",
    len(own_tables) == len(quoting) and len(own_tables) > 0,
    "%d table rows carry one of the three; %d of them are SS11 rows quoting mg-28ff's line"
    % (len(own_tables), len(quoting)))
mine = [(i + 1, l) for i, l in enumerate(head51)
        if l.strip().startswith("| **7** |") or l.strip().startswith("| 7 |")]
print("      mg-51f4's OWN n = 7 table rows (SS4 / SS6), and what they carry:")
for ln, l in mine:
    hit = [v for v in FIGS if v in l]
    print("        :%-4d %s   <- carries %s" % (ln, " ".join(l.split())[:110], hit or "none of the three"))
arm("(3h) none of the three figures enters mg-51f4's OWN tables — 'carried and not used'",
    all(not any(v in l for v in FIGS) for _, l in mine))
print()

# ======================================================================== (4)
print("-" * 96)
print("(4)  WAS ANYTHING HARMONISED?")
print("-" * 96)
print()
touched = [l for l in sh("git", "show", "--stat", "--name-only", "--format=", LANDING).split("\n") if l.strip()]
docs_touched = [f for f in touched if f.startswith("docs/")]
print("      files the landing touched:")
for f in touched:
    print("        " + f)
arm("(4a) the landing edited EXACTLY ONE document, and it is the one it decided against",
    docs_touched == [D51], str(docs_touched))
diff28 = sh("git", "diff", "%s^" % LANDING, LANDING, "--", D28)
arm("(4b) mg-28ff was NOT edited — the false document was corrected, the true one left alone",
    diff28.strip() == "")
arm("(4c) the two documents are NOT harmonised — mg-51f4 does not adopt mg-28ff's wording,\n"
    "       it strikes its own and says which is true",
    "mg-28ff:21` is TRUE" in H51 or "`mg-28ff:21` is TRUE" in H51 or "is TRUE and is left alone" in H51,
    "SS0.0 states the verdict in the corrected document itself, where a reader of the false\n"
    "sentence will meet it.")
# nothing deleted: every line of the base survives or is accounted for
base_set = [l for l in base51 if l.strip()]
gone = [l for l in base_set if l not in head51 and l.replace("**", "") not in H51]
print()
print("      lines present at %s and absent at HEAD: %d" % (BASE51, len(gone)))
for l in gone[:12]:
    print("        - " + " ".join(l.split())[:130])
arm("(4d) the struck sentences remain READABLE — a reader arriving with the old text finds it",
    all(any(k in H51 for k in (needle,)) for _, _, needle, _ in SITES))
# the 'absent lines' above are LINE-WRAP artefacts, not deletions. The honest test is at
# WORD granularity: HEAD must be the base document with INSERTIONS ONLY, i.e. the base's
# word stream must be a SUBSEQUENCE of HEAD's. D3 (MINE, KEPT): my first two forms of this
# arm compared whole LINES and went RED five times on re-wrapping and on bold markers the
# landing added inside the text it was quoting — a deletion detector that cannot tell a
# deletion from a line break.
def words(t):
    t = t.replace("~~", " ").replace("**", " ").replace("*", " ").replace("`", " ")
    return [w.strip(",.;:—-()") for w in re.split(r"\s+", t) if w.strip(",.;:—-()")]
wb, wh = words(B51), words(H51)
i = 0
missed = []
for w in wb:
    j = i
    while j < len(wh) and wh[j] != w:
        j += 1
    if j < len(wh):
        i = j + 1
    else:
        missed.append(w)
print("      base words: %d   HEAD words: %d   base words NOT matched in order: %d"
      % (len(wb), len(wh), len(missed)))
if missed:
    print("        " + " ".join(missed[:40]))
arm("(4e) NOTHING WAS DELETED — mg-51f4 at HEAD is its own landing text with INSERTIONS\n"
    "       ONLY: the entire base word stream, %d words, is an in-order subsequence of\n"
    "       HEAD's %d.  The six 'absent LINES' above are re-wrapping and added bold\n"
    "       markers, not withdrawal." % (len(wb), len(wh)),
    len(missed) == 0)
print()

print("=" * 96)
if FAILS:
    print("REFUTED ARMS: " + "; ".join(FAILS))
    print("=" * 96)
    sys.exit(1)
print("a2 — THE ADJUDICATION IS CONFIRMED ON EVERY ARM.")
print("     mg-28ff:21 TRUE.  Three sites, all handled, all the same claim.")
print("     No true clause struck.  Nothing harmonised.  mg-28ff untouched.")
print("=" * 96)
