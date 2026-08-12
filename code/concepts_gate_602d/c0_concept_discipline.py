#!/usr/bin/env python3
"""mg-602d — A CONCEPTUAL DOCUMENT IS THE EASIEST PLACE IN THE ESTATE TO ACCUMULATE CONFIDENT
PROSE THAT NO LONGER MATCHES THE FORMAL RECORD, SO IT IS SUBJECT TO THE DEFECT IT REMEDIES.

`docs/CONCEPTS.md` exists because the formal record was complete and the conceptual one did not
exist -- Daniel asked "what is alpha?" about a quantity central to four work items, and nobody
had written down what it MEANS.  The obvious way for the fix to fail is not that it goes unread:
it is that it drifts.  Prose about meaning has no population attached and no arithmetic to
check, so a sentence that was true when written stays readable forever after the row that earned
it has moved, and the file becomes a confident account of a programme that no longer exists.

The ticket's own answer to that is two rules, and this arm checks them MECHANICALLY:

    POINTERS  every row of the quantities table (S2) and of the killed-intuitions table (S5)
              carries a pointer -- an `mg-XXXX`, a ledger row, or a link into STATE.md/FACTS.md
              -- in its last column.  A conceptual claim that points at nothing is the failure.
    MARKERS   every item of the beliefs section (S6) says `BELIEF` IN THE ITEM, not in a
              footnote.  An unearned claim that reads like an earned one is the whole hazard.
    LENGTH    the file stays under a declared word ceiling.  "Succinct is a requirement, not a
              style note" is the ticket's phrasing: a long conceptual document is not re-read,
              and a conceptual document that is not re-read decays into a second STATE.md.
    LINKS     every relative link resolves on disk.
    FINDABLE  STATE.md links to it.  A document nobody links to from the canonical file is
              exactly as findable as the several arcs it was built to consolidate -- i.e. it
              would land, be unread, and the ticket's gap would be intact with an extra file in
              it.  docs/FACTS.md's own housekeeping section makes this same argument about
              itself, and it is the same argument here.

WHAT THIS ARM DOES NOT DO, said here so its green is not over-read.  It CANNOT CHECK THAT A
POINTER IS CORRECT -- that the item cited says what the row claims it says.  That is a reading of
a dozen documents and it was done by hand at mg-602d, not by this file.  What it checks is that a
pointer is THERE, which is the failure mode that scales: a row added in a hurry six months from
now with the intuition and without the artifact.  The gate is on STRUCTURE, not on truth, exactly
as code/facts_registry_03cf/f0_registry_discipline.py is and for the same stated reason.

A SECOND LIMIT, and it is the sharper one.  The sections are located by ANCHOR PHRASES in their
headings.  If a heading is reworded the anchor is not found and this arm REFUSES (exit 2) rather
than passing -- a rename must be LOUD.  It cannot be silent-green, because a gate that quietly
stops checking is worse than no gate: it is a gate people believe in.

EXITS 0 if the document is disciplined, 1 if it is not, 2 if it could not reach a decision at
all -- 'could not tell' must not map onto 'nothing wrong'.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONCEPTS = os.path.join(ROOT, "docs", "CONCEPTS.md")
STATE = os.path.join(ROOT, "STATE.md")

# --- THE WORD CEILING, AND WHY THE NUMBER IS HERE -----------------------------------------
# 3,200 words.  The file stands at 2,989 at mg-602d, so the headroom is ~7% -- enough that
# ordinary editing does not demand a config change, and not enough that the file can double
# without anyone deciding to let it.
#
# This is NOT STATE.md's ratchet and deliberately does not copy it.  That one is a MONOTONE
# FLOOR under a regression, with a banking rule, because STATE.md's problem is unbanked cuts
# (code/state_ratchet_e331/CEILING.json records two that were 78% and 59% undone).  This one is
# a plain CAP, because CONCEPTS.md's problem is the opposite: nothing here needs to shrink, and
# the only thing that must not happen is silent growth into a second STATE.md.  Raising it is
# allowed and is one edit -- move the number, and say in the commit what the words are and why
# they could not be a citation instead.  The distinction matters because "cite, do not restate"
# is the file's own first rule, and almost every honest reason to grow it is a reason to cite.
WORDS_CEILING = 3200

# Section anchors: (label, phrase that must appear in a '## ' heading).
S_QUANTITIES = ("S2 quantities", "what each one MEANS")
S_KILLED = ("S5 killed intuitions", "Intuitions that have been killed")
S_BELIEFS = ("S6 beliefs", "What we believe and cannot prove")

# A pointer is an item id, a ledger row, or a link into the two formal documents.
POINTER_RE = re.compile(r"mg-[0-9a-f]{4}|STATE\.md|FACTS\.md|\brows? \d")

LINK_RE = re.compile(r"\]\((?!https?:)([^)#]+)")


def fail(msgs, text):
    msgs.append(text)
    print("    FIRED: " + text)


def section(text, phrase):
    """Body of the '## ' section whose heading contains `phrase`, or None."""
    parts = re.split(r"^(## .+)$", text, flags=re.M)
    for i in range(1, len(parts), 2):
        if phrase in parts[i]:
            return parts[i + 1]
    return None


def table_rows(body):
    """Data rows of every markdown table in `body`, as lists of stripped cells."""
    rows = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|") or not line.endswith("|"):
            continue
        cells = [c.strip() for c in line[1:-1].split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
            continue  # the |---|---| separator
        rows.append(cells)
    return rows[1:] if rows else []  # drop the header row


def main():
    print("=" * 88)
    print("mg-602d  docs/CONCEPTS.md asked its own two rules")
    print("=" * 88)
    print()

    for path in (CONCEPTS, STATE):
        if not os.path.exists(path):
            print("REFUSED: %s does not exist, so this arm reached no decision about it."
                  % os.path.relpath(path, ROOT))
            return 2

    text = open(CONCEPTS, encoding="utf-8").read()
    fired = []

    # --- the three sections must be locatable, or this arm refuses -------------------------
    print("ANCHORS  -- a reworded heading REFUSES rather than passing")
    bodies = {}
    missing = False
    for label, phrase in (S_QUANTITIES, S_KILLED, S_BELIEFS):
        body = section(text, phrase)
        bodies[label] = body
        print("    %-22s %s" % (label, "found" if body is not None else "NOT FOUND"))
        if body is None:
            missing = True
    if missing:
        print()
        print("REFUSED: a section anchor is missing.  Either a heading was reworded -- in which")
        print("         case fix the anchor in this file IN THE SAME COMMIT -- or a section was")
        print("         deleted, in which case the rule it carried is gone and that is the")
        print("         finding.  This arm does not decide which, and does not pass either.")
        return 2
    print()

    # --- POINTERS -------------------------------------------------------------------------
    print("POINTERS -- every claim row carries the artifact that earns it")
    for label in (S_QUANTITIES[0], S_KILLED[0]):
        rows = table_rows(bodies[label])
        if not rows:
            fail(fired, "%s: no table rows found at all" % label)
            continue
        bad = 0
        for cells in rows:
            subject = cells[0][:48] if cells else "(empty row)"
            if len(cells) < 3:
                fail(fired, "%s: row %r has %d columns, expected 3"
                     % (label, subject, len(cells)))
                bad += 1
            elif not POINTER_RE.search(cells[-1]):
                fail(fired, "%s: row %r has no pointer in its last column (%r)"
                     % (label, subject, cells[-1][:60]))
                bad += 1
        print("    %-22s %d rows, %d without a pointer" % (label, len(rows), bad))
    print()

    # --- MARKERS --------------------------------------------------------------------------
    print("MARKERS  -- every unearned claim says BELIEF in the item, not in a footnote")
    bullets = [ln for ln in bodies[S_BELIEFS[0]].splitlines() if ln.startswith("- ")]
    if not bullets:
        fail(fired, "S6 beliefs: no items found at all")
    bad = 0
    for ln in bullets:
        if "BELIEF" not in ln:
            fail(fired, "S6 beliefs: item %r is not marked BELIEF" % ln[2:50])
            bad += 1
    print("    %-22s %d items, %d unmarked" % ("S6 beliefs", len(bullets), bad))
    print()

    # --- LENGTH ---------------------------------------------------------------------------
    words = len(text.split())
    print("LENGTH   -- succinct is a requirement, not a style note")
    print("    %-22s %d words against a ceiling of %d" % ("docs/CONCEPTS.md", words,
                                                          WORDS_CEILING))
    if words > WORDS_CEILING:
        fail(fired, "the file is %d words over its declared ceiling.  Cite instead of "
                    "restating, or raise WORDS_CEILING in this file in the same commit and say "
                    "why the words could not be a citation." % (words - WORDS_CEILING))
    print()

    # --- LINKS ----------------------------------------------------------------------------
    print("LINKS    -- every relative link resolves on disk")
    targets = sorted(set(LINK_RE.findall(text)))
    bad = 0
    for t in targets:
        if not os.path.exists(os.path.join(os.path.dirname(CONCEPTS), t)):
            fail(fired, "dead relative link: %s" % t)
            bad += 1
    print("    %-22s %d relative links, %d dead" % ("docs/CONCEPTS.md", len(targets), bad))
    print()

    # --- FINDABLE -------------------------------------------------------------------------
    print("FINDABLE -- STATE.md links to it, or nobody arrives")
    state = open(STATE, encoding="utf-8").read()
    linked = "docs/CONCEPTS.md" in state
    print("    %-22s %s" % ("STATE.md pointer", "present" if linked else "ABSENT"))
    if not linked:
        fail(fired, "STATE.md does not link to docs/CONCEPTS.md.  A pointer is only "
                    "discoverable at the site the reader already reads.")
    print()

    print("-" * 88)
    if fired:
        print("VERDICT: %d finding(s).  The document is not disciplined as it stands." % len(fired))
        return 1
    print("VERDICT: green.  Every claim row points somewhere, every belief is marked as one,")
    print("         the file is inside its ceiling, and it is reachable from STATE.md.")
    print("         THIS SAYS NOTHING ABOUT WHETHER ANY POINTER IS CORRECT.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
