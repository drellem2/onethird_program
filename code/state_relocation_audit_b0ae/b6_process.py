"""B6 — DID THE BUILDER EXERCISE JUDGEMENT IT WAS NOT GIVEN, and what did the move break?

The brief gave mg-ea0e THREE MOVES and no editorial latitude, so every line that left
STATE.md must fall inside one of three ranges.  Any line removed from outside them is an
editorial decision taken without a mandate, and is a finding about the process whether or not
the result reads better.

It then measures the one consequence mg-ea0e disclosed as NOT-DONE but did not size: STATE.md
shrank from 386 lines to 175, and every `STATE.md:<n>` citation anywhere else in the repo
that points past :175 — or at content that has moved — is now a reference into empty space.
"Flagged, not fixed" is an honest disclosure; it is not a measurement, and the blast radius is
the number nobody has printed.
"""

import re
import libb0ae as L

L.hdr("B6.1  EVERY REMOVED LINE, CHARGED TO ONE OF THE THREE MOVES")

old_t = L.text(L.git_show(L.OLD_REV, "STATE.md"))
new_t = L.text(L.git_show(L.NEW_REV, "STATE.md"))
old_lines, new_lines = old_t.split("\n"), new_t.split("\n")

MOVES = {"MOVE 1 Appendix A :180-381": range(180, 382),
         "MOVE 2 threads :142-177": range(142, 178),
         "MOVE 3 seven rows :130-136": range(130, 137)}

new_set = set(new_lines)
removed = [(i + 1, l) for i, l in enumerate(old_lines) if l.strip() and l not in new_set]
POP = "the %d non-blank lines of old STATE.md" % sum(1 for l in old_lines if l.strip())
L.row("lines no longer present verbatim in STATE.md", len(removed), POP,
      "whole lines, exact string")

charged = {k: 0 for k in MOVES}
uncharged = []
for n, l in removed:
    hit = [k for k, r in MOVES.items() if n in r]
    if hit:
        charged[hit[0]] += 1
    else:
        uncharged.append((n, l))
for k in MOVES:
    L.row("  charged to %s" % k, charged[k], POP, "removed lines whose old line number is in that range")
L.row("REMOVED FROM OUTSIDE ALL THREE MOVES", len(uncharged), POP,
      "removed lines with no mandate in the brief — each is editorial judgement")
for n, l in uncharged[:30]:
    print("      old:%d  %.140s" % (n, l))

# and the converse: lines added to STATE.md that are not in the old file
composed = [(i + 1, l) for i, l in enumerate(new_lines) if l.strip() and l not in set(old_lines)]
L.row("lines in new STATE.md with no old antecedent", len(composed),
      "the %d non-blank lines of new STATE.md" % sum(1 for l in new_lines if l.strip()),
      "whole lines, exact string — composed prose, which the brief allows only for links, "
      "provenance headers and one current-position paragraph")
for n, l in composed:
    tag = "LINK" if "](" in l and len(l) < 400 else ("ROW" if l.startswith("|") else "PROSE")
    print("      new:%-4d %-5s %.120s" % (n, tag, l))

L.hdr("B6.2  THE TWO SELF-REPORTED DEPARTURES, CHECKED")

L.row("old :382-386 ('Why 1/3') still in STATE.md",
      all(old_lines[i] in new_set for i in range(381, 386) if old_lines[i].strip()),
      "the 5 lines old:382-386 that departure 1 says were kept",
      "boolean — all non-blank lines present verbatim")
row133_new = new_lines[132]
n_sent = row133_new.count("**") // 2
L.row("row :133 sentence-markers in new STATE.md", n_sent,
      "the single line new STATE.md:133", "bold-delimiter pairs — departure 2 says it kept TWO sentences")
L.row("row :133 mentions DISCHARGED", "DISCHARGED" in row133_new,
      "the same line", "boolean — the reason departure 2 gives for keeping the second sentence")

L.hdr("B6.2b  THE ONE COMPOSED PARAGRAPH — is it quoted, as mg-ea0e says, or written?")
L.note("MOVE 2 permits 'a short current-position paragraph'.  That paragraph is the ONLY place\n"
       "in this change where a human sentence about the mathematics was composed rather than\n"
       "moved, so it is the only place a claim could have been invented.  mg-ea0e says it is\n"
       "'built from the chronology's own quoted clauses'.  Every quoted span is checked.")
para = "\n".join(new_lines[143:157])
chron = L.text(L.git_show(L.NEW_REV, "docs/state-history/threads-chronology.md"))
quotes = re.findall(r'\*"([^"]+)"\*', para)
# DEFECT D2 of this instrument, found and fixed during the run: STATE.md hard-wraps its
# prose, so a quoted clause spans a newline and an exact-substring test against the
# unwrapped source reports it MISSING.  Four of nine failed for that reason alone.  Both
# sides are whitespace-normalised; the exact-string test is kept as the stricter column.
def ws(s):
    return " ".join(s.split())


def strip_markup(s):
    return ws(s).replace("*", "").replace("`", "")


chron_n, old_n = ws(chron), ws(old_t)
chron_m, old_m = strip_markup(chron), strip_markup(old_t)
q_exact = [q for q in quotes if q in chron or q in old_t]
q_ok = [q for q in quotes if ws(q) in chron_n or ws(q) in old_n]
q_markup = [q for q in quotes if strip_markup(q) in chron_m or strip_markup(q) in old_m]
L.row("quoted clauses in the current-position paragraph", len(quotes),
      "the %d characters of new STATE.md:144-157" % len(para),
      "spans delimited by *\"...\"* — the paragraph's own quotation marks")
L.row("  found EXACTLY (line breaks and all)", len(q_exact),
      "the %d quoted clauses above" % len(quotes),
      "spans, exact string — fails on any clause the paragraph hard-wrapped")
L.row("  found after whitespace normalisation", len(q_ok),
      "the %d quoted clauses above" % len(quotes),
      "spans, whitespace-collapsed on BOTH sides — the honest grain for wrapped prose")
L.row("  found after markup is stripped too", len(q_markup),
      "the %d quoted clauses above" % len(quotes),
      "spans with * and ` removed on both sides — the WORDS, ignoring emphasis")
for q in quotes:
    if ws(q) not in chron_n and ws(q) not in old_n:
        tag = "WORDS MATCH, MARKUP DROPPED" if strip_markup(q) in chron_m or strip_markup(q) in old_m \
              else "NOT FOUND AT ANY GRAIN"
        print("      %-28s %r" % (tag, ws(q)[:130]))
L.note("A clause in the WORDS-MATCH row is not an invented claim and not a verbatim quotation\n"
       "either: the summary set it inside quotation marks having dropped the source's own\n"
       "emphasis (`*cancellation*` -> cancellation).  mg-ea0e's 'NO MATHEMATICAL CLAIM IS\n"
       "REWORDED' survives at the word grain, which is the grain that claim is about.")
L.row("paragraph length", len(para), "the same paragraph", "characters — 'short' is the brief's word")
ids_para = sorted(set(L.MG_ID_RE.findall(para)))
L.row("mg-ids cited inside the paragraph", len(ids_para), "the same paragraph", "distinct ids")
print("      %s" % ", ".join(ids_para))

L.hdr("B6.3  THE BLAST RADIUS NOBODY SIZED — STATE.md:<n> citations elsewhere in the repo")

files = [p for p in L.git_ls(L.NEW_REV) if p != "STATE.md"
         and p.rsplit(".", 1)[-1] in ("md", "txt", "py", "sh", "html")]
CITE = re.compile(r"STATE\.md[: ]?:?(\d{1,4})(?:\s*[-–]\s*(\d{1,4}))?")
NEW_LEN = len(new_lines)

cites = []
for p in files:
    try:
        body = L.text(L.git_show(L.NEW_REV, p))
    except Exception:
        continue
    for m in CITE.finditer(body):
        lo = int(m.group(1))
        hi = int(m.group(2)) if m.group(2) else lo
        cites.append((p, lo, hi, m.group(0)))

POPC = ("every `STATE.md:<n>` citation in the %d tracked md/txt/py/sh/html files of the repo "
        "other than STATE.md itself, at %s" % (len(files), L.NEW_REV))
L.row("STATE.md line citations found", len(cites), POPC, "citations, one per regex match")
L.row("  distinct citing files", len(set(c[0] for c in cites)), POPC, "files")

past_end = [c for c in cites if c[1] > NEW_LEN]
moved_into = [c for c in cites if c[1] <= NEW_LEN and c[1] > 129]
still_ok = [c for c in cites if c[1] <= 129]
L.row("citations pointing PAST the new end of file", len(past_end), POPC,
      "citations with a line number > %d — these now resolve to nothing" % NEW_LEN)
L.row("citations into :130-%d (the rewritten zone)" % NEW_LEN, len(moved_into), POPC,
      "citations whose target line still exists but whose CONTENT may have changed")
L.row("citations into :1-129 (the untouched prefix)", len(still_ok), POPC,
      "citations whose target is byte-identical — these are safe by construction")

by_file = {}
for p, lo, hi, txt in past_end:
    by_file.setdefault(p, []).append(lo)
print("\n  FILES CITING A LINE THAT NO LONGER EXISTS (top 25 by count):")
for p in sorted(by_file, key=lambda x: -len(by_file[x]))[:25]:
    print("      %-64s %3d citations, max :%d" % (p, len(by_file[p]), max(by_file[p])))

L.hdr("B6.3b  ARE THE DEAD CITATIONS LIVE REFERENCES OR HISTORICAL RECORD?")
L.note("A committed transcript that says STATE.md:355 is recording what it read at the commit\n"
       "it ran on; it is archaeology and is SUPPOSED to be frozen.  A live script or a live\n"
       "document that says STATE.md:355 is now wrong.  Splitting them is the difference\n"
       "between a scary number and a true one.")


def kind(p):
    if p.startswith("code/") and ("/out_" in p or p.endswith(".txt")):
        return "transcript (frozen record)"
    if p.startswith("code/"):
        return "LIVE SCRIPT"
    return "LIVE DOCUMENT"


kinds = {}
for p, lo, hi, t in past_end:
    kinds.setdefault(kind(p), set()).add(p)
for k in sorted(kinds):
    n_c = sum(1 for p, lo, hi, t in past_end if kind(p) == k)
    L.row("%s" % k, "%d citations in %d files" % (n_c, len(kinds[k])), POPC,
          "citations past :%d, split by whether the citing artifact is still consulted" % NEW_LEN)
    for p in sorted(kinds[k]):
        if k != "transcript (frozen record)":
            print("      %s" % p)

L.row("CONTROL citations past end measured at %s" % L.OLD_REV,
      sum(1 for p, lo, hi, t in cites if lo > len(old_lines)), POPC,
      "citations — the SAME citation set scored against the OLD file, which must be far "
      "smaller: that difference is exactly what this commit created")

L.hdr("B6.4  LINK INTEGRITY OF THE NEW FILE")
tracked = set(L.git_ls(L.NEW_REV))
targets = [m.group(1).split("#")[0] for m in L.LINK_RE.finditer(new_t)]
local = [t for t in targets if not t.startswith("http")]
dead = sorted(set(t for t in local if t not in tracked))
L.row("markdown links in new STATE.md", len(targets),
      "every ](...) target in new STATE.md", "link occurrences")
L.row("  local (non-http) targets", len(local), "the same", "link occurrences")
L.row("DEAD local links", len(dead), "the %d distinct local targets" % len(set(local)),
      "targets that are not tracked paths at %s" % L.NEW_REV)
for d in dead:
    print("      DEAD: %s" % d)

print("\nB6 DONE")
