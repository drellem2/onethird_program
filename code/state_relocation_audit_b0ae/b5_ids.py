"""B5 — THE mg-IDS.  A lost id is a lost attempt record, and is this ticket's headline if any.

mg-ea0e reports "68 distinct mg-ids in the old file, 0 UNREACHABLE. 34 still in STATE.md, 34
one link away."  Two things are re-derived here rather than checked:

  * the POPULATION.  68 is a fact about a regex as much as about a file.  This script states
    its own regex, prints its own count, and prints the SYMMETRIC DIFFERENCE against a
    deliberately looser and a deliberately stricter alternative, so the reader can see how
    much of "68" is the file and how much is the pattern.
  * the SPLIT.  "34 in place, 34 one link away" is a partition claim, and a partition claim
    is where an id can hide: an id counted as "one link away" that is in fact only reachable
    at hop 2 is not one link away, and one reachable at NO hop is a lost record.
"""

import re
import libb0ae as L

L.hdr("B5  mg-IDS — population first, then reachability, then the split")

old_t = L.text(L.git_show(L.OLD_REV, "STATE.md"))
new_t = L.text(L.git_show(L.NEW_REV, "STATE.md"))

STRICT = re.compile(r"\bmg-[0-9a-f]{4}\b")          # this audit's pattern
LOOSE = re.compile(r"mg-[0-9a-zA-Z]{4,}")           # anything that looks like an id
TIGHT = re.compile(r"(?<![\w-])mg-[0-9a-f]{4}(?![\w-])")

s_ids = set(STRICT.findall(old_t))
l_ids = set(LOOSE.findall(old_t))
t_ids = set(TIGHT.findall(old_t))

POP = "every mg-id-shaped string in old STATE.md (%d bytes)" % len(old_t.encode())
L.row("distinct ids, STRICT r'\\bmg-[0-9a-f]{4}\\b'", len(s_ids), POP, "distinct id strings")
L.row("distinct ids, LOOSE r'mg-[0-9a-zA-Z]{4,}'", len(l_ids), POP, "distinct id strings")
L.row("distinct ids, TIGHT (no adjacent word char)", len(t_ids), POP, "distinct id strings")
L.row("mg-ea0e reports", 68, "mg-ea0e's commit message, quoted", "distinct id strings — its number")
L.row("STRICT == mg-ea0e's 68", len(s_ids) == 68, POP, "boolean")
extra = sorted(l_ids - s_ids)
L.row("ids the LOOSE pattern adds", len(extra), POP, "distinct strings the strict pattern rejects")
for e in extra[:20]:
    print("      %s" % e)

L.row("total occurrences (not distinct)", len(STRICT.findall(old_t)), POP,
      "occurrences — the DIFFERENT grain, printed so 68 cannot be mistaken for it")

# ---------------------------------------------------------------------------
L.hdr("B5.1  REACHABILITY — by hop distance, computed from the file")

closure, hops = L.link_closure(new_t, L.NEW_REV)
bodies = {p: L.text(L.git_show(L.NEW_REV, p)) for p in sorted(closure)}
added_per_file = {p: "\n".join(L.diff_added_lines(L.OLD_REV, L.NEW_REV, p)) for p in sorted(closure)}

in_state, hop1, hop2plus, unreachable = [], [], [], []
for i in sorted(s_ids):
    if i in new_t:
        in_state.append(i)
        continue
    where = [p for p in sorted(closure) if i in bodies[p]]
    if not where:
        unreachable.append(i)
    elif min(hops[p] for p in where) == 1:
        hop1.append(i)
    else:
        hop2plus.append((i, min(hops[p] for p in where)))

POPI = "the %d distinct mg-ids of old STATE.md under this audit's STRICT pattern" % len(s_ids)
L.row("ids still in new STATE.md", len(in_state), POPI, "distinct ids, substring presence")
L.row("ids at hop 1 (genuinely one link away)", len(hop1), POPI, "distinct ids")
L.row("ids only at hop >= 2", len(hop2plus), POPI, "distinct ids — NOT one link away")
L.row("ids UNREACHABLE", len(unreachable), POPI, "distinct ids — each is a lost attempt record")
for i in unreachable:
    print("      LOST: %s" % i)
for i, h in hop2plus:
    print("      hop %d only: %s" % (h, i))
L.row("mg-ea0e's split", "34 in place / 34 one link away",
      "mg-ea0e's commit message, quoted", "distinct ids — its partition")
L.row("this audit's split", "%d in place / %d hop-1 / %d hop>=2" % (len(in_state), len(hop1), len(hop2plus)),
      POPI, "distinct ids")

# strictest reading: reachable only via text THIS COMMIT wrote
strict_unreach = []
for i in sorted(s_ids):
    if i in new_t:
        continue
    if not any(i in added_per_file[p] for p in sorted(closure)):
        strict_unreach.append(i)
L.row("ids not in new STATE.md nor in ADDED text", len(strict_unreach), POPI,
      "distinct ids — reachable only through text that predates this commit")
for i in strict_unreach:
    print("      pre-existing witness only: %s  (in %s)"
          % (i, ",".join(p for p in sorted(closure) if i in bodies[p])[:80]))

# ---------------------------------------------------------------------------
L.hdr("B5.2  CONTROLS — the instrument shown finding an absence")

fake = ["mg-0000", "mg-ffff", "mg-dead"]
found_fake = [f for f in fake if f in new_t or any(f in bodies[p] for p in closure)]
L.row("CONTROL invented ids found in the corpus", len(found_fake),
      "3 ids of the same shape that do not exist in this repo",
      "ids — MUST be 0, else 'reachable' is satisfiable by anything")

held = "docs/audit-stage-process.md"
unreach_wo = 0
for i in sorted(s_ids):
    if i in new_t:
        continue
    if not any(i in bodies[p] for p in sorted(closure) if p != held):
        unreach_wo += 1
L.row("CONTROL ids unreachable with %s withheld" % held.split("/")[-1], unreach_wo, POPI,
      "distinct ids — MUST be > 0, else withholding the largest destination changes nothing "
      "and the check is not measuring reachability")

L.hdr("B5.3  PER-FILE ENUMERATION (mg-ea0e's A4 — 'enumerated, not taken from the moves')")
print("  %-46s %5s %7s %7s" % ("file", "hop", "ids", "of which new-to-corpus"))
for p in sorted(closure, key=lambda x: (hops[x], x)):
    ids_here = set(STRICT.findall(bodies[p])) & s_ids
    ids_added = set(STRICT.findall(added_per_file[p])) & s_ids
    print("  %-46s %5d %7d %7d" % (p.replace("docs/", ""), hops[p], len(ids_here), len(ids_added)))
print("  %-46s %5s %7d" % ("STATE.md (new)", 0, len(set(STRICT.findall(new_t)) & s_ids)))

print("\nB5 DONE")
