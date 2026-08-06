"""B4 — "LINES 1-129 ARE BYTE-IDENTICAL" and "NO MATHEMATICAL CLAIM IS REWORDED".

Both are claims a word-level diff would pass and a careful retyping would defeat.  So:

  * the prefix is compared by SHA-256 over the exact byte range, and the boundary is
    LOCATED rather than assumed — the script finds the longest byte-identical prefix
    itself and then reports whether 129 is that number, one short of it, or inside it;
  * the mathematics is not sampled by eye.  Every atom of the old file carrying a
    mathematical token is a member of a stated population, and every member is checked for
    verbatim survival.  Five relocated ones are then printed in full, as the ticket asks,
    but the five are an ILLUSTRATION of a census, not the census.
"""

import re
import libb0ae as L

L.hdr("B4.1  THE UNTOUCHED PREFIX — located, not assumed")

old_b = L.git_show(L.OLD_REV, "STATE.md")
new_b = L.git_show(L.NEW_REV, "STATE.md")
old_t, new_t = L.text(old_b), L.text(new_b)
old_lines, new_lines = old_t.split("\n"), new_t.split("\n")

# longest common line prefix, found by this script
k = 0
while k < min(len(old_lines), len(new_lines)) and old_lines[k] == new_lines[k]:
    k += 1

POP = "the %d line-positions the two files have in common" % min(len(old_lines), len(new_lines))
L.row("longest byte-identical line prefix", k, POP,
      "lines, counted from :1 — the FIRST position where the two files differ is :%d" % (k + 1))
L.row("mg-ea0e claims byte-identical through", 129, "mg-ea0e's commit message, quoted",
      "lines — its claim, not my measurement")
L.row("claim is inside the true prefix", k >= 129, POP, "boolean")

pre_old = "\n".join(old_lines[:129]).encode()
pre_new = "\n".join(new_lines[:129]).encode()
L.row("SHA-256 of old :1-129", L.sha256(pre_old)[:32], "the first 129 lines of STATE.md at %s" % L.OLD_REV,
      "hex digest (first 32 of 64 chars), over exact bytes including inner newlines")
L.row("SHA-256 of new :1-129", L.sha256(pre_new)[:32], "the first 129 lines of STATE.md at %s" % L.NEW_REV,
      "hex digest, same construction")
L.row("digests equal", L.sha256(pre_old) == L.sha256(pre_new),
      "the two byte ranges above", "boolean — a retyped line changes this and survives a word-diff")
L.row("bytes in the identical prefix", L.commas(len(pre_old)),
      "lines :1-129 of both files", "utf-8 bytes")

# control: the hash must move for a one-character change
tampered = pre_old.replace(b"1/3", b"1/4", 1)
L.row("CONTROL digest after one 1/3 -> 1/4", L.sha256(tampered)[:32] != L.sha256(pre_old)[:32],
      "the same byte range with a single mathematical substitution",
      "boolean — MUST be True, else the digest is not an instrument")

L.row("first differing line number", k + 1, POP, "1-based line number")
print("      old:%d  %.150s" % (k + 1, old_lines[k] if k < len(old_lines) else "<eof>"))
print("      new:%d  %.150s" % (k + 1, new_lines[k] if k < len(new_lines) else "<eof>"))

# ---------------------------------------------------------------------------
L.hdr("B4.2  THE MATHEMATICS — a census, not a sample")

MATH = re.compile(
    r"(\d+\s*/\s*\d+|[≤≥≠≈⟹→←≪≫±·×∑∏√∫∀∃∈⊆∪∩]|\^|`\\?[a-zA-Z]*_?\{?|"
    r"\bO\(|\bΘ\(|\bΩ\(|sqrt|\blog\b|\bbeta\b|\bλ|\bδ|\bε|\bσ|\bΦ|\bVar\b|\bE\[|"
    r"\bn\^?2\b|\bPr\[|\binequal|\bbound\b|\blemma\b|\btheorem\b)")

links = L.linked_files(new_t, L.NEW_REV)
added_per_file = {p: "\n".join(L.diff_added_lines(L.OLD_REV, L.NEW_REV, p)) for p in links}
added = "\n".join(added_per_file[p] for p in links)
HAY_LIKE = new_t + "\n" + added

atoms = L.atomise(old_t, "old")
math_atoms = [a for a in atoms if MATH.search(a["text"])]
POPM = ("the %d atoms of old STATE.md matching this script's math-token regex "
        "(fractions, relation/operator glyphs, ^, O(/Theta(/Omega(, sqrt, log, the greek "
        "names this corpus uses, Var/E[/Pr[, and the words bound/lemma/theorem)" % len(math_atoms))
L.row("mathematical atoms in old STATE.md", len(math_atoms), POPM, "atoms")
L.row("  as a share of all atoms", "%.1f%%" % (100.0 * len(math_atoms) / len(atoms)),
      "the %d atoms of old STATE.md" % len(atoms), "percent")

changed = [a for a in math_atoms if a["text"] not in HAY_LIKE]
L.row("mathematical atoms NOT present verbatim", len(changed), POPM,
      "atoms, exact-substring presence in new STATE.md or in text THIS COMMIT ADDED")
for a in changed[:20]:
    print("      old:%d  %r" % (a["lineno"], a["text"][:160]))

ctrl = sum(1 for a in math_atoms
           if (a["text"][:len(a["text"]) // 2] + "Z" + a["text"][len(a["text"]) // 2 + 1:]) not in HAY_LIKE)
L.row("CONTROL math atoms lost under 1-char edit", ctrl, POPM,
      "atoms, each mutated at its midpoint — MUST equal the population, else 'verbatim' is not tested")

# the 8-row proof ledger and the L1b section, named explicitly
L.hdr("B4.3  THE 8-ROW PROOF LEDGER AND L1b — located by content, then compared")

def find_section(lines, needle):
    for i, l in enumerate(lines):
        if needle.lower() in l.lower():
            return i + 1
    return None

for needle in ("ledger", "L1b", "proof chain", "Why 1/3"):
    o, n = find_section(old_lines, needle), find_section(new_lines, needle)
    same = (o is not None and n is not None and old_lines[o - 1] == new_lines[n - 1])
    print("      %-14s old:%-5s new:%-5s  header line identical: %s" % (needle, o, n, same))

led_old = [i + 1 for i, l in enumerate(old_lines) if l.startswith("|") and "L1" in l]
L.row("ledger-style rows naming an L-lemma", len(led_old),
      "the table rows of old STATE.md whose text contains 'L1'", "rows")
ident = sum(1 for i in led_old if i - 1 < len(new_lines) and new_lines[i - 1] == old_lines[i - 1])
L.row("  byte-identical at the same line number", ident,
      "the %d rows above" % len(led_old), "rows, exact string at the SAME 1-based line")

L.hdr("B4.4  FIVE RELOCATED MATHEMATICAL SENTENCES, PRINTED IN FULL (the ticket's §4)")
relocated = [a for a in math_atoms if a["text"] not in new_t][:5]
for j, a in enumerate(relocated, 1):
    holder = [p for p in links if a["text"] in added_per_file[p]]
    print("\n  (%d) old STATE.md:%d, %d chars — now in %s" % (j, a["lineno"], len(a["text"]),
                                                             ", ".join(holder) or "NOWHERE"))
    print("      %s" % a["text"][:600].replace("\n", " "))
L.row("of the five, present verbatim in a destination", sum(
    1 for a in relocated if any(a["text"] in added_per_file[p]
                                for p in links)),
      "the five relocated mathematical atoms printed above", "atoms, exact string")

print("\nB4 DONE")
