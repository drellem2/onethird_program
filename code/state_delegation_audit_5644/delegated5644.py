#!/usr/bin/env python3
"""mg-5644 — B1: THE DELEGATED SURFACE HAS A CONTENT DIGEST AND NO PRESENTATION RECORD.

THE CLAIM UNDER TEST, quoted from the party under test:

    COVERAGE.md, the layer table:
        | L1 what a region points at | ... | **closed for cited sections** (T1 T2 T3).
          The target's own framing is not |
    code/state_delegation_repair_bee1/README.md, the layer table:
        | L1 what a region points at | **closed for cited sections** (T1 T2 T3 D1 D2 D3).
          The target's uncited sections and its own framing are not (D4 D5) |

Both state the BOUND of the new delegation in terms of WHICH SECTIONS are followed — cited
versus uncited.  Neither states it in terms of WHETHER A READER IS SHOWN THEM.

That distinction is the whole content of mg-babf's B1 and of mg-4acd's repair.  mg-7870 put
a CONTENT digest on each certified region; mg-babf got four mutations past it that changed
no certified byte, by changing whether a reader is shown the region at all; mg-4acd answered
with a PRESENTATION RECORD per certified region, and mg-218d verified it against two real
GFM renderers.

mg-bee1 created a NEW REGION SET — five sections of docs/state-history/attempt-mg-276d.md,
digested under the same N — and gave it a content digest and NO presentation record.  Its
own docstring records that, factually, in the coverage list:

    DELEGATED (mg-bee1), digested under the same N but NOT carrying a presentation record

and nowhere says what it costs.  So the question this file asks is mg-babf's question, put
to the surface mg-bee1 just built: CAN A READER BE SHOWN NOTHING OF A CITED SECTION WHILE
EVERY CITED SECTION'S DIGEST STILL MATCHES?

Q1 and Q2 are mg-babf's B06 and B05 — the HTML comment and the code fence, the two
mutations mg-4acd exists to catch — moved one file out, onto the delegated target.  They
need ONE LINE at the top of a file that is outside both certified files, and they change no
byte of any cited section, because every cited section begins at its own `###` heading and
the mutation is above the first one.

Q3 and Q4 are mg-bee1's STATED bound (its D5 and D4) restated in this harness rather than
inherited from its battery, so the bound is measured here too and not taken on trust.
Q5 and Q6 are positive controls: the delegation mechanism itself works, and this audit is
not reporting an inert layer.
"""
import sys

import harness5644 as H

ATTEMPT = H.ATTEMPT


# --- Q1 / Q2 — mg-babf's B06 and B05, on the delegated surface ----------------------------
# CommonMark: an HTML block begun by `<!--` runs until a line containing `-->`; with none in
# the file it runs to the end of the document.  A fenced code block begun by ``` runs to a
# closing fence or, with none, to the end of its container.  So one line at the top of the
# target puts EVERY cited section inside a container, and no cited section's bytes move.

def q1_target_html_commented(t):
    """One `<!--` line at the top, never closed: a reader is shown NOTHING of the file."""
    return {ATTEMPT: "<!--\n" + t[ATTEMPT]}


def q2_target_fenced(t):
    """One ``` line at the top, never closed: the whole file renders as a code sample."""
    return {ATTEMPT: "```\n" + t[ATTEMPT]}


# --- Q3 / Q4 — mg-bee1's stated bound, measured here rather than inherited ----------------

def q3_retraction_at_top(t):
    return {ATTEMPT: "**RETRACTED — everything below is void.**\n\n" + t[ATTEMPT]}


def q4_uncited_section_added(t):
    return {ATTEMPT: t[ATTEMPT] + "\n### H9 — a section nothing cites\n\nText.\n"}


# --- Q5 / Q6 — positive controls: the mechanism is not inert ------------------------------

def q5_cited_heading_retitled(t):
    old = "### H3 — the all-+1"
    txt = t[ATTEMPT]
    if txt.count(old) != 1:
        raise LookupError("H3's heading does not read as published")
    return {ATTEMPT: txt.replace(old, "### H3zz — the all-+1", 1)}


def q6_cited_body_inverted(t):
    old = "### H3 — the all-+1 invariance theorem, and the repair of its citation\n"
    txt = t[ATTEMPT]
    if txt.count(old) != 1:
        raise LookupError("H3's heading does not read as published")
    return {ATTEMPT: txt.replace(
        old, old + "\n**THIS IS RETRACTED AND WAS NEVER PROVED.**\n", 1)}


ROWS = [
    ("Q1", "L4 on L1's surface", "the cited file HTML-commented whole (reader sees nothing)",
     0, q1_target_html_commented),
    ("Q2", "L4 on L1's surface", "the cited file fenced whole (renders as a code sample)",
     0, q2_target_fenced),
    ("Q3", "L1 stated boundary", "a retraction at the TOP of the target",
     0, q3_retraction_at_top),
    ("Q4", "L1 stated boundary", "a new UNCITED section appended to the target",
     0, q4_uncited_section_added),
    ("Q5", "L1 delegated content", "a cited section's HEADING retitled (positive control)",
     H.FAIL, q5_cited_heading_retitled),
    ("Q6", "L1 delegated content", "a contradiction inserted INSIDE cited H3 (positive)",
     H.MOVED, q6_cited_body_inverted),
]


def main():
    tree = H.Tree([ATTEMPT])
    got = tree.battery(
        ROWS,
        "mg-5644 — B1: SIX MUTATIONS ON THE SURFACE mg-bee1 CREATED",
        "Q1 and Q2 are mg-babf's B06 and B05 — HTML comment, code fence — moved one file "
        "out onto\nthe delegated target.  Q5 and Q6 are positive controls.")

    print("=" * 90)
    print("WHAT Q1 AND Q2 MEAN")
    print("=" * 90)
    print("  Both exit 0.  In both, every one of the five sections the certified ledger cell")
    print("  cites BY NAME is byte-identical and every delegated digest matches, and a reader")
    print("  who follows any of the cell's six links is shown a blank page (Q1) or a wall of")
    print("  unrendered source (Q2).  That is exactly the state mg-babf's B05/B06 put the F1")
    print("  block into while the control said PASS — the state mg-4acd was filed to close.")
    print()
    print("  It is closed for the two files this instrument READS: section 8's default-deny")
    print("  guards report raw HTML in prose and unmodelled block constructs over the whole")
    print("  of STATE.md and the state-history README, so neither Q1 nor Q2 has an analogue")
    print("  there.  The delegated target gets neither guard, and neither does any other")
    print("  file a certified region may come to cite.")
    print()
    print("  So 'closed for cited sections' is FALSE AS STATED, in the same shape as the")
    print("  sentence mg-bee1 was filed to repair: the claim is quantified over cited")
    print("  sections and the mechanism is quantified over their BYTES.")
    print()

    bad = [r for r in ("Q1", "Q2") if got[r] != 0]
    if bad:
        print(f"  NOTE: {bad} did NOT exit 0 — this finding does not reproduce; read the rows.")
    print("=" * 90)
    return 0


if __name__ == "__main__":
    sys.exit(main())
