#!/usr/bin/env python3
"""
mg-1953 REPAIR instrument -- NEGATIVE CONTROL FOR THE DOCUMENT DIRECTION.

document_figures.py is a new guard, so it owes evidence that it can FAIL --
this repo's standing criterion, code/hodge_leverage_audit_86a3/
audit_controls.py:4: "a control must be able to FAIL on the construction it
guards".  A guard whose only evidence is that it currently passes is exactly
the defect mg-3b51's A1 found one level up.

THE BATTERY IS NOT A CHOSEN LIST.  mg-2216's finding against bf17716 was that
a control certified by a list of mutations its own author picked will be blind
to the ones they did not think of.  So this enumerates the mutations
MECHANICALLY and EXHAUSTIVELY over the stated coverage: for every figure in
FIGURES, and for every captured number within it,

  (1) DIGIT MUTATION -- rewrite that number's last digit (d -> (d+1) % 10),
      preserving digit count and spacing so the regex still matches and only
      the VALUE changes.  The guard must report a different value.
  (2) EXCISION -- delete the whole matched span, as a rewrite of the sentence
      would.  The guard must report NOT FOUND.

Every number under the coverage boundary is therefore attacked, not a sample.
What is NOT attacked is what is not covered: prose, status words, attributions
and any figure not listed in FIGURES.  That boundary is stated, not hidden --
it is the same posture as code/state_landing_control_2da3/COVERAGE.md.

Exits non-zero if any mutation passes silently.
"""

import re
import sys

import document_figures


def bump(text):
    """Change the last digit, preserving length and spacing."""
    i = max(idx for idx, ch in enumerate(text) if ch.isdigit())
    return text[:i] + str((int(text[i]) + 1) % 10) + text[i + 1:]


def main():
    doc = document_figures.read()
    base = document_figures.extract(doc)

    missing = [n for n, v in base.items() if v is None]
    if missing:
        print("BASELINE BROKEN -- these figures are not in the document:")
        for n in missing:
            print("   %s" % n)
        return 1

    caught = missed = 0
    for name, where, pattern in document_figures.FIGURES:
        m = re.search(pattern, doc, re.DOTALL)
        span = doc[m.start():m.end()]

        # (2) EXCISION.
        mutated = doc[:m.start()] + doc[m.end():]
        got = document_figures.extract(mutated).get(name)
        ok = got is None
        caught, missed = (caught + 1, missed) if ok else (caught, missed + 1)
        print("  %-42s %-14s %s"
              % (name, "excision", "CAUGHT (not found)" if ok
                 else "MISSED -- still reports %s" % (got,)))

        # (1) DIGIT MUTATION, one per captured number.
        for g in range(1, m.re.groups + 1):
            original = m.group(g)
            lo = m.start(g) - m.start()
            hi = m.end(g) - m.start()
            mutated_span = span[:lo] + bump(original) + span[hi:]
            mutated = doc[:m.start()] + mutated_span + doc[m.end():]
            got = document_figures.extract(mutated).get(name)
            ok = got != base[name]
            caught, missed = (caught + 1, missed) if ok else (caught, missed + 1)
            print("  %-42s %-14s %s"
                  % (name, "group %d" % g,
                     "CAUGHT (%s -> %s)" % (base[name][g - 1],
                                            got[g - 1] if got else None)
                     if ok else "MISSED -- %r changed and nothing moved"
                     % (original,)))

    print()
    print("%d mutations, %d CAUGHT, %d MISSED" % (caught + missed, caught, missed))
    if missed:
        print("NEGATIVE CONTROL FAILED -- the guard is blind to %d of its own"
              " covered figures" % missed)
        return 1
    print("NEGATIVE CONTROL PASSED -- every number under the stated coverage")
    print("boundary, and every sentence carrying one, is guarded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
