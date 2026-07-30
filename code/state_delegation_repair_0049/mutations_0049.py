#!/usr/bin/env python3
"""mg-0049 — THE NINE MUTATIONS, defined once and read by two scripts.

Every one of them edits ONLY `docs/state-history/attempt-mg-276d.md` — the file the
certified ledger cell POINTS AT, which is the surface mg-bee1's repair created and left
uncontrolled.  Not one of them touches STATE.md, the state-history README or the
instrument.  That is the point: the whole of mg-5644's B1 is that a reader can be shown
NOTHING while every byte this instrument certifies is exactly the byte it certified.

WHY ONE MODULE AND TWO READERS.  `battery_0049.py` writes each mutation into the working
tree and runs the real control as a subprocess, reading its EXIT CODE from the process.
`split_0049.py` applies the SAME functions to a string in memory and asks which MECHANISM
would have fired — the section-8 guards, the presentation record, or the content digest —
so the claim "the guards alone would have closed R1 and not R2" is measured rather than
argued.  Sharing the mutations is what makes the two runs comparable; if they were written
twice they would be two populations and the comparison would be worthless.

EVERY ROW CARRIES THE EXIT CODE PREDICTED BEFORE THE RUN.  That discipline is mg-218d's,
kept by mg-bee1 and by mg-5644, and kept here: the `want` column below was written into
this file and committed to before `battery_0049.py` was executed for the first time.
"""
import os
import subprocess

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()

ATTEMPT = "docs/state-history/attempt-mg-276d.md"

FAIL, MOVED = 1, 2

# The two anchors the mutations key on, checked before use so a rot in the target file is a
# loud LookupError and not a silently inert mutation.  Same locator discipline as the
# instrument's: by content, never by line number.
_H1_HEAD = "### H1 — the step-4d clause — first of the three A3 sites"
_H3_HEAD = "### H3 — the all-+1 invariance theorem, and the repair of its citation"
_OPENING = "Every passage below was **moved verbatim** out of that cell."


def _once(text, needle):
    if text.count(needle) != 1:
        raise LookupError(f"{needle!r} matched {text.count(needle)} times, need exactly 1")
    return text


def original():
    with open(os.path.join(REPO, ATTEMPT), "r", encoding="utf-8") as fh:
        return fh.read()


# --- R1 / R2 — mg-5644's Q1 and Q2 verbatim: the two mutations mg-4acd exists to catch ----
def r1_html_commented(t):
    """One `<!--` line at the top, never closed: a reader is shown NOTHING of the file."""
    return "<!--\n" + t


def r2_fenced(t):
    """One ``` line at the top, never closed: the whole file renders as a code sample."""
    return "```\n" + t


# --- R3 / R4 — the bound, RE-MEASURED here rather than inherited from mg-5644 -------------
def r3_retraction_at_top(t):
    """Text a reader IS shown, outside every cited section.  Outside coverage, and said to
    be: the claim is about the sections a citation lands on, not the page they sit in."""
    return "**RETRACTED — everything below is void.**\n\n" + t


def r4_uncited_section_appended(t):
    return t + "\n### H9 — a section nothing cites\n\nText.\n"


# --- R5 — a wrapper that suppresses NOTHING, caught by the guard and by no record ---------
def r5_details_wrapper(t):
    """`<details>` at the top of the target: every cited section still renders, so no
    presentation record moves.  The raw-HTML guard is the only thing that sees it, which is
    why extending the guards was necessary and not merely tidy."""
    return "<details>\n\n" + t


# --- R6 — mg-babf's B04 shape, one file out: the section moved under a void heading -------
def r6_appendix_heading_above_h1(t):
    """A `## Appendix Z` heading immediately above the first cited section.  No cited
    section's bytes move — every one of them begins at its own `###` — and every cited
    section's HEADING PATH now runs through "nothing below is in force"."""
    _once(t, _H1_HEAD)
    return t.replace(_H1_HEAD,
                     "## Appendix Z — superseded drafts; nothing below is in force\n\n"
                     + _H1_HEAD, 1)


# --- R7 — positive control: the pre-existing delegated-content mechanism still fires ------
def r7_cited_section_deleted(t):
    """H3 removed outright.  mg-bee1's T1 shape, re-run to show this repair did not weaken
    what it inherited."""
    _once(t, _H3_HEAD)
    lines = t.split("\n")
    i = lines.index(_H3_HEAD)
    j = i + 1
    while j < len(lines) and not lines[j].startswith("#"):
        j += 1
    return "\n".join(lines[:i] + lines[j:])


# --- R8 — the same blank page by a CLOSED comment, so the catch is not about closure ------
def r8_whole_file_commented_closed(t):
    """`<!--` first line, `-->` last: a well-formed comment around the whole document.  A
    reader is shown a blank page exactly as in R1, and no cited section's bytes move."""
    return "<!--\n" + t + "\n-->\n"


# --- R9 — the running cost of default-deny, on the new surface, measured not asserted -----
def r9_tab_in_uncited_prose(t):
    """A single tab in the target's OPENING PARAGRAPH — uncited text, no cited section's
    bytes, no cited section's presentation.  The section-8 guards read the whole file, so
    they fire.  This is the cost the two certified files already pay, now paid by the
    target too, and it is a row here rather than a sentence because a cost that is only
    asserted is a cost nobody has measured."""
    _once(t, _OPENING)
    return t.replace(_OPENING, _OPENING.replace("was **moved", "was\t**moved"), 1)


ROWS = [
    ("R1", "L4 on L1's surface", "the cited file HTML-commented whole (reader sees nothing)",
     FAIL, r1_html_commented),
    ("R2", "L4 on L1's surface", "the cited file fenced whole (renders as a code sample)",
     FAIL, r2_fenced),
    ("R3", "L1 stated boundary", "a retraction at the TOP of the target",
     0, r3_retraction_at_top),
    ("R4", "L1 stated boundary", "a new UNCITED section appended to the target",
     0, r4_uncited_section_appended),
    ("R5", "L4 guard only", "a <details> wrapper: suppresses nothing, is raw HTML",
     MOVED, r5_details_wrapper),
    ("R6", "L4 heading path", "the cited sections moved under an 'Appendix Z' heading",
     MOVED, r6_appendix_heading_above_h1),
    ("R7", "L1 delegated content", "a cited section DELETED (positive control)",
     FAIL, r7_cited_section_deleted),
    ("R8", "L4 on L1's surface", "the whole file inside a CLOSED HTML comment",
     FAIL, r8_whole_file_commented_closed),
    ("R9", "L4 guard, cost row", "one TAB in the target's uncited opening paragraph",
     MOVED, r9_tab_in_uncited_prose),
]
