"""B1 — RE-DERIVE THE BYTE ACCOUNTING, and attack the +1,262 surplus.

mg-ea0e's A1 row says: 29,976 bytes of old text still in place + 157,996 bytes of old text
found verbatim in linked files = 187,972 against an original 186,710, surplus +1,262,
"explained" as each relocated row's retained sentence sitting in BOTH places.

TWO THINGS ARE WRONG WITH ACCEPTING THAT AS STATED, and this script measures both:

  (a) A SURPLUS IS NOT A PROOF OF SURVIVAL.  187,972 >= 186,710 is also consistent with
      10,000 bytes lost and 11,262 bytes duplicated.  Byte totals that balance are not the
      same as content that survived.  So the surplus is decomposed here into the bytes that
      are genuinely double-counted, and B2 answers survival at atom grain independently.

  (b) THE SEVEN DESTINATION FILES PRE-EXISTED THE COMMIT (mg-34bf built them, and mg-ea0e's
      own appended header says so).  A search for old STATE.md text "in linked files" run at
      HEAD is satisfied by text that was ALREADY THERE and never moved.  So the credit is
      split three ways here: in-place, arrived-in-this-commit, and already-present.
"""

import libb0ae as L

L.hdr("B1  BYTE ACCOUNTING, RE-DERIVED (not checked against mg-ea0e's arithmetic)")

old_b = L.git_show(L.OLD_REV, "STATE.md")
new_b = L.git_show(L.NEW_REV, "STATE.md")
old_t, new_t = L.text(old_b), L.text(new_b)

L.note("audited object: %s (mg-ea0e); its parent: %s" % (L.rev_parse(L.NEW_REV)[:7],
                                                         L.rev_parse(L.OLD_REV)[:7]))

L.row("old STATE.md size", L.commas(len(old_b)),
      "the single file STATE.md at %s" % L.OLD_REV, "bytes (utf-8, as stored)")
L.row("new STATE.md size", L.commas(len(new_b)),
      "the single file STATE.md at %s" % L.NEW_REV, "bytes (utf-8, as stored)")
L.row("reduction", "%.1f%%" % (100.0 * (1 - len(new_b) / len(old_b))),
      "the two files above", "percent of old bytes")

# ---------------------------------------------------------------------------
# word and line counts -- two instruments, both printed, because mg-ea0e's
# published figures reproduce under NEITHER of the obvious ones exactly.
# ---------------------------------------------------------------------------
L.hdr("B1.1  SHAPE — every count under TWO instruments, because the parent's do not agree")

for name, t in (("old", old_t), ("new", new_t)):
    ws = len(t.split())
    L.row("%s words, whitespace-split" % name, L.commas(ws),
          "STATE.md at %s" % (L.OLD_REV if name == "old" else L.NEW_REV),
          "maximal runs of non-whitespace (== `wc -w`)")
    L.row("%s lines, wc -l grain" % name, L.commas(t.count("\n")),
          "same file", "newline characters (== `wc -l`)")
    L.row("%s lines, split grain" % name, L.commas(len(t.split("\n"))),
          "same file", "elements of text.split('\\n') (one MORE on a newline-terminated file)")

longest = max(new_t.split("\n"), key=len)
L.row("new longest line", L.commas(len(longest)),
      "the %d lines of new STATE.md" % len(new_t.split("\n")), "characters (not bytes)")
L.row("new longest line, bytes", L.commas(len(longest.encode())),
      "the same single line", "utf-8 bytes — DIFFERENT from the character count above")
L.row("  at line", new_t.split("\n").index(longest) + 1,
      "same", "1-based line number, split grain")

old_longest = max(old_t.split("\n"), key=len)
L.row("old longest line", L.commas(len(old_longest)),
      "the %d lines of old STATE.md" % len(old_t.split("\n")), "characters (not bytes)")
L.row("old longest line, bytes", L.commas(len(old_longest.encode())),
      "the same single line", "utf-8 bytes — the brief's '13,601 -> 1,772' is this figure "
      "against the NEW file's CHARACTER count, one grain each side")
L.row("  at line", old_t.split("\n").index(old_longest) + 1, "same", "1-based line number")

# ---------------------------------------------------------------------------
# the corpus, derived from the file
# ---------------------------------------------------------------------------
L.hdr("B1.2  THE REACHABLE CORPUS, parsed out of new STATE.md")

links = L.linked_files(new_t, L.NEW_REV)
L.row("distinct tracked files linked", len(links),
      "every markdown link target in new STATE.md that is a tracked path at %s" % L.NEW_REV,
      "distinct repo-relative file paths")
for p in links:
    at_new = L.git_show(L.NEW_REV, p)
    try:
        at_old = L.git_show(L.OLD_REV, p)
        existed = "PRE-EXISTED"
    except Exception:
        at_old = b""
        existed = "created here"
    print("      %-52s %9s B  (%9s B at %s, %s)"
          % (p, L.commas(len(at_new)), L.commas(len(at_old)), L.OLD_REV, existed))

# ---------------------------------------------------------------------------
# in-place / arrived / pre-existing, at LINE grain over the old file
# ---------------------------------------------------------------------------
L.hdr("B1.3  WHERE EACH OLD LINE'S BYTES ARE NOW — three-way split")

old_lines = [l for l in old_t.split("\n") if l.strip()]
new_line_set = set(l for l in new_t.split("\n"))

added_by_commit = {}
pre_existing = {}
for p in links:
    added_by_commit[p] = set(L.diff_added_lines(L.OLD_REV, L.NEW_REV, p))
    try:
        pre_existing[p] = set(L.text(L.git_show(L.OLD_REV, p)).split("\n"))
    except Exception:
        pre_existing[p] = set()

all_added = set().union(*added_by_commit.values()) if added_by_commit else set()
all_pre = set().union(*pre_existing.values()) if pre_existing else set()

b_inplace = b_arrived = b_pre_only = b_nowhere = 0
n_inplace = n_arrived = n_pre_only = n_nowhere = 0
nowhere_lines = []
for l in old_lines:
    nb = len(l.encode())
    if l in new_line_set:
        b_inplace += nb; n_inplace += 1
    elif l in all_added:
        b_arrived += nb; n_arrived += 1
    elif l in all_pre:
        b_pre_only += nb; n_pre_only += 1
    else:
        b_nowhere += nb; n_nowhere += 1
        nowhere_lines.append(l)

pop_lines = "the %d non-blank lines of old STATE.md" % len(old_lines)
L.row("old lines still in new STATE.md", n_inplace, pop_lines, "whole lines, exact string")
L.row("  their bytes", L.commas(b_inplace), pop_lines, "utf-8 bytes, newline excluded")
L.row("old lines ADDED to a linked file here", n_arrived, pop_lines, "whole lines, exact string")
L.row("  their bytes", L.commas(b_arrived), pop_lines, "utf-8 bytes, newline excluded")
L.row("old lines matched ONLY by PRE-EXISTING text", n_pre_only, pop_lines,
      "whole lines, exact string")
L.row("  their bytes", L.commas(b_pre_only), pop_lines, "utf-8 bytes, newline excluded")
L.row("old lines matched NOWHERE at line grain", n_nowhere, pop_lines,
      "whole lines, exact string")
L.row("  their bytes", L.commas(b_nowhere), pop_lines, "utf-8 bytes, newline excluded")

L.note("A line-grain miss is NOT yet a loss: mg-ea0e rewrote the THIRD COLUMN of seven table\n"
       "rows, so those seven lines cannot match as whole lines by construction.  B2 resolves\n"
       "these at CELL grain.  The lines that miss here are listed by line number:")
old_all = old_t.split("\n")
miss_no = [old_all.index(l) + 1 for l in nowhere_lines]
print("      old line numbers missing at LINE grain: %s" % (sorted(set(miss_no)) or "none"))

L.row("bytes credited to PRE-EXISTING text", L.commas(b_pre_only), pop_lines,
      "utf-8 bytes of old STATE.md lines whose only match is text present at %s" % L.OLD_REV)
L.note("P3 in PREDICTIONS.md: a NON-ZERO figure here is the mechanism by which a byte total\n"
       "can balance while content is lost — the corpus at HEAD contains matching text that\n"
       "this commit did not put there.")

# ---------------------------------------------------------------------------
# the surplus, decomposed
# ---------------------------------------------------------------------------
L.hdr("B1.4  THE +1,262 SURPLUS — decomposed rather than accepted")

n_both = 0
b_both = 0
both_examples = []
for l in old_lines:
    if l in new_line_set and (l in all_added or l in all_pre):
        n_both += 1
        b_both += len(l.encode())
        both_examples.append(l)

L.row("old lines present in BOTH places", n_both, pop_lines,
      "whole lines found in new STATE.md AND in a linked file")
L.row("  their bytes (double-counted)", L.commas(b_both), pop_lines, "utf-8 bytes")

L.note("mg-ea0e's own surplus is +1,262 by ITS definition of the two addends.  Mine is\n"
       "computed over a different, stated decomposition, so the two are not required to\n"
       "agree; what matters is whether the double-counting mg-ea0e names as the cause is\n"
       "LARGE ENOUGH to be the cause.  The seven relocated rows retain an OPENING SENTENCE\n"
       "that also appears in the destination file.  Those sentences are measured next.")

# the seven relocated rows: which retained sentence sits in both places
MOVED_ROWS = [130, 131, 132, 133, 134, 135, 136]
retained_bytes = 0
print()
for ln in MOVED_ROWS:
    new_line = new_t.split("\n")[ln - 1]
    cells = new_line.strip().strip("|").split("|")
    result_cell = cells[2].strip() if len(cells) >= 3 else ""
    # the retained sentence is the part before the link boilerplate
    cut = result_cell.find("**Full record")
    retained = result_cell[:cut].strip() if cut > 0 else result_cell
    # does that exact sentence also appear in the destination file's ADDED text?
    in_dest = any(retained and retained in "\n".join(added_by_commit[p]) for p in links)
    retained_bytes += len(retained.encode()) if in_dest else 0
    print("      :%d  retained %5s B  also-in-destination=%-5s  %.70s"
          % (ln, L.commas(len(retained.encode())), in_dest, retained))

L.row("retained-sentence bytes in BOTH places", L.commas(retained_bytes),
      "the 7 ledger rows mg-ea0e relocated (:130-:136 of old STATE.md)",
      "utf-8 bytes of the result-column sentence the row kept AND the destination file carries")
L.row("mg-ea0e's stated surplus (ITS number)", "+1,262",
      "mg-ea0e's own two addends, quoted not re-derived", "utf-8 bytes")
L.row("shortfall of the stated explanation", L.commas(1262 - retained_bytes),
      "the difference of the two rows above", "utf-8 bytes left unexplained by retained sentences")

print("\nB1 DONE")
