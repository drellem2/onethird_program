"""mg-9160 / S3 -- THE POPULATION RULE, REPAIRED, AND WHAT THE REPAIR FINDS
IN THE RULE THAT FOUND IT.

My ticket: `count_rows` returns ONE label and ONE grain PER LINE, so 626
integers inside labels are never classified at all, and repairing `_classify`
would not reach a single one of them.  That is right and it UNDERSTATES ITSELF
BY A FACTOR OF 3.4, because the same rule returns a LIST of trailing integers
per line and gives the whole list ONE grain: measured, 2107 of the corpus's 2894
printed integers have no grain of their own, against the 626 the ticket names.

  S3a  the repaired population: ONE ROW PER INTEGER.  How many integers the
       old rule gives a grain of their own, and how many it does not.
  S3b  ATTRIBUTION -- which noun a label-internal integer belongs to.  The one
       place this tree disagrees with mg-03d1's rule rather than composing it.
  S3c  AF2's five rows, re-read.  The count of 5 stands; four of the five
       DETAIL LINES name the wrong noun, in the direction AS1 already repaired
       once in the same instrument.
  S3d  what the repair does NOT do.

Exit code = number of S3 checks that fail.
"""

import sys
import textwrap

import lib9160 as G

BAD = 0
A = G.A

G.bar("mg-9160 / S3 -- ONE ROW PER INTEGER")
print("HEAD: %s   subject: `lib56dc.count_rows`, `lib03d1.embedded_counts`"
      % G.head())

CORPUS = G.parent_corpus()

# ---------------------------------------------------------------------------
G.hdr("S3a  THE REPAIRED POPULATION, AND THE SECOND COLLAPSE NOBODY COUNTED")

rows = 0
trailing = 0
shared = 0
embedded = 0
for p, r in CORPUS:
    t = G.read(p, r)
    if t is None:
        continue
    for i, where, v, noun, verd, label in G.count_items(t):
        if where == "trailing":
            trailing += 1
            shared += verd == "SHARED"
        else:
            embedded += 1
    rows += len(A.count_rows(t))

items = trailing + embedded
print("  `count_rows` is a shape rule over the LINE, and its unit is the line.")
print("  So a line is one row however many integers it prints.  Counting the")
print("  population in INTEGERS instead:")
print()
G.pop("every INTEGER printed in a count row of the reconstructed corpus",
      ref=G.RECON)
G.row("...count ROWS the old rule returns", rows, "printed line")
G.row("...INTEGERS in those rows, counted one at a time", items, "integer")
G.row("...INTEGERS the old rule returns as values", trailing, "integer")
G.row("...INTEGERS inside labels, in no population at all", embedded, "integer")
G.row("...INTEGERS SHARING one grain with a neighbour", shared, "integer")
print()
own = trailing - shared
print("      integers with a grain of their OWN:     %4d of %4d  (%4.1f%%)"
      % (own, items, 100.0 * own / items))
print("      integers with a SHARED grain:           %4d of %4d  (%4.1f%%)"
      % (shared, items, 100.0 * shared / items))
print("      integers with NO grain at all:          %4d of %4d  (%4.1f%%)"
      % (embedded, items, 100.0 * embedded / items))
print()
print("  MY TICKET SAYS 626 INTEGERS ARE NEVER CLASSIFIED.  It is right about")
print("  those and it stops there.  %d MORE are classified only in the sense"
      % shared)
print("  that a grain was computed for the LINE they sit on and handed to all")
print("  of them at once: `ROWS 49 SITES 47 GAP 2` gets ONE symbol.  Counted")
print("  in integers rather than in lines, the rule gives an own-grain to %d"
      % own)
print("  of %d -- %.1f%%.  The floor is %.1fx deeper than the ticket says."
      % (items, 100.0 * own / items, 1.0 * (items - own) / embedded))
p5 = trailing > rows
print()
print("      P5 as pre-registered (trailing integers > count rows)   %s"
      % ("HIT -- %d > %d" % (trailing, rows) if p5
         else "*** MISS -- %d vs %d" % (trailing, rows)))
BAD += not p5

# ---------------------------------------------------------------------------
G.hdr("S3b  ATTRIBUTION -- WHICH NOUN A LABEL-INTERNAL INTEGER BELONGS TO")

print("  `lib03d1.embedded_counts` attaches the word immediately AFTER the")
print("  integer.  That is right for prose --")
print()
print("      ...ROWS outside it, across 10 distinct basenames        14")
print()
print("  -- and wrong for a column table, which this arc writes as often --")
print()
print("      973ca61 ALL rows   ROWS  49  SITES  47  GAP  2")
print()
print("  -- where the word after `49` is `SITES`, the noun of the NEXT")
print("  column's value.  Attaching it makes 49 a count of sites when the")
print("  label says it is a count of rows.")
print()
print("  So `attribute` returns BOTH neighbours and a verdict and never")
print("  silently picks.  Census over the label-internal integers:")
print()
counts = {}
shapes = {}
for p, r in CORPUS:
    t = G.read(p, r)
    if t is None:
        continue
    for i, label, nums in A.count_rows(t):
        e = G.B.embedded_counts(label)
        if not e:
            continue
        sh = G.column_shape(label, nums)
        for m in G._INT.finditer(label):
            _pv, _nv, verd = G.attribute(label, m.span(1))
            counts[verd] = counts.get(verd, 0) + 1
            shapes[sh] = shapes.get(sh, 0) + 1
G.pop("the %d label-internal INTEGERS of the reconstructed corpus" % embedded,
      ref=G.RECON)
for k in ("NEXT", "PREV", "AMBIGUOUS", "NEITHER"):
    G.row("...INTEGERS whose attribution reads %s" % k, counts.get(k, 0),
          "integer")
print()
amb = counts.get("AMBIGUOUS", 0)
nxt = counts.get("NEXT", 0)
prv = counts.get("PREV", 0)
print("  READ AGAINST THE PARENT'S RULE, WHICH ALWAYS TAKES THE FOLLOWING WORD:")
print("      it names a noun at                 %4d of %4d integers"
      % (nxt + amb, embedded))
print("      it returns an EMPTY noun at        %4d  (nothing follows the"
      % prv)
print("                                              integer; a noun PRECEDES)")
print("      of the %4d it does name, the attribution is UNRESOLVED at %4d"
      % (nxt + amb, amb))
print("      -- %.1f%% -- because a grain noun sits on the other side too."
      % (100.0 * amb / (nxt + amb) if nxt + amb else 0))
print()
print("  AND THE TIE-BREAK, OFFERED BESIDE THE VERDICT AND NEVER IN PLACE OF")
print("  IT.  `column_shape` asks whether the whole row alternates strictly")
print("  word,integer,word,integer -- the `NOUN VALUE` column convention --")
print("  or does not.  DESIGNED AFTER LOOKING AT THE ROWS IT SEPARATES, which")
print("  is said here so a reader can discount it.")
print()
G.pop("the same %d label-internal INTEGERS, by the SHAPE of their row"
      % embedded, ref=G.RECON)
for k in ("NOUN-VALUE", "VALUE-NOUN", "UNDETERMINED"):
    G.row("...INTEGERS in rows of shape %s" % k, shapes.get(k, 0), "integer")
print()
print("      resolved by the tie-break:  %d of %d;  left open: %d"
      % (shapes.get("NOUN-VALUE", 0) + shapes.get("VALUE-NOUN", 0), embedded,
         shapes.get("UNDETERMINED", 0)))
print()
print("  THE TIE-BREAK IS NOT A REPAIR OF THE PARENT'S RULE AND I AM NOT")
print("  PROPOSING IT AS ONE.  It resolves %d of %d and leaves %d open, and"
      % (shapes.get("NOUN-VALUE", 0) + shapes.get("VALUE-NOUN", 0), embedded,
         shapes.get("UNDETERMINED", 0)))
print("  the open ones are open because the label genuinely does not say.")

# ---------------------------------------------------------------------------
G.hdr("S3c  AF2's FIVE ROWS, RE-READ -- THE COUNT STANDS, FOUR DETAIL LINES "
      "DO NOT")

AF2 = [("code/runner_exit_repair_70c7/out_r4_property.txt", 30),
       ("code/runner_exit_repair_bf79/out_p1_grain.txt", 76),
       ("code/runner_exit_repair_bf79/out_p1_grain.txt", 79),
       ("code/runner_exit_repair_bf79/out_p1_grain.txt", 81),
       ("code/runner_exit_repair_bf79/out_p1_grain.txt", 85)]

print("  AF2 reports 5 rows whose two counts are at different grains, and")
print("  prints a detail line for each naming the embedded count's grain.")
print("  The FINDING is right.  Four of the five DETAIL LINES name the noun")
print("  one column to the right of the value they are about.")
print()
wrong = 0
for path, ln in AF2:
    ref = dict(CORPUS).get(path)
    t = G.read(path, ref)
    hit = [(i, lab, nums) for i, lab, nums in A.count_rows(t) if i == ln]
    if not hit:
        print("      %s:%d -- not a count row at this ref" % (path, ln))
        BAD += 1
        continue
    i, lab, nums = hit[0]
    sh = G.column_shape(lab, nums)
    print("      %s:%d" % (path.split("/")[-1], ln))
    print("          %s   [trailing: %s]"
          % (lab[:56], ",".join(str(x) for x in nums)))
    print("          row shape: %s" % sh)
    for m in G._INT.finditer(lab):
        v = int(m.group(1).replace(",", ""))
        pv, nv, verd = G.attribute(lab, m.span(1))
        parent = dict(G.B.embedded_counts(lab)).get(v, "")
        mine = pv if sh == "NOUN-VALUE" else nv if sh == "VALUE-NOUN" else \
            "%s|%s" % (pv, nv)
        bad = sh == "NOUN-VALUE" and parent and parent != pv
        wrong += bad
        print("          %-6d parent says `%-10s`   the label reads `%-10s`  %s"
              % (v, parent, mine, "<-- one column right" if bad else ""))
    print()
G.pop("the 5 ROWS of AF2, re-read one integer at a time")
G.row("...INTEGERS the parent's detail lines name one column right", wrong,
      "integer")
print()
print("  WHAT THIS DOES AND DOES NOT MOVE.  AF2's count of 5 STANDS -- on")
print("  every one of those rows the two counts really are at different")
print("  grains, and on the four table rows there are THREE grains on the")
print("  line, not two: a ROW count, a SITE count, and a GAP.  The finding")
print("  gets bigger.  What moves is the attribution in the printed detail:")
print("  `the embedded 10 sites is at grain site` reads 10 as a site count")
print("  where the label says `ROWS 10 SITES 9`.")
print()
print("  AND IT IS THE SAME DEFECT AS THE PARENT'S OWN AS1, IN THE OPPOSITE")
print("  DIRECTION.  AS1: *`label_grain` took the LAST grain noun of a label,")
print("  so it read `basenames` -- the EMBEDDED count's noun.*  That was")
print("  repaired.  `embedded_counts` takes the FOLLOWING noun and was not")
print("  repaired with it.  A value attributed to the wrong noun on the same")
print("  line, twice, in one instrument, in the tree that measures exactly")
print("  that defect.")

# ---------------------------------------------------------------------------
G.hdr("S3d  WHAT THE REPAIR DOES NOT DO")

for t in [
    "BEING IN THE POPULATION IS NOT BEING CLASSIFIED CORRECTLY.  E6, filed "
    "before the code existed.  `count_items` puts every integer in scope and "
    "attaches the noun its own words give it.  Whether that noun is the right "
    "grain for that integer is a fact about the CODE that printed it, and the "
    "only way to get it is to re-derive the quantity -- which is possible only "
    "where a re-derivation sits beside the row.  Nothing here re-derives one.",

    "THE SHARED-GRAIN INTEGERS ARE COUNTED, NOT ATTRIBUTED.  The %d trailing "
    "integers sharing a line's grain are reported as SHARED and no attempt is "
    "made to give each its own noun from the column header above it.  Doing "
    "that needs a header parser, this arc has none, and writing one to fix a "
    "row I found today is how the next instrument gets a rule nobody checked."
    % shared,

    "NO CALL SITE IS MIGRATED.  `lib56dc`, `lib03d1`, `libbf79` and `lib70c7` "
    "are unmodified, no transcript of another tree is regenerated, and no "
    "number published by another tree moves.  The repaired population runs "
    "HERE and is reported HERE.",

    "THE TIE-BREAK IS NOT VALIDATED AGAINST GROUND TRUTH.  `column_shape` "
    "agrees with a reading of five rows I did by hand.  There is no labelled "
    "set to score it on, so its %d resolutions are a rule's output and not a "
    "measured accuracy." % (shapes.get("NOUN-VALUE", 0)
                            + shapes.get("VALUE-NOUN", 0)),
]:
    body = textwrap.wrap(" ".join(t.split()), 70)
    print("  * " + body[0])
    for extra in body[1:]:
        print("    " + extra)
    print()

print("S3 TOTAL BAD: %d" % BAD)
sys.exit(BAD)
