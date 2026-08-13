#!/usr/bin/env python3
"""mg-9bc2 — the negative control: does `twin_pin.py` actually fail when it should?

WHY THIS FILE EXISTS.  The artifact this ticket repairs was a claim nobody could check
(`Generated 2026-07-19`), and the obvious way to fail this ticket is to replace it with a
SECOND claim nobody can check — a control that exits 0 because it is looking at nothing.
mg-2da3's battery is the local precedent: it passed byte-identically while `STATE.md` was
gutted from 175,552 to 37,958 bytes, because every path in it was revision-pinned.  So each
mutation below is a specific way the twin or `STATE.md` could go wrong, applied to COPIES in
a temporary directory, with the section that is supposed to catch it named in advance.

READ THE LAST COLUMN.  A mutation that exits 0 is a hole in the instrument, not a pass.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
STATE = os.path.join(ROOT, "STATE.md")
TWIN = os.path.join(ROOT, "docs", "state-of-the-wall.html")

sys.path.insert(0, HERE)
import lib9bc2 as L  # noqa: E402

# The live tree is ALREADY at exit 1 (some ledger rows have drifted), so "did the mutation
# make it fail?" is not a question the exit code can answer on its own here.  Every
# expectation below is therefore stated as a SECTION and a STRING that must appear in the
# output, and the baseline's own output is subtracted first.
#
# NOTHING IN THIS FILE MAY NAME THE DRIFTED ROWS AS A LITERAL.  The drift set is the one
# thing here that is SUPPOSED to change — every reconciliation moves it — so a fixture that
# hardcodes it is a fixture with a one-use lifetime.  Both defects mg-2f44 found were of
# exactly that shape: a literal commit hash that became a no-op, and a literal row list that
# matched an unrelated line and could never fail.  Derive from the pin; assert exactly.
MUTATIONS = []


def mutation(name, section, expect, target):
    def deco(fn):
        MUTATIONS.append((name, section, expect, target, fn))
        return fn
    return deco


# ---------------------------------------------------------------------- section 1
@mutation("pin block deleted entirely", "1",
          "no STATE-PIN block in the twin", "twin")
def m_no_pin(text):
    i = text.find("<!-- STATE-PIN v1")
    j = text.find("STATE-PIN end -->") + len("STATE-PIN end -->")
    return text[:i] + text[j:]


@mutation("a ledger row deleted from the twin only", "1",
          "the row sets disagree", "twin")
def m_drop_twin_row(text):
    return re.sub(r'<tr><td class="rowlabel">7</td>.*?</tr>', "", text, count=1, flags=re.S)


# ---------------------------------------------------------------------- section 2
@mutation("one character changed in an UNDRIFTED STATE.md ledger row (row 1)", "2",
          "row 1    MOVED", "state")
def m_touch_row1(text):
    return text.replace("| 1 | `λ_std = 1 ⟺ ordinal sum` | `U` | **proven** | any |",
                        "| 1 | `λ_std = 1 ⟺ ordinal sum` | `U` | **proven** | ANY |", 1)


@mutation("a whole STATE.md ledger cell emptied (row 10 status)", "2",
          "row 10   MOVED", "state")
def m_empty_row10(text):
    return text.replace("| ⚠️ **`FP`** | empirical (125/126) | n ≤ 6 data |",
                        "| ⚠️ **`FP`** |  | n ≤ 6 data |", 1)


# ---------------------------------------------------------------------- section 4
@mutation("twin's KIND mark for row 10 flipped FP -> U", "4",
          "row 10   MISMATCH", "twin")
def m_flip_kind(text):
    return text.replace('<span class="kind fp">&#9888;&#65039; FP</span>',
                        '<span class="kind u">U</span>', 1)


@mutation("STATE.md's KIND mark for row 9 flipped FP✗ -> U", "4",
          "row 9    MISMATCH", "state")
def m_flip_state_kind(text):
    return text.replace("| `FP✗` | **first disjunct** false as stated",
                        "| `U` | **first disjunct** false as stated", 1)


# ---------------------------------------------------------------------- section 5
@mutation("`Generated <date>` re-introduced into the header", "5",
          r"matches /\bGenerated\b", "twin")
def m_regenerate_claim(text):
    return text.replace("<span><b>Maintained by</b> pm-onethird</span>",
                        "<span><b>Maintained by</b> pm-onethird</span>\n"
                        "      <span><b>Generated</b> 2026-08-10</span>", 1)


@mutation("the twin re-claims canonicity in the footer", "5",
          "a canonicity claim on a line that does not name STATE.md", "twin")
def m_reclaim_canon(text):
    return text.replace("<footer>",
                        "<footer>\n    <p>This is the source of truth for the program.</p>", 1)


# ---------------------------------------------------------------------- section 6
@mutation("visible provenance line points at a DIFFERENT commit than the pin", "6",
          "the visible provenance line does not name exactly the pinned commit", "twin")
def m_desync_visible(text):
    """Repoint the VISIBLE provenance line at a commit the pin does not name.

    THIS MUTATION USED TO BE WRITTEN AS A LITERAL, `text.replace("@ 276aead1a8c5
    (2026-08-07)", ...)`, AND THE FIRST RECONCILIATION AFTER IT WAS WRITTEN TURNED IT INTO A
    NO-OP (mg-2f44, re-pinning row 9).  The harness scored that SETUP FAILED and said so,
    which is the harness working — but the fixture was guaranteed to rot at exactly the
    moment the instrument is used for its purpose, i.e. it was a check with a one-use
    lifetime.  It now reads the commit out of the file, so it survives every re-pin.
    """
    return re.sub(r'(<span id="provenance">.*?@ )([0-9a-f]{7,40})',
                  r"\g<1>deadbeefcafe", text, count=1, flags=re.S)


@mutation("visible provenance line removed (pin becomes machine-only)", "6",
          "no <span id=\"provenance\">", "twin")
def m_drop_visible(text):
    return re.sub(r'<span id="provenance">.*?</span>\s*$', "", text, count=1, flags=re.M | re.S)


# ------------------------------------------------- arms added by mg-9876's audit
# Each of these is a known-bad input that the section it names USED TO PASS.  They are here
# rather than in the auditing directory because a demonstration that lives somewhere else is
# a demonstration this file's own runner will never make again.

@mutation("the ledger GAINS A COLUMN (header and every row)", "1",
          "the ledger's column set has changed since the pin", "state")
def m_sixth_column(text):
    out = text.replace("| # | Result | Kind | Status | Width |",
                       "| # | Result | Kind | Status | Width | Owner |", 1)
    for line in text.split("\n"):
        if re.match(r"^\|\s*[0-9]+[a-z]?\s*\|", line):
            out = out.replace(line + "\n", line + " pm-onethird |\n", 1)
    return out


@mutation("the pin's `state-sha256` field is deleted outright", "3",
          "the pin carries no well-formed `state-sha256` field", "twin")
def m_drop_state_sha(text):
    return re.sub(r"\n\s*state-sha256: [0-9a-f]+", "", text, count=1)


@mutation("the pin's `columns` field is deleted outright", "1",
          "the pin does not record the ledger columns", "twin")
def m_drop_columns(text):
    return re.sub(r"\n\s*columns: [^\n]+", "", text, count=1)


@mutation("`Generated <date>` re-introduced BEHIND an HTML comment opener", "5",
          r"matches /\bGenerated\b", "twin")
def m_regenerate_behind_comment(text):
    """The bypass mg-9876 demonstrated: section 5 skipped every line containing `<!--`."""
    return text.replace("<span><b>Maintained by</b> pm-onethird</span>",
                        "<span><b>Maintained by</b> pm-onethird</span>\n"
                        "      <!----><span><b>Generated</b> 2026-08-10</span>", 1)


@mutation("visible provenance names the pinned commit AND a second one", "6",
          "does not name exactly the pinned commit", "twin")
def m_two_commits(text):
    """`pinned_commit in shown` was satisfied by any line CONTAINING the commit."""
    return re.sub(r'(<span id="provenance">.*?@ [0-9a-f]{7,40})',
                  r"\g<1> (was deadbeefcafe)", text, count=1, flags=re.S)


# ------------------------------------------------- arms added by mg-7cc3's fold of mg-3902
_PIN_COMMIT = re.compile(r"(\n\s*commit:\s*)[0-9a-f]{7,40}")
_VISIBLE_AT = re.compile(r'(<span id="provenance">.*?@ )[0-9a-f]{7,40}', re.S)


@mutation("BOTH copies of the pinned commit name a revision that does not exist", "7",
          "the pinned commit DOES NOT RESOLVE in this repository", "twin")
def m_pin_unresolvable(text):
    """mg-3902's HEADLINE MEASUREMENT, reproduced here as a row of this table.

    Setting the pin's `commit:` AND its visible duplicate to a commit this repository does not
    contain left the SIX-section control at `VERDICT: CLEAN`, exit 0.  Section 3 compares the
    pinned digest against the LIVE WORKING TREE and section 6 compares the pinned commit
    against the visible copy of ITSELF, so moving both copies together satisfied every check
    there was.  That is `Generated 2026-07-19` in a new field: an unfalsifiable provenance
    claim, shipped inside the instrument built to remove unfalsifiable provenance claims.

    BOTH COPIES, NOT ONE, AND THAT IS THE WHOLE POINT.  Mutating only the visible line is
    already covered — it is `m_desync_visible`, and section 6 catches it.  This row exists
    because moving them TOGETHER was invisible, and it is section 7 that sees it.

    The commit is a literal here and that does not rot: `deadbee` is chosen for NOT naming
    anything, and the fixtures this file's own header warns about are the ones that name
    something real and stop doing so.
    """
    text = _PIN_COMMIT.sub(lambda m: m.group(1) + "deadbee", text, count=1)
    return _VISIBLE_AT.sub(lambda m: m.group(1) + "deadbee", text, count=1)


# ---------------------------------------------------------------------- positive control
@mutation("NO MUTATION — the baseline", "-",
          None, "none")
def m_none(text):
    return text


_WORKLIST = re.compile(r"since the twin was last reconciled: (.*)$", re.M)


def expected_drift(state_text, twin_text):
    """The drift worklist the baseline MUST report, derived from the pin, not hardcoded."""
    pin = L.parse_pin(twin_text)
    if pin is None:
        return None
    now = L.row_digests(state_text)
    return [lbl for lbl in sorted(now, key=lambda s: (int(re.match(r"\d+", s).group()), s))
            if lbl in pin["rows"] and pin["rows"][lbl] != now[lbl]]


def score_baseline(code, out, want_rows):
    """Score the unmutated run.  Returns (ok, detail).

    THE ASSERTION THIS REPLACES COULD NOT FAIL, AND IT DID NOT FAIL WHEN IT SHOULD HAVE
    (found mg-2f44).  It read:

        ok = (code == 1 and "rows 8 and 9" not in out and "8 9" in out
              and "STRUCTURAL" not in out)

    `"8 9" in out` was meant to say "the drift worklist is exactly rows 8 and 9".  It is a
    substring test against the WHOLE report, and section 1 prints

        PASS  all three row sets agree: 1 2 3a 3b 4 5 6 7 8 9 10 11

    on every healthy run — so `"8 9"` matched there, unconditionally and forever, no matter
    which rows had actually drifted.  When mg-2f44 reconciled row 9 and the true worklist
    became `8`, this line still scored CAUGHT.  A positive control that cannot fail is the
    exact defect the whole ticket is about — mg-9bc2's own run_all.sh laundered a DRIFT
    verdict into `CLEAN` in the same directory — and it is worth more than the mutation it
    was guarding, because the baseline is what licenses reading every other row.

    The replacement parses section 2's worklist LINE and compares the row list EXACTLY,
    against an expectation derived from the pin rather than typed in, so it neither rots at
    the next reconciliation nor passes on a coincidence.
    """
    if code != 1 and want_rows:
        return False, f"exit {code}; expected DRIFT (exit 1) at rows {' '.join(want_rows)}"
    if "STRUCTURAL" in out:
        return False, f"exit {code}; a structural failure fired on an unmutated tree"
    m = _WORKLIST.search(out)
    got = m.group(1).split() if m else []
    if got != want_rows:
        return False, (f"exit {code}; worklist is {got or '(none)'}, "
                       f"expected exactly {want_rows or '(none)'}")
    return True, (f"exit {code}; worklist is EXACTLY {' '.join(want_rows) or '(none)'} "
                  f"— parsed from section 2, expectation derived from the pin")


def run(state_path, twin_path):
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "twin_pin.py"),
         "--state", state_path, "--twin", twin_path],
        capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def main():
    base_state = open(STATE, encoding="utf-8").read()
    base_twin = open(TWIN, encoding="utf-8").read()

    print("=" * 92)
    print("mg-9bc2 — NEGATIVE CONTROL for twin_pin.py")
    print("=" * 92)
    print()
    want_drift = expected_drift(base_state, base_twin) or []

    print("Each mutation is applied to a COPY.  The live tree is never written.")
    if want_drift:
        print(f"The instrument's baseline verdict is DRIFT (exit 1) because ledger row(s) "
              f"{' '.join(want_drift)}")
        print("really have moved, so the exit code alone cannot score these; each row states")
        print("the section that must fire and the string that must appear.")
    else:
        print("The instrument's baseline verdict is CLEAN (exit 0): no pinned ledger row has")
        print("moved.  Each row below states the section that must fire and the string that")
        print("must appear.")
    print("The drift set above is DERIVED FROM THE PIN, never typed in — see the note at the")
    print("top of this file for the two fixtures that rotted when it was (mg-2f44).")
    print()

    # ------------------------------------------------------------------ mg-9876
    # THE BASELINE-ABSENCE GUARD, WHICH IS mg-2f44's REPAIR GENERALISED TO EVERY ARM.
    # Each mutation below scores CAUGHT when its `expect` string appears in the mutated
    # report.  The question this file never asked is whether that string was ALREADY THERE
    # before the mutation — and for the positive control it was, for its whole life:
    # `"8 9" in out` matched section 1's row-set listing on every healthy run.  A one-sided
    # membership test cannot tell a string the mutation caused from a string the report
    # prints unconditionally, so the test is now run against the UNMUTATED report first.
    # An expect string present in the baseline is scored UNFALSIFIABLE and counted as a hole:
    # not because the twin is wrong, but because that row of the table is not evidence.
    _base_code, base_report = run(STATE, TWIN)
    unfalsifiable = [(name, section, expect)
                     for name, section, expect, _t, _f in MUTATIONS
                     if expect is not None and expect in base_report]

    tmp = tempfile.mkdtemp(prefix="twinpin9bc2-")
    rows, holes = [], 0
    try:
        for name, section, expect, target, fn in MUTATIONS:
            sp = os.path.join(tmp, "STATE.md")
            tp = os.path.join(tmp, "twin.html")
            state_text = fn(base_state) if target == "state" else base_state
            twin_text = fn(base_twin) if target == "twin" else base_twin
            if target == "state" and state_text == base_state:
                rows.append((name, section, "SETUP FAILED", "mutation was a no-op"))
                holes += 1
                continue
            if target == "twin" and twin_text == base_twin:
                rows.append((name, section, "SETUP FAILED", "mutation was a no-op"))
                holes += 1
                continue
            with open(sp, "w", encoding="utf-8") as fh:
                fh.write(state_text)
            with open(tp, "w", encoding="utf-8") as fh:
                fh.write(twin_text)

            code, out = run(sp, tp)
            if expect is None:
                ok, detail = score_baseline(code, out, want_drift)
                verdict = "CAUGHT" if ok else "HOLE"
            elif expect in base_report:
                ok, verdict = False, "UNFALSIFIABLE"
                detail = (f"exit {code}; {expect!r} is in the UNMUTATED report too, so this "
                          f"row could not have failed")
            else:
                ok = expect in out
                verdict = "CAUGHT" if ok else "HOLE"
                detail = f"exit {code}; looked for {expect!r} (absent from the baseline)"
            if not ok:
                holes += 1
            rows.append((name, section, verdict, detail))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    width = max(len(r[0]) for r in rows)
    print(f"{'mutation'.ljust(width)}  sec  verdict  detail")
    print("-" * 92)
    for name, section, verdict, detail in rows:
        print(f"{name.ljust(width)}  {section:<3}  {verdict:<7}  {detail}")
    print()
    print(f"{len(rows) - holes} of {len(rows)} caught; {holes} hole(s).")
    print(f"{len(unfalsifiable)} row(s) UNFALSIFIABLE — expect string present in the "
          f"unmutated report (mg-9876's guard).")
    print()
    if holes:
        print("A HOLE IS A FINDING, NOT A TEST FAILURE TO SUPPRESS — it is a way the twin can")
        print("go wrong that this instrument does not see.  Record it in COVERAGE.md.")
        return 1
    print("Every mutation was caught by the section that claimed it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
