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

import hashlib
import json
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
INFLIGHT = os.path.join(HERE, "IN-FLIGHT.json")

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


# ------------------------------------------------- arms added by mg-1344's section 8
# THE DECLARATION IS THE ONE FILE IN THIS DIRECTORY WHOSE ONLY POWER IS TO MAKE THE GATE
# ACCEPT SOMETHING IT WOULD OTHERWISE REFUSE.  Every arm below is a way of writing one that
# buys a subtraction it has not earned, and each names the check that must refuse it.  The
# target is `inflight`: the base text is the EMPTY STRING, because absence is the normal
# state and every one of these is a file appearing where there was none.

@mutation("a declaration for a row that has NOT moved", "8",
          "declares row(s) that have NOT moved", "inflight")
def m_declare_unmoved(_text):
    """THE MOVE THIS SECTION IS MOST LIKELY TO BE USED FOR, AND IT IS REFUSED.

    Nothing in the ledger has moved on an ordinary tree, so a declaration naming any row at
    all is a standing subtraction bought for a row that is fine — COVERAGE.md item 4's
    "re-pinning a row nobody reconciled", one level up.  Row 1 is a literal here and cannot
    rot in the way this file's header warns about: the fixture asserts the row is NOT moved,
    which is the ordinary state, rather than asserting which rows ARE.
    """
    return json.dumps({"schema": 1, "declared_by": "mg-1344 (planted)", "rows": ["1"],
                       "why": "planted world: this row has not moved",
                       "landing_b": "twin_pin.py --reconcile --rows 1"}, indent=2)


@mutation("a declaration for a row that is not in the ledger", "8",
          "declares row(s) that are not in STATE.md's ledger", "inflight")
def m_declare_phantom(_text):
    return json.dumps({"schema": 1, "declared_by": "mg-1344 (planted)", "rows": ["99z"],
                       "why": "planted world: no such row",
                       "landing_b": "twin_pin.py --reconcile --rows 99z"}, indent=2)


@mutation("a declaration that is not valid JSON", "8",
          "is not valid JSON", "inflight")
def m_declare_malformed(_text):
    """A MALFORMED DECLARATION MUST BE RED, NOT ABSENT.

    The fail-open reading is the tempting one — "unreadable, so nothing is declared, so
    nothing is subtracted, so carry on" — and it is wrong in the direction that matters: it
    makes a file whose whole job is to weaken a check unauditable and silent at once.
    """
    return '{"schema": 1, "rows": ["1"],,,'


@mutation("a declaration with an EMPTY row list", "8",
          "`rows` is EMPTY", "inflight")
def m_declare_no_rows(_text):
    return json.dumps({"schema": 1, "declared_by": "mg-1344 (planted)", "rows": [],
                       "why": "planted world: declares nothing",
                       "landing_b": "n/a"}, indent=2)


@mutation("a declaration with no `why` and no `landing_b`", "8",
          "is missing or empty", "inflight")
def m_declare_no_reason(_text):
    """BASELINE.json's OWN RULE, APPLIED HERE: a value in a declaration with no reason beside
    it is an assertion nobody can audit, and writing one costs nothing.  `landing_b` is
    required for a second reason specific to this file — the expiry is enforced against
    WHOEVER MEETS IT, who is often not the author, and an expiry with no instruction attached
    strands them."""
    return json.dumps({"schema": 1, "rows": ["1"]}, indent=2)


@mutation("a declaration at an unreadable schema version", "8",
          "this control reads schema 1 only", "inflight")
def m_declare_bad_schema(_text):
    return json.dumps({"schema": 2, "declared_by": "x", "rows": ["1"],
                       "why": "x", "landing_b": "x"}, indent=2)


# ---------------------------------------------------------------------- positive control
@mutation("NO MUTATION — the baseline", "-",
          None, "none")
def m_none(text):
    return text


_WORKLIST = re.compile(r"since the twin was last reconciled: (.*)$", re.M)


def expected_drift(state_text, twin_text, inflight_path=INFLIGHT):
    """The drift worklist the baseline MUST report, derived from the pin, not hardcoded.

    THE DECLARED SET IS SUBTRACTED HERE TOO (mg-1344), because section 2 subtracts it and an
    expectation that does not would go wrong on the first landing A this repository makes —
    i.e. exactly when the mechanism is used.  What is NOT reproduced here is the DISCHARGE
    test: if the declaration has expired, twin_pin exits 2 and `score_baseline` refuses on
    `STRUCTURAL` anyway, which is the right answer and is reached without a second copy of
    the predicate living in the scoring code.
    """
    pin = L.parse_pin(twin_text)
    if pin is None:
        return None
    now = L.row_digests(state_text)
    declared = set()
    if os.path.exists(inflight_path):
        try:
            with open(inflight_path, encoding="utf-8") as fh:
                declared = set(json.load(fh).get("rows") or [])
        except (ValueError, AttributeError):
            declared = set()
    return [lbl for lbl in sorted(now, key=lambda s: (int(re.match(r"\d+", s).group()), s))
            if lbl in pin["rows"] and pin["rows"][lbl] != now[lbl] and lbl not in declared]


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


def run(state_path, twin_path, inflight_path=INFLIGHT, root=None):
    argv = [sys.executable, os.path.join(HERE, "twin_pin.py"),
            "--state", state_path, "--twin", twin_path, "--inflight", inflight_path]
    if root is not None:
        argv += ["--root", root]
    proc = subprocess.run(argv, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


# ---------------------------------------------------------------------------------------
# mg-1344 — the two worlds that CANNOT be planted by editing a file
# ---------------------------------------------------------------------------------------
#
# Section 8's whole load is carried by REACHABILITY: a declaration is honoured while no
# integration-reachable commit carries these STATE.md bytes, and red once one does.  Neither
# state can be produced by mutating text, so these two worlds build a THROWAWAY GIT
# REPOSITORY with a real `main` and run the instrument inside it with `--root`.
#
# A FAKE GIT WOULD HAVE BEEN CHEAPER AND WORTH LESS.  The thing under test is what `git
# rev-list`, `git cat-file` and `git merge-base` actually answer about a real history; a stub
# that returns what this file expects is a control scoring its own expectations, which is
# mg-9876's UNFALSIFIABLE class and the reason section 7 exists at all.
#
# THE FIXTURE HAS TO BE TWO COMMITS AND THAT IS THE TICKET'S OWN PROBLEM IN MINIATURE: the
# pin must name a commit that CARRIES the STATE.md it digests, so the pin cannot be written
# into the commit it names.  C1 carries STATE.md and the old pin; C2 rewrites the pin to name
# C1.  Amending C1 instead would rewrite the very hash the pin had just recorded — which is
# the rebase hazard this whole protocol is about, met while building the fixture for it.

# THE EXPECT STRINGS ARE NAMED CONSTANTS BECAUSE TWO FILES READ THEM.  a2_discriminate's
# probes for N27-N29 hand these worlds a baseline report that already contains their expect
# string, to demonstrate that the UNFALSIFIABLE guard fires — and a second copy of the
# string over there would agree today and rot the moment either side is reworded, leaving a
# probe that passes because it is looking for nothing.
EXPECT_HONOURED = "HONOURED — REPORTED, NOT GRADED"
EXPECT_EXPIRED = "THE DEFERRAL HAS EXPIRED"
EXPECT_NOT_HONOURED = "REPORTED, NOT GRADED, AND NOT HONOURED"
EXPECT_WORKLIST = "This is the WORKLIST"


def _git(repo, *args, **kw):
    return subprocess.run(["git", "-C", repo] + list(args),
                          capture_output=True, text=True, **kw)


def _commit(repo, message):
    _git(repo, "add", "-A")
    _git(repo, "-c", "user.email=nc@mg-9bc2", "-c", "user.name=negative-control",
         "-c", "commit.gpgsign=false", "commit", "-q", "-m", message)
    return _git(repo, "rev-parse", "--short", "HEAD").stdout.strip()


_PIN_FIELD_SUB = {
    "commit": r"(\n\s*commit:\s*)[0-9a-f]{7,40}",
    "commit-date": r"(\n\s*commit-date:\s*)\S+",
    "state-sha256": r"(\n\s*state-sha256:\s*)[0-9a-f]{64}",
}


def build_protocol_repo(tmp, base_state, base_twin, moved_row_from, moved_row_to):
    """A repository in which landing A has happened on a branch and nothing else has.

    Returns (repo_path, inflight_path) or (None, reason).
    """
    repo = os.path.join(tmp, "protocol")
    os.makedirs(os.path.join(repo, "docs"))
    with open(os.path.join(repo, "STATE.md"), "w", encoding="utf-8") as fh:
        fh.write(base_state)
    twin_path = os.path.join(repo, "docs", "state-of-the-wall.html")
    with open(twin_path, "w", encoding="utf-8") as fh:
        fh.write(base_twin)
    if _git(repo, "-c", "init.defaultBranch=main", "init", "-q", ".").returncode != 0:
        return None, "git init failed"
    c1 = _commit(repo, "c1: STATE.md and the twin")
    if not c1:
        return None, "the fixture's first commit did not land"
    date = _git(repo, "log", "-1", "--format=%cs").stdout.strip()
    sha = hashlib.sha256(base_state.encode("utf-8")).hexdigest()
    twin = base_twin
    for value, pattern in ((c1, _PIN_FIELD_SUB["commit"]),
                           (date, _PIN_FIELD_SUB["commit-date"]),
                           (sha, _PIN_FIELD_SUB["state-sha256"])):
        twin, n = re.subn(pattern, lambda m, v=value: m.group(1) + v, twin, count=1)
        if n != 1:
            return None, "could not repoint the pin's %r field" % pattern
    twin, n = re.subn(r'(<span id="provenance">.*?@ )[0-9a-f]{7,40}( \()[^)]*(\))',
                      lambda m: m.group(1) + c1 + m.group(2) + date + m.group(3),
                      twin, count=1, flags=re.S)
    if n != 1:
        return None, "could not repoint the visible provenance line"
    with open(twin_path, "w", encoding="utf-8") as fh:
        fh.write(twin)
    _commit(repo, "c2: point the pin at c1, which survives")

    # LANDING A, on a branch: the row's text moves out and the row is DECLARED.
    _git(repo, "switch", "-q", "-c", "landing-a")
    with open(os.path.join(repo, "STATE.md"), "w", encoding="utf-8") as fh:
        fh.write(base_state.replace(moved_row_from, moved_row_to, 1))
    inflight = os.path.join(repo, "code", "rendered_twin_pin_9bc2", "IN-FLIGHT.json")
    os.makedirs(os.path.dirname(inflight))
    with open(inflight, "w", encoding="utf-8") as fh:
        json.dump({"schema": 1, "declared_by": "mg-1344 (planted world)", "rows": ["1"],
                   "why": "landing A: row 1's text relocated, twin cell reconciled, re-pin "
                          "deferred because no integration-reachable commit carries it yet",
                   "landing_b": "twin_pin.py --reconcile --rows 1"}, fh, indent=2)
    _commit(repo, "c3: landing A")
    return repo, inflight


def protocol_worlds(tmp, base_state, base_twin, base_report):
    """The two graded worlds, plus the one that must NOT be honoured.  Returns table rows."""
    moved_from = "| 1 | `λ_std = 1 ⟺ ordinal sum` | `U` | **proven** | any |"
    moved_to = ("| 1 | `λ_std = 1 ⟺ ordinal sum` | `U` | **proven** | "
                "see docs/state-history/ledger-row-1.md |")
    # EXACTLY ONCE, NOT `in` — mg-9876's smell #1 is a membership test standing in for a
    # fact, and a fixture that relocates "the" row when TWO lines match it is a fixture that
    # relocates an arbitrary one.  A count is the fact; a membership test is a guess at it.
    if base_state.count(moved_from) != 1:
        why = ("row 1's ledger line occurs %d time(s) in STATE.md; this fixture relocates "
               "exactly one" % base_state.count(moved_from))
        return [("landing A planted in a real git repository", "8", "SETUP FAILED", why),
                ("landing A after its bytes reach `main`", "8", "SETUP FAILED", why)]
    repo, inflight = build_protocol_repo(tmp, base_state, base_twin, moved_from, moved_to)
    if repo is None:
        return [("landing A planted in a real git repository", "8", "SETUP FAILED", inflight),
                ("landing A after its bytes reach `main`", "8", "SETUP FAILED", inflight)]
    state_path = os.path.join(repo, "STATE.md")
    twin_path = os.path.join(repo, "docs", "state-of-the-wall.html")
    rows = []

    def score(name, expect, forbid=None):
        code, out = run(state_path, twin_path, inflight, root=repo)
        if expect in base_report:
            rows.append((name, "8", "UNFALSIFIABLE",
                         "%r is in the UNMUTATED report too" % expect))
            return False
        ok = expect in out and (forbid is None or forbid not in out)
        detail = "exit %d; looked for %r" % (code, expect)
        if forbid is not None:
            detail += " and required %r to be absent" % forbid
        rows.append((name, "8", "CAUGHT" if ok else "HOLE", detail))
        return ok

    # WORLD A — landing A on a branch.  HONOURED, exit 0, and the row is OUT of the worklist.
    # This is the only world in this file that must PASS: the point of the protocol is that
    # landing A can merge, and a mechanism that refuses it is the deadlock with more code.
    score("landing A planted in a real git repository", EXPECT_HONOURED,
          forbid=EXPECT_WORKLIST)

    # WORLD B — the SAME declaration once its bytes are on `main`.  The excuse has expired.
    _git(repo, "branch", "-f", "main", "landing-a")
    score("landing A after its bytes reach `main`", EXPECT_EXPIRED)
    return rows


def unknown_world(tmp, base_state, base_twin, base_report):
    """A declaration in a checkout git cannot be asked about is NOT honoured.

    THE DIRECTION THIS ARM DEFENDS IS THE FAIL-OPEN ONE.  Section 7 answers `unknown` by
    reporting and not grading, and the first draft of section 8 copied that verbatim — which,
    for a check whose effect is to REMOVE a row from the merge gate's worklist, means an
    export, a tarball or a shallow clone silently honours any declaration at all.  Not
    grading and not honouring are the same doctrine at opposite signs, and this world is the
    half that could otherwise have gone quiet.
    """
    plain = os.path.join(tmp, "no-git")
    os.makedirs(os.path.join(plain, "docs"))
    state_path = os.path.join(plain, "STATE.md")
    twin_path = os.path.join(plain, "docs", "state-of-the-wall.html")
    moved_from = "| 1 | `λ_std = 1 ⟺ ordinal sum` | `U` | **proven** | any |"
    if base_state.count(moved_from) != 1:
        return [("a declaration in a checkout with no git at all", "8", "SETUP FAILED",
                 "row 1's ledger line occurs %d time(s) in STATE.md; this fixture relocates "
                 "exactly one" % base_state.count(moved_from))]
    with open(state_path, "w", encoding="utf-8") as fh:
        fh.write(base_state.replace(moved_from, moved_from.replace("any |", "elsewhere |"), 1))
    with open(twin_path, "w", encoding="utf-8") as fh:
        fh.write(base_twin)
    inflight = os.path.join(plain, "IN-FLIGHT.json")
    with open(inflight, "w", encoding="utf-8") as fh:
        json.dump({"schema": 1, "declared_by": "mg-1344 (planted world)", "rows": ["1"],
                   "why": "planted world: no history to check the expiry against",
                   "landing_b": "twin_pin.py --reconcile --rows 1"}, fh, indent=2)
    expect = EXPECT_NOT_HONOURED
    code, out = run(state_path, twin_path, inflight, root=plain)
    if expect in base_report:
        return [("a declaration in a checkout with no git at all", "8", "UNFALSIFIABLE",
                 "%r is in the UNMUTATED report too" % expect)]
    ok = expect in out and EXPECT_WORKLIST in out
    return [("a declaration in a checkout with no git at all", "8",
             "CAUGHT" if ok else "HOLE",
             "exit %d; the declaration must be neither graded nor honoured, so row 1 must "
             "stay in section 2's worklist" % code)]


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
            ip = os.path.join(tmp, "IN-FLIGHT.json")
            state_text = fn(base_state) if target == "state" else base_state
            twin_text = fn(base_twin) if target == "twin" else base_twin
            # THE `inflight` TARGET's BASE IS THE EMPTY STRING, not a file's contents, because
            # ABSENCE is this file's normal state — every one of those mutations is a
            # declaration appearing where there was none, so "" is the honest baseline and an
            # empty return is still a no-op that must score SETUP FAILED.
            inflight_text = fn("") if target == "inflight" else ""
            if target in ("state", "twin", "inflight") and not {
                    "state": state_text != base_state,
                    "twin": twin_text != base_twin,
                    "inflight": bool(inflight_text)}[target]:
                rows.append((name, section, "SETUP FAILED", "mutation was a no-op"))
                holes += 1
                continue
            with open(sp, "w", encoding="utf-8") as fh:
                fh.write(state_text)
            with open(tp, "w", encoding="utf-8") as fh:
                fh.write(twin_text)
            if inflight_text:
                with open(ip, "w", encoding="utf-8") as fh:
                    fh.write(inflight_text)
            elif os.path.exists(ip):
                os.remove(ip)

            code, out = run(sp, tp, ip)
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

        # The three worlds that need a REAL git history rather than a mutated file.
        for row in (protocol_worlds(tmp, base_state, base_twin, base_report)
                    + unknown_world(tmp, base_state, base_twin, base_report)):
            rows.append(row)
            if row[2] != "CAUGHT":
                holes += 1
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
