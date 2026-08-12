#!/usr/bin/env python3
"""mg-03cf — THE REGISTRY IS ITSELF A DOCUMENT FULL OF NUMBERS, SO IT IS SUBJECT TO THE DEFECT
IT REMEDIES.

`docs/FACTS.md` exists because a figure quoted away from the population that makes it true is
how `0/132` happened (STATE.md row 3b).  A registry whose OWN entries carried figures without
their frames would be that defect at scale, wearing the language of a fix.  So this arm asks
the registry the question the registry asks everyone else, mechanically:

    STRUCTURE   every entry carries all five declared fields -- STATEMENT, KIND, SCOPE, FROM,
                and either NOT or an explicit statement that no near-miss exists
    VOCABULARY  every KIND line names a mark from STATE.md:99's vocabulary, or says in words
                that it is WEAKER than FP.  An invented mark is a silent re-grading
    COUNT       the entry count in the file's own STATE.md pointer matches the entries here,
                because a pointer that drifts is how the registry stops being read
    LINKS       every relative link resolves on disk

WHAT THIS ARM DOES NOT DO, said here so its green is not over-read.  It cannot check that a
SCOPE line is TRUE, or that it is the RIGHT scope for its statement -- that is a reading of six
source documents and it was done by hand at mg-03cf, not by this file.  What it checks is that
no entry is missing the field, which is the failure mode that scales: an entry added in a hurry
six months from now with the number and without the population.

EXITS 0 if the registry is disciplined, 1 if it is not, 2 if it could not read the registry at
all -- 'could not tell' must not map onto 'nothing wrong'.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FACTS = os.path.join(ROOT, "docs", "FACTS.md")
STATE = os.path.join(ROOT, "STATE.md")

REQUIRED = ["STATEMENT", "KIND", "SCOPE", "FROM"]
KIND_MARKS = ["`U-id`", "`U`", "`FP✗`", "`FP`", "`OPEN`"]
WEAKER = "weaker than"


def entries(text):
    """Split on '## F<k> · <title>' headings; return [(id, title, body)]."""
    out = []
    parts = re.split(r"^## (F\d+) · (.+)$", text, flags=re.M)
    # parts = [preamble, id, title, body, id, title, body, ...]
    for i in range(1, len(parts), 3):
        out.append((parts[i], parts[i + 1].strip(), parts[i + 2]))
    return out


def main():
    print("=" * 88)
    print("mg-03cf  docs/FACTS.md asked its own question")
    print("=" * 88)
    print()

    for path in (FACTS, STATE):
        if not os.path.exists(path):
            print("REFUSED: %s does not exist, so this arm reached no decision about it."
                  % os.path.relpath(path, ROOT))
            print("VERDICT: REFUSED")
            return 2

    text = open(FACTS, encoding="utf-8").read()
    ents = entries(text)
    if not ents:
        print("REFUSED: no '## F<k> · ...' entry headings found -- either the registry is empty")
        print("or its heading convention changed and this arm is checking nothing.")
        print("VERDICT: REFUSED")
        return 2

    ok = True

    print("§1  STRUCTURE -- every entry carries every declared field")
    print("-" * 88)
    for (eid, title, body) in ents:
        missing = [f for f in REQUIRED if ("**%s.**" % f) not in body]
        has_not = "**NOT.**" in body or "no near-miss" in body.lower()
        if not has_not:
            missing.append("NOT")
        status = "PASS" if not missing else "FAIL  missing " + ", ".join(missing)
        ok &= not missing
        print("  %-5s %-58s %s" % (eid, title[:58], status))
    print()

    print("§2  VOCABULARY -- every KIND names a STATE.md:99 mark, or says WEAKER in words")
    print("-" * 88)
    for (eid, _title, body) in ents:
        m = re.search(r"\*\*KIND\.\*\*(.+?)(?:\n\n|\Z)", body, flags=re.S)
        line = m.group(1) if m else ""
        found = [k for k in KIND_MARKS if k in line]
        good = bool(found) or WEAKER in line
        ok &= good
        print("  %-5s %s   %s" % (eid, ("+".join(found) or ("(" + WEAKER + ")" if good else "NONE")),
                                  "PASS" if good else "FAIL  no recognised mark"))
    print()

    print("§3  COUNT -- STATE.md's pointer must not drift from the registry")
    print("-" * 88)
    # Anchored on the LINK, not on any wording: a pointer paragraph may be rewritten freely,
    # but it must exist and its count must not drift.  Anchoring on a date string would make
    # this row go red for an edit that changed nothing -- a wrong-direction control.
    state = open(STATE, encoding="utf-8").read()
    ptr = [ln for ln in state.splitlines() if "docs/FACTS.md" in ln]
    if not ptr:
        print("  FAIL  STATE.md does not link docs/FACTS.md at all -- the registry is")
        print("        unreachable from the canonical document, which is the whole gap it")
        print("        was filed to close.")
        ok = False
    else:
        m = re.search(r"(\d+) entries", " ".join(ptr))
        if not m:
            print("  FAIL  STATE.md links the registry but states no entry count, so drift")
            print("        between the two documents is undetectable.")
            ok = False
        else:
            claimed = int(m.group(1))
            good = claimed == len(ents)
            ok &= good
            print("  STATE.md claims %d entries; docs/FACTS.md has %d   [%s]"
                  % (claimed, len(ents), "PASS" if good else "FAIL"))
    print()

    print("§4  LINKS -- every relative link in the registry resolves on disk")
    print("-" * 88)
    bad = []
    for target in re.findall(r"\]\(([^)#][^)]*)\)", text):
        if target.startswith("http"):
            continue
        p = os.path.normpath(os.path.join(os.path.dirname(FACTS), target.split("#")[0]))
        if not os.path.exists(p):
            bad.append(target)
    ok &= not bad
    print("  %d relative links checked, %d broken   [%s]"
          % (len(re.findall(r"\]\(([^)#][^)]*)\)", text)), len(bad), "PASS" if not bad else "FAIL"))
    for b in bad:
        print("    BROKEN  %s" % b)
    print()

    print("§5  THE POSITIVE CONTROL -- this arm is shown able to fail")
    print("-" * 88)
    planted = text.replace("**SCOPE.**", "**Scope-ish.**", 1)
    pe = entries(planted)
    caught = any("**SCOPE.**" not in b for (_i, _t, b) in pe)
    ok &= caught
    print("  an entry with its SCOPE field renamed is [%s]"
          % ("CAUGHT" if caught else "MISSED -- this arm cannot fire and its green means nothing"))
    planted2 = re.sub(r"\*\*KIND\.\*\* `U` —", "**KIND.** `probably` —", text, count=1)
    pe2 = entries(planted2)
    caught2 = False
    for (_i, _t, b) in pe2:
        m = re.search(r"\*\*KIND\.\*\*(.+?)(?:\n\n|\Z)", b, flags=re.S)
        if m and not any(k in m.group(1) for k in KIND_MARKS) and WEAKER not in m.group(1):
            caught2 = True
    ok &= caught2
    print("  an entry graded with an invented mark is [%s]"
          % ("CAUGHT" if caught2 else "MISSED -- the vocabulary check is decorative"))
    print()

    print("VERDICT: %s — %d entries" % ("GREEN" if ok else "RED", len(ents)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
