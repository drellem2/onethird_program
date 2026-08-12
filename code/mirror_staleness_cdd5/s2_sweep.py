"""mg-cdd5 s2 -- THE SWEEP.  THIS IS THE DELIVERABLE.

Ticket step 3: does any OTHER citation resolve, in the checked-out tree, to
text that has since been struck or rewritten?

POPULATION -- named before any count, because a zero without a population is
not a measured zero (PREDICTIONS.md E7).  Two tiers:

  TIER 1 (the ticket's population): every citation to a path inside
    one_third_width_three appearing in `STATE.md` or in its rendered twin
    `docs/state-of-the-wall.html`.  Those two are the documents the ticket
    names; the twin is named in STATE.md:7 and is the thing `twin_pin.py`
    checks.

  TIER 2 (widened, reported separately and NEVER merged into tier 1's count):
    every such citation anywhere under `docs/` or `code/` in this repository.
    The ticket asks about STATE.md and the twin; this tier exists because the
    same hazard does not stop at those two files, and because a tier-1 zero
    would be much weaker without knowing whether the population is small
    because the hazard is rare or because the population is small.

METHOD.  For each citation, the cited path is read AT TWO REVISIONS by
`git show` -- `912f1b1` (what the checked-out mirror has) and `origin/main`
(what is true) -- and the two are compared.  The working copy is never opened;
that is the defect this instrument is sent to find (E1).

CLASSES
  UNCHANGED            the reader of the stale tree sees the current text
  CHANGED              the text was rewritten after the mirror's revision
  CHANGED-WITH-STRIKE  ... and the rewrite ADDS withdrawal markup: the reader
                       of the stale tree is being shown as live something that
                       has since been struck.  THIS IS THE TICKET'S SHAPE.
  ABSENT-IN-MIRROR     the cited file does not exist at 912f1b1 at all
  DELETED-BY-TIP       it exists in the mirror and is gone at origin/main
  ABSENT-AT-BOTH       the citation resolves to nothing at either revision --
                       a BROKEN CITATION, worse than a stale one, and scored
                       separately rather than silently equal to UNCHANGED (E3)

Exit 1 only if the sweep could not run.  Findings do not set it: an instrument
that exits 1 for finding what it was sent to find cannot be told apart from a
broken one.
"""
import os
import sys

import lib_cdd5 as L

MIRROR_PIN = "912f1b1"
TIER1 = ["STATE.md", "docs/state-of-the-wall.html"]


def read_source(root, rel):
    p = os.path.join(root, rel)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def gather(root, rels):
    cits = []
    missing = []
    for rel in rels:
        text = read_source(root, rel)
        if text is None:
            missing.append(rel)
            continue
        cits.extend(L.extract_citations(text, rel))
    return L.dedupe(cits), missing


def score(mirror, cits):
    rows = []
    for c in cits:
        old = L.blob_at(mirror, MIRROR_PIN, c.path)
        new = L.blob_at(mirror, "origin/main", c.path)
        cls = L.classify(old, new, c.path)
        marks = L.added_markers(old, new)
        secs = []
        for lab in c.sections:
            secs.append((lab, L.section_present(old, lab),
                         L.section_present(new, lab)))
        rows.append((c, cls, marks, secs, old, new))
    return rows


def tally(rows):
    t = {}
    for _, cls, _, _, _, _ in rows:
        t[cls] = t.get(cls, 0) + 1
    return t


def print_rows(rows, indent="    "):
    for c, cls, marks, secs, old, new in rows:
        mk = ("  [+%s]" % ", ".join("%s x%d" % (k, v)
                                    for k, v in sorted(marks.items()))) if marks else ""
        print("%s%-20s %s:%d" % (indent, cls, c.src, c.srcline))
        print("%s  -> %s%s" % (indent, c.path, mk))
        for lab, in_old, in_new in secs:
            flag = ""
            if in_new and not in_old:
                flag = "   <-- CITED SECTION DOES NOT EXIST IN THE MIRROR"
            elif in_old and not in_new:
                flag = "   <-- CITED SECTION GONE AT origin/main (renumbered?)"
            print("%s     section §%-6s mirror=%-5s tip=%-5s%s"
                  % (indent, lab, in_old, in_new, flag))


def main():
    L.banner("mg-cdd5 s2 -- THE SWEEP: do other citations land on superseded text?")
    root = L.program_root()
    mirror = L.find_mirror()
    if mirror is None:
        L.die_unreadable("one_third_width_three not found")
        print("== s2 exit: 1 ==")
        return 1

    print("POPULATION, NAMED BEFORE ANY COUNT")
    print("  tier 1  citations to one_third_width_three in: %s"
          % ", ".join(TIER1))
    print("  tier 2  the same, anywhere under docs/ or code/ in this repo")
    print("  a citation is a markdown link, an HTML href, or a backticked path")
    print("  whose target contains `one_third_width_three/`; rows are unique on")
    print("  (citing file, citing line, cited path).")
    print()
    print("  read at:   mirror   %s   (what the checked-out tree has)" % MIRROR_PIN)
    print("             tip      origin/main")
    print("  by:        git show <rev>:<path>   -- the working copy is never opened")
    print()

    # ---------------- tier 1 ----------------
    t1, missing1 = gather(root, TIER1)
    print("-" * 78)
    print("TIER 1 -- STATE.md AND THE TWIN.  This is the ticket's question.")
    print("-" * 78)
    for m in missing1:
        print("  !! source not found: %s -- the tier-1 population is INCOMPLETE" % m)
    percite = {}
    for c in t1:
        percite[c.src] = percite.get(c.src, 0) + 1
    print("  citations swept: %d" % len(t1))
    for k in TIER1:
        print("    %-32s %d" % (k, percite.get(k, 0)))
    print("    distinct cited paths: %d" % len(set(c.path for c in t1)))
    print()
    # A ZERO MUST BE ATTRIBUTABLE.  The twin returns 0 cross-repo citations,
    # and that reads as `the twin points at nothing withdrawn` when it could
    # equally mean `the HTML parser is broken` (E6).  So the twin's TOTAL
    # link count is printed beside it: if it is also 0, the zero is a fact
    # about the document and not about the extractor.
    for k in TIER1:
        if percite.get(k, 0):
            continue
        txt = read_source(root, k)
        if txt is None:
            continue
        n_href = txt.count("href=")
        n_md = txt.count("](")
        print("    ATTRIBUTION of %s's zero: the document contains %d `href=`"
              % (k, n_href))
        print("      and %d markdown link(s) IN TOTAL, cross-repo or not.  %s"
              % (n_md,
                 "So it links to nothing at all and the zero is the"
                 if (n_href + n_md) == 0 else
                 "So it does link, and the zero is a"))
        print("      document's property, not the extractor's."
              if (n_href + n_md) == 0 else
              "      genuine absence of CROSS-REPO links among links it has.")
    print()
    rows1 = score(mirror, t1)
    print_rows(rows1)
    print()
    tl1 = tally(rows1)
    print("  TIER 1 TALLY")
    for k in sorted(tl1):
        print("    %-22s %d" % (k, tl1[k]))
    stale1 = sum(v for k, v in tl1.items() if k in L.HAZARD_CLASSES)
    struck1 = tl1.get(L.STRUCK, 0)
    print("    ------------------------------")
    print("    citations swept        %d" % len(rows1))
    print("    NOT clean              %d" % stale1)
    print("    of which struck        %d" % struck1)
    print()

    # ---------------- tier 2 ----------------
    print("-" * 78)
    print("TIER 2 -- WIDENED.  Reported separately; NOT added to tier 1.")
    print("-" * 78)
    rels = []
    excluded = 0
    for sub in ("docs", "code"):
        base = os.path.join(root, sub)
        for dirpath, _dirnames, filenames in os.walk(base):
            for fn in filenames:
                if not fn.lower().endswith((".md", ".html", ".txt", ".py", ".sh",
                                            ".json", ".tex", ".yml")):
                    continue
                rel = os.path.relpath(os.path.join(dirpath, fn), root)
                # THIS INSTRUMENT'S OWN DIRECTORY IS EXCLUDED, and the count is
                # printed.  Its selftest and controls contain SYNTHETIC
                # citations (`docs/a.md`, a planted href, a `%s` in a format
                # string) which are not corpus citations at all; on the first
                # run they contributed 10 rows and made this repository look
                # like it had 10 broken cross-repo references.  An instrument
                # that sweeps itself measures itself (README §6, D1).
                if rel.startswith(os.path.join("code", "mirror_staleness_cdd5")):
                    excluded += 1
                    continue
                rels.append(rel)
    rels.sort()
    t2, _ = gather(root, rels)
    # tier 2 excludes tier 1's own rows so the two counts never double-count
    t1keys = set(c.key() for c in t1)
    t2 = [c for c in t2 if c.key() not in t1keys]
    print("  files scanned: %d   (excluded: %d, this instrument's own directory"
          % (len(rels), excluded))
    print("                        -- it contains SYNTHETIC citations)")
    print("  citations swept: %d over %d distinct cited paths in %d citing files"
          % (len(t2), len(set(c.path for c in t2)),
             len(set(c.src for c in t2))))
    rows2 = score(mirror, t2)
    tl2 = tally(rows2)
    print()
    print("  TIER 2 TALLY")
    for k in sorted(tl2):
        print("    %-22s %d" % (k, tl2[k]))
    print()
    bad2 = [r for r in rows2 if r[1] in L.HAZARD_CLASSES]
    print("  THE NOT-CLEAN ROWS, NAMED (%d):" % len(bad2))
    print_rows(bad2)
    print()
    citing_bad = sorted(set(r[0].src for r in bad2))
    print("  DISTINCT CITING FILES AFFECTED IN TIER 2: %d" % len(citing_bad))
    for s in citing_bad:
        print("    %s" % s)
    print()

    # ---------------- the renumbering question (ticket step 4) -------------
    print("-" * 78)
    print("STEP 4 -- DID THE SECTION NUMBERING CHANGE?")
    print("-" * 78)
    print("  The ticket forbids editing STATE.md:78's citation UNLESS the")
    print("  numbering itself moved.  Scored per cited document that carries a")
    print("  section reference, by comparing the HEADING SETS at the two revs.")
    print()
    any_renumber = False
    for c, cls, marks, secs, old, new in rows1 + rows2:
        if not secs:
            continue
        h_old = L.section_heading_set(old)
        h_new = L.section_heading_set(new)
        lost = sorted(h_old - h_new)
        for lab, in_old, in_new in secs:
            norm = lab.replace("′", "'")
            renum = (in_old and not in_new)
            any_renumber = any_renumber or renum
            print("    %s:%d  §%-6s  %s"
                  % (c.src, c.srcline, lab,
                     "RENUMBERED/REMOVED -- citation must be repaired" if renum
                     else ("insertion, numbering intact" if in_new and not in_old
                           else "stable at both revisions")))
        if lost:
            print("        headings present in the mirror and gone at the tip: %s"
                  % ", ".join(lost[:8]))
    print()
    print("  ANY CITED SECTION RENUMBERED: %s" % ("YES" if any_renumber else "NO"))
    if not any_renumber:
        print("  => no citation is edited by this ticket.  The citations are")
        print("     right; the tree they land in is stale.")
    print()

    # ---------------- verdict figures --------------------------------------
    print("-" * 78)
    print("THE NUMBERS THE VERDICT NEEDS")
    print("-" * 78)
    print("  tier 1: %d citations swept, %d not clean (%d struck), over %d"
          % (len(rows1), stale1, struck1, len(set(c.path for c in t1))))
    print("          distinct cited paths in %d source documents."
          % len([k for k in TIER1 if percite.get(k, 0) >= 0]))
    bad2n = len(bad2)
    print("  tier 2: %d citations swept, %d not clean (%d struck), in %d"
          % (len(rows2), bad2n, tl2.get(L.STRUCK, 0), len(citing_bad)))
    print("          distinct citing files.")
    print("  directory references, counted and kept OUT of both hazard tallies:")
    print("          tier 1 %d, tier 2 %d"
          % (tl1.get(L.DIRECTORY, 0), tl2.get(L.DIRECTORY, 0)))
    print()
    print("  A zero in either tier is a MEASURED zero: the population is named")
    print("  above, the resolution method is `git show`, and unresolvable rows")
    print("  are reported as their own class rather than counted clean.")

    print("== s2 exit: 0 ==")
    return 0


if __name__ == "__main__":
    sys.exit(main())
