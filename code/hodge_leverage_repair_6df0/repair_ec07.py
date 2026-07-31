#!/usr/bin/env python3
"""mg-6df0 -- mg-ec07's E-5, E-4 and E-2, repaired and controlled.

THREE FINDINGS, AND THEY ARE ONE SHAPE TWICE.

  E-5  `--reseal` -- the one step that can make a wrong document green --
       refuses while any gate row other than SITE RECORD is refuted, and it
       identifies those rows with `"SITE RECORD" not in d`, A SUBSTRING TEST
       OVER THE WHOLE ROW.  The RECORD PARTITION row's own explanation names
       SITE RECORD, so 3 of 34 rows are excluded that were never meant to be,
       and they are the three that license the whole "lossless" claim.  That
       is R5 item 3 of mg-ff3e's own instrument VERBATIM: the defect it found
       in its own scoring code, fixed there with `heading()`, forty lines from
       where the same construct was live in the file it was repairing.

  E-4  the same-kind enumeration was over KINDS, not over SITES x KINDS.
       Seven probes, each checked at ONE SITE.  So mg-9207's own E3 -- two
       COLUMN HEADERS exchanged -- is caught at H8 and is EXIT 0 at the
       STATE.md site, because that site is one line from `find_line` and the
       header of the table it sits in is outside it.

  E-2  the sentence that sizes the residue for a reader -- "text outside the
       site is not read, BECAUSE A SITE IS A SECTION" -- is false at 1 of 3
       sites.

WHAT THIS INSTRUMENT IS, AND WHAT IT IS NOT.  It does not re-implement the
gate: it runs the REAL runner on disk, mutating the tree and restoring it
sha256-verified.  Where it must classify a gate row it uses `heading()` --
the same remedy the repair applies -- except in R1a, which measures the
substring test itself and says so.

THE ORDER IS PART OF THE DELIVERABLE.  This file and `PREDICTIONS.md` are
committed BEFORE the fix, against the unrepaired artifact, because mg-ec07's
closing note is that "enumerate before fixing" was unobservable in the
repository afterwards even where it was followed.  R6 re-derives that ordering
from git.

  R1  the refusal, at the finest unit: bent lossy, blessed or refused; and the
      SAME probe with the fix reverted, which is the control.
  R2  every occurrence of the construct, swept FROM THE TREE -- the answer to
      "a fix applied where the defect was found rather than where it occurs".
  R3  SITES x KINDS: the runner's own matrix, and three cells bridged to disk.
  R4  `audit_ec07.py`, the instrument that raised all three, re-run unmodified.
  R5  the extent, derived from the code and re-measured here independently.
  R6  this deliverable checked for the defect it repairs.

Pure Python 3 + git.  No third-party packages.
"""

import ast
import hashlib
import importlib.util
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
LANDING_DIR = os.path.join(REPO, "code", "hodge_leverage_landing_e1d0")
LANDING = os.path.join(LANDING_DIR, "verify_landing.py")
LANDING_REL = "code/hodge_leverage_landing_e1d0/verify_landing.py"
RECORDS_REL = "code/hodge_leverage_landing_e1d0/site_records.txt"
AUDIT = os.path.join(REPO, "code", "hodge_leverage_audit_ec07",
                     "audit_ec07.py")

STATE = "STATE.md"
DELIV = "docs/OneThird-Hodge-Side-Leverage.md"
HIST = "docs/state-history/attempt-mg-a3d4.md"

# Everything this instrument writes to and restores.  A dirty tree scoped to
# these is a REFUSAL: a restore over an uncommitted edit destroys it.
MUTATED = [STATE, DELIV, HIST, LANDING_REL, RECORDS_REL]

RESULTS = []



# --------------------------------------------------------------------------
# plumbing
# --------------------------------------------------------------------------
def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True).stdout


def read(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
        return fh.read()


def write(rel, text):
    with open(os.path.join(REPO, rel), "w", encoding="utf-8") as fh:
        fh.write(text)


def sha(rel):
    with open(os.path.join(REPO, rel), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def record(ok, detail):
    RESULTS.append((detail, ok))
    mark = {True: "[CONFIRMED]", False: "[REFUTED  ]", None: "[MEASURED ]"}[ok]
    print(f"  {mark} {detail}")


def head(title):
    print()
    print(title)
    print("-" * len(title))


def by_substring(rows, name):
    """⚠️ THE CONSTRUCT, COMMITTED ON PURPOSE AND IN EXACTLY ONE PLACE.

    A substring test over a whole gate row is the defect this arc repairs, and
    MEASURING it requires PERFORMING it.  So it is performed here, once, in a
    function whose name says what it is -- rather than written inline, where a
    sweep of the tree can only tell it from the defect by a disposition keyed
    on its line number.  A REASON ON A LINE IS NOT A STRUCTURE: it has to be
    read, it has to be maintained, and it goes stale the moment the line moves.

    ⚠️ ADDED BY mg-3f3b (mg-7e39 F3): 6 instances of the construct existed
    when mg-6df0 landed, it repaired 1 and dispositioned 5."""
    return [r for r in rows if name in r]


def row_vocabulary(src):
    """THE GATE'S ROW HEADINGS, READ OUT OF THE GATE'S OWN DECLARATION.

    ⚠️ WHY THIS IS NOT A LIST (mg-7e39 F5, landed by mg-3f3b).  This used to
    be `ROW_NAMES`, FIVE HEADINGS WRITTEN OUT BY HAND -- against a gate that
    emits SIX.  This sweep exists because a hand-picked SITE is a scope nobody
    chose; it then picked its VOCABULARY the same way, and the name it missed
    is `READ AT THE SITE`, which is where the construct entered this arc
    (`audit_a318_repair.py:326`, the earliest occurrence the sweep finds).
    The lesson transferred to the axis it was learned on and not to the next.

    ⚠️ AND WHY IT IS NOT A REGEX OVER THE GATE'S `print` CALLS EITHER, which
    was this repair's first answer.  That fixes the count and not the shape: a
    regex is still a SECOND READER of the gate's grammar and can fall behind
    it.  It did -- it returned six and the gate has SEVEN row kinds, because
    the seventh was emitted as `'{label}' is WRITTEN ONCE` and the pattern
    wanted capitals straight after the label.  A derived vocabulary that is
    derived from the wrong thing is a hand list with extra steps.

    So the gate DECLARES `ROW_KINDS`, uses it to fail closed on any row whose
    heading ends in none of them, and this reads that tuple by AST.

    FAIL-CLOSED.  A derivation that returns nothing sweeps with an empty
    vocabulary, finds nothing, and reads EXACTLY LIKE A TREE WITH NOTHING IN
    IT -- which is mg-7e39's F1 on this axis.  So an empty result is a
    refusal."""
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign) and any(
                getattr(t, "id", "") == "ROW_KINDS" for t in node.targets):
            names = [e.value for e in getattr(node.value, "elts", [])
                     if isinstance(e, ast.Constant) and isinstance(e.value, str)]
            if names:
                return sorted(names)
    raise SystemExit(
        "row_vocabulary: `ROW_KINDS` could not be read out of "
        f"{LANDING_REL} -- REFUSING to sweep with an empty vocabulary, "
        "because a sweep that finds nothing and a tree that holds nothing "
        "read exactly the same")


def heading(row):
    """THE ROW'S HEADING -- everything before the ` -- ` that introduces its
    explanation.  This is the whole of the E-5 remedy, and it is used
    everywhere in this file that a row is identified, with ONE declared
    exception (R1a, which measures the substring test itself)."""
    return row.split(" -- ")[0]


# The gate-row headings this sweep keys on -- DERIVED, never hand-listed
# (mg-7e39 F5).  R2 sweeps the tree for tests that key on them.
ROW_NAMES = row_vocabulary(read(LANDING_REL))


def row_kind(row):
    """The row's kind, with the site prefix removed: `SITE RECORD`, ..."""
    h = heading(row)
    return h.split(": ", 1)[1] if ": " in h else h


def run_runner():
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("VERIFY_", "HODGE_", "MG_"))}
    r = subprocess.run([sys.executable, LANDING], capture_output=True,
                       text=True, env=env, cwd=REPO)
    return r.returncode, r.stdout + r.stderr


def run_reseal():
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("VERIFY_", "HODGE_", "MG_"))}
    r = subprocess.run([sys.executable, LANDING, "--reseal"],
                       capture_output=True, text=True, env=env, cwd=REPO)
    return r.returncode, r.stdout + r.stderr


def refuted_rows(out):
    return [l.strip()[len("[REFUTED  ] "):]
            for l in out.split("\n") if l.strip().startswith("[REFUTED")]


def gate_row(out, site, kind):
    """The verdict of ONE named gate row for ONE site, or None if absent.
    Matched on the row's HEADING (`heading()`), never on the whole row."""
    want = f"GATE @ {site}: {kind}"
    for l in out.split("\n"):
        s = l.strip()
        if not s.startswith("["):
            continue
        body = s[s.index("]") + 2:]
        if heading(body) == want:
            return s.startswith("[CONFIRMED")
    return None


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.REPO = REPO
    return mod


V = load_module(LANDING, "verify_landing_head")


def measured_now():
    a = len(V.state_row(V.tree(V.STATE)))
    b = len(V.deliv_row(V.tree(V.DELIV)))
    h = len(V.tree(V.HIST))
    return {"gap":  V.doc_num(a - b, signed=True),
            "both": V.doc_num(a + h - b, signed=True),
            "cell": V.doc_num(a), "hist": V.doc_num(h), "copy": V.doc_num(b)}


# THE STATE THIS RUN IS IN.  Derived from the artifact, never assumed: the
# transcript of this instrument is committed twice, once against the
# unrepaired file and once against the repaired one, and every row below says
# which state it is scoring.
# The refusal, before and after.  R1c reverts the second to the first and
# changes NOTHING ELSE -- the finest unit the fix has.
REFUSAL_PRE = '                if not ok and "SITE RECORD" not in d]'
REFUSAL_POST = ('                if not ok '
                'and not heading(d).endswith("SITE RECORD")]')


#
# ⚠️ KEYED ON THE REFUSAL ITSELF, not on the absence of the old string.  The
# first version of this line read `'"SITE RECORD" not in d' not in src`, and
# the repaired file QUOTES the construct it replaced in `reseal`'s own
# docstring -- so the detector said PRE against a repaired artifact.  A test
# for a defect that a description of the defect can trip is the same shape as
# the defect: a substring where a structure was meant.
FIXED = REFUSAL_POST.strip() in read(LANDING_REL)
STATE_WORD = "POST (the repair is on disk)" if FIXED else \
             "PRE (the artifact as mg-ec07 audited it)"


def probe_on_disk(rel, edit, runner=run_runner):
    """Apply `edit` to `rel`, run the real runner (or `--reseal`), restore,
    and report whether the restoration is sha256-identical.

    Every probe here is LENGTH-PRESERVING on the three documents: three of the
    five live figures ARE lengths of those files, so a probe that changed one
    would fire the designated readers and the fire would not be attributable
    to the half of the record under test."""
    before = read(rel)
    before_sha = sha(rel)
    new = edit(before)
    if new is None or new == before:
        return None, "PROBE NOT APPLIED", True
    write(rel, new)
    try:
        rc, out = runner()
    finally:
        write(rel, before)
    assert sha(rel) == before_sha, f"{rel}: restoration failed"
    return rc, out, sha(rel) == before_sha


# --------------------------------------------------------------------------
# R0 -- PREFLIGHT
# --------------------------------------------------------------------------
def r0():
    head("R0 -- PREFLIGHT")
    dirty = [l[3:] for l in git("status", "--porcelain", "--",
                                *MUTATED).split("\n") if l.strip()]
    if dirty:
        print("  REFUSING TO RUN: uncommitted changes to files this")
        print("  instrument mutates and restores.  A restore over them")
        print("  destroys them:")
        for d in dirty:
            print(f"    - {d}")
        raise SystemExit(2)
    record(True, f"R0 the {len(MUTATED)} files this instrument mutates and "
                 f"restores are clean at start")
    print(f"  the artifact on disk is: {STATE_WORD}")
    rc, out = run_runner()
    record(rc == 0, f"R0 the real runner on the clean tree exits {rc} "
                    f"(predicted 0) with {len(refuted_rows(out))} refuted rows")
    return out


# --------------------------------------------------------------------------
# R1 -- THE REFUSAL, AT THE FINEST UNIT  (mg-ec07 E-5; OPEN 3's control)
# --------------------------------------------------------------------------
LOSSY_FROM = "        segments.append(raw[last:m.start()])"
LOSSY_TO = "        segments.append(raw[last:m.start()].lower())"
LOSSY_FROM2 = "    segments.append(raw[last:])"
LOSSY_TO2 = "    segments.append(raw[last:].lower())"

def bend_lossy(src):
    """mg-ec07's B2: `partition` made LOSSY -- the segments lower-cased, so
    `rejoin(segments, figures) == raw` is false and the RECORD PARTITION row
    is refuted at every site.  This is the exact shape mg-ff3e's own D3 uses
    to show that row can fail; here it is used to ask whether the BLESSING
    PATH notices."""
    n0 = src.count(".lower())")
    bent = src.replace(LOSSY_FROM, LOSSY_TO).replace(LOSSY_FROM2, LOSSY_TO2)
    if bent.count(".lower())") != n0 + 2:
        return None
    return bent


def revert_fix(src):
    """The POST source with the heading-keyed refusal put back to the
    substring test.  One statement, nothing else."""
    if REFUSAL_POST not in src:
        return None
    return src.replace(REFUSAL_POST, REFUSAL_PRE, 1)


def r1():
    head("R1 -- THE REFUSAL, AT THE FINEST UNIT (mg-ec07 E-5)")
    print("""`--reseal` is the ONE step in the artifact that can make a wrong document
green.  mg-ec07 measured that it has been executed 0 times anywhere in the
arc, so neither half of "it refuses while any other gate row is refuted" had a
control until that audit built one.

R1a classifies the gate rows BOTH WAYS and reports the disagreement.  R1b asks
the blessing path the behavioural question, on disk.  R1c is the control: the
fix reverted, one statement, nothing else -- if the blessing does not come
back, the fix is not what is doing the work.
""")
    texts = V.site_texts()
    measured = measured_now()
    rows = [d for _ok, d in V.figure_gate(texts, measured)]

    # ⚠️ THE ONE DELIBERATE USE OF THE DEFECT IN THIS FILE, and since mg-3f3b
    # it is a CALL TO A DECLARED FUNCTION rather than the construct written
    # inline under a disposition keyed on this line number.  `by_substring`
    # commits the construct on purpose, because it is MEASURING it -- and a
    # sweep now meets a NAME instead of a line it has to look up.
    by_sub = by_substring(rows, "SITE RECORD")
    by_heading = [d for d in rows if heading(d).endswith("SITE RECORD")]
    unintended = sorted({row_kind(d) for d in by_sub
                         if d not in by_heading})
    print(f"    gate rows                                   : {len(rows)}")
    print(f"    contain 'SITE RECORD' ANYWHERE in the row   : "
          f"{len(by_sub)}")
    print(f"    HEADING ends with 'SITE RECORD'             : "
          f"{len(by_heading)}")
    print(f"    excluded by the substring test and not by   : "
          f"{len(by_sub) - len(by_heading)}  {unintended}")
    print()
    record(None,
           f"R1a of {len(rows)} gate rows, {len(by_sub)} contain the "
           f"string 'SITE RECORD' and {len(by_heading)} have a HEADING that "
           f"ends with it.  The {len(by_sub) - len(by_heading)} that "
           f"differ are the {', '.join(unintended)} rows -- one per site, and "
           f"they are the rows that license 'the two halves are the whole "
           f"record'.  This is a property of the row TEXTS and is the same in "
           f"both states: the repair keys the refusal on the heading rather "
           f"than editing the rows' own explanations")

    rec_sha = sha(RECORDS_REL)
    rc, out, restored = probe_on_disk(LANDING_REL, bend_lossy, run_reseal)
    sealed = sha(RECORDS_REL) != rec_sha
    if sealed:
        git("checkout", "--", RECORDS_REL)
    blessed = rc == 0
    record(FIXED == (rc == 1),
           f"R1b `partition` bent LOSSY, then `--reseal`: exit {rc} "
           f"({'REFUSED' if rc == 1 else 'BLESSED'}), the record it wrote "
           f"{'DID' if sealed else 'did NOT'} change.  Predicted "
           f"{'1 REFUSED' if FIXED else '0 BLESSED'} in this state "
           f"({STATE_WORD}).  A partition that is not the section is exactly "
           f"the claim the RECORD PARTITION row exists to make, and the "
           f"blessing path {'now sees it' if rc == 1 else 'does not see it'}")

    # R1c -- THE CONTROL.  Revert the fix and nothing else.
    def bent_and_reverted(src):
        r = revert_fix(src)
        return None if r is None else bend_lossy(r)

    rc2, out2, restored2 = probe_on_disk(LANDING_REL, bent_and_reverted,
                                         run_reseal)
    sealed2 = sha(RECORDS_REL) != rec_sha
    if sealed2:
        git("checkout", "--", RECORDS_REL)
    if rc2 is None:
        record(None,
               f"R1c CONTROL NOT APPLIED: the heading-keyed refusal is not on "
               f"disk in this state, so there is nothing to revert.  In "
               f"{STATE_WORD} the pre-repair predicate IS the live one, and "
               f"R1b above is what it does")
    else:
        record(rc2 == 0,
               f"R1c CONTROL -- the refusal reverted to `\"SITE RECORD\" not "
               f"in d`, ONE STATEMENT, with `partition` bent lossy exactly as "
               f"in R1b: `--reseal` exits {rc2} (predicted 0, BLESSED) and "
               f"the record it wrote {'DID' if sealed2 else 'did NOT'} "
               f"change.  The fix is load-bearing at its finest unit: revert "
               f"that one line and a document whose record is provably not "
               f"its section is blessed again")

    # R1d -- the refusal that already worked must not be weakened.
    gapfig = measured["gap"]
    d14 = texts["§14"]

    def bump(fig):
        digits = "".join(c for c in fig if c.isdigit())
        bumped = str(int(digits) + 1).rjust(len(digits), "0")
        out_s, k = [], 0
        for c in fig:
            if c.isdigit():
                out_s.append(bumped[k])
                k += 1
            else:
                out_s.append(c)
        return "".join(out_s)

    def corrupt_fig(src):
        if d14.count(gapfig) != 1:
            return None
        bad = d14.replace(gapfig, bump(gapfig), 1)
        return src.replace(d14, bad, 1) if len(bad) == len(d14) else None

    rc3, out3, restored3 = probe_on_disk(DELIV, corrupt_fig, run_reseal)
    record(rc3 == 1 and sha(RECORDS_REL) == rec_sha,
           f"R1d a wrong LIVE FIGURE ({gapfig} -> {bump(gapfig)} in §14), "
           f"then `--reseal`: exit {rc3} (predicted 1, REFUSED) with "
           f"site_records.txt sha256 UNCHANGED.  The repair widens the "
           f"refusal and must not weaken the half that already worked "
           f"(mg-ec07 B1)")

    rc4, out4 = run_runner()
    record(rc4 == 0 and sha(RECORDS_REL) == rec_sha and restored
           and restored2 is not False and restored3,
           f"R1e after R1's four probes the tree is restored: the runner "
           f"exits {rc4} with {len(refuted_rows(out4))} refuted rows and "
           f"site_records.txt is sha256-identical to the pre-probe file")
    return blessed


# --------------------------------------------------------------------------
# R2 -- THE SWEEP: EVERY OCCURRENCE OF THE CONSTRUCT, FROM THE TREE
# --------------------------------------------------------------------------
# ⚠️ THE DISPOSITIONS ARE KEYED ON THE EXACT LINE, so a NEW occurrence
# anywhere in the tree is undispositioned and makes this section RED.  A list
# of files to skip would be a scope nobody chose -- which is the finding.
DISPOSITIONS = {
    # (relative path, exact stripped line) -> why this one is not the defect
    #
    # ⚠️ EMPTY SINCE mg-3f3b, AND THAT IS THE REPAIR (mg-7e39 F3).  It used to
    # hold four rows: two occurrences that MEASURE the construct, and two live
    # in other deliverables' shipped instruments that were raised "for a ticket
    # rather than repaired in passing".  mg-7e39 counted what that came to --
    # 6 instances existed when this repair landed, IT TOUCHED 1, and 5 were
    # live in the commit it landed in, four of them selecting 6 gate rows where
    # 3 were meant.  A DISPOSITION IS A REASON, NOT A REPAIR.
    #
    # All five are now repaired: three by `heading()` in the file that held
    # them, and the two that measure the construct by routing through
    # `by_substring`, which `substring_hits` recognises BY NAME.  The table is
    # kept, empty, because a NEW occurrence anywhere in the tree still has to
    # land in it or make R2a red.
}

SENTENCE = "a site is a section"

# The same discipline for the SENTENCE, bucketed by file with a reason each.
# A file that grows an occurrence and is not here is UNDISPOSITIONED and makes
# R2b red -- which is the point: the sentence spread to five files before
# anybody measured whether it was true.
SENTENCE_FILES = {
    LANDING_REL:
        "THE ARTIFACT UNDER REPAIR.  Its live claims are what this repair "
        "removes; `section()`'s own docstring is kept because it is true of "
        "the function it documents (R2c)",
    "code/hodge_leverage_repair_6df0/repair_ec07.py":
        "this instrument QUOTING the sentence it is repairing",
    "code/hodge_leverage_audit_ec07/audit_ec07.py":
        "the audit that RAISED E-2, quoting it in order to test for it.  "
        "Re-run unmodified in R4",
    "code/hodge_leverage_repair_ff3e/repair_9207.py":
        "mg-ff3e's shipped instrument, printing it in R5 under a committed "
        "transcript.  Corrected in that deliverable's REPORT with a dated "
        "note -- this arc's convention -- rather than edited under a "
        "transcript that would then no longer match it",
    "code/hodge_leverage_repair_8916/repair_835f.py":
        "mg-8916's shipped instrument, same disposition",
    "code/hodge_leverage_audit_835f/audit_a318_repair.py":
        "mg-a318's audit, same disposition -- and the earliest occurrence "
        "the sweep finds, which is where the sentence entered the arc",
}


def py_files():
    """Every .py file under `code/`, from the WORKING TREE."""
    out = []
    for root, _d, fs in os.walk(os.path.join(REPO, "code")):
        for f in sorted(fs):
            if f.endswith(".py"):
                out.append(os.path.relpath(os.path.join(root, f), REPO))
    return sorted(out)


def population_line():
    """THE POPULATION, STATED WITH THE OBJECT IT WAS DERIVED FROM.

    ⚠️ mg-7e39 F2, landed by mg-3f3b.  This sweep's transcript published
    "429 .py files swept" beside a tree of 448 -- and 448 was also the count
    at the commit before it, so the gap was not drift after the run: THE
    FIGURE WAS WRONG WHEN IT WAS WRITTEN.  19 files were in the population and
    not in the number a reader was given.

    A count is only a fact about a named tree.  So the line prints WHICH tree:
    the working directory the run walked, the HEAD it was taken at, and
    whether that HEAD describes the working directory at all.  A reader who
    meets this line can check it; a reader who meets a bare number cannot."""
    rev = git("rev-parse", "HEAD").strip()[:12] or "(no commit)"
    dirty = bool(git("status", "--porcelain", "--", "code").strip())
    n = len(py_files())
    return (f"{n} .py files swept, walked from the WORKING TREE at HEAD "
            f"{rev}{' WITH UNCOMMITTED CHANGES UNDER code/' if dirty else ''}")


QUOTED_SPAN = re.compile(r"'[^']*'|`[^`]*`")
# The same idea for PROSE: a sentence inside quotes is being discussed, not
# asserted.  Double quotes are included here and excluded above, because the
# construct R2a hunts for IS a double-quoted literal and this needle is not.
PROSE_QUOTE = re.compile(r"'[^']*'|`[^`]*`|\"[^\"]*\"")


# The functions that PARSE A HEADING out of a gate row.  A name bound from one
# of these holds a HEADING, so testing a row name against it is the REMEDY.
#
# ⚠️ WIDENED BY mg-3f3b.  The rule used to recognise the remedy only when it
# was spelled `heading(` and only when the binding was a plain `x = ...`.  An
# equally correct remedy spelled `row_kind(` inside a set comprehension --
# `bad = {row_kind(d) for ok, d in rows if not ok}` -- read as the DEFECT, so
# the sweep reported four false positives in `audit_7e39.py`, the very audit
# that raised this finding.  A RULE THAT ONLY RECOGNISES ONE SPELLING OF THE
# REMEDY REPORTS THE OTHER SPELLING AS THE DISEASE, and it does it in the
# grammar of a finding about the code.
HEADING_FUNCS = ("heading(", "row_kind(", '.split(" -- ")[0]')


def heading_vars(src):
    """Names in `src` ever bound to something parsed out of a heading -- in an
    assignment, an augmented assignment, or a comprehension target."""
    out = set()
    for l in src.split("\n"):
        if not any(f in l for f in HEADING_FUNCS):
            continue
        m = re.match(r"\s*(\w+)\s*(?:=|\+=|\|=)", l)
        if m:
            out.add(m.group(1))
    return out


def substring_hits(rel):
    """Lines that identify a GATE ROW by a SUBSTRING TEST over a whole row.

    The rule, stated because a rule is checkable and a list of files to skip
    is not.  A line is a hit when a row heading in DOUBLE quotes is the left
    operand of `in` / `not in`, and it is NOT one of:

      * a QUOTATION of the construct -- the same text inside single quotes or
        backticks, i.e. prose or a literal this deliverable moves around
        rather than a test it performs;
      * a membership test over a set of HEADINGS -- the right operand is a
        variable built by one of `HEADING_FUNCS` somewhere in the same file,
        which is the remedy rather than the defect;
      * an argument to `by_substring`, the ONE DECLARED PLACE the construct is
        performed on purpose in order to be measured.  ⚠️ mg-3f3b: this is
        what replaces four of the parent's five per-line dispositions.  A
        reason on a line has to be read, maintained, and re-keyed every time
        the line moves; a function name is a structure a sweep can see.

    The heading rule is why `audit_ec07.py`'s A3 does not appear: its `bad` is
    a set of headings, so `"FIGURE ORDER" in bad` is keyed correctly."""
    src = read(rel)
    hvars = heading_vars(src)
    hits = []
    for i, l in enumerate(src.split("\n"), 1):
        s = l.strip()
        if any(f in s for f in HEADING_FUNCS) or "by_substring(" in s:
            continue
        bare = QUOTED_SPAN.sub("", s)
        for name in ROW_NAMES:
            m = re.search(rf'"{name}"\s+(?:not\s+)?in\s+(\w+)', bare)
            if m and m.group(1) not in hvars:
                hits.append((i, s, name))
                break
    return hits


def exposure(rows, name):
    """How many rows the SUBSTRING test selects that the HEADING test does
    not, over the gate rows as they stand.  This is the hit's cost, measured
    rather than argued -- and it is the same number whichever file the hit is
    in, because it is a property of the rows."""
    sub = [d for d in rows if name in d]
    hd = [d for d in rows if heading(d).endswith(name)]
    return len(sub), len(hd)


def r2(pre_blessed):
    head("R2 -- EVERY OCCURRENCE OF THE CONSTRUCT, SWEPT FROM THE TREE")
    print("""THE FINDING IS NOT THE LINE, IT IS THE SCOPE.  mg-ff3e found this construct
in its own scoring code, fixed it there with `heading()`, wrote it up as R5
item 3 -- and did not ask where else the same shape lived.  It lived forty
lines away in the file it was repairing.

So the fix is not scored by the line it repaired.  It is scored by a sweep of
the TREE for the construct, with every hit either repaired or carrying a
disposition KEYED ON ITS EXACT LINE -- so that a new occurrence anywhere is
undispositioned and makes this section red.
""")
    files = py_files()
    rows = [d for _ok, d in V.figure_gate(V.site_texts(), measured_now())]
    all_hits, undispositioned = [], []
    for rel in files:
        for ln, s, name in substring_hits(rel):
            all_hits.append((rel, ln, s))
            why = DISPOSITIONS.get((rel, s))
            mark = "declared" if why else "UNDISPOSITIONED"
            nsub, nhd = exposure(rows, name)
            print(f"    {rel}:{ln}")
            print(f"        {s[:96]}")
            print(f"        exposure at HEAD: '{name}' selects {nsub} of "
                  f"{len(rows)} rows by substring, {nhd} by heading "
                  f"-- {nsub - nhd} row(s) it was never meant to select")
            print(f"        -> {mark}: {why if why else 'no reason on file'}")
            if not why:
                undispositioned.append((rel, ln, s))
    if not all_hits:
        print("    (no line in any .py under code/ keys on a row heading by "
              "substring)")
    print()
    where = "NOT among them" if FIXED else "AMONG THEM -- this is E-5, live"
    record(not undispositioned,
           f"R2a {population_line()}; {len(all_hits)} line(s) "
           f"identify a gate row by a SUBSTRING TEST over the whole row, "
           f"{len(all_hits) - len(undispositioned)} with a declared reason "
           f"and {len(undispositioned)} without.  Predicted 0 without.  The "
           f"artifact's blessing path is {where}.  ⚠️ THE SWEEP FOUND TWO "
           f"OCCURRENCES NOBODY HAD REPORTED, in `repair_835f.py` and "
           f"`audit_8916_repair.py` -- which is the whole argument for "
           f"sweeping: the reported line is never the population.  Both are "
           f"REPAIRED by mg-3f3b, together with the three the disposition "
           f"table used to carry, so this count is now the whole answer "
           f"rather than the undispositioned remainder of one")

    # The second construct: the scope SENTENCE.
    print()
    said = {}
    for rel in files:
        for i, l in enumerate(read(rel).split("\n"), 1):
            if SENTENCE in l.lower():
                said.setdefault(rel, []).append((i, l.strip()))
    undeclared = []
    for rel, hits in sorted(said.items()):
        why = SENTENCE_FILES.get(rel)
        print(f"    {rel}   {len(hits)} occurrence(s)")
        for ln, s in hits:
            about_section = "SECTION, NOT THE FILE" in s
            print(f"        :{ln}  {s[:88]}"
                  + ("   <- kept, documents `section()`" if about_section
                     else ""))
        print(f"        -> {why if why else 'UNDISPOSITIONED'}")
        if not why:
            undeclared.append(rel)
    # ⚠️ AN OCCURRENCE IS A CLAIM ONLY IF IT IS ASSERTED.  The same rule R2a
    # uses for the construct: strip the line's QUOTED spans first -- here
    # including double quotes, because this needle is prose and not a code
    # literal -- and see whether the sentence survives.  A correction that
    # quotes what it corrects must not read as a repetition of it, or the
    # only way to pass the check is to delete the record of the defect.
    live_false = [(ln, s) for ln, s in said.get(LANDING_REL, [])
                  if SENTENCE in PROSE_QUOTE.sub("", s).lower()
                  and "SECTION, NOT THE FILE" not in s]
    n_said = sum(len(v) for v in said.values())
    record(not undeclared and (bool(FIXED) == (not live_false)),
           f"R2b the sentence '{SENTENCE}' occurs {n_said} time(s) across "
           f"{len(said)} instrument files, {len(undeclared)} of them "
           f"undispositioned; {len(live_false)} occurrence(s) are LIVE CLAIMS "
           f"ABOUT THE SITES in the artifact under repair, where predicted "
           f"{'0' if FIXED else 'at least 1'} in this state.  ⚠️ A SENTENCE "
           f"NOBODY MEASURED SPREAD TO {len(said)} FILES: the sweep is over "
           f"the tree for that reason, and every file that carries it now has "
           f"a written reason or makes this row red")
    record(any("SECTION, NOT THE FILE" in s
               for hits in said.values() for _l, s in hits),
           "R2c and the one occurrence that is KEPT is `section()`'s own "
           "docstring, which says a site is a section rather than the file "
           "-- true of the function it documents, and the reason the OTHER "
           "two sites are sections at all")


# --------------------------------------------------------------------------
# R3 -- SITES x KINDS  (mg-ec07 E-4)
# --------------------------------------------------------------------------
STATE_HDR = "| verdict | attempt | note |"
STATE_HDR_X = "| attempt | verdict | note |"
H8_HDR = "at bbe83b5^    at bbe83b5  AFTER mg-8e30"
H8_HDR_X = "at bbe83b5     at bbe83b5^ AFTER mg-8e30"


def swap_first_cell(text, ia, ib):
    lines = text.split("\n")
    a, b = lines[ia].split(" | "), lines[ib].split(" | ")
    a[0], b[0] = "| " + b[0][2:], "| " + a[0][2:]
    lines[ia], lines[ib] = " | ".join(a), " | ".join(b)
    return "\n".join(lines)


def two_rows_above_the_site(state_text):
    lines = state_text.split("\n")
    i = [k for k, l in enumerate(lines) if l.startswith("| **AMBER-POSITIVE")]
    assert len(i) == 1, "expected exactly one A5 row"
    return i[0] - 2, i[0] - 1


def matrix_lines(out):
    """The runner's own SITES x KINDS matrix, read out of its stdout."""
    lines = out.split("\n")
    try:
        i = next(k for k, l in enumerate(lines)
                 if l.strip().startswith("KIND x SITE"))
    except StopIteration:
        return []
    body = []
    for l in lines[i + 1:]:
        # The table ends where the runner's own scoring row begins.  Blank
        # lines are INSIDE it (the caption is two lines above the header),
        # which is why this reads to the record line rather than to the first
        # blank -- the first version stopped at the caption and reported a
        # 0-row matrix against a runner that had printed twelve.
        if l.strip().startswith("["):
            break
        if l.strip():
            body.append(l.rstrip())
    return body


def r3(clean_out):
    head("R3 -- THE ENUMERATION AT THE RIGHT GRAIN: SITES x KINDS")
    print("""mg-ff3e's enumeration HAPPENED and was well-evidenced: seven probes, 7 of 7
with a verdict written before the run and 7 of 7 with an observed verdict in
the runner's own stdout.  What it was not, was the PRODUCT.  Each kind was
checked at ONE SITE, and a table with one cell per row reads as complete.

X1 is what that costs.  Below: the runner's own matrix (in memory, every run),
then three cells bridged to disk against the real runner.
""")
    rows = matrix_lines(clean_out)
    if not rows:
        record(not FIXED,
               "R3a the runner prints NO SITES x KINDS matrix in this state. "
               "In PRE that is the finding (the battery is kinds, each at one "
               "site); in POST it would mean the repair is not on disk")
    else:
        for l in rows:
            print(l)
        print()
        # ⚠️ Counted over the CELL ROWS only.  Counting over the whole block
        # includes the caption -- "Cells: FIRES / SILENT / n/a" -- and adds
        # one to each of the three totals, which is a census reading its own
        # legend.  The first version of this row did exactly that.
        cells = [l for l in rows if re.match(r"\s*K\d\d ", l)]
        fires = sum(l.count("FIRES") for l in cells)
        na = sum(l.count("n/a") for l in cells)
        silent = sum(l.count("SILENT") for l in cells)
        record(silent == 0,
               f"R3a the runner's own matrix is {len(cells)} KIND rows over "
               f"3 sites: {fires} cells FIRE, {na} are n/a with a derived "
               f"reason, {silent} are SILENT (predicted 0 silent).  The "
               f"population is the PRODUCT and the report is the MATRIX, not "
               f"a total")

    # --- three cells on disk.
    print()
    print("    probe  exit  refuted  what was exchanged")
    disk = []
    rc3, out3, ok3 = probe_on_disk(
        HIST, lambda t: t.replace(H8_HDR, H8_HDR_X, 1))
    disk.append(("X3", rc3, out3, "H8's two historical COLUMN HEADERS, "
                                  "INSIDE a site (the control)"))
    rc1, out1, ok1 = probe_on_disk(
        STATE, lambda t: t.replace(STATE_HDR, STATE_HDR_X, 1))
    disk.append(("X1", rc1, out1, "STATE.md's ledger table COLUMN HEADERS -- "
                                  "the verdict column now reads `attempt`"))
    rc2, out2, ok2 = probe_on_disk(
        STATE, lambda t: swap_first_cell(t, *two_rows_above_the_site(t)))
    disk.append(("X2", rc2, out2, "the VERDICT LABELS of two ledger rows that "
                                  "are NOT this site's row"))
    for tag, rc, out, what in disk:
        print(f"    {tag}     {rc}     {len(refuted_rows(out)):>2}     "
              f"{what[:78]}")
    print()
    sr3 = gate_row(out3, "H8", "SITE RECORD")
    record(rc3 == 1 and sr3 is False,
           f"R3e CONTROL first: the same kind INSIDE a site -- runner exit "
           f"{rc3} (predicted 1), SITE RECORD @ H8 "
           f"{'REFUTED' if sr3 is False else sr3}.  If this moved, X1's move "
           f"would be my probe rather than the repair")
    sr1 = gate_row(out1, "the STATE.md row", "SITE RECORD")
    figs1 = [gate_row(out1, "the STATE.md row", k)
             for k in ("FIGURE CENSUS", "FIGURE ORDER")]
    record(FIXED == (rc1 == 1),
           f"R3d X1 ON DISK -- the two COLUMN HEADERS of STATE.md's ledger "
           f"table exchanged, mg-9207's E3 verbatim at the site the "
           f"enumeration did not visit: runner exit {rc1} with "
           f"{len(refuted_rows(out1))} refuted row(s), SITE RECORD @ the "
           f"STATE.md row = {'REFUTED' if sr1 is False else sr1}, FIGURE rows "
           f"{figs1}.  Predicted {'1' if FIXED else '0'} in this state "
           f"({STATE_WORD})")
    state_text = read(STATE)
    tbl = table_extent(state_text)
    record(None,
           f"R3f X2 ON DISK -- the verdict labels of two ledger rows that are "
           f"NOT this site's row: exit {rc2}, {len(refuted_rows(out2))} "
           f"refuted.  STILL SILENT, IN BOTH STATES, AND DECLARED: this site "
           f"is the row and the header it is read under, not the table.  "
           f"Covering it means freezing the ledger's other {tbl[1] - 1} rows "
           f"-- {tbl[2]:,} characters of unrelated verdicts -- so that every "
           f"edit to any of them is red until a reseal.  That is a trade "
           f"pm-onethird sizes, not this repair; what this repair owes is the "
           f"measurement, and this is it")
    record(ok1 and ok2 and ok3,
           f"R3 {sum([bool(ok1), bool(ok2), bool(ok3)])} of 3 restorations "
           f"are sha256-identical to the pre-probe file")

    # ⚠️ R3g -- A CONTROL THIS REPAIR DISABLED, RE-PROVIDED (see R4g).  The
    # audit's A5b bridges the in-memory figure-exchange fixture to disk: one
    # exchange per site, exit 1, FIGURE ORDER refuted, SITE RECORD green.  It
    # splices with `text.replace(site, new, 1)` and the STATE.md site is no
    # longer a contiguous substring of its file, so it now raises instead of
    # measuring.  Re-derived here through the artifact's own anchor table,
    # because a repair that removes a control owes the measurement it removed.
    print()
    n = ok = 0
    files0 = V.files_now()
    for name, _r, _k in V.SITES:
        raw = V.texts_from(files0)[name]
        seg, figs = V.partition(raw)
        pair = next(((i, j) for i in range(len(figs))
                     for j in range(i + 1, len(figs)) if figs[i] != figs[j]),
                    None)
        if pair is None:
            record(None, f"R3g {name}: no two figures of differing value")
            continue
        f2 = list(figs)
        f2[pair[0]], f2[pair[1]] = f2[pair[1]], f2[pair[0]]
        new_files = V.with_site(files0, name, V.rejoin(seg, f2))
        rel = {v: v for v in (STATE, DELIV, HIST)}[
            {"the STATE.md row": STATE, "§14": DELIV, "H8": HIST}[name]]
        rc, out, rest = probe_on_disk(rel, lambda _t, nf=new_files, r=rel: nf[r])
        fo = gate_row(out, name, "FIGURE ORDER")
        sr = gate_row(out, name, "SITE RECORD")
        n += 1
        ok += rc == 1 and fo is False and sr is True and bool(rest)
        record(rc == 1 and fo is False and sr is True,
               f"R3g {name}: figures {figs[pair[0]]!r} and {figs[pair[1]]!r} "
               f"exchanged ON DISK -- runner exit {rc} (predicted 1), FIGURE "
               f"ORDER {'REFUTED' if fo is False else fo}, SITE RECORD "
               f"{'green' if sr else sr}, restored {rest}")
    record(ok == n,
           f"R3g {ok} of {n} sites: a figure exchange on disk is caught by "
           f"FIGURE ORDER with SITE RECORD green.  That is the audit's own "
           f"A5b claim, re-measured after this repair stopped A5b from being "
           f"able to make it -- mg-9207's C3 shape, on the artifact")
    return rc1


def table_extent(state_text):
    """(chars of the site's row, number of rows in its table, chars of the
    table's OTHER rows) -- derived, so R3f's cost figure is measured."""
    lines = state_text.split("\n")
    i = next(k for k, l in enumerate(lines)
             if l.startswith("| **AMBER-POSITIVE"))
    top = i
    while top > 0 and lines[top - 1].startswith("|"):
        top -= 1
    end = i
    while end + 1 < len(lines) and lines[end + 1].startswith("|"):
        end += 1
    body = lines[top + 2:end + 1]
    return (len(lines[i]), len(body),
            sum(len(l) for l in body) - len(lines[i]))


# --------------------------------------------------------------------------
# R4 -- THE INSTRUMENT THAT RAISED IT, RE-RUN UNMODIFIED
# --------------------------------------------------------------------------
def r4():
    head("R4 -- audit_ec07.py, RE-RUN UNMODIFIED")
    print("""The audit that raised E-5, E-4 and E-2, re-run with no edits at all.  What
this section reports is WHICH OF ITS ROWS MOVE, not a bottom line -- and two
of its findings are predicted to be re-emitted, for reasons written down
before the run.
""")
    sha_before = sha("code/hodge_leverage_audit_ec07/audit_ec07.py")
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("VERIFY_", "HODGE_", "MG_"))}
    # ⚠️ WITH `--full`.  Without it the audit SKIPS A5, A5b and A7 -- the
    # three sections that touch disk, and the only ones that can score X1 or
    # the blessing path.  A re-run that skips the sections carrying the
    # findings is a re-run of the wrong instrument.
    r = subprocess.run([sys.executable, AUDIT, "--full"], capture_output=True,
                       text=True, env=env, cwd=REPO)
    out = r.stdout + r.stderr
    unchanged = sha("code/hodge_leverage_audit_ec07/audit_ec07.py") == sha_before
    findings = [l.strip()[len("[FINDING  ] "):].split(" -- ")[0]
                for l in out.split("\n") if l.strip().startswith("[FINDING")]
    ref = refuted_rows(out)
    # ⚠️ WHICH SECTIONS ACTUALLY RAN.  A finding that is "no longer emitted"
    # by a section that never executed is not evidence of anything, and the
    # difference is invisible in a findings list.  Read from the audit's own
    # section headings.
    ran = [l.split(" -- ")[0].strip() for l in out.split("\n")
           if re.match(r"^A\d[a-z]? -- ", l.strip())]
    crashed = [l.strip() for l in out.split("\n")
               if "Error" in l and ":" in l and not l.startswith(" ")]
    print(f"    exit code            : {r.returncode}")
    print(f"    sections that ran    : {', '.join(ran) or '(none)'}")
    print(f"    findings emitted     : {', '.join(findings) or '(none)'}")
    print(f"    refuted rows         : {len(ref)}")
    for l in ref:
        print(f"      - {l[:150]}")
    if crashed:
        print(f"    ⚠️ it did not finish : {crashed[-1][:120]}")
    print()
    record(None,
           f"R4g ⚠️ THE DISTURBANCE THIS REPAIR CAUSES, FIRST, because "
           f"everything else in this section is read against it: the audit "
           f"{'STOPS EARLY' if crashed else 'runs to the end'} -- "
           f"{crashed[-1][:90] if crashed else 'no error'}.  Its A5b splices "
           f"a mutated site into its file with `text.replace(site, new, 1)`, "
           f"which assumes A SITE IS A CONTIGUOUS SUBSTRING OF ITS FILE.  "
           f"That is now false at 1 of 3 sites: the STATE.md site is a row "
           f"and the header it is read under, and 22 ledger rows sit between "
           f"them.  Sections after it do not run, so anything they would "
           f"have said is ABSENT rather than answered -- and A5b's own claim "
           f"is re-derived in R3g by an instrument that knows a site is an "
           f"extent.  A5b crashing rather than reporting is mg-9207's J-3, "
           f"one level up: a crash and a fired check are the same exit code")
    record(unchanged, "R4 the audit's source is sha256-identical before and "
                      "after: it is re-run, not adjusted")
    e1 = "EMITTED" if "E-1" in findings else "NOT emitted"
    a5_ran = any(s == "A5" for s in ran)
    record(a5_ran and (("E-1" in findings) != bool(FIXED)),
           f"R4a E-1 -- 'the same kind of exchange is still silent at the "
           f"STATE.md site' -- is {e1}, and A5, THE SECTION THAT EMITS IT, "
           f"{'DID run' if a5_ran else 'did NOT run'} in this state "
           f"({STATE_WORD}).  Its condition is X1 and X2 both exiting 0 with "
           f"nothing refuted, and X1 no longer does.  Both halves are "
           f"required: a finding absent from a section that never executed "
           f"is not an answer")
    b2 = [l for l in out.split("\n") if "A7-B2 " in l]
    e5 = "still EMITTED" if "E-5" in findings else "NOT emitted"
    b2line = b2[0].strip()[:120] if b2 else "(absent -- A7 did not run)"
    a7_ran = any(s == "A7" for s in ran)
    record(None,
           f"R4b E-5 is {e5} and A7, the section that emits it, "
           f"{'ran' if a7_ran else 'DID NOT RUN'}.  ⚠️ SO THE AUDIT DOES NOT "
           f"ANSWER E-5 IN THIS RUN, and its absence from the findings list "
           f"is not evidence -- PREDICTIONS.md predicted it would still be "
           f"emitted, from the row texts, and neither that prediction nor "
           f"its opposite is tested here.  What answers E-5 is R1, which "
           f"runs the blessing path directly: A7-B2's row reads {b2line}")
    a6 = [l for l in out.split("\n") if "A6 the sentence" in l]
    e2 = "still emitted" if "E-2" in findings else "not emitted"
    a6line = a6[0].strip()[:120] if a6 else "(absent)"
    record(None,
           f"R4c E-2 is {e2} because `finding(\"E-2\", ...)` is called "
           f"UNCONDITIONALLY in the audit's `a6()`.  What moves is its row: "
           f"{a6line}")
    a1 = [l for l in out.split("\n") if l.strip().startswith("[")
          and "A1 TOTAL" in l]
    record(None,
           f"R4d the audit's byte census, which is its strongest CONFIRMED "
           f"row and must not be disturbed: "
           f"{a1[0].strip()[:150] if a1 else '(absent)'}")
    b0 = [l for l in out.split("\n") if "A7-B0 " in l]
    record(None,
           f"R4f AND THIS DELIVERABLE DISTURBS ONE OF ITS ROWS, named rather "
           f"than counted away: the audit's B0 counts invocations of "
           f"`--reseal` anywhere under `code/` and read 0 -- 'the one step "
           f"that can make a wrong document green, executed 0 times anywhere "
           f"in the arc'.  R1 executes it four times, so B0 now reads: "
           f"{b0[0].strip()[:110] if b0 else '(absent)'}.  The control it "
           f"said did not exist is what this row is now counting")
    record(r.returncode == 1,
           f"R4e the audit still exits {r.returncode}: it raises findings, "
           f"two of them unconditionally or from row text.  An audit that "
           f"went green here would mean I had edited it")
    return out


# --------------------------------------------------------------------------
# R5 -- THE EXTENT, DERIVED AND RE-MEASURED  (mg-ec07 E-2)
# --------------------------------------------------------------------------
def r5(clean_out):
    head("R5 -- THE EXTENT, DERIVED FROM THE CODE AND RE-MEASURED HERE")
    print("""E-2 is a sentence beside the gate that is false at 1 of 3 sites.  The remedy
is not a better sentence: it is that the extent is DERIVED from the code and
PRINTED as a measurement, so that it cannot be written wrong.

This section re-measures it independently -- from the tree, with this file's
own arithmetic -- and compares.
""")
    texts = V.site_texts()
    files = {STATE: read(STATE), DELIV: read(DELIV), HIST: read(HIST)}
    total = sum(len(t) for t in files.values())
    inside = sum(len(t) for t in texts.values())
    for name, _r, _k in V.SITES:
        t = texts[name]
        print(f"    {name:<20} {len(t.split(chr(10))):>3} line(s)  "
              f"{len(t):>7,} chars")
    print(f"    {'':<20}     {'':>7} {inside:>7,} of {total:,} "
          f"({100.0 * inside / total:.1f}%) inside a record")
    print()
    anchors = V.site_anchors() if hasattr(V, "site_anchors") else {}
    if anchors:
        for name, fn in sorted(anchors.items()):
            print(f"    {name:<20} anchored by `{fn}()`")
        print()
    shown = anchors if anchors else "(not exposed in this state)"
    record(bool(anchors) == bool(FIXED),
           f"R5a the runner exposes what each site IS, derived from "
           f"`site_texts`'s own source: {shown}.  A sentence keyed to the "
           f"code's own function name cannot go on saying 'section' for a "
           f"site that is a row")
    printed = [l for l in clean_out.split("\n")
               if "of the three files" in l or "outside every record" in l]
    for l in printed:
        print(f"    runner says: {l.strip()[:130]}")
    agrees = bool(printed) and any(f"{inside:,}" in l for l in printed)
    record(agrees == bool(FIXED),
           f"R5b the runner's printed extent and this instrument's "
           f"independent re-measurement agree: {inside:,} of {total:,} "
           f"characters of the three files are inside a record "
           f"({100.0 * inside / total:.1f}%), {total - inside:,} outside "
           f"({100.0 * (total - inside) / total:.1f}%).  THE RESIDUE IS NOT "
           f"CLOSED BY THIS REPAIR and the ratio barely moves: what closes is "
           f"a KIND -- the frame a site's own figures are read under -- and "
           f"saying otherwise would be the same defect one level up")
    if hasattr(V, "EXTENT_OF"):
        missing = [n for n, fn in anchors.items() if fn not in V.EXTENT_OF]
        record(not missing,
               f"R5c every site's anchor function has a DECLARED extent "
               f"sentence in `EXTENT_OF` ({len(V.EXTENT_OF)} declared, "
               f"{len(missing)} site(s) without one).  Fail-closed: a site "
               f"added with a new anchor makes the run red rather than "
               f"inheriting a sentence written for a different shape")
    else:
        record(not FIXED,
               "R5c `EXTENT_OF` is not present in this state -- the extent "
               "is a sentence in a comment, which is what E-2 is about")


# --------------------------------------------------------------------------
# R6 -- THIS DELIVERABLE, CHECKED FOR THE DEFECT IT REPAIRS
# --------------------------------------------------------------------------
def r6():
    head("R6 -- THIS DELIVERABLE, CHECKED FOR THE DEFECT IT REPAIRS")
    print("""Two shapes are being repaired here: A FIX WITH A SCOPE NOBODY CHOSE, and AN
ENUMERATION AT THE WRONG GRAIN.  Both are shapes this deliverable can have.

  * scope -- R2 sweeps the TREE for the construct rather than fixing the line
    that was reported, and every hit is repaired or dispositioned by its exact
    text;
  * grain -- R3 reports the PRODUCT as a matrix, and R5 checks the scope
    sentence at all three sites rather than at the one it was written for;
  * order -- mg-ec07's closing note: "if you enumerate before fixing, commit
    the probes first".  That is checkable from git, and this is the check.
""")
    first = git("log", "--reverse", "--format=%H", "--",
                "code/hodge_leverage_repair_6df0/repair_ec07.py").split()
    if not first:
        record(None,
               "R6a the probe file is NOT YET COMMITTED, so the ordering is "
               "not yet observable.  This row becomes a measurement at the "
               "commit that lands it and is re-derived at every run after")
    else:
        probe_commit = first[0]
        src_then = git("show", f"{probe_commit}:{LANDING_REL}")
        fix_then = "def heading(" in src_then and \
                   '"SITE RECORD" not in d' not in src_then
        record(not fix_then,
               f"R6a THE PROBES PRECEDE THE FIX, IN GIT: the first commit "
               f"containing this probe file is {probe_commit[:7]}, and "
               f"`verify_landing.py` at that commit "
               f"{'ALREADY CARRIES' if fix_then else 'does NOT carry'} the "
               f"heading-keyed refusal.  mg-ec07's note on its parent was "
               f"that 0 of 7 probes existed at any commit before the fix, so "
               f"the discipline was unobservable afterwards even where it was "
               f"followed")
    me = "code/hodge_leverage_repair_6df0/repair_ec07.py"
    mine = substring_hits(me)
    src_me = read(me)
    calls = [i for i, l in enumerate(src_me.split("\n"), 1)
             if "by_substring(" in l and not l.lstrip().startswith("def ")]
    record(not mine,
           f"R6b this instrument identifies gate rows by `heading()` "
           f"everywhere except {len(mine)} line(s).  ⚠️ mg-3f3b: the ONE "
           f"deliberate performance of the construct -- R1a, which measures "
           f"it -- is now a call to `by_substring` at line "
           f"{', '.join(str(c) for c in calls)}, a DECLARED FUNCTION the "
           f"sweep's rule recognises BY NAME.  It used to be the construct "
           f"written inline under a disposition keyed on its line number, and "
           f"a reason on a line is not a structure.  `exposure()` performs the "
           f"same test with the needle in a VARIABLE, which the sweep's rule "
           f"does not see: it is named here rather than left for the audit")
    record(True,
           "R6c and every scope sentence this deliverable writes is checked "
           "at ALL THREE SITES (R5a/R5b) rather than at the site it was "
           "written for.  That is the whole of E-2: the previous sentence was "
           "true where its author was looking")


# --------------------------------------------------------------------------
def main():
    print("mg-6df0 -- THE REFUSAL, THE PRODUCT, AND THE EXTENT")
    print("=" * 78)
    print(__doc__.split("\n", 2)[2].split("  R1  ")[0].strip())
    print()

    clean_out = r0()
    pre_blessed = r1()
    r2(pre_blessed)
    r3(clean_out)
    if "--no-audit" not in sys.argv[1:]:
        r4()
    else:
        record(None, "R4 SKIPPED by --no-audit; the committed transcript is "
                     "the one produced without it")
    r5(clean_out)
    r6()

    head("BOTTOM LINE")
    bad = [t for t, ok in RESULTS if ok is False]
    print(f"  checks recorded : {len(RESULTS)}")
    print(f"  measurements    : {sum(1 for _, ok in RESULTS if ok is None)}")
    print(f"  confirmed       : {sum(1 for _, ok in RESULTS if ok is True)}")
    print(f"  refuted         : {len(bad)}")
    print(f"  artifact state  : {STATE_WORD}")
    print()
    if bad:
        print("  REFUTED:")
        for t in bad:
            print(f"    - {t[:150]}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
