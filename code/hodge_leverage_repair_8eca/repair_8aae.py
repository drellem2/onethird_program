#!/usr/bin/env python3
"""mg-8eca -- THE mg-8aae REPAIR, MEASURED ON THE ARTIFACT RATHER THAN A HOOK.

mg-8aae audited the mg-8916 repair and returned PARTIAL.  What held is not
re-opened here: mg-835f's 12 of 12 survives the widening AT ROW GRANULARITY,
and G-1 is closed against wording that audit chose.  Two things were open, and
mg-8aae's own closing note says they are one question in two costumes:

  H-1  THE CENSUS IS A MULTISET, SO EXCHANGING TWO DECLARED FIGURES IS SILENT.
       A transposition preserves a multiset exactly, so the property the gate
       measured was INVARIANT UNDER THE FAILURE IT GUARDED.  Two declared
       figures of equal length exchanged in ordinary prose left the runner at
       exit 0 at 2 of 2 sites, with H8's own table then saying the `STATE.md`
       row SHRANK across mg-a2bd and the chain F-1 was born in running
       backwards.

  H-2  `SUMMARY vs ROWS` WAS `x == x`.  It scored `printed == derived` where
       `printed = FORCE_SUMMARY or derived`, so off the forcing hook it could
       not fail for any tree.  It was demonstrated firing, and the
       demonstration went through a hook built to make it fire.

THE TWO QUESTIONS THIS INSTRUMENT IS ORGANISED AROUND, because they are
mg-8aae's and they are the whole finding:

  (1) IS THE MEASURED PROPERTY INVARIANT UNDER THE GUARDED FAILURE?  A multiset
      is invariant under exchange; `x == x` is invariant under everything.
      Neither is fixed by checking MORE things -- both are fixed by changing
      WHAT IS MEASURED.  R1 and R2 each show the new property MOVING under the
      exact failure that left the old one still.

  (2) IS THE DEMONSTRATION AT THE RIGHT TARGET?  DEMONSTRATING A CHECK FIRES
      VIA A TEST HOOK PROVES THE HOOK WORKS, NOT THE CHECK.  So R2's headline
      direction sets NO environment variable: it edits the artifact by hand,
      the way G-2 was actually made, and reads the transcript.  The hook is
      kept and still exercised, but it is no longer what the claim rests on.

  R1  THE CENSUS, POSITION-AWARE, ON DISK, IN BOTH POSITIONAL SENSES.  Four
      exchanges of two DECLARED figures -- mg-8aae's own two, verbatim, plus
      one more per site exchanged the other way round -- written to disk
      length-preservingly and run through the REAL runner.  Each is ASSERTED to
      be a permutation and nothing else before it is scored: same multiset,
      same designated reads, same length.  The requirement is stricter than
      "the run goes red": the row that fails must be the `FIGURE ORDER` row FOR
      THAT SITE, because a widening that made the run red for a new reason
      while the positional check stayed quiet would keep the headline and lose
      the result.  Every restoration is checked by sha256 and the runner is run
      AGAIN -- a gate that fires on everything is worth no more than one that
      fires on nothing.

  R2  `SUMMARY vs ROWS`, FIRED ON THE REAL ARTIFACT WITH NO HOOK SET.  Five
      directions.  D0: as it stands, green.  D1: the mg-8916 forcing hook,
      kept, still red, count still moving by exactly one -- nothing mg-8916
      demonstrated is dropped.  D2: THE HEADLINE, EDITED BY HAND ON DISK, no
      environment variable -- mg-8aae's own direction-2 mutation, verbatim,
      which the old check passed.  D3: the COUNT edited and the verdict word
      left correct, so the second read is shown to be load-bearing on its own.
      D4: THE DEFECT REINSTATED -- `printed = FORCE_SUMMARY or derived` put
      back, with D2's edit also applied, and the check must go GREEN again.
      D4 is what makes D2 attributable: without it, "the check fires" and "the
      instrument fires" are the same sentence.

  R3  THE TWO INSTRUMENTS THIS REPAIR ANSWERS TO, UNMODIFIED, RE-RUN AGAINST
      THE REPAIRED TREE.  A repair scored only by its author's instrument is
      scored by the author.  mg-8aae's A4 predicted `gate SILENT` at 2 of 2 and
      its A5 predicted the check would not catch direction 2; both predictions
      are now MISSED, which is what a landed finding looks like from the
      raising instrument's side.  And mg-8916's own instrument must still
      report 18 checks / 0 refuted at exit 0, because a repair that quietly
      drops what the last one demonstrated is a narrowing wearing a widening's
      name.  Neither committed transcript is overwritten, both are
      sha256-checked after -- and the SEAM that leaves is DECLARED.

  R4  WHAT IS STILL NOT COVERED, printed rather than left for the next audit.
      An extent that is not printed becomes the next claim wider than its code,
      which is the defect this whole arc keeps paying for.

PREDICTED EXIT CODE, WRITTEN BEFORE THE FIRST RUN: 0.  Every probe's verdict is
written before it runs and any disagreement is a refutation.

IT MUTATES THE TREE AND RESTORES IT.  R1 writes to `STATE.md`, the deliverable
and the row-history file; R2 writes to `audit_repair_8e30.py`.  Each is
`git checkout --`ed back inside a `finally`, every restoration is CHECKED by
sha256 rather than asserted, and it REFUSES TO RUN against a tree in which any
of them is dirty -- a checkout over an uncommitted edit destroys it.

REPRODUCTION CONTRACT, stated in terms of the FILES READ rather than a commit.
This transcript regenerates byte-identically for any tree in which `STATE.md`,
`docs/OneThird-Hodge-Side-Leverage.md`, `docs/state-history/attempt-mg-a3d4.md`,
`code/hodge_leverage_landing_e1d0/`, `code/hodge_leverage_audit_8a5c/` and
`code/hodge_leverage_audit_8aae/` are unchanged.  It embeds no sha of its own.

Pure Python 3 + git.  No third-party packages.  Runtime ~5 min, almost all of
it the 9 runs of the audited runner, the 6 runs of the mg-8a5c instrument and
the runs of mg-8aae's and mg-8916's own instruments in R3.
"""

import hashlib
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LANDING = os.path.join(REPO, "code/hodge_leverage_landing_e1d0")
sys.path.insert(0, LANDING)
import verify_landing as V                              # noqa: E402  the REPAIRED module

RUNNER = os.path.join(LANDING, "verify_landing.py")
AUDIT_8A5C = "code/hodge_leverage_audit_8a5c/audit_repair_8e30.py"
AUDIT_8AAE = "code/hodge_leverage_audit_8aae/audit_8916_repair.py"
AUDIT_8AAE_OUT = "code/hodge_leverage_audit_8aae/out_audit_8916.txt"
REPAIR_8916 = "code/hodge_leverage_repair_8916/repair_835f.py"
REPAIR_8916_OUT = "code/hodge_leverage_repair_8916/out_repair_8916.txt"

MUTABLE = [V.STATE, V.DELIV, V.HIST, AUDIT_8A5C]
# Not mutated here, but mg-8aae's instrument (R3) and the mg-8a5c instrument
# both `git checkout --` it and refuse to run if it is dirty.  Checked here so
# that a dirty tree is a REFUSAL with a reason rather than a crash inside R3.
REQUIRE_CLEAN = MUTABLE + ["code/hodge_leverage_landing_e1d0/out_verify.txt"]

RESULTS = []
CLEAN = {}


# --------------------------------------------------------------------------
# plumbing
# --------------------------------------------------------------------------
def record(ok, detail, tag=None):
    """`tag` marks the rows a BOTTOM LINE sentence speaks FOR.  Without it the
    bottom line can only be written by hand, and a hand-written summary beside
    regenerated rows is mg-835f's G-2 -- which mg-8916 repaired with a check
    that was `x == x`, which is mg-8aae's H-2, which is what this instrument
    exists to land.  It would be a poor landing that reproduced the shape."""
    RESULTS.append((detail, ok, tag))
    mark = {True: "[CONFIRMED]", False: "[REFUTED  ]", None: "[MEASURED ]"}[ok]
    print(f"  {mark} {detail}")


def tagged(tag):
    return [(d, ok) for d, ok, t in RESULTS if t == tag]


def head(title):
    print()
    print(title)
    print("-" * len(title))


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True, check=True).stdout


def sha(path):
    with open(os.path.join(REPO, path), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def read(path):
    with open(os.path.join(REPO, path), encoding="utf-8") as fh:
        return fh.read()


def write(path, text):
    with open(os.path.join(REPO, path), "w", encoding="utf-8") as fh:
        fh.write(text)


def restore(*paths):
    subprocess.run(["git", "-C", REPO, "checkout", "--"] + list(paths), check=True)


def run_runner():
    """The REAL runner against whatever is on disk.  (exit, [refuted rows])."""
    r = subprocess.run([sys.executable, RUNNER], capture_output=True,
                       text=True, cwd=REPO)
    return r.returncode, [l.strip() for l in r.stdout.split("\n")
                          if l.strip().startswith("[REFUTED  ]")]


def run_8a5c(force=None):
    """The mg-8a5c audit instrument against whatever is on disk."""
    env = dict(os.environ)
    env.pop("MG8916_FORCE_SUMMARY", None)
    if force:
        env["MG8916_FORCE_SUMMARY"] = force
    r = subprocess.run([sys.executable, os.path.join(REPO, AUDIT_8A5C)],
                       capture_output=True, text=True, cwd=REPO, env=env)
    return r.returncode, r.stdout


def parse_8a5c(out):
    """(the SUMMARY vs ROWS row, the refuted count, the printed headlines)."""
    lines = out.split("\n")
    row = next((l.strip() for l in lines if "SUMMARY vs ROWS" in l
                and l.strip().startswith("[")), None)
    ref = None
    for l in lines:
        m = re.match(r"\s*refuted\s*:\s*(\d+)", l)
        if m:
            ref = int(m.group(1))
    headline = [l.strip() for l in lines
                if l.strip().startswith("THE PRIMARY TARGET IS")]
    return row, ref, headline


# --------------------------------------------------------------------------
# the sites, and writing a mutated section back into its file
# --------------------------------------------------------------------------
SITE_FILE = {"the STATE.md row": V.STATE, "§14": V.DELIV, "H8": V.HIST}


def site_raw(site, full=None):
    full = V.tree(SITE_FILE[site]) if full is None else full
    if site == "the STATE.md row":
        return V.state_row(full)
    if site == "§14":
        return V.section(full, "## §14 — `STATE.md` row, as landed")
    return V.section(full, "### H8 — ")


def put_site(site, new_raw):
    """Write `new_raw` back over the site, length-preservingly."""
    path = SITE_FILE[site]
    full = V.tree(path)
    raw = site_raw(site, full)
    assert len(new_raw) == len(raw), (site, len(new_raw) - len(raw))
    assert full.count(raw) == 1, site
    write(path, full.replace(raw, new_raw, 1))
    return path


def measured():
    a = len(V.state_row(V.tree(V.STATE)))
    b = len(V.deliv_row(V.tree(V.DELIV)))
    h = len(V.tree(V.HIST))
    return {"gap": V.doc_num(a - b, signed=True),
            "both": V.doc_num(a + h - b, signed=True),
            "cell": V.doc_num(a), "hist": V.doc_num(h), "copy": V.doc_num(b)}


# --------------------------------------------------------------------------
# R1 -- THE CENSUS IS POSITION-AWARE, ON DISK, IN BOTH POSITIONAL SENSES
# --------------------------------------------------------------------------
# The first of each pair is mg-8aae's own probe, verbatim -- the mutation that
# raised H-1 and left the runner at exit 0.  The second exchanges a DIFFERENT,
# DISJOINT pair at the same site in the other positional sense: an earlier pair
# of the chain rather than its last two, and a later-column value moved earlier
# rather than an earlier one moved later.  A transposition is its own inverse,
# so "both orderings" of ONE pair is one text; two disjoint pairs per site is
# what makes the demonstration not a single accident per site.
CHAIN = "2 928 → 6 069 → −875 → +755"
H8_TABLE = ("STATE.md row  before mg-a2bd :  13 551 chars\n"
            "    STATE.md row  after  mg-a2bd :  16 692 chars")
H8_HIST_ROW = ("this file (the relocated history)                   "
               "10 483        16 268")

EXCHANGES = [
    ("H8", "mg-8aae's own probe: the mg-a2bd table's before/after",
     H8_TABLE,
     H8_TABLE.replace("13 551", "\0").replace("16 692", "13 551")
             .replace("\0", "16 692"),
     "H8's own table now says the STATE.md row SHRANK across mg-a2bd, against "
     "the (+3 141) printed on the same line"),
    ("H8", "the other sense: the row-history line's two historical columns",
     H8_HIST_ROW,
     H8_HIST_ROW.replace("10 483        16 268", "16 268        10 483"),
     "the three-column table now says this file SHRANK from bbe83b5^ to "
     "bbe83b5, in the row whose growth is the reason the gap moved"),
    ("the STATE.md row", "mg-8aae's own probe: the chain's LAST two terms",
     CHAIN, "2 928 → 6 069 → +755 → −875",
     "the chain F-1 was born in now asserts the gap reached +755 BEFORE it "
     "went negative"),
    ("the STATE.md row", "the other sense: the chain's FIRST two terms",
     CHAIN, "6 069 → 2 928 → −875 → +755",
     "the same chain now says the clause mismatch SHRANK, in the sentence "
     "that ends 'while the clause mismatch only ever grew'"),
]


def r1():
    head("R1 -- THE CENSUS IS POSITION-AWARE: EXCHANGES, ON DISK, BOTH SENSES")
    print("""H-1's mechanism in one line: A MULTISET IS INVARIANT UNDER A TRANSPOSITION,
so the census could not see one.  The repair does not check MORE things -- it
changes WHAT IS MEASURED.  The roster in `verify_landing.py` is now an ORDERED
list of slots and the census compares the SEQUENCE as well as the bag, with the
bag and `LIVE_CENSUS` DERIVED from the same list so the two cannot drift.

  Each probe below exchanges two DECLARED figures of equal length, in ordinary
  prose, inside the section, outside any marked quotation.  That it is a
  PERMUTATION AND NOTHING ELSE is asserted before it is written: identical
  multiset, identical designated reads, identical length.  A probe that also
  moved the bag would be re-measuring the census that already existed.

  Predicted, before the run: GATE FIRES at 4 of 4, the failing row is the
  FIGURE ORDER row FOR THAT SITE, and 4 of 4 restorations return exit 0.
""")
    m = measured()
    print(f"    {'probe':<68}{'predicted':<12}{'observed':<12}{'restored'}")
    fired = at_row = back = 0
    for site, what, before, after, why in EXCHANGES:
        raw = site_raw(site)
        assert raw.count(before) == 1, (site, before)
        new_raw = raw.replace(before, after, 1)
        # The mutation is a permutation and nothing else -- asserted, not hoped.
        reader = dict((n, r) for n, r, _k in V.SITES)[site]
        record(len(new_raw) == len(raw)
               and V.figure_tokens(new_raw) == V.figure_tokens(raw)
               and reader(new_raw) == reader(raw),
               f"{site} / {what}: the mutation is a PERMUTATION and nothing "
               f"else -- the MULTISET of {len(V.figure_tokens(raw))} figure "
               "tokens is identical before and after, every designated "
               "statement reads the same value, and the length is unchanged")
        path = put_site(site, new_raw)
        try:
            rc, refuted = run_runner()
        finally:
            restore(path)
        assert sha(path) == CLEAN[path], f"restoration of {path} not identical"
        rc2, _ = run_runner()
        want_row = f"GATE @ {site}: FIGURE ORDER"
        only_order = len(refuted) == 1 and want_row in refuted[0]
        fired += 1 if rc != 0 else 0
        at_row += 1 if only_order else 0
        back += 1 if rc2 == 0 else 0
        print(f"    {site + ': ' + what:<68}"
              f"{'GATE FIRES':<12}"
              f"{('GATE FIRES' if rc else 'gate passes'):<12}"
              f"{'green' if rc2 == 0 else 'STILL RED'}"
              f"{'' if rc else '   <-- PREDICTION MISSED'}")
        print(f"        rows that failed: {len(refuted)}; the first of them: "
              f"{(refuted[0][12:110] if refuted else '(none -- the run was green)')}")
        print(f"        what a reader would have read: {why}")
    print()
    record(fired == len(EXCHANGES),
           f"{fired} of {len(EXCHANGES)} exchanges make the REAL runner red, "
           "where the multiset census left it at exit 0.  The property the "
           "gate measures is no longer invariant under the failure it guards",
           "H-1")
    record(at_row == len(EXCHANGES),
           f"and at {at_row} of {len(EXCHANGES)}, the row that failed is the "
           "`FIGURE ORDER` row FOR THAT SITE and it is the ONLY row that "
           "failed -- the fire is attributable to the positional check, not "
           "to some other row of a widened gate going red for a new reason",
           "H-1")
    record(back == len(EXCHANGES),
           f"and {back} of {len(EXCHANGES)} restorations return the runner to "
           "exit 0, sha256-verified: the gate does not fire on everything",
           "H-1")


# --------------------------------------------------------------------------
# R2 -- `SUMMARY vs ROWS`, FIRED ON THE REAL ARTIFACT WITH NO HOOK SET
# --------------------------------------------------------------------------
# mg-8aae's direction-2 mutation, VERBATIM: the REFUTED branch's own headline
# edited from the derived f-string to a hand-written literal.  This is the
# shape G-2 actually had -- a sentence somebody wrote -- and the old check
# passed it.
HEADLINE_OLD = 'f"  THE PRIMARY TARGET IS {verdict} IN THIS TREE: "'
HEADLINE_NEW = 'f"  THE PRIMARY TARGET IS CONFIRMED IN THIS TREE: "'
# The COUNT half alone: the verdict word left correct and only the
# parenthetical moved, so the second of the two independent reads is shown to
# carry weight by itself rather than riding on the first.
COUNT_OLD = 'f"{len(bad)} of {len(rows)} rows tagged",'
COUNT_NEW = 'f"{len(bad) + 1} of {len(rows)} rows tagged",'
# The DEFECT ITSELF, reinstated: the two lines mg-8aae quoted.
VACUOUS_OLD = "    printed = printed_summary_verdict(summary)\n" \
              "    said = printed_summary_count(summary)\n"
VACUOUS_NEW = "    printed = FORCE_SUMMARY or derived\n" \
              "    said = printed_summary_count(summary)\n"


def edit_8a5c(*pairs):
    """Apply hand-edits to the mg-8a5c instrument ON DISK and run it."""
    src = read(AUDIT_8A5C)
    for old, new in pairs:
        assert src.count(old) == 1, (old, src.count(old))
        src = src.replace(old, new, 1)
    write(AUDIT_8A5C, src)
    try:
        return run_8a5c()
    finally:
        restore(AUDIT_8A5C)


def r2():
    head("R2 -- `SUMMARY vs ROWS`: FIRED ON THE ARTIFACT, WITH NO HOOK SET")
    print("""H-2's mechanism in one line: the check scored `printed == derived` where
`printed = FORCE_SUMMARY or derived`, so off the hook it was `x == x` AND
COULD NOT FAIL FOR ANY TREE.  The repair does not add checks -- it makes the
two sides INDEPENDENTLY OBTAINED.  The printed verdict and its count are parsed
back out of the lines the run will print; the rows' verdict and count are
recomputed from the rows.

  D2 IS THE ONE THAT MATTERS, and it sets no environment variable: it is
  mg-8aae's own direction-2 edit, applied to the real file, with the transcript
  read afterwards.  DEMONSTRATING A CHECK FIRES VIA A TEST HOOK PROVES THE HOOK
  WORKS, NOT THE CHECK -- so D1 is kept because mg-8916 demonstrated it and
  nothing is silently dropped, but it is not what the claim rests on.

  D4 is the control that makes D2 mean something: the DEFECT IS REINSTATED
  under D2's edit and the check must go GREEN AGAIN.  Without it, "the check
  fires" and "the instrument fires" are the same sentence.

  Predicted, before the run: D0 green; D1 red, count +1; D2 RED, count +1;
  D3 RED, count +1; D4 GREEN, count back to D0's.
""")
    # ---- D0: the artifact as it stands.
    rc0, out0 = run_8a5c()
    row0, ref0, head0 = parse_8a5c(out0)
    print(f"    D0  as it stands                      "
          f"{(row0[:11] if row0 else 'ABSENT'):<13} refuted {ref0}  exit {rc0}")
    record(bool(row0) and row0.startswith("[CONFIRMED]"),
           "D0: the `SUMMARY vs ROWS` check EXISTS, is recorded as a check, "
           "and is GREEN on the artifact as it stands -- so a red below is a "
           "discrimination and not a check that fires on everything")

    # ---- D1: the mg-8916 forcing hook, kept.
    rc1, out1 = run_8a5c("CONFIRMED")
    row1, ref1, _ = parse_8a5c(out1)
    print(f"    D1  the mg-8916 forcing hook          "
          f"{(row1[:11] if row1 else 'ABSENT'):<13} refuted {ref1}  exit {rc1}")
    record(bool(row1) and row1.startswith("[REFUTED") and ref1 == ref0 + 1,
           f"D1: the mg-8916 hook still fires and still moves the refuted "
           f"count by exactly one ({ref0} -> {ref1}).  Nothing mg-8916 "
           "demonstrated is dropped by this repair; what changes is that it "
           "is no longer the ONLY way to make this check red")

    # ---- D2: the artifact, edited by hand.  No environment variable.
    rc2, out2 = edit_8a5c((HEADLINE_OLD, HEADLINE_NEW))
    assert sha(AUDIT_8A5C) == CLEAN[AUDIT_8A5C]
    row2, ref2, head2 = parse_8a5c(out2)
    says_confirmed = any("THE PRIMARY TARGET IS CONFIRMED" in l for l in head2)
    print(f"    D2  the HEADLINE edited on disk       "
          f"{(row2[:11] if row2 else 'ABSENT'):<13} refuted {ref2}  exit {rc2}")
    print(f"        the transcript prints : "
          f"{(head2[0][:66] if head2 else '(none)')}")
    print(f"        while its PRIMARY rows: REFUTED")
    record(says_confirmed,
           "D2: G-2's exact artifact is REPRODUCED with no environment "
           "variable set -- the transcript prints 'THE PRIMARY TARGET IS "
           "CONFIRMED' above its own [REFUTED] PRIMARY rows")
    record(bool(row2) and row2.startswith("[REFUTED") and ref2 == ref0 + 1,
           f"D2: AND THE CHECK CATCHES IT, on the REAL artifact, off no hook "
           f"({ref0} -> {ref2}, exactly one).  This is mg-8aae's own "
           "direction-2 mutation, verbatim, which the old check passed at "
           "[CONFIRMED] with the count unmoved",
           "H-2")

    # ---- D3: the count alone, verdict word left correct.
    rc3, out3 = edit_8a5c((COUNT_OLD, COUNT_NEW))
    assert sha(AUDIT_8A5C) == CLEAN[AUDIT_8A5C]
    row3, ref3, _ = parse_8a5c(out3)
    print(f"    D3  the COUNT edited, verdict correct "
          f"{(row3[:11] if row3 else 'ABSENT'):<13} refuted {ref3}  exit {rc3}")
    record(bool(row3) and row3.startswith("[REFUTED") and ref3 == ref0 + 1,
           f"D3: with the verdict word LEFT CORRECT and only the "
           f"parenthetical count moved, the check still fires ({ref0} -> "
           f"{ref3}).  The second of the two independent reads carries weight "
           "on its own -- it is not decoration on the first")

    # ---- D4: the defect reinstated.  D2's edit must stop being caught.
    rc4, out4 = edit_8a5c((HEADLINE_OLD, HEADLINE_NEW),
                          (VACUOUS_OLD, VACUOUS_NEW))
    assert sha(AUDIT_8A5C) == CLEAN[AUDIT_8A5C]
    row4, ref4, head4 = parse_8a5c(out4)
    still = any("THE PRIMARY TARGET IS CONFIRMED" in l for l in head4)
    print(f"    D4  the DEFECT reinstated, under D2   "
          f"{(row4[:11] if row4 else 'ABSENT'):<13} refuted {ref4}  exit {rc4}")
    record(still and bool(row4) and row4.startswith("[CONFIRMED]")
           and ref4 == ref0,
           f"D4: THE DELETION TEST.  With `printed = FORCE_SUMMARY or derived` "
           f"put back and D2's edit still applied, the same artifact goes "
           f"UNCAUGHT again -- [CONFIRMED], count back to {ref4}.  So D2's red "
           "is attributable to the two-line change and to nothing else, and "
           "the old check really was invariant under the failure it guarded",
           "H-2")

    # ---- and the mechanism, read off the source rather than argued.  The
    # match is anchored to the CODE LINE, indentation and all: the repaired
    # file quotes the removed line in its own ⚠️ block and in its docstring, and
    # a check that cannot tell the defect from the note recording its removal
    # would go red on an honest repair and green on a silent revert.
    src = read(AUDIT_8A5C)
    record("\n    printed = FORCE_SUMMARY or derived\n" not in src
           and "\n    printed = printed_summary_verdict(summary)\n" in src,
           "and the mechanism is read off the source rather than argued: "
           "`printed = FORCE_SUMMARY or derived` is GONE from the code and "
           "`printed` is now parsed from the printed lines.  `FORCE_SUMMARY` "
           "still exists and still reaches the SENTENCE, which is why D1 "
           "still fires -- it no longer reaches the CHECK's left-hand side",
           "H-2")
    # Provenance as a COUNT, with NEITHER SHA NOR SUBJECT printed.  One of the
    # two commits is this instrument's own, so printing its sha would make the
    # reproduction contract above false the moment the transcript is committed
    # (mg-f922 finding E) -- and printing its SUBJECT would do the same the
    # first time this branch is squashed or reworded.  The count is a fact
    # about the history; the transcript stays a fact about the tree.
    touched = [l for l in git("log", "-G",
                              r"^    printed = FORCE_SUMMARY or derived$",
                              "--format=%H", "--", AUDIT_8A5C).split("\n")
               if l.strip()]
    record(len(touched) == 2,
           f"and the defect was really there to remove: `git log -G` on that "
           f"exact code line returns {len(touched)} commit(s) for this file -- "
           "the one that introduced it and the one that removed it.  Neither "
           "sha nor subject is printed: one of the two is this run's own "
           "commit, and a transcript that names it stops regenerating the "
           "first time the branch is squashed or reworded")


# --------------------------------------------------------------------------
# R3 -- mg-8aae's OWN INSTRUMENT, UNMODIFIED, RE-RUN
# --------------------------------------------------------------------------
def r3():
    head("R3 -- THE TWO INSTRUMENTS THIS ANSWERS TO, UNMODIFIED, RE-RUN")
    print("""A repair scored only by the instrument its author wrote is a repair scored
by its author.  So mg-8aae's instrument is re-run here -- not quoted from its
transcript -- and its committed transcript is sha256-checked afterwards.  So is
mg-8916's, because a repair that quietly drops what the last one demonstrated
is a narrowing wearing a widening's name.

  What a LANDED finding looks like from the raising instrument's side is a
  MISSED PREDICTION: A4 predicted `gate SILENT` at 2 of 2 and A5 predicted its
  direction-2 mutation would go uncaught.  Both should now be wrong, and the
  instrument should say so in its own words rather than in ours.

  Predicted, before the run: A4's two permutation rows read GATE FIRES; A5's
  direction-2 row reports the check catching it; H-1 and H-2 are no longer
  raised as findings.
""")
    record(git("diff", "--stat", "HEAD~1", "HEAD", "--", AUDIT_8AAE).strip() == "",
           f"`{AUDIT_8AAE}` is untouched by this repair -- the instrument that "
           "RAISED H-1 and H-2 was not edited by the commit that answers them")
    before = sha(AUDIT_8AAE_OUT)
    r = subprocess.run([sys.executable, os.path.join(REPO, AUDIT_8AAE)],
                       capture_output=True, text=True, cwd=REPO)
    out = r.stdout
    perm = [l for l in out.split("\n")
            if "two declared figures exchanged" in l]
    fires = sum(1 for l in perm if "GATE FIRES" in l)
    findings = [l.strip() for l in out.split("\n")
                if l.strip().startswith("[FINDING")]
    raised = {t for t in ("H-1", "H-2") if any(t in l for l in findings)}
    print(f"      its A4 permutation rows : {fires} of {len(perm)} read GATE FIRES")
    print(f"      its findings            : {len(findings)}"
          + (f" -- {sorted(raised)}" if raised else ""))
    print(f"      its exit                : {r.returncode}")
    record(fires == 2 and len(perm) == 2,
           f"{fires} of 2 of its A4 permutation probes now read GATE FIRES "
           "where it observed exit 0 at 2 of 2 -- measured by re-running its "
           "instrument, not by quoting ours")
    record(not raised,
           f"and neither H-1 nor H-2 is raised as a finding by the instrument "
           f"that raised them ({len(findings)} finding(s) remain)"
           if not raised else
           f"and it STILL raises {sorted(raised)}: the repair does not close "
           "what mg-8aae found")
    record(sha(AUDIT_8AAE_OUT) == before,
           "and its committed transcript is sha256-identical afterwards: the "
           "run as TAKEN is not overwritten to agree with this repair")

    # ---- and mg-8916's own repair instrument, likewise unmodified.  The
    # claim "nothing mg-8916 demonstrated is dropped" is measured here rather
    # than argued from the fact that D1 still fires.
    print()
    before8916 = sha(REPAIR_8916_OUT)
    r = subprocess.run([sys.executable, os.path.join(REPO, REPAIR_8916)],
                       capture_output=True, text=True, cwd=REPO)
    got = {}
    for l in r.stdout.split("\n"):
        m = re.match(r"\s*(checks recorded|confirmed|measurements|refuted)"
                     r"\s*:\s*(\d+)", l)
        if m:
            got[m.group(1)] = int(m.group(2))
    print(f"      mg-8916's own instrument: {got}  exit {r.returncode}")
    record(got.get("checks recorded") == 18 and got.get("refuted") == 0
           and r.returncode == 0,
           f"and mg-8916's own `repair_835f.py`, unmodified, still reports "
           f"{got.get('checks recorded')} checks / {got.get('refuted')} "
           f"refuted at exit {r.returncode} against the REPAIRED tree -- "
           "nothing it demonstrated is dropped, its `MG8916_FORCE_SUMMARY` "
           "demonstration included")

    # ---- and the seam this repair creates, DECLARED rather than left to be
    # found.  mg-8aae's A7 checks mg-8916's document against mg-8916's
    # transcript by looking for an ECHO of the mg-8a5c check's message text --
    # and that message text is one of the two things this repair changed.  The
    # transcript is therefore LEFT AS TAKEN, which is also what it is: the run
    # mg-8916 made, at the tree it made it on.
    echoed = "sentence says CONFIRMED and its 2 PRIMARY rows say REFUTED"
    record(sha(REPAIR_8916_OUT) == before8916
           and echoed in read(REPAIR_8916_OUT),
           "and mg-8916's committed transcript is untouched by this run and "
           "still carries the line mg-8aae's A7 looks for.  DECLARED, because "
           "it is a seam: A7's needle is an ECHO of the mg-8a5c check's "
           "message text, and this repair changed that text.  Regenerating "
           f"`{REPAIR_8916_OUT}` would silently break A7 -- so it is left as "
           "TAKEN, which is what a frozen run is, and anyone who regenerates "
           "it must move A7's needle in the same commit")


# --------------------------------------------------------------------------
# R4 -- WHAT IS STILL NOT COVERED
# --------------------------------------------------------------------------
def r4():
    head("R4 -- WHAT IS STILL NOT COVERED, PRINTED")
    print("""An extent that is not printed becomes the next claim wider than its code.
Both of mg-8aae's findings were exactly that, one generation apart, so this
list is part of the repair rather than an afterthought.

  THE CENSUS, after this repair, covers: every figure-shaped token the section
  asserts, at the value it should have AND in the slot a reader meets it in.
  It does NOT cover:

    * two occurrences of the SAME token exchanged with each other.  This is
      not an omission that can be closed: the sequence is over VALUES, and
      exchanging equal values is the identity map on the artifact as well as
      on the measurement.  There is nothing there to see.
    * a figure outside the section, or inside a marked quotation, or not of
      the figure-shaped class.  Unchanged from mg-8916, and unchanged
      deliberately: `assertions()` states the quotation convention and a site
      is a section.
    * WHAT a figure means.  The roster says `10 483` is "this file at
      bbe83b5^"; nothing checks that sentence against git.  A roster entry
      whose PROSE is wrong is invisible here.

  `SUMMARY vs ROWS`, after this repair, compares the printed verdict AND its
  count against the rows, both sides obtained independently.  It does NOT
  cover:

    * the REST of the branch text, which is still hand-written prose asserting
      things the rows do not carry ("the repair's three figures are the
      POST-commit ones and reproduce exactly from the tree").  The verdict
      sentence is checked; the paragraph around it is not.  mg-8aae named
      this and it is named again here rather than quietly counted as closed.
    * any row not tagged PRIMARY.  The bottom line speaks for the PRIMARY
      rows and the check is scoped to exactly those.
""")
    record(None,
           "the two exclusions that matter are stated above rather than left "
           "to be found: an exchange of EQUAL tokens (which is the identity "
           "map and cannot be seen), and the branch's surrounding prose "
           "(which is hand-written and unchecked).  NOT findings -- declared "
           "extent")


# --------------------------------------------------------------------------
# THE BOTTOM LINE, DERIVED FROM ITS ROWS -- AND CHECKED THE WAY THIS REPAIR
# ASKS THE mg-8a5c INSTRUMENT TO BE CHECKED
#
# This instrument lands H-2, whose content is that a summary-versus-rows check
# comparing a value with itself is not a check.  So its own bottom line is
# derived from the rows tagged `H-1` and `H-2`, and the agreement is scored by
# READING THE VERDICT BACK OUT OF THE LINES ABOUT TO BE PRINTED -- the same
# repair, applied here, rather than asserted about somebody else's file.
# --------------------------------------------------------------------------
CLOSING = {
    "H-1": ("BY CHANGING WHAT THE CENSUS MEASURES: the roster is an ORDERED",
            "list of slots, the multiset and LIVE_CENSUS are derived from it,",
            "and the four exchanges make the REAL runner red ON DISK at the",
            "FIGURE ORDER row for that site -- the mutation a multiset cannot",
            "see, because a transposition preserves it exactly."),
    "H-2": ("BY CHANGING WHERE THE CHECK READS FROM: the printed verdict and",
            "its count are parsed back out of the lines the run will print,",
            "the rows' are recomputed, and D2 fires on the REAL ARTIFACT with",
            "NO environment variable set -- with D4 showing that reinstating",
            "the two removed lines makes the same artifact pass again."),
}


def verdict_for(tag):
    rows = tagged(tag)
    if not rows:
        return "NOT MEASURED"
    return "CLOSED" if all(ok is True for _, ok in rows) else "OPEN"


def bottom_line():
    """The two sentences, DERIVED from the rows tagged with each finding.  The
    closing prose is reachable ONLY down the CLOSED branch; an OPEN verdict
    prints the rows that did not hold instead of the sentence they were
    supposed to license."""
    out = []
    for tag in ("H-1", "H-2"):
        rows = tagged(tag)
        good = sum(1 for _, ok in rows if ok is True)
        v = verdict_for(tag)
        if v == "CLOSED":
            out.append(f"  mg-8aae {tag} IS CLOSED {CLOSING[tag][0]}")
            out += [f"  {l}" for l in CLOSING[tag][1:]]
        else:
            out.append(f"  mg-8aae {tag} IS {v} IN THIS TREE, and the closing")
            out.append("  sentence is therefore NOT written.  The rows that")
            out.append("  did not hold:")
            out += [f"    - {d[:150]}" for d, ok in rows if ok is not True]
        out.append(f"  ({good} of {len(rows)} rows tagged {tag} are "
                   "[CONFIRMED].)")
        out.append("")
    return out


PRIMARY_SENTENCE = re.compile(r"mg-8aae (H-1|H-2) IS (NOT MEASURED|CLOSED|OPEN)\b")
PRIMARY_COUNT = re.compile(r"\((\d+) of (\d+) rows tagged (H-1|H-2) are")


def summary_versus_rows(summary):
    """SUMMARY vs ROWS, for this instrument's own bottom line.  Both sides are
    obtained independently: one PARSED OUT OF THE LINES ABOUT TO BE PRINTED,
    one RECOMPUTED FROM THE ROWS.  Editing the sentences above moves one and
    not the other -- which is exactly what mg-8aae H-2 found missing, so an
    instrument landing H-2 with a hand-written bottom line would be landing it
    in name only."""
    text = " ".join("\n".join(summary).split())
    said = dict(PRIMARY_SENTENCE.findall(text))
    counts = {t: (int(a), int(b)) for a, b, t in PRIMARY_COUNT.findall(text)}
    owed, ok = {}, True
    for tag in ("H-1", "H-2"):
        rows = tagged(tag)
        owed[tag] = (sum(1 for _, r in rows if r is True), len(rows))
        ok = ok and said.get(tag) == verdict_for(tag) \
            and counts.get(tag) == owed[tag]
    record(ok,
           "SUMMARY vs ROWS: the two sentences below, READ BACK OUT OF THE "
           f"LINES THIS RUN WILL PRINT, say "
           + "; ".join(f"{t} {said.get(t, 'UNREADABLE')} "
                       f"{counts.get(t, ('?', '?'))}" for t in ("H-1", "H-2"))
           + ", and the rows they summarise, counted again here, say "
           + "; ".join(f"{t} {verdict_for(t)} {owed[t]}"
                       for t in ("H-1", "H-2"))
           + " -- " + ("they agree, and the two sides are obtained "
                       "independently: one parsed from the printed sentences, "
                       "one recomputed from the rows"
                       if ok else
                       "THEY DISAGREE.  The rows are regenerated every run "
                       "and the summary is written once; believe the rows"))


# --------------------------------------------------------------------------
def main():
    print("mg-8eca -- THE mg-8aae REPAIR, MEASURED ON THE ARTIFACT")
    print("=" * 78)
    print("""mg-8aae returned PARTIAL with two open items and one closing note: both are
the same two questions in different clothes.  IS THE MEASURED PROPERTY
INVARIANT UNDER THE GUARDED FAILURE -- a multiset is invariant under exchange,
`x == x` is invariant under everything -- and IS THE DEMONSTRATION AT THE RIGHT
TARGET, the hook or the check.  Neither is a coverage problem and neither is
fixed by checking more things, so neither is answered here by adding checks:
R1 changes what the census measures, R2 changes where the summary check reads
from, and each is then shown MOVING under the exact failure the old one sat
still for.  0 mathematical statements are touched.""")

    dirty = git("status", "--porcelain", "--", *REQUIRE_CLEAN).strip()
    if dirty:
        print()
        print("  REFUSING TO RUN: a file this run will restore is already")
        print("  dirty.  A restore that cannot be told apart from your own")
        print("  edit is not a restore.  git status over those files:")
        for l in dirty.split("\n"):
            print(f"    {l}")
        return 2
    for p in MUTABLE + [AUDIT_8AAE_OUT, REPAIR_8916_OUT]:
        CLEAN[p] = sha(p)

    r1()
    r2()
    r3()
    r4()

    head("BOTTOM LINE")
    summary = bottom_line()
    summary_versus_rows(summary)
    print()
    bad = [t for t, ok, _g in RESULTS if ok is False]
    print(f"  checks recorded : {len(RESULTS)}")
    print(f"  measurements    : {sum(1 for _, ok, _g in RESULTS if ok is None)}")
    print(f"  confirmed       : {sum(1 for _, ok, _g in RESULTS if ok is True)}")
    print(f"  refuted         : {len(bad)}")
    print()
    if bad:
        print("  REFUTED -- a claim this repair makes did not hold, and the")
        print("  prose must not be written:")
        for t in bad:
            print(f"    - {t}")
        print()
    for line in summary:
        print(line)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
