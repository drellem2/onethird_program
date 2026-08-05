"""mg-bf79 -- shared instrument for the repair of mg-56dc's four openings.

WHAT THIS FILE IS ALLOWED TO CONTAIN, GIVEN WHAT IT REPAIRS.  One of the four
openings (O4) is *two copies of `figures()` disagree on 3*, and the floor item
this repair adds (F) is that `figures()` was not the only rule kept in two
copies.  A library for that repair may therefore not open with a fourth copy of
anything.  So the rule is explicit and mechanical, and `p5_self.py` checks it:

    THIS FILE DEFINES NO RULE THAT ALREADY EXISTS IN THE ARC.  Every predicate
    it needs is IMPORTED from the tree that owns it, and the import is named:

      `lib56dc`  -- mg-56dc's audit instrument.  `count_rows` and `grain_of`
                    are the sixth-in-the-family CLASSIFIER the brief tells this
                    repair to run over the whole artifact rather than one row;
                    `exec_site_rows` / `exec_sites` are its re-derivation of
                    the caller census AT TWO GRAINS, which is the measurement
                    O1 turns on; `figures(line, small=)` is its parameterised
                    third copy, the only one that can measure the disagreement
                    between the other two without being either of them.
      `lib7522`  -- the arc's marker rule `MARK`, `strength_lines`,
                    `alternatives`, `figures`.
      `lib70c7`  -- `outs`, and (after this repair) its `figures` /
                    `alternatives` which now delegate to `lib7522`'s.

MG-56DC'S TREE IS READ AND NOT WRITTEN.  An audit's tree is its evidence; this
repair imports mg-56dc's library and modifies none of its bytes, and
`p5_self.py` asserts that with `git diff --stat` against the commit that
published it.  Importing an auditor's instrument to repair what it found is not
the same as editing its findings.

WHAT IS WRITTEN HERE FROM SCRATCH, AND WHY THAT IS NOT A COPY.  One thing:

  `grain_ledger`  -- the LEDGER shape: for every printed count, the LABEL, the
                     GRAIN the label declares, the stage that grain was found
                     at, and the value.  It composes `lib56dc.count_rows` and
                     `lib56dc.grain_of`; it re-implements neither.  The ledger
                     is the shape `mg-03d1` is instructed to report in, and
                     producing it here is how this repair states its own counts
                     under the standard its auditor will apply.

The PROVENANCE population -- the O2 repair -- is deliberately NOT here.  It is
`lib70c7.published_by`, in the library of the tree whose rule ranges over it,
because R4's own finding is that a property stated somewhere other than where
the check lives is a property nothing enforces.  This file imports it.

EVERY COUNT THIS TREE PRINTS NAMES ITS POPULATION AND ITS GRAIN IN ITS OWN
LABEL.  Not in a column header, not on the line above.  The audit waiting on
this repair (`mg-03d1`) is instructed to report, for every printed count, the
label, the grain of the value, and whether they agree -- so a count of mine
whose grain lives in a header would be the same defect class as O1, found in
the repair of O1.  `p5_self.py` measures that at stage `label` and goes red on
any other stage.
"""

import os
import re
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True,
                      check=True).stdout.strip()

TREE = "code/runner_exit_repair_bf79"
SUBJECT = "code/runner_exit_repair_70c7"        # mg-70c7, the repair audited
AUDIT = "code/runner_exit_audit_56dc"           # mg-56dc, the audit being closed
LIB7522 = "code/runner_exit_repair_7522"        # where the one marker rule lives
SUBJECT_DOC = "docs/repair-mg-70c7-grain-and-population.md"

# The commit that published mg-70c7's transcripts.  NOT a hand-chosen anchor:
# `p1_grain.py` re-derives it with `git log -1 -- <transcript>` and goes red if
# this constant and the plumbing disagree.  It is written here so the constant
# can be checked against the derivation rather than trusted.
SUBJECT_REV = "973ca61"

# mg-70c7's work item id, as its own commits spell it.  The provenance
# population is built from this string, so it is a parameter and not a literal
# buried in a query.
SUBJECT_TAG = "(mg-70c7)"

for _p in (AUDIT, LIB7522, SUBJECT):
    sys.path.insert(0, os.path.join(REPO, _p))

import lib56dc as A          # noqa: E402  the sixth instrument's classifier
import lib7522 as L          # noqa: E402  the one marker rule
import lib70c7 as M          # noqa: E402  the repaired tree's library


# ---------------------------------------------------------------------------
# Output.  Borrowed, not restated -- `bar`/`hdr`/`rows` are already identical
# in three libraries of this arc and a fourth copy would be this repair's own
# floor item.
# ---------------------------------------------------------------------------

bar = A.bar
hdr = A.hdr
git = A.git
read = A.read
run_argv = A.run_argv
finding = A.finding


# ---------------------------------------------------------------------------
# O2.  A POPULATION DEFINED BY PROVENANCE RATHER THAN BY A PATH.
# ---------------------------------------------------------------------------

# DELEGATED, NOT RESTATED.  The provenance property is the O2 repair, and R4's
# own standard -- *the property, the check and the test in one directory* -- puts
# it in the library of the tree whose rule it is.  So it lives in `lib70c7.py`
# next to the `r6_self.py` that ranges over it, and this repair's probes call
# the same object rather than a copy of it.  A second definition here would be
# this repair committing its own floor item on the day it recorded it.
published_by = M.published_by
provenance_commits = M.provenance_commits
MY_TAG = "(mg-bf79)"                      # this tree's own tag, for p5_self


# ---------------------------------------------------------------------------
# O1.  THE LEDGER.  For every printed count: the LABEL, the GRAIN the label
# declares, the STAGE that grain was found at, the VALUE.
# ---------------------------------------------------------------------------

def grain_ledger(text, lookback=A.HEADER_LOOKBACK):
    """[(line, label, [ints], grain, stage)] for every count row in `text`.

    Composed from `lib56dc.count_rows` (the population -- a shape rule over the
    printed line) and `lib56dc.grain_of` (the classifier -- which grain word the
    label declares, and at which stage of widening it was found).  Neither is
    reimplemented here; this function is the JOIN, which is what was missing.

    WHAT THE LEDGER ESTABLISHES AND WHAT IT DOES NOT.  It reports what the
    LABEL SAYS.  It does not know what the value counts -- that is a fact about
    the code that printed it, and the only way to get it is to re-derive the
    quantity, which `p1_grain.py` does for the one row O1 is about and cannot
    do for prose.  So a row here reading `SITE` means *the label declares site
    grain*, and the audit's question -- whether the label and the value agree
    -- is answerable from this ledger only where a re-derivation sits beside
    it.  That asymmetry is O1 itself and it is why the classifier cannot be the
    last word on its own subject.
    """
    lines = text.splitlines()
    out = []
    for i, label, nums in A.count_rows(text):
        above = [lines[j] for j in range(i - 2, max(-1, i - 2 - lookback), -1)
                 if 0 <= j < len(lines)]
        grain, stage = A.grain_of(label, above)
        out.append((i, label, nums, grain, stage))
    return out


def ledger_table(ledger, limit=None, indent="      "):
    """Print a ledger as rows of (line, grain, stage, value(s), label)."""
    print("%s%-6s %-9s %-6s %-10s %s"
          % (indent, "line", "grain", "stage", "value(s)", "label"))
    shown = ledger if limit is None else ledger[:limit]
    for i, label, nums, grain, stage in shown:
        print("%s%-6d %-9s %-6s %-10s %s"
              % (indent, i, grain, stage,
                 ",".join(str(n) for n in nums), label[:44]))
    if limit is not None and len(ledger) > limit:
        print("%s... %d more row(s), all in this transcript above"
              % (indent, len(ledger) - limit))


def tally(ledger):
    """{grain: n} and {stage: n} over a ledger, as two dicts."""
    g, s = {}, {}
    for _i, _l, _n, grain, stage in ledger:
        g[grain] = g.get(grain, 0) + 1
        s[stage] = s.get(stage, 0) + 1
    return g, s


# ---------------------------------------------------------------------------
# Running a probe of the SUBJECT tree live, so a repaired transcript is a thing
# this tree produced rather than a file it cites.
# ---------------------------------------------------------------------------

def run_probe(rel):
    """(exit code, combined output) of one probe of another tree, run in place.

    The probe is run with `cwd` set to its own directory, which is how
    `run_all.sh` runs it, so `sys.path.insert(dirname)` finds its library.
    Nothing is written: the output is captured and returned.
    """
    d = os.path.join(REPO, os.path.dirname(rel))
    return run_argv([sys.executable, "-B", os.path.basename(rel)], d)


def clean_tree(paths):
    """[path] among `paths` whose bytes differ from the index, sorted.

    Used to assert mg-56dc's tree is unmodified.  `git diff --name-only` and
    not a hash of my own, because the index is the repository's own answer.
    """
    out = git("diff", "--name-only", "--", *paths).splitlines()
    return sorted(p.strip() for p in out if p.strip())


_DEF = re.compile(r"^def\s+(\w+)\s*\(", re.M)


def defined_names(path, ref=None):
    """{name} -- every module-level `def` in a Python file.

    An AST walk would also return nested and class-level definitions; the
    question F asks is which names a library EXPORTS as a rule, so the regex is
    anchored at column 0 and that is stated rather than implied.
    """
    return set(_DEF.findall(read(path, ref)))


def same_body(name, path_a, path_b, ref=None):
    """True when `name`'s body is identical in both files, docstring excluded.

    `lib7522.function_code` does the unparsing -- a fifth copy of an AST walk
    in a repair whose subject is duplicated rules would be indefensible.  The
    docstring is excluded because two copies that differ only in their prose
    are still one rule, and because a rule's TEXT is not its BEHAVIOUR: this
    predicate answers *are these the same code*, and `p4_figures.py` answers
    *do these agree on every input* separately.  Both are printed.
    """
    return (L.function_code(path_a, name, ref)
            == L.function_code(path_b, name, ref))
