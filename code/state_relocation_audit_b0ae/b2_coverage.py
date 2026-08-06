"""B2 — DID ANY TEXT ACTUALLY DIE?  Atom-grain coverage, with attribution and controls.

B1 showed the byte totals are of the right size.  A total of the right size is not survival:
187,972 >= 186,710 is equally consistent with 10,000 bytes lost against 11,262 duplicated.
This script answers survival directly and at the grain where the relocation actually worked —
the TABLE CELL, because mg-ea0e rewrote the third column of seven rows and left the first two
alone, so a line-grain verdict on those rows can only say "changed".

THREE THINGS THIS DOES THAT A PLAIN PRESENCE CHECK DOES NOT:

  1. ATTRIBUTION.  Every surviving atom is charged to exactly one of: still in STATE.md /
     arrived in a linked file IN THIS COMMIT / matched only by text that was ALREADY in a
     linked file at 78ae4d9.  The third bucket is the one that can disguise a loss, because
     mg-34bf built the seven destination files out of these same rows months earlier.

  2. A NEGATIVE CONTROL THAT COULD HAVE SHOWN THE POSITIVE.  A coverage checker that reports
     0 missing is worthless unless it is shown reporting a positive number when content IS
     absent.  Two controls run here: withhold the largest destination file, and corrupt every
     atom by one character.  Both must go red.

  3. A RE-DERIVED SUBSTRING GUARD.  `atom in haystack` is a weak test: a short atom such as
     "---" or a status label can be satisfied by an unrelated coincidence.  Atoms shorter
     than 24 characters are therefore counted SEPARATELY and their coincidence rate measured
     against a haystack they are NOT supposed to be in.
"""

import libb0ae as L

L.hdr("B2  COVERAGE AT ATOM GRAIN — every cell and every line of old STATE.md")

old_t = L.text(L.git_show(L.OLD_REV, "STATE.md"))
new_t = L.text(L.git_show(L.NEW_REV, "STATE.md"))
links = L.linked_files(new_t, L.NEW_REV)

atoms = L.atomise(old_t, "STATE.md@%s" % L.OLD_REV)
n_line = sum(1 for a in atoms if a["kind"] == "line")
n_cell = sum(1 for a in atoms if a["kind"] == "cell")
POP = "the %d atoms of old STATE.md (%d whole lines + %d table cells)" % (len(atoms), n_line, n_cell)

L.row("atoms in old STATE.md", len(atoms), POP, "one atom = one table cell, or one non-table line")
L.row("  of which table cells", n_cell, POP, "cells, after splitting rows on '|'")
L.row("  of which whole lines", n_line, POP, "non-blank non-table lines, stripped")

# column-count sanity: a row with an unexpected column count means '|' split is unsafe
rows_cols = {}
for a in atoms:
    if a["kind"] == "cell":
        rows_cols[a["lineno"]] = rows_cols.get(a["lineno"], 0) + 1
dist = {}
for v in rows_cols.values():
    dist[v] = dist.get(v, 0) + 1
L.row("table rows by cell count", str(sorted(dist.items())),
      "the %d table rows of old STATE.md" % len(rows_cols),
      "(cells-in-row, number-of-rows) — a stray '|' inside a cell would show here")

# ---------------------------------------------------------------------------
# the three haystacks
# ---------------------------------------------------------------------------
H_state = new_t
added_per_file = {p: "\n".join(L.diff_added_lines(L.OLD_REV, L.NEW_REV, p)) for p in links}
H_added = "\n".join(added_per_file[p] for p in links)
pre_per_file = {}
for p in links:
    try:
        pre_per_file[p] = L.text(L.git_show(L.OLD_REV, p))
    except Exception:
        pre_per_file[p] = ""
H_pre = "\n".join(pre_per_file[p] for p in links)

L.row("linked files forming the corpus", len(links),
      "markdown link targets in new STATE.md that are tracked paths", "files")
L.row("bytes of ADDED text in linked files", L.commas(len(H_added.encode())),
      "the %d linked files" % len(links), "utf-8 bytes of lines this commit added")
L.row("bytes of PRE-EXISTING text in linked files", L.commas(len(H_pre.encode())),
      "the %d linked files" % len(links), "utf-8 bytes of those files at %s" % L.OLD_REV)


def classify(atom_text):
    if atom_text in H_state:
        return "in-place"
    if atom_text in H_added:
        return "arrived"
    if atom_text in H_pre:
        return "pre-existing-only"
    return "MISSING"


L.hdr("B2.1  VERDICT — where each atom of old STATE.md is now")

buckets = {"in-place": [], "arrived": [], "pre-existing-only": [], "MISSING": []}
for a in atoms:
    buckets[classify(a["text"])].append(a)

for k in ("in-place", "arrived", "pre-existing-only", "MISSING"):
    L.row(k, len(buckets[k]), POP, "atoms, exact-substring presence")

if buckets["MISSING"]:
    print("\n  MISSING ATOMS — each is a lost record:")
    for a in buckets["MISSING"]:
        print("      old:%d %s col=%s  %r" % (a["lineno"], a["kind"], a["col"], a["text"][:160]))
else:
    L.note("0 MISSING.  That verdict is only worth the controls below.")

if buckets["pre-existing-only"]:
    print("\n  ATOMS MATCHED ONLY BY TEXT THIS COMMIT DID NOT WRITE:")
    for a in buckets["pre-existing-only"][:40]:
        holder = [p for p in links if a["text"] in pre_per_file[p]]
        print("      old:%d %s  in %s  %r"
              % (a["lineno"], a["kind"], ",".join(holder)[:60], a["text"][:110]))
    L.row("atoms whose ONLY witness pre-existed", len(buckets["pre-existing-only"]), POP,
          "atoms present in a linked file at %s and absent from this commit's additions" % L.OLD_REV)

# ---------------------------------------------------------------------------
# short atoms: how much of the pass is coincidence?
# ---------------------------------------------------------------------------
L.hdr("B2.2  IS THE PASS COINCIDENCE?  Short atoms measured separately")

SHORT = 24
short = [a for a in atoms if len(a["text"]) < SHORT]
longa = [a for a in atoms if len(a["text"]) >= SHORT]
L.row("atoms shorter than %d chars" % SHORT, len(short), POP, "atoms, by character length")
L.row("atoms >= %d chars" % SHORT, len(longa), POP, "atoms, by character length")
L.row("long atoms MISSING", sum(1 for a in longa if classify(a["text"]) == "MISSING"),
      "the %d atoms of old STATE.md at least %d characters long" % (len(longa), SHORT),
      "atoms, exact-substring presence")

# coincidence rate: a haystack the atoms are NOT supposed to be in
foreign = L.text(L.git_show(L.NEW_REV, "code/state_restructure_ea0e/build.py"))
co_short = sum(1 for a in short if a["text"] in foreign)
co_long = sum(1 for a in longa if a["text"] in foreign)
L.row("short atoms found in an UNRELATED file", co_short,
      "the %d short atoms, searched in code/state_restructure_ea0e/build.py" % len(short),
      "atoms — this is the coincidence rate of the `in` test at short grain")
L.row("long atoms found in an UNRELATED file", co_long,
      "the %d long atoms, same foreign haystack" % len(longa), "atoms")

# ---------------------------------------------------------------------------
# controls
# ---------------------------------------------------------------------------
L.hdr("B2.3  NEGATIVE CONTROLS — the instrument shown reporting a positive")

biggest = max(links, key=lambda p: len(L.git_show(L.NEW_REV, p)))
H_added_wo = "\n".join(added_per_file[p] for p in links if p != biggest)
H_pre_wo = "\n".join(pre_per_file[p] for p in links if p != biggest)
missing_wo = sum(1 for a in atoms
                 if a["text"] not in H_state and a["text"] not in H_added_wo
                 and a["text"] not in H_pre_wo)
L.row("CONTROL 1 missing with %s withheld" % biggest.split("/")[-1], missing_wo, POP,
      "atoms — MUST be > 0, else the checker cannot see an absence")

def corrupt(s):
    if len(s) < 8:
        return s + "ÿÿ"
    i = len(s) // 2
    return s[:i] + ("Z" if s[i] != "Z" else "Q") + s[i + 1:]

missing_corrupt = sum(1 for a in atoms if classify(corrupt(a["text"])) == "MISSING")
L.row("CONTROL 2 missing after 1-char corruption", missing_corrupt, POP,
      "atoms, each mutated at its midpoint — MUST be ~= the population size")
L.row("CONTROL 2 survivors (false passes)", len(atoms) - missing_corrupt, POP,
      "corrupted atoms still 'found' — each is a place the test is too loose")

selfcheck = sum(1 for a in atoms if a["text"] not in old_t)
L.row("CONTROL 3 old atoms absent from old file", selfcheck, POP,
      "atoms — MUST be 0, else atomisation itself invents text")

# ---------------------------------------------------------------------------
# the seven relocated rows, column by column, charged to added text ONLY
# ---------------------------------------------------------------------------
L.hdr("B2.4  THE SEVEN RELOCATED ROWS — every column, against ADDED text only")

MOVED = [130, 131, 132, 133, 134, 135, 136]
strict_missing = []
for ln in MOVED:
    cells = [a for a in atoms if a["lineno"] == ln]
    ids = L.MG_ID_RE.findall(cells[0]["text"]) if cells else []
    dest = "docs/state-history/attempt-%s.md" % ids[0] if ids else "?"
    for a in cells:
        add_only = a["text"] in added_per_file.get(dest, "")
        anywhere_added = a["text"] in H_added
        in_state = a["text"] in H_state
        if not (add_only or anywhere_added):
            strict_missing.append((ln, a["col"]))
        print("      :%d col%d %6d chars  in-its-own-dest=%-5s  in-any-added=%-5s  in-STATE=%-5s"
              % (ln, a["col"], len(a["text"]), add_only, anywhere_added, in_state))

L.row("moved columns not in this commit's additions", len(strict_missing),
      "the %d columns of the 7 relocated ledger rows" % sum(1 for a in atoms if a["lineno"] in MOVED),
      "columns, exact-substring presence in ADDED text only")

print("\nB2 DONE")
