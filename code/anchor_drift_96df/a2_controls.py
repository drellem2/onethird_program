"""mg-96df a2 -- THE CONTROLS, and they are mostly aimed at THIS REPAIR.

A remedy is an artifact of the same kind as the defect, so it is subject to it.
The defect here is "a document carries a line number into a file that moved."
The repair is three documents that carry line numbers into a file that will
move.  Every arm below exists because the repair could commit the defect it
reports, and the enumeration was written before the notes were:

  X1  APPEND-ONLY.  Inserting a banner at the top of any of these three files
      shifts every line in it -- and all three ARE cited by line, from
      mg-688c's own deliverable and from mg-cdd5's README.  A repair that
      broke those would have created the defect while reporting it.  This is
      the arm that forced the notes to the bottom of the files.
  X2  NOT ONE NUMBER IN THE NOTES WAS TYPED.  Every relocation the notes state
      is re-derived here from the two revisions and then checked to appear in
      the note.  A typo fails on one side; a wrong derivation on the other.
  X3  THE DURABLE FORM IS DURABLE.  Every section named in a note must exist
      at the cited revision and be UNIQUE there -- a heading occurring twice
      is no better than a line number.
  X4  THE PIN.  The notes' numbers are true at one revision.  This arm checks
      the revision is NAMED, and REPORTS whether it is still current.  It does
      not score currency: a control that goes red because the world moved on
      is mg-d0e2's shape, and mg-cdd5 caught the same arm doing it.
  X5  D1 -- the sweep must not sweep itself, and the exclusion must MATTER.
  X6  THE FINDING ABOUT THE CITED REPO'S OWN BANNER, re-derived.  This is the
      load-bearing evidence for "do not renumber by hand," so it is measured
      here rather than quoted from the note that states it.
  X7  THE ADJUDICATION OF §1.4, re-derived -- which halves of that sentence
      survive at the new revision.
"""
import os
import re
import sys

import lib96df as L

ARMS = []


def arm(name, ok, detail=""):
    ARMS.append((name, bool(ok), detail))
    print("  %-4s %-34s %s" % ("ok" if ok else "FAIL", name, detail))


def banner(t):
    print("\n" + t)
    print("-" * 78)


AUDIT = "docs/state-history/audit-mg-eba7-of-mg-55f2.md"
OUTCOMES = "code/row3b_audit_eba7/OUTCOMES.md"
BB60 = "docs/OneThird-Compression-W1-LinearEigenfunction-Provenance-mg-bb60.md"
EDITED = [AUDIT, OUTCOMES, BB60]

KS = "OneThird-Spectral-NearOrdinalSum-KillShot-Probe.md"
CR = "OneThird-StandardDominance-ComparisonRoute.md"
RC = "OneThird-L1b-Reverse-Cheeger-Proof-Attempt.md"
BK = "OneThird-L1b-BK-Transport-Transfer-Probe.md"
ER = "OneThird-L1b-ExpectedRank-Certificate.md"

#: Every relocation the three notes assert.  DECLARED HERE, DERIVED BELOW, and
#: then required to appear in the note -- so the note cannot disagree with the
#: repository in either direction.
#: (note file, cited doc, old line, old end, new line, section heading)
CLAIMS = [
    (AUDIT, CR, 104, None, 104,
     '§1 Three inequivalent statements called "standard dominance"'),
    (AUDIT, KS, 20, None, 68, "Executive verdict"),
    (AUDIT, KS, 103, None, 151, "Kill-shot 2 — Standard dominance"),
    (AUDIT, KS, 198, None, 251, "The N-poset: the skeptical-bar centrepiece"),
    (AUDIT, KS, 286, None, 350, "Data appendix"),
    (AUDIT, RC, 310, None, 449, "5.0′ Correction to the bullet above (mg-d1be)"),
    (AUDIT, RC, 310, 313, 449, "5.0′ Correction to the bullet above (mg-d1be)"),
    (AUDIT, BK, 112, None, 121,
     "2.1 The naive single-cut reading is FALSE (the 166 refuters)"),
    (OUTCOMES, CR, 104, None, 104,
     '§1 Three inequivalent statements called "standard dominance"'),
    (BB60, KS, 127, 142, 180, "Kill-shot 3 — Monotonicity (L2) — AMBER"),
    (BB60, ER, 84, 90, 84, "1. The certificate"),
]


def main():
    root = L.program_root()
    st = L.mirror_state()
    if st.error:
        print("CANNOT MEASURE: %s" % st.error)
        return 2
    now = st.remote_main or st.origin_main

    print("=" * 78)
    print("mg-96df a2 -- CONTROLS ON THE REPAIR")
    print("=" * 78)

    # E1b (mg-20ee).  X1 compares the three edited documents BEFORE and AFTER
    # mg-96df's repair.  It used to spell that "HEAD vs the working tree",
    # which is only the same thing while the repair is still uncommitted in
    # the author's own checkout -- so it measured p96df's desk, and for every
    # later operator it silently re-answered a different question about a
    # corpus three months further on.  The two states are now named as what
    # they are: SELF_AT^ is before the repair, SELF_AT is after it.  MEASURED,
    # NOT ASSERTED: this reproduces the committed 363/115, 77/33 and 253/32.
    notes = {rel: L.self_read(root, rel) for rel in EDITED}
    before = L.SELF_AT + "^" if L.SELF_AT != "WORKTREE" else "HEAD"

    # ------------------------------------------------------------------ X1
    banner("X1  APPEND-ONLY -- no existing line number in the three edited\n"
           "    documents moved, so no anchor INTO them can have broken.")
    for rel in EDITED:
        rc, head, _ = L.git(["show", before + ":" + rel], cwd=root)
        if rc != 0:
            arm("X1 " + os.path.basename(rel)[:22], False, "not at " + before)
            continue
        old = head.split("\n")
        new = notes[rel].split("\n")
        n = len(old)
        # git's blob ends with a trailing "" from the final newline; compare
        # the real lines only.
        while old and old[-1] == "":
            old.pop()
        n = len(old)
        same = new[:n] == old
        grew = len(new) > n
        arm("X1 " + os.path.basename(rel)[:22], same and grew,
            "%d lines unchanged, %d appended" % (n, max(0, len(new) - n))
            if same else "AN EXISTING LINE CHANGED -- anchors into this file broke")

    # E1b (mg-20ee): the corpus is read AT L.SELF_AT, not off the working tree.
    incoming = []
    for path in L.self_tracked(root):
        if path.startswith("code/anchor_drift_96df"):
            continue
        if not path.endswith((".md", ".txt", ".py", ".html")):
            continue
        try:
            body = L.self_read(root, path)
        except (UnicodeDecodeError, OSError):
            continue
        for target in EDITED:
            for m in re.finditer(re.escape(target) + r":(\d+)", body):
                incoming.append((path, target, int(m.group(1))))
    arm("X1 incoming anchors exist", len(incoming) > 0,
        "%d line anchors point INTO the three edited documents -- this is why "
        "the notes are appended" % len(incoming))
    for src, tgt, n in sorted(set(incoming)):
        print("        %s  ->  %s:%d" % (src, os.path.basename(tgt), n))

    # ------------------------------------------------------------------ X2
    banner("X2  NOT ONE NUMBER IN THE NOTES WAS TYPED -- every relocation is\n"
           "    re-derived from the two revisions, then required to appear.")
    blobs = {}

    def get(rev, doc):
        k = (rev, doc)
        if k not in blobs:
            blobs[k] = L.blob_lines(st.path, rev, "docs/" + doc)
        return blobs[k]

    for note, doc, a, b, want, _sec in CLAIMS:
        old, new = get(L.READ_REV, doc), get(now, doc)
        m = L.relocate_block(old, a, b, new) if b else L.relocate(old, a, new)
        label = "%s:%d%s" % (doc.split("-")[-1][:14], a, "-%d" % b if b else "")
        derived_ok = m.determinate and m.line == want
        in_note = ("`:%d`" % want) in notes[note] or (":%d" % want) in notes[note]
        arm("X2 %-22s" % label, derived_ok and in_note,
            "derived :%s (%s), note says :%d" % (m.line, m.tier, want))

    # ------------------------------------------------------------------ X3
    banner("X3  THE DURABLE FORM IS DURABLE -- every section a note names must\n"
           "    exist at the cited revision AND be unique there.")
    for note, doc, a, b, want, sec in CLAIMS:
        new = get(now, doc)
        head = L.enclosing_heading(new, want)
        found = head is not None and head[1].startswith(sec)
        uniq = found and L.heading_is_unique(new, head[1])
        in_note = sec[:34] in notes[note]
        arm("X3 %-22s" % sec[:22], found and uniq and in_note,
            "encloses :%d, unique, quoted in the note" % want if found and uniq
            else "heading missing, not unique, or not quoted")

    # ------------------------------------------------------------------ X4
    banner("X4  THE PIN.  Numbers in a note are true at ONE revision, so the\n"
           "    revision must be NAMED.  Currency is REPORTED, never scored.")
    for rel in EDITED:
        arm("X4 %s" % os.path.basename(rel)[:22], L.PINNED_REV in notes[rel],
            "names the revision its numbers are true at")
    current = now is not None and now.startswith(L.PINNED_REV)
    print("      REPORTED, NOT SCORED: the cited repo's remote main is %s, and "
          "the notes'\n      revision is %s -- %s"
          % ((now or "?")[:12], L.PINNED_REV,
             "still current" if current else
             "NO LONGER CURRENT.  The notes' numbers need re-deriving; run a1."))

    # ------------------------------------------------------------------ X5
    banner("X5  D1 -- the sweep must exclude the directories that DISCUSS\n"
           "    anchors, and the exclusion must MATTER.")
    # Measured by running the extraction BOTH ways.  "The exclusion is
    # correct" is an opinion; "the exclusion changes the answer by N" is not.
    import a1_anchors as A1

    def count(excluded):
        keep, A1.EXCLUDED_DIRS = A1.EXCLUDED_DIRS, excluded
        try:
            hits = 0
            for rel in A1.repo_files(root):
                try:
                    body = L.self_read(root, rel)
                except (UnicodeDecodeError, OSError):
                    continue
                hits += len(A1.RE_EXPLICIT.findall(body))
            return hits
        finally:
            A1.EXCLUDED_DIRS = keep

    with_ex = count(A1.EXCLUDED_DIRS)
    without = count([])
    mine = count([d for d in A1.EXCLUDED_DIRS if d != "code/anchor_drift_96df"])
    arm("X5 self-exclusion matters", without > with_ex,
        "%d anchor-shaped strings repo-wide, %d after excluding the three "
        "instrument directories (%d of the difference are this instrument's own)"
        % (without, with_ex, mine - with_ex))

    # ------------------------------------------------------------------ X6
    banner("X6  THE CITED REPO'S OWN HAND-WRITTEN RENUMBERING, re-derived.\n"
           "    This is the evidence for 'do not renumber by hand', so it is\n"
           "    measured here and not quoted from the note that states it.")
    new_ks = get(now, KS)
    old_ks = get(L.READ_REV, KS)
    row = L.relocate(old_ks, 286, new_ks)
    arm("X6 the row is at :350", row.line == 350, "content match says :%s" % row.line)
    at345 = L.line_at(new_ks, 345) or ""
    arm("X6 :345 is NOT the row", "standard-dominance failures" not in at345,
        "the banner's own number lands on: %s" % at345.strip()[:46])
    banner_txt = "\n".join(new_ks[20:24])
    arm("X6 the banner says :345", ":345" in banner_txt and "+59" in banner_txt,
        "quoted verbatim from %s lines 21-24" % KS[:26])
    offsets = []
    for a in (20, 103, 127, 198, 286):
        m = L.relocate(old_ks, a, new_ks)
        offsets.append(m.line - a if m.line else None)
    arm("X6 no single offset exists", len(set(offsets)) > 1,
        "the five anchors move by %s -- '+59 from here down' cannot be right "
        "for all of them" % ", ".join("+%d" % o for o in offsets))
    rc, out, _ = L.git(["log", "--format=%H", "912f1b1..%s" % now, "--",
                        "docs/" + KS], cwd=st.path)
    touching = [x for x in out.split("\n") if x.strip()]
    arm("X6 one commit did it all", len(touching) == 1,
        "%d commit touched that file in the window, so this is NOT later drift "
        "-- the figure was wrong when written" % len(touching))

    # ------------------------------------------------------------------ X7
    banner("X7  THE ADJUDICATION OF §1.4 -- which halves of its closing\n"
           "    observation survive at the new revision.")
    qualifier = ("FRAME", "IN-FRAME")
    for old_n, new_n, want_qual in ((20, 68, True), (103, 151, True),
                                    (198, 251, False)):
        line = L.line_at(new_ks, new_n) or ""
        has = any(q in line for q in qualifier)
        arm("X7 :%d -> :%d qualifier" % (old_n, new_n), has == want_qual,
            "%s scope qualifier at the new revision"
            % ("gained a" if has else "still carries NO"))
    arm("X7 :198 is byte-identical",
        L.line_at(old_ks, 198) == L.line_at(new_ks, 251),
        "so '*a reader who stops at :198 gets an unqualified holds*' still stands")

    # ------------------------------------------------------------------
    bad = [n for n, ok, _ in ARMS if not ok]
    print("\n" + "=" * 78)
    print("a2: %d arms, %d satisfactory, %d FAIL%s"
          % (len(ARMS), len(ARMS) - len(bad), len(bad),
             "  -- " + ", ".join(bad) if bad else ""))
    print("=" * 78)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
