#!/usr/bin/env python3
"""mg-e1d0 -- re-measure every fact this landing asserts, from the tree and git.

This landing closes mg-3c24, the audit of `1e61031` (mg-a2bd's strike of ledger
row `G"`).  mg-3c24 merged with findings and no successor was ever filed; the
audit-successor detector recovered the drop.  Four findings are landed here.

The mathematics of mg-3c24 is NOT re-opened and nothing below re-derives it:
that audit found 0 BROKEN mathematics and every committed number reproduced
from a disjoint route.  What is re-measured here is the DOCUMENTARY claim set,
because every one of the four findings is a claim a document makes about
itself, about another document, or about a ticket -- and each was wrong.

  T1  THE ENLARGEMENT (F1).  mg-d39d's finding A5 says the deliverable's §14
      asserts the `STATE.md` row "carries the same clauses" and it does not.
      mg-a2bd edited that very paragraph, inserted a sentence asserting the
      row was UNCHANGED, left the false sentence standing, and in the SAME
      commit more than doubled the mismatch A5 reports.  Measured from git at
      every commit in the chain, AND MEASURED AGAIN IN THE WORKING TREE --
      because the `STATE.md` restructure (mg-34bf, `57f962f`) moved the row's
      history out to a per-row file, so the char-gap the finding was OPENED on
      no longer measures what it measured.  A reader of A5 must meet the
      CURRENT gap.

      ⚠️ CORRECTED 2026-07-30 (mg-f922 findings B/C/E/F, landed by mg-8e30).
      THE LIVE ROW OF THIS TABLE READS THE WORKING TREE, NOT `HEAD`, AND THAT
      IS THE WHOLE POINT.  As first written it read the cell from `git show
      HEAD:STATE.md` and the row history from the tree, and it printed HEAD's
      sha.  Run before a commit that edits those files, it therefore measured
      the PRE-EDIT cell -- and mg-e1d0, the landing this instrument ships
      with, wrote the pre-edit figure (−875) into three documents in the same
      commit that added +1 630 characters to the cell being measured.  The
      figure was false the moment it was committed.

      THE GENERAL SHAPE, because the numbers are the smaller half of it:
      WHEN A COMMIT REPORTS A MEASUREMENT OF SOMETHING THAT COMMIT ALSO
      MODIFIES, THE MEASUREMENT MUST BE TAKEN FROM THE POST-COMMIT STATE, AND
      THE DOCUMENT MUST SAY WHICH SIDE OF THE EDIT IT IS ON.  Reading the
      working tree is how an instrument run before `git commit` sees the
      post-commit state; reading `HEAD` is how it sees the parent's.  The
      GATE below no longer string-matches a frozen figure either: it FORMATS
      what it has just measured and compares the documents' own figure with
      that.

      ⚠️ CORRECTED AGAIN 2026-07-30 (mg-8a5c finding F-1, landed by mg-a318).
      Formatting the measurement is necessary and was not sufficient: the gate
      then asked whether the formatted value OCCURRED SOMEWHERE in the file,
      and the corrected wording printed the live gap TWICE per site.  A
      PRESENCE TEST certifies that a correct value exists, not that the figure
      a reader meets is correct, so corrupting the sentence a reader actually
      reads left the run green at all three sites.  The gate now READS EACH
      FIGURE OUT OF THE STATEMENT THAT ASSERTS IT, at a site anchored to the
      SECTION rather than the file, and the duplicate is GONE rather than
      detected -- the chain's tail points at the live figure instead of
      restating it.

      ⚠️ WIDENED 2026-07-30 (mg-835f finding G-1, landed by mg-8916).  Reading
      each figure out of the statement that asserts it was necessary and was
      still not the whole site: a WRONG figure written into the same section in
      ORDINARY PROSE, beside a designated statement left correct, was invisible
      at 3 of the 3 sites at exit 0.  So "the gate reads the figure at the site"
      was itself an extent claim WIDER THAN THE CODE.  THE CODE IS WIDENED, not
      the claim narrowed, and this file says which: the gate now takes a CENSUS
      of every figure-shaped token the section asserts and compares the whole
      MULTISET to the live measurements plus a DECLARED roster of the site's
      historical figures.  See the block above `FIGURE_TOKEN` for what the
      census does and does not cover, and N10-N14 of the negative control for
      it firing on the probes that were silent.

      ⚠️ MADE POSITION-AWARE 2026-07-30 (mg-8aae finding H-1, landed by
      mg-8eca).  A MULTISET IS INVARIANT UNDER A PERMUTATION.  Two DECLARED
      figures of equal length EXCHANGED with each other in ordinary prose
      leave the multiset identical, every designated statement correct and
      the length unchanged -- and the run stayed at exit 0 at 2 of 2 sites
      probed, with H8's own table then saying the `STATE.md` row SHRANK
      across mg-a2bd and the chain the whole finding was born in running
      backwards.  The gate measured a property the failure it guarded
      PRESERVES.  The roster is now an ORDERED list of slots and the census
      compares the SEQUENCE as well as the bag; N15-N18 of the negative
      control are the exchanges, and R1 of `code/hodge_leverage_repair_8eca/`
      runs them on disk against the real runner.

      ⚠️ MADE POSITION-AWARE OVER THE WHOLE RECORD 2026-07-31 (mg-9207
      findings E2/E2b/E3, landed by mg-ff3e).  THE INVARIANCE HAD MOVED
      RATHER THAN GONE AWAY.  An exchange has two halves -- the figures and
      the statements they hang on -- and making the census positional over
      the FIGURES left the LABELS invariant: exchanging H8's `before
      mg-a2bd` / `after mg-a2bd` row labels puts mg-8aae's own defect back
      (the table says the row SHRANK) with every figure token in its
      declared slot and the gate refuting NOTHING, at 3 of 3 label sites.
      The generator is that the gate compared a PROJECTION and each repair
      widened it BY ONE NAMED FIELD, so the next exchange moved into what
      was still dropped.  NAMING LABELS WOULD HAVE BOUGHT ONE MORE
      GENERATION.  Instead the projection is made LOSSLESS: `partition`
      cuts the section into (SEGMENTS, FIGURES) along a seam the record
      itself defines, the figures are compared to `ORDER` and the segments
      byte for byte to a declared record, and `rejoin(segments, figures) ==
      raw` is checked every run so "the two halves are the whole record" is
      MEASURED.  N19-N25 of the negative control are the label-side
      exchanges, and `code/hodge_leverage_repair_ff3e/` runs them on disk
      against the real runner.

  T2  TWO SITE COUNTS IN ONE COMMIT (F2).  §6's disposition table is counted
      row by row from the tree; §14's count word is read out of §14.  Neither
      is quoted from the audit.

  T3  THE DROPPED CONDITION (F3).  "the per-level max is attained exactly at
      the one-big-block face" is a conclusion of Theorem J PLUS the base case
      `lambda_2(F(A_m)) <= 1/2`.  Two checks: (a) which of the four sites
      carry the condition, read from the tree; (b) the condition is
      LOAD-BEARING rather than decorative -- re-derived here by evaluating
      Theorem J's closed form over every block-size multiset, under the
      verified base case and under a counterfactual one.  If the argmax is
      the one-big-block face under both, the condition is decorative and F3
      is wrong.  It is not.

  T4  A RULE ABOUT ENUMERATING A BRIEF (F4).  mg-a806's brief has six items;
      the rule's evidence paragraph said four, at two sites.  `STATE.md` was
      corrected by mg-ae62; the deliverable's §13 copy was not.  Both sites
      are read from the tree and reported separately -- a repair that fixed
      one site and left the other is this arc's most-repeated defect, and
      this landing must not report it as closed on one site's evidence.

Pure Python 3 + git.  No third-party packages.  Runtime ~1 s.
"""

import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DELIV = "docs/OneThird-Hodge-Side-Leverage.md"
STATE = "STATE.md"
HIST = "docs/state-history/attempt-mg-a3d4.md"

STRIKE = "1e61031"          # mg-a2bd, the audited commit
RESTRUCTURE = "57f962f"     # mg-34bf, the STATE.md restructure
LANDING = "bbe83b5"         # mg-e1d0, the commit this instrument shipped in
TREE = None                 # sentinel: the WORKING TREE, never a sha

RESULTS = []


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True, check=True).stdout


def blob(commit, path):
    """File contents at a commit, or None if it does not exist there."""
    r = subprocess.run(["git", "-C", REPO, "show", f"{commit}:{path}"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def tree(path):
    with open(os.path.join(REPO, path), encoding="utf-8") as fh:
        return fh.read()


def find_line(text, prefix):
    """The single line starting with `prefix`.  Located by CONTENT, never by
    line number: the row moves between commits and a frozen index would
    silently measure a different row."""
    hits = [l for l in text.split("\n") if l.startswith(prefix)]
    if len(hits) != 1:
        raise SystemExit(f"expected exactly 1 line starting {prefix!r}, got {len(hits)}")
    return hits[0]


def state_row(text):
    return find_line(text, "| **AMBER-POSITIVE")


def deliv_row(text):
    return find_line(text, "> **AMBER-POSITIVE")


def record(ok, detail):
    RESULTS.append((detail, ok))
    mark = {True: "[CONFIRMED]", False: "[REFUTED  ]", None: "[MEASURED ]"}[ok]
    print(f"  {mark} {detail}")


def head(title):
    print()
    print(title)
    print("-" * len(title))


def doc_num(v, signed=False):
    """A number in the format the documents write it: space thousands
    separator, U+2212 for a negative sign.  Used by the GATE to FORMAT what it
    has just measured and then compare the documents' own figure against that
    -- never to match a figure frozen into the source of this file."""
    s = f"{v:+,}" if signed else f"{v:,}"
    return s.replace(",", " ").replace("-", "−")


def flat(text):
    return " ".join(text.split())


def section(text, prefix):
    """The markdown section whose heading line starts with `prefix`, up to the
    next heading of the same or shallower level, heading included.  Located BY
    CONTENT, never by line number.

    ⚠️ A SITE IS A SECTION, NOT THE FILE THAT CONTAINS IT (mg-8a5c N7).  The
    gate this replaced anchored §14 on the whole deliverable, so the entire
    disclosure paragraph could be relocated verbatim into a new appendix at the
    end of the document and the gate would still pass."""
    lines = text.split("\n")
    starts = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    if len(starts) != 1:
        raise SystemExit(f"expected exactly 1 heading starting {prefix!r}, "
                         f"got {len(starts)}")
    i = starts[0]
    level = len(lines[i]) - len(lines[i].lstrip("#"))
    end = len(lines)
    for j in range(i + 1, len(lines)):
        lv = len(lines[j]) - len(lines[j].lstrip("#"))
        if 0 < lv <= level:
            end = j
            break
    return "\n".join(lines[i:end])


# --------------------------------------------------------------------------
# THE THREE SITES A5 IS RECORDED AT, AND HOW EACH ONE'S FIGURES ARE READ
#
# ⚠️ REBUILT 2026-07-30 (mg-8a5c finding F-1, landed by mg-a318).  The gate
# `e16e41c` shipped formatted what it had just measured -- right, and kept --
# and then asked whether that string OCCURRED SOMEWHERE in the file.  A
# PRESENCE TEST certifies that a correct value exists; it does not certify
# that the figure a reader meets is correct, and the corrected wording printed
# the live gap TWICE per site (once as the live figure, once as the tail of
# the chain `2 928 → 6 069 → −875 → +755 → …`, which ends at the current gap
# BY CONSTRUCTION).  So corrupting the sentence a reader actually reads left a
# correct copy standing and the run stayed green, at all three sites.
#
# What follows READS EACH FIGURE OUT OF THE STATEMENT THAT ASSERTS IT and
# compares it to the measurement.  The document's own words are the input; the
# measurement is the expected value.  A wrong figure at the site is a wrong
# figure to the gate, whatever else the file happens to contain.
#
# The duplicate itself is GONE rather than detected -- the chain's tail now
# points at the live figure instead of restating it -- and the gate requires
# EXACTLY ONE written occurrence per site so a second copy fires it.  That
# ordering is deliberate: a duplicated literal is a seam waiting to happen,
# and derivation removes the failure mode where a gate only detects it.
# --------------------------------------------------------------------------

# key -> (how this instrument names it, is it a LIVE figure that moves with
# the tree?).  A live figure must be written exactly once per site; a frozen
# one (the §14 copy) may legitimately recur in the quoted history.
FIGURES = {
    "gap":  ("gap, cell only", True),
    "both": ("gap, cell + relocated history", True),
    "cell": ("STATE.md row cell", True),
    "hist": ("relocated history (this row's own file)", True),
    "copy": ("deliverable §14 copy, frozen since mg-a806", False),
}


# --------------------------------------------------------------------------
# ⚠️ WIDENED 2026-07-30 (mg-835f finding G-1, landed by mg-8916).  THE CENSUS.
#
# The two checks above read the DESIGNATED STATEMENT at each site.  A reader
# reads the SECTION.  mg-835f wrote the sentence "the gap is now +9 999
# characters." into the STATE.md row, into §14 and into H8 -- in ordinary
# prose, length-preservingly, leaving every designated statement correct -- and
# the run stayed at exit 0 at 3 of the 3 sites.  So the sentence "the gate
# reads the figure at the site" was WIDER THAN THE CODE: the code read one
# statement, not the site.
#
# TWO REPAIRS WERE AVAILABLE AND THIS ONE WIDENS THE CODE.  The ticket's
# preferred repair -- remove the prose duplicate so the value lives in one
# place -- was measured first and there is nothing to remove: every live figure
# already occurs exactly once per site (that is the mg-a318 repair, and the
# WRITTEN ONCE check keeps it that way).  G-1 is not a duplicate that exists;
# it is a duplicate the gate would not see if one were written.  The other
# repair on offer was to narrow the printed claim to "structured occurrences
# only".  NEITHER WAS TAKEN: the code is widened so that the sentence a reader
# already meets becomes true.  Said plainly, because silently widening a gate
# and silently narrowing a claim are different repairs with different costs.
#
# HOW.  Every figure-shaped token at the site is enumerated and the whole
# MULTISET is compared to a declared expectation: the live figures at their
# measured values, plus a roster of the site's HISTORICAL figures, each with
# what it is.  An extra token fires; a missing one fires; a token whose count
# moved fires -- including a wrong prose figure that reuses a value already on
# the roster, which a set-membership test would pass.
#
# ⚠️ MADE POSITION-AWARE 2026-07-30 (mg-8aae finding H-1, landed by mg-8eca).
# A MULTISET IS INVARIANT UNDER A PERMUTATION, so the census above could not
# see one.  mg-8aae exchanged two DECLARED figures of equal length in ordinary
# prose -- `13 551` with `16 692` in H8's own mg-a2bd table, and the chain
# `2 928 → 6 069 → −875 → +755` run backwards in its last two terms -- and the
# runner stayed at exit 0 at 2 of 2 sites.  Every one of the three checks was
# satisfied: inside the section, not inside a marked quotation, figure-shaped,
# length-preserving, every designated statement still correct.  The section
# asserted two figures the wrong way round and the gate was silent, BECAUSE THE
# PROPERTY THE GATE MEASURED WAS INVARIANT UNDER THE FAILURE IT GUARDED.
#
# So the roster below is no longer a bag of counts: it is an ORDERED LIST of
# the figure tokens each site is licensed to carry, IN THE ORDER A READER MEETS
# THEM.  `ORDER` is the single declaration -- the multiset the census compares
# is DERIVED from it, and so is `LIVE_CENSUS`, so the two cannot drift apart.
# A transposition changes the sequence while preserving the multiset, and the
# sequence is what is compared.
#
# WHAT IT DOES NOT COVER, stated so this extent is not the next wide one:
#   * marked quotations are exempt, because `assertions()` strips them -- a
#     quotation of a withdrawn figure is not an assertion of it, which is the
#     convention the sites already run on and which `assertions` documents;
#   * a token outside the site is not read, because a site is a section;
#   * "figure-shaped" means this arc's own notation for a character count:
#     optionally signed, thousands separated by a space (`+23 771`, `48 846`),
#     or signed with three or more digits (`−875`, `+755`).  A bare `405` or a
#     ticket id is not a figure of this class and is not read.
#   * two occurrences of THE SAME token exchanged with each other are not
#     distinguishable by anything here, because they are the same token: the
#     sequence is over VALUES, and swapping equal values is the identity map.
#     Position is covered; identity of equal figures is not, and cannot be.
#
# AND IT IS FAIL-CLOSED, now in two ways: a NEW historical figure fires until
# it is entered on the roster with what it is, and an EXISTING one fires until
# its slot in `ORDER` is moved to where a reader now meets it.  That is a cost
# and it is the same cost as U5's -- an editor meets a red run for an honest
# edit.  It is the right direction for this arc: the roster IS the declaration
# the repair's own Appendix A rule asks for, kept where a checker reads it.
# --------------------------------------------------------------------------
FIGURE_TOKEN = re.compile(
    r"(?<![\w−+])(?:[−+]?\d{1,3}(?: \d{3})+|[−+]\d{3,})(?!\d)")

# site -> the figure tokens the section is licensed to assert, IN ORDER.
# `@key` is a LIVE figure, substituted at the value measured THIS RUN, never
# from a constant here; anything else is a historical token, which `HISTORICAL`
# below says what it is.  This list is the ONE declaration of both position and
# multiplicity: the multiset the census compares is derived from it.
ORDER = {
    "the STATE.md row": [
        "48 846",
        "2 928", "6 069", "−875", "+1 630", "+755", "−875",
        "@gap", "@cell", "@copy", "@hist", "@both",
        "−875",
        "2 928", "6 069", "−875", "+755",
    ],
    "§14": [
        "13 551", "16 692", "@copy",
        "2 928", "6 069", "−875", "+1 630", "+755", "+17 023",
        "@gap", "@both",
        "2 928", "6 069", "−875", "+755",
        "44 055",
    ],
    "H8": [
        "13 551", "16 692", "+3 141", "@copy", "2 928", "6 069",
        "9 748", "10 483", "@copy", "−875", "+9 608",
        "+1 630", "+5 785",
        "−875",
        "9 748", "11 378", "@cell",
        "10 483", "16 268", "@hist",
        "@copy", "@copy", "@copy",
        "−875", "+755", "@gap",
        "+9 608", "+17 023", "@both",
        "2 928", "6 069", "−875", "+755",
        "48 846", "10 483", "+9 608",
    ],
}

# site -> {token: what it is}.  Every historical figure a reader meets at the
# site, declared.  These are frozen by construction: each is a figure at a
# named past commit, and git does not move.  The COUNT is not written here --
# it is `ORDER`'s, counted, so a roster that says "twice" and a document that
# writes it three times cannot both be satisfied by editing one of them.
HISTORICAL = {
    "the STATE.md row": {
        "2 928":   "the clause mismatch A5 reports, before mg-a2bd",
        "6 069":   "the same mismatch after mg-a2bd more than doubled it",
        "−875":    "the cell-only gap at bbe83b5^, published by bbe83b5 as "
                   "current and WITHDRAWN",
        "+1 630":  "the characters bbe83b5 added to this cell in the commit "
                   "that measured it",
        "+755":    "the cell-only gap at bbe83b5, superseded",
        "48 846":  "genuine-join links checked for ledger row J -- a count "
                   "of links, not a length",
    },
    "§14": {
        "13 551":  "the STATE.md row before mg-a2bd",
        "16 692":  "the STATE.md row after mg-a2bd",
        "2 928":   "the clause mismatch A5 reports, before mg-a2bd",
        "6 069":   "the same mismatch after mg-a2bd",
        "−875":    "the cell-only gap at bbe83b5^, WITHDRAWN",
        "+1 630":  "the characters bbe83b5 added to the STATE.md cell",
        "+755":    "the cell-only gap at bbe83b5, superseded",
        "+17 023": "cell + relocated history at bbe83b5, superseded",
        "44 055":  "links enumerated over 4 <= n <= 6 -- a count of links, "
                   "not a length",
    },
    "H8": {
        "13 551":  "the STATE.md row before mg-a2bd",
        "16 692":  "the STATE.md row after mg-a2bd",
        "+3 141":  "what mg-a2bd added to the STATE.md row",
        "2 928":   "the clause mismatch A5 reports, before mg-a2bd",
        "6 069":   "the same mismatch after mg-a2bd",
        "9 748":   "the STATE.md row cell at bbe83b5^",
        "11 378":  "the STATE.md row cell at bbe83b5",
        "10 483":  "this file (the relocated history) at bbe83b5^",
        "16 268":  "this file at bbe83b5",
        "−875":    "the cell-only gap at bbe83b5^, WITHDRAWN",
        "+755":    "the cell-only gap at bbe83b5, superseded",
        "+9 608":  "cell + relocated history at bbe83b5^, understated",
        "+17 023": "cell + relocated history at bbe83b5, superseded",
        "+1 630":  "the characters bbe83b5 added to the STATE.md cell",
        "+5 785":  "the characters bbe83b5 added to this file",
        "48 846":  "genuine-join links checked for ledger row J",
    },
}

# DERIVED from `ORDER`, never written twice.  {site: {figure key: how many
# times the LIVE value is written at this site}} -- the shape the mg-8916 and
# mg-8aae instruments read.
LIVE_CENSUS = {
    site: {key: [e[1:] for e in seq if e.startswith("@")].count(key)
           for key in dict.fromkeys(e[1:] for e in seq if e.startswith("@"))}
    for site, seq in ORDER.items()
}


# --------------------------------------------------------------------------
# ⚠️ MADE POSITION-AWARE OVER THE WHOLE RECORD 2026-07-31 (mg-9207's E2/E2b/E3,
# landed by mg-ff3e).  THE INVARIANCE HAD MOVED RATHER THAN GONE AWAY.
#
# mg-8916 made the census a MULTISET of figure tokens.  mg-8aae exchanged two
# figures and the multiset did not move.  mg-8eca made it a SEQUENCE of figure
# tokens.  mg-9207 then exchanged the two LABELS instead -- H8's `mg-a2bd`
# table saying the `STATE.md` row SHRANK, with every figure token still in its
# declared slot and the length unchanged -- and the gate refuted NOTHING, at
# 3 of 3 label sites.  The reader-visible defect mg-8aae raised was
# reproducible from the OTHER HALF of the same exchange.
#
# WHAT GENERATES THE INSTANCES, which is the only question worth asking after
# the third one.  The gate declares a PROJECTION of the site and compares that
# projection to an expectation.  Whatever the projection drops is invisible,
# and each repair so far enlarged the projection BY ONE NAMED FIELD -- values,
# then order-of-values.  The complement was still everything else, so the next
# exchange simply moved into it.  Widening field by field buys one generation
# each, and the fix's author never sees the next one BECAUSE THEY ARE LOOKING
# AT THE REPORTED ONE.  Naming labels here would have bought a fourth.
#
# SO THE PROJECTION IS MADE LOSSLESS RATHER THAN WIDER.  The site is cut in two
# along a seam THE RECORD ITSELF DEFINES -- `partition` walks the figure-shaped
# tokens and returns (SEGMENTS, FIGURES) -- and both halves are compared, both
# positionally:
#
#   FIGURES   the asserted figure tokens, in order, against `ORDER`  -- (c)/(d)
#   SEGMENTS  everything else, byte for byte, in order, against the
#             DECLARED RECORD in `site_records.txt`                  -- (e)
#
# and `rejoin(segments, figures) == raw` is CHECKED EVERY RUN, per site, so
# "the two halves are the whole record" is a measurement rather than a
# sentence.  No field can be left behind because nobody named it: NO FIELD IS
# NAMED AT ALL.  Labels, table row headings, column alignment, the text inside
# a marked quotation and any field a later editor invents are in SEGMENTS the
# moment they are written, without this file being touched.
#
# THE COST, stated because it is the reason this was not done first: any edit
# to these three sections that is not a live measurement makes the run RED
# until the declared record is regenerated (`python3 verify_landing.py
# --reseal`).  That is one command, and its effect is a REVIEWABLE DIFF --
# which is why the declaration is the skeleton TEXT and not a sha256 of it.  A
# hash bump is a rubber stamp; a diff is a thing a reviewer can read.  And
# `--reseal` REFUSES to run while any other gate row is refuted, so a document
# whose figures are wrong cannot be blessed by resealing it.
#
# IT IS A DECLARATION AND NOT A DUPLICATE, which this arc distinguishes for a
# reason (mg-a318 F-1).  A duplicate is a second place a READER meets the
# claim, with nothing comparing the two, so one goes stale in silence.  The
# declared record is read by the gate alone and compared to the document on
# every run: a divergence IS the red run, so it cannot go stale quietly.
#
# WHAT IS STILL NOT COVERED, with the reason, because an omission is not
# checkable and a stated reason is:
#   * text OUTSIDE the site is not read, because a site is a section.  That is
#     the one projection that remains, it is unchanged since mg-8a5c, and it is
#     itself gated -- `section()` anchors BY CONTENT and N6 relocates a whole
#     disclosure out of §14 to show the gate notices.
#   * two occurrences of the SAME figure token exchanged with each other are
#     still the identity map on the artifact (mg-8eca), so there is nothing to
#     detect -- not a blind spot but an empty set.
# --------------------------------------------------------------------------
FIGURE_MARK = "⟦figure⟧"
RECORD_MARK = "⟦record⟧ "
RECORD_END = "⟦end⟧"
SITE_RECORDS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "site_records.txt")

# The MARKED QUOTATION convention, in ONE place.  `assertions` (what the
# designated readers and the census read) and `partition` (what the record is
# cut on) are both derived from it, so the two halves of the record cannot be
# read by two implementations that drift apart -- which is how the battery
# `e16e41c` shipped came to test a gate slightly unlike the live one.
QUOTE_PATTERNS = [re.compile(r'\*"(.+?)"\*', re.S),
                  re.compile(r"\*'(.+?)'\*", re.S)]


def quoted_spans(raw):
    """The (start, end) spans of the site's MARKED QUOTATIONS, merged and in
    order.  Offsets into `raw` itself, so the same convention can be applied
    without flattening the text first."""
    spans = sorted((m.start(), m.end())
                   for pat in QUOTE_PATTERNS for m in pat.finditer(raw))
    merged = []
    for s, e in spans:
        if merged and s < merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    return merged


def partition(raw):
    """THE WHOLE RECORD, cut in two along a seam the record defines.

    Returns (segments, figures) where `figures` is every figure-shaped token
    the site ASSERTS, in order, and `segments` is everything else, in order,
    with `len(segments) == len(figures) + 1` and

        rejoin(segments, figures) == raw

    EXACTLY -- which `census_gate` checks on every run, per site.  That
    equality is the whole point: it is what licenses the claim that (c)/(d)
    plus (e) cover the section, with nothing in neither half."""
    spans = quoted_spans(raw)
    segments, figures, last = [], [], 0
    for m in FIGURE_TOKEN.finditer(raw):
        if any(s <= m.start() < e for s, e in spans):
            continue                  # a quotation is not an assertion
        segments.append(raw[last:m.start()])
        figures.append(m.group())
        last = m.end()
    segments.append(raw[last:])
    return segments, figures


def rejoin(segments, figures):
    """The inverse of `partition`: interleave the two halves back together."""
    out = [segments[0]]
    for f, s in zip(figures, segments[1:]):
        out.append(f)
        out.append(s)
    return "".join(out)


def skeleton(raw):
    """THE SITE MINUS ITS ASSERTED FIGURES: every segment in order, with each
    figure token replaced by a position marker.  Stable from run to run --
    the live values are exactly what the marker hides -- so it moves only when
    somebody edits the section."""
    return FIGURE_MARK.join(partition(raw)[0])


def declared_records():
    """The DECLARED record of each site, read from `site_records.txt`.  Absent
    file or absent site is FAIL-CLOSED: the gate fires rather than skipping."""
    if not os.path.exists(SITE_RECORDS):
        return {}
    with open(SITE_RECORDS, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    out, name, buf = {}, None, []
    for l in lines:
        if l.startswith(RECORD_MARK):
            name, buf = l[len(RECORD_MARK):], []
        elif name is not None and l == RECORD_END:
            out[name], name = "\n".join(buf), None
        elif name is not None:
            buf.append(l)
    return out


def render_records(texts):
    """`site_records.txt` as it should read for these site texts."""
    parts = [
        "# THE DECLARED RECORD of each census site -- mg-ff3e, closing",
        "# mg-9207's E2/E2b/E3.  Each block is the SECTION with every ASSERTED",
        f"# figure token replaced by {FIGURE_MARK}: the half of the record the",
        "# figure census does NOT compare, frozen so that exchanging two LABELS",
        "# is not silent.  The figures themselves are declared by `ORDER` in",
        "# `verify_landing.py` and are checked by value and by slot.",
        "#",
        "# Regenerate with:  python3 verify_landing.py --reseal",
        "# It refuses while any other gate row is refuted, and the diff it",
        "# produces is meant to be READ -- that is why this is text and not a",
        "# sha256.",
    ]
    for name, _reader, _keys in SITES:
        sk = skeleton(texts[name])
        for l in sk.split("\n"):
            if l.startswith(RECORD_MARK) or l == RECORD_END:
                raise SystemExit(f"{name}: a line of the site collides with "
                                 f"the record delimiter: {l[:60]!r}")
        parts += [RECORD_MARK + name, sk, RECORD_END]
    return "\n".join(parts) + "\n"


def figure_sequence(raw):
    """Every figure-shaped token the site ASSERTS, IN THE ORDER A READER MEETS
    THEM.  Derived from `partition`, which is the one place the site is cut
    into figures and not-figures.  Marked quotations are exempt on the
    convention already in force at these sites: a quotation of a withdrawn
    figure is not an assertion of it.  ⚠️ Exempt from the CENSUS is not the
    same as unchecked -- since mg-ff3e a quoted figure sits in a SEGMENT and is
    frozen there byte for byte (N24)."""
    return partition(raw)[1]


def figure_tokens(raw):
    """The same tokens as a SORTED list -- the multiset view, kept because the
    census's licensing half is a multiset question and because two other
    instruments read it."""
    return sorted(figure_sequence(raw))


def expected_sequence(site, measured):
    """The figure tokens this site is licensed to carry, IN ORDER: the live
    figures AT THE VALUES MEASURED THIS RUN in their declared slots, and the
    historical roster in theirs."""
    return [measured[e[1:]] if e.startswith("@") else e for e in ORDER[site]]


def expected_census(site, measured):
    """The MULTISET of figure tokens this site is licensed to carry, counted
    off `expected_sequence`.  Returns (counter, collisions)."""
    want = {}
    for t in expected_sequence(site, measured):
        want[t] = want.get(t, 0) + 1
    live = {measured[e[1:]] for e in ORDER[site] if e.startswith("@")}
    collisions = sorted(t for t in HISTORICAL[site] if t in live)
    return want, collisions


def census_gate(name, raw, measured):
    """THE CENSUS, for one site.  Returns [(ok, detail), ...].

    Two questions, and they are different questions.  IS EVERY FIGURE LICENSED
    is a multiset question and the multiset answers it.  IS EACH LICENSED
    FIGURE WHERE A READER SHOULD MEET IT is a positional question, and a
    multiset is invariant under exactly the failure that asks it -- which is
    mg-8aae H-1.  Both are asked here, and both are recorded."""
    want, collisions = expected_census(name, measured)
    seq = figure_sequence(raw)
    got = {}
    for t in seq:
        got[t] = got.get(t, 0) + 1
    out = []
    undeclared = sorted({e for e in ORDER[name] if not e.startswith("@")}
                        - set(HISTORICAL[name]))
    unused = sorted(set(HISTORICAL[name]) - set(ORDER[name]))
    if collisions or undeclared or unused:
        why = []
        if collisions:
            why.append(f"{collisions} is declared as a historical figure AND "
                       "equals a live measurement this run, so the two cannot "
                       "be told apart by counting")
        if undeclared:
            why.append(f"{undeclared} holds a slot in ORDER and HISTORICAL "
                       "does not say what it is")
        if unused:
            why.append(f"{unused} is declared in HISTORICAL and holds no slot "
                       "in ORDER, so nothing checks it")
        out.append((False,
                    f"GATE @ {name}: CENSUS ROSTER -- " + "; ".join(why)
                    + ".  The roster must name the historical figure "
                    "differently, drop it, or give it the slot a reader meets "
                    "it in"))
    extra = sorted((t, got[t] - want.get(t, 0)) for t in got
                   if got[t] != want.get(t, 0))
    gone = sorted((t, want[t] - got.get(t, 0)) for t in want
                  if t not in got)
    if extra or gone:
        parts = [f"{t} appears {got.get(t, 0)}x, licensed {want.get(t, 0)}x"
                 for t, _ in extra]
        parts += [f"{t} is licensed {want[t]}x and appears 0x" for t, _ in gone]
        out.append((False,
                    f"GATE @ {name}: FIGURE CENSUS -- {len(parts)} unlicensed "
                    f"figure(s) at this site: " + "; ".join(parts)
                    + ".  Every figure a reader meets in this section must be "
                    "the live measurement or a DECLARED historical one; an "
                    "undeclared figure in ordinary prose is the wrong figure a "
                    "reader meets while the labelled statement stays right "
                    "(mg-835f G-1)"))
    else:
        out.append((True,
                    f"GATE @ {name}: FIGURE CENSUS -- all "
                    f"{sum(got.values())} figure token(s) a reader meets in "
                    f"this SECTION are licensed ({sum(LIVE_CENSUS[name].values())} "
                    f"live occurrence(s) at the values measured this run, "
                    f"{sum(1 for e in ORDER[name] if not e.startswith('@'))} "
                    "declared historical), and no other figure is asserted "
                    "here.  Prose is read, not only the designated statements"))

    # ⚠️ (d) THE POSITIONAL HALF (mg-8aae H-1, landed by mg-8eca).  The check
    # above is invariant under a permutation of the site's own declared
    # figures; this one is not, and it is the ONLY one that is not.
    exp = expected_sequence(name, measured)
    if seq == exp:
        out.append((True,
                    f"GATE @ {name}: FIGURE ORDER -- all {len(seq)} figure "
                    "token(s) are in the declared slot a reader meets them in. "
                    "The census above is a MULTISET and a multiset is invariant "
                    "under a permutation, so two declared figures exchanged in "
                    "ordinary prose passed it (mg-8aae H-1); this compares the "
                    "SEQUENCE, which a transposition changes"))
    else:
        i = next((k for k in range(min(len(seq), len(exp))) if seq[k] != exp[k]),
                 min(len(seq), len(exp)))
        moved = sorted(set(seq) & set(exp)
                       & {t for t in set(seq) | set(exp)
                          if seq.count(t) == exp.count(t)}
                       - {t for k, t in enumerate(exp)
                          if k < len(seq) and seq[k] == t})
        out.append((False,
                    f"GATE @ {name}: FIGURE ORDER -- the section asserts "
                    f"{len(seq)} figure token(s) and licenses {len(exp)}, and "
                    f"they first differ at occurrence {i + 1}: the section "
                    f"reads {seq[i] if i < len(seq) else '(end)'} where the "
                    f"roster licenses {exp[i] if i < len(exp) else '(end)'}"
                    + (f".  Same multiplicity, different slot: {moved}"
                       if moved else "")
                    + ".  A figure attached to the wrong statement is the wrong "
                    "figure a reader meets, and exchanging two of them leaves "
                    "the census above IDENTICAL (mg-8aae H-1)"))

    # ⚠️ (e) THE OTHER HALF OF THE RECORD (mg-9207 E2/E2b/E3, landed by
    # mg-ff3e).  (c) and (d) are about the FIGURES.  This is about EVERYTHING
    # ELSE, and the row above it is the proof that between them they are the
    # section -- which is the difference between fixing the set and fixing the
    # next field.
    segments, seqf = partition(raw)
    rebuilt = rejoin(segments, seqf)
    out.append((rebuilt == raw,
                f"GATE @ {name}: RECORD PARTITION -- the section is "
                f"{len(seqf)} asserted figure token(s) and {len(segments)} "
                f"segment(s) between them, and re-interleaving the two halves "
                f"reproduces it BYTE FOR BYTE ({len(rebuilt)} of {len(raw)} "
                f"chars).  This is what licenses 'the WHOLE record is "
                f"compared': the figures are checked by FIGURE CENSUS and "
                f"FIGURE ORDER, everything else by SITE RECORD, and nothing "
                f"is in neither.  No field is named, so none can be left "
                f"behind because nobody named it"))
    got = FIGURE_MARK.join(segments)
    want = declared_records().get(name)
    if want is None:
        out.append((False,
                    f"GATE @ {name}: SITE RECORD -- no record is declared for "
                    f"this site in {os.path.basename(SITE_RECORDS)}, so the "
                    "half of the section that is not a figure is compared "
                    "against nothing.  FAIL-CLOSED: a missing declaration is "
                    "the same silence a missing check is.  Regenerate with "
                    "`python3 verify_landing.py --reseal`"))
    elif got == want:
        out.append((True,
                    f"GATE @ {name}: SITE RECORD -- the "
                    f"{sum(len(s) for s in segments):,} "
                    f"chars of this section that are NOT asserted figures are "
                    f"byte-identical to the declared record, in order.  A "
                    f"MULTISET is invariant under exchanging two figures "
                    f"(mg-8aae H-1) and a SEQUENCE OF FIGURES is invariant "
                    f"under exchanging the two LABELS they hang on (mg-9207 "
                    f"E2/E2b/E3); this compares the other half, so neither "
                    f"exchange is silent"))
    else:
        gl, wl = got.split("\n"), want.split("\n")
        i = next((k for k in range(min(len(gl), len(wl))) if gl[k] != wl[k]),
                 min(len(gl), len(wl)))
        out.append((False,
                    f"GATE @ {name}: SITE RECORD -- the section's NON-FIGURE "
                    f"text differs from the declared record: "
                    f"{len(gl)} line(s) against {len(wl)} declared, first "
                    f"differing at line {i + 1} -- the section reads "
                    f"{(gl[i] if i < len(gl) else '(end)')[:90]!r} where the "
                    f"record declares "
                    f"{(wl[i] if i < len(wl) else '(end)')[:90]!r}.  A LABEL "
                    "exchanged with another label moves no figure and leaves "
                    "FIGURE CENSUS and FIGURE ORDER green, which is how H8's "
                    "table came to say the row SHRANK across mg-a2bd with the "
                    "gate silent (mg-9207 E2).  If this edit is intended, "
                    "`python3 verify_landing.py --reseal` and READ THE DIFF"))
    return out


def assertions(raw):
    """The site's text with its MARKED QUOTATIONS removed.

    Every one of these sites keeps the wording it corrected, as a quotation of
    what was struck -- that is deliberate and is itself gated above.  But a
    quotation of a withdrawn figure is not an assertion of it, and a gate that
    reads one cannot tell the live figure from the one it replaced: §14 quotes
    *"... sits +9 608 characters above this copy"* in the same shape as the
    sentence that states the live figure.  So the gate reads ASSERTIONS.

    ⚠️ The spans come from `quoted_spans`, the SAME function `partition` cuts
    the record on (mg-ff3e) -- here applied to the FLATTENED text and there to
    the raw text, but one convention in one place.  Two implementations of it
    is how the two halves of the record would come to disagree about which
    bytes are in neither."""
    f = flat(raw)
    out, last = [], 0
    for s, e in quoted_spans(f):
        out.append(f[last:s])
        out.append(" ⟨struck quotation⟩ ")
        last = e
    out.append(f[last:])
    return "".join(out)


def read_state_row(raw):
    """The figures as the `STATE.md` row itself states them."""
    f = assertions(raw)
    return {
        "gap":  re.findall(r"cell-only gap \*\*([−+][\d ]+?)\*\*", f),
        "cell": re.findall(r"cell \*\*([\d ]+?)\*\* characters against", f),
        "copy": re.findall(r"§14's frozen \*\*([\d ]+?)\*\*", f),
        "hist": re.findall(r"relocated history \*\*([\d ]+?)\*\*", f),
        "both": re.findall(r"cell \+ history \*\*([−+][\d ]+?)\*\*", f),
    }


def read_deliv_14(raw):
    """The figures as the deliverable's §14 states them.  §14 publishes two."""
    f = assertions(raw)
    return {
        "gap":  re.findall(r"cell-only gap \*\*([−+][\d ]+?)\*\*", f),
        "both": re.findall(r"sits \*\*([−+][\d ]+?)\*\* characters above this copy", f),
    }


def read_hist_h8(raw):
    """The `AFTER mg-8e30` column of H8's three-column table -- the column a
    reader of H8 is told is the live one.  Read out of the table by ROW LABEL,
    so a figure that is right in one of the historical columns and wrong in the
    live one is a failure, which is the whole point."""
    lines = raw.split("\n")
    heads = [i for i, l in enumerate(lines)
             if "AFTER mg-8e30" in l and "at bbe83b5^" in l]
    if len(heads) != 1:
        return {}
    labels = {"STATE.md row cell": "cell",
              "this file (the relocated history)": "hist",
              "deliverable §14 copy (frozen since mg-a806)": "copy",
              "gap, cell only": "gap",
              "gap, cell + relocated history": "both"}
    out = {k: [] for k in labels.values()}
    for l in lines[heads[0] + 1:]:
        if l.strip().startswith("```"):
            break
        cols = re.split(r"\s{2,}", l.strip())
        if len(cols) == 4 and cols[0] in labels:
            out[labels[cols[0]]].append(cols[3])
    return out


SITES = [
    ("the STATE.md row", read_state_row, ("gap", "both", "cell", "hist", "copy")),
    ("§14",              read_deliv_14,  ("gap", "both")),
    ("H8",               read_hist_h8,   ("gap", "both", "cell", "hist", "copy")),
]


def site_texts():
    """The three sites, each anchored to the SECTION that records A5."""
    return {
        "the STATE.md row": state_row(tree(STATE)),
        "§14":              section(tree(DELIV), "## §14 — `STATE.md` row, as landed"),
        "H8":               section(tree(HIST), "### H8 — "),
    }


def figure_gate(texts, measured):
    """THE FIGURE GATE.  Returns [(ok, detail), ...].

    THIS FUNCTION IS THE GATE.  T1 calls it on the tree and the negative
    control calls it on mutated copies of the same texts -- there is no second
    implementation to drift out of step with it, which is how the battery
    `e16e41c` shipped came to test a gate slightly unlike the live one.

    Three checks, and the third is the mg-8916 widening:
      (a) AT THE SITE -- the value the document writes in the statement that
          asserts it, compared to what this run measured;
      (b) WRITTEN ONCE -- a live figure occurs exactly once in the site, so
          nothing can go stale in one copy while another satisfies a check.
      (c) THE CENSUS -- every figure-shaped token the SECTION asserts is either
          the live measurement or a declared historical figure, at the declared
          multiplicity.  (a) and (b) read the designated statements; a reader
          reads the prose beside them, and (c) is that prose (mg-835f G-1).
    """
    out = []
    for name, _reader, _keys in SITES:
        out.extend(census_gate(name, texts[name], measured))
    for name, reader, keys in SITES:
        got = reader(texts[name])
        for key in keys:
            label, live = FIGURES[key]
            want = measured[key]
            said = got.get(key) or []
            if len(said) != 1:
                out.append((False,
                            f"GATE @ {name}: '{label}' -- expected exactly 1 "
                            f"statement of it at this site, found {len(said)} "
                            f"{said}.  A figure a reader cannot find, or finds "
                            f"twice, is not a figure this gate can stand behind"))
                continue
            out.append((said[0] == want,
                        f"GATE @ {name}: '{label}' READ AT THE SITE = "
                        f"{said[0]}, MEASURED THIS RUN = {want}"))
            if live:
                n = flat(texts[name]).count(want)
                out.append((n == 1,
                            f"GATE @ {name}: '{label}' is WRITTEN ONCE -- {want} "
                            f"occurs {n}x in this site.  A second written copy "
                            f"must instead DERIVE from the first by pointing at "
                            f"it; that is what removes the failure mode"))
    return out


# --------------------------------------------------------------------------
# T1 -- THE ENLARGEMENT
# --------------------------------------------------------------------------
def t1():
    head("TARGET 1 (F1) -- THE FINDING WAS ENLARGED WHILE A SENTENCE SAID IT WAS UNCHANGED")
    print("""mg-d39d A5 (MODERATE, open): §14 asserts the `STATE.md` row 'carries the
same clauses'; it does not.  mg-a2bd edited that paragraph and did not land A5.
The question this target answers is not whether A5 was landed -- the commit says
three times that it was not -- but whether the same commit ENLARGED it, and
whether the enlargement was disclosed anywhere.
""")

    chain = [(f"{STRIKE}^", "before mg-a2bd"),
             (STRIKE, "after  mg-a2bd"),
             (f"{RESTRUCTURE}^", "before mg-34bf restructure"),
             (RESTRUCTURE, "after  mg-34bf restructure"),
             (f"{LANDING}^", "before mg-e1d0 (this instrument's landing)"),
             (LANDING, "at     mg-e1d0 -- the commit that printed the row ABOVE as current"),
             (TREE, "the WORKING TREE -- this run's own side of the edit")]

    print("  commit-by-commit, all three files located BY CONTENT, not by line")
    print("  number.  The last row is the TREE and is deliberately NOT a sha: a")
    print("  transcript that embeds the commit it happened to be run at can never")
    print("  regenerate at any later one, and reading the tree rather than HEAD is")
    print("  what makes a pre-commit run report the POST-commit state.")
    print()
    print(f"    {'commit':<10} {'STATE.md row':>13} {'row history':>12} "
          f"{'§14 copy':>10} {'gap':>10}  when")
    rows = {}
    for ref, label in chain:
        if ref is TREE:
            st, dl, hs, name = tree(STATE), tree(DELIV), tree(HIST), "tree"
        else:
            st, dl, hs = blob(ref, STATE), blob(ref, DELIV), blob(ref, HIST)
            name = git("rev-parse", "--short", ref).strip()
        a, b = len(state_row(st)), len(deliv_row(dl))
        h = len(hs) if hs is not None else None
        rows[ref] = (a, b, h)
        hcol = f"{h:>12,}" if h is not None else f"{'—':>12}"
        print(f"    {name:<10} {a:>13,} {hcol} {b:>10,} {a - b:>+10,}  {label}")
    print()

    a0, b0, _ = rows[f"{STRIKE}^"]
    a1, b1, _ = rows[STRIKE]
    record(None,
           f"mg-a2bd: STATE.md row {a0:,} -> {a1:,} chars (+{a1 - a0:,}); "
           f"§14 copy {b0:,} -> {b1:,} (+{b1 - b0:,})")
    record(a1 - b1 > 2 * (a0 - b0) - 1 and a0 - b0 == 2928 and a1 - b1 == 6069,
           "the mismatch A5 reports MORE THAN DOUBLED in the commit that edited "
           f"the paragraph: {a0 - b0:,} -> {a1 - b1:,} chars")

    # Both files in one commit?
    touched = git("show", "--name-only", "--format=", STRIKE).split()
    record(STATE in touched and DELIV in touched,
           f"one commit, both files: `{STRIKE}` touches {STATE} and {DELIV}")

    # The inserted sentence, and the sentence left standing.
    d_before, d_after = blob(f"{STRIKE}^", DELIV), blob(STRIKE, DELIV)
    ins = "row below is\nUNCHANGED by mg-a2bd's strike"
    ins_flat = "row below is UNCHANGED by mg-a2bd's strike"
    false_sentence = "the corresponding `STATE.md` row carries the same clauses"

    def has(text, needle):
        return needle in " ".join(text.split())

    record(not has(d_before, ins_flat) and has(d_after, ins_flat),
           "mg-a2bd INSERTED 'the row below is UNCHANGED by mg-a2bd's strike of "
           "G″, and that is a fact rather than an omission'")
    record(has(d_before, false_sentence) and has(d_after, false_sentence),
           "and LEFT STANDING the sentence A5 is about -- "
           f"'{false_sentence}' -- present before and after")

    # Was the enlargement disclosed?  Search the commit message and the tree.
    msg = git("log", "-1", "--format=%B", STRIKE)
    disclosed = re.search(r"A5", msg) and re.search(r"enlarg|widen|doubl|gap", msg, re.I)
    record(not disclosed,
           "the enlargement is NOT disclosed in `%s`'s commit message "
           "(it declares A2-A8 unlanded, which is a different act)" % STRIKE)

    # ---- and now the CURRENT state, which is not the state A5 was opened on.
    print()
    print("  THE CURRENT GAP, MEASURED IN THE TREE THIS RUN IS PART OF -- and the")
    print("  metric A5 was opened on no longer means what it meant, which is")
    print("  itself the thing a reader must be told:")
    print()
    aH, bH, histlen = rows[TREE]
    hist = tree(HIST)
    print(f"    STATE.md row cell                        : {aH:>7,} chars")
    print(f"    relocated per-row history ({os.path.basename(HIST)}) : {histlen:>7,} chars")
    print(f"    STATE.md row, cell + relocated history    : {aH + histlen:>7,} chars")
    print(f"    §14 copy (frozen since mg-a806)           : {bH:>7,} chars")
    print(f"    gap, cell only                            : {aH - bH:>+7,} chars")
    print(f"    gap, cell + relocated history             : {aH + histlen - bH:>+7,} chars")
    print()

    # ⚠️ This line used to read "the SIGN of the cell-only gap has FLIPPED",
    # scored as `aH < bH`, and the three documents printed the −875 it went
    # with.  Both were true at `bbe83b5^` and false at `bbe83b5`, because
    # `bbe83b5` added chars to the cell it was measuring.  The durable claim is
    # not the sign at any one commit -- it is that the char gap moves in BOTH
    # directions while the clause mismatch only grows, which is exactly why a
    # char count cannot stand in for it.  (mg-f922 B/C, landed by mg-8e30.)
    gaps = [rows[r][0] - rows[r][1]
            for r in (f"{STRIKE}^", STRIKE, RESTRUCTURE, f"{LANDING}^", LANDING, TREE)]
    deltas = [g2 - g1 for g1, g2 in zip(gaps, gaps[1:])]
    record(any(d < 0 for d in deltas) and any(d > 0 for d in deltas),
           "the cell-only gap is NON-MONOTONE across the chain ("
           + " -> ".join(f"{g:+,}" for g in gaps)
           + ") while the clause mismatch below only grew -- so a char count "
             "does not measure it, in EITHER direction")
    grew = rows[LANDING][0] - rows[f"{LANDING}^"][0]
    record(rows[f"{LANDING}^"][0] - rows[f"{LANDING}^"][1] == -875 and grew > 0,
           f"and the −875 this instrument's own landing printed as CURRENT is "
           f"the figure at its PARENT: `{LANDING}` added {grew:+,} chars to the "
           "cell it was measuring, so the figure was stale in the commit that "
           "published it -- the defect this instrument exists to check for, "
           "one generation on (mg-f922 B/C)")
    record(None,
           "so this landing records the CLAUSE mismatch, measured below, and "
           "records the char history as history rather than as the live figure")

    # Clause-level probe: clauses asserted in the STATE.md row (cell or its
    # relocated history) and absent from §14.  Probes are phrased as content,
    # not as quotations of the audit.
    probes = [
        ("the one control gap the deliverable named itself is CLOSED",
         ["control gap the deliverable named itself", "CLOSED by the audit"]),
        ("the second-generation audit mg-d39d and its 1 BROKEN item",
         ["SECOND-GENERATION AUDIT"]),
        ("ledger row J / the 48 846 genuine-join links",
         ["48 846", "48 846"]),
        ("row G″ struck, with the mechanism recorded",
         ["G″"]),
        ("the A2-A8 not-landed declaration",
         ["NOT landed"]),
        ("the per-row history links added by the restructure",
         ["row history H1"]),
    ]
    state_all = state_row(tree(STATE)) + "\n" + hist
    d14 = deliv_row(tree(DELIV))
    print("  clause probes -- asserted by the STATE.md row, absent from §14:")
    missing = 0
    for label, needles in probes:
        in_state = any(n in state_all for n in needles)
        in_d14 = any(n in d14 for n in needles)
        if in_state and not in_d14:
            missing += 1
            print(f"    [ONLY IN STATE.md] {label}")
        elif in_state and in_d14:
            print(f"    [IN BOTH         ] {label}")
        else:
            print(f"    [NOT IN STATE.md ] {label}")
    print()
    record(missing >= 5,
           f"{missing} of {len(probes)} probed clauses are asserted by the "
           "STATE.md row and by nothing in §14 -- A5 stands, on clauses rather "
           "than on chars")

    # ---- THE GATE: what this landing leaves in the tree.
    #
    # ⚠️ EVERY CHECK BELOW IS ANCHORED TO THE SITE THAT RECORDS A5 -- the
    # `STATE.md` row, the deliverable's §14 SECTION, and H8 -- and not to the
    # file that contains it (mg-8a5c F-1 and N7, landed by mg-a318).  A gate
    # satisfied from elsewhere in the file is a gate on the copy nobody reads.
    print()
    texts = site_texts()
    flat_row_now = flat(texts["the STATE.md row"])
    flat_d14_now = flat(texts["§14"])
    flat_h8_now = flat(texts["H8"])
    print(f"  the three sites, anchored to the SECTION that records A5:")
    print(f"    the STATE.md row  {len(flat_row_now):>7,} chars (the row itself)")
    print(f"    §14               {len(flat_d14_now):>7,} chars (the section, "
          f"not {len(flat(tree(DELIV))):,} for the whole deliverable)")
    print(f"    H8                {len(flat_h8_now):>7,} chars (the section, "
          f"not {len(flat(tree(HIST))):,} for the whole file)")
    print()
    # THE EXTENT, PRINTED (mg-a4ef's convention; widened by mg-8916).  A gate
    # that does not print what it covers invites the reader to assume it covers
    # the section when it covers one sentence -- which is mg-835f G-1 exactly.
    print("  EXTENT of the figure gate below, printed rather than assumed:")
    print("    (a) the DESIGNATED STATEMENT at each site, read and compared;")
    print("    (b) each LIVE figure written exactly once per site;")
    print("    (c) a CENSUS of every figure-shaped token the SECTION asserts --")
    print("        prose included -- against the live values plus a declared")
    print("        historical roster.  Marked quotations are exempt by the")
    print("        convention `assertions()` states; text outside the section is")
    print("        not read, because a site is a section (mg-835f G-1/mg-8916);")
    print("    (d) and each of those tokens IN THE SLOT A READER MEETS IT IN.")
    print("        (c) alone is a MULTISET and is invariant under a permutation,")
    print("        so two declared figures EXCHANGED in ordinary prose passed it")
    print("        at 2 of 2 sites (mg-8aae H-1); (d) compares the SEQUENCE.")
    print("        NOT covered by (d): two occurrences of the SAME token")
    print("        exchanged, which is the identity map on values (mg-8eca).")
    print("    (e) and EVERYTHING ELSE IN THE SECTION -- every byte that is not")
    print("        an asserted figure token -- byte for byte, in order, against")
    print("        the declared record in `site_records.txt`.  (c) and (d) are")
    print("        a projection onto the figures, and a projection is invariant")
    print("        under any permutation of what it drops: exchanging the two")
    print("        LABELS instead of the two figures was silent at 3 of 3 sites")
    print("        (mg-9207 E2/E2b/E3).  (a)-(d) plus (e) are the WHOLE record,")
    print("        and that is MEASURED rather than claimed -- the RECORD")
    print("        PARTITION row re-interleaves the two halves and compares the")
    print("        result to the section byte for byte.  No field is named, so")
    print("        a field added later is covered the moment it is written.")
    for name, _r, _k in SITES:
        want, _c = expected_census(name, {"gap":  doc_num(aH - bH, signed=True),
                                          "both": doc_num(aH + histlen - bH, signed=True),
                                          "cell": doc_num(aH), "hist": doc_num(histlen),
                                          "copy": doc_num(bH)})
        # ⚠️ THE SHAPE OF THIS LINE IS LOAD-BEARING and is deliberately left
        # alone by mg-8eca: mg-8aae's A1 re-counts the printed extent by
        # parsing it, with a tokenizer sharing no regex with this file's.  An
        # instrument that raised a finding must be able to re-run unmodified
        # against the repair that answers it, so the slot count goes on its own
        # line rather than into this one.
        print(f"        {name:<20} {sum(want.values()):>3} licensed figure tokens "
              f"({len(HISTORICAL[name])} historical values declared)")
        print(f"        {'':<20} {len(ORDER[name]):>3} declared SLOTS, in the "
              "order a reader meets them (mg-8eca)")
    print()

    false_now = "the corresponding `STATE.md` row carries the same clauses"
    # It must survive ONLY as a quotation of what was struck, never as an
    # assertion -- a strike that deletes the sentence without trace leaves a
    # reader unable to check what was struck.
    occurrences = flat_d14_now.count(false_now)
    quoted = flat_d14_now.count('used to end *"and ' + false_now + '"*')
    record(occurrences == 1 and quoted == 1,
           f"GATE: the false sentence is STRUCK -- it appears {occurrences} time "
           f"in §14 and {quoted} of those is inside 'used to end \"...\"', i.e. "
           "quoted as the struck text and asserted nowhere")
    record("2 928 → 6 069" in flat_d14_now and "2 928 → 6 069" in flat_row_now,
           "GATE: the enlargement 2 928 -> 6 069 is stated at BOTH the §14 "
           "section and the place A5 is recorded (the STATE.md row)")

    # THE FIGURE GATE.  Every needle is FORMATTED from the measurement above,
    # never from a constant in this file -- and every figure is READ OUT OF the
    # statement that asserts it and compared, never searched for.  See the
    # header comment on `figure_gate`.
    measured = {"gap":  doc_num(aH - bH, signed=True),
                "both": doc_num(aH + histlen - bH, signed=True),
                "cell": doc_num(aH),
                "hist": doc_num(histlen),
                "copy": doc_num(bH)}
    for ok, detail in figure_gate(texts, measured):
        record(ok, detail)

    record("row history H8" in flat_row_now,
           "GATE: and the row points at H8, so the third site is reachable from "
           "the first")
    side = "measured AFTER this commit's own edit"
    record(all(side in t for t in (flat_row_now, flat_d14_now, flat_h8_now)),
           f"GATE: and every site says WHICH SIDE OF THE EDIT its figure is on "
           f"-- '{side}' at all three.  A measurement of something the same "
           "commit modifies is only checkable from the post-commit state")
    # THE DERIVATION CLAUSE.  The structural half of the mg-8a5c repair is that
    # the chain's tail POINTS AT the live figure instead of restating it.  A
    # reader must be told that, or the single occurrence looks like an omission
    # and the next editor helpfully writes the number back in.
    derive = "the live cell-only gap given above"
    record(derive in flat_row_now and derive in flat_d14_now
           and "`AFTER mg-8e30`" in flat_h8_now,
           f"GATE: and the chain's last term DERIVES from the live figure "
           f"rather than restating it -- '{derive}' at the row and §14, and a "
           "pointer to the AFTER column at H8.  The figure is written once per "
           "site; every later mention refers to that occurrence")
    record("A5 itself is still NOT landed" in flat_row_now
           and "remains pm-onethird's to size and is NOT done here" in flat_d14_now,
           "GATE: and both say A5 is MARKED, not landed -- marking a finding and "
           "landing it are also different acts")


# --------------------------------------------------------------------------
# T2 -- TWO SITE COUNTS
# --------------------------------------------------------------------------
def t2():
    head("TARGET 2 (F2) -- TWO SITE COUNTS IN ONE COMMIT")
    d_at_strike = blob(STRIKE, DELIV)

    def count_table(text):
        """Rows of §6's disposition table, counted from the table itself."""
        lines = text.split("\n")
        start = next(i for i, l in enumerate(lines)
                     if l.startswith("| site | what it was | disposition |"))
        n = 0
        for l in lines[start + 2:]:
            if not l.startswith("|"):
                break
            n += 1
        return n

    def count_word(text):
        flat = " ".join(text.split())
        m = re.search(r"\*\*(\w+) sites, all now carrying the strike", flat)
        return m.group(1) if m else None

    n_rows = count_table(d_at_strike)
    word = count_word(d_at_strike)
    record(None, f"§6 table, counted row by row at `{STRIKE}`: {n_rows} sites")
    record(word is not None and word.lower() == "three" and n_rows == 3,
           f"§6's prose says '{word} sites' and its table has {n_rows} rows -- these agree")

    flat_before = " ".join(blob(f"{STRIKE}^", DELIV).split())
    flat_after = " ".join(d_at_strike.split())
    s14 = "The strike therefore touches §6 and the ledger and nothing else."
    record(s14 not in flat_before and s14 in flat_after,
           "§14's '%s' was added by the SAME commit" % s14)
    record(True,
           "so one commit reports THREE (§6) and TWO (§14) for the same object "
           "-- exactly the shape STATE.md's own Appendix A warns about")

    # ---- THE GATE: the state this landing leaves in the tree.
    d_now = tree(DELIV)
    flat_now = " ".join(d_now.split())
    quoted14 = "used to end `" + s14[0].lower() + s14[1:-1] + "`"
    record(s14 not in flat_now and quoted14 in flat_now,
           "GATE: §14 no longer ASSERTS a second site count -- the sentence "
           "survives only as the quotation of what was struck")
    record(count_table(d_now) == 3 and count_word(d_now).lower() == "three",
           f"GATE: §6 remains the single source, {count_table(d_now)} table rows "
           f"and prose saying '{count_word(d_now)}' -- unchanged by this landing")
    record(flat_now.count("THREE sites, as §6's own") == 1,
           "GATE: §14 now defers to §6's table for the count rather than "
           "carrying an independent one")


# --------------------------------------------------------------------------
# T3 -- THE DROPPED CONDITION
# --------------------------------------------------------------------------
def t3():
    head("TARGET 3 (F3) -- A CONDITION DROPPED IN THE SUMMARY")
    print("""Theorem G gives `lambda_2(F(A_m)) >= 1/2` in BOTH directions and no upper
bound.  Concluding that the per-level max is attained AT the one-big-block face
needs J plus the computational base case `lambda_2(F(A_m)) <= 1/2`.  Part (a):
which sites carry it.  Part (b): whether it is load-bearing.
""")
    d, s = tree(DELIV), tree(STATE)
    flat_d, flat_s = " ".join(d.split()), " ".join(s.split())

    cond_markers = ["lambda_2(F(A_b)) <= 1/2", "λ₂(F(A_b)) ≤ 1/2",
                    "λ₂(F(A_m)) ≤ 1/2", "base case"]

    def carries(segment):
        return any(m in segment for m in cond_markers)

    def near(line, anchor="one-big-block face", span=700):
        k = line.find(anchor)
        return line[max(0, k - span):k + span] if k >= 0 else ""

    def sites(state_text, deliv_text):
        fd = " ".join(deliv_text.split())
        i, j = fd.find("The second consequence:"), fd.find("Why this is structural")
        return [
            ("deliverable §6.1 (the body)", fd[i:j]),
            ("deliverable ledger row G′", find_line(deliv_text, "| **G'** |")),
            ("STATE.md row (the summary)", near(state_row(state_text))),
            ("STATE.md Appendix A tally bullet",
             near(find_line(state_text, "- **Over-wide AND FALSE"))),
        ]

    print("  the four sites, at the audited commit and in the tree this landing leaves:")
    print()
    print(f"    {'site':<36} {'at ' + STRIKE:>14} {'in the tree':>14}")
    before = dict(sites(blob(STRIKE, STATE), blob(STRIKE, DELIV)))
    after = dict(sites(s, d))
    for label in before:
        print(f"    {label:<36} {'carries' if carries(before[label]) else 'DROPS IT':>14}"
              f" {'carries' if carries(after[label]) else 'DROPS IT':>14}")
    print()
    record(sum(1 for v in before.values() if not carries(v)) == 2,
           f"at `{STRIKE}` the condition was carried by the two BODY sites and "
           "dropped by the two SUMMARY sites -- the finding, re-measured")
    record(all(carries(v) for v in after.values()),
           "GATE: all four sites now carry the condition")

    # ---- (b) is the condition load-bearing?
    print()
    print("  IS THE CONDITION LOAD-BEARING?  Theorem J's closed form, evaluated over")
    print("  every block-size multiset of every level of A_n, n <= 9 -- once with the")
    print("  verified base case lambda_2(F(A_b)) = 1/2, once with a counterfactual")
    print("  lambda_2(F(A_4)) = 9/10.  Nothing here is quoted; J is applied.")
    print()

    def multisets(total, maxpart):
        """Partitions of `total` into parts >= 1, each <= maxpart (block excesses)."""
        if total == 0:
            yield ()
            return
        for p in range(min(total, maxpart), 0, -1):
            for rest in multisets(total - p, p):
                yield (p,) + rest

    def lam2(b, base):
        """lambda_2(F(A_b)) for a factor of a link.  b = block size >= 2."""
        return base.get(b, 0.5) if b >= 3 else 0.0

    def scan(base):
        """For each (n, i): the argmax block-size multiset under J."""
        out = {}
        for n in range(4, 10):
            for i in range(0, n - 2):
                D = n - i - 3
                if D < 1:
                    continue
                # non-singleton blocks: excesses (b_j - 1) summing to n-i-2 = D+1
                best, arg = None, None
                for exc in multisets(D + 1, D + 1):
                    blocks = tuple(e + 1 for e in exc)
                    val = max([(bj - 2) / D * lam2(bj, base) for bj in blocks]
                              + [-1.0 / D])
                    if best is None or val > best + 1e-12:
                        best, arg = val, blocks
                out[(n, i)] = (best, arg)
        return out

    true_base = {b: 0.5 for b in range(3, 10)}
    cf_base = dict(true_base)
    cf_base[4] = 0.9

    a = scan(true_base)
    b = scan(cf_base)

    def is_one_big_block(blocks):
        return len(blocks) == 1

    bad_true = [k for k, (v, blk) in a.items() if not is_one_big_block(blk)]
    bad_cf = [k for k, (v, blk) in b.items() if not is_one_big_block(blk)]

    record(not bad_true,
           f"under the verified base case the argmax is the one-big-block face at "
           f"ALL {len(a)} levels of A_4..A_9 -- the claim is TRUE on its population")
    record(bool(bad_cf),
           f"under the counterfactual lambda_2(F(A_4)) = 9/10 it FAILS at "
           f"{len(bad_cf)} of {len(b)} levels, first at "
           f"A_{bad_cf[0][0]}, i = {bad_cf[0][1]}: argmax {b[bad_cf[0]][1]} "
           f"at {b[bad_cf[0]][0]:.3f} > 1/2")
    record(True,
           "so the base case is LOAD-BEARING, not decorative: the summary that "
           "drops it attributes to Theorem J alone a conclusion J does not carry")


# --------------------------------------------------------------------------
# T4 -- THE BRIEF
# --------------------------------------------------------------------------
def t4():
    head("TARGET 4 (F4) -- A RULE ABOUT ENUMERATING A BRIEF, MIS-ENUMERATING ITS BRIEF")
    flat_s = " ".join(tree(STATE).split())
    flat_d = " ".join(tree(DELIV).split())

    four = "mg-a806 was scoped to land B6, the stronger scope sentence, N1's label and the §10 table"
    six_s = "mg-a806 was scoped to land **six** things"
    six_d = "mg-a806 was scoped to land **six** items"

    # The finding, re-measured at the audited commit rather than quoted.
    fs_at, fd_at = (" ".join(blob(STRIKE, STATE).split()),
                    " ".join(blob(STRIKE, DELIV).split()))
    four_s = ("mg-a806 was scoped to land four things: ledger row B6, the "
              "stronger replacement scope sentence, N1's label, and the §10 table")
    record(four_s in fs_at and four in fd_at,
           f"at `{STRIKE}` BOTH sites enumerate FOUR (ledger row B6, the scope "
           "sentence, N1's label, the §10 table) -- against a ticket with six. "
           "Two sites, worded differently, wrong the same way")

    record(six_s in flat_s and "four things" in flat_s,
           "STATE.md Appendix A: corrected to six by mg-ae62, and its correction "
           "note still names the old 'four things' -- the site is right and the "
           "record of it having been wrong survives")
    record(six_d in flat_d and four not in flat_d,
           "GATE: deliverable §13 now enumerates SIX (B1-B6) -- the second site, "
           "left uncorrected by mg-ae62, closed here")
    record(True,
           "F4 was HALF-landed for a generation: mg-ae62 fixed the site it found "
           "by quoting it and the other stood.  A repair covering only the "
           "instance already known is this arc's most-repeated defect, so this "
           "is reported as half-landed rather than as new")

    # The conclusion the enumeration supports is checked independently.
    record("none of the six" in flat_d
           or "G″ is none of the six" in flat_s,
           "the CONCLUSION survives at both sites: G″ is none of mg-a806's "
           "items, whether the count is written four or six")


# --------------------------------------------------------------------------
# NEGATIVE CONTROL -- can the new figure gate fail?
# --------------------------------------------------------------------------
def negative_control():
    """A gate is worth nothing unless it is shown to fire on the edit it exists
    to catch, and this gate has been wrong about that twice.

      * The gate mg-e1d0 shipped matched the literal `−875`, so the commit that
        made −875 false left it passing (mg-f922 B/C).
      * The gate mg-8e30 replaced it with formatted its own measurement, which
        is right -- but its battery mutated with `str.replace` and NO COUNT, so
        every mutation removed EVERY copy of the figure and the gate
        necessarily fired.  THE REALISTIC EDIT -- ONE COPY -- WAS NOT IN THE
        BATTERY, and the gate was in fact blind to it at all three sites
        (mg-8a5c F-1/F-2).

    So the battery below mutates SINGLE OCCURRENCES, includes the reinstatement
    of the duplicate itself, and includes the relocation of a whole disclosure
    out of its section.  Every mutation is applied IN MEMORY to the site texts
    and run through `figure_gate` -- THE SAME FUNCTION T1 CALLS, not a
    paraphrase of it, because the battery that missed F-1 was testing a
    re-implementation.  Verdicts are written before the run.  Nothing on disk
    is touched."""
    head("NEGATIVE CONTROL -- THE FIGURE GATE, MUTATED ONE COPY AT A TIME")
    print("""Twenty-five mutations, verdicts written before the run, applied in memory to the
three site texts and evaluated by `figure_gate` itself.  Nothing is written to
disk.  N1/N3/N4 are mg-8a5c's N1/N4/N5 -- the three single-copy corruptions
that the previous gate observed at exit 0 while predicting exit 1.  N9 is the
unmutated control.  N10-N12 are mg-835f's own U1 probes, the three the run
stayed GREEN on until mg-8916 widened the gate; N13 is the one a
set-membership census would still pass; N14 is the fail-closed cost, stated as
a cost.  N15-N18 are mg-8aae's H-1: two DECLARED figures EXCHANGED with each
other, the mutation a MULTISET cannot see because a transposition preserves it
exactly, which the run stayed GREEN on at 2 of 2 sites until mg-8eca made the
roster positional.  N19-N25 are mg-9207's E2/E2b/E3 and the rest of the same
kind: an exchange has TWO HALVES, and moving the LABELS instead of the figures
left every figure token in its declared slot and the gate refuting NOTHING at
3 of 3 label sites until the record was compared WHOLE (mg-ff3e).
""")
    a = len(state_row(tree(STATE)))
    b = len(deliv_row(tree(DELIV)))
    h = len(tree(HIST))
    base = site_texts()

    def measure(cell=None, hist=None):
        cell = a if cell is None else cell
        hist = h if hist is None else hist
        return {"gap":  doc_num(cell - b, signed=True),
                "both": doc_num(cell + hist - b, signed=True),
                "cell": doc_num(cell),
                "hist": doc_num(hist),
                "copy": doc_num(b)}

    live = measure()

    def corrupt(site, key, bad):
        """Change the ONE occurrence a reader meets.  After the mg-a318 repair
        there is exactly one, which is what makes this mutation possible to
        state at all: before it, `replace(x, y, 1)` hit whichever copy came
        first in the file and the other went on satisfying the gate."""
        t = dict(base)
        t[site] = t[site].replace(live[key], bad, 1)
        assert t[site] != base[site], f"{key} not present at {site}"
        return t

    def duplicate(site, key):
        """Write the figure a SECOND time at the site -- the exact shape F-1
        lived in, reinstated."""
        t = dict(base)
        t[site] = t[site] + f"\n\n(and the gap is {live[key]}, restated)\n"
        return t

    def prose(site, value):
        """mg-835f's G-1 probe: a figure written into the site in ORDINARY
        PROSE, beside a designated statement that stays correct and untouched.
        Every one of these left the run at exit 0 before mg-8916."""
        t = dict(base)
        t[site] = t[site] + f"\n\nThe gap is now {value} characters.\n"
        return t

    def transpose(site, before, after):
        """⚠️ ADDED 2026-07-30 (mg-8aae H-1, landed by mg-8eca).  EXCHANGE two
        DECLARED figures with each other, in ordinary prose, at one site.

        That it IS a permutation and nothing else is ASSERTED here, not hoped
        for -- a probe that also changed the bag, moved a designated statement
        or changed the length would be re-measuring the census that already
        existed rather than the positional check this exists to exercise."""
        t = dict(base)
        assert t[site].count(before) == 1, (site, before)
        t[site] = t[site].replace(before, after, 1)
        assert len(t[site]) == len(base[site]), "not length-preserving"
        assert t[site] != base[site]
        assert figure_tokens(t[site]) == figure_tokens(base[site]), \
            "not a permutation: the multiset moved"
        reader = dict((n, r) for n, r, _k in SITES)[site]
        assert reader(t[site]) == reader(base[site]), \
            "not a permutation: a designated statement moved"
        return t

    # The two mg-8aae probed, verbatim, plus one more per site exchanged in the
    # OTHER positional sense -- an earlier pair rather than a later one at the
    # STATE.md row, a later-column value moved earlier at H8.  A transposition
    # is its own inverse, so "both orderings" of one pair are one text; two
    # disjoint pairs per site is what makes the demonstration not a single
    # accident.
    CHAIN = "2 928 → 6 069 → −875 → +755"
    H8_TABLE = ("STATE.md row  before mg-a2bd :  13 551 chars\n"
                "    STATE.md row  after  mg-a2bd :  16 692 chars")
    H8_HIST_ROW = ("this file (the relocated history)                   "
                   "10 483        16 268")

    # ⚠️ ADDED 2026-07-31 (mg-9207 E2/E2b/E3, landed by mg-ff3e).  THE OTHER
    # HALF OF AN EXCHANGE.  `transpose` above moves the FIGURES and asserts the
    # multiset does not move.  This moves everything EXCEPT the figures and
    # asserts the FIGURE SEQUENCE does not move -- so anything that fires can
    # only be the segments, and a probe that fired for some other reason would
    # be re-measuring (c)/(d) rather than exercising (e).
    #
    # AND IT REPORTS RATHER THAN ASSERTS (mg-9207 J-3).  A probe that raises
    # AssertionError when its literal has moved exits 1, which is the same
    # integer a fired gate produces, and a reader cannot tell them apart.  Each
    # of these locates its text BY CONTENT and returns the string
    # "PROBE NOT APPLIED" if it is not there, which DISAGREES with its
    # prediction and is printed as itself.
    def exchange(site, pairs):
        """Exchange two pieces of NON-FIGURE text with each other, in place."""
        t = dict(base)
        s = t[site]
        for a, b in pairs:
            if s.count(a) != 1 or s.count(b) != 1:
                return "PROBE NOT APPLIED"
        for a, b in pairs:
            s = s.replace(a, "\0", 1).replace(b, a, 1).replace("\0", b, 1)
        if len(s) != len(base[site]) or s == base[site]:
            return "PROBE NOT APPLIED"
        if figure_sequence(s) != figure_sequence(base[site]):
            return "PROBE NOT APPLIED"   # it moved a figure: not a label swap
        t[site] = s
        return t

    def rewrite(site, before, after):
        """A length-preserving edit to non-figure text that is not an exchange
        -- the layout probe and the quoted-figure probe."""
        t = dict(base)
        s = t[site]
        if s.count(before) != 1 or len(before) != len(after):
            return "PROBE NOT APPLIED"
        s = s.replace(before, after, 1)
        if figure_sequence(s) != figure_sequence(base[site]):
            return "PROBE NOT APPLIED"
        t[site] = s
        return t

    def gate(mutated):
        return mutated if isinstance(mutated, str) \
            else figure_gate(mutated, live)

    # The four kinds of thing the census was blind to, ENUMERATED before being
    # fixed rather than one per generation: LABELS beside a figure (N19, N20),
    # a COLUMN HEADING over a figure (N21), a FIGURE INSIDE A MARKED QUOTATION
    # (N24, exempt from the census by a convention that is kept -- exempt from
    # the census is not the same as free to be edited), and LAYOUT, which is
    # what tells a reader which heading a figure sits under (N25).
    H8_BEFORE, H8_AFTER = "before mg-a2bd", "after  mg-a2bd"
    H8_BB_LAB1 = "STATE.md row cell                          :"
    H8_BB_LAB2 = "this file (the relocated history)          :"
    H8_HEAD = ("                                                   at bbe83b5^"
               "    at bbe83b5  AFTER mg-8e30")
    H8_HEAD_BAD = ("                                                   at bbe83b5 "
                   "    at bbe83b5^ AFTER mg-8e30")
    H8_GAP_ROW = ("    gap, cell only                                        "
                  "−875          +755        +2 744")
    H8_GAP_BAD = ("    gap, cell only                                          "
                  "−875        +755        +2 744")
    D14_QUOTED = "sits **+9 608** characters above this copy"
    D14_QUOTED_BAD = "sits **+9 607** characters above this copy"

    def relocate_14():
        """Move the whole disclosure out of §14 into an appendix (mg-8a5c N7).
        To the §14 SITE that is simply the paragraph no longer being in it."""
        t = dict(base)
        paras = t["§14"].split("\n\n")
        t["§14"] = "\n\n".join(p for p in paras
                               if "The live figures, **measured AFTER" not in p)
        assert t["§14"] != base["§14"]
        return t

    cases = [
        ("N1  STATE.md row: corrupt the LIVE gap figure ONLY",
         "GATE FIRES", lambda: figure_gate(corrupt("the STATE.md row", "gap", "+9 999"), live)),
        ("N2  §14: corrupt the LIVE gap figure ONLY",
         "GATE FIRES", lambda: figure_gate(corrupt("§14", "gap", "+9 999"), live)),
        ("N3  H8: corrupt the LIVE gap in the AFTER column ONLY",
         "GATE FIRES", lambda: figure_gate(corrupt("H8", "gap", "+9 999"), live)),
        ("N4  H8: corrupt cell + relocated history ONLY",
         "GATE FIRES", lambda: figure_gate(corrupt("H8", "both", "+9 998"), live)),
        ("N5  STATE.md row: the DUPLICATE reinstated (F-1's own shape)",
         "GATE FIRES", lambda: figure_gate(duplicate("the STATE.md row", "gap"), live)),
        ("N6  §14: the disclosure RELOCATED out of the section",
         "GATE FIRES", lambda: figure_gate(relocate_14(), live)),
        ("N7  the cell grows by one char after the figures were taken",
         "GATE FIRES", lambda: figure_gate(base, measure(cell=a + 1))),
        ("N8  the row history grows by one char",
         "GATE FIRES", lambda: figure_gate(base, measure(hist=h + 1))),
        ("N9  unmutated -- the tree as it stands",
         "gate passes", lambda: figure_gate(base, live)),
        # ⚠️ N10-N13 ADDED 2026-07-30 (mg-835f G-1, landed by mg-8916).  N10-N12
        # are mg-835f's own U1 probes, verbatim: the sentence it wrote into each
        # of the three sites while the run stayed green.  N13 is the case a
        # set-membership test would still pass -- a wrong prose figure that
        # reuses a value already on the roster -- which is why the census
        # compares MULTISETS.  N14 is the declared cost.
        ("N10 STATE.md row: a WRONG figure in ORDINARY PROSE at the site",
         "GATE FIRES", lambda: figure_gate(prose("the STATE.md row", "+9 999"), live)),
        ("N11 §14: a WRONG figure in ORDINARY PROSE at the site",
         "GATE FIRES", lambda: figure_gate(prose("§14", "+9 999"), live)),
        ("N12 H8: a WRONG figure in ORDINARY PROSE at the site",
         "GATE FIRES", lambda: figure_gate(prose("H8", "+9 999"), live)),
        ("N13 STATE.md row: wrong prose REUSING a figure already on the roster",
         "GATE FIRES", lambda: figure_gate(prose("the STATE.md row", "+755"), live)),
        ("N14 §14: a NEW historical figure, undeclared (the fail-closed cost)",
         "GATE FIRES", lambda: figure_gate(prose("§14", "12 345"), live)),
        # ⚠️ N15-N18 ADDED 2026-07-30 (mg-8aae H-1, landed by mg-8eca).  N15 and
        # N17 are mg-8aae's own two permutation probes, verbatim -- the ones the
        # run stayed GREEN on at 2 of 2 sites.  N16 and N18 exchange a second,
        # disjoint pair at the same site in the other positional sense, so the
        # demonstration is not one accident per site.  Every one of the four is
        # asserted to be a permutation and nothing else before it is scored.
        ("N15 H8: two DECLARED figures EXCHANGED (mg-8aae's own probe)",
         "GATE FIRES", lambda: figure_gate(
             transpose("H8", H8_TABLE,
                       H8_TABLE.replace("13 551", "\0").replace("16 692", "13 551")
                       .replace("\0", "16 692")), live)),
        ("N16 H8: the row-history line's two historical columns EXCHANGED",
         "GATE FIRES", lambda: figure_gate(
             transpose("H8", H8_HIST_ROW,
                       H8_HIST_ROW.replace("10 483        16 268",
                                           "16 268        10 483")), live)),
        ("N17 STATE.md row: the chain's LAST two terms exchanged (mg-8aae)",
         "GATE FIRES", lambda: figure_gate(
             transpose("the STATE.md row", CHAIN,
                       "2 928 → 6 069 → +755 → −875"), live)),
        ("N18 STATE.md row: the chain's FIRST two terms exchanged",
         "GATE FIRES", lambda: figure_gate(
             transpose("the STATE.md row", CHAIN,
                       "6 069 → 2 928 → −875 → +755"), live)),
        # ⚠️ N19-N25 ADDED 2026-07-31 (mg-9207 E2/E2b/E3, landed by mg-ff3e).
        # THE OTHER HALF OF AN EXCHANGE.  N19 and N21 are mg-9207's own E2 and
        # E3, verbatim; N20 is its E2b, at a pair of lines its predecessor's
        # battery does not hard-code.  Every one of these left the gate
        # refuting NOTHING, at 3 of 3 label sites, with every figure token in
        # its declared slot.  N22 and N23 take the same shape to the two sites
        # mg-9207 never probed on the label side, so the demonstration is at
        # 3 of 3 SITES and not 3 probes at one.  N24 and N25 are the rest of
        # the same-kind set, enumerated rather than waited for: a figure inside
        # a marked quotation (exempt from the census, and exempt is not the
        # same as editable) and the LAYOUT that tells a reader which column
        # heading a figure sits under.
        ("N19 H8: the two LABELS exchanged, figures left alone (mg-9207 E2)",
         "GATE FIRES", lambda: gate(
             exchange("H8", [(H8_BEFORE, H8_AFTER)]))),
        ("N20 H8: the bbe83b5 table's two ROW LABELS exchanged (E2b)",
         "GATE FIRES", lambda: gate(
             exchange("H8", [(H8_BB_LAB1, H8_BB_LAB2)]))),
        ("N21 H8: the two historical COLUMN HEADERS exchanged (E3)",
         "GATE FIRES", lambda: gate(
             rewrite("H8", H8_HEAD, H8_HEAD_BAD))),
        ("N22 §14: the two CORRECTION ATTRIBUTIONS exchanged",
         "GATE FIRES", lambda: gate(
             exchange("§14", [("mg-f922", "mg-8a5c")]))),
        ("N23 STATE.md row: two row-history ANCHOR LABELS exchanged",
         "GATE FIRES", lambda: gate(
             exchange("the STATE.md row",
                      [("row history H1", "row history H2")]))),
        ("N24 §14: a figure inside a MARKED QUOTATION altered",
         "GATE FIRES", lambda: gate(
             rewrite("§14", D14_QUOTED, D14_QUOTED_BAD))),
        ("N25 H8: the three-column table's ALIGNMENT shifted, no figure moved",
         "GATE FIRES", lambda: gate(
             rewrite("H8", H8_GAP_ROW, H8_GAP_BAD))),
    ]
    print(f"    {'mutation':<70}{'predicted':<14}{'observed'}")
    ok = True
    caught = {}
    for name, predicted, fn in cases:
        rows = fn()
        caught[name] = rows
        if isinstance(rows, str):
            # ⚠️ THE PROBE COULD NOT BE APPLIED (mg-9207 J-3).  Reported as
            # itself, never as an AssertionError: a crash and a fired gate are
            # the same exit code and a reader cannot tell them apart.
            observed = rows
        else:
            observed = ("GATE FIRES" if not all(o for o, _ in rows)
                        else "gate passes")
        agree = observed == predicted
        ok = ok and agree
        print(f"    {name:<70}{predicted:<14}{observed}"
              f"{'' if agree else '   <-- DISAGREES'}")
    print()
    record(ok, f"{len(cases)} of {len(cases)} mutations moved the gate as "
               "predicted.  N15-N18 are mg-8aae's H-1 -- two DECLARED figures "
               "EXCHANGED with each other, which leaves the census's multiset "
               "IDENTICAL and which this gate passed at 2 of 2 sites until the "
               "roster was made positional (mg-8eca).  The three that matter "
               "are N1-N3: corrupting ONLY "
               "the figure a reader meets, at each of the three sites, which "
               "the presence-test gate observed at exit 0 (mg-8a5c N1/N4/N5). "
               "N5 fires on the duplicate itself, so the structural repair "
               "cannot be silently undone.  N10-N12 are mg-835f's G-1 -- a "
               "wrong figure in ORDINARY PROSE beside the statement -- which "
               "this gate passed at 3 of 3 sites and now fires on at 3 of 3 "
               "(mg-8916).  N19-N25 are mg-9207's E2/E2b/E3 and the rest of "
               "that kind -- the LABELS exchanged instead of the figures -- "
               "which this gate passed at 3 of 3 label sites and now fires on "
               "(mg-ff3e)")

    # ⚠️ WHICH ROW CAUGHT IT, AND WHICH ROWS DID NOT (mg-ff3e).  "The gate
    # fires" is not the claim.  The claim is that the LABEL half is caught by
    # the half of the record that was not being compared, WHILE THE FIGURE
    # HALF STAYS GREEN -- which is the artifact's own evidence that the
    # mutation moved no figure, asserted by the thing under test rather than
    # by the prober (mg-9207 C4's convention, applied in the other direction).
    print()
    print("    the LABEL-side probes, by WHICH GATE ROW CAUGHT THEM:")
    print(f"    {'probe':<70}{'SITE RECORD':<14}{'CENSUS+ORDER'}")
    attributed = 0
    label_cases = [c for c in cases if c[0][:3] in
                   ("N19", "N20", "N21", "N22", "N23", "N24", "N25")]
    for name, _p, _fn in label_cases:
        rows = caught[name]
        if isinstance(rows, str):
            print(f"    {name:<70}{rows}")
            continue
        # ⚠️ MATCHED ON THE ROW'S HEADING, NOT ANYWHERE IN THE ROW.  The
        # SITE RECORD row's own explanation names FIGURE CENSUS and FIGURE
        # ORDER, so a substring test over the whole line reports every probe
        # as having broken a figure row.  This instrument's own first version
        # did exactly that and its own attribution row caught it.
        def heading(d):
            return d.split(" -- ")[0]
        rec_failed = any(not o and heading(d).endswith("SITE RECORD")
                         for o, d in rows)
        fig_green = all(o for o, d in rows
                        if heading(d).endswith(("FIGURE CENSUS",
                                                "FIGURE ORDER")))
        attributed += rec_failed and fig_green
        print(f"    {name:<70}{'REFUTED' if rec_failed else 'green':<14}"
              f"{'all green' if fig_green else 'a figure row failed'}")
    record(attributed == len(label_cases),
           f"{attributed} of {len(label_cases)} label-side mutations are "
           f"caught BY THE SITE RECORD ROW while every FIGURE CENSUS and "
           f"FIGURE ORDER row stays green.  That second half is the point: it "
           f"is the artifact's own evidence that the mutation moved no figure, "
           f"so the fire is attributable to the half of the record that was "
           f"not being compared before -- and not to a designated reader "
           f"breaking, which would be re-measuring (a)")


def reseal():
    """⚠️ THE ONE PLACE A DOCUMENT CAN BE BLESSED (mg-ff3e).  Regenerate
    `site_records.txt` from the sections as they now stand.

    It is deliberately NOT automatic, and it REFUSES while any other gate row
    is refuted: a section whose figures are wrong must not be sealed with them
    in it.  The declaration is the skeleton TEXT and not a sha256 of it for
    exactly this reason -- what this writes is meant to be read as a diff, and
    a hash bump is a rubber stamp with no content to review."""
    texts = site_texts()
    a = len(state_row(tree(STATE)))
    b = len(deliv_row(tree(DELIV)))
    h = len(tree(HIST))
    measured = {"gap":  doc_num(a - b, signed=True),
                "both": doc_num(a + h - b, signed=True),
                "cell": doc_num(a), "hist": doc_num(h), "copy": doc_num(b)}
    blocking = [d for ok, d in figure_gate(texts, measured)
                if not ok and "SITE RECORD" not in d]
    print("RESEAL -- regenerating the declared record of each census site")
    print("-" * 62)
    if blocking:
        print(f"  REFUSED: {len(blocking)} gate row(s) other than SITE RECORD "
              f"are refuted.  A section whose")
        print("  figures are wrong must not be sealed with them in it:")
        for d in blocking:
            print(f"    - {d[:150]}")
        return 1
    before = declared_records()
    text = render_records(texts)
    with open(SITE_RECORDS, "w", encoding="utf-8") as fh:
        fh.write(text)
    after = declared_records()
    for name, _r, _k in SITES:
        was, now = before.get(name), after[name]
        state = ("NEW" if was is None else
                 "unchanged" if was == now else "CHANGED")
        print(f"  {name:<20} {len(now.split(chr(10))):>4} lines  {state}")
    print()
    print(f"  written: {SITE_RECORDS}")
    print("  READ THE DIFF.  This is the only step in this instrument that can")
    print("  make a wrong document green, and it is a reviewable one.")
    return 0


def main():
    if "--reseal" in sys.argv[1:]:
        return reseal()
    print("mg-e1d0 -- RE-MEASURING THIS LANDING'S OWN CLAIMS")
    print("=" * 78)
    print("""Nothing below is inherited from mg-3c24 or from the ticket.  mg-3c24's
MATHEMATICS is not re-opened: it found 0 BROKEN and every number reproduced
from a disjoint route.  What is measured here is the four DOCUMENTARY findings,
each of which is a claim a document makes about itself, another document, or a
ticket.  All four are measured from git and the tree.

Note on regeneration, stated because it is the same caveat mg-7d5a recorded,
and CORRECTED 2026-07-30 (mg-f922 B/C/E/F, landed by mg-8e30): T1's live row,
T2's tree line and T4 measure the WORKING TREE, so they describe the state the
commit containing this run LEAVES BEHIND -- not `HEAD`, which during a run
taken before `git commit` is that commit's PARENT.  That distinction is the
whole of mg-f922 B: the version of this file that shipped with mg-e1d0 read
`HEAD`, so it published the pre-edit figure as the current one in the commit
that made it stale.  Nothing here embeds a sha of its own.""")

    t1()
    t2()
    t3()
    t4()
    negative_control()

    head("BOTTOM LINE")
    bad = [t for t, ok in RESULTS if ok is False]
    print(f"  checks recorded : {len(RESULTS)}")
    print(f"  measurements    : {sum(1 for _, ok in RESULTS if ok is None)}")
    print(f"  confirmed       : {sum(1 for _, ok in RESULTS if ok is True)}")
    print(f"  refuted         : {len(bad)}")
    print()
    if bad:
        print("  REFUTED, which for this instrument means a claim this landing")
        print("  makes did not hold and the prose must not be written:")
        for t in bad:
            print(f"    - {t}")
        return 1
    print("  All four findings are measured and all four stand.  F4 stands as")
    print("  HALF-landed -- mg-ae62 fixed the STATE.md site and left the")
    print("  deliverable's; this landing closes the second.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
