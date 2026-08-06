"""B7 — AN ORPHANED FIGURE: the one published number that reproduces against nothing.

mg-ea0e publishes an A1 acceptance row in TWO places — its commit message and
code/state_restructure_ea0e/README.md — ending "Corpus total 245,161 -> 261,318".

Its own committed transcript, out_verify_relocation_ea0e.txt, which the README says
"re-derives everything", prints on the line it is computed on:

      corpus total, old: 276,707   new: 295,751   (+19,044)

Every OTHER figure in that acceptance row matches the transcript character for character.
This script establishes three things, in order, and refuses to stop at the first:

  1. that the two pairs really do differ (parse both artifacts, do not retype them);
  2. that the difference is not arithmetic — it is a POPULATION difference;
  3. WHICH file the published pair is missing, by finding the file whose before-size is
     exactly the old gap and whose after-size is exactly the new gap.

A number that cannot be chased to a producing procedure is the defect this arc keeps
finding.  This one can be chased, and it lands somewhere specific.
"""

import re
import libb0ae as L

L.hdr("B7  THE ORPHANED CORPUS FIGURE — parsed from both artifacts, then chased")

readme = L.text(L.git_show(L.NEW_REV, "code/state_restructure_ea0e/README.md"))
trans = L.text(L.git_show(L.NEW_REV, "code/state_restructure_ea0e/out_verify_relocation_ea0e.txt"))
msg = L.sh(["git", "log", "-1", "--format=%B", L.NEW_REV]).decode()


def num(s):
    return int(s.replace(",", ""))


m_r = re.search(r"Corpus total `([\d,]+) → ([\d,]+)`", readme)
m_m = re.search(r"Corpus ([\d,]+) -> ([\d,]+)", msg)
m_t = re.search(r"corpus total, old: ([\d,]+)\s+new: ([\d,]+)", trans)

L.row("corpus pair in README.md", "%s -> %s" % (m_r.group(1), m_r.group(2)),
      "code/state_restructure_ea0e/README.md at %s, its A1 acceptance row" % L.NEW_REV,
      "utf-8 bytes, as published")
L.row("corpus pair in the COMMIT MESSAGE", "%s -> %s" % (m_m.group(1), m_m.group(2)),
      "the commit message of %s" % L.NEW_REV, "utf-8 bytes, as published")
L.row("corpus pair in ITS OWN TRANSCRIPT", "%s -> %s" % (m_t.group(1), m_t.group(2)),
      "code/state_restructure_ea0e/out_verify_relocation_ea0e.txt at %s" % L.NEW_REV,
      "utf-8 bytes, as printed by the instrument")

pub_old, pub_new = num(m_r.group(1)), num(m_r.group(2))
tr_old, tr_new = num(m_t.group(1)), num(m_t.group(2))
L.row("published == transcript", (pub_old, pub_new) == (tr_old, tr_new),
      "the two pairs above", "boolean")
L.row("gap on the OLD side", L.commas(tr_old - pub_old), "the two pairs above", "utf-8 bytes")
L.row("gap on the NEW side", L.commas(tr_new - pub_new), "the two pairs above", "utf-8 bytes")

L.note("Two different gaps rule out a typo and a units error.  A POPULATION difference — one\n"
       "file present in one total and absent from the other — predicts exactly this: the gap\n"
       "on each side equals that file's size on that side.  So look for such a file.")

L.hdr("B7.1  WHICH FILE IS MISSING FROM THE PUBLISHED PAIR")

rows = re.findall(r"^\s+(\S+\.md)\s+([\d,]+) -> \s*([\d,]+)", trans, re.M)
L.row("destination files listed in the transcript", len(rows),
      "the 'destination files, before -> after' block of the transcript", "file rows")

hit = [(p, num(a), num(b)) for p, a, b in rows
       if num(a) == tr_old - pub_old and num(b) == tr_new - pub_new]
L.row("files whose BOTH sizes equal BOTH gaps", len(hit),
      "the %d destination files above" % len(rows),
      "files — a unique hit identifies the population difference exactly")
for p, a, b in hit:
    print("      %s   %s -> %s" % (p, L.commas(a), L.commas(b)))
    L.row("  reproduces the published pair when removed",
          (tr_old - a, tr_new - b) == (pub_old, pub_new),
          "the transcript pair minus that file's two sizes", "boolean")

L.hdr("B7.2  WHAT IT MEANS, AND WHAT IT DOES NOT")
L.note("mg-ea0e's verifier builds its corpus total from the files whose size CHANGED.\n"
       "docs/state-history/README.md changed only because mg-ea0e itself edited it.  A run\n"
       "taken BEFORE that edit would find the file unchanged, exclude it from the block, and\n"
       "print exactly the published pair.  So the published figure is a REAL measurement of\n"
       "an EARLIER state of the same tree, carried into the final commit message and README\n"
       "beside nine figures that were re-derived at the end.")
L.row("other A1 figures that DO match the transcript",
      sum(1 for n in ("186,710", "32,772", "2,796", "29,976", "157,996", "+1,262")
          if n in readme and n.lstrip("+") in trans),
      "the six other numbers in mg-ea0e's A1 acceptance row",
      "figures appearing in both README.md and the transcript")
L.row("acceptance decisions that change", 0,
      "mg-ea0e's six acceptance checks A1-A5, C0",
      "checks — the corpus row feeds only 'the corpus as a whole did not shrink', which "
      "passes under BOTH pairs (261,318 > 245,161 and 295,751 > 276,707)")

print("\nB7 DONE")
