#!/usr/bin/env python3
"""mg-5644 — B2: THE L0 PROBES ARE FOUR FIXTURES SOMEBODY CHOSE, PUBLISHED AS A RULE.

BEYOND-BRIEF MATERIAL, AUDITED FIRST.  mg-bee1's brief has five acceptance items: repair the
statement, decide the mechanism on its merits, re-run mg-218d's sixteen unmodified, do not
over-correct, name the uncontrolled layer.  Section 0 of delta_control.py — `NORM_RULE` and
`norm_rule_probes()` — is none of them.  It is mg-bee1's own addition, closing mg-218d's I2.
Roughly seven consecutive generations of this arc have put their worst finding in
beyond-brief work, because unbriefed work has no acceptance criteria and so nothing tests it.

THE CLAIMS UNDER TEST, quoted:

    delta_control.py, section 0's header:
        "These probes are the rule as an assertion: each one is a sentence of the docstring
         above, and each fails if the code stops meaning it.  They are BEHAVIOURAL, not
         textual, so they FIRE ON A WIDENED EDGE CONSTANT exactly as on a widened strip()
         call."
        "It raises one specific silent divergence — the code drifting from its own published
         rule — FROM FREE TO TWO EDITS, and that is the whole claim."

    COVERAGE.md, "The normalisation, as an assertion rather than only as prose":
        "the four sentences above become four probes, so a widened `strip()` call *or* a
         widened `EDGE` constant IS A NON-ZERO EXIT."

THE PUBLISHED RULE, quoted from the same docstring, is the standard both are measured against:

    N(region) = the region's characters with ASCII SPACE, TAB, CR and LF removed from the
                TWO ENDS of the whole region — NOTHING ELSE — encoded UTF-8.

THE ARITHMETIC.  `str.strip()` removes every character for which `str.isspace()` is true.
There are 29 of them.  The published rule admits 4.  So there are 25 characters whose
appearance in EDGE makes the code stop meaning its own published rule.  The four probes
name TWO of them — U+00A0 and U+2028.  The remaining 23 can be added to EDGE, one edit,
and every probe still passes.

mg-bee1's own battery row I3 is "the EDGE constant widened, norm() untouched", and the
character it widens EDGE with is U+00A0 — the character probe 2 is built around.  It is a
positive control presented as the general claim.  It is E2 below.

This is generation 2's defect — author-chosen substrings at the MUTATION SET — inside the
repair of generation 5's defect, which was a universally quantified sentence over a
mechanism quantified on a chosen subset.  Both, in the same file, in the same commit.
"""
import subprocess
import sys

import harness5644 as H

CONTROL = H.CONTROL
EDGE_LINE = 'EDGE = " \\t\\r\\n"'
NORM_LINE = 'return text.strip(EDGE).encode("utf-8")'

PUBLISHED = " \t\r\n"
ALL_WS = [chr(c) for c in range(0x110000) if chr(c).isspace()]
PROBED = "  "
UNPROBED = [c for c in ALL_WS if c not in PUBLISHED and c not in PROBED]


def _esc(chars):
    return "".join("\\u%04x" % ord(c) for c in chars)


def _widen_edge(t, chars):
    txt = t[CONTROL]
    if txt.count(EDGE_LINE) != 1:
        raise LookupError("EDGE does not read as published")
    return {CONTROL: txt.replace(EDGE_LINE, 'EDGE = " \\t\\r\\n" + "%s"' % _esc(chars), 1)}


def _rewrite_norm(t, expr):
    txt = t[CONTROL]
    if txt.count(NORM_LINE) != 1:
        raise LookupError("norm() does not read as published")
    return {CONTROL: txt.replace(NORM_LINE, expr, 1)}


ROWS = [
    ("E1", "L0 published rule",
     f"EDGE widened by the {len(UNPROBED)} whitespace chars no probe names",
     0, lambda t: _widen_edge(t, UNPROBED)),
    ("E2", "L0 published rule", "EDGE widened by U+00A0 (mg-bee1's I3, restated)",
     H.FAIL, lambda t: _widen_edge(t, " ")),
    ("E3", "L0 published rule", "EDGE widened by U+2028 (probe 3's own character)",
     H.FAIL, lambda t: _widen_edge(t, " ")),
    ("E4", "L0 published rule", "EDGE widened by U+000C alone (FORM FEED, unprobed)",
     0, lambda t: _widen_edge(t, "")),
    ("E5", "L0 published rule", "EDGE widened by U+2003 alone (EM SPACE, unprobed)",
     0, lambda t: _widen_edge(t, " ")),
    ("E6", "L0 'nothing INTERIOR'", "norm() gains an interior .replace(U+200B, '')",
     0, lambda t: _rewrite_norm(
         t, 'return text.strip(EDGE).replace("\\u200b", "").encode("utf-8")')),
    ("E7", "L0 'nothing INTERIOR'", "norm() gains an interior .replace(U+00A0, ' ') (positive)",
     H.FAIL, lambda t: _rewrite_norm(
         t, 'return text.strip(EDGE).replace("\\u00a0", " ").encode("utf-8")')),
    ("E8", "L0 published rule", "norm() widened to a bare .strip() (mg-218d's I2, restated)",
     H.FAIL, lambda t: _rewrite_norm(t, 'return text.strip().encode("utf-8")')),
]


def sweep_every_character(tree):
    """The population, not a sample: EVERY character str.strip() removes and the rule does
    not, added to EDGE one at a time, with the control's exit code for each."""
    fired, silent = [], []
    for c in sorted(set(ALL_WS) - set(PUBLISHED), key=ord):
        code = tree.run_mutated(_widen_edge(tree.orig, c))
        (fired if code else silent).append((c, code))
    return fired, silent


def main():
    tree = H.Tree([CONTROL])
    print(f"THE POPULATION.  str.strip() removes {len(ALL_WS)} characters; the published "
          f"rule admits {len(PUBLISHED)};")
    print(f"so {len(ALL_WS) - len(PUBLISHED)} characters in EDGE make the code stop meaning "
          f"its own rule.  The probes name {len(PROBED)}.")
    print()

    tree.battery(ROWS, "mg-5644 — B2: EIGHT MUTATIONS AT THE L0 PROBES")

    print("=" * 90)
    print("THE SWEEP — every character, not a sample")
    print("=" * 90)
    print(f"  Each of the {len(ALL_WS) - len(PUBLISHED)} characters above added to EDGE on "
          f"its own, one full run of the control each.")
    fired, silent = sweep_every_character(tree)
    total = len(fired) + len(silent)
    print(f"  population {total}; {len(fired)} fire; {len(silent)} exit 0")
    print(f"  FIRE   ({len(fired)}): " + " ".join("U+%04X" % ord(c) for c, _ in fired))
    print(f"  SILENT ({len(silent)}): " + " ".join("U+%04X" % ord(c) for c, _ in silent))
    print()
    print("  The two that fire are the two the probes name.  The other "
          f"{len(silent)} are one edit each.")
    print()
    print("=" * 90)
    print("THE VERDICT ON THE TWO PUBLISHED SENTENCES")
    print("=" * 90)
    print("  'they fire on a widened EDGE constant exactly as on a widened strip() call'")
    print(f"      — FALSE for {len(silent)} of {total} widenings.  True for {len(fired)}:")
    print("        the two the probe list was built around.")
    print("  'raises ... the code drifting from its own published rule, from free to two edits'")
    print("      — FALSE.  E1, E4, E5, E6 and every row of the sweep's silent list are ONE")
    print("        edit, and the probes are left in place and passing.")
    print()
    print("  WHAT IS TRUE, and this audit does not retract it: mg-218d's I2 — the widening")
    print("  to a bare str.strip() — DOES now fire (E8), because a bare strip() eats U+00A0")
    print("  and U+2028 and probes 2 and 3 are built from exactly those.  The specific")
    print("  divergence mg-218d found is closed.  The RULE is not asserted, and the two")
    print("  sentences above say it is.")
    print()
    print("  This is not a certification-of-the-instrument complaint.  delta_control.py's")
    print("  'nothing certifies the instrument' caveat is correct and is not the issue: it")
    print("  covers an edit that deletes the probes.  Every row above LEAVES THE PROBES IN")
    print("  PLACE AND PASSING, which is the case the caveat says is covered.")
    print("=" * 90)
    return 0


if __name__ == "__main__":
    sys.exit(main())
