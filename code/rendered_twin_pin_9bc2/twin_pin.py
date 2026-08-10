#!/usr/bin/env python3
"""mg-9bc2 — the working-tree control for `docs/state-of-the-wall.html`, the rendered twin.

WHAT WENT WRONG.  The twin carried `Generated 2026-07-19` from 2026-07-19 to 2026-08-10.
In that window `STATE.md` was committed to 55 times and went 36,753 -> 186,710 -> 32,772 ->
110,640 bytes, i.e. it was rewritten wholesale twice under a fixed date.  The
drift was eventually found — ledger row 9, mg-07fd's audit of mg-3329 — by a human reading
the two files against each other.  NOTHING COULD HAVE FAILED.  A generation date tells a
reader WHEN a rendering was made; the question a reader actually has is WHETHER it still
matches, and no date has ever been able to answer it.

WORSE, AND IT IS THE MORE IMPORTANT FINDING: the word `Generated` was FALSE.  There is no
generator.  `git log --follow docs/state-of-the-wall.html` is five commits, the first of
which (`29ffbf7`) adds the twin and `STATE.md` together, and the four after it are hand
edits — mg-957a's says so in as many words, "the .html carried the identical false sentence
verbatim".  Nothing in this repository writes the file.  The three scripts that mention it
by name (`code/eps_spec_sweep_372e/s1_census.py`, `s2_classify.py`,
`code/rate_sweep_910c/r2_classify.py`) all READ it as a corpus member.  So for three weeks
the twin asserted a reproducible relationship to a source that it has never had.

WHAT THIS INSTRUMENT DOES, AND WHAT IT REFUSES TO PRETEND TO DO.  It cannot regenerate the
twin, because there is nothing to regenerate it with.  What it can do is make the twin NAME
THE `STATE.md` IT IS A RENDERING OF — mg-1abe's phrase, A PUBLISHER IS NOT A PIN — and then
check that pin.  The pin lives in the twin, at the top of the file, so it cannot be
separated from the artifact it describes.

SIX CHECKS.  Sections 1-3 are the pin; 4 is a cross-document check that does not use the pin
at all; 5 is a default-deny guard on the sentences that caused this; 6 checks the one
duplicate this repair deliberately introduces.

    1  the pin is present, parses, and its row set matches both documents
    2  per-row digests: which STATE.md ledger rows have MOVED since the twin was pinned
    3  the whole-file STATE.md digest, as the coarse "has anything at all moved" signal
    4  KIND MARKS agree between the two documents, live, right now
    5  the twin does not claim to be `Generated`, and does not claim canonicity for itself
    6  the VISIBLE provenance line in the header quotes the same commit as the pin

EXIT CODES.  0 clean · 1 drift (section 2/3) · 2 structural failure (section 1/4/5/6).
Drift is a lower grade than structural failure on purpose: drift is the normal condition of
a hand-maintained rendering between reconciliations, and it is INFORMATION — the row list is
the worklist.  A missing pin, a row set that disagrees, or a re-introduced `Generated` is a
defect in the mechanism itself.

WHAT IS NOT COVERED is stated here and at length in COVERAGE.md.  The twin is a SUMMARY.
Its prose is deliberately shorter than `STATE.md`'s and no byte relation between the two
exists or should, so THIS CONTROL CANNOT TELL YOU THAT AN UNMOVED ROW IS FAITHFULLY
SUMMARISED.  It tells you which rows have moved underneath the summary.  That is strictly
less than "the twin is correct", and it is strictly more than a date.
"""

import argparse
import hashlib
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib9bc2 as L  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATE = os.path.join(ROOT, "STATE.md")
TWIN = os.path.join(ROOT, "docs", "state-of-the-wall.html")

# Section 5's default-deny rules.  Each is (regex, why, exemption-predicate-or-None).
# A rule fires when the regex matches a tag-stripped line AND the exemption does not hold.
#
# THE SECOND RULE IS NOT A BAN ON A PHRASE, it is a ban on an UNATTRIBUTED phrase.  The twin
# is allowed to talk about canonicity and about the source of truth — it must, since it is a
# rendering and has to say what of.  What it may not do is use those words about ITSELF.  So
# the rule is: if the line claims canonicity, the same line must name `STATE.md`.  That is
# checkable, it explains itself in the failure message, and it does not require the guard to
# understand English.
_NAMES_SOURCE = re.compile(r"STATE\.md")

# The visible twin of the pin — see section 6 for why a second copy is allowed to exist.
_PROVENANCE = re.compile(r'<span id="provenance">(.*?)</span>\s*$', re.M | re.S)

# Section 6 compares PARSED FIELDS, so it needs to know what a commit looks like in the
# visible line.  `@ <hash>` is the shape `reconcile()` writes; anything hex-and-long in that
# line is treated as a commit reference, because a SECOND revision named there is exactly the
# ambiguity the arm exists to forbid.
_VISIBLE_COMMIT = re.compile(r"\b[0-9a-f]{7,40}\b")

# Section 3 requires the pin to CARRY a whole-file digest, not merely to disagree with one.
_SHA256 = re.compile(r"^[0-9a-f]{64}$")

BANNED = [
    (re.compile(r"\bGenerated\b\s*20\d\d-\d\d-\d\d"),
     "a generation date on a file that is NOT generated — the false claim this ticket "
     "exists for.  There is no generator; see this instrument's README.",
     None),
    (re.compile(r"source of truth|\bcanonical\b", re.I),
     "a canonicity claim on a line that does not name STATE.md, i.e. the twin claiming to "
     "be canonical.  STATE.md is; the twin's own lede says so.",
     lambda flat: bool(_NAMES_SOURCE.search(flat))),
]


def sha256_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def sort_labels(labels):
    return sorted(labels, key=lambda s: (int(re.match(r"\d+", s).group()), s))


def check(state_text, twin_text, state_sha):
    """Run all five sections.  Returns (exit_code, list_of_lines)."""
    out = []
    worst = 0

    def emit(line=""):
        out.append(line)

    emit("=" * 86)
    emit("mg-9bc2 — rendered-twin pin control")
    emit("  source : STATE.md")
    emit("  twin   : docs/state-of-the-wall.html")
    emit("=" * 86)
    emit()

    # ---------------------------------------------------------------- section 1
    emit("SECTION 1 — the pin is present and its row set matches both documents")
    emit("-" * 86)
    pin = L.parse_pin(twin_text)
    if pin is None:
        emit("  FAIL  no STATE-PIN block in the twin.")
        emit("        The twin does not say which STATE.md it is a rendering of.  That is the")
        emit("        defect this instrument exists to prevent; there is nothing to check.")
        return 2, out

    state_rows = L.parse_state_ledger(state_text)
    twin_rows = L.parse_twin_ledger(twin_text)
    s_labels = set(l for l, _, _ in state_rows)
    t_labels = set(l for l, _ in twin_rows)
    p_labels = set(pin["rows"])

    emit(f"  pin commit      : {pin.get('commit', '(absent)')}")
    emit(f"  pin commit-date : {pin.get('commit-date', '(absent)')}")
    emit(f"  pinned rows     : {len(p_labels)}   STATE.md rows: {len(s_labels)}   "
         f"twin rows: {len(t_labels)}")
    if s_labels == t_labels == p_labels:
        emit(f"  PASS  all three row sets agree: {' '.join(sort_labels(s_labels))}")
    else:
        worst = 2
        emit("  FAIL  the row sets disagree — a row was added or dropped in one document only.")
        emit(f"        in STATE.md not twin : {sort_labels(s_labels - t_labels) or '—'}")
        emit(f"        in twin not STATE.md : {sort_labels(t_labels - s_labels) or '—'}")
        emit(f"        in STATE.md not pin  : {sort_labels(s_labels - p_labels) or '—'}")
    # THE COLUMN LIST IS PART OF THE PIN (mg-9876).  `row_digests` joins FOUR NAMED CELLS,
    # so every column the ledger grows is outside the pin from the day it is added.  A sixth
    # column was demonstrated being added to the header and to all twelve rows with section 2
    # byte-identical and nothing raising — `parse_state_ledger` refuses FEWER than five cells
    # and has no opinion about more.  The pin now records the columns its digests were taken
    # over, so the answer comes from the pin and is not a list typed here.
    pinned_cols = pin.get("columns", "")
    actual_cols = " | ".join(L.ledger_columns(state_text))
    emit(f"  pinned columns  : {pinned_cols or '(absent)'}")
    emit(f"  actual columns  : {actual_cols}")
    if not pinned_cols:
        worst = 2
        emit("  FAIL  the pin does not record the ledger columns its digests were taken over,")
        emit("        so a column added to the ledger would sit outside every digest silently.")
    elif pinned_cols == actual_cols:
        emit("  PASS  the ledger's columns are the ones the pinned digests were taken over.")
    else:
        worst = 2
        emit("  FAIL  the ledger's column set has changed since the pin.  Every per-row digest")
        emit("        below is taken over a DIFFERENT set of cells than the ledger now has.")
        emit(f"        in pin not STATE.md  : {sort_labels(p_labels - s_labels) or '—'}")
    emit()

    # ---------------------------------------------------------------- section 2
    emit("SECTION 2 — per-row digests: which STATE.md rows have MOVED since the twin was pinned")
    emit("-" * 86)
    now = L.row_digests(state_text)
    moved, unmoved = [], []
    for label in sort_labels(s_labels & p_labels):
        if pin["rows"][label] == now[label]:
            unmoved.append(label)
            emit(f"  row {label:<3}  ok       {now[label]}")
        else:
            moved.append(label)
            emit(f"  row {label:<3}  MOVED    pinned {pin['rows'][label]}  ->  now {now[label]}")
    emit()
    if moved:
        worst = max(worst, 1)
        emit(f"  DRIFT  {len(moved)} of {len(s_labels & p_labels)} ledger rows have changed in")
        emit(f"         STATE.md since the twin was last reconciled: {' '.join(moved)}")
        emit("         Each is a row the twin renders from text that no longer exists.")
        emit("         This is the WORKLIST.  Reconcile the twin's cell, then re-pin that row:")
        emit(f"             python3 code/rendered_twin_pin_9bc2/twin_pin.py --reconcile "
             f"--rows {','.join(moved)}")
    else:
        emit(f"  PASS  all {len(unmoved)} pinned rows still match STATE.md.")
    emit()

    # ---------------------------------------------------------------- section 3
    emit("SECTION 3 — whole-file digest (the coarse signal)")
    emit("-" * 86)
    pinned_sha = pin.get("state-sha256", "")
    emit(f"  pinned STATE.md sha256 : {pinned_sha or '(absent)'}")
    emit(f"  actual STATE.md sha256 : {state_sha}")
    # THE FIELD MUST BE PRESENT AND WELL-FORMED, AND THAT IS A SEPARATE ARM (mg-9876).
    # Without this, deleting `state-sha256` from the pin entirely made section 3 compare the
    # real digest against the empty string and print `DIFFERS` — the same words it prints on
    # every ordinary run, under a heading that says in terms that DIFFERS `is NOT a defect
    # and must not be read as one`.  A broken pin was therefore indistinguishable from the
    # normal condition, and read as it.  COVERAGE.md already records the ancestor of this:
    # the field-name pattern was `[a-z-]+`, `state-sha256` has digits, and section 3 printed
    # the right answer for the wrong reason.  The PATTERN was repaired; the ABSENCE never was.
    if not _SHA256.match(pinned_sha):
        worst = 2
        emit("  FAIL  the pin carries no well-formed `state-sha256` field.  This is a broken")
        emit("        pin, NOT a moved STATE.md, and the two must not print the same word.")
    elif pinned_sha == state_sha:
        emit("  PASS  STATE.md is byte-identical to the revision the twin was pinned against.")
    else:
        worst = max(worst, 1)
        emit("  DIFFERS  STATE.md has changed since the pin.")
        emit("           This alone is NOT a defect and must not be read as one: STATE.md")
        emit("           changes constantly outside the ledger, and section 2 is the check")
        emit("           that carries the verdict.  This line exists so that 'the ledger is")
        emit("           unmoved' cannot be mistaken for 'the file is unmoved'.")
    emit()

    # ---------------------------------------------------------------- section 4
    emit("SECTION 4 — KIND MARKS agree between the two documents (live, does not use the pin)")
    emit("-" * 86)
    twin_kind = {l: L.canonical_kind(d["kind"]) for l, d in twin_rows}
    bad = []
    for label, cells, _raw in state_rows:
        want = L.md_kinds(cells["kind"])
        got = twin_kind.get(label, [])
        if want == got:
            emit(f"  row {label:<3}  ok       {' / '.join(want)}")
        else:
            bad.append(label)
            emit(f"  row {label:<3}  MISMATCH STATE.md {want}  vs  twin {got}")
    emit()
    if bad:
        worst = 2
        emit(f"  FAIL  the Kind column disagrees at {len(bad)} row(s): {' '.join(bad)}")
        emit("        Kind is a controlled vocabulary (U / U-id / FP / FP✗ / OPEN) and is the")
        emit("        one column that IS directly comparable across the summary boundary.")
        emit("        STATE.md's § Kinds says a row's kind decides what may be quoted from it,")
        emit("        so a twin carrying the wrong kind mis-licenses every quote of that row.")
    else:
        emit(f"  PASS  all {len(state_rows)} rows carry the same kind mark in both documents.")
    emit()

    # ---------------------------------------------------------------- section 5
    emit("SECTION 5 — default-deny guard on the two false self-descriptions")
    emit("-" * 86)
    # THE SCAN IS OVER TAG-STRIPPED TEXT, AND THAT IS NOT A REFINEMENT — IT IS THE FIX FOR
    # A DEFECT THIS GUARD SHIPPED WITH.  The first version matched the raw line, and it did
    # not fire on the twin's own `<span><b>Generated</b> 2026-07-19</span>`: the markup sits
    # between the word and the date, so /\bGenerated\b\s+20\d\d/ never matched the one
    # string the guard was written to catch.  A guard against a false claim, blind to that
    # claim, in the file the ticket is about.  Caught only by running it.
    # USE vs MENTION, and this is not a hypothetical.  The repaired lede EXPLAINS the false
    # claim, so it contains the words `Generated 2026-07-19` in order to repudiate them, and
    # the first version of this guard duly failed the very repair that removed the defect.
    # A guard that cannot tell a claim from a quotation of a dead claim forces the fix to be
    # silent about what it fixed, which is worse than the false positive.
    #
    # THE CONVENTION, stated so it is a convention and not a loophole found later: in this
    # file, a superseded string may be quoted ONLY inside <i>…</i> or <s>…</s>.  Both render
    # visibly as quotation / strike-through, so a reader sees a dead string marked dead —
    # the same discipline STATE.md already uses with ~~…~~, which lib9bc2.md_kinds honours.
    # This IS a bypass: wrapping a live claim in <i> hides it from section 5.  It is a
    # declared one, it costs the writer visible italics, and COVERAGE.md records it.
    # THE SKIP IS A LINE RANGE, NOT A TOKEN MATCH, AND THAT IS A REPAIR (mg-9876).  It read
    # `if L.PIN_START.split()[0] in line: continue` — which is the token `<!--`, so EVERY
    # line carrying an HTML comment opener was exempt from the whole guard, and a live
    # `<!----><span><b>Generated</b> 2026-08-10</span>` was demonstrated walking straight
    # past section 5.  It also failed at its stated job in the other direction: only the pin
    # block's FIRST line contains `<!--`, so the rest of the block was scanned anyway.  An
    # exemption wider than the thing it names, and narrower, at once.
    pin_lo = twin_text[:twin_text.find(L.PIN_START)].count("\n") + 1
    pin_hi = twin_text[:twin_text.find(L.PIN_END)].count("\n") + 1
    hits = []
    for line_no, line in enumerate(twin_text.split("\n"), 1):
        if pin_lo <= line_no <= pin_hi:
            continue
        quoted = re.sub(r"<(i|s)>.*?</\1>", " ", line, flags=re.S)
        flat = L.normalise(L.strip_tags(quoted))
        for pattern, why, exempt in BANNED:
            if pattern.search(flat) and not (exempt and exempt(flat)):
                hits.append((line_no, pattern.pattern, why, flat))
    for line_no, pattern, why, flat in hits:
        emit(f"  FAIL  :{line_no} matches /{pattern}/")
        emit(f"        {why}")
        emit(f"        line: {flat[:150]}")
    if hits:
        worst = 2
    else:
        emit(f"  PASS  no banned self-description is present ({len(BANNED)} rules).")
    emit()

    # ---------------------------------------------------------------- section 6
    emit("SECTION 6 — the VISIBLE provenance line quotes the pin (the duplicate is checked)")
    emit("-" * 86)
    emit("  Section 1's pin is an HTML comment: correct, machine-readable, and INVISIBLE to")
    emit("  every reader who opens the page in a browser.  So the header carries the commit")
    emit("  in visible text too — and that is a SECOND copy of a provenance string, i.e.")
    emit("  exactly the kind of thing this whole ticket is about going stale.  It is only")
    emit("  safe because it is checked here.")
    emit()
    m = _PROVENANCE.search(twin_text)
    if not m:
        worst = 2
        emit('  FAIL  no <span id="provenance"> in the twin — the pin is machine-only and no')
        emit("        reader is shown which STATE.md this is a rendering of.")
    else:
        shown = L.normalise(L.strip_tags(m.group(1)))
        pinned_commit = pin.get("commit", "")
        # THE COMMIT IS PARSED OUT OF THE LINE AND COMPARED EXACTLY (mg-9876).  This read
        # `pinned_commit in shown` — a membership test against the whole visible line, which
        # is ticket smell #1 sitting inside the arm added to check a duplicated provenance
        # string.  Truncating the pin's commit to a four-character prefix was demonstrated to
        # PASS, and so would a line that names the pinned commit alongside another one.  What
        # the arm is for is that the two copies name THE SAME revision, and that is an
        # equality between two parsed fields, not a substring relation.
        shown_commits = _VISIBLE_COMMIT.findall(shown)
        emit(f"  visible : {shown}")
        emit(f"  pinned  : {pinned_commit}")
        emit(f"  commits parsed out of the visible line: {shown_commits or '—'}")
        if not pinned_commit:
            worst = 2
            emit("  FAIL  the pin carries no `commit:` field, so there is nothing to quote.")
        elif shown_commits == [pinned_commit]:
            emit("  PASS  the visible line names exactly the pinned commit and no other.")
        else:
            worst = 2
            emit("  FAIL  the visible provenance line does not name exactly the pinned commit.")
            emit("        A reader and the control would be told two different revisions.")
    emit()

    emit("=" * 86)
    emit({0: "VERDICT: CLEAN — the twin is pinned and its ledger rows have not moved.",
          1: "VERDICT: DRIFT — see section 2's worklist.  The twin renders rows that have "
             "since changed.",
          2: "VERDICT: STRUCTURAL FAILURE — the pin mechanism itself is broken or a banned "
             "claim is back."}[worst])
    emit("=" * 86)
    return worst, out


def reconcile(rows_arg, note):
    """Re-pin.  Per-row and deliberate, never a blanket 'make it pass' button.

    THE TRAP THIS AVOIDS.  A detector with a one-word reset is a detector that gets reset
    instead of read — the drift becomes invisible again and the instrument now certifies it.
    So `--reconcile` requires the caller to NAME the rows they actually reconciled in the
    twin.  Naming a row that has not moved is refused, and `--rows all` still prints every
    row it re-pins so the diff shows what was claimed.
    """
    state_text = open(STATE, encoding="utf-8").read()
    twin_text = open(TWIN, encoding="utf-8").read()
    now = L.row_digests(state_text)
    pin = L.parse_pin(twin_text)

    if pin is None:
        targets = sort_labels(now)
        print(f"no existing pin — seeding all {len(targets)} rows")
    else:
        moved = [l for l in sort_labels(now) if pin["rows"].get(l) != now[l]]
        if rows_arg == "all":
            targets = moved
        else:
            targets = [r.strip() for r in rows_arg.split(",") if r.strip()]
            unknown = [r for r in targets if r not in now]
            if unknown:
                sys.exit(f"REFUSED: no such ledger row(s): {unknown}")
            still = [r for r in targets if r not in moved]
            if still:
                sys.exit(f"REFUSED: row(s) {still} have not moved since the pin — "
                         f"re-pinning them would record a reconciliation that did not happen.")
        if not targets:
            print("nothing to reconcile: no row has moved since the pin.")
            return 0

    merged = dict(pin["rows"]) if pin else {}
    for label in targets:
        merged[label] = now[label]
    for label in list(merged):
        if label not in now:
            del merged[label]

    commit = subprocess.run(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    date = subprocess.run(["git", "-C", ROOT, "log", "-1", "--format=%cs", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    block = L.render_pin(commit, date, sha256_file(STATE), merged, note,
                         " | ".join(L.ledger_columns(state_text)))

    if pin is None:
        twin_text = block + "\n" + twin_text
    else:
        i = twin_text.find(L.PIN_START)
        j = twin_text.find(L.PIN_END, i) + len(L.PIN_END)
        twin_text = twin_text[:i] + block + twin_text[j:]

    # The visible copy moves with the machine-readable one, ALWAYS — section 6 checks that
    # they agree, so leaving this to the caller would just relocate the drift into the
    # reconciliation step and fail the control on the next run.
    visible = (f'<span id="provenance"><b>Reconciled against</b> '
               f'<span class="q">STATE.md</span> @ {commit} ({date}) '
               f'&mdash; a pin, not a date</span>')
    twin_text, n_sub = _PROVENANCE.subn(lambda _m: visible, twin_text)
    if n_sub != 1:
        sys.exit(f'REFUSED: expected exactly one <span id="provenance">, found {n_sub}. '
                 f'Not writing — a half-updated provenance is worse than a stale one.')

    with open(TWIN, "w", encoding="utf-8") as fh:
        fh.write(twin_text)

    print(f"re-pinned {len(targets)} row(s) at {commit} ({date}): {' '.join(targets)}")
    print("NOTE: this records that the twin's cells for those rows WERE ACTUALLY UPDATED.")
    print("      If they were not, the pin is now a lie and the control will not say so.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--reconcile", action="store_true",
                    help="re-pin rows you have actually reconciled in the twin")
    ap.add_argument("--rows", default="",
                    help="comma-separated ledger rows to re-pin, or 'all'")
    ap.add_argument("--note", default="hand-maintained rendering; reconciled per row",
                    help="the note recorded in the pin block")
    ap.add_argument("--state", default=STATE, help="override the STATE.md path (tests)")
    ap.add_argument("--twin", default=TWIN, help="override the twin path (tests)")
    args = ap.parse_args()

    if args.reconcile:
        if not args.rows:
            sys.exit("--reconcile requires --rows: name the rows you reconciled, or 'all'")
        return reconcile(args.rows, args.note)

    state_text = open(args.state, encoding="utf-8").read()
    twin_text = open(args.twin, encoding="utf-8").read()
    code, lines = check(state_text, twin_text, sha256_file(args.state))
    print("\n".join(lines))
    return code


if __name__ == "__main__":
    sys.exit(main())
