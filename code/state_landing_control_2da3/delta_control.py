#!/usr/bin/env python3
"""mg-2da3 — a WORKING-TREE control for b68db5d's delta (mg-7735's landing).

    mg-7870: THE CERTIFYING MECHANISM IS NOW A CONTENT DIGEST, NOT A LIST OF SUBSTRINGS.
    See "WHY THE MECHANISM CHANGED" and "COVERAGE" below.  The substring checks are still
    here; they no longer carry the certification.

    mg-4acd: EACH REGION NOW CARRIES A SECOND DIGEST, OF WHAT A READER SEES.  The content
    digest answers "are these the certified bytes?".  It does not answer "is anybody shown
    them?", and mg-babf got four mutations past it on exactly that gap — including this
    file's own certified F1 block HTML-commented out of the rendered page.  See "WHAT A
    READER SEES" below.

WHY THIS EXISTS.  b68db5d's headline evidence sentence is

    "I re-ran both: `sh code/state_audit_6a2f/run_all.sh` reproduces out_audit.txt
     BYTE-IDENTICALLY with these edits applied."

Every script in that battery pins fixed revisions (97cb533 / 60f4dac / 57f962f) and reads
the committed docs/state-history/*.md at 57f962f.  Not one of them opens the working tree
or resolves HEAD.  So the sentence is TRUE and carries NO INFORMATION about the edits:
mg-bd41 gutted STATE.md from 175,552 to 37,958 bytes and the battery still emitted the
identical 96,291 bytes.  The battery is not wrong — reproducing an audit of a specific
historical state is exactly what mg-6a2f built it to do, and pinning is a FEATURE there.
What was wrong was re-running it in a later commit and describing the result as certifying
that commit's own new edits.

THIS FILE IS THE MISSING INSTRUMENT, NOT A REPLACEMENT FOR THAT ONE.  It reads the
WORKING TREE for everything it certifies.  `b68db5d^` appears only as the BEFORE side of a
measured delta, which is what a baseline is for.  Run negative_control.py to see it fail.

WHAT IT CERTIFIES — the two files b68db5d changed:

    STATE.md                       row :135, the F1 repair (one line, +173 characters)
    docs/state-history/README.md   the F1 / F2 / B1 correction blocks, and the A1 / A3
                                   blocks this repair's own record rests on

WHY THE MECHANISM CHANGED (mg-7870, repairing mg-2216's B1 and B2).
------------------------------------------------------------------
The first version of this file certified those regions by asserting that five chosen
SUBSTRINGS were present.  mg-2216 built fourteen independent mutations and EIGHT of them
exited 0:

    the certified cell's "every ridge in 1 or 2 facets" -> "1 or 3"    (one character)
    the certified cell's "the proof is sound" -> "bogus"              (five characters)
    the certified cell's ASCII spaces -> U+00A0                       (no visible change)
    two adjacent sentences of the cell swapped                        (length AND tokens kept)
    the last 3,000 of the cell's 7,876 characters replaced by 'x'     (38% of the cell)
    the README F1 block hollowed, its header kept                     (1,556-character body)
    the README F2 block's "13,188 -> 7,703 characters" falsified
    the README A1 block's "175,552 to 37,958 bytes" falsified         (this repair's own figure)

The README half was blind because it tested BLOCK HEADERS, and the negative control this
file ships cuts each block INCLUDING its header — the one mutation the check is shaped
around.  The STATE.md half was blind because presence-of-substring plus total-length is
transparent to every length-preserving edit.

Extending the list a third time would fail the same way, because "does it catch mutation
X?" is open-ended and every list is a list somebody chose.  So the list was not extended.
Each certified region now carries a SHA-256 OF ITS NORMALISED BYTES, compared against a
constant recorded here.  That converts an unbounded question into a closed one: a digest
cannot be fooled by a length-preserving edit, a whitespace substitution, a reordering or a
bulk overwrite, and it is equally unfooled by mutations nobody has thought of.

THE NORMALISATION IS THE ONLY PLACE A MUTATION CAN STILL HIDE, so it is one rule and it is
stated in full:

    N(region) = the region's characters with ASCII SPACE, TAB, CR and LF removed from the
                TWO ENDS of the whole region — nothing else — encoded UTF-8.

Nothing interior is touched: no case folding, no Unicode normalisation, no whitespace
collapsing, no line-ending rewriting, no markdown parsing.  U+00A0 is NOT whitespace to
this rule (Python's str.strip() would eat it; `.strip(" \\t\\r\\n")` does not), so the
whitespace-substitution mutation dies on the digest like any other.  The rule tolerates
exactly one class of edit — padding at a region's outer edge, e.g. trailing spaces before
a cell's closing pipe — and that tolerance is deliberate and is on the record below.

The digested cell is 7,876 characters, the same figure b68db5d's message reports under its
own "stripped" convention: on this material `.strip()` and `.strip(" \\t\\r\\n")` agree, so
the normalisation change moves no published number.

WHAT THE SUBSTRING CHECKS ARE FOR NOW.  They no longer certify; they CLASSIFY.  A digest
says only "these are not the bytes that were certified".  The substring checks say whether
the load-bearing sentences of the repair are still there, which is what separates FAIL
("the repair is damaged") from MOVED ("the region changed; go look at the diff").  Both
are non-zero.  The block markers additionally LOCATE each README region; a block that
cannot be located is a FAIL, so the header line is covered by the locator and by the
digest, which spans the whole block including it.

WHAT A READER SEES (mg-4acd, repairing mg-babf's B1).
-----------------------------------------------------
The digest above was the right move and it is not undone.  What mg-babf found is that the
blind spot MOVED ONE LAYER UP.  A digest answers *"are these the certified bytes?"* — now
correctly, on all five of mg-2216's survivors.  The LOCATOR answers *"which bytes are the
certified ones?"*, and underneath that it was silently answering *"and is anybody shown
them?"* — a question nothing controlled.  Four mutations changed NO certified byte and
exited 0:

    a certified block MOVED VERBATIM under "Appendix Z ... nothing below is in force"
    a certified block wrapped in a ```text FENCE, rendering as a code sample
    a certified block wrapped in an HTML COMMENT, absent from every rendered view
    a "RETRACTED ... is void" paragraph inserted immediately ABOVE a certified block

THE PROPERTY NOW CERTIFIED:  A MUTATION THAT CHANGES WHAT A READER SEES MUST CHANGE A
DIGEST.  Each region carries a second digest, of its PRESENTATION RECORD — an ordered,
printed-in-full set of four block-level facts:

    state       is the region presented as prose at all, or is it inside a code fence, an
                HTML comment or a raw HTML block?  (for the ledger cell: does its line
                render as a GFM table row, and which of its fields does GFM show?)
    heading     the ATX heading path in force where the region sits
    position    the region's ordinal among the blocks of its section, and the section's
                block count
    presented   sha256 of the region's text with block-quote markers removed

Why those four and not a renderer's output: see presentation.py, which is the whole of the
new mechanism and states its closure argument, its declared subset and its cost.  The
short form of the closure argument is that the CONTENT digest already fires on every edit
INSIDE a region, so the presentation layer only has to answer for edits OUTSIDE it, and
the ways an outside edit can change how a region is presented are block-level and few.

THE COST, because this is a trade and not a free win.  mg-babf proposed digesting the
RENDERED text and named the cost: a dependency on a renderer, under which a renderer
upgrade becomes a false positive.  The direction is taken, the mechanism is not — no
markdown renderer exists on this box (checked: no markdown / markdown_it / mistune /
commonmark / cmarkgfm module, no pandoc / cmark / cmark-gfm binary), and every instrument
in this cluster imports nothing.  THE COST TAKEN INSTEAD is that presentation.py is a
MODEL of a renderer rather than a renderer: where model and renderer disagree, this
control is wrong, and the model is argued from the CommonMark and GFM block rules rather
than measured against an implementation, because there is none here to measure against.
What bounds it is DEFAULT-DENY — a construct outside the declared subset, or any raw HTML
in prose, is reported and exits non-zero rather than passing.  What is NOT bounded is the
model being confident and wrong, and that is now the uncontrolled layer.  It is named
here, and in COVERAGE.md, so the next auditor tests it rather than discovers it.

POSITION IS NOW CERTIFIED, AND THAT REVERSES A PUBLISHED TOLERANCE.  mg-2216's M12 (60
lines inserted above the certified row) and M13 (the row moved to the end of the file,
byte-identical) were declared TOLERATE against this file's stated design goal of surviving
line insertion.  Both now fire, and the reason is not a change of taste: both break the
ledger table — M12 splits it so the certified row has no delimiter row above it, M13 lifts
the row out of the table entirely — so under GFM the row stops rendering as a table row and
becomes pipes in a paragraph.  That is a change to what a reader sees, so under the
property above it must fire.  The reclassification is argued from the GFM table rules and
is NOT verified against a renderer, for the reason given above; it is recorded in
COVERAGE.md as a reversal rather than folded in quietly.  Locating BY KEY rather than by
line number is unchanged and still buys what it always bought: the instrument does not rot
when lines are inserted somewhere else in the file.

COVERAGE — what is digested, and what is deliberately not.
----------------------------------------------------------
DIGESTED (9 regions, listed in CERTIFIED below), each with TWO digests — content and
presentation:
    STATE.md      row mg-276d's content cell, in the working tree      7,876 chars
    STATE.md      the same cell at b68db5d^, the BEFORE of the delta   7,703 chars
    README        the F2 correction block                              2,306 chars
    README        the F1 correction block                              1,643 chars
    README        the B1 attribution-correction paragraph                565 chars
    README        the B1 bullet's A3 correction block                    719 chars
    README        the index note carrying the moved cell figure           310 chars
    README        the A1 correction block (b68db5d's headline sentence) 3,060 chars
    README        the mg-2216 / mg-7870 correction to that A1 block       2,736 chars

NOT COVERED, on purpose — this instrument certifies b68db5d's DELTA, not the two files:
    * Every other row of STATE.md's ledger, and every other line of it.  Only the whole-file
      ** parity and largest-cell checks in section 6, and the two presentation guards in
      section 8, look outside the certified row, and those are invariants, not digests.
      Deleting an unrelated ledger row exits 0 here.
    * Every other paragraph, table and block of the state-history README, including the
      per-row index table's own numeric columns and all ten attempt-*.md files.
    * Padding at the outer edge of a digested region (see the normalisation rule).
    * THE ROW'S INDEX WITHIN THE LEDGER TABLE, and any certified region's absolute line
      number.  Position is certified as an ordinal among the BLOCKS of a section, not as a
      row number or a line number, so that deleting an unrelated ledger row stays outside
      coverage — which it was before mg-4acd and still is.
    * INLINE presentation.  presentation.py resolves block structure only: emphasis, links,
      code spans and entities inside a region are certified as BYTES by the content digest
      and are not rendered or compared as rendered.
    * WHETHER THE MODEL MATCHES THE RENDERER.  presentation.py is a model of a renderer
      argued from the CommonMark / GFM block rules, not measured against one.  Constructs
      outside its declared subset are reported by the section-8 guards and exit non-zero;
      the residual exposure is a construct the model classifies CONFIDENTLY AND WRONGLY.
    * WHETHER A CHANGE IS LEGITIMATE.  A digest mismatch is reported as MOVED and exits
      non-zero; this instrument does not and cannot decide whether the new bytes are damage
      or a correct later edit.  Re-baseline with `--emit-baseline` and say which commit
      moved it.  The point is that it cannot go quietly green either way.
    * Anything in the two files at any revision other than the working tree and b68db5d^.

The goal is not a control that catches everything.  It is a control whose coverage is
stated and bounded, so the next auditor can test the boundary instead of guessing at it.

HOW IT LOCATES THINGS, and this is deliberate.  Every check keys on CONTENT — the ledger
row is found by its attempt id, the cell by being the row's widest, each README region by a
marker inside it — never by line number and never by a whole-file frozen blob comparison.
The scope mismatch this arc keeps hitting (mg-6a2f F1: "a claim about a cell, checked
against a clause") is what line-anchored checking buys you.  A key-based check also
survives legitimate later commits that insert lines above the row, so this instrument does
not age out the way a line-pinned one would.  The digests are per-REGION for the same
reason: a digest of the whole file would fire on every unrelated edit and would have to be
re-baselined into meaninglessness.

EXIT CODES, both non-zero on failure and distinguishable on purpose:

    0   every check passed
    1   FAIL   — a certification check failed.  b68db5d's repair is damaged in the tree, a
                 certified region can no longer be located at all, or a certified region is
                 NO LONGER PRESENTED TO A READER — inside a code fence, inside an HTML
                 comment, inside a raw HTML block, or (for the ledger cell) no longer
                 rendering as a table row.  A region nobody is shown is damage, not drift.
    2   MOVED  — the repair's load-bearing sentences are intact, but a certified region's
                 content digest no longer matches, its PRESENTATION RECORD no longer
                 matches (it moved under a different heading, or its position among the
                 blocks of its section changed), a measured constant of the landing has
                 changed, or a presentation guard tripped — a block construct outside
                 presentation.py's declared subset, or raw HTML in text presented as prose.
                 Re-baseline this instrument, record the new figure, and say which commit
                 moved it.  It exits non-zero so it CANNOT go on quietly reporting green
                 about a delta that is no longer the delta it was written for — which is
                 the whole failure this file was filed against.

Exit 3 is deliberately NOT used for digest mismatches: mg-2216's independent battery reads
1 and 2, and an instrument that invents a code its own auditor's harness scores as a miss
would be repairing the defect by hiding it.

INSTRUMENT DISCIPLINE (this arc has been bitten by all three):
  * `wc -m` counts BYTES on this box (LC_CTYPE=C) and agrees with `wc -c`, so cross-checking
    the two reads as confirmation while both are wrong.  Nothing here shells out to wc:
    characters are len(str), bytes are len(bytes).
  * Every figure names its UNIT and, for cells, its CONVENTION.  b68db5d's message measures
    cells STRIPPED (7,703 -> 7,876); the README index measures them RAW, i.e. including the
    space either side of the boundary pipe (7,705 -> 7,878).  Both are printed, both are
    labelled, and the split is REPORTED not silently reconciled — it is mg-bd41's A4, a
    MINOR finding outside this ticket's brief, and it stays open.
  * Every tally is over UNBOUNDED input.  No head/tail/sed -n/--limit anywhere; each count
    prints the population it was taken over.
  * The digests are printed in full, not truncated, so a reader can recompute one by hand.

Imports nothing from code/state_restructure_34bf/, code/state_audit_6a2f/,
code/state_landing_audit_bd41/, code/state_control_audit_2216/ or
code/state_control_audit_babf/.  The one module it does import, presentation.py, sits
beside it and is part of this instrument.
"""
import hashlib
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import presentation as pres              # noqa: E402  (path fixed up on the line above)

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()

BASELINE = "b68db5d^"          # the BEFORE side of the delta.  Never the certified side.
LANDING = "b68db5d"            # named in prose only; nothing here reads it as evidence.

ROW_KEY = "mg-276d"            # the attempt id of the row b68db5d edited (STATE.md:135)
BIGGEST_KEY = "mg-a3d4"        # the row holding the largest cell in the file (:136)

# --- the measured constants of the landing, from b68db5d's own SCOPE paragraph -----------
CELL_AFTER_STRIPPED = 7876
CELL_BEFORE_STRIPPED = 7703
CELL_DELTA = 173
BIGGEST_STRIPPED = 8440
GAP_CHARS = 399                # counterexample -> F1 sentence, inside row :135's cell
GAP_WORDS = 72

# --- the text the F1 repair put in the tree ----------------------------------------------
# These CLASSIFY (damaged vs merely changed) and LOCATE.  They do not certify; the digests
# below do.  Adding to this list does not widen coverage — see "WHY THE MECHANISM CHANGED".
F1_NARROW = "This row states no 4d *tally* of its own"
F1_ABSOLUTE_QUOTED = 'mg-34bf wrote that as an absolute *"states no count of its own"*'
F1_ATTRIBUTION = "mg-6a2f F1, narrowed to the true claim by mg-7735"
F1_COUNTEREXAMPLE = "five previous rows"
F1_OLD_ABSOLUTE = "This row states no count of its own"

README = "docs/state-history/README.md"

FAIL, MOVED = 1, 2
_seen = {FAIL: 0, MOVED: 0}
_digest_misses = []


# =========================================================================================
# THE NORMALISATION — the whole of it.  See the module docstring.
# =========================================================================================
EDGE = " \t\r\n"


def norm(text):
    """N(region): strip ASCII space/tab/CR/LF from the two ends, encode UTF-8.

    Deliberately NOT str.strip(), which also strips U+00A0, U+2028 and friends — the
    whitespace-substitution mutation must die on the digest, not be normalised away.
    Nothing interior is touched.
    """
    return text.strip(EDGE).encode("utf-8")


def digest(text):
    return hashlib.sha256(norm(text)).hexdigest()


def exit_code():
    """FAIL outranks MOVED: a damaged repair is the more serious report, and a
    non-zero code is produced by either."""
    if _seen[FAIL]:
        return FAIL
    if _seen[MOVED]:
        return MOVED
    return 0


def blob(rev, path):
    """Bytes of `path` at `rev`.  Baselines only — never the certified side."""
    return subprocess.run(["git", "-C", REPO, "show", f"{rev}:{path}"],
                          capture_output=True, check=True).stdout


def tree(path):
    """Bytes of `path` in the WORKING TREE.  This is what the instrument certifies."""
    with open(os.path.join(REPO, path), "rb") as fh:
        return fh.read()


def split_row(line):
    """Escape-aware markdown table split.

    Literal pipes inside STATE.md cells are written `\\|`, so a cell boundary is a '|'
    NOT preceded by a backslash.  Returns the RAW fragments between boundary pipes
    (leading/trailing space intact), or None if the line is not a table row.
    """
    bounds = [i for i, ch in enumerate(line)
              if ch == "|" and (i == 0 or line[i - 1] != "\\")]
    if len(bounds) < 2 or bounds[0] != 0:
        return None
    return [line[bounds[i] + 1:bounds[i + 1]] for i in range(len(bounds) - 1)]


def all_rows(text):
    """(1-indexed line number, raw cell list) for every table row in `text`."""
    out = []
    for n, line in enumerate(text.split("\n"), start=1):
        if line.startswith("|"):
            cells = split_row(line)
            if cells:
                out.append((n, cells))
    return out


def find_row(text, key):
    """The unique ledger row carrying `key` in one of its first two columns.

    Columns 1 and 2 (verdict, attempt) are what mg-34bf's restructure left untouched —
    "which is also what makes the completeness check's row key stable", in the README's
    words — and b68db5d changed neither.  So they are the stable key, and the third
    (content) column, which is the thing being certified, is deliberately not searched.
    """
    hits = [(n, cells) for n, cells in all_rows(text)
            if len(cells) >= 3 and any(key in c for c in cells[:2])]
    return hits


def widest(cells):
    """The row's CONTENT cell: its widest.  Returned raw; strip at the call site.

    'The third column' is not portable — STATE.md holds tables of different arities.
    """
    return max(cells, key=len)


# =========================================================================================
# REGION EXTRACTORS.  Each returns (first line number, last line number, region text) or
# raises LookupError, which the caller turns into a FAIL.  Every one locates by a marker
# inside the region — never by line number.
# =========================================================================================


def _unique_marker_line(lines, marker):
    hits = [i for i, l in enumerate(lines) if marker in l]
    if len(hits) != 1:
        raise LookupError(f"marker matched {len(hits)} lines, need exactly 1")
    return hits[0]


def quote_block(text, marker):
    """The maximal run of consecutive blockquote lines containing `marker`.

    A blockquote line is one whose first non-space character is '>', so the bullet-indented
    correction blocks are found on the same rule as the top-level ones.  The run INCLUDES
    the header line: hollowing a block while keeping its header changes the digest, which
    is mg-2216's B1.
    """
    lines = text.split("\n")
    i = _unique_marker_line(lines, marker)

    def is_quote(k):
        return 0 <= k < len(lines) and lines[k].lstrip().startswith(">")

    if not is_quote(i):
        raise LookupError("marker line is not a blockquote line")
    s = i
    while is_quote(s - 1):
        s -= 1
    e = i + 1
    while is_quote(e):
        e += 1
    return s + 1, e, "\n".join(lines[s:e])


def paragraph(text, marker):
    """The maximal run of consecutive non-blank, non-blockquote lines containing `marker`.

    Used for the two certified regions that are prose rather than blockquotes: the B1
    attribution correction (inside a bullet) and the index note that carries the moved
    cell figure.
    """
    lines = text.split("\n")
    i = _unique_marker_line(lines, marker)

    def is_body(k):
        return (0 <= k < len(lines) and lines[k].strip()
                and not lines[k].lstrip().startswith(">"))

    if not is_body(i):
        raise LookupError("marker line is blank or a blockquote line")
    s = i
    while is_body(s - 1):
        s -= 1
    e = i + 1
    while is_body(e):
        e += 1
    return s + 1, e, "\n".join(lines[s:e])


# =========================================================================================
# THE CERTIFIED REGIONS.  (id, label, kind, marker, characters after N, sha256 of N)
#
# Baselined at mg-7870 against the working tree at 6b1eacf.  Regenerate with:
#     python3 code/state_landing_control_2da3/delta_control.py --emit-baseline
# and, when you paste the result in, say in the commit message WHICH COMMIT MOVED IT.
#
# RULE FOR CHOOSING A MARKER, learned from this repair's own NC5: a marker must sit
# OUTSIDE the figures and claims its region certifies.  A marker that contains them is
# self-defeating — falsify the figure and the region stops being locatable, so the
# instrument reports FAIL "not locatable" instead of MOVED "these are not the certified
# bytes".  Both are non-zero, so nothing goes green either way, but the classification is
# wrong and a reader chasing a FAIL looks for a deletion that is not there.  readme.index
# keys on the sentence that introduces the figures, not on "**7,878**"; readme.F1 keys on
# "no 4d tally is a correction" and deliberately not on the "133 / 220" that follow it.
# =========================================================================================
CERTIFIED = [
    ("cell.tree", "row :135's content cell, WORKING TREE", "cell", None, 7876,
     "b53ad402349d531fb8d18893ca55c380517ed3b809bfc0d4aeb0c41b795ccf87"),
    ("cell.base", f"row :135's content cell at {BASELINE}", "cell-base", None, 7703,
     "8316d1b578e497c80c34820e9ae25057edb75faf2ec1bcf8fe67dd667f341fcc"),
    ("readme.F2", "the F2 correction block", "quote",
     "**THOSE FIVE FIGURES WERE WRONG, here and in `57f962f`'s commit message", 2306,
     "ad9143cc402c797a600166968d7fbc4d1dc9423f03f00d373dfc026004020b06"),
    ("readme.F1", "the F1 correction block", "quote",
     "**`no 4d tally` is a correction", 1643,
     "f81e2cdc63bd0fbcc2790f2878959ac4aab35c54ce9690fdec84ab7e0dc51908"),
    ("readme.B1", "the B1 attribution correction", "para",
     "**Two corrections to this bullet, from mg-6a2f §B1, made by mg-7735.**", 565,
     "0a82cf6e268e3c14feed39dd9b0526f30a48bec0dec092c2ed25a1eb62564991"),
    ("readme.B1.A3", "the B1 bullet's A3 ancestry correction", "quote",
     "**`two commits before mg-34bf's parent` was off by one", 719,
     "3105129a342e1b68b6d229e6adb223f2a33044dd612d18b72490dfb19dcedb51"),
    ("readme.index", "the index note carrying the moved cell figure", "para",
     "**`cell before` and `cell after` are measured at", 310,
     "a1e051c6f2bfa83f3be63870b5a6b80c41bce10e96069695a2999b3681570acc"),
    ("readme.A1", "the A1 correction block (b68db5d's headline sentence)", "quote",
     "**`b68db5d`'s HEADLINE VERIFICATION SENTENCE IS BLIND TO THE CHANGE IT CERTIFIES",
     3060, "edd94cc24bf1b6f0a78b1c311a974e986f84875c54a102b8c9cae9452f9b8468"),
    ("readme.A1.7870", "the mg-2216 / mg-7870 correction to the A1 block", "quote",
     "DID NOT ESTABLISH WHAT THE BLOCK ABOVE CLAIMS", 2736,
     "59ab8f5068742edb7e67ae0efd060d0eeb09f3174d8789df29ac529304620bd2"),
    ("readme.A1.4acd", "the mg-babf / mg-4acd correction to the A1 block", "quote",
     "mg-babf B1, BROKEN, repaired by mg-4acd", 3695,
     "779702c03697be89bfd9c40ffc483e78aec834a6d3eb58989ac60399aef45c11"),
]

# =========================================================================================
# THE PRESENTATION BASELINE (mg-4acd).  rid -> sha256 of the region's PRESENTATION RECORD.
#
# The record is four ordered fields — state, heading, position, presented — serialised one
# `key=value` per line and hashed.  Every field is PRINTED IN FULL by section 2b, so a
# reader can recompute any of these by hand, exactly as for the content digests.
#
# Baselined by mg-4acd against the working tree at 1db0be9.  Regenerate with
#     python3 code/state_landing_control_2da3/delta_control.py --emit-baseline
# and say in the commit message WHICH COMMIT MOVED IT.
#
# A NOTE ON WHAT MOVES THESE.  A presentation digest is by construction sensitive to the
# region's surroundings: adding or removing a block anywhere in the region's section moves
# `position` for every block after it in that section, and renaming a heading moves
# `heading` for every region under it.  That is not a defect, it is the coverage: position
# and context are what the four mutations exploited.  It is also the running cost, and it
# is stated in COVERAGE.md beside the mechanism rather than discovered later.
# =========================================================================================
PRESENTATION = {
    "cell.tree": "a621c910868ba3bc254216e983fb8cb84da6007d94a01f24e2f71c2a60ecba0e",
    "cell.base": "14e4171a94061a951b0e4b653d11f42857ee328b6fd6e13d870727faf4fe7b77",
    "readme.F2": "dbe341f97e051849c23746029854c43dcac35812f5332f8f5fb39b3e36e6565d",
    "readme.F1": "52edb2c400a888536146c716dabb14837fa14f75dad026b80f797ff1c708c63b",
    "readme.B1": "7d1a3e1daaee38e0622e4133a2c475828d4928d2a42b30cde51e58cfc6f3fa5d",
    "readme.B1.A3": "245cc23b4b24a718a7fe220dff71937878496f5546c6e11dce99481dc3ac95b9",
    "readme.index": "5a73c86c64b2ec773e73dff12ee0f49f8477f7397ebe901f5049d364c907d4df",
    "readme.A1": "f642d170bc7bdc7c869ea8f23e1f452c2994a27fb16a446e554c5bcb975a2780",
    "readme.A1.7870": "25892df23732ba028e28ba99d83b5cc4aa16d552f2d877dfd44fdff1c81e3326",
    "readme.A1.4acd": "5c28bc769bf19d59ed094432ee6629bf048e48cbcd32eababdf32e1be315fade",
}


def extract(rid, kind, marker, state_tree, state_base, readme_tree):
    """(where, region text) for a certified region.  Raises LookupError if unlocatable."""
    if kind in ("cell", "cell-base"):
        text = state_tree if kind == "cell" else state_base
        hits = find_row(text, ROW_KEY)
        if len(hits) != 1:
            raise LookupError(f"key {ROW_KEY} matched {len(hits)} rows")
        n, cells = hits[0]
        return (f"STATE.md:{n}" if kind == "cell"
                else f"{BASELINE}:STATE.md:{n}"), widest(cells)
    s, e, text = (quote_block if kind == "quote" else paragraph)(readme_tree, marker)
    return f"{README}:{s}-{e}", text


def presentation_record(kind, marker, docs, state_tree, state_base, readme_tree):
    """The PRESENTATION RECORD of a certified region: what a reader is shown, and where.

    Same locating rule as extract() — by content marker, never by line number — because a
    presentation record about the wrong region would be worse than none.
    """
    if kind in ("cell", "cell-base"):
        text = state_tree if kind == "cell" else state_base
        hits = find_row(text, ROW_KEY)
        if len(hits) != 1:
            raise LookupError(f"key {ROW_KEY} matched {len(hits)} rows")
        n, cells = hits[0]
        return pres.table_record(docs["cell" if kind == "cell" else "base"], n - 1, cells)
    s, e, _text = (quote_block if kind == "quote" else paragraph)(readme_tree, marker)
    return pres.region_record(docs["readme"], s - 1, e - 1)


def is_presented(record):
    """True iff a reader is shown this region as prose (or as a GFM table row).

    Anything else — a code fence, an HTML comment, a raw HTML block, pipes that no longer
    form a table row — means the certified bytes are present and nobody sees them, which is
    exactly the state mg-babf's B05/B06 put the F1 block into while the control said PASS.
    """
    return dict(record)["state"] in ("rendered", "gfm-table-row")


def check(label, ok, detail="", kind=FAIL):
    verdict = "pass" if ok else ("FAIL" if kind == FAIL else "MOVED")
    print(f"  [{verdict}] {label}")
    if detail:
        print(f"         {detail}")
    if not ok:
        _seen[kind] += 1
    return ok


def emit_baseline(docs, state_tree, state_base, readme_tree):
    """Print a PASTEABLE CERTIFIED table and PRESENTATION map for the tree as it stands.

    Two mg-babf MINORs are fixed here rather than left in the documented recovery path:
    the emitter used to print a literal "..." in place of the label / kind / marker, so
    what two documents told you to paste was not pasteable; and it crashed with an
    uncaught LookupError emitting NOTHING AT ALL if any one region was unlocatable, which
    is precisely the tree it exists for.  Unlocatable regions are now emitted commented
    out, with the reason, and the rest of the table still comes out.
    """
    print("# regenerated by --emit-baseline; say which commit moved each figure")
    print("CERTIFIED = [")
    for rid, label, kind, marker, _chars, _sha in CERTIFIED:
        m = "None" if marker is None else '"%s"' % marker.replace('"', '\\"')
        try:
            where, text = extract(rid, kind, marker, state_tree, state_base, readme_tree)
        except LookupError as exc:
            print(f'    # UNLOCATABLE ({exc}) — left for a human:')
            print(f'    # ("{rid}", "{label}", "{kind}", {m}, ?, "?"),')
            continue
        print(f'    ("{rid}", "{label}", "{kind}",  # {where}\n'
              f'     {m},\n'
              f'     {len(norm(text).decode())}, "{digest(text)}"),')
    print("]")
    print("PRESENTATION = {")
    for rid, _label, kind, marker, _chars, _sha in CERTIFIED:
        try:
            record = presentation_record(kind, marker, docs,
                                         state_tree, state_base, readme_tree)
        except LookupError as exc:
            print(f'    # "{rid}": UNLOCATABLE ({exc}) — left for a human')
            continue
        for k, v in record:
            print(f"    # {k:<10} {v}")
        print(f'    "{rid}": "{pres.record_digest(record)}",')
    print("}")
    return 0


def main():
    print("mg-2da3 — working-tree control for b68db5d's delta")
    print("           (mg-7870: certified by CONTENT DIGEST — are these the certified bytes?)")
    print("           (mg-4acd: and by PRESENTATION RECORD — is a reader shown them?)")
    print(f"certified side  : the WORKING TREE (STATE.md, {README})")
    print(f"baseline side   : {BASELINE}  — used ONLY as the BEFORE of a measured delta")
    print()

    state_tree_b = tree("STATE.md")
    state_tree = state_tree_b.decode("utf-8")
    state_base = blob(BASELINE, "STATE.md").decode("utf-8")
    readme_tree = tree(README).decode("utf-8")
    docs = {"cell": pres.Doc(state_tree), "base": pres.Doc(state_base),
            "readme": pres.Doc(readme_tree)}

    if "--emit-baseline" in sys.argv:
        return emit_baseline(docs, state_tree, state_base, readme_tree)

    lines_tree = state_tree.split("\n")
    print(f"STATE.md in the working tree: {len(state_tree_b)} bytes, "
          f"{len(state_tree)} characters, "
          f"{len(lines_tree) - (1 if lines_tree[-1] == '' else 0)} lines")
    rows_tree = all_rows(state_tree)
    cells_tree = [c for _, cells in rows_tree for c in cells]
    print(f"                             {len(rows_tree)} table rows, "
          f"{len(cells_tree)} cells (the population every whole-file tally below is over)")
    print()

    # ---- 1. locate the row b68db5d edited, by key, in the tree ---------------------------
    print("1. THE ROW b68db5d EDITED, located by attempt id (not by line number)")
    hits = find_row(state_tree, ROW_KEY)
    if not check(f"exactly one ledger row keys to {ROW_KEY} in the working tree",
                 len(hits) == 1, f"found {len(hits)}"):
        print()
        print("=" * 78)
        print("RESULT: FAIL (exit 1) — the row b68db5d edited is not identifiable in the")
        print("        working tree at all, so nothing below it can be certified.")
        print("=" * 78)
        return FAIL
    row_line, row_cells = hits[0]
    cell_raw = widest(row_cells)
    cell = cell_raw.strip(EDGE)
    check("it is a three-column row", len(row_cells) == 3, f"columns: {len(row_cells)}")
    print(f"         at line :{row_line} in this tree "
          f"(observed, not asserted — the check above is key-based)")
    print()

    base_hits = find_row(state_base, ROW_KEY)
    if not check(f"the same key locates exactly one row at {BASELINE}",
                 len(base_hits) == 1, f"found {len(base_hits)}"):
        print()
        print("=" * 78)
        print(f"RESULT: FAIL (exit 1) — no baseline row at {BASELINE} to measure against.")
        print("=" * 78)
        return FAIL
    base_cell_raw = widest(base_hits[0][1])
    base_cell = base_cell_raw.strip(EDGE)

    # ---- 2. THE CERTIFICATION ITSELF: a content digest per certified region --------------
    print("2. CERTIFIED REGION DIGESTS — sha256 of N(region), N = strip ASCII space/tab/")
    print("   CR/LF from the two ends and nothing else.  This is what certifies the delta;")
    print(f"   {len(CERTIFIED)} regions, all located by content, all printed in full.")
    for rid, label, kind, marker, want_chars, want_sha in CERTIFIED:
        try:
            where, text = extract(rid, kind, marker, state_tree, state_base, readme_tree)
        except LookupError as exc:
            check(f"{rid} — {label}: LOCATABLE", False, f"{exc}")
            _digest_misses.append((rid, label, "not locatable"))
            continue
        got_norm = norm(text)
        got_chars, got_sha = len(got_norm.decode("utf-8")), digest(text)
        ok = got_sha == want_sha
        check(f"{rid} — {label}", ok,
              f"{where}; {got_chars} characters, {len(got_norm)} bytes after N\n"
              f"         certified sha256 {want_sha}\n"
              f"         measured  sha256 {got_sha}"
              + ("" if ok else
                 f"\n         >>> the bytes of this region are NOT the bytes that were "
                 f"certified ({got_chars - want_chars:+d} characters)"),
              kind=MOVED)
        if not ok:
            _digest_misses.append((rid, label, f"{got_chars - want_chars:+d} characters"))
    print()

    # ---- 2b. WHAT A READER SEES: a presentation record per certified region --------------
    print("2b. CERTIFIED PRESENTATION RECORDS — the content digest above says these are the")
    print("    certified BYTES; these say a reader is still SHOWN them, in the same place.")
    print("    Four fields, printed in full, hashed in the order printed.  A region that is")
    print("    no longer presented at all is a FAIL; one that moved is a MOVED.")
    for rid, label, kind, marker, _chars, _sha in CERTIFIED:
        try:
            record = presentation_record(kind, marker, docs,
                                         state_tree, state_base, readme_tree)
        except LookupError as exc:
            check(f"{rid} — {label}: LOCATABLE for presentation", False, f"{exc}")
            _digest_misses.append((rid, label, "not locatable"))
            continue
        want = PRESENTATION.get(rid, "")
        got = pres.record_digest(record)
        shown = is_presented(record)
        detail = "\n".join(f"         {k:<10} {v}" for k, v in record).lstrip()
        detail += (f"\n         certified record sha256 {want}"
                   f"\n         measured  record sha256 {got}")
        if not shown:
            detail += ("\n         >>> THE CERTIFIED BYTES ARE PRESENT AND NOBODY IS SHOWN "
                       "THEM.")
            check(f"{rid} — {label}: PRESENTED", False, detail, kind=FAIL)
            _digest_misses.append((rid, label, "not presented to a reader"))
        else:
            ok = got == want
            if not ok:
                detail += ("\n         >>> a reader does not see this region where the "
                           "certified record says it is")
            check(f"{rid} — {label}: presentation", ok, detail, kind=MOVED)
            if not ok:
                _digest_misses.append((rid, label, "presentation record moved"))
    print()

    # ---- 3. the F1 repair itself — CLASSIFIERS, not the certification --------------------
    print("3. THE F1 REPAIR — present in the tree, absent at the baseline")
    print("   (these separate 'damaged' from 'changed'; section 2 is what certifies)")
    check("tree row states the NARROW claim", F1_NARROW in cell,
          f'"{F1_NARROW}"')
    check("tree row QUOTES the false absolute it replaced", F1_ABSOLUTE_QUOTED in cell)
    check("tree row ATTRIBUTES the correction", F1_ATTRIBUTION in cell)
    check("baseline row carried the bare absolute", F1_OLD_ABSOLUTE in base_cell)
    check("baseline row did NOT carry the narrow claim", F1_NARROW not in base_cell)
    print()

    # ---- 4. the counterexample the repair exists because of ------------------------------
    print("4. THE COUNTEREXAMPLE THAT MADE THE ABSOLUTE FALSE — still in the cell,")
    print("   and still EARLIER in it than the sentence that used to deny it")
    i = cell.find(F1_COUNTEREXAMPLE)
    j = cell.find(F1_NARROW)
    if check(f'the cell still opens on "{F1_COUNTEREXAMPLE}"', i >= 0):
        check("it precedes the F1 sentence", 0 <= i < j,
              f"counterexample at char {i}, F1 sentence at char {j}")
        gap = cell[i:j]
        check(f"the gap is {GAP_CHARS} characters", len(gap) == GAP_CHARS,
              f"measured {len(gap)} characters "
              f"(from the start of the phrase to the start of the sentence)",
              kind=MOVED)
        check(f"the gap is {GAP_WORDS} words", len(gap.split()) == GAP_WORDS,
              f"measured {len(gap.split())} whitespace-separated words", kind=MOVED)
    print()

    # ---- 5. the measured delta ----------------------------------------------------------
    print("5. THE MEASURED DELTA — tree against baseline, both conventions printed")
    print(f"         stripped: {len(base_cell)} -> {len(cell)} characters")
    print(f"         raw     : {len(base_cell_raw)} -> {len(cell_raw)} characters "
          f"(raw = including the space either side of the boundary pipe)")
    print(f"         bytes   : {len(base_cell.encode())} -> {len(cell.encode())} "
          f"(stripped convention)")
    check(f"baseline cell is {CELL_BEFORE_STRIPPED} characters (stripped)",
          len(base_cell) == CELL_BEFORE_STRIPPED, f"measured {len(base_cell)}", kind=MOVED)
    check(f"tree cell is {CELL_AFTER_STRIPPED} characters (stripped)",
          len(cell) == CELL_AFTER_STRIPPED, f"measured {len(cell)}", kind=MOVED)
    check(f"the delta is +{CELL_DELTA} characters",
          len(cell) - len(base_cell) == CELL_DELTA,
          f"measured {len(cell) - len(base_cell):+d}", kind=MOVED)
    print()

    # ---- 6. whole-file invariants b68db5d claims, measured on the TREE -------------------
    print("6. WHOLE-FILE INVARIANTS, measured on the working tree")
    print("   (invariants, NOT digests — the rest of the ledger is outside coverage)")
    odd = [(n, k) for n, cells in rows_tree for k, c in enumerate(cells)
           if c.count("**") % 2]
    check("** parity is even in every cell",
          not odd,
          f"over all {len(cells_tree)} cells; "
          + (f"odd at {odd}" if odd else "0 odd"))

    big_hits = find_row(state_tree, BIGGEST_KEY)
    if check(f"exactly one ledger row keys to {BIGGEST_KEY}", len(big_hits) == 1,
             f"found {len(big_hits)}"):
        big_cell = widest(big_hits[0][1]).strip(EDGE)
        largest = max(cells_tree, key=lambda c: len(c.strip(EDGE)))
        check(f"the {BIGGEST_KEY} row still holds the largest cell in the file",
              largest.strip(EDGE) == big_cell,
              f"largest cell is {len(largest.strip(EDGE))} characters (stripped), "
              f"over all {len(cells_tree)} cells")
        check(f"and it is still {BIGGEST_STRIPPED} characters (stripped)",
              len(big_cell) == BIGGEST_STRIPPED, f"measured {len(big_cell)}", kind=MOVED)
        check("the edited row is still smaller than it",
              len(cell) < len(big_cell), f"{len(cell)} < {len(big_cell)}")
    print()

    # ---- 7. the README half of the delta -------------------------------------------------
    print(f"7. {README} — the correction blocks b68db5d and this repair added")
    print(f"         {len(readme_tree.encode())} bytes, {len(readme_tree)} characters, "
          f"{len(readme_tree.split(chr(10)))} lines")
    print("         (their CONTENT is certified in section 2; these lines report where")
    print("          each one was found and how much of it the digest spans)")
    for rid, label, kind, marker, want_chars, _sha in CERTIFIED:
        if kind in ("cell", "cell-base"):
            continue
        try:
            where, text = extract(rid, kind, marker, state_tree, state_base, readme_tree)
        except LookupError as exc:
            print(f"  [FAIL] {rid} — {label}: {exc}")
            continue
        head, _, body = text.partition("\n")
        print(f"  {rid:<14} {where:<38} header {len(head.strip(EDGE))} chars, "
              f"body {len(body.strip(EDGE))} chars")
    print()

    # ---- 8. THE PRESENTATION GUARDS — default-deny over both certified files -------------
    print("8. PRESENTATION GUARDS, over BOTH certified files in full")
    print("   presentation.py models a declared subset of CommonMark + GFM block structure.")
    print("   These two guards are how that subset is BOUNDED rather than assumed: a")
    print("   construct it does not model, or raw HTML in text presented as prose, is")
    print("   reported and exits non-zero instead of passing.  Both are 0 as things stand.")
    for label, doc, nlines in (("STATE.md", docs["cell"], len(docs["cell"].lines)),
                               (README, docs["readme"], len(docs["readme"].lines))):
        anom = doc.anomalies()
        html = doc.html_tokens()
        check(f"{label}: 0 block constructs outside the modelled subset",
              not anom,
              f"over all {nlines} lines; "
              + ("0 found" if not anom else "; ".join(
                  f":{n} {kind} {text!r}" for n, kind, text in anom[:6])),
              kind=MOVED)
        check(f"{label}: 0 raw-HTML tokens in text presented as prose",
              not html,
              f"over all {nlines} lines, code fences and inline code spans masked; "
              + ("0 found" if not html else "; ".join(
                  f":{n} {tok!r} in {text!r}" for n, tok, text in html[:6])),
              kind=MOVED)
        print(f"         {len(doc.blocks)} rendered blocks in "
              f"{len(doc.siblings)} sections (the population section 2b's positions are"
              f" ordinals within)")
    print()

    worst = exit_code()
    print("=" * 78)
    if worst == 0:
        print("RESULT: PASS — every check above read the working tree and every one held,")
        print(f"        including {len(CERTIFIED)} content digests and the same number of")
        print("        PRESENTATION RECORDS: the certified bytes are the certified bytes,")
        print("        AND a reader is still shown them, in the same place, as prose.")
        print("        Coverage is stated in this file's header and in COVERAGE.md: what")
        print("        is digested, what is not, and what the presentation model cannot")
        print("        see.  This instrument CAN fail; negative_control.py makes it fail.")
    elif worst == MOVED:
        print("RESULT: MOVED (exit 2) — the F1 repair's load-bearing sentences are intact,")
        if _digest_misses:
            print("        but a CERTIFIED REGION'S CONTENT, OR ITS PRESENTATION, IS NOT")
            print("        WHAT WAS CERTIFIED:")
            for rid, label, why in _digest_misses:
                print(f"          {rid} — {label} ({why})")
            print("        A digest says only that the bytes changed.  It does NOT say")
            print("        whether that is damage or a legitimate later edit, and this")
            print("        instrument does not guess: go read the diff.")
        else:
            print("        but a measured constant of the landing has changed.")
        print("        If the change is legitimate: RE-BASELINE with --emit-baseline,")
        print("        record the new figures, and say which commit moved them.  It exits")
        print("        non-zero rather than quietly reporting green about a delta that is")
        print("        no longer the delta it was written for.")
    else:
        print("RESULT: FAIL (exit 1) — b68db5d's repair is DAMAGED in the working tree,")
        print("        or a certified region is no longer PRESENTED to a reader at all.")
        if _seen[MOVED]:
            print(f"        ({_seen[FAIL]} FAIL, {_seen[MOVED]} MOVED; FAIL is reported"
                  " because it is the more serious of the two.)")
    print("=" * 78)
    return worst


if __name__ == "__main__":
    sys.exit(main())
