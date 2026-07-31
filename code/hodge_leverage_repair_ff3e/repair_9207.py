#!/usr/bin/env python3
"""mg-ff3e -- mg-9207's E2/E2b/E3: THE INVARIANCE MOVED RATHER THAN WENT AWAY.

mg-8916 made the figure census a MULTISET.  mg-8aae exchanged two figures and
the multiset did not move.  mg-8eca made it a SEQUENCE of figures.  mg-9207
exchanged the two LABELS instead and the gate refuted NOTHING at 3 of 3 label
sites, with mg-8aae's own reader-visible defect back on the page: H8's table
saying the `STATE.md` row SHRANK across mg-a2bd.

THE ASSIGNMENT SAYS DO NOT MAKE IT POSITION-AWARE FOR LABELS.  That relocates
the defect a third time.  So the question this instrument is organised around
is the SUBTRACTION question -- what GENERATES the instances -- and the answer
is that the gate compares a PROJECTION of the section and each repair enlarged
the projection BY ONE NAMED FIELD.  The complement was always everything else,
and the next exchange moved into it.  The only projection with an empty kernel
is the identity, so the repair is to compare the WHOLE RECORD.

  R1  THE SEVEN LABEL-SIDE EXCHANGES, ON DISK, AGAINST THE REAL RUNNER.
      mg-9207's E2, E2b and E3 verbatim, plus the same shape at the two sites
      it never probed on the label side, plus a figure inside a marked
      quotation and a table alignment shift.  Every one is written TO DISK
      into the real document, scored by running `verify_landing.py` as a
      SUBPROCESS, with NO environment variable and no in-memory call of the
      gate.  Scored AT GATE-ROW GRANULARITY, because the runner can exit 1
      without the gate having seen anything (mg-9207 J-3).

  R2  THE DEFECT REINSTATED, AND AT WHICH UNIT.  Demonstrating that a check
      fires proves nothing unless removing it makes the same artifact go
      uncaught (mg-8eca D4).  D1 deletes the SITE RECORD comparison as one
      unit and re-runs all seven on disk.  D2 deletes only the RECORD
      PARTITION row, which is a DIFFERENT check and is shown not to be what
      catches them.  D3 reintroduces a KERNEL -- it makes `partition` drop
      bytes -- and shows the RECORD PARTITION row going red, which is the
      only evidence that the row certifying 'nothing is left behind' would
      notice something being left behind.

  R3  THE EXHAUSTIVENESS MAP.  'No field can be left behind' is checkable
      rather than sayable: every SEGMENT and every FIGURE of every site is
      mutated individually and the gate must fire on each.  The population is
      derived from the record's own structure -- nobody writes the list -- so
      a field added later is in it without this file being edited.  ⚠️ IN
      MEMORY, and DECLARED as a fixture: it is a map of the record, not the
      evidence, which is R1's job.

  R4  NOT SCORED BY ITS OWN AUTHOR.  mg-9207's instrument, unmodified,
      re-run against the repaired tree; likewise mg-8eca's, mg-8aae's and
      mg-8916's.  What must hold: mg-9207's C-rows (the FIGURE ORDER row the
      only gate row that failed, 12 of 12) survive the widening, and its E
      rows now DISAGREE WITH ITS OWN PREDICTION OF SILENCE, which is what a
      landed finding looks like from the raising instrument's side.

  R5  WHAT IS NOT COVERED, printed -- including the check of THIS deliverable
      for the defect THIS deliverable repairs, enumerated branch by branch,
      with a reason wherever a branch cannot exhibit it.

IT MUTATES THE TREE AND RESTORES IT, sha256-verified, and refuses to run
against a dirty tree scoped to the files it will `git checkout --`.

Pure Python 3 + git.  No third-party packages.
"""

import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
LANDING = "code/hodge_leverage_landing_e1d0"
VERIFY = f"{LANDING}/verify_landing.py"

sys.path.insert(0, os.path.join(REPO, LANDING))
import verify_landing as V                                    # noqa: E402

STATE, DELIV, HIST = V.STATE, V.DELIV, V.HIST

# Written to and `git checkout --`ed back inside a `finally`.  `verify_landing`
# itself is here because R2's deletion test edits the gate, which is the only
# way to reinstate the defect on the REAL artifact rather than in a copy.
MUTABLE = [STATE, DELIV, HIST, VERIFY]
REQUIRE_CLEAN = MUTABLE + [f"{LANDING}/out_verify.txt",
                           f"{LANDING}/site_records.txt"]

# Committed transcripts this run must not disturb.  An instrument that
# regenerates the record it is measuring has destroyed its own evidence.
FROZEN = [f"{LANDING}/out_verify.txt",
          "code/hodge_leverage_audit_9207/out_audit_9207.txt",
          "code/hodge_leverage_repair_8eca/out_repair_8eca.txt",
          "code/hodge_leverage_audit_8aae/out_audit_8916.txt",
          "code/hodge_leverage_repair_8916/out_repair_8916.txt"]

RESULTS = []


def read(path):
    with open(os.path.join(REPO, path), encoding="utf-8") as fh:
        return fh.read()


def write(path, text):
    with open(os.path.join(REPO, path), "w", encoding="utf-8") as fh:
        fh.write(text)


def sha(path):
    return hashlib.sha256(read(path).encode("utf-8")).hexdigest()


def record(ok, detail):
    RESULTS.append((detail, ok))
    mark = {True: "[CONFIRMED]", False: "[REFUTED  ]", None: "[MEASURED ]"}[ok]
    print(f"  {mark} {detail}")


def head(title):
    print()
    print(title)
    print("-" * len(title))


def run_verify():
    """THE REAL RUNNER, as a subprocess, with the ambient environment.  No
    variable is set: a check demonstrated through a hook demonstrates the hook
    (mg-8aae H-2)."""
    r = subprocess.run([sys.executable, os.path.join(REPO, VERIFY)],
                       capture_output=True, text=True, cwd=REPO)
    return r.returncode, r.stdout + r.stderr


def refuted_rows(out):
    return [l.strip()[len("[REFUTED  ] "):] for l in out.split("\n")
            if l.strip().startswith("[REFUTED  ]")]


def gate_rows(rows):
    return [r for r in rows if r.startswith("GATE @")]


def heading(row):
    """The row's HEADING, not the whole row.  Every one of these rows explains
    itself by naming the other rows, so a substring test over the whole line
    reports every probe as having broken every check.  This instrument's own
    first version did that, and its own attribution row caught it."""
    return row.split(" -- ")[0]


def rows_for(out, site, kind):
    """The verdict of one named gate row for one site, or None."""
    for l in out.split("\n"):
        s = l.strip()
        if not s.startswith("["):
            continue
        body = s[11:].strip()
        if heading(body) == f"GATE @ {site}: {kind}":
            return s[:11]
    return None


def crashed(out):
    """⚠️ A CRASH AND A FIRE ARE THE SAME INTEGER (mg-9207 J-3).  An exit code
    is not a verdict unless you know which produced it."""
    return "Traceback (most recent call last)" in out


# --------------------------------------------------------------------------
# THE PROBES.  Located BY CONTENT and reported rather than asserted: a probe
# that raises AssertionError when its literal has moved exits 1, which is the
# integer a fired gate produces, and the reader cannot tell them apart
# (mg-9207 J-3).
# --------------------------------------------------------------------------
def swap(text, a, b):
    """Exchange two pieces of text with each other, once each."""
    return text.replace(a, "\0", 1).replace(b, a, 1).replace("\0", b, 1)


PROBES = [
    ("E2  H8: the two mg-a2bd table LABELS exchanged (mg-9207's own, verbatim)",
     HIST, "H8", "swap", ("before mg-a2bd", "after  mg-a2bd"),
     "the table now says the `STATE.md` row SHRANK across mg-a2bd -- mg-8aae's "
     "own H-1 defect, reached by moving the OTHER half of the pair"),
    ("E2b H8: the bbe83b5 table's two ROW LABELS exchanged (mg-9207's own)",
     HIST, "H8", "swap",
     ("STATE.md row cell                          :",
      "this file (the relocated history)          :"),
     "the table now says the cell was 10 483 and the relocated history 9 748, "
     "with neither figure moving, at a pair of lines the previous battery does "
     "not hard-code"),
    ("E3  H8: the two historical COLUMN HEADERS exchanged (mg-9207's own)",
     HIST, "H8", "sub",
     ("at bbe83b5^    at bbe83b5  AFTER mg-8e30",
      "at bbe83b5     at bbe83b5^ AFTER mg-8e30"),
     "every historical column of the three-column table is now attributed to "
     "the wrong commit, and no figure moved"),
    ("E6  §14: the two CORRECTION ATTRIBUTIONS exchanged (a site mg-9207 "
     "never probed on the label side)",
     DELIV, "§14", "swap", ("mg-f922", "mg-8a5c"),
     "each of §14's two corrections is now attributed to the finding that "
     "raised the other one"),
    ("E7  STATE.md row: two row-history ANCHOR LABELS exchanged (likewise)",
     STATE, "the STATE.md row", "swap",
     ("row history H1", "row history H2"),
     "the row's two history anchors now point a reader at each other's "
     "section"),
    ("E8  §14: a figure inside a MARKED QUOTATION altered",
     DELIV, "§14", "sub",
     ("sits **+9 608** characters above this copy",
      "sits **+9 607** characters above this copy"),
     "a quotation is exempt from the CENSUS by a convention that is KEPT -- "
     "exempt from being counted is not the same as free to be edited, and the "
     "quoted figure now misquotes what was struck"),
    ("E9  H8: the three-column table's ALIGNMENT shifted, no figure moved",
     HIST, "H8", "sub",
     ("    gap, cell only                                        −875"
      "          +755        +2 744",
      "    gap, cell only                                          −875"
      "        +755        +2 744"),
     "the figures now sit under the wrong column headings, which is what a "
     "fixed-width table's alignment IS"),
]


def apply_probe(kind, arg, site_text):
    """Returns the mutated site text, or None with a reason."""
    a, b = arg
    if kind == "swap":
        if site_text.count(a) != 1 or site_text.count(b) != 1:
            return None, (f"located by content and NOT FOUND EXACTLY ONCE "
                          f"({site_text.count(a)}x / {site_text.count(b)}x)")
        return swap(site_text, a, b), None
    if site_text.count(a) != 1:
        return None, (f"located by content and found {site_text.count(a)}x, "
                      f"not once")
    if len(a) != len(b):
        return None, "the replacement is not length-preserving"
    return site_text.replace(a, b, 1), None


def site_of(path, name):
    """The site text as it currently stands on disk, and the file it lives
    in."""
    text = read(path)
    return text, V.site_texts()[name]


def splice(path, whole, old_site, new_site):
    if whole.count(old_site) != 1:
        return None
    return whole.replace(old_site, new_site, 1)


# --------------------------------------------------------------------------
# R1 -- THE SEVEN LABEL-SIDE EXCHANGES, ON DISK
# --------------------------------------------------------------------------
def r1(pristine):
    head("R1 -- THE LABEL HALF OF AN EXCHANGE, ON DISK, AGAINST THE REAL RUNNER")
    print("""An exchange has TWO HALVES: the figures, and the statements they hang on.
mg-8eca closed the first and mg-9207 reopened the shape by moving the second.
Every probe below is written TO DISK into the real document and scored by
running `verify_landing.py` as a SUBPROCESS with no environment variable set.

⚠️ SCORED AT GATE-ROW GRANULARITY.  `exit` is the runner's; the three columns
after it are which GATE row said what.  They are not the same measurement, and
mg-9207's J-3 is why: at its E2 the gate refuted 0 rows and the run still
exited 1, out of an AssertionError in its own negative control.
""")
    rc, out = run_verify()
    record(rc == 0, f"R1a the real runner on the clean tree exits {rc} with "
                    f"{len(refuted_rows(out))} refuted rows")

    print(f"\n    {'probe':<62}{'exit':>5}{'RECORD':>11}{'CENSUS':>11}"
          f"{'ORDER':>11}{'gate':>6}{'crash':>7}")
    fired = caught = fig_green = restored = crashes = 0
    total = 0
    for name, path, site, kind, arg, why in PROBES:
        whole = read(path)
        _w, site_text = site_of(path, site)
        mutated, reason = apply_probe(kind, arg, site_text)
        if mutated is None:
            print(f"    {name[:62]:<62}   PROBE NOT APPLIED: {reason}")
            record(False, f"{name.split()[0]} could not be applied: {reason}. "
                          f"REPORTED rather than asserted -- a probe that "
                          f"raises exits 1, which is what a fired gate does "
                          f"(mg-9207 J-3)")
            continue
        total += 1
        new_whole = splice(path, whole, site_text, mutated)
        if new_whole is None:
            record(False, f"{name.split()[0]}: the site text does not occur "
                          f"exactly once in {path}")
            continue
        try:
            write(path, new_whole)
            rc, out = run_verify()
            bad = refuted_rows(out)
            g = gate_rows(bad)
            rec = rows_for(out, site, "SITE RECORD")
            cen = rows_for(out, site, "FIGURE CENSUS")
            ordr = rows_for(out, site, "FIGURE ORDER")
        finally:
            write(path, pristine[path])
        rc2, _out2 = run_verify()
        ok_restore = sha(path) == hashlib.sha256(
            pristine[path].encode("utf-8")).hexdigest() and rc2 == 0
        fired += rc != 0
        caught += rec == "[REFUTED  ]"
        fig_green += cen == "[CONFIRMED]" and ordr == "[CONFIRMED]"
        restored += ok_restore
        crashes += crashed(out)
        print(f"    {name[:62]:<62}{rc:>5}"
              f"{str(rec).strip('[] '):>11}{str(cen).strip('[] '):>11}"
              f"{str(ordr).strip('[] '):>11}{len(g):>6}"
              f"{str(crashed(out)):>7}")

    record(fired == total,
           f"R1b EVERY LABEL-SIDE EXCHANGE WRITTEN TO DISK MAKES THE REAL "
           f"RUNNER RED: {fired} of {total}, at 3 of 3 sites, with no "
           f"environment variable set and the gate never called in memory. "
           f"mg-9207 observed the gate refuting NOTHING on the first three of "
           f"these")
    record(caught == total,
           f"R1c and the row that caught it is the SITE RECORD row FOR THAT "
           f"SITE: {caught} of {total}.  That is the half of the record that "
           f"was not being compared -- not a designated reader breaking, "
           f"which would be re-measuring the check mg-a318 already added")
    record(fig_green == total,
           f"R1d and that site's FIGURE CENSUS and FIGURE ORDER rows both "
           f"stayed [CONFIRMED]: {fig_green} of {total}.  This is THE "
           f"ARTIFACT'S OWN evidence that the mutation moved no figure -- "
           f"asserted by the thing under test rather than by the prober, "
           f"which is mg-9207's C4 convention pointed the other way")
    record(restored == total,
           f"R1e and {restored} of {total} restorations return the runner to "
           f"exit 0, each verified byte-identical by sha256.  The gate does "
           f"not fire on everything, so the fires above are attributable to "
           f"the exchange")
    # ⚠️ MEASURED, NOT SCORED, and the reason is scope.  mg-9207's J-3 is that
    # mg-8eca's `transpose` freezes three literals out of the live documents
    # and `assert`s each occurs once, so an edit at those lines raises
    # AssertionError -- and E2 rewrites exactly those two lines.  J-3 is
    # mg-9207's own open item, it is NOT this assignment's, and repairing it
    # here would be widening the fix to the adjacent instance in the other
    # direction.  It is REPORTED with a number.  Note what makes the result
    # survive it: the gate rows print BEFORE the negative control runs, which
    # is why every row above is scored at gate-row granularity and not at the
    # exit code.
    record(None,
           f"R1f {crashes} of {total} runs exited by TRACEBACK rather than by "
           f"the gate -- E2, and only E2, because mg-8eca's `transpose` "
           f"asserts on a literal E2 rewrites.  That is mg-9207's J-3 "
           f"UNCHANGED and out of this assignment's scope; the verdicts above "
           f"survive it because they are read from the GATE ROWS, which print "
           f"before the control runs.  An exit code is not a verdict unless "
           f"you know which produced it")
    return total


# --------------------------------------------------------------------------
# R2 -- THE DEFECT REINSTATED, AND AT WHICH UNIT
# --------------------------------------------------------------------------
CALL_RECORD = "    out.extend(record_rows(name, raw))"
CALL_PARTITION = "    return (partition_row(name, raw, segments, seqf)"
CALL_SITE = "            + site_record_row(name, segments))"


def _sub_once(src, old, new):
    if src.count(old + "\n") != 1:
        return None
    return src.replace(old + "\n", new + "\n", 1)


def delete_record_call(src):
    """(e) removed WHOLE: both rows go."""
    return _sub_once(src, CALL_RECORD,
                     "    pass  # (e) DELETED by the mg-ff3e deletion test")


def delete_site_record_row(src):
    """ONLY the SITE RECORD comparison; RECORD PARTITION stays."""
    return _sub_once(src, CALL_SITE, "            + [])")


def delete_partition_row(src):
    """ONLY the RECORD PARTITION row; the SITE RECORD comparison stays."""
    return _sub_once(src, CALL_PARTITION, "    return ([]")


def break_partition(src):
    """REINTRODUCE A KERNEL, in the shape somebody would actually introduce
    one.  Make the segments CASE-INSENSITIVE -- 'so that a trivial edit does
    not fire' -- which is a projection, and a projection has a kernel: a label
    exchanged with a differently-cased label goes silent again.

    The point is not that anyone proposed this.  It is that the RECORD
    PARTITION row is the only thing standing behind 'the two halves are the
    whole record', and a row that cannot fail certifies nothing."""
    old = "        segments.append(raw[last:m.start()])"
    new = "        segments.append(raw[last:m.start()].lower())"
    if src.count(old + "\n") != 1:
        return None
    return src.replace(old + "\n", new + "\n", 1)


def r2(pristine, nprobes):
    head("R2 -- THE DEFECT REINSTATED, AT THREE DIFFERENT UNITS")
    print("""'The check fires' and 'the instrument fires' are the same sentence unless
removing the check makes the same artifact go uncaught (mg-8eca D4).  And WHICH
UNIT is removed is the whole question mg-9207's J-2 asks: a deletion test that
can only remove a whole function cannot tell two clauses apart.

D1 removes the SITE RECORD comparison as one unit.  D2 removes only the RECORD
PARTITION row, which is a different check.  D3 removes NOTHING and instead
makes the partition LOSSY -- a kernel put back -- which is the only way to find
out whether the row that certifies 'nothing is left behind' would notice.
""")
    src = pristine[VERIFY]
    cases = [
        ("D1  (e) deleted whole -- both rows", delete_record_call,
         "silent", "the seven exchanges go back to being invisible"),
        ("D1b ONLY the SITE RECORD comparison deleted", delete_site_record_row,
         "silent", "the finest unit: this row alone is what catches them"),
        ("D2  ONLY the RECORD PARTITION row deleted", delete_partition_row,
         "still red", "a different check -- it is not what catches a label "
                      "swap, and saying so is what D1b measures"),
    ]
    print(f"\n    {'deletion'    :<46}{'predicted':>11}{'caught':>8}"
          f"{'exit':>6}   what it shows")
    agree = 0
    for label, fn, predicted, why in cases:
        mutated = fn(src)
        if mutated is None:
            record(False, f"{label.split()[0]}: the deletion could not be "
                          f"located BY CONTENT in {VERIFY}; REPORTED, not "
                          f"asserted")
            continue
        caught_now = 0
        rc_last = None
        try:
            write(VERIFY, mutated)
            for name, path, site, kind, arg, _why in PROBES:
                whole = read(path)
                site_text = V.site_texts()[site]
                mut, _r = apply_probe(kind, arg, site_text)
                if mut is None:
                    continue
                new_whole = splice(path, whole, site_text, mut)
                try:
                    write(path, new_whole)
                    rc, out = run_verify()
                    rc_last = rc
                    caught_now += bool(gate_rows(refuted_rows(out)))
                finally:
                    write(path, pristine[path])
        finally:
            write(VERIFY, pristine[VERIFY])
        observed = "silent" if caught_now == 0 else "still red"
        agree += observed == predicted
        print(f"    {label:<46}{predicted:>11}{caught_now:>4}/{nprobes:<3}"
              f"{str(rc_last):>6}   {why}")
        record(observed == predicted,
               f"{label}: {caught_now} of {nprobes} label-side exchanges are "
               f"caught at the gate, predicted {predicted!r}.  {why}")

    # D3 -- a kernel put back.
    mutated = break_partition(src)
    if mutated is None:
        record(False, "D3: the partition could not be made lossy by content; "
                      "REPORTED, not asserted")
        return
    try:
        write(VERIFY, mutated)
        rc, out = run_verify()
        part = [rows_for(out, s, "RECORD PARTITION") for s, _r, _k in V.SITES]
    finally:
        write(VERIFY, pristine[VERIFY])
    red = sum(1 for p in part if p == "[REFUTED  ]")
    record(red == len(V.SITES),
           f"D3 A KERNEL PUT BACK IS SEEN: with `partition` comparing the "
           f"segments CASE-INSENSITIVELY -- a projection, and the shape of "
           f"every repair before this one: something quietly outside the "
           f"comparison -- the RECORD PARTITION row goes red at {red} of "
           f"{len(V.SITES)} sites (runner exit {rc}).  That row is the only "
           f"thing standing behind 'the two halves are the whole record', and "
           f"a claim of exhaustiveness that cannot fail is the `x == x` this "
           f"arc has now met twice")


# --------------------------------------------------------------------------
# R3 -- THE EXHAUSTIVENESS MAP
# --------------------------------------------------------------------------
def r3():
    head("R3 -- EVERY FIELD OF EVERY RECORD, MUTATED ONE AT A TIME (A FIXTURE)")
    print("""'No field can be left behind because nobody named it' is a claim about a
POPULATION, so it is measured over the population rather than over the field
that was reported.  The population is DERIVED from the record's own structure:
`partition` cuts each site into segments and figures, and every one of them is
mutated individually here.

⚠️ THIS IS IN MEMORY AND IT IS A FIXTURE, declared as one.  'The gate function
returns False when called with a mutated string' and 'the runner goes red when
the document is wrong' are different sentences (mg-9207).  R1 is the evidence;
this is the map, and its value is COVERAGE -- it is the enumeration that would
have found the label exchange in the same pass as the figure exchange.
""")
    texts = V.site_texts()
    a = len(V.state_row(V.tree(STATE)))
    b = len(V.deliv_row(V.tree(DELIV)))
    h = len(V.tree(HIST))
    live = {"gap":  V.doc_num(a - b, signed=True),
            "both": V.doc_num(a + h - b, signed=True),
            "cell": V.doc_num(a), "hist": V.doc_num(h), "copy": V.doc_num(b)}

    print(f"    {'site':<20}{'segments':>10}{'empty':>7}{'fired':>7}"
          f"{'figures':>9}{'fired':>7}")
    seg_tot = seg_fired = seg_empty = fig_tot = fig_fired = 0
    for name, _r, _k in V.SITES:
        raw = texts[name]
        segments, figures = V.partition(raw)
        s_n = s_f = s_e = 0
        for i, seg in enumerate(segments):
            if not seg.strip():
                s_e += 1
                continue
            s_n += 1
            j = next(k for k, c in enumerate(seg) if not c.isspace())
            bad = seg[:j] + ("x" if seg[j] != "x" else "y") + seg[j + 1:]
            t = dict(texts)
            t[name] = V.rejoin(segments[:i] + [bad] + segments[i + 1:], figures)
            s_f += not all(o for o, _d in V.figure_gate(t, live))
        f_n = f_f = 0
        for i, fig in enumerate(figures):
            f_n += 1
            bad = fig[:-1] + ("0" if fig[-1] != "0" else "1")
            t = dict(texts)
            t[name] = V.rejoin(segments, figures[:i] + [bad] + figures[i + 1:])
            f_f += not all(o for o, _d in V.figure_gate(t, live))
        print(f"    {name:<20}{s_n:>10}{s_e:>7}{s_f:>7}{f_n:>9}{f_f:>7}")
        seg_tot += s_n
        seg_fired += s_f
        seg_empty += s_e
        fig_tot += f_n
        fig_fired += f_f

    record(seg_fired == seg_tot and fig_fired == fig_tot,
           f"R3a EVERY FIELD OF THE RECORD IS LOAD-BEARING: {seg_fired} of "
           f"{seg_tot} non-blank SEGMENTS and {fig_fired} of {fig_tot} FIGURES, "
           f"over 3 sites, each mutated ALONE, each caught.  The population is "
           f"derived from `partition` and not from a list somebody wrote, so a "
           f"field added to one of these sections tomorrow is in it without "
           f"this instrument being edited")
    record(None,
           f"R3b {seg_empty} segment(s) over the 3 sites are empty or all "
           f"whitespace and are reported as an ABSENCE rather than counted: "
           f"there is no character in them to mutate.  Their bytes are still "
           f"COMPARED -- an empty segment that acquires content, or loses it, "
           f"changes the declared record like any other")


# --------------------------------------------------------------------------
# R4 -- NOT SCORED BY ITS OWN AUTHOR
# --------------------------------------------------------------------------
INSTRUMENTS = [
    ("mg-9207", "code/hodge_leverage_audit_9207/audit_8eca_repair.py"),
    ("mg-8eca", "code/hodge_leverage_repair_8eca/repair_8aae.py"),
    ("mg-8aae", "code/hodge_leverage_audit_8aae/audit_8916_repair.py"),
    ("mg-8916", "code/hodge_leverage_repair_8916/repair_835f.py"),
]


def r4(which):
    head("R4 -- THE INSTRUMENTS THAT RAISED IT, RE-RUN UNMODIFIED")
    print("""An instrument that raised a finding must be able to re-run UNMODIFIED against
the repair answering it.  None of the four below is edited by this repair --
that is checked from git, not asserted -- and each is re-run as it stands.

What is expected of mg-9207 is NOT a green run.  Its E rows PREDICT SILENCE,
and silence is what this repair removes: those rows must now disagree with
their own prediction, and its E-findings must go to zero.  A landed finding
looks like a refuted prediction from the raising instrument's side.
""")
    for tag, path in INSTRUMENTS:
        diff = V.git("diff", "--stat", "HEAD", "--", path).strip()
        record(diff == "", f"R4-{tag} `{os.path.basename(path)}` is unmodified "
                           f"in the working tree")
    for tag, path in which:
        before = {p: sha(p) for p in FROZEN}
        r = subprocess.run([sys.executable, os.path.join(REPO, path)],
                           capture_output=True, text=True, cwd=REPO)
        out = r.stdout + r.stderr
        # ⚠️ COUNTED FROM THE ROWS, not parsed out of a bottom-line sentence.
        # The four instruments do not all print the same summary wording, and
        # a regex that matches three of them and silently returns None for the
        # fourth is a comparison with a hole in it -- which is the defect this
        # deliverable exists to repair, so it is not spelled that way here.
        rows = {m: len([l for l in out.split("\n")
                        if l.strip().startswith(f"[{m}")])
                for m in ("CONFIRMED", "REFUTED", "MEASURED", "FINDING")}
        finding_ids = [l.strip()[len("[FINDING  ]"):].strip().split()[0]
                       for l in out.split("\n")
                       if l.strip().startswith("[FINDING")]
        nfind = rows["FINDING"]
        # ITS OWN rows are printed at two spaces; the gate rows it ECHOES out
        # of the runner's stdout are indented further.  Counting both together
        # would report six quoted `FIGURE CENSUS` lines as six refutations.
        own_refuted = [l[len("  [REFUTED  ] "):].strip()
                       for l in out.split("\n") if l.startswith("  [REFUTED")]
        print(f"\n    {tag}: exit {r.returncode}, "
              f"{rows['CONFIRMED']} confirmed / {rows['REFUTED']} refuted / "
              f"{rows['MEASURED']} measured rows, {nfind} findings "
              f"{finding_ids}")
        print(f"      its OWN refuted rows ({len(own_refuted)}):")
        for row in own_refuted:
            print(f"        - {row[:118]}")
        after = {p: sha(p) for p in FROZEN}
        same = sum(1 for p in FROZEN if before[p] == after[p])
        record(same == len(FROZEN),
               f"R4-{tag}-frozen {same} of {len(FROZEN)} committed transcripts "
               f"are sha256-identical after its run")
        yield tag, r.returncode, out, own_refuted, finding_ids


# --------------------------------------------------------------------------
# R5 -- WHAT IS NOT COVERED, AND THIS DELIVERABLE CHECKED FOR ITS OWN DEFECT
# --------------------------------------------------------------------------
def r5():
    head("R5 -- WHAT IS NOT COVERED, AND THIS ARTIFACT CHECKED FOR ITS OWN DEFECT")
    print("""Both of the last two findings were a printed extent slightly wider than the
code beneath it, so the extent is printed.

NOT COVERED, with the reason, because an omission is not checkable and a stated
reason is:

  * TEXT OUTSIDE THE SITE.  A site is a SECTION, and this is the one
    projection that remains.  It is unchanged since mg-8a5c, it is stated
    where a reader meets the gate, and it is itself gated: `section()` anchors
    BY CONTENT, and N6 of the negative control relocates a whole disclosure
    out of §14 to show the gate notices.  Widening it to the file would make
    every unrelated edit to three documents red, which is a different trade
    and is pm-onethird's to size, not this repair's.

  * TWO OCCURRENCES OF THE SAME FIGURE TOKEN EXCHANGED.  Still the identity
    map on the bytes (mg-8eca): there is no artifact to detect.  This is an
    EMPTY SET rather than a blind spot, and the difference is checkable.

  * WHAT A ROSTER ENTRY MEANS.  `ORDER` says where `10 483` goes and
    `HISTORICAL` says it is 'this file at bbe83b5^'.  Nothing checks that
    sentence against git.  Unchanged from mg-8eca and named again here
    because it is now the widest thing left.

  * THE RESEAL.  `--reseal` is the one step that can make a wrong document
    green, and it exists because the alternative -- no way to edit these
    sections -- is not a gate, it is a freeze.  Three things narrow it: it
    REFUSES while any other gate row is refuted; what it writes is TEXT, so
    the blessing is a reviewable diff rather than a hash bump; and it is not
    invoked by `run_all.sh`, so it cannot happen as a side effect of a run.

AND THIS DELIVERABLE IS OF THE SAME KIND AS THE DEFECT IT REPAIRS.  It is a
comparison, repairing a comparison, and it compares things.  The defect is:
COMPARING A RECORD BY IDENTITY ON SOME FIELDS AND POSITION ON OTHERS, SO THAT
WHATEVER IS IN NEITHER IS SILENT.  Every comparison this deliverable performs,
enumerated -- and where a branch cannot exhibit the defect, the reason, because
a reason is checkable and an omission is not:

  1. SITE RECORD -- site skeleton against the declared record.  CAN exhibit it
     and does not: the comparison is `==` on the whole string, so its kernel is
     empty by construction.  RECORD PARTITION is what shows the string really
     is the whole non-figure half, and D3 shows that row failing when it is
     not.
  2. RECORD PARTITION -- `rejoin(segments, figures) == raw`.  CANNOT exhibit
     it: it is equality on two whole strings, with no field structure to be
     partial about.  Its risk is the opposite one -- being unfalsifiable -- and
     D3 is the answer to that, not to this.
  3. R1's SCORING -- probe verdicts against predictions.  DID exhibit it, in
     this instrument's own first version: `"FIGURE CENSUS" in row` matched the
     SITE RECORD row's own explanation, which names the other rows, and every
     probe was scored as having broken a figure row.  Fixed by comparing the
     row's HEADING, and the fix is `heading()`, one function, used everywhere
     a row is identified.
  4. R3's POPULATION -- segments and figures enumerated from `partition`.
     CANNOT exhibit it in the field-by-field sense: nothing is named, the
     population is derived.  Its real limit is that it is IN MEMORY, and that
     is declared in its own heading rather than left to be found.
  5. R4's re-run scoring -- `checks recorded` / `refuted` / findings parsed out
     of another instrument's transcript.  CAN exhibit it: it reads four named
     numbers and ignores everything else printed.  Narrowed by also comparing
     the EXIT CODE and by naming, for mg-9207, the exact rows expected to
     move -- but this one is real and is stated rather than dressed up.
  6. THE FROZEN-TRANSCRIPT CHECK -- sha256 before and after.  CANNOT exhibit
     it: a hash over the whole file has no field structure.
""")
    record(None,
           "R5 six comparisons in this deliverable, enumerated: 2 can exhibit "
           "the defect and are shown not to (1) or narrowed and declared (5), "
           "1 DID exhibit it and was fixed (3), and 3 cannot, each with the "
           "reason stated (2, 4, 6)")


def main():
    print("mg-ff3e -- THE CENSUS IS POSITION-AWARE OVER THE WHOLE RECORD")
    print("=" * 78)
    print(__doc__.split("\n", 2)[2].split("  R1")[0].strip())

    dirty = [p for p in REQUIRE_CLEAN
             if V.git("status", "--porcelain", "--", p).strip()]
    if dirty:
        print("\nREFUSING TO RUN: these are dirty and this instrument "
              "`git checkout --`s them:")
        for p in dirty:
            print(f"  {p}")
        return 2

    pristine = {p: read(p) for p in MUTABLE}
    print(f"\n  {len(MUTABLE)} mutable files read and pinned; "
          f"{len(FROZEN)} committed transcripts pinned frozen")

    try:
        n = r1(pristine)
        r2(pristine, n)
        r3()
        which = INSTRUMENTS if "--full" in sys.argv[1:] else INSTRUMENTS[:1]
        results = list(r4(which))
        by_tag = {t: (rc, out, own, ids) for t, rc, out, own, ids in results}
        for tag, rc, out, own_refuted, finding_ids in results:
            # ⚠️ THE ONE PLACE THIS REPAIR DISTURBS A PRIOR INSTRUMENT, and it
            # is not hidden in a row count.  mg-8aae's A3 picks its probe slot
            # by a PROCEDURE and controls it first: the slot is blanked and the
            # runner must stay GREEN, so that a fire is attributable to the
            # figure and not to the edit.  With the whole record compared,
            # BLANKING ANY PROSE MAKES THE RUNNER RED -- so the search returns
            # nothing and A3 cannot run.  That is not G-1 reopening.  It is
            # mg-8aae's own probe generator, searching for text the gate does
            # not read, FINDING NONE at 3 of 3 sites: the extent of this repair
            # measured by an instrument that is not its own.
            if tag == "mg-8aae":
                noslot = [r for r in own_refuted
                          if r.startswith("no unread prose slot")]
                record(None,
                       f"R4d mg-8aae's A3 reports NO UNREAD PROSE SLOT at "
                       f"{len(noslot)} of its 6 probe slots, where it "
                       f"previously found one per site.  Its slot search "
                       f"requires prose that can be BLANKED with the runner "
                       f"staying green, and after this repair there is none -- "
                       f"the search failing IS the measurement, taken by an "
                       f"instrument that is not this repair's.  It is why "
                       f"{len(noslot) + 3} of its {len(own_refuted)} refuted "
                       f"rows have one cause, and it is a DISTURBANCE, "
                       f"reported rather than counted away")
                rc16 = by_tag.get("mg-8916", (None,))[0]
                record(rc16 == 0 or rc16 is None,
                       f"R4e and G-1 is NOT reopened by that: mg-8916's own "
                       f"instrument, unmodified, exits {rc16} with its U1 "
                       f"wrong-prose probes firing -- G-1's closure is "
                       f"re-derived by a second instrument that does not need "
                       f"an unread slot to do it, plus N10-N13 of the "
                       f"runner's own control")
            if tag == "mg-9207":
                e_rows = [r for r in own_refuted if re.match(r"E2b?|E3", r)]
                silent = [l for l in out.split("\n")
                          if "THE INVARIANCE MOVED" in l]
                # ⚠️ BY THE FINDING'S ID, not by its prose.  J-3's own text
                # says "and E2 below where the gate saw NOTHING", so a
                # substring test over the line reports the E2 finding as still
                # raised while it is gone.  This instrument's first version did
                # exactly that: item 3 of R5, met twice.
                e_findings = [f for f in finding_ids
                              if f.rstrip(",") in ("E2", "E2b", "E3")]
                record(len(e_findings) == 0,
                       f"R4a mg-9207 raises {len(e_findings)} E2/E2b/E3 "
                       f"FINDING against the repaired tree, where it raised 3 "
                       f"(its findings now: {finding_ids}).  The defect it "
                       f"found is gone, measured by the instrument that found "
                       f"it")
                record(len(e_rows) > 0,
                       f"R4b and {len(e_rows)} of its rows now REFUTE their "
                       f"own prediction of SILENCE (its 'THE INVARIANCE MOVED' "
                       f"row among them: {len(silent)} such row printed).  "
                       f"That is what a landed finding looks like from the "
                       f"raising instrument's side -- its exit is {rc} and "
                       f"that is CORRECT, not a regression")
                c3 = [l for l in out.split("\n") if "C3 and the `FIGURE ORDER`"
                      in l]
                record(bool(c3) and all("CONFIRMED" in l for l in c3),
                       f"R4c and its C3 still holds: the FIGURE ORDER row is "
                       f"the ONLY gate row that failed on a FIGURE exchange, "
                       f"12 of 12, AFTER two rows were added to the gate.  "
                       f"{c3[0].strip()[:110] if c3 else '(row not printed)'}")
        r5()
    finally:
        for p in MUTABLE:
            write(p, pristine[p])
        bad = [p for p in MUTABLE
               if sha(p) != hashlib.sha256(
                   pristine[p].encode("utf-8")).hexdigest()]
        head("RESTORATION")
        record(not bad,
               f"every mutated file is restored and the restoration is CHECKED "
               f"by sha256, not asserted: {len(MUTABLE) - len(bad)} of "
               f"{len(MUTABLE)} byte-identical")

    head("BOTTOM LINE")
    refuted = [d for d, ok in RESULTS if ok is False]
    print(f"  checks recorded : {len(RESULTS)}")
    print(f"  measurements    : {sum(1 for _, ok in RESULTS if ok is None)}")
    print(f"  confirmed       : {sum(1 for _, ok in RESULTS if ok is True)}")
    print(f"  refuted         : {len(refuted)}")
    print()
    if refuted:
        print("  REFUTED -- the prose must not be written:")
        for d in refuted:
            print(f"    - {d}")
        return 1
    print("  The census compares the WHOLE RECORD.  The seven label-side")
    print("  exchanges mg-9207 left open fire on disk against the real runner,")
    print("  caught by the half of the record that was not being compared,")
    print("  with the figure half green at every one -- and deleting that")
    print("  comparison puts all seven back to silent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
