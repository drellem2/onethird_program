#!/usr/bin/env python3
"""mg-9876 — step 3 of the ticket: DEMONSTRATE DISCRIMINATION, DO NOT ASSERT IT.

THE RULE, AND IT IS TWO-SIDED ON PURPOSE.  Every arm is run twice: once against an input in
which its subject HOLDS, and once against an input in which its subject has STOPPED HOLDING.
The arm's own report is read both times through one predicate, and the arm is scored:

    DISCRIMINATES   predicate FALSE on the good input, TRUE on the bad one.
    LAUNDERED       predicate FALSE on both — the arm reports the same thing when the property
                    it is named for has stopped.  This is the ticket's definition.
    UNFALSIFIABLE   predicate TRUE on the GOOD input.  This is NOT a finding against the arm;
                    it is a finding against THIS INSTRUMENT, and it is the mg-2f44 defect
                    exactly — `"8 9" in out` was true on the good input, so it could not fail.
                    Scored red, never silently accepted.
    SETUP FAILED    the bad input was not actually bad (a rotted fixture), or the probe threw.

THE ONE-SIDED VERSION OF THIS TEST IS WHAT PRODUCED ALL THREE LAUNDERED GREENS IN THE TARGET
DIRECTORY.  `negative_control.py` asks only "does the expected string appear after the
mutation?".  That question cannot distinguish a string the mutation caused from a string the
report prints unconditionally, which is how section 1's `all three row sets agree: 1 2 3a 3b
4 5 6 7 8 9 10 11` satisfied a positive control about the drift worklist for its whole life.
Running the predicate against the UNMUTATED report is the entire repair, generalised.

PREDICATES ARE SCOPED TO A PARSED REGION, NOT TO THE WHOLE REPORT.  `sect(text, 2)` returns
section 2 and nothing else.  A membership test against a whole transcript is smell #1 in the
ticket and it is not used here even where it would be convenient.

PART B — AUXILIARY PROBES.  A separate register, because an arm can DISCRIMINATE and still be
blind to a specific bad input its name promises to catch.  Those are holes, not laundering,
and conflating them would flatter both.  Each is a demonstrated failure with a transcript,
never a suspicion.
"""

import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import contextlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib9876 as L  # noqa: E402

sys.path.insert(0, L.TARGET)
import lib9bc2 as B  # noqa: E402

TWIN_REL = os.path.join("docs", "state-of-the-wall.html")
DIR_REL = os.path.join("code", L.TARGET_DIRNAME)


# ======================================================================================
# helpers
# ======================================================================================

def sect(text, n):
    """Return SECTION `n` of a twin_pin report and NOTHING else.

    Predicates read this, not the transcript.  The whole point of the exercise.

    THE `$` FALLBACK IS NOT COSMETIC.  The first version required a following `SECTION` or a
    rule line, and section 1's structural FAIL RETURNS IMMEDIATELY — nothing follows it.  So
    the extractor returned the empty string, every predicate over it was False, and arm C1a
    scored LAUNDERED on a report that named the defect in full.  That is a laundered green
    produced by the auditor, on its first run, in the file written to find laundered greens.
    It was caught because the rule is two-sided and the failure was visible on the BAD side.
    """
    m = re.search(r"^SECTION %s\b.*?(?=^SECTION \d|^={20,}$|\Z)" % re.escape(str(n)),
                  text, re.M | re.S)
    return m.group(0) if m else ""


def has(needle):
    return lambda rc, text: needle in text


def in_sect(n, needle):
    return lambda rc, text: needle in sect(text, n)


def rx_sect(n, pattern):
    p = re.compile(pattern, re.M)
    return lambda rc, text: bool(p.search(sect(text, n)))


class Probe:
    """One arm's two-sided demonstration.

    `good` and `bad` are zero-argument callables returning (rc, text).  They are called in
    that order so that a probe which mutates a sandbox cannot leak the mutation into the
    good side.
    """

    def __init__(self, arm_id, good, bad, red, bad_desc):
        self.arm_id = arm_id
        self.good = good
        self.bad = bad
        self.red = red
        self.bad_desc = bad_desc


PROBES = []


def probe(arm_id, bad_desc):
    def deco(fn):
        PROBES.append((arm_id, bad_desc, fn))
        return fn
    return deco


# ======================================================================================
# PART A — one probe per arm
# ======================================================================================
#
# Each `fn(box)` receives a fresh sandbox root and returns (good_thunk, bad_thunk, red).

def _pair(box):
    return os.path.join(box, "STATE.md"), os.path.join(box, TWIN_REL)


def _ctl(box):
    return os.path.join(box, DIR_REL)


# ------------------------------------------------------------------ twin_pin sections

@probe("C1a", "the twin carries no STATE-PIN block")
def p_c1a(box):
    sp, tp = _pair(box)
    good = lambda: L.run_control(sp, tp, _ctl(box))                        # noqa: E731

    def bad():
        t = L.read(tp)
        i, j = t.find(B.PIN_START), t.find(B.PIN_END) + len(B.PIN_END)
        L.write(tp, t[:i] + t[j:])
        return L.run_control(sp, tp, _ctl(box))
    return good, bad, in_sect(1, "FAIL  no STATE-PIN block in the twin")


@probe("C1b", "a ledger row exists in STATE.md but not in the twin")
def p_c1b(box):
    sp, tp = _pair(box)
    good = lambda: L.run_control(sp, tp, _ctl(box))                        # noqa: E731

    def bad():
        t = L.read(tp)
        L.write(tp, re.sub(r'<tr><td class="rowlabel">7</td>.*?</tr>', "", t, count=1,
                           flags=re.S))
        return L.run_control(sp, tp, _ctl(box))
    return good, bad, in_sect(1, "FAIL  the row sets disagree")


@probe("C1c", "the ledger grows a sixth column, outside every pinned digest")
def p_c1c(box):
    sp, tp = _pair(box)
    good = lambda: L.run_control(sp, tp, _ctl(box))                        # noqa: E731

    def bad():
        s = L.read(sp)
        out = s.replace("| # | Result | Kind | Status | Width |",
                        "| # | Result | Kind | Status | Width | Owner |", 1)
        for _lbl, _cells, raw in B.parse_state_ledger(s):
            out = out.replace(raw + "\n", raw + " pm-onethird |\n", 1)
        L.write(sp, out)
        return L.run_control(sp, tp, _ctl(box))
    return good, bad, in_sect(1, "the ledger's column set has changed since the pin")


@probe("C3a", "the pin's `state-sha256` field is deleted outright")
def p_c3a(box):
    sp, tp = _pair(box)
    good = lambda: L.run_control(sp, tp, _ctl(box))                        # noqa: E731

    def bad():
        L.write(tp, re.sub(r"\n\s*state-sha256: [0-9a-f]+", "", L.read(tp), count=1))
        return L.run_control(sp, tp, _ctl(box))
    return good, bad, in_sect(3, "the pin carries no well-formed `state-sha256` field")


@probe("C6c", "the pin's `commit:` field is deleted outright")
def p_c6c(box):
    sp, tp = _pair(box)
    good = lambda: L.run_control(sp, tp, _ctl(box))                        # noqa: E731

    def bad():
        L.write(tp, re.sub(r"\n\s*commit: [0-9a-f]+", "", L.read(tp), count=1))
        return L.run_control(sp, tp, _ctl(box))
    return good, bad, in_sect(6, "the pin carries no `commit:` field")


@probe("C2", "an UNDRIFTED STATE.md ledger row is edited under the pin")
def p_c2(box):
    """THE GOOD SIDE HAS TO BE MADE GOOD FIRST, and the first version of this probe did not.

    Row 8 of the live tree has been drifted since mg-9bc2 seeded the pin, so `^  row \\S+
    MOVED` was already TRUE on the unmutated input and the probe scored UNFALSIFIABLE — it
    could not have failed, which is the `"8 9" in out` defect with my name on it.  The good
    side now re-pins every row in the sandbox so that NO row has moved, and only then is one
    row edited.  The predicate is now false on one side and true on the other by construction.
    """
    sp, tp = _pair(box)
    t = L.read(tp)
    for lbl, dg in B.row_digests(L.read(sp)).items():
        t = re.sub(r"(\n  row %s\s+)[0-9a-f]{16}" % re.escape(lbl),
                   lambda m, d=dg: m.group(1) + d, t, count=1)
    L.write(tp, t)
    good = lambda: L.run_control(sp, tp, _ctl(box))                        # noqa: E731

    def bad():
        s = L.read(sp)
        rows = B.parse_state_ledger(s)
        pin = B.parse_pin(L.read(tp))
        now = B.row_digests(s)
        target = next(r for r in rows if pin["rows"].get(r[0]) == now[r[0]])
        # INSIDE a cell, not after the final pipe.  The first version appended past the last
        # `|`, which `split_md_cells` turns into a SIXTH cell that `row_digests` never reads
        # — so the digest did not move and C2 scored LAUNDERED off an inert mutation.  That
        # blindness is real and is filed as an auxiliary probe below; it is not C2 failing.
        cells = B.split_md_cells(target[2])
        cells[4] = cells[4] + " ⟪mg-9876 probe⟫"
        L.write(sp, s.replace(target[2], "| " + " | ".join(cells) + " |", 1))
        return L.run_control(sp, tp, _ctl(box))
    return good, bad, rx_sect(2, r"^  row \S+\s+MOVED")


@probe("C3", "STATE.md is no longer byte-identical to the pinned revision")
def p_c3(box):
    """THE GOOD SIDE HAS TO BE MADE GOOD FIRST — C2's own rule, not applied here until mg-188d.

    C2's docstring two hundred lines above states the rule and C2 obeys it; C3 was left with a
    raw sandbox, and section 3 says `DIFFERS` whenever STATE.md has moved at all — which
    COVERAGE.md itself calls the NORMAL condition, `DIFFERS on nearly every run and that is not
    a defect`.  So the predicate was already true on the good input and C3 scored
    UNFALSIFIABLE.  mg-9876 published that as a standing finding and mg-724a GATED it at
    `audit.arms_not_shown = 1` so its repair would be deliberate.  This is that repair.

    IT IS ALSO WHY THE FIELD COULD NOT SIMPLY BE RE-BASELINED AT 0.  mg-188d's reconciliation
    made STATE.md byte-identical to the pin, which made C3 discriminate BY ACCIDENT — and the
    next STATE.md edit by anybody would have taken it back to UNFALSIFIABLE and turned the
    merge gate red for an author who could not act on it.  A gated value has to be an
    EXPECTATION, not a dated reading about whether the corpus happens to be still (mg-724a's
    own recorded/gated split).  Re-pointing the sandbox's `state-sha256` at the sandbox's OWN
    STATE.md makes the good side good on every tree, so 0 is stable and means what it says.
    The digest is COMPUTED from the bytes under test, never typed.
    """
    sp, tp = _pair(box)
    with open(sp, "rb") as fh:
        actual = hashlib.sha256(fh.read()).hexdigest()
    t, n = re.subn(r"(\n  state-sha256:\s*)[0-9a-f]{64}",
                   lambda m: m.group(1) + actual, L.read(tp), count=1)
    if n != 1:
        raise AssertionError("expected exactly one `state-sha256` field in the pin, found %d" % n)
    L.write(tp, t)
    good = lambda: L.run_control(sp, tp, _ctl(box))                        # noqa: E731

    def bad():
        L.write(sp, L.read(sp) + "\n<!-- mg-9876 probe: one appended byte -->\n")
        return L.run_control(sp, tp, _ctl(box))
    return good, bad, in_sect(3, "DIFFERS  STATE.md has changed since the pin")


@probe("C4", "the twin's Kind mark for a row disagrees with STATE.md's")
def p_c4(box):
    sp, tp = _pair(box)
    good = lambda: L.run_control(sp, tp, _ctl(box))                        # noqa: E731

    def bad():
        t = L.read(tp)
        L.write(tp, t.replace('<span class="kind fp">&#9888;&#65039; FP</span>',
                              '<span class="kind u">U</span>', 1))
        return L.run_control(sp, tp, _ctl(box))
    return good, bad, rx_sect(4, r"^  row \S+\s+MISMATCH")


@probe("C5a", "the twin claims `Generated <date>` again")
def p_c5a(box):
    sp, tp = _pair(box)
    good = lambda: L.run_control(sp, tp, _ctl(box))                        # noqa: E731

    def bad():
        t = L.read(tp)
        L.write(tp, t.replace("<span><b>Maintained by</b> pm-onethird</span>",
                              "<span><b>Maintained by</b> pm-onethird</span>\n"
                              "      <span><b>Generated</b> 2026-08-10</span>", 1))
        return L.run_control(sp, tp, _ctl(box))
    return good, bad, rx_sect(5, r"matches /\\bGenerated")


@probe("C5b", "the twin calls itself the source of truth")
def p_c5b(box):
    sp, tp = _pair(box)
    good = lambda: L.run_control(sp, tp, _ctl(box))                        # noqa: E731

    def bad():
        t = L.read(tp)
        L.write(tp, t.replace("<footer>",
                              "<footer>\n    <p>This is the source of truth for the "
                              "program.</p>", 1))
        return L.run_control(sp, tp, _ctl(box))
    return good, bad, in_sect(5, "a canonicity claim on a line that does not name STATE.md")


@probe("C6a", "the visible provenance line is deleted")
def p_c6a(box):
    sp, tp = _pair(box)
    good = lambda: L.run_control(sp, tp, _ctl(box))                        # noqa: E731

    def bad():
        t = L.read(tp)
        L.write(tp, re.sub(r'<span id="provenance">.*?</span>\s*$', "", t, count=1,
                           flags=re.M | re.S))
        return L.run_control(sp, tp, _ctl(box))
    return good, bad, in_sect(6, 'FAIL  no <span id="provenance">')


@probe("C6b", "the visible provenance line names a different commit than the pin")
def p_c6b(box):
    sp, tp = _pair(box)
    good = lambda: L.run_control(sp, tp, _ctl(box))                        # noqa: E731

    def bad():
        t = L.read(tp)
        L.write(tp, re.sub(r'(<span id="provenance">.*?@ )([0-9a-f]{7,40})',
                           r"\g<1>deadbeefcafe", t, count=1, flags=re.S))
        return L.run_control(sp, tp, _ctl(box))
    return good, bad, in_sect(6, "does not name exactly the pinned commit")


# ------------------------------------------------------------------ reconcile refusals

def _reconcile(box, *args):
    """Run `--reconcile` in the sandbox, restoring the pair FIRST.

    THE GOOD SIDE OF A RECONCILE PROBE MUTATES THE SANDBOX — that is what reconciling is —
    and the first version let it.  So `good()` re-pinned the drifted row, and `bad()` then
    met a tree with nothing left to reconcile and was refused for the WRONG reason: R4 scored
    LAUNDERED while its refusal was firing perfectly one message away.  Both sides now start
    from the same bytes, snapshotted before either runs.
    """
    _restore(box)
    for extra in _PENDING.pop(box, []):
        extra()
    proc = subprocess.run([sys.executable, os.path.join(_ctl(box), "twin_pin.py"),
                           "--reconcile"] + list(args), capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


_SNAP = {}
_PENDING = {}


def _snapshot(box):
    sp, tp = _pair(box)
    _SNAP[box] = (L.read(sp), L.read(tp))


def _restore(box):
    sp, tp = _pair(box)
    s, t = _SNAP[box]
    L.write(sp, s)
    L.write(tp, t)


def _moved_row(box):
    """A ledger row whose STATE.md digest differs from the pin — PLANTED if none does.

    THIS IS THE THIRD TIME A FIXTURE IN THIS LINEAGE BORROWED THE SUBJECT'S OWN BROKENNESS,
    AND THE FIRST TIME THE REPAIR ARRIVED (mg-188d).  R1-R4 all need a row to reconcile, and
    this helper used to hand them whatever row happened to be drifted in the live tree,
    returning None when none was.  Row 8 had been drifted since mg-9bc2 seeded the pin, so
    None was unreachable and nothing said so.  mg-188d reconciled row 8, the tree went CLEAN
    for the first time, and all four arms came back `SETUP FAILED  TypeError: expected str,
    bytes or os.PathLike object, not NoneType` — four arms of this instrument destroyed by
    the subject being FIXED.  That is `C2`'s own docstring two hundred lines above ("the good
    side has to be MADE good first"), and it is this file's own recorded defect — "two planted
    worlds in my own selftest were borrowed from the subject under audit, so my repairs
    destroyed them" — arriving a third time, in the arms that were not looked at when the
    first two were.

    So the drifted row is now CONSTRUCTED when it is absent, and the construction is DERIVED
    FROM THE CAPTURED BYTES rather than typed: one row's pinned digest is overwritten with
    ANOTHER ROW'S pinned digest, both read out of the pin.  Nothing here spells out a row
    label or a digest, so this cannot rot at the next reconciliation the way the thing it
    replaces did.  The plant is re-snapshotted, because `_reconcile` restores the pair before
    every side and would otherwise undo it.
    """
    sp, tp = _pair(box)
    pin = B.parse_pin(L.read(tp))
    now = B.row_digests(L.read(sp))
    label = next((l for l in now if pin["rows"].get(l) != now[l]), None)
    if label is not None:
        return label

    labels = sorted(now)
    label = labels[0]
    donor = next((l for l in labels[1:] if pin["rows"][l] != pin["rows"][label]), None)
    if donor is None:
        raise AssertionError(
            "cannot plant a drifted row: every pinned digest is identical, so no digest "
            "read out of this pin differs from any other.  Refusing to type one in.")
    L.write(tp, re.sub(r"(\n  row %s\s+)[0-9a-f]{16}" % re.escape(label),
                       lambda m: m.group(1) + pin["rows"][donor], L.read(tp), count=1))
    if B.parse_pin(L.read(tp))["rows"][label] == now[label]:
        raise AssertionError("the planted drift did not take: row %s still matches" % label)
    _snapshot(box)
    return label


@probe("R1", "a re-pin is requested without naming any row")
def p_r1(box):
    _snapshot(box)
    row = _moved_row(box)
    good = lambda: _reconcile(box, "--rows", row)                          # noqa: E731
    bad = lambda: _reconcile(box)                                          # noqa: E731
    return good, bad, has("--reconcile requires --rows")


@probe("R2", "a re-pin names a ledger row that does not exist")
def p_r2(box):
    _snapshot(box)
    row = _moved_row(box)
    good = lambda: _reconcile(box, "--rows", row)                          # noqa: E731
    bad = lambda: _reconcile(box, "--rows", "99z")                         # noqa: E731
    return good, bad, has("REFUSED: no such ledger row(s)")


@probe("R3", "a re-pin names a row that has NOT moved — a reconciliation that did not happen")
def p_r3(box):
    _snapshot(box)
    sp, tp = _pair(box)
    # THE ORDER IS LOAD-BEARING: `_moved_row` may PLANT the drift (see its docstring), and a
    # row read as `unmoved` beforehand can be the very row it plants on.  The pin is therefore
    # re-read AFTERWARDS, so `unmoved` is unmoved in the tree the two sides actually run in.
    moved = _moved_row(box)
    pin = B.parse_pin(L.read(tp))
    now = B.row_digests(L.read(sp))
    unmoved = next(l for l in now if pin["rows"].get(l) == now[l])
    good = lambda: _reconcile(box, "--rows", moved)                        # noqa: E731
    bad = lambda: _reconcile(box, "--rows", unmoved)                       # noqa: E731
    return good, bad, has("have not moved since the pin")


@probe("R4", "the twin carries two visible provenance lines, so a re-pin would half-update")
def p_r4(box):
    _snapshot(box)
    sp, tp = _pair(box)
    row = _moved_row(box)
    good = lambda: _reconcile(box, "--rows", row)                          # noqa: E731

    def duplicate_span():
        t = L.read(tp)
        m = re.search(r'<span id="provenance">.*?</span>\s*$', t, re.M | re.S)
        L.write(tp, t[:m.end()] + "\n" + m.group(0) + t[m.end():])

    def bad():
        _PENDING[box] = [duplicate_span]
        return _reconcile(box, "--rows", row)
    return good, bad, has('REFUSED: expected exactly one <span id="provenance">')


# ------------------------------------------------------------------ lib9bc2 parser raises

def _call(fn, *args):
    try:
        fn(*args)
        return 0, "(no exception)"
    except Exception as exc:                                              # noqa: BLE001
        return 1, f"{type(exc).__name__}: {exc}"


@probe("L1", "STATE.md no longer contains the ledger header this instrument reads")
def p_l1(box):
    sp, _tp = _pair(box)
    s = L.read(sp)
    good = lambda: _call(B.parse_state_ledger, s)                          # noqa: E731
    bad = lambda: _call(B.parse_state_ledger,                              # noqa: E731
                        s.replace("| # | Result | Kind | Status | Width |",
                                  "| # | RESULT | Kind | Status | Width |", 1))
    return good, bad, has("no ledger header")


@probe("L2", "a ledger row loses a column")
def p_l2(box):
    sp, _tp = _pair(box)
    s = L.read(sp)
    rows = B.parse_state_ledger(s)
    raw = rows[0][2]
    short = "| " + " | ".join(B.split_md_cells(raw)[:3]) + " |"
    good = lambda: _call(B.parse_state_ledger, s)                          # noqa: E731
    bad = lambda: _call(B.parse_state_ledger, s.replace(raw, short, 1))    # noqa: E731
    return good, bad, has("expected 5")


@probe("L3", "the ledger header survives but every row under it is gone")
def p_l3(box):
    sp, _tp = _pair(box)
    s = L.read(sp)
    rows = B.parse_state_ledger(s)
    stripped = s
    for _lbl, _cells, raw in rows:
        stripped = stripped.replace(raw + "\n", "", 1)
    good = lambda: _call(B.parse_state_ledger, s)                          # noqa: E731
    bad = lambda: _call(B.parse_state_ledger, stripped)                    # noqa: E731
    return good, bad, has("no rows under it")


@probe("L4", "the twin renders no ledger rows at all")
def p_l4(box):
    _sp, tp = _pair(box)
    t = L.read(tp)
    good = lambda: _call(B.parse_twin_ledger, t)                           # noqa: E731
    bad = lambda: _call(B.parse_twin_ledger,                               # noqa: E731
                        re.sub(r'<td class="rowlabel">[0-9]+[a-z]?</td>', "", t))
    return good, bad, has("no ledger rows found in the twin")


@probe("L5", "a pin block starts and never ends")
def p_l5(box):
    _sp, tp = _pair(box)
    t = L.read(tp)
    good = lambda: _call(B.parse_pin, t)                                   # noqa: E731
    bad = lambda: _call(B.parse_pin, t.replace(B.PIN_END, "", 1))          # noqa: E731
    return good, bad, has("present with no")


# ------------------------------------------------------------------ seed_pin refusals

def _seed(box, pin_commit=None, twin_name="twin_pinless.html"):
    """Run seed_pin.main() in-process with its TWIN repointed into the sandbox.

    IT IS IMPORTED FROM THE REAL DIRECTORY, NOT THE SANDBOX COPY, AND THAT IS A REPAIR.  The
    first version imported the sandbox copy — whereupon `seed_pin`'s `from twin_pin import
    ROOT` bound ROOT to the SANDBOX, which is not a git repository, so `git show 276aead:...`
    failed on BOTH sides and S1 scored UNFALSIFIABLE while S2 and S3 scored LAUNDERED.  Three
    arms condemned by a defect in the probe.  seed_pin's whole job is to read history, so ROOT
    must be the real repository; only TWIN is repointed, because seed_pin WRITES it and an
    audit that writes docs/state-of-the-wall.html would be doing the thing it audits.
    """
    for mod in ("seed_pin", "twin_pin", "lib9bc2"):
        sys.modules.pop(mod, None)
    import seed_pin as SP                                                  # noqa: N814
    tp = os.path.join(box, twin_name)
    L.assert_sandboxed(tp)
    SP.TWIN = tp
    if pin_commit is not None:
        SP.PIN_COMMIT = pin_commit
    buf = io.StringIO()
    rc = 0
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            rc = SP.main()
    except SystemExit as exc:
        rc = 1
        buf.write(str(exc.code) if isinstance(exc.code, str) else "")
    finally:
        for mod in ("seed_pin", "twin_pin", "lib9bc2"):
            sys.modules.pop(mod, None)
    return rc, buf.getvalue()


def _make_pinless(box):
    _sp, tp = _pair(box)
    t = L.read(tp)
    i, j = t.find(B.PIN_START), t.find(B.PIN_END) + len(B.PIN_END)
    out = os.path.join(box, "twin_pinless.html")
    L.write(out, t[:i] + t[j:])
    return out


@probe("S1", "the commit the pin is seeded at is not reachable in this repository")
def p_s1(box):
    _make_pinless(box)
    good = lambda: _seed(box)                                              # noqa: E731
    bad = lambda: _seed(box, pin_commit="0000000badc0ffee")                # noqa: E731
    return good, bad, has("cannot read STATE.md at")


@probe("S2", "the seed commit is a ONE-SIDED edit, not a reconciliation of both files")
def p_s2(box):
    _make_pinless(box)
    one_sided = subprocess.run(
        ["git", "-C", L.ROOT, "log", "-1", "--format=%h", "--", "docs/roadmap.md"],
        capture_output=True, text=True).stdout.strip()
    good = lambda: _seed(box)                                              # noqa: E731
    bad = lambda: _seed(box, pin_commit=one_sided)                         # noqa: E731
    return good, bad, has("does not touch")


@probe("S3", "the twin already carries a reconciled pin and a re-seed would erase it")
def p_s3(box):
    _make_pinless(box)
    shutil.copy2(os.path.join(box, TWIN_REL), os.path.join(box, "twin_pinned.html"))
    good = lambda: _seed(box)                                              # noqa: E731
    bad = lambda: _seed(box, twin_name="twin_pinned.html")                 # noqa: E731
    return good, bad, has("REFUSED: the twin already carries a pin")


# ------------------------------------------------------------------ negative_control arms
#
# THE PROBE FOR N1..N10 IS THE GENERALISATION OF mg-2f44's REPAIR.  Each of those arms scores
# `expect in out` after a mutation.  The question the harness never asks is whether `expect`
# was already in the report BEFORE the mutation — and for the positive control it was, for
# the arm's whole life.  So: good side = the UNMUTATED report, bad side = the mutated one.
# An arm whose expect string is present unmutated scores UNFALSIFIABLE, which is red.

import negative_control as NC  # noqa: E402

_NC_BY_ARM = {
    "N1": "pin block deleted entirely",
    "N2": "a ledger row deleted from the twin only",
    "N3": "one character changed in an UNDRIFTED STATE.md ledger row (row 1)",
    "N4": "a whole STATE.md ledger cell emptied (row 10 status)",
    "N5": "twin's KIND mark for row 10 flipped FP -> U",
    "N6": "STATE.md's KIND mark for row 9 flipped FP✗ -> U",
    "N7": "`Generated <date>` re-introduced into the header",
    "N8": "the twin re-claims canonicity in the footer",
    "N9": "visible provenance line points at a DIFFERENT commit than the pin",
    "N10": "visible provenance line removed (pin becomes machine-only)",
    "N14": "the ledger GAINS A COLUMN (header and every row)",
    "N15": "the pin's `state-sha256` field is deleted outright",
    "N16": "the pin's `columns` field is deleted outright",
    "N17": "`Generated <date>` re-introduced BEHIND an HTML comment opener",
    "N18": "visible provenance names the pinned commit AND a second one",
}


def _nc_probe(arm_id):
    mut_name = _NC_BY_ARM[arm_id]

    def build(box):
        sp, tp = _pair(box)
        name, section, expect, target, fn = next(m for m in NC.MUTATIONS if m[0] == mut_name)
        base_s, base_t = L.read(sp), L.read(tp)

        def good():
            return L.run_control(sp, tp, _ctl(box))

        def bad():
            s = fn(base_s) if target == "state" else base_s
            t = fn(base_t) if target == "twin" else base_t
            if (s, t) == (base_s, base_t):
                raise RuntimeError("mutation was a no-op — the fixture has rotted")
            L.write(sp, s)
            L.write(tp, t)
            return L.run_control(sp, tp, _ctl(box))

        return good, bad, has(expect)
    return build


for _aid in _NC_BY_ARM:
    PROBES.append((_aid, f"the mutation `{_NC_BY_ARM[_aid]}` is applied", _nc_probe(_aid)))


@probe("N11", "the drift worklist is NOT the one derived from the pin")
def p_n11(box):
    sp, tp = _pair(box)
    code, out = L.run_control(sp, tp, _ctl(box))
    want = NC.expected_drift(L.read(sp), L.read(tp)) or []

    def score(want_rows):
        ok, detail = NC.score_baseline(code, out, want_rows)
        return (0 if ok else 1), f"ok={ok}  {detail}"

    good = lambda: score(want)                                             # noqa: E731
    bad = lambda: score(want + ["9"])                                      # noqa: E731
    return good, bad, lambda rc, text: rc != 0


@probe("N19", "a mutation's expect string is one the UNMUTATED report already prints")
def p_n19(box):
    """THE ARM THAT WOULD HAVE CAUGHT INSTANCE 3, exercised against instance 3's own shape.

    The bad world re-points a mutation's `expect` at `all three row sets agree` — a line
    section 1 prints on every healthy run, which is precisely where `"8 9" in out` was
    matching for the positive control's whole life.  The guard must call that row
    UNFALSIFIABLE and take the harness non-zero, not score it CAUGHT.
    """
    ctl = _ctl(box)
    src = L.read(os.path.join(L.TARGET, "negative_control.py"))

    def run_nc(text):
        L.write(os.path.join(ctl, "negative_control.py"), text)
        proc = subprocess.run([sys.executable, os.path.join(ctl, "negative_control.py")],
                              capture_output=True, text=True)
        return proc.returncode, proc.stdout + proc.stderr

    rotted = src.replace('"the row sets disagree", "twin")',
                         '"all three row sets agree", "twin")', 1)
    good = lambda: run_nc(src)                                             # noqa: E731
    bad = lambda: run_nc(rotted)                                           # noqa: E731
    return good, bad, lambda rc, text: rc != 0 and "UNFALSIFIABLE" in text


@probe("N12", "a mutation's search string has rotted into a no-op")
def p_n12(box):
    def run_nc(patched):
        ctl = _ctl(box)
        src = L.read(os.path.join(L.TARGET, "negative_control.py"))
        L.write(os.path.join(ctl, "negative_control.py"), patched(src))
        proc = subprocess.run([sys.executable, os.path.join(ctl, "negative_control.py")],
                              capture_output=True, text=True)
        return proc.returncode, proc.stdout + proc.stderr

    good = lambda: run_nc(lambda s: s)                                     # noqa: E731
    bad = lambda: run_nc(lambda s: s.replace(                              # noqa: E731
        'return re.sub(r\'<tr><td class="rowlabel">7</td>.*?</tr>\', "", text, count=1, flags=re.S)',
        'return text'))
    return good, bad, has("SETUP FAILED")


@probe("N13", "a mutation is no longer caught, i.e. the instrument has a hole")
def p_n13(box):
    ctl = _ctl(box)
    src = L.read(os.path.join(L.TARGET, "negative_control.py"))

    def run_nc(patched):
        L.write(os.path.join(ctl, "negative_control.py"), patched)
        proc = subprocess.run([sys.executable, os.path.join(ctl, "negative_control.py")],
                              capture_output=True, text=True)
        return proc.returncode, proc.stdout + proc.stderr

    holed = src.replace('"the row sets disagree", "twin")',
                        '"a string twin_pin.py never prints", "twin")', 1)
    good = lambda: run_nc(src)                                             # noqa: E731
    bad = lambda: run_nc(holed)                                            # noqa: E731
    return good, bad, lambda rc, text: rc != 0


# ------------------------------------------------------------------ run_all.sh arms
#
# The runner's four branches classify four WORLDS, so the probe substitutes the two producers
# with stubs that exit with a chosen code.  That is the only way to enter three of the four
# branches at all; they had never been entered before this file existed.

_STUB = ("#!/usr/bin/env python3\n"
         "import sys\n"
         "print({body!r})\n"
         "sys.exit({code})\n")


_VERDICT_STUB = "VERDICT: DRIFT — see section 2's worklist.\nsince the twin was last reconciled: 8"


def _runner(box, control_code, negative_code, control_body="(stub control output)"):
    ctl = _ctl(box)
    L.write(os.path.join(ctl, "twin_pin.py"),
            _STUB.format(body=control_body, code=control_code))
    L.write(os.path.join(ctl, "negative_control.py"),
            _STUB.format(body="(stub negative control output)", code=negative_code))
    proc = subprocess.run(["sh", os.path.join(ctl, "run_all.sh")],
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


@probe("H1", "the control reports a STRUCTURAL FAILURE (exit 2)")
def p_h1(box):
    good = lambda: _runner(box, 1, 0, _VERDICT_STUB)                       # noqa: E731
    bad = lambda: _runner(box, 2, 0, _VERDICT_STUB)                        # noqa: E731
    return good, bad, lambda rc, text: rc == 2 and "STRUCTURAL FAILURE" in text


@probe("H2", "the negative control finds a hole (exit 1)")
def p_h2(box):
    good = lambda: _runner(box, 1, 0, _VERDICT_STUB)                       # noqa: E731
    bad = lambda: _runner(box, 1, 1, _VERDICT_STUB)                        # noqa: E731
    return good, bad, lambda rc, text: rc == 2 and "FOUND A HOLE" in text


@probe("H3", "the control reports drift (exit 1)")
def p_h3(box):
    good = lambda: _runner(box, 0, 0, "VERDICT: CLEAN")                    # noqa: E731
    bad = lambda: _runner(box, 1, 0, _VERDICT_STUB)                        # noqa: E731
    return good, bad, has("DRIFT, and the instrument demonstrably fails")


@probe("H5", "the control DIED before printing a verdict")
def p_h5(box):
    good = lambda: _runner(box, 1, 0, _VERDICT_STUB)                       # noqa: E731
    bad = lambda: _runner(box, 1, 0,                                       # noqa: E731
                          "Traceback (most recent call last):\nValueError: no ledger header")
    return good, bad, lambda rc, text: rc == 2 and "WITHOUT printing a VERDICT line" in text


@probe("H6", "the control reports DRIFT with no row in section 2's worklist")
def p_h6(box):
    good = lambda: _runner(box, 1, 0, _VERDICT_STUB)                       # noqa: E731
    bad = lambda: _runner(box, 1, 0, "VERDICT: DRIFT — see section 2's worklist.")
    return good, bad, lambda rc, text: rc == 2 and "section 2 named no drifted row" in text


@probe("H7", "the control exits with a code that is not one of its three verdicts")
def p_h7(box):
    good = lambda: _runner(box, 0, 0, "VERDICT: CLEAN")                    # noqa: E731
    bad = lambda: _runner(box, 3, 0, "VERDICT: CLEAN")                     # noqa: E731
    return good, bad, lambda rc, text: rc == 2 and "not one of its three verdicts" in text


@probe("H4", "the control NEVER RAN — the runner's green must not mean 'found nothing'")
def p_h4(box):
    good = lambda: _runner(box, 0, 0, "VERDICT: CLEAN")                    # noqa: E731
    bad = lambda: _runner(box, 127, 0,                                     # noqa: E731
                          control_body="sh: python3: command not found")
    return good, bad, lambda rc, text: rc != 0 or "CLEAN" not in text


# ======================================================================================
# PART B — auxiliary probes: demonstrated holes in arms that DO discriminate
# ======================================================================================

AUX = []


def aux(title, arm_id, smell):
    def deco(fn):
        AUX.append((title, arm_id, smell, fn))
        return fn
    return deco


@aux("section 5 skips EVERY line containing `<!--`, not just the pin block",
     "C5a/C5b", "a guard exempting far more than it declares")
def x_comment_bypass(box):
    sp, tp = _pair(box)
    t = L.read(tp)
    L.write(tp, t.replace("<span><b>Maintained by</b> pm-onethird</span>",
                          "<span><b>Maintained by</b> pm-onethird</span>\n"
                          "      <!----><span><b>Generated</b> 2026-08-10</span>", 1))
    rc, out = L.run_control(sp, tp, _ctl(box))
    caught = bool(re.search(r"matches /\\bGenerated", sect(out, 5)))
    return (not caught,
            f"OBSERVED NOW: a live `Generated 2026-08-10` prefixed with an empty HTML comment "
            f"makes section 5 say {'FAIL' if caught else 'PASS'} (exit {rc}).  WHAT WAS FOUND: "
            f"the skip read `if L.PIN_START.split()[0] in line`, which is the token `<!--`, so "
            f"EVERY line carrying an HTML comment opener was exempt from the whole guard — and "
            f"it did not even achieve its stated purpose, since only the pin block's FIRST line "
            f"contains `<!--` and the rest of the block was scanned anyway.  An exemption wider "
            f"than the thing it names and narrower, at once.  COVERAGE.md declares an <i>/<s> "
            f"bypass; this one was undeclared.  REPAIRED to a line range (mg-9876).")


@aux("section 6 is a SUBSTRING test — a truncated pin commit passes",
     "C6b", "substring/membership test rather than a parsed field")
def x_sec6_substring(box):
    sp, tp = _pair(box)
    t = L.read(tp)
    pin = B.parse_pin(t)
    full = pin["commit"]
    L.write(tp, t.replace(f"commit: {full}", f"commit: {full[:4]}", 1))
    rc, out = L.run_control(sp, tp, _ctl(box))
    passed = "PASS  the visible line quotes the pinned commit" in sect(out, 6)
    return (passed,
            f"OBSERVED NOW: with the pin's commit truncated to {full[:4]!r}, section 6 says "
            f"{'PASS' if passed else 'FAIL'}.  WHAT WAS FOUND: the test was "
            f"`pinned_commit in shown` — a membership test against the whole visible line — so "
            f"any prefix of the displayed hash satisfied it, and so did a line naming the "
            f"pinned commit ALONGSIDE another revision.  Ticket smell #1, in the arm added to "
            f"check a duplicated provenance string.  REPAIRED to parse the commits out of the "
            f"line and compare the list EXACTLY (mg-9876).")


@aux("section 3 cannot tell 'STATE.md moved' from 'the pin records no digest'",
     "C3", "an arm whose only failure state is annotated 'NOT a defect'")
def x_sec3_confusable(box):
    sp, tp = _pair(box)
    base_rc, base_out = L.run_control(sp, tp, _ctl(box))
    t = L.read(tp)
    L.write(tp, re.sub(r"\n\s*state-sha256: [0-9a-f]+", "", t, count=1))
    rc, out = L.run_control(sp, tp, _ctl(box))
    absent = sect(out, 3)
    moved_sp = os.path.join(box, "STATE_moved.md")
    L.write(moved_sp, L.read(sp) + "\nx\n")
    L.write(tp, t)
    _rc2, out2 = L.run_control(moved_sp, tp, _ctl(box))
    same_class = ("DIFFERS" in absent) and ("DIFFERS" in sect(out2, 3))
    return (same_class,
            f"OBSERVED NOW: the two inputs report the same section-3 class: {same_class}.  "
            "WHAT WAS FOUND: deleting the pin's `state-sha256` field entirely and moving "
            "STATE.md both printed `DIFFERS`, under a heading whose own text says that state "
            "`is NOT a defect and must not be read as one`.  A broken pin was therefore "
            "indistinguishable from the normal condition and read as it.  Same shape as the "
            "`state-sha256` parse defect COVERAGE.md records as fixed — the field PATTERN was "
            "repaired, the ABSENCE never was.  REPAIRED: absence is now its own arm, C3a, at "
            "structural grade (mg-9876).")


@aux("a CRASH in the control is reported by the runner as DRIFT, and exits 0",
     "H3", "a check downstream of a construct that cannot distinguish failure from finding")
def x_crash_is_drift(box):
    sp, _tp = _pair(box)
    ctl = _ctl(box)
    L.write(os.path.join(box, "STATE.md"),
            L.read(sp).replace("| # | Result | Kind | Status | Width |",
                               "| # | RESULT | Kind | Status | Width |", 1))
    L.write(os.path.join(ctl, "negative_control.py"),
            _STUB.format(body="(stub: negative control forced green)", code=0))
    proc = subprocess.run(["sh", os.path.join(ctl, "run_all.sh")],
                          capture_output=True, text=True)
    text = proc.stdout + proc.stderr
    laundered = proc.returncode == 0 and "DRIFT, and the instrument demonstrably fails" in text
    return (laundered,
            f"OBSERVED NOW: STATE.md's ledger header renamed so `parse_state_ledger` raises — "
            f"twin_pin.py dies with a traceback (present: {'Traceback' in text}) and the runner "
            f"exits {proc.returncode}.  WHAT WAS FOUND: python exits 1 both when the control "
            f"finds drift and when it dies before reaching a decision, so the runner reported "
            f"a traceback as `DRIFT, and the instrument demonstrably fails when it should` and "
            f"exited 0.  Removing the `tee` fixed WHOSE status was read and left standing the "
            f"deeper error, that the exit code was being asked a question it cannot answer.  "
            f"REPAIRED: the control must first be shown to have printed a VERDICT line "
            f"(mg-9876), which is the rule mg-f8e5 reached from the other direction.")


@aux("the ledger can GAIN A COLUMN and every arm stays green",
     "C2/L2", "an assertion over a fixed field list rather than over the row")
def x_sixth_column(box):
    sp, tp = _pair(box)
    s = L.read(sp)
    rows = B.parse_state_ledger(s)
    mutated = s.replace("| # | Result | Kind | Status | Width |",
                        "| # | Result | Kind | Status | Width | Owner |", 1)
    for _lbl, _cells, raw in rows:
        mutated = mutated.replace(raw, raw + " pm-onethird |", 1)
    base_rc, base_out = L.run_control(sp, tp, _ctl(box))
    L.write(sp, mutated)
    rc, out = L.run_control(sp, tp, _ctl(box))
    same = sect(out, 2) == sect(base_out, 2)
    quiet = same and "expected 5" not in out and rc == base_rc
    return (quiet,
            f"OBSERVED NOW: a sixth column added to the ledger header AND to every row — the "
            f"control exits "
            f"{rc} and section 2 is identical to the unmutated run: {same}.  WHAT WAS FOUND: "
            f"`parse_state_ledger` refuses FEWER than five cells and has no opinion about "
            f"more, and `row_digests` joins four cells BY NAME, so the load-bearing check "
            f"digests a FIXED FIELD LIST rather than the row — any column the ledger grew was "
            f"outside every digest from the day it was added, silently.  REPAIRED: the pin now "
            f"records its column list and section 1 compares it, so the answer comes from the "
            f"pin and is not a list typed into the checker (mg-9876).")


@aux("run_all.sh's DRIFT branch names rows 8 and 9 as LITERALS in its own prose",
     "H3", "an expected value typed by the author rather than derived")
def x_hardcoded_rows(box):
    src = L.read(os.path.join(L.TARGET, "run_all.sh"))
    hits = [ln.strip() for ln in src.split("\n")
            if re.search(r"\brow[s]? \d", ln) and not ln.strip().startswith("#")]
    return (bool(hits),
            "OBSERVED NOW: lines in the runner asserting a row number: "
            + (" | ".join(hits) if hits else "(none)")
            + ".  WHAT WAS FOUND: the DRIFT branch ended with `Row 9 was mg-2f44's and is "
              "RECONCILED; row 8 is the one no ticket names yet` — an expected value typed by "
              "the author, in the runner, and already half wrong.  REPAIRED: the worklist is "
              "now read out of section 2 with sed (mg-9876).  negative_control.py's own rule — 'nothing in this file may name a pinned "
              "commit or a drifted row as a literal' — was adopted one file away and not "
              "applied here.  Nothing checks these sentences against section 2's worklist, "
              "so they rot exactly as the fixture mg-2f44 repaired did.")


# ======================================================================================
# driver
# ======================================================================================

def main():
    print("=" * 92)
    print("mg-9876 — DISCRIMINATION HARNESS for code/rendered_twin_pin_9bc2")
    print("=" * 92)
    print()
    print("PART A — every arm run twice: once where its subject HOLDS, once where it has")
    print("STOPPED.  The arm's own report is read through one predicate on BOTH sides.")
    print("A predicate satisfied by the GOOD input is scored UNFALSIFIABLE and is red — it is")
    print("a defect in THIS instrument, and it is the mg-2f44 defect exactly.")
    print()

    order = {a.id: i for i, a in enumerate(L.ARMS)}
    probes = sorted(PROBES, key=lambda p: order.get(p[0], 999))

    rows = []
    for arm_id, bad_desc, build in probes:
        arm = L.ARMS_BY_ID[arm_id]
        box = L.make_sandbox()
        try:
            good_fn, bad_fn, red = build(box)
            g_rc, g_out = good_fn()
            g_red = bool(red(g_rc, g_out))
            b_rc, b_out = bad_fn()
            b_red = bool(red(b_rc, b_out))
            if g_red:
                verdict, detail = "UNFALSIFIABLE", (
                    f"the predicate is already TRUE on the GOOD input (exit {g_rc}) — this "
                    f"probe cannot fail and is not evidence")
            elif b_red:
                verdict, detail = "DISCRIMINATES", f"good exit {g_rc} silent / bad exit {b_rc} RED"
            else:
                verdict, detail = "LAUNDERED", (
                    f"good exit {g_rc} and bad exit {b_rc} both report the same thing — the "
                    f"arm does not report its subject stopping")
        except Exception as exc:                                          # noqa: BLE001
            verdict, detail = "SETUP FAILED", f"{type(exc).__name__}: {exc}"
        finally:
            shutil.rmtree(box, ignore_errors=True)
        rows.append((arm, bad_desc, verdict, detail))

    covered = {r[0].id for r in rows}
    missing = [a.id for a in L.ARMS if a.id not in covered]

    width = max(len(a.name) for a, _, _, _ in rows)
    print(f"{'arm':<5} {'name'.ljust(width)}  verdict        detail")
    print("-" * 92)
    for arm, bad_desc, verdict, detail in rows:
        print(f"{arm.id:<5} {arm.name.ljust(width)}  {verdict:<14} {detail}")
        print(f"      known-bad input: {bad_desc}")
    print()

    tally = {}
    for _a, _b, v, _d in rows:
        tally[v] = tally.get(v, 0) + 1
    print(f"PART A TALLY over {len(rows)} arms of {len(L.ARMS)} registered:")
    for k in ("DISCRIMINATES", "LAUNDERED", "UNFALSIFIABLE", "SETUP FAILED"):
        print(f"    {k:<14} {tally.get(k, 0)}")
    if missing:
        print(f"    NO PROBE      {len(missing)}  -> {' '.join(missing)}")
    print()

    print("=" * 92)
    print("PART B — AUXILIARY PROBES: arms that discriminate and are still blind")
    print("=" * 92)
    print("Each is a specific known-bad input the arm's NAME promises to catch and does not.")
    print("A hole is not a laundering and is scored separately so neither flatters the other.")
    print()
    aux_hits = 0
    for title, arm_id, smell, fn in AUX:
        box = L.make_sandbox()
        try:
            fired, detail = fn(box)
        except Exception as exc:                                          # noqa: BLE001
            fired, detail = True, f"PROBE ERROR {type(exc).__name__}: {exc}"
        finally:
            shutil.rmtree(box, ignore_errors=True)
        aux_hits += 1 if fired else 0
        print(f"  [{'CONFIRMED' if fired else 'CLOSED'}]  {title}")
        print(f"      arm  : {arm_id}")
        print(f"      smell: {smell}")
        for line in _wrap(detail, 84):
            print(f"      {line}")
        print()
    print(f"PART B TALLY: {aux_hits} of {len(AUX)} auxiliary defects still CONFIRMED; "
          f"{len(AUX) - aux_hits} CLOSED.")
    print("Every one of the six was CONFIRMED before repair.  The frozen transcript of that")
    print("run is out_a2_discriminate_PREREPAIR.txt beside this file — a register that can")
    print("only ever print CONFIRMED is a list of accusations, and one that prints only CLOSED")
    print("is a list of assertions; both halves are on disk.")
    print()

    bad_a = tally.get("LAUNDERED", 0) + tally.get("UNFALSIFIABLE", 0) + tally.get("SETUP FAILED", 0)
    print("=" * 92)
    print(f"VERDICT: {len(rows)} arms probed, {tally.get('DISCRIMINATES', 0)} shown to "
          f"discriminate, {bad_a} not; {aux_hits} demonstrated holes in arms that do.")
    print("=" * 92)
    return 0 if (bad_a == 0 and not missing) else 1


def _wrap(text, width):
    words, line, out = text.split(), "", []
    for w in words:
        if len(line) + len(w) + 1 > width:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return out


if __name__ == "__main__":
    sys.exit(main())
