#!/usr/bin/env python3
"""mg-688c s2 -- THE DESCENT SWEEP.  Did anything build on the withdrawn reading?

The ticket's step 3, and the only question mg-cdd5's remedy does not answer.

FOUR POPULATIONS, NAMED BEFORE ANY COUNT:

  POP-A  every line ADDED by a commit in onethird_program whose committer date
         falls inside the relevant claim's hazard window
  POP-B  every macguffin work item whose [created, last-written] interval
         OVERLAPS a hazard window
  POP-C  every macguffin mail message dated inside a hazard window
  POP-D  every reference of the form <affected-doc>:<N> anywhere in
         onethird_program at HEAD -- the line-anchor test, which is the one
         mechanical way to prove somebody read the STALE copy rather than a
         current one

A FINGERPRINT HIT IS NOT A DESCENDANT.  Most traffic about these claims in this
programme IS the withdrawal propagating.  A hit counts as a descendant only if
it asserts the withdrawn reading with no trace of the withdrawal around it, and
every such hit is printed in full for adjudication rather than being counted.
"""
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lib688c import *  # noqa

REPAIR = mirror_reflog()[0]["at"]
HAZARD = {c["id"]: push_time(c["landed"])[0] for c in CLAIMS}

# This instrument's own directory contains SYNTHETIC occurrences of every
# fingerprint -- the claim table in lib688c.py, the controls in s3, this
# docstring.  mg-cdd5 had to exclude its own directory for the same reason.
SELF_DIR = "code/superseded_descent_688c"

print("=" * 78)
print("mg-688c s2 -- DID ANYTHING DESCEND FROM THE SUPERSEDED READINGS?")
print("=" * 78)
print("""
  repair at %s -- every hazard window closes here
  fingerprints: %d, over %d withdrawn claims
  self-exclusion: %s (contains synthetic fingerprints)
""" % (fmt(REPAIR), sum(len(c["fps"]) for c in CLAIMS), len(CLAIMS), SELF_DIR))

print("  PER-CLAIM HAZARD WINDOWS (from s0):")
for c in CLAIMS:
    print("    %-4s %s -> repair   (%s)" %
          (c["id"], fmt(HAZARD[c["id"]]), dur(HAZARD[c["id"]], REPAIR)))

totals = {"hits": 0, "bare": 0}
bare_rows = []


def report(popname, unit, in_window, scanned, hits):
    totals["hits"] += len(hits)
    bare = [h for h in hits if h["verdict"] == "BARE"]
    totals["bare"] += len(bare)
    print()
    print(rule())
    print("%s" % popname)
    print(rule())
    print("  %-42s %d" % ("%s in population (all time)" % unit, scanned))
    print("  %-42s %d" % ("%s inside a hazard window" % unit, in_window))
    print("  %-42s %d" % ("fingerprint occurrences", len(hits)))
    print("  %-42s %d" % ("of which CARRIES-WITHDRAWAL", len(hits) - len(bare)))
    print("  %-42s %d" % ("of which BARE (hand-adjudicated below)", len(bare)))
    by_claim = {}
    for h in hits:
        by_claim.setdefault(h["claim"], [0, 0])
        by_claim[h["claim"]][0] += 1
        if h["verdict"] == "BARE":
            by_claim[h["claim"]][1] += 1
    if by_claim:
        print("  by claim:  " + "   ".join(
            "%s %d(%d bare)" % (k, v[0], v[1]) for k, v in sorted(by_claim.items())))
    for h in bare:
        bare_rows.append((popname, h))


# ---------------------------------------------------------------------------
# POP-A -- onethird_program commits
# ---------------------------------------------------------------------------
all_commits = citing_commits(ts("2026-01-01T00:00:00Z"), REPAIR)
earliest = min(HAZARD.values())
window_commits = [c for c in all_commits if earliest <= c["at"] <= REPAIR]
hits = []
for com in window_commits:
    added = None
    for cl in CLAIMS:
        if not (HAZARD[cl["id"]] <= com["at"] <= REPAIR):
            continue
        if added is None:
            added = "\n".join(added_lines(com["sha"]))
            # a commit that only touches this instrument is self-exclusion
        for h in scan(added, cl):
            h["where"] = "%s %s %s" % (com["sha"][:7], fmt(com["at"]),
                                       com["subject"][:60])
            hits.append(h)
report("POP-A -- onethird_program commits (ADDED lines only)",
       "commits", len(window_commits), len(all_commits), hits)

# ---------------------------------------------------------------------------
# POP-B -- macguffin work items
# ---------------------------------------------------------------------------
wis = work_items()
hits = []
n_in = 0
for wi in wis:
    live = [cl for cl in CLAIMS
            if wi["mtime"] >= HAZARD[cl["id"]] and wi["created"] <= REPAIR]
    if live:
        n_in += 1
    for cl in live:
        for h in scan(wi["text"], cl):
            h["where"] = "%s  created %s  written %s" % (
                os.path.relpath(wi["path"], MG_ROOT),
                fmt(wi["created"]), fmt(wi["mtime"]))
            hits.append(h)
report("POP-B -- macguffin work items", "work items", n_in, len(wis), hits)

# ---------------------------------------------------------------------------
# POP-C -- macguffin mail
# ---------------------------------------------------------------------------
mails = mail_items()
hits = []
n_in = 0
for m in mails:
    live = [cl for cl in CLAIMS if HAZARD[cl["id"]] <= m["at"] <= REPAIR]
    if live:
        n_in += 1
    for cl in live:
        for h in scan(m["text"], cl):
            h["where"] = "%s  %s" % (os.path.relpath(m["path"], MG_ROOT),
                                     fmt(m["at"]))
            hits.append(h)
report("POP-C -- macguffin mail", "messages", n_in, len(mails), hits)

# ---------------------------------------------------------------------------
# POP-D -- THE LINE-ANCHOR TEST
# ---------------------------------------------------------------------------
# The other three populations detect a claim being REPEATED.  This one detects
# the ACT OF READING: a line number into an affected document that resolves at
# 912f1b1 and does not resolve at origin/main can only have been copied out of
# the stale copy.  It is the only test here that does not depend on the author
# happening to reuse the claim's wording.
print()
print(rule())
print("POP-D -- LINE ANCHORS INTO THE AFFECTED DOCUMENTS  (the ACT OF READING)")
print(rule())

basenames = {k: v.split("/")[-1] for k, v in DOCS.items()}
short = {"RC": "Reverse-Cheeger", "KS": "KillShot", "CR": "ComparisonRoute",
         "BK": "BK-Transport"}

# Two exclusions, both instrument directories that hold stale anchors AS DATA:
# this one, and mg-cdd5's -- whose transcripts quote the mirror-era anchors it
# was measuring.  Counting those as descendants would score the investigation
# of the defect as an instance of it.
EXCLUDE = (SELF_DIR, "code/mirror_staleness_cdd5")
files = [f for f in git(CITING_REPO, "ls-files").splitlines()
         if not f.startswith(EXCLUDE)]
print("  files at HEAD: %d  (excluded: %s)" % (len(files), ", ".join(EXCLUDE)))

mirror_lines = {k: show(MIRROR_REPO, MIRROR_REV, v).splitlines()
                for k, v in DOCS.items()}
tip_lines = {k: show(MIRROR_REPO, TIP_REV, v).splitlines()
             for k, v in DOCS.items()}

# Two anchor shapes, and the second one is why this is not a one-line grep.
#
#   EXPLICIT   `...Reverse-Cheeger-Proof-Attempt.md:310`  -- path then line
#   BARE       the document is named, and a few clauses later a backticked
#              `:310-313` refers to it with no path repeated
#
# mg-cdd5's extractor saw only the first shape and its author found a bare one
# BY HAND.  A bare anchor is attributed to the NEAREST PRECEDING filename, not
# to whatever affected document was mentioned somewhere earlier in the
# paragraph: attributing by mere proximity pulls in `step1.tex:20-26` and
# `main.tex:283-291` sitting in the same sentence, and those are not anchors
# into these documents at all.  That over-attribution is what a first cut of
# this step did, and it produced 33 "stale-only" anchors of which most were
# other files' line numbers wearing this file's name.
FNAME = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.\-]*\.(?:md|tex|py|json|html|txt)")
BARE = re.compile(r"`:(\d+)(?:[-\u2013]\d+)?`")

anchors = []
for f in files:
    try:
        with open(os.path.join(CITING_REPO, f), errors="replace") as fh:
            text = fh.read()
    except (OSError, IsADirectoryError):
        continue
    for key in DOCS:
        for m in re.finditer(re.escape(basenames[key]) + r"[`)\]]{0,3}:(\d+)", text):
            anchors.append((f, key, int(m.group(1)), "EXPLICIT"))
    for m in BARE.finditer(text):
        prev = None
        for fm in FNAME.finditer(text, max(0, m.start() - 400), m.start()):
            prev = fm.group(0)
        if prev is None:
            continue
        for key in DOCS:
            if prev == basenames[key]:
                anchors.append((f, key, int(m.group(1)), "BARE"))

seen = set()
uniq = []
for a in anchors:
    k = (a[0], a[1], a[2])
    if k not in seen:
        seen.add(k)
        uniq.append(a)

print("  anchors found: %d raw, %d unique (file, doc, line)" %
      (len(anchors), len(uniq)))

stale_only = []
for f, key, n, shape in uniq:
    ml = mirror_lines[key][n - 1] if 0 < n <= len(mirror_lines[key]) else None
    tl = tip_lines[key][n - 1] if 0 < n <= len(tip_lines[key]) else None
    if ml is not None and ml.strip() and ml != tl:
        stale_only.append((f, key, n, ml, tl, shape))

print("  anchors whose line differs between the two revisions: %d" %
      len(stale_only))
if not stale_only:
    print("""
  ZERO.  Every line anchor into the four affected documents that survives at
  HEAD resolves to the SAME text at %s and at %s.  There is no
  anchor left anywhere in this repository that can only have come from the
  stale copy -- mg-cdd5 repaired the three that existed, and there is no
  fourth.""" % (MIRROR_REV, TIP_REV))
else:
    for f, key, n, ml, tl, shape in stale_only:
        print("    [%s] %s -> %s:%d" % (shape, f, basenames[key], n))
        print("       at %s: %s" % (MIRROR_REV, (ml or "")[:90]))
        print("       at %s: %s" % (TIP_REV, (tl or "(past end of file)")[:90]))

# --- DATING EACH BROKEN ANCHOR ------------------------------------------
# The decisive question for a broken anchor is NOT that it is broken.  It is
# WHEN it was written.  An anchor authored BEFORE the push that shifted those
# line numbers was CORRECT against the live remote at the moment it was typed;
# it says nothing about which tree its author was reading.  Only an anchor
# authored AFTER that push can prove a stale read -- at that point the live
# remote no longer carries the cited text at the cited line and the mirror
# still does.
print()
print("  DATING EACH BROKEN ANCHOR -- authored before or after the shift?")
SHIFTED_BY = {"RC": "bde9610", "KS": "a8688f2", "CR": "a8688f2",
              "BK": "af7fc2d"}
proved_stale = []
for f, key, n, ml, tl, shape in stale_only:
    shift_at = push_time(SHIFTED_BY[key])[0]
    needle = ("%s:%d" % (basenames[key], n)) if shape == "EXPLICIT" else (":%d" % n)
    log = git(CITING_REPO, "log", "--format=%H%x00%cI%x00%s", "-S", needle,
              "--", f, check=False).strip().splitlines()
    intro = log[-1].split("\x00") if log else None
    when = ts(intro[1]) if intro else None
    verdict = "UNDATED"
    if when is not None:
        verdict = ("PROVES-STALE-READ" if when > shift_at
                   else "correct-when-written")
    print("    %-56s :%-4d %s" % (f[-56:], n, verdict))
    print("        anchor written %s   lines shifted %s (%s)" %
          (fmt(when) if when else "?", fmt(shift_at), SHIFTED_BY[key]))
    if intro:
        print("        by %s  %s" % (intro[0][:7], intro[2][:56]))
    if verdict == "PROVES-STALE-READ":
        proved_stale.append((f, key, n, ml, when))

print()
print("    ANCHORS THAT PROVE A STALE READ: %d of %d" %
      (len(proved_stale), len(stale_only)))

if stale_only:
    print()
    print("  WHERE THE CITED TEXT MOVED TO AT %s (repair table, NOT applied)" % TIP_REV)
    print("  -- reported so a successor's repair is a lookup, not a re-derivation.")
    print("  -- mg-cdd5 scoped its anchor repair to STATE.md; editing three other")
    print("  -- documents is a different job from answering what descended.")
    for f, key, n, ml, tl, shape in stale_only:
        target = [i + 1 for i, ln in enumerate(tip_lines[key]) if ln == ml]
        print("    %-50s %s:%d -> %s" %
              (f[-50:], basenames[key], n,
               ", ".join(":%d" % t for t in target) if target
               else "(text no longer present verbatim)"))

# the same test against what the WINDOW authored, not just what survives
print()
print("  AND AGAINST WHAT THE WINDOW AUTHORED (not just what survives at HEAD):")
authored = []
for com in window_commits:
    for ln in added_lines(com["sha"]):
        for key in DOCS:
            for m in re.finditer(re.escape(basenames[key]) + r"[^\n]{0,4}?:(\d+)",
                                 ln):
                authored.append((com, key, int(m.group(1)), ln))
print("    anchors written by in-window commits: %d" % len(authored))
aw_stale = []
for com, key, n, ln in authored:
    ml = mirror_lines[key][n - 1] if 0 < n <= len(mirror_lines[key]) else None
    tl = tip_lines[key][n - 1] if 0 < n <= len(tip_lines[key]) else None
    if ml is not None and ml.strip() and ml != tl:
        aw_stale.append((com, key, n, ln))
print("    of which resolve at %s but not at %s: %d" %
      (MIRROR_REV, TIP_REV, len(aw_stale)))
for com, key, n, ln in aw_stale:
    print("      %s %s  ->  %s:%d" % (com["sha"][:7], fmt(com["at"]),
                                      basenames[key], n))
    print("        %s" % re.sub(r"\s+", " ", ln)[:150])

# ---------------------------------------------------------------------------
print()
print(rule("="))
print("THE BARE HITS, IN FULL -- these are the candidate descendants")
print(rule("="))
if not bare_rows:
    print("""
  NONE.  Every fingerprint occurrence in every population carried a withdrawal
  marker within %d characters.""" % CONTEXT)
else:
    for i, (pop, h) in enumerate(bare_rows, 1):
        print()
        print("  [%d] %s  claim %s  fp %r" % (i, pop.split(" --")[0],
                                              h["claim"], h["fp"]))
        print("      %s" % h["where"])
        for line in wrap(h["excerpt"], 6):
            print(line)

print()
print(rule("="))
print("TALLY")
print(rule("="))
print("  fingerprint occurrences, all populations: %d" % totals["hits"])
print("  CARRIES-WITHDRAWAL:                       %d" %
      (totals["hits"] - totals["bare"]))
print("  BARE (candidate descendants):             %d" % totals["bare"])
print("  stale-only line anchors at HEAD:          %d" % len(stale_only))
print("  stale-only line anchors authored in-window: %d" % len(aw_stale))
print("== s2 exit: 0 ==")
