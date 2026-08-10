"""mg-2ff6 / D1 -- WHICH FIGURE MOVED, AND BY HOW MUCH.

THE TICKET'S ITEM 1, and the part cfd9c could not do: *This MOVES PUBLISHED
OUTPUT IN TWO TREES.  Report which figure moved and by how much, per figure, in
the same commit.*

cfd9c's `run_all.sh` proves it moved nothing, with `git status` rather than an
assertion.  That check is not available to me -- moving them is the ticket --
so what replaces it is this: every count row of every transcript this ticket
re-runs, compared with its own published text at `5c0849a`, with a verdict per
row.  A figure that moved and is not named below is a figure this accounting
missed, and there is no bucket it can hide in: `ADDED` and `DROPPED` are
reported beside `MOVED`, because a convention that quietly deleted a published
figure and reported `nothing moved` would be the worst outcome available here.

  D1a  THE ROLL, per transcript: published -> now, per figure
  D1b  THE SUMMARY, and the split that matters -- how many MOVED and how many
       were only ever UNDATED
  D1c  THE ARC-WIDE SUBSET, by cfd9c's own selector, with its class
  D1d  WHAT THIS TICKET DID NOT RE-RUN, named rather than omitted

Exit code = 0.  Nothing here is a check; it is an account.  A non-zero exit
would say a figure moving is a fault, and the whole finding is that it is not.
"""

import sys

import lib2ff6 as U

U.bar("mg-2ff6 / D1 -- WHICH FIGURE MOVED, AND BY HOW MUCH")
print("HEAD: %s   published-from: %s" % (U.head(), U.PUBLISHED_AT))

rx = U.corpus_label_rx()
ALL = {}

# ---------------------------------------------------------------------------
U.hdr("D1a  THE ROLL")

print("  Every count row of every transcript this ticket re-runs, keyed by")
print("  (section, label, ordinal) and compared with its published text.  The")
print("  `arc` column is cfd9c's own selector, lifted from `s4_convention.py`")
print("  rather than re-typed: `*` is a row S4c counts as an arc-wide corpus")
print("  figure.  Rows without it are here because they are in the same")
print("  transcript, not because anyone claimed they were arc-wide.")
for path in U.MOVED:
    rows = U.diff_rows(path)
    ALL[path] = rows
    print()
    U.pop("every count ROW of `%s`, at %s and now"
          % (path.split("/", 1)[1], U.PUBLISHED_AT))
    print("      %-3s %-52s %10s %10s %9s"
          % ("arc", "figure", "published", "now", "delta"))
    for (sec, label, ordn), old, new, verdict in rows:
        mark = "*" if rx.search(label) else " "
        name = label if ordn == 1 else "%s (#%d)" % (label, ordn)
        print(("      %-3s %-52.52s %10s %10s %9s   %s"
               % (mark, name, U.fmt_nums(old), U.fmt_nums(new),
                  U.delta(old, new),
                  "" if verdict == "SAME" else verdict)).rstrip())

# ---------------------------------------------------------------------------
U.hdr("D1b  THE SUMMARY, AND THE SPLIT THAT MATTERS")

flat = [(p, r) for p in U.MOVED for r in ALL[p]]
moved = [x for x in flat if x[1][3] == "MOVED"]
same = [x for x in flat if x[1][3] == "SAME"]
added = [x for x in flat if x[1][3] == "ADDED"]
dropped = [x for x in flat if x[1][3] == "DROPPED"]

print("  Two things are being counted and they are not the same thing.  A")
print("  figure that MOVED is one the arc's growth changed.  A figure that is")
print("  SAME was undated and is now dated, and its value never depended on")
print("  the arc at all -- it is FROZEN, and the convention's whole job is to")
print("  make that visible without a reader re-running anything.")
print()
U.pop("every count ROW of the %d TRANSCRIPTS re-run by this ticket"
      % len(U.MOVED))
U.plain("...FIGURES in them", len(flat))
print("      ^ one unit of that number is one printed count row")
U.plain("...of them that MOVED", len(moved))
print("      ^ one unit of that number is one printed count row")
U.plain("...of them UNCHANGED -- dated, not recomputed", len(same))
print("      ^ one unit of that number is one printed count row")
U.plain("...FIGURES ADDED by this ticket", len(added))
print("      ^ one unit of that number is one printed count row")
U.plain("...FIGURES DROPPED by this ticket", len(dropped))
print("      ^ one unit of that number is one printed count row")
arc_churn = [x for x in added + dropped if rx.search(x[1][0][1])]
U.plain("...of those ADDED or DROPPED that are ARC-WIDE", len(arc_churn))
print("      ^ one unit of that number is one printed count row")
print()
print("  THE ADDED AND DROPPED ROWS ARE NOT MINE, AND THE CHECK THAT SAYS SO")
print("  IS D0g: every line this ticket adds to another tree's transcript --")
print("  the `population:` line, the CLASS line, the interval block -- is put")
print("  through `lib56dc.count_rows` there and returns nothing.  They end in")
print("  a ref or a bracket, and `_COUNT_ROW` requires digits at the end of")
print("  the line.")
print()
if added or dropped:
    print("  WHAT THEY ARE IS WORSE THAN A FIGURE MOVING, AND NO CONVENTION")
    print("  THAT DATES VALUES CATCHES IT.  `a6_self.py`/AF2 prints ONE ROW")
    print("  PER TREE that carries an uncounted count, so the ROW SET of that")
    print("  table is itself a function of the corpus.  Trees left it and")
    print("  trees joined it, and a reader diffing the two transcripts by")
    print("  value would find rows with no counterpart on the other side:")
    print()
    for tag, rows in (("DROPPED", dropped), ("ADDED", added)):
        for p, ((sec, label, ordn), o, n, _v) in rows:
            print("      %-8s %-40.40s %-26.26s %s"
                  % (tag, p.split("/", 1)[1], label,
                     U.fmt_nums(o if tag == "DROPPED" else n)))
    print()
    U.note("D1b", "A PUBLISHED TABLE IN THIS ARC HAS A POPULATION-DEPENDENT "
           "ROW SET, not merely population-dependent values: %d rows left "
           "`out_a6_self.txt`'s per-tree table and %d joined it between %s "
           "and this run, and NONE of them is arc-wide by S4c's selector, so "
           "the convention this ticket adopts does not reach them.  Dating a "
           "value does not date a MEMBERSHIP."
           % (len(dropped), len(added), U.PUBLISHED_AT))
else:
    print("  NO PUBLISHED FIGURE WAS ADDED OR DROPPED.  Every count row that")
    print("  existed at %s still exists, under the same section and label."
          % U.PUBLISHED_AT)

# ---------------------------------------------------------------------------
U.hdr("D1c  THE ARC-WIDE SUBSET, WITH ITS CLASS")

print("  The rows S4c's selector flags, and what happened to each.  The class")
print("  is not read off the value -- it is read off the POPULATION LINE the")
print("  probe now prints above the figure, which is the only place it could")
print("  honestly come from.")
print()
U.pop("the count ROWS above that cfd9c's `CORPUS_LABEL` selects")
arc = [(p, r) for p, r in flat if rx.search(r[0][1])]
arcmoved = [x for x in arc if x[1][3] == "MOVED"]
print("      %-46s %9s %9s"
      % ("figure", "published", "now"))
for p, ((sec, label, ordn), old, new, verdict) in arc:
    print("      %-46.46s %9s %9s   %s"
          % ("%s / %s" % (p.split("/")[1][:16], label[:28]),
             U.fmt_nums(old), U.fmt_nums(new),
             verdict if verdict != "SAME" else "FROZEN or unaffected"))
print()
U.plain("...ARC-WIDE FIGURES in the re-run transcripts", len(arc))
print("      ^ one unit of that number is one printed count row")
U.plain("...of those ARC-WIDE FIGURES that MOVED", len(arcmoved))
print("      ^ one unit of that number is one printed count row")
print()
U.note("D1", "THIS TICKET MOVED %d PUBLISHED FIGURES ACROSS %d TRANSCRIPTS IN "
       "TWO TREES, %d of them arc-wide corpus figures.  The remaining %d "
       "arc-wide figures DID NOT MOVE, and not because they are fresh: their "
       "population is a REF and not the disk, so they were never stale, only "
       "undated.  A ticket that had `refreshed the stale figures` would have "
       "changed %d numbers that are constants and called it a repair."
       % (len(moved), len(U.MOVED), len(arcmoved), len(arc) - len(arcmoved),
          len(arc) - len(arcmoved)))

# ---------------------------------------------------------------------------
U.hdr("D1d  WHAT THIS TICKET DID NOT RE-RUN")

print("  Named rather than omitted, because a silent cap reads as coverage.")
print()
U.pop("every `out_*.txt` of the two trees this ticket edits")
notrun = [p for p in U.B.all_transcripts()
          if (p.startswith("code/grain_axis_audit_03d1/")
              or p.startswith("code/grain_arity_9160/"))
          and p not in U.MOVED]
U.plain("...TRANSCRIPTS in those two trees", len(notrun) + len(U.MOVED))
print("      ^ one unit of that number is one transcript file")
U.plain("...of them RE-RUN by this ticket", len(U.MOVED))
print("      ^ one unit of that number is one transcript file")
U.plain("...LEFT AT THEIR PUBLISHED BYTES", len(notrun))
print("      ^ one unit of that number is one transcript file")
print()
for p in notrun:
    print("      %s" % p)
print()
print("  WHY, AND IT IS NOT `THEY DO NOT MATTER`.  None of them prints a row")
print("  cfd9c's selector flags, so none carries a figure this ticket was")
print("  scoped to date.  `a4_sweep.py` additionally runs ANOTHER TREE's whole")
print("  suite twice; re-running it would regenerate `runner_exit_repair_bf79`")
print("  as a side effect of a citation.  The cost of leaving them is that")
print("  `mg-03d1` is now a tree whose transcripts are from two different")
print("  runs, which is a condition this convention exists to make readable")
print("  and which every population line in `out_a1_axes.txt` and")
print("  `out_a6_self.txt` now states outright.")

print()
print("D1 TOTAL BAD: 0")
sys.exit(0)
