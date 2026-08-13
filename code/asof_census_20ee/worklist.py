#!/usr/bin/env python3
"""WORKLIST -- THE WORK-LIST IS ITSELF A TRANSCRIPT, AND NOTHING RE-TAKES IT.

`out_ground_truth.txt` is the number this directory tells everybody to quote.
Its own header says what it is: ONE DATED RUN, ~70 minutes, executing instrument
code, against `the working tree at 5a62e8c`.  `run_all.sh` does not run it and
says why.  So it has exactly the property every instrument on it is on it FOR --
IT IS A COMMITTED TRANSCRIPT WHOSE SUBJECT KEEPS MOVING UNDERNEATH IT -- and
five tranches have quoted its count without re-taking it.

    mg-0e77 published `25 instruments remain`; mg-885d and mg-e5f3 each
    restated it UNCHANGED; mg-44da and mg-23af restated nothing and re-took
    nothing either.  UNCHANGED IS THE CLAIM, and it was inherited rather than
    measured -- the sweep's transcript has had exactly ONE commit in its life,
    which section 1 counts rather than this paragraph asserting it.  This file
    asks the repository instead.

--------------------------------------------------------------------------------
1.  WHAT IT MEASURES, AND THE DIRECTION IT CAN ANSWER IN
--------------------------------------------------------------------------------

For every candidate row recorded in the sweep, read AT A DECLARED COMMIT:

  * has the instrument's own directory MOVED between the sweep's tree and
    AS_OF, and in which commits;
  * did any of those commits LAND A PIN -- by two different rules, counted
    side by side, because they disagree on real rows here (section 3);
  * does THIS DIRECTORY'S OWN RECORD name the instrument, which is the
    difference between a pin the arc has accounted for and one it has not.

THE ANSWER IS ONE-DIRECTIONAL AND THAT IS THE WHOLE HONEST STATEMENT OF IT.
Repo movement can prove a recorded row WRONG.  It can never prove one RIGHT: an
instrument whose directory has not been touched since the sweep may have gone
stale ANYWAY, because what moved is its CORPUS -- which is the defect class this
entire arc exists for.  So this file cannot replace `ground_truth.sh`; it can
only say that the list is no longer true, and where to look first.  Reported as
FALSIFIED / NOT FALSIFIED for that reason, never as REPRODUCES / DIFFERS.

--------------------------------------------------------------------------------
2.  THE FINDING THAT MADE IT WORTH WRITING, AND IT WAS FOUND BY RUNNING
--------------------------------------------------------------------------------

mg-e8b0's ticket says the remaining instruments must be SCORED AND NOT
EYEBALLED.  Taking that literally means running one, and the cheapest name on
the list is the one tranche 1's README hands the next tranche:

    the small ones (`species_remainder_f8fa` at `2+/2-`, `species_repair_a4ef`
    at `2+/4-`) are cheap

`sh code/species_remainder_f8fa/run_all.sh` REPRODUCES BYTE-IDENTICALLY at
07a2fd0.  It is not stale, and it is not stale because `e29ba2a` PINNED IT --
`pin: w3_scope READS ITS CORPUS AT A DECLARED COMMIT` -- AND THAT COMMIT IS
THIS ARC'S OWN, mg-6e4f, TRANCHE 2.  So the cheapest item this record offers
the next tranche is one the arc itself repaired the tranche after writing the
offer, and the sentence offering it has stood through four tranches since.

    THAT IS THE FINDING AND IT IS NOT `SOMEBODY ELSE MOVED UNDERNEATH US`,
    which was this file's first draft and was WRONG: e29ba2a carries `(mg-6e4f)`
    and pins w3_scope.py.  The count knew -- tranche 3 reports `26 remain`,
    which is 32 less tranche 1's five less this one -- and THE NAME DID NOT.
    A count is not a record of WHICH, and the reader picking the next
    instrument reads the name.

That is not a criticism of the sweep, which declares itself dated in its own
header.  It is the arc's own subject arriving on the arc's own list: A FIGURE
NO `AS_OF` PINS HAS A SHORT HALF-LIFE (mg-23af, on out_consumers.txt, twice).

--------------------------------------------------------------------------------
3.  HOW THIS FILE COULD EXHIBIT THE DEFECT IT REPORTS -- ENUMERATED, AND ONE OF
    THEM WAS LIVE IN THE FIRST DRAFT
--------------------------------------------------------------------------------

  * IT COULD READ ITS OWN SUBJECT FROM THE LIVE WORKTREE.  Every input here --
    the recorded sweep, this directory's README, the commit log, the diffs --
    is read THROUGH A COMMIT (`git show <AS_OF>:<path>`, `git log SWEEP..AS_OF`).
    Nothing is opened off disk.  That is the one thing permuted.py had to
    repair in itself at mg-e5f3, so it is asserted rather than promised: P26
    plants a mutated `out_ground_truth.txt` IN THE WORKTREE and requires every
    figure to stand still.

  * ITS OWN TRANSCRIPT COULD GO STALE THE WAY THE SWEEP'S DID.  It cannot go
    stale in the sense the sweep's did -- every number is a function of two
    commits and nothing else -- but it WILL go stale in the sense that matters:
    AS_OF stops being the newest thing on main the moment anything lands.  That
    is a property of a pin and not a defect of one, and the remedy is the same
    as for every pinned transcript here: MOVE THE PIN AND RE-RUN, deliberately.

  * THE `RECORD NAMES IT` RULE IS A SUBSTRING COUNT AND IT OVER-FORGIVES.  A
    directory this record names for an UNRELATED reason -- as remaining work,
    say -- reads as ACCOUNTED FOR.  The bias is toward reporting FEWER
    unaccounted pins than there are, which is the safe direction for a finding,
    and it is not hypothetical: it is how this tranche's own subject was found.
    `species_remainder_f8fa` was named exactly once in the record, in the
    sentence calling it cheap REMAINING work, and it had been PINNED four
    tranches earlier.  N28 asserts the limit ON THE RULE -- accounting and
    offering score identically -- rather than on that sentence, which this
    commit annotates, because a control that goes red when somebody closes its
    instance invites the next tranche to `repair` it by re-opening the trap.
    THE MECHANICAL COUNT IS THE LOW WATER MARK, and the remedy for the rule not
    reading English is that THIS FILE PRINTS THE SENTENCE beside the row.

  * IT COULD REPORT MOVEMENT AS STALENESS.  It does not: `MOVED` is printed as
    `NOT FALSIFIED` unless a pin rule fires, because a commit touching a
    directory is not a statement about its transcript.

--------------------------------------------------------------------------------
4.  USAGE
--------------------------------------------------------------------------------

    python3 worklist.py                     # the git half.  In run_all.sh.
    python3 worklist.py --rerun <file>      # compare a fresh ground_truth.sh
                                            # output against the recorded one

The second is the HAND-RUN half and is dated exactly the way `out_ground_truth.txt`
is: it takes a file produced by `sh ground_truth.sh <dirs>`, which executes
instrument code and cannot be a build step.  `out_worklist_rerun.txt` records one
such run and says which tree it ran against.
"""

import os
import re
import subprocess
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", ".."))

# The commit every figure below is a function of.  An ancestor of origin/main --
# condition 1 applied to this file's own transcript -- and the reason that
# transcript has a fixed point.  Move it deliberately, and re-run.
AS_OF = "07a2fd0"

RECORD = "code/asof_census_20ee/README.md"
SWEEP_TRANSCRIPT = "code/asof_census_20ee/out_ground_truth.txt"

# The sweep's own row format, as ground_truth.sh writes it and out_ground_truth.txt
# indents it.  Parsed rather than re-typed: a hand-copied list of 44 directories
# is a second copy of the population, and two copies drift (mg-1344's P5).
ROW = re.compile(r"^\s*(code/\S+) (DIFFERS|REPRODUCES|NO_RUN_ALL)"
                 r"(?: rc=(-?\d+))?(?: lines=(\d+)\+/(\d+)-)?")

# The tree the sweep ran against, taken from its own header sentence rather than
# hard-coded here, for the same reason.
SWEEP_REV = re.compile(r"against the working tree at ([0-9a-f]{7,40})")

# pinnable.py's R2 token, character for character.  Same question, one spelling.
HEXTOK = re.compile(r"\b[0-9a-f]{7,40}\b")

# RULE A for "a pin landed here": the commit says so.  A rule about a COMMIT
# MESSAGE, and this estate writes its subjects to a convention (`pin:`, `fix:`,
# `refresh:`), so it is a real signal and not a guess.
PIN_SUBJECT = re.compile(r"^pin:", re.I)


def git(*args, **kw):
    got = subprocess.run(["git", "-C", ROOT, *args], capture_output=True,
                         input=kw.get("input"))
    if got.returncode != 0:
        raise SystemExit("worklist: git %s failed: %s"
                         % (" ".join(args),
                            got.stderr.decode("utf-8", "replace").strip()))
    return got.stdout


def text(b):
    return b.decode("utf-8", "surrogateescape")


def read_rev(rev, path):
    return text(git("show", "%s:%s" % (rev, path)))


def resolves(token):
    """R2's test, and it is what makes this a rule rather than a regex.

    `deadbeef` is hex-shaped and an eight-letter word; only an object that
    exists means somebody declared a revision.  `^{commit}` rather than a bare
    `-e`, because a blob whose abbreviated hash happens to be hex-shaped is not
    a declared revision either.
    """
    got = subprocess.run(["git", "-C", ROOT, "cat-file", "-e", token + "^{commit}"],
                         capture_output=True)
    return got.returncode == 0


def parse_rows(transcript_text):
    rows = []
    for line in transcript_text.splitlines():
        m = ROW.match(line)
        if m:
            rows.append({
                "dir": m.group(1),
                "verdict": m.group(2),
                "rc": m.group(3),
                "size": int(m.group(4) or 0) + int(m.group(5) or 0),
            })
    return rows


def commits_touching(directory, old, new):
    # `%h %s` and a split on the FIRST space: an abbreviated hash contains no
    # space, so the split is exact.  A NUL separator would be the obvious
    # choice and cannot be used -- a NUL in argv is rejected before git ever
    # sees it.
    out = text(git("log", "--format=%h %s", "%s..%s" % (old, new), "--", directory))
    got = []
    for line in out.splitlines():
        if not line.strip():
            continue
        h, _, subject = line.partition(" ")
        got.append({"hash": h, "subject": subject})
    return got


def added_revisions(commit, directory):
    """RULE B for "a pin landed here": the diff ADDED a revision that resolves.

    A rule about CONTENT rather than about a commit message.  It is the shape of
    a pin as pinnable.py's R2 defines one -- a declared revision in the
    subject's own scripts -- read across a single commit's diff to that
    directory.  It disagrees with rule A in BOTH directions on real rows here,
    which is why both are printed (section 3 of the output).
    """
    diff = text(git("show", "--format=", "-U0", commit, "--", directory))
    tokens = set()
    for line in diff.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            tokens.update(HEXTOK.findall(line))
    return sorted(t for t in tokens if resolves(t))


def pin_landed_in(commit):
    """Which directories of a commit's own diff gained a revision that resolves.

    This is what turns rule A's over-count into an ATTRIBUTION rather than a
    caveat.  A commit's subject says `pin:` once and its diff touches several
    directories; asking the diff which of them actually gained a declared
    revision answers `where did the pin land` without any judgement about the
    sentence.
    """
    got = []
    for path in text(git("show", "--name-only", "--format=", commit)).splitlines():
        if not path.strip():
            continue
        d = os.path.dirname(path)
        if d and d not in got and added_revisions(commit, d):
            got.append(d)
    return got


def scan():
    """Every figure this file publishes, computed from two commits and nothing
    else.  SEPARATE FROM THE PRINTING SO THE CONTROLS CAN CALL IT: a control
    that had to parse this file's own transcript to check it would be reading a
    report rather than running the rule, which is the shape mg-937c's rule
    forbids one directory over.
    """
    recorded_text = read_rev(AS_OF, SWEEP_TRANSCRIPT)
    record_text = read_rev(AS_OF, RECORD)
    rows = parse_rows(recorded_text)
    m = SWEEP_REV.search(recorded_text)
    if not m:
        raise SystemExit("worklist: the sweep transcript at %s does not state "
                         "the tree it ran against" % AS_OF)
    sweep = m.group(1)

    moved = []
    for r in rows:
        cs = commits_touching(r["dir"], sweep, AS_OF)
        r["commits"] = cs
        r["by_subject"] = [c for c in cs if PIN_SUBJECT.match(c["subject"])]
        r["by_content"] = [c for c in cs if added_revisions(c["hash"], r["dir"])]
        base = r["dir"].split("/")[-1]
        r["named"] = record_text.count(base)
        r["mentions"] = [ln.strip() for ln in record_text.splitlines() if base in ln]
        if cs:
            moved.append(r)

    # COUNTED PER (DIRECTORY, COMMIT) AND NOT PER DIRECTORY, because that is
    # what section 3 enumerates and the two grains give different numbers on
    # real data here: absent_step_7ae5 has one commit each rule sees alone, and
    # counted per directory it would read as `both rules agree`.
    pairs = [(r["dir"], c["hash"], c in r["by_subject"], c in r["by_content"])
             for r in moved for c in r["commits"]
             if c in r["by_subject"] or c in r["by_content"]]

    # R2 AT AS_OF, FOR EVERY ROW AND NOT JUST THE MOVED ONES.  pinnable.py's R2
    # asks `does a tracked script here declare a revision that resolves`, and it
    # asks it of a DIRTY WORKTREE because the rest of that file classifies a
    # diff.  This half needs no diff at all, so it can be asked of all 44 rows
    # at a commit -- which is mg-e8b0's third property (`wants an AS_OF`)
    # measured per instrument instead of inherited from list membership.
    # IT IS R2, SO IT CARRIES R2's DECLARED OVER-COUNT: a revision declared
    # anywhere in the subject's scripts fires it, and it may be a CONTROL's
    # rather than the corpus read's (species_repair_a4ef is the instance R2 was
    # built from).  Firing means `a revision is declared here, go and read why`.
    for r in rows:
        scripts = [p for p in text(git("ls-tree", "-r", "--name-only", AS_OF,
                                       r["dir"] + "/")).splitlines()
                   if p.endswith((".py", ".sh"))]
        found = []
        for p in scripts:
            body = text(git("show", "%s:%s" % (AS_OF, p)))
            for tok in sorted(set(HEXTOK.findall(body))):
                if resolves(tok):
                    found.append((p, tok))
                    break
        r["declares"] = found

    return {
        "sweep": sweep,
        "ncommits": text(git("rev-list", "--count",
                             "%s..%s" % (sweep, AS_OF))).strip(),
        "rows": rows,
        "moved": moved,
        "pairs": pairs,
        "only_a": [(d, h) for d, h, sa, sb in pairs if sa and not sb],
        "only_b": [(d, h) for d, h, sa, sb in pairs if sb and not sa],
        "both": [(d, h) for d, h, sa, sb in pairs if sa and sb],
        "falsified": [r for r in moved if r["by_content"]],
        "wide": [r for r in moved if r["by_subject"]],
    }


def main(argv):
    if len(argv) > 1 and argv[1] == "--rerun":
        tree = argv[argv.index("--tree") + 1] if "--tree" in argv else None
        return rerun(argv[2] if len(argv) > 2 else None, tree)

    got = scan()
    sweep, rows, moved = got["sweep"], got["rows"], got["moved"]

    bar = "=" * 78
    rule = "-" * 78
    print(bar)
    print("mg-e8b0 -- IS THE WORK-LIST STILL TRUE?  Read at AS_OF = %s" % AS_OF)
    print(bar)
    print()
    print("  out_ground_truth.txt is the number this directory tells everybody")
    print("  to quote, and it is ONE DATED RUN against the tree at %s." % sweep)
    print("  The count derived from it has been carried forward BY HAND since")
    print("  mg-0e77 and NOTHING HAS RE-TAKEN THE RUN -- the transcript's own")
    print("  commit count, one line up, is that sentence measured.  This")
    print("  section asks the repository, which is cheap and is one-directional:")
    print("  movement can FALSIFY a recorded row and can never confirm one.")
    print("  METHOD AND BLIND SPOTS are in this file's docstring and are not")
    print("  repeated; the sentence that matters is: THIS DOES NOT REPLACE THE")
    print("  RE-RUN.  An untouched instrument goes stale when its CORPUS moves.")
    print()

    ncommits = got["ncommits"]
    print(rule)
    print("1  THE LIST'S OWN AGE, IN THE UNIT THIS REPOSITORY MOVES IN")
    print(rule)
    print()
    print("      %-52s %s" % ("the sweep's tree", sweep))
    print("      %-52s %s" % ("this file's AS_OF", AS_OF))
    print("      %-52s %s" % ("commits on main between them", ncommits))
    # THE CLAIM `NOTHING RE-TAKES IT` IS MEASURED HERE RATHER THAN ASSERTED IN
    # THE PROSE ABOVE IT, which is this directory's own rule (mg-2959: the
    # prose was the one surface no instrument covered).
    print("      %-52s %d" % ("commits the sweep's transcript has EVER had",
                              len(text(git("log", "--format=%h", AS_OF, "--",
                                           SWEEP_TRANSCRIPT)).split())))
    print("      %-52s %d" % ("candidate rows recorded", len(rows)))
    for verdict in ("DIFFERS", "REPRODUCES", "NO_RUN_ALL"):
        n = sum(1 for r in rows if r["verdict"] == verdict)
        print("      %-52s %d" % ("  recorded %s" % verdict, n))
    print()

    print(rule)
    print("2  THE ROWS THE REPOSITORY CONTRADICTS")
    print(rule)
    print()
    print("      %-52s %d of %d" % ("directories moved since the sweep",
                                    len(moved), len(rows)))
    pinned, wide = got["falsified"], got["wide"]
    print("      %-52s %d" % ("  a pin landed, by CONTENT -- the verdict", len(pinned)))
    print("      %-52s %d" % ("  a pin landed, by SUBJECT -- the wide net", len(wide)))
    unaccounted = [r for r in pinned if not r["named"]]
    print("      %-52s %d" % ("  of the verdict rows, unnamed in this record",
                              len(unaccounted)))
    print()
    print("  A row is FALSIFIED when a pin has landed ON IT since the sweep:")
    print("  the recorded verdict is a statement about a tree that no longer")
    print("  exists.  MOVED WITHOUT A PIN is printed as NOT FALSIFIED, because")
    print("  a commit touching a directory says nothing about its transcript.")
    print()
    print("  THE VERDICT RESTS ON THE CONTENT RULE AND NOT ON THE SUBJECT ONE,")
    print("  and section 3 is where that choice is measured rather than argued:")
    print("  A SUBJECT IS A PROPERTY OF A COMMIT, AND A COMMIT TOUCHES SEVERAL")
    print("  DIRECTORIES.  Where they disagree the commit's own diff is read to")
    print("  say WHICH directory the pin landed in, so the over-count is")
    print("  attributed rather than declared.")
    print()
    for r in sorted(moved, key=lambda r: r["dir"]):
        print("  %s" % r["dir"])
        print("      recorded                     %s%s"
              % (r["verdict"], "" if not r["size"] else "  %d line(s) of drift" % r["size"]))
        print("      commits since the sweep      %d" % len(r["commits"]))
        for c in r["commits"]:
            print("          %-9s %s" % (c["hash"], c["subject"][:56]))
        print("      pin by SUBJECT / by CONTENT  %s / %s"
              % (",".join(c["hash"] for c in r["by_subject"]) or "-",
                 ",".join(c["hash"] for c in r["by_content"]) or "-"))
        print("      named in this record         %d time(s)" % r["named"])
        # THE SENTENCE, NOT JUST THE COUNT.  `named` is a substring count and
        # over-forgives by construction (N28); printing the line it matched is
        # what lets a reader see WHAT the record says about it, which on
        # species_remainder_f8fa is `cheap remaining work` about an instrument
        # this arc had already pinned.
        for ln in r["mentions"]:
            print("          %s" % ln[:64])
        if r["by_content"] and not r["named"]:
            print("      -> FALSIFIED, AND UNACCOUNTED.  A pin has landed and")
            print("         nothing in this directory's record knows about it.")
        elif r["by_content"]:
            print("      -> FALSIFIED.  A pin has landed; the record names it.")
        elif r["by_subject"]:
            for c in r["by_subject"]:
                elsewhere = pin_landed_in(c["hash"])
                print("      -> NOT FALSIFIED.  %s calls itself a pin and its" % c["hash"])
                print("         diff HERE declares no revision.  The revision it")
                print("         declares is in:")
                for d in elsewhere:
                    print("             %s" % d)
                if not elsewhere:
                    print("             (nowhere in its own diff -- read it)")
        else:
            print("      -> NOT FALSIFIED.  Moved, but no pin rule fires.")
        print()

    print(rule)
    print("3  TWO RULES FOR `A PIN LANDED`, COUNTED SIDE BY SIDE")
    print(rule)
    print()
    print("  Neither is a definition.  RULE A reads the commit SUBJECT, which")
    print("  this estate writes to a convention; RULE B reads the DIFF for a")
    print("  revision that resolves, which is pinnable.py's R2 across one")
    print("  commit.  They are printed together because THEY DISAGREE ON REAL")
    print("  ROWS HERE, in both directions, and a file publishing one of them")
    print("  alone would be publishing a choice it had not measured.")
    print()
    print("      %-52s %d" % ("(directory, commit) pairs either rule fires on",
                              len(got["pairs"])))
    print("      %-52s %d" % ("  rule A only -- the subject says `pin:`",
                              len(got["only_a"])))
    print("      %-52s %d" % ("  rule B only -- the diff added a resolving rev",
                              len(got["only_b"])))
    print("      %-52s %d" % ("  both", len(got["both"])))
    print()
    for r in sorted(moved, key=lambda r: r["dir"]):
        sa = set(c["hash"] for c in r["by_subject"])
        sb = set(c["hash"] for c in r["by_content"])
        for h in sorted(sa - sb):
            print("      A NOT B  %-42s %s" % (r["dir"], h))
            print("               a commit calling itself a pin whose diff to this")
            print("               directory adds NO revision that resolves")
        for h in sorted(sb - sa):
            print("      B NOT A  %-42s %s" % (r["dir"], h))
            print("               a revision declared here by a commit that does")
            print("               not call itself a pin")
    print()

    print(rule)
    print("4  `WANTS AN AS_OF`, MEASURED PER INSTRUMENT FOR ALL %d ROWS" % len(rows))
    print(rule)
    print()
    print("  mg-4020 established that `drifts` and `wants an AS_OF` are")
    print("  DIFFERENT PROPERTIES and that the second must be measured per")
    print("  instrument rather than inherited from list membership.  It")
    print("  measured three.  This is pinnable.py's R2 -- a revision declared")
    print("  in the subject's own scripts that RESOLVES -- asked of every row")
    print("  at AS_OF, which needs no dirty tree and so is not the 45 minutes")
    print("  conditions 1-3 cost.  IT CARRIES R2's OVER-COUNT UNCHANGED: the")
    print("  revision may be a CONTROL's rather than the corpus read's, so")
    print("  firing means `go and read why`, not `pinned`.")
    print()
    dec = [r for r in rows if r["declares"]]
    diff_rows = [r for r in rows if r["verdict"] == "DIFFERS"]
    open_rows = [r for r in diff_rows
                 if not r["declares"] and not r["by_content"]]
    print("      %-52s %d of %d" % ("rows declaring a revision at AS_OF",
                                    len(dec), len(rows)))
    print("      %-52s %d" % ("  of the recorded DIFFERS rows",
                              sum(1 for r in diff_rows if r["declares"])))
    print("      %-52s %d" % ("recorded DIFFERS, no revision, not falsified",
                              len(open_rows)))
    print()
    print("  THE LAST NUMBER IS THE ONE A SUCCESSOR WANTS, and it is a")
    print("  PREFILTER and not a work-list: `no revision declared` is not")
    print("  `wants one` -- mg-4020's a4ef drift is `.gitignore`d directories")
    print("  no AS_OF can reach, and it declares two revisions anyway.  These")
    print("  are the rows nothing on record has yet given a reason to skip:")
    print()
    for r in sorted(open_rows, key=lambda r: (r["size"], r["dir"])):
        print("      %-46s %d line(s) of recorded drift" % (r["dir"], r["size"]))
    print()

    print(rule)
    print("5  WHAT THIS SECTION CANNOT SAY, RESTATED WHERE IT IS READ")
    print(rule)
    print()
    print("  * NOT FALSIFIED IS NOT REPRODUCES.  %d rows are not contradicted"
          % (len(rows) - len(pinned)))
    print("    by anything above, and that is a statement about the REPOSITORY,")
    print("    not about their transcripts.  The backstop is ground_truth.sh.")
    print("  * A PIN IS NOT A REPAIR.  Rule A and rule B both say a revision")
    print("    was declared, not that the transcript now reproduces --")
    print("    pinnable.py's R2 fires on b0ae, which is pinned and drifts.")
    print("  * RULE B READS `git show`, WHICH PRINTS NOTHING FOR A MERGE.  A")
    print("    pin landing in a merge commit would be invisible to it.  There")
    print("    are %s merge commits between the two revisions this file reads,"
          % (text(git("rev-list", "--count", "--merges",
                      "%s..%s" % (sweep, AS_OF))).strip() or "0"))
    print("    and none in this repository at all, because the refinery")
    print("    REBASES -- so the rule is safe HERE by a property of the repo")
    print("    and not by anything this file does.  Counted rather than")
    print("    assumed, because the day that changes nothing else will say so.")
    print("  * THE UNACCOUNTED COUNT IS A LOW WATER MARK.  `named in this")
    print("    record` is a substring count, so an instrument this record names")
    print("    for any other reason -- AS REMAINING WORK, SAY -- reads as")
    print("    accounted for.  N28 asserts that with its live instance.")
    print()
    print("CONDITION 0 (work-list): %d of %d rows FALSIFIED, %d UNACCOUNTED, at %s"
          % (len(pinned), len(rows), len(unaccounted), AS_OF))
    return 0


def rerun(path, tree=None):
    """The hand-run half: a fresh ground_truth.sh output against the recorded one.

    Dated exactly the way out_ground_truth.txt is dated, and for the same reason
    -- it executes instrument code, so no build path may take it.

    THE TREE IT RAN AGAINST IS DECLARED AND THE DECLARATION IS CHECKED, which is
    permuted.py's `--declare` discipline applied to the one fact a hand-run's
    reader cannot recover: out_ground_truth.txt states its tree in a hand-typed
    header sentence and nothing verifies it.  `--tree <rev>` must RESOLVE and
    must be an ancestor of origin/main -- mg-20ee's condition 1, applied to the
    hand-run's own provenance.  Reading HEAD instead would be worse than
    hand-typing it: the answer would silently change under a rebase, which is
    this whole directory's subject.
    """
    if not path:
        raise SystemExit("worklist: --rerun needs a ground_truth.sh output file")
    if tree:
        if not resolves(tree):
            raise SystemExit("worklist: --tree %s does not resolve" % tree)
        anc = subprocess.run(["git", "-C", ROOT, "merge-base", "--is-ancestor",
                              tree, "origin/main"], capture_output=True)
        if anc.returncode != 0:
            raise SystemExit("worklist: --tree %s is not an ancestor of "
                             "origin/main (condition 1)" % tree)
    recorded = {r["dir"]: r for r in parse_rows(read_rev(AS_OF, SWEEP_TRANSCRIPT))}
    with open(path, "rb") as fh:
        fresh = {r["dir"]: r for r in parse_rows(text(fh.read()))}

    bar = "=" * 78
    print(bar)
    print("mg-e8b0 -- THE WORK-LIST RE-TAKEN.  Recorded at AS_OF = %s" % AS_OF)
    print(bar)
    print()
    print("  A DATED HAND-RUN, and it says so in the same words the sweep it")
    print("  compares against uses.  `sh ground_truth.sh <dirs>` re-runs each")
    print("  suite and reports whether its committed transcripts still")
    print("  reproduce; this reads that output beside the recorded one.")
    print()
    print("      %-52s %s" % ("the tree this re-run ran against",
                             tree or "NOT DECLARED"))
    if tree:
        print("      %-52s %s" % ("  resolves, and is an ancestor of origin/main",
                                 "CHECKED"))
    else:
        print("      %-52s %s" % ("  provenance",
                                  "UNSOURCED -- nothing here can check it"))
    print("      %-52s %d" % ("rows recorded in out_ground_truth.txt", len(recorded)))
    print("      %-52s %d" % ("rows in this re-run", len(fresh)))
    print()

    order = [d for d in recorded if d in fresh]
    changed = [d for d in order if recorded[d]["verdict"] != fresh[d]["verdict"]]
    stale_then = [d for d in order if recorded[d]["verdict"] == "DIFFERS"]
    stale_now = [d for d in order if fresh[d]["verdict"] == "DIFFERS"]
    print("      %-52s %d" % ("rows measurable in both", len(order)))
    print("      %-52s %d" % ("recorded DIFFERS, over those rows", len(stale_then)))
    print("      %-52s %d" % ("re-run  DIFFERS, over those rows", len(stale_now)))
    print("      %-52s %d" % ("rows whose verdict MOVED", len(changed)))
    print()
    for d in changed:
        print("  %-46s %s -> %s" % (d, recorded[d]["verdict"], fresh[d]["verdict"]))
        if recorded[d]["size"]:
            print("      recorded drift %d line(s); re-run %d line(s)"
                  % (recorded[d]["size"], fresh[d]["size"]))
    print()
    missing = [d for d in recorded if d not in fresh]
    if missing:
        print("  NOT RE-RUN HERE, AND NAMED RATHER THAN DROPPED -- a partial")
        print("  re-take that did not say which rows it skipped would read as a")
        print("  complete one:")
        for d in sorted(missing):
            print("      %-46s recorded %s" % (d, recorded[d]["verdict"]))
        print()
    print("RE-RUN: %d of %d rows moved verdict" % (len(changed), len(order)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
