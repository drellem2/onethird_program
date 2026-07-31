#!/usr/bin/env python3
"""mg-8916 -- THE mg-835f REPAIR, MEASURED IN BOTH DIRECTIONS.

mg-835f audited the mg-a318 repair and returned PARTIAL.  The primary target
held and is not re-opened here: 12 of 12 reader-facing figures corrupted ON
DISK make the run red and 12 of 12 restorations make it green again.  Two sites
were left open, and this instrument is the evidence that both are now closed.

  G-1  A WRONG FIGURE IN ORDINARY PROSE BESIDE THE SITE WAS INVISIBLE, at 3 of
       the 3 sites, at exit 0.  The gate read one DESIGNATED STATEMENT per
       site; a reader reads the SECTION.  So the sentence "the gate reads the
       figure at the site" was itself an extent claim WIDER THAN THE CODE.

  G-2  THE mg-8a5c INSTRUMENT'S OWN BOTTOM LINE ASSERTED A PRIMARY TARGET ITS
       OWN T1 ROW REFUTED.  Re-run at HEAD it printed two [REFUTED] lines in
       T1 -- its declared PRIMARY TARGET -- and then printed, unconditionally,
       "THE PRIMARY TARGET IS CONFIRMED".  Both in the same transcript.

WHICH OF THE TWO REPAIRS WAS DONE FOR G-1, SAID PLAINLY.  The ticket prefers
removing the duplicate over gating it, and offers narrowing the STATED extent
as the fallback.  R1 measures the first: there is nothing to remove.  Every
live figure already occurs exactly ONCE per site -- that is the mg-a318 repair
and the WRITTEN ONCE check keeps it so -- and G-1 is not a duplicate that
exists, it is a duplicate the gate would not SEE if the next correction wrote
one, which is precisely how F-1 was born.  So THE CODE IS WIDENED AND THE CLAIM
IS NOT NARROWED: `figure_gate` now takes a CENSUS of every figure-shaped token
the section asserts.  Neither repair was done silently; this paragraph is the
saying-which the ticket asks for.

  R1  THE CENSUS, ON DISK, BOTH DIRECTIONS.  mg-835f's own U1 probe -- the
      sentence "The gap is now +9 999 characters." written into each of the
      three sites in ordinary prose, LENGTH-PRESERVINGLY so that no measurement
      moves underneath the gate -- run against the REAL runner.  Each probe is
      restored, the restoration is checked by sha256, and the runner is run
      AGAIN, because a gate that fires on everything is worth no more than one
      that fires on nothing.  Plus the probe a set-membership census would
      still pass: a wrong prose figure REUSING a value already on the roster.

  R2  THE SUMMARY-VERSUS-ROWS CHECK, DEMONSTRATED FIRING.  The mg-8a5c
      instrument is run twice: once normally, where its derived bottom line and
      its PRIMARY rows agree; and once with the summary FORCED to the sentence
      it used to print unconditionally, where the check goes red.  A
      summary-versus-rows check that has never been shown to fire is the
      vacuous-check defect this arc has produced three times.

  R3  THE RESIDUE, AND WHAT WAS WRITTEN VERSUS REGENERATED.  What the census
      does not cover, printed rather than left to be found; and which artifact
      in this repair is a frozen run and which is regenerated to follow.

  R4  mg-835f's OWN INSTRUMENT, UNMODIFIED, RE-RUN against the repaired tree.
      A repair scored only by its own new instrument is a repair scored by the
      party that wrote it.  Its committed transcript is NOT overwritten.

PREDICTED EXIT CODE, WRITTEN BEFORE THE FIRST RUN: 0.  Every probe's verdict is
written before it runs and any disagreement is a refutation.

IT MUTATES THE TREE AND RESTORES IT.  R1 writes to `STATE.md`, the deliverable
and the row-history file, and `git checkout --`s each back inside a `finally`.
It REFUSES TO RUN against a dirty tree, scoped to those three files: a
`git checkout --` over an uncommitted edit to one of them destroys it.  Every
restoration is CHECKED by sha256, not asserted.

REPRODUCTION CONTRACT, in terms of the FILES READ.  This transcript regenerates
byte-identically for any tree in which `STATE.md`,
`docs/OneThird-Hodge-Side-Leverage.md`, `docs/state-history/attempt-mg-a3d4.md`,
`code/hodge_leverage_landing_e1d0/`, `code/hodge_leverage_audit_8a5c/` and
`code/hodge_leverage_audit_835f/` are unchanged.  It embeds no sha of its own.

Pure Python 3 + git.  No third-party packages.  Runtime ~3 min, almost all of
it the 13 runs of the audited runner, the 2 runs of the mg-8a5c instrument and
the one run of mg-835f's own instrument in R4.
"""

import hashlib
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LANDING = os.path.join(REPO, "code/hodge_leverage_landing_e1d0")
sys.path.insert(0, LANDING)
import verify_landing as V                              # noqa: E402  the REPAIRED module

RUNNER = os.path.join(LANDING, "verify_landing.py")
AUDIT_8A5C = os.path.join(REPO, "code/hodge_leverage_audit_8a5c/audit_repair_8e30.py")
AUDIT_8A5C_OUT = "code/hodge_leverage_audit_8a5c/out_audit_8e30.txt"
AUDIT_835F = os.path.join(REPO, "code/hodge_leverage_audit_835f/audit_a318_repair.py")
AUDIT_835F_OUT = "code/hodge_leverage_audit_835f/out_audit_a318.txt"

MUTABLE = [V.STATE, V.DELIV, V.HIST]
# Not mutated here, but the mg-8a5c instrument R2 invokes restores it by
# `git checkout --` and refuses to run if it is dirty.  Checked here so that a
# dirty tree is a REFUSAL with a reason rather than an exit 2 inside R2.
REQUIRE_CLEAN = MUTABLE + ["code/hodge_leverage_landing_e1d0/out_verify.txt"]

RESULTS = []


# --------------------------------------------------------------------------
# plumbing
# --------------------------------------------------------------------------
def heading(row):
    """THE ROW'S HEADING -- everything before the ` -- ` that introduces its
    explanation.

    ⚠️ ADDED BY mg-3f3b (mg-7e39 F3).  The line below used to identify a gate
    row by testing a heading against THE WHOLE ROW, and every row of this gate
    explains itself by NAMING THE OTHER ROWS -- so the test selected rows it
    was never meant to.  mg-ff3e found that construct in its own scoring code
    and fixed it there; mg-6df0 found it 6 times in the tree, repaired 1 and
    gave the other 5 a disposition keyed on their line number.  A DISPOSITION
    IS A REASON, NOT A REPAIR."""
    return row.split(" -- ")[0]


def record(ok, detail):
    RESULTS.append((detail, ok))
    mark = {True: "[CONFIRMED]", False: "[REFUTED  ]", None: "[MEASURED ]"}[ok]
    print(f"  {mark} {detail}")


def head(title):
    print()
    print(title)
    print("-" * len(title))


def sha(path):
    with open(os.path.join(REPO, path), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True, check=True).stdout


def write(path, text):
    with open(os.path.join(REPO, path), "w", encoding="utf-8") as fh:
        fh.write(text)


def restore(*paths):
    subprocess.run(["git", "-C", REPO, "checkout", "--"] + list(paths), check=True)


def run_gate():
    """The REAL runner, against whatever is on disk.  Returns (exit, refuted)."""
    r = subprocess.run([sys.executable, RUNNER], capture_output=True, text=True,
                       cwd=REPO)
    return r.returncode, [l.strip() for l in r.stdout.split("\n")
                          if "[REFUTED  ]" in l]


def run_8a5c(force=None):
    """The mg-8a5c audit instrument.  `force` sets MG8916_FORCE_SUMMARY, whose
    ONLY effect is to make the printed summary disagree with the rows."""
    env = dict(os.environ)
    env.pop("MG8916_FORCE_SUMMARY", None)
    if force:
        env["MG8916_FORCE_SUMMARY"] = force
    r = subprocess.run([sys.executable, AUDIT_8A5C], capture_output=True,
                       text=True, cwd=REPO, env=env)
    return r.returncode, r.stdout


CLEAN = {}


# --------------------------------------------------------------------------
# the sites, and how prose is written into one without moving the figures
# --------------------------------------------------------------------------
SITE_FILE = {"the STATE.md row": V.STATE, "§14": V.DELIV, "H8": V.HIST}

# Prose inside each site that NO check in `verify_landing.py` reads -- named
# rather than found by search, so the transcript says exactly what a probe
# overwrote -- used only to absorb a length delta.  Same ballast mg-835f used.
BALLAST = {
    "the STATE.md row": ["up, down and up again, while the clause mismatch only ever grew"],
    "§14": ["whether or not anyone has stepped on it yet",
            "which is right, and is not retracted"],
    "H8": ["A quantity that moves in both directions while the thing it stands "
           "for moves in one is not a measurement of that thing",
           "while the clause mismatch only ever grew"],
}

ANCHOR = {"the STATE.md row": "**The character metric fails in BOTH directions",
          "§14": "**The conclusion is untouched",
          "H8": "**The sign claim is WITHDRAWN"}


def site_raw(site, full=None):
    full = V.tree(SITE_FILE[site]) if full is None else full
    if site == "the STATE.md row":
        return V.state_row(full)
    if site == "§14":
        return V.section(full, "## §14 — `STATE.md` row, as landed")
    return V.section(full, "### H8 — ")


def measured():
    a = len(V.state_row(V.tree(V.STATE)))
    b = len(V.deliv_row(V.tree(V.DELIV)))
    h = len(V.tree(V.HIST))
    return {"gap": V.doc_num(a - b, signed=True),
            "both": V.doc_num(a + h - b, signed=True),
            "cell": V.doc_num(a), "hist": V.doc_num(h), "copy": V.doc_num(b)}


def retune(site, raw, new_raw):
    """Absorb a length delta into the site's named ballast, so the mutation is
    LENGTH-PRESERVING and the figures do not move underneath it.  Four of the
    five figures are lengths of the very text being mutated: an INSERTION moves
    the measurement, and a gate that fires because the file grew has read
    nothing (mg-835f's own missed prediction, kept as written)."""
    d = len(new_raw) - len(raw)
    for victim in BALLAST[site]:
        if d == 0:
            break
        if new_raw.count(victim) != 1:
            continue
        if d > 0:
            take = min(d, len(victim) - 1)
            new_raw = new_raw.replace(victim, victim[:len(victim) - take], 1)
            d -= take
        else:
            new_raw = new_raw.replace(victim, victim + " " * (-d), 1)
            d = 0
    if d != 0:
        raise SystemExit(f"cannot make the mutation length-preserving at {site}: {d:+d}")
    return new_raw


def prose_at_site(site, value):
    """mg-835f's U1 probe, verbatim: a WRONG figure restated in ORDINARY PROSE
    inside the site, leaving the designated statement correct and untouched."""
    path = SITE_FILE[site]
    full = V.tree(path)
    raw = site_raw(site, full)
    anchor = ANCHOR[site]
    assert raw.count(anchor) == 1, site
    sentence = f"The gap is now {value} characters."
    new_raw = retune(site, raw, raw.replace(anchor, sentence + " " + anchor, 1))
    new_full = full.replace(raw, new_raw, 1)
    assert new_full != full and len(new_full) == len(full), site
    write(path, new_full)
    return path


# --------------------------------------------------------------------------
# R1 -- THE CENSUS, ON DISK, BOTH DIRECTIONS
# --------------------------------------------------------------------------
def r1():
    head("R1 -- G-1: A WRONG FIGURE IN ORDINARY PROSE, ON DISK, BOTH DIRECTIONS")
    print("""mg-835f wrote 'The gap is now +9 999 characters.' into each of the three
sites, in ordinary prose, length-preservingly, leaving the labelled statement
the gate reads correct and untouched -- and THE RUN STAYED AT EXIT 0 EVERY TIME
(its A6 U1 x3).  The same probe is run here against the REAL runner, one site
at a time, every other occurrence of every figure left correct.

Then the file is restored, the restoration is CHECKED by sha256, and the runner
is run AGAIN.  Both directions per probe, because a gate that fires on
everything is worth no more than one that fires on nothing.

  population: the 3 sites x 2 wrong-prose shapes.  +9 999 is a value the roster
  does not carry; +755 IS on the roster (the cell-only gap at bbe83b5), which
  is the probe a SET-membership census would still pass and a MULTISET census
  catches.  Verdicts written before the run.
""")
    print("    THE PREFERRED REPAIR, MEASURED FIRST: is there a prose duplicate")
    print("    to REMOVE?  Live figures and how many times each is written per")
    print("    site, read from the tree:")
    m = measured()
    dup = 0
    for site in ("the STATE.md row", "§14", "H8"):
        raw = site_raw(site)
        toks = V.figure_tokens(raw)
        counts = {k: toks.count(m[k]) for k in V.LIVE_CENSUS[site]}
        over = {k: c for k, c in counts.items()
                if c > V.LIVE_CENSUS[site][k]}
        dup += len(over)
        print(f"      {site:<20} " + "  ".join(f"{k}={c}" for k, c in counts.items())
              + ("" if not over else f"   <-- MORE THAN LICENSED: {over}"))
    print()
    record(dup == 0,
           f"{dup} live figure is written more times than its site licenses, "
           "over 3 sites -- so the ticket's PREFERRED repair (remove the prose "
           "duplicate) has nothing to remove: each live figure already lives in "
           "exactly one place per site.  G-1 is the duplicate the gate would "
           "not SEE if the next correction wrote one.  THE CODE IS WIDENED AND "
           "THE STATED EXTENT IS NOT NARROWED, and this line is the saying-which")

    rc, _ = run_gate()
    record(rc == 0, f"the unmutated tree: the real runner exits {rc} -- the "
                    "baseline every probe below is measured against")

    cases = []
    for site in ("the STATE.md row", "§14", "H8"):
        cases.append((f"N1 {site}: wrong prose figure +9 999 (mg-835f's own U1)",
                      site, "+9 999"))
    for site in ("the STATE.md row", "§14", "H8"):
        cases.append((f"N2 {site}: wrong prose figure +755 -- ALREADY ON THE ROSTER",
                      site, "+755"))

    print()
    print(f"    {'probe':<70}{'predicted':<13}{'observed':<13}{'restored'}")
    fired = restored_silent = 0
    for name, site, value in cases:
        path = prose_at_site(site, value)
        try:
            rc, refuted = run_gate()
        finally:
            restore(path)
        assert sha(path) == CLEAN[path], f"restoration of {path} is not byte-identical"
        rc2, _ = run_gate()
        obs = "GATE FIRES" if rc else "gate passes"
        back = "silent" if rc2 == 0 else "STILL RED"
        fired += 1 if rc else 0
        restored_silent += 1 if rc2 == 0 else 0
        flag = "" if rc else "   <-- PREDICTION MISSED"
        print(f"    {name:<70}{'GATE FIRES':<13}{obs:<13}{back}{flag}")
        if rc:
            hit = [l for l in refuted
                   if heading(l).endswith("FIGURE CENSUS")]
            print(f"        {(hit[0] if hit else refuted[0])[:150]}")
    print()
    record(fired == len(cases),
           f"{fired} of {len(cases)} wrong-prose probes make the REAL runner "
           "red, at 3 of 3 sites and in both shapes.  mg-835f observed 3 of 3 "
           "of these at exit 0 -- G-1 is CLOSED by widening the code")
    record(restored_silent == len(cases),
           f"{restored_silent} of {len(cases)} restorations return the runner to "
           "exit 0, each verified byte-identical by sha256 -- the gate does not "
           "fire on everything, so the fires above are attributable to the prose")


# --------------------------------------------------------------------------
# R2 -- THE SUMMARY-VERSUS-ROWS CHECK, DEMONSTRATED FIRING
# --------------------------------------------------------------------------
PRIMARY_CONFIRMED = "THE PRIMARY TARGET IS CONFIRMED"
SUMMARY_LINE = "SUMMARY vs ROWS"


def primary_rows(out):
    """The [CONFIRMED]/[REFUTED] lines of T1 the bottom line speaks for."""
    keep = ("the three published parts reproduce from the tree",
            "THE REPAIR'S FIGURES DID NOT GO STALE")
    # The mark is required: the bottom line ECHOES these details under the
    # derived sentence, and an echo of a row is not the row.
    return [l.strip() for l in out.split("\n")
            if l.strip().startswith("[") and any(k in l for k in keep)]


def r2():
    head("R2 -- G-2: THE BOTTOM LINE, DERIVED FROM ITS ROWS AND CHECKED")
    print("""mg-835f: the mg-8a5c instrument, re-run at HEAD, printed two [REFUTED] lines
in T1 -- its own declared PRIMARY TARGET -- and then printed, unconditionally,
'THE PRIMARY TARGET IS CONFIRMED'.  A document contradicting itself between its
summary and its data, with the summary being the part that travels.

THE RULE APPLIED, and it is worth carrying beyond this ticket: every time a
summary and its supporting rows have disagreed in this arc, the summary was
wrong and the rows were right.  The summary is written once, early, by whoever
is most invested in the conclusion; the rows are regenerated.  SO THE BOTTOM
LINE IS FIXED TO MATCH T1, NOT T1 TO MATCH THE BOTTOM LINE -- T1's expectations
are the figures `e16e41c` published and this instrument audits `e16e41c`.

Two runs.  Verdicts written before both.
""")
    rc, out = run_8a5c()
    record(rc in (0, 1),
           f"the mg-8a5c instrument ran to completion (exit {rc}; it exits 1 "
           "whenever a FINDING is present, and F-3 and F-4 are still open) -- "
           "any other code is a crash and the two runs below would compare "
           "nothing")
    rows = primary_rows(out)
    ref_rows = [l for l in rows if "[REFUTED" in l]
    summary = [l.strip() for l in out.split("\n") if SUMMARY_LINE in l]
    print(f"    RUN 1 -- as it stands.  exit {rc}")
    for l in rows:
        print(f"      T1 row   {l[:132]}")
    for l in summary:
        print(f"      check    {l[:132]}")
    print()
    record(len(rows) == 2 and len(ref_rows) == 2,
           f"{len(ref_rows)} of {len(rows)} PRIMARY rows read [REFUTED] at this "
           "tree -- a later commit moved the figures mg-8e30 published, which "
           "is a true statement about a tree this audit was never taken against")
    record(PRIMARY_CONFIRMED not in out,
           "and the bottom line NO LONGER prints 'THE PRIMARY TARGET IS "
           "CONFIRMED' while those rows are refuted.  The summary follows the "
           "rows; mg-835f G-2 is CLOSED")
    record(len(summary) == 1 and "[CONFIRMED]" in summary[0],
           "and the SUMMARY vs ROWS check is present and green -- the sentence "
           "printed and the rows it summarises agree")

    print()
    rc_f, out_f = run_8a5c(force="CONFIRMED")
    rows_f = primary_rows(out_f)
    summary_f = [l.strip() for l in out_f.split("\n") if SUMMARY_LINE in l]
    print("    RUN 2 -- THE SAME RUN WITH THE SUMMARY FORCED to the sentence it")
    print(f"    used to print unconditionally.  exit {rc_f}")
    for l in summary_f:
        print(f"      check    {l[:132]}")
    print()
    record(len(summary_f) == 1 and "[REFUTED" in summary_f[0],
           "FORCED TO DISAGREE, THE CHECK FIRES.  This is the demonstration the "
           "ticket requires: a summary-versus-rows check never shown to fire is "
           "the vacuous-check defect this arc has produced three times")
    record(PRIMARY_CONFIRMED in out_f
           and all("[REFUTED" in l for l in rows_f),
           "and the forced run reproduces the EXACT shape mg-835f found -- "
           "'THE PRIMARY TARGET IS CONFIRMED' printed in the same transcript as "
           "its own refuted PRIMARY rows.  It is now reachable only by forcing "
           "it, and forcing it is caught")
    n1 = sum(1 for l in out.split("\n") if "[REFUTED" in l)
    n2 = sum(1 for l in out_f.split("\n") if "[REFUTED" in l)
    record(n2 == n1 + 1,
           f"and the forced run refutes exactly one MORE check than the normal "
           f"run ({n1} -> {n2}) -- the check moves the count, so it is not "
           "decorative")


# --------------------------------------------------------------------------
# R3 -- THE RESIDUE, AND WRITTEN VERSUS REGENERATED
# --------------------------------------------------------------------------
def r3():
    head("R3 -- THE RESIDUE, AND WHICH ARTIFACT IS FROZEN")
    print("""What the census does NOT read, printed rather than left for the next audit
to find.  An extent that is not printed becomes the next claim wider than its
code, which is exactly what G-1 was.
""")
    m = measured()
    total = 0
    for site in ("the STATE.md row", "§14", "H8"):
        raw = site_raw(site)
        want, coll = V.expected_census(site, m)
        toks = V.figure_tokens(raw)
        total += len(toks)
        quoted = len(V.FIGURE_TOKEN.findall(V.flat(raw))) - len(toks)
        print(f"    {site:<20} {len(toks):>3} tokens read, "
              f"{sum(want.values()):>3} licensed, "
              f"{quoted:>2} inside marked quotations and EXEMPT, "
              f"{len(coll)} roster/live collision(s)")
    print()
    record(total > 0,
           f"{total} figure tokens are read across the 3 sites, where the gate "
           "previously read 12 designated statements and nothing else")
    record(None,
           "NOT COVERED, and declared: figures inside MARKED QUOTATIONS (a "
           "quotation of a withdrawn figure is not an assertion of it -- the "
           "convention `assertions()` already ran on); figures OUTSIDE the "
           "section, because a site is a section; and numbers that are not of "
           "this arc's character-count shape (a bare `405`, a ticket id)")
    record(None,
           "THE COST, stated rather than discovered: the census is FAIL-CLOSED. "
           "A legitimately new historical figure at a site makes the run red "
           "until it is entered on the roster with what it is.  That is the "
           "same cost mg-835f reported for U5 (an innocent rewording is a red "
           "run), and it is the direction a locator should fail in")

    print()
    print("    WRITTEN ONCE AND FROZEN, versus REGENERATED TO FOLLOW:")
    frozen = git("diff", "--stat", "main", "--", AUDIT_8A5C_OUT).strip()
    print(f"      {AUDIT_8A5C_OUT}")
    print("        FROZEN -- the mg-8a5c run as TAKEN, at f58f7fd.  Not")
    print("        regenerated by this repair; its verdict is unchanged.")
    print("      code/hodge_leverage_landing_e1d0/out_verify.txt")
    print("        REGENERATED to follow the widened gate -- it gains the")
    print("        census lines and the extent block, and nothing else.")
    print("      code/hodge_leverage_repair_8916/out_repair_8916.txt")
    print("        REGENERATED -- this run.")
    print()
    record(frozen == "",
           f"and `{os.path.basename(AUDIT_8A5C_OUT)}` is byte-identical to "
           "`main`: the frozen artifact is frozen, measured rather than "
           "asserted.  A document left wrong with its evidence bent to agree "
           "presents identically in a diff to a document corrected with its "
           "evidence regenerated to follow -- so which is which is written down")


# --------------------------------------------------------------------------
# R4 -- THE AUDITOR'S OWN INSTRUMENT, UNMODIFIED, AGAINST THE REPAIRED TREE
# --------------------------------------------------------------------------
def r4():
    head("R4 -- mg-835f's OWN INSTRUMENT, UNMODIFIED, RE-RUN")
    print("""The strongest check available, and it costs nothing but time: the instrument
that FOUND G-1 and G-2 is re-run against the repaired tree without a byte of it
being edited.  A repair scored only by its own new instrument is a repair
scored by the party that wrote it.

`code/hodge_leverage_audit_835f/audit_a318_repair.py` is invoked directly
rather than through its runner, so its COMMITTED transcript is not overwritten:
`out_audit_a318.txt` is the run as TAKEN and stays frozen.  It mutates the tree
and restores it under its own `finally` + sha256, and refuses to run against a
dirty one.
""")
    r = subprocess.run([sys.executable, AUDIT_835F], capture_output=True,
                       text=True, cwd=REPO)
    out = r.stdout
    u1 = [l.strip() for l in out.split("\n")
          if "U1 " in l and "ordinary prose at the site" in l and "  " in l.strip()]
    findings = [l.strip() for l in out.split("\n") if "[FINDING" in l]
    print(f"    exit {r.returncode}, findings {len(findings)}")
    for l in u1:
        print(f"      {l[:150]}")
    for l in findings:
        print(f"      {l[:150]}")
    print()
    fires = sum(1 for l in u1 if "GATE FIRES" in l)
    record(len(u1) == 3 and fires == 3,
           f"mg-835f's own U1 probes -- the three it observed at `gate passes` "
           f"and raised G-1 on -- now read GATE FIRES at {fires} of {len(u1)}, "
           "measured by the instrument that raised the finding rather than by "
           "the one that repairs it")
    record(len(findings) == 0 and r.returncode == 0,
           f"and that instrument, unmodified, now reports {len(findings)} "
           f"findings at exit {r.returncode} -- it reported 2 (G-1 and G-2) "
           "against the tree it was taken against.  Its predictions are LEFT AS "
           "WRITTEN and now read `PREDICTION MISSED`, which is the correct "
           "record of a gate that got wider after the prediction was made")
    record(sha(AUDIT_835F_OUT) == CLEAN[AUDIT_835F_OUT],
           "and its COMMITTED transcript is untouched by this run, sha256-"
           "verified -- the frozen artifact stays the run as taken")


# --------------------------------------------------------------------------
def main():
    print("mg-8916 -- THE mg-835f REPAIR, MEASURED IN BOTH DIRECTIONS")
    print("=" * 78)
    print("""Predicted exit code, written before the first run: 0.

G-1 is closed by WIDENING THE CODE and G-2 by DERIVING THE SUMMARY FROM ITS
ROWS.  Nothing below re-opens the mg-a318 primary target, which held: 12 of 12
reader-facing figures corrupted on disk make the run red and 12 of 12
restorations make it green again.  0 mathematical statements are touched.""")

    dirty = [l[3:] for l in git("status", "--porcelain").split("\n")
             if l[3:] in REQUIRE_CLEAN]
    if dirty:
        raise SystemExit(f"refusing to run against a dirty tree: {dirty}.  This "
                         f"instrument and the mg-8a5c one it invokes both "
                         f"restore by `git checkout --`, which would destroy "
                         f"uncommitted edits to these files.")
    for p in MUTABLE + [AUDIT_835F_OUT]:
        CLEAN[p] = sha(p)

    try:
        r1()
        r2()
        r3()
        r4()
    finally:
        restore(*MUTABLE)

    head("BOTTOM LINE")
    # ⚠️ THIS SENTENCE IS DERIVED FROM THE ROWS ABOVE, which is the whole of
    # G-2.  There is no branch here that can assert a verdict the rows refute.
    bad = [t for t, ok in RESULTS if ok is False]
    print(f"  checks recorded : {len(RESULTS)}")
    print(f"  confirmed       : {sum(1 for _, ok in RESULTS if ok is True)}")
    print(f"  measurements    : {sum(1 for _, ok in RESULTS if ok is None)}")
    print(f"  refuted         : {len(bad)}")
    print()
    if bad:
        print("  REFUTED -- a claim this repair makes did not hold, and the")
        print("  prose must not be written:")
        for t in bad:
            print(f"    - {t[:150]}")
        return 1
    print("  BOTH OPEN SITES ARE CLOSED, AND BOTH ARE MEASURED IN BOTH")
    print("  DIRECTIONS.  G-1: the wrong prose figure that was invisible at 3")
    print("  of 3 sites now makes the real runner red at 3 of 3, in two shapes,")
    print("  and every restoration returns it to green.  G-2: the bottom line")
    print("  is derived from its PRIMARY rows, and the check that they agree is")
    print("  shown FIRING when they are forced apart.  AND mg-835f's OWN")
    print("  INSTRUMENT AGREES: unmodified, it now reports 0 findings at exit 0,")
    print("  with its three U1 rows reading GATE FIRES.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
