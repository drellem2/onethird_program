"""B3 — THE MARKERS.  Counting is not matching, and increases are not safety.

mg-ea0e's A5 row reports every marker count RISING: STRUCK 8->13, RETRACTED 0->2,
RETIRED 2->3, CORRECTED 5->7, SUPERSEDED 1->1, REFUTED 6->10, DISCHARGED 5->7,
BROKEN 43->71, withdrawn 4->4, void 5->9, and concludes 0 LOST.

TWO SEPARATE OBJECTIONS, MEASURED HERE:

  (1) POPULATION.  The "before" is one file.  The "after" is a corpus of thirteen files, ten
      of which EXISTED ALREADY and eight of which this commit never touched.  An increase
      under that comparison is what you get for free by widening the population; it would
      read exactly the same if the relocation had dropped markers.  So this script prints the
      counts over FOUR explicitly named populations and shows which one reproduces mg-ea0e's
      figures.

  (2) GRAIN.  43 BROKEN -> 71 BROKEN is arithmetically consistent with all 43 originals being
      deleted and 71 unrelated ones appearing.  A count cannot distinguish those.  So every
      marker OCCURRENCE in the old file is matched individually, by the text around it, and
      the match is shown failing when that text is disturbed.
"""

import libb0ae as L

L.hdr("B3  MARKERS — over four named populations, then at occurrence grain")

old_t = L.text(L.git_show(L.OLD_REV, "STATE.md"))
new_t = L.text(L.git_show(L.NEW_REV, "STATE.md"))
links = L.linked_files(new_t, L.NEW_REV)

added_per_file = {p: "\n".join(L.diff_added_lines(L.OLD_REV, L.NEW_REV, p)) for p in links}
pre_per_file = {}
for p in links:
    try:
        pre_per_file[p] = L.text(L.git_show(L.OLD_REV, p))
    except Exception:
        pre_per_file[p] = ""

P_OLD = old_t
P_NEW_ONLY = new_t
P_LIKE = new_t + "\n" + "\n".join(added_per_file[p] for p in links)
P_CORPUS = new_t + "\n" + "\n".join(L.text(L.git_show(L.NEW_REV, p)) for p in links)

# POPULATION 5 -- the TRANSITIVE closure of markdown links, computed here because the
# one-hop populations above fail to reproduce three of mg-ea0e's ten rows and a difference
# is a reason to look, not a finding.
closure, hops = L.link_closure(new_t, L.NEW_REV)
P_CLOSURE = new_t + "\n" + "\n".join(L.text(L.git_show(L.NEW_REV, p)) for p in sorted(closure))

untouched = [p for p in links if not added_per_file[p]]

L.note("POPULATION 1  old STATE.md alone .................. 1 file, %s B" % L.commas(len(P_OLD.encode())))
L.note("POPULATION 2  new STATE.md alone .................. 1 file, %s B" % L.commas(len(P_NEW_ONLY.encode())))
L.note("POPULATION 3  new STATE.md + ONLY text this commit added to linked files\n"
       "              ................................... %d files, %s B  <-- LIKE-FOR-LIKE"
       % (1 + len(links), L.commas(len(P_LIKE.encode()))))
L.note("POPULATION 4  new STATE.md + linked files ENTIRE at %s\n"
       "              ................................... %d files, %s B  <-- WIDER THAN 1"
       % (L.NEW_REV, 1 + len(links), L.commas(len(P_CORPUS.encode()))))
L.row("linked files this commit did NOT touch", len(untouched),
      "the %d files new STATE.md links to" % len(links),
      "files with 0 added lines in %s — their markers are free additions to POPULATION 4" % L.NEW_REV)
for p in untouched:
    print("      %s" % p)

PARENT = {"STRUCK": (8, 13), "RETRACTED": (0, 2), "RETIRED": (2, 3), "CORRECTED": (5, 7),
          "SUPERSEDED": (1, 1), "REFUTED": (6, 10), "DISCHARGED": (5, 7), "BROKEN": (43, 71),
          "withdrawn": (4, 4), "void": (5, 9)}

L.note("POPULATION 5  new STATE.md + the TRANSITIVE link closure ............ %d files, %s B"
       % (1 + len(closure), L.commas(len(P_CLOSURE.encode()))))
L.row("files by LINK DISTANCE from new STATE.md", str(sorted({h: sum(1 for v in hops.values() if v == h)
                                                             for h in set(hops.values())}.items())),
      "the %d files in the transitive closure" % len(closure),
      "(hops, files) — hop 1 is 'one link away'; hop >= 2 is not")
for p in sorted(hops, key=lambda x: (hops[x], x)):
    print("      hop %d  %s" % (hops[p], p))

L.hdr("B3.1  COUNTS — the same ten markers over each population")
print("  %-12s %7s %7s %7s %7s %7s   | %-16s"
      % ("marker", "P1 old", "P2 new", "P3 like", "P4 1hop", "P5 clos", "mg-ea0e says"))
print("  " + "-" * 84)
p3_ge = p4_matches = p3_matches = p5_matches = 0
for m in L.MARKERS:
    c1, c2, c3, c4 = P_OLD.count(m), P_NEW_ONLY.count(m), P_LIKE.count(m), P_CORPUS.count(m)
    c5 = P_CLOSURE.count(m)
    po, pn = PARENT[m]
    flag = []
    if (c1, c4) == (po, pn):
        p4_matches += 1
        flag.append("P4=parent")
    if (c1, c3) == (po, pn):
        p3_matches += 1
        flag.append("P3=parent")
    if (c1, c5) == (po, pn):
        p5_matches += 1
        flag.append("P5=parent")
    if c3 >= c1:
        p3_ge += 1
    print("  %-12s %7d %7d %7d %7d %7d   | %d->%-6d %s" % (m, c1, c2, c3, c4, c5, po, pn, " ".join(flag)))

L.row("markers whose parent pair == POPULATION 5", p5_matches,
      "the 10 markers mg-ea0e reports",
      "markers — identifies WHICH population its published figures are over")
L.row("markers whose parent pair == POPULATION 4", p4_matches,
      "the 10 markers mg-ea0e reports", "markers, one-hop corpus")
L.row("markers whose parent pair == POPULATION 3", p3_matches,
      "the 10 markers mg-ea0e reports", "markers, like-for-like population")
L.row("markers not falling under like-for-like", 10 - p3_ge,
      "the 10 markers mg-ea0e reports",
      "markers whose POPULATION-3 count is BELOW its POPULATION-1 count")

L.hdr("B3.1b  WHERE THE INCREASES COME FROM — per file, per marker")
print("  %-44s %5s  %s" % ("file", "hop", "markers it contributes"))
for p in sorted(hops, key=lambda x: (hops[x], x)):
    body = L.text(L.git_show(L.NEW_REV, p))
    contrib = {m: body.count(m) for m in L.MARKERS if body.count(m)}
    add_only = {m: added_per_file.get(p, "").count(m) for m in L.MARKERS
                if added_per_file.get(p, "").count(m)}
    print("  %-44s %5d  %s" % (p.replace("docs/", ""), hops[p], contrib or "-"))
    if contrib and contrib != add_only:
        print("  %-44s %5s    of which arrived in THIS commit: %s"
              % ("", "", add_only or "NONE — every one of these pre-dates mg-ea0e"))

L.note("Read the P2 column, not the P4 column, to see what the SUMMARY now carries: that is\n"
       "the file a reader opens.  P4 rises partly because eight linked files were never\n"
       "touched by this commit and bring their own markers with them.")

# ---------------------------------------------------------------------------
# occurrence grain
# ---------------------------------------------------------------------------
L.hdr("B3.2  OCCURRENCE GRAIN — each marker matched by its own surrounding text")

atoms = L.atomise(old_t, "old")
WINDOW = 60
occ = []
for a in atoms:
    for m in L.MARKERS:
        start = 0
        while True:
            i = a["text"].find(m, start)
            if i < 0:
                break
            lo = max(0, i - WINDOW)
            hi = min(len(a["text"]), i + len(m) + WINDOW)
            occ.append(dict(marker=m, lineno=a["lineno"], ctx=a["text"][lo:hi], atom=a["text"]))
            start = i + 1

POPO = ("every occurrence of the 10 markers inside the %d atoms of old STATE.md" % len(atoms))
L.row("marker occurrences in old STATE.md", len(occ), POPO,
      "one occurrence = one (marker, position) pair, case-sensitive")

def found(s):
    return (s in P_NEW_ONLY) or any(s in added_per_file[p] for p in links)

lost = [o for o in occ if not found(o["ctx"])]
L.row("occurrences whose +/-%d-char context survives" % WINDOW, len(occ) - len(lost), POPO,
      "occurrences matched in new STATE.md or in text THIS COMMIT ADDED (POPULATION 3)")
L.row("occurrences LOST", len(lost), POPO, "occurrences with no surviving context")
for o in lost[:25]:
    print("      old:%d %-11s %r" % (o["lineno"], o["marker"], o["ctx"][:120]))

lost_wide = [o for o in occ if not (o["ctx"] in P_CORPUS)]
L.row("occurrences LOST against POPULATION 4", len(lost_wide), POPO,
      "occurrences — printed so the two populations can be compared on the SAME grain")

def corrupt(s):
    i = len(s) // 2
    return s[:i] + ("Z" if s[i] != "Z" else "Q") + s[i + 1:]

ctrl = sum(1 for o in occ if not found(corrupt(o["ctx"])))
L.row("CONTROL occurrences lost after 1-char corruption", ctrl, POPO,
      "occurrences — MUST be ~= the population, else context matching proves nothing")

# per-marker occurrence survival, so a single marker cannot hide inside a total
print()
print("  %-12s %9s %9s" % ("marker", "occ old", "lost"))
for m in L.MARKERS:
    n = sum(1 for o in occ if o["marker"] == m)
    nl = sum(1 for o in lost if o["marker"] == m)
    print("  %-12s %9d %9d" % (m, n, nl))

L.hdr("B3.3  DID THE SUMMARY KEEP ITS CORRECTIONS?  Markers in new STATE.md by provenance")
new_atoms = L.atomise(new_t, "new")
kept = 0
composed = 0
for a in new_atoms:
    for m in L.MARKERS:
        c = a["text"].count(m)
        if c:
            if a["text"] in old_t:
                kept += c
            else:
                composed += c
L.row("marker occurrences in new STATE.md carried verbatim", kept,
      "the %d atoms of new STATE.md" % len(new_atoms),
      "occurrences inside an atom that appears verbatim in old STATE.md")
L.row("marker occurrences in new STATE.md inside REWRITTEN atoms", composed,
      "the %d atoms of new STATE.md" % len(new_atoms),
      "occurrences inside an atom with no verbatim antecedent — each needs reading by hand")

print("\nB3 DONE")
