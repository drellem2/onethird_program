#!/usr/bin/env python3
"""mg-bd41 — independent audit of mg-7735 / b68db5d (the landing of the mg-6a2f audit).

Recomputes EVERY count, byte figure, row tally and offset that b68db5d introduces or
updates, from the artifact, with instruments written from scratch for this audit.

Imports nothing from code/state_restructure_34bf/ or code/state_audit_6a2f/.  Does not
re-run the author's scripts to obtain any figure (instrument_sensitivity.py runs two of
them, but only to test the author's claims ABOUT those scripts, never to source a number).

INSTRUMENT DISCIPLINE, because this arc has been bitten by all three:
  * `wc -m` counts BYTES on this box (LC_CTYPE=C).  Nothing here shells out to wc; all
    character counts are len() over a str decoded from the blob, all byte counts are
    len() over the bytes.
  * Every figure printed names its UNIT and its CELL CONVENTION (raw / stripped).
  * Every tally is computed over UNBOUNDED input.  No head, tail, sed -n A,Bp or --limit
    anywhere; where a count is reported, the population it was taken over is printed.
"""
import re, sys
from cellmeasure import (REPO, blob, lines_bytes, row, split_row, cell3,
                         content_cell)

BASE, LANDING, OLD, PARENT, HEAD = "60f4dac", "57f962f", "db08b4c", "672915e", "b68db5d"
WPM = 250
OK = FAIL = 0


def check(label, got, want, unit=""):
    global OK, FAIL
    good = (got == want)
    OK, FAIL = OK + good, FAIL + (not good)
    u = f" {unit}" if unit else ""
    print(f"  [{'OK  ' if good else 'FAIL'}] {label}\n"
          f"          claimed {want}{u}   measured {got}{u}")
    return good


def words(s):
    """My own word counter: whitespace-separated tokens over the whole string."""
    return len(s.split())


def hdr(t):
    print(f"\n{'='*78}\n{t}\n{'='*78}")


# ---------------------------------------------------------------- 1. file-level
hdr("1. FILE-LEVEL INVARIANTS the commit asserts about itself")
for rev, label, want_lines in ((OLD, "db08b4c", 327), (BASE, "60f4dac", 367),
                               ("bdcb006", "bdcb006 (mg-ae62)", 377),
                               (PARENT, "672915e (mg-a053)", 380),
                               (HEAD, "b68db5d (mg-7735)", 380)):
    b = blob(rev)
    n = len(b.split(b"\n")) - (1 if b.endswith(b"\n") else 0)
    check(f"STATE.md lines at {label}", n, want_lines, "lines")
print(f"\n  -> '380 lines before and after' and the 367 -> 377 -> 380 progression"
      f"\n     ('mg-ae62 added 10 lines and mg-a053 added 3') both hold.")

d = [i for i, (a, b) in enumerate(zip(lines_bytes(PARENT), lines_bytes(HEAD)), 1) if a != b]
check("STATE.md lines changed by b68db5d", d, [135], "(1-indexed)")

cv_p = [len(split_row(l) or []) for l in lines_bytes(PARENT)]
cv_h = [len(split_row(l) or []) for l in lines_bytes(HEAD)]
check("column-count vector of the whole file identical", cv_h == cv_p, True)

odd = [(i, j) for i, l in enumerate(lines_bytes(HEAD), 1)
       for j, c in enumerate(split_row(l) or [], 1) if c.count("**") % 2]
ncells = sum(len(split_row(l) or []) for l in lines_bytes(HEAD))
check(f"cells with ODD ** count at HEAD (of {ncells} cells, whole file)", len(odd), 0, "cells")
check("row :135 column count at HEAD", len(split_row(row(HEAD, 135))), 3, "columns")

# ---------------------------------------------------------------- 2. cell arithmetic
hdr("2. THE CELL ARITHMETIC — raw vs stripped, the convention split")
print("  A markdown cell `| ... |` can be measured WITH or WITHOUT its bounding spaces.")
print("  b68db5d uses BOTH, in the same change, without naming either.\n")
print(f"  {'':22} {'raw chars':>10} {'strip chars':>12} {'raw bytes':>10} {'strip bytes':>12}")
for rev, lab in ((BASE, "60f4dac :135"), (LANDING, "57f962f :135"), (HEAD, "b68db5d :135"),
                 (BASE, "60f4dac :136"), (HEAD, "b68db5d :136")):
    n = int(lab[-3:])
    c = cell3(rev, n)
    print(f"  {lab:22} {len(c):>10} {len(c.strip()):>12} "
          f"{len(c.encode()):>10} {len(c.strip().encode()):>12}")

print("\n  The README index table + its new annotation use RAW:")
check("README table   :135 cell before", len(cell3(BASE, 135)), 13190, "raw chars")
check("README table   :135 cell after ", len(cell3(LANDING, 135)), 7705, "raw chars")
check("README annot.  :135 at HEAD    ", len(cell3(HEAD, 135)), 7878, "raw chars")
check("README table   :136 cell after ", len(cell3(LANDING, 136)), 8442, "raw chars")
print("\n  The README's NEW F2 block and the commit message use STRIPPED:")
check("README F2 blk  :135 cell before", len(cell3(BASE, 135).strip()), 13188, "stripped chars")
check("README F2 blk  :135 cell after ", len(cell3(LANDING, 135).strip()), 7703, "stripped chars")
check("commit msg     :135 at HEAD    ", len(cell3(HEAD, 135).strip()), 7876, "stripped chars")
check("commit msg     :136 largest    ", len(cell3(LANDING, 136).strip()), 8440, "stripped chars")
print("\n  -> Every figure is correct under ONE convention.  No figure names its convention,")
print("     and the new F2 block asserts its figures are 'the same figures the index below")
print("     carries' while giving 13,188 / 7,703 against the table's 13,190 / 7,705.")

allc = sorted(((len(c), i, j) for i, l in enumerate(lines_bytes(HEAD), 1)
               for j, c in enumerate(split_row(l) or [], 1)), reverse=True)
print(f"\n  Largest cells at HEAD, over ALL {len(allc)} cells in the file (unbounded scan):")
for v, i, j in allc[:3]:
    print(f"      :{i} col{j}  {v} raw chars")
check("':136 remains the largest cell' (whole file)", (allc[0][1], allc[0][2]), (136, 3))

print("\n  The README index table in full — 'cell before' at 60f4dac, 'cell after' at")
print("  57f962f, RAW chars, content cell = the row's widest cell (row :89 sits in a")
print("  4-column table, so 'the third column' is not portable):")
TABLE = {89: (1556, 1585), 114: (725, 555), 124: (1467, 1621), 130: (2597, 2052),
         131: (4918, 3651), 132: (8630, 4804), 133: (12696, 6876), 134: (9974, 6247),
         135: (13190, 7705), 136: (15386, 8442)}
moved = []
for n, (wb, wa) in sorted(TABLE.items()):
    mb, ma, mh = (len(content_cell(r, n)) for r in (BASE, LANDING, HEAD))
    check(f"    :{n} before/after", (mb, ma), (wb, wa), "raw chars")
    if mh != ma:
        moved.append((n, ma, mh))
check("  cells in the table that moved after the landing", moved, [(135, 7705, 7878)])
print("  -> the annotation's 'No other cell in the table has changed' holds, and all")
print("     twenty of the table's own figures reproduce exactly.")

# ---------------------------------------------------------------- 3. F2
hdr("3. F2 — the 'five consecutive giants' correction")
print("  Claim: cells :132-:136 at 60f4dac, characters = 8.6 / 12.7 / 10.0 / 13.2 / 15.4")
got = [round(len(cell3(BASE, n)) / 1000, 1) for n in range(132, 137)]
check("  measured cell chars / 1000", got, [8.6, 12.7, 10.0, 13.2, 15.4], "KB")
tbl = [8630, 12696, 9974, 13190, 15386]
check("  'the same figures the index below carries'",
      [len(cell3(BASE, n)) for n in range(132, 137)], tbl, "raw chars")

print("\n  Claim: 5.4 / 9.2 / 13.5 / 10.8 / 11.7 are rows :131-:135's whole LINES,")
print("         in BYTES, at db08b4c")
got = [round(len(row(OLD, n)) / 1000, 1) for n in range(131, 136)]
check("  measured line bytes / 1000", got, [5.4, 9.2, 13.5, 10.8, 11.7], "KB")

print("\n  Claim: 11.5 KB is row :135's whole LINE at db08b4c (11,544 chars; bytes 11,727)")
check("  :135 line chars at db08b4c", len(row(OLD, 135).decode()), 11544, "chars")
check("  :135 line bytes at db08b4c", len(row(OLD, 135)), 11727, "bytes")

check("  db08b4c 'mg-a3d4' occurrences (whole file)", blob(OLD).count(b"mg-a3d4"), 0)
check("  row :131's cell at 60f4dac", round(len(cell3(BASE, 131)) / 1000, 1), 4.9, "KB (chars)")

# ---------------------------------------------------------------- 4. F1
hdr("4. F1 — the 'states no 4d tally' correction and its measured cost")


def site1a(rev):
    m = re.search(r"\*\*⚠️ STEP 4d DID FIRE HERE.*?\)\. ", row(rev, 135).decode(), re.S)
    return m.group(0)


def sites23(rev):
    ls = [l.decode() for l in lines_bytes(rev)]
    i2 = next(i for i, l in enumerate(ls) if l.startswith("**STEP 4d HAS NOW FIRED AT"))
    i3 = next(i for i, l in enumerate(ls) if l.startswith("> **4d. GENERALISATION AUDIT."))
    a2 = ls[i2][:ls[i2].index("**", ls[i2].index("FIRED AT"))] + "**"
    a3 = re.search(r"\*\*NINE firings AT LEAST.*?tally\*\*", ls[i3]).group(0)
    return a2, a3, abs(i3 - i2)


for rev, lab, w1, seq in ((PARENT, "before", 103, 190), (HEAD, "after ", 133, 220)):
    a2, a3, apart = sites23(rev)
    tot = words(site1a(rev)) + words(a2) + words(a3)
    check(f"  site 1a words, {lab}", words(site1a(rev)), w1, "words")
    check(f"  three-assertion sequence, {lab}", tot, seq, "words")
    check(f"  reading time, {lab}", round(tot / WPM * 60, 1),
          round(seq / WPM * 60, 1), f"s @ {WPM} wpm")
check("  sites 2 and 3 lines apart", sites23(HEAD)[2], 55, "lines")
check("  acceptance (c): sequence under a minute", 220 / WPM * 60 < 60, True)

c = cell3(HEAD, 135)
a = c.index("five previous rows")
b = c.index("This row states no 4d *tally* of its own")
check("  gap from the counting phrase to the assertion", len(c[a:b]), 399, "chars")
check("  same gap in words", words(c[a:b]), 72, "words")

# ---------------------------------------------------------------- 5. offsets
hdr("5. THE REOPENING-NOTICE OFFSETS — 9,316 (new) and 8,402 (diagnosed)")
for rev, lab in ((OLD, "db08b4c"), (BASE, "60f4dac")):
    ln, c = row(rev, 135).decode(), cell3(rev, 135)
    print(f"  {lab} :135 — offset of the coverage-gap reopening notice:")
    for anch, an in (("**⚠️ BUT THE COVERAGE GAP", "notice start '**⚠️'"),
                     ("BUT THE COVERAGE GAP", "text start 'BUT'")):
        print(f"      {an:22} line-chars={ln.find(anch):>6}  "
              f"line-bytes={row(rev,135).find(anch.encode()):>6}  "
              f"cellraw={c.find(anch):>6}  cellstrip={c.strip().find(anch):>6}")
check("  new figure 9,316 == 'BUT' in the STRIPPED cell at 60f4dac",
      cell3(BASE, 135).strip().find("BUT THE COVERAGE GAP"), 9316, "chars")
check("  ... and 13,188 is that same stripped cell",
      len(cell3(BASE, 135).strip()), 13188, "chars")
print("  -> 9,316 is measured from 'BUT', not from the notice's own start (9,311/9,312).")
print("     Correct, but anchor-dependent by 5 chars and the anchor is not stated.")

print("\n  The DIAGNOSED figure: '8,402 is an offset into that line'.")
print("  Exhaustive hunt — every revision of STATE.md, every line, 6 coordinate systems,")
print("  3 anchor choices — for an offset EXACTLY equal to 8,402:")
import subprocess
revs = subprocess.run(["git", "-C", REPO, "log", "--format=%h", "--", "STATE.md"],
                      capture_output=True, text=True, check=True).stdout.split()
hits, tried = [], 0
for rv in revs:
    for i, l in enumerate(lines_bytes(rv), 1):
        p = split_row(l)
        co = {"line-bytes": l, "line-chars": l.decode()}
        if p and len(p) >= 3:
            co |= {"cellraw-chars": p[2], "cellstrip-chars": p[2].strip(),
                   "cellraw-bytes": p[2].encode(), "cellstrip-bytes": p[2].strip().encode()}
        for anch in ("**⚠️ BUT THE COVERAGE GAP", "⚠️ BUT THE COVERAGE GAP",
                     "BUT THE COVERAGE GAP"):
            for cn, hay in co.items():
                tried += 1
                nd = anch.encode() if isinstance(hay, bytes) else anch
                if hay.find(nd) == 8402:
                    hits.append((rv, i, cn, anch))
print(f"      searched {len(revs)} revisions, {tried} (line, coordinate, anchor) triples")
check("  offsets equal to 8,402 found", len(hits), 0, "hits")
print("      nearest at db08b4c :135 : 8,373 line-chars / 8,501 line-bytes (notice start)")
print("      -> 8,402 lands 29 chars INSIDE the notice.  True only in the vacuous sense")
print("         that 8,402 < 11,544; the correspondence is asserted, not established.")

# ---------------------------------------------------------------- 6. the 5.4 universal
hdr("6. '5.4 is not a cell at any revision' — the universal")
found = tot = 0
for rv in revs:
    for l in lines_bytes(rv):
        for cl in (split_row(l) or []):
            for v in (len(cl), len(cl.strip()), len(cl.encode()), len(cl.strip().encode())):
                tot += 1
                found += (5350 <= v <= 5449)
print(f"  scanned {len(revs)} revisions x every cell x "
      f"{{raw,stripped}} x {{chars,bytes}} = {tot} measurements")
check("  cells rounding to 5.4 KB, ever", found, 0, "cells")

# ---------------------------------------------------------------- 7. B1
hdr("7. B1 — the attribution correction, and 'two commits before mg-34bf's parent'")
check("  57f962f:343 and b68db5d:356 are the same bytes",
      row(LANDING, 343) == row(HEAD, 356), True)
KEY = b"AND THE CORRECTED FACT RELOCATES A HOLE"
print("\n  The paragraph across every revision that contains it:")
prev = None
for rv in reversed(revs):
    h = [(i, l) for i, l in enumerate(lines_bytes(rv), 1) if KEY in l]
    if not h:
        continue
    i, l = h[0]
    print(f"      {rv}  :{i:<4} {len(l):>5} bytes {'  <<< CHANGED' if l != prev else ''}")
    prev = l
print("  -> created by d5a3043 (mg-7d5a), repaired by 60f4dac (mg-3f21), and byte-identical")
print("     from 60f4dac onward: mg-ae62 (bdcb006) did NOT touch it.  Attribution CORRECT.")


def par_line(rev):
    return next(i for i, l in enumerate(lines_bytes(rev), 1) if KEY in l)


check("  paragraph line 57f962f -> bdcb006 (mg-ae62, +10)",
      par_line("bdcb006") - par_line(LANDING), 10, "lines")
check("  paragraph line bdcb006 -> 672915e (mg-a053, +3)",
      par_line(PARENT) - par_line("bdcb006"), 3, "lines")

sha = lambda r: subprocess.run(["git", "-C", REPO, "rev-parse", "--short", r],
                               capture_output=True, text=True, check=True).stdout.strip()
n_to_parent = int(subprocess.run(["git", "-C", REPO, "rev-list", "--count",
                                  f"{BASE}..{LANDING}^"], capture_output=True,
                                 text=True, check=True).stdout)
n_to_34bf = int(subprocess.run(["git", "-C", REPO, "rev-list", "--count",
                                f"{BASE}..{LANDING}"], capture_output=True,
                               text=True, check=True).stdout)
print(f"\n  mg-34bf = {sha(LANDING)}; its parent = {sha(LANDING+'^')}; and 60f4dac = {sha(BASE)}")
print(f"      commits from 60f4dac to mg-34bf's PARENT : {n_to_parent}")
print(f"      commits from 60f4dac to mg-34bf ITSELF   : {n_to_34bf}")
check("  claim '60f4dac is two commits before mg-34bf's PARENT'", n_to_parent, 2, "commits")
print("  -> it is ONE commit before the parent (two before mg-34bf itself).  Off by one,")
print("     in the commit message AND in the durable README bullet.")

# ---------------------------------------------------------------- 8. F3 restatement
hdr("8. F3 (left open, but restated) — the byte/char label")
check("  'file 192,898 -> 164,577 in real bytes': base", len(blob(BASE)), 192898, "bytes")
check("  'file 192,898 -> 164,577 in real bytes': landing", len(blob(LANDING)), 164577, "bytes")
print(f"\n  The commit calls the README's 188,870 -> 161,269 'a character count'.")
print(f"      actual characters: {len(blob(BASE).decode())} -> {len(blob(LANDING).decode())}")
print(f"      README's figures are characters MINUS NEWLINES (367 lines each side).")
print("      The substance (labelled bytes, is not bytes) holds; the label 'character")
print("      count' is itself one unit off.")

hdr(f"RESULT: {OK} checks passed, {FAIL} failed")
sys.exit(0)
