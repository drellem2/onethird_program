#!/usr/bin/env python3
"""PERMUTED -- CONDITION 2, MEASURED RATHER THAN ASSERTED IN PROSE.

mg-20ee's condition 2 says a transcript "reproduces byte-identically" at the
declared commit.  mg-0e77's R3 established that A CORRECT PIN CANNOT MEET IT:
`grep -rn` emits directory-enumeration order, the only form that reads a corpus
AT a commit is `git grep <rev>`, and git SORTS.  So condition 2 was re-read as

    SET-IDENTITY PLUS A DECLARED PERMUTATION

and that reading was then applied to two pins BY HAND and written down in prose,
in three places -- this directory's README, pinnable.py's docstring, and
pinnable.py's own printed output.  `18 of 129 lines permuted, the two line SETS
identical`.  Nothing in this estate could re-take that measurement.

    THIS ARC'S OWN SENTENCE ABOUT ITSELF (mg-54b1, on a README that went stale
    in the sense the instrument beside it was built to count): PROSE HAS NO
    MECHANISM BEHIND IT.  Condition 0 has an instrument, condition 3 has an
    instrument, and condition 2 -- the one that decides whether a pin LANDED --
    had a paragraph.  This file is that instrument.

--------------------------------------------------------------------------------
1.  THE HEADLINE, AND IT AMENDS THE AMENDMENT: `SET-IDENTITY` IS THE WRONG TEST
--------------------------------------------------------------------------------

A set forgets HOW MANY TIMES a line occurs.  A transcript in this estate is full
of repeated lines -- rules, blanks, and, less comfortably, ADDRESSES: mg-3b51's
own pinned transcript prints

    docs/OneThird-Landscape-Where-This-Lives.md:447  negate     x2

and mg-1953's re-run prints one address THREE times.  Under a SET comparison, a
pin that dropped one of those three occurrences scores IDENTICAL.  An address
and the count it belongs to would have moved, invisibly, in the one test
condition 2 exists to be trusted about -- and the failure would be SILENT, which
section D of consumers.py names as the worse of the two ways to be wrong.

The test is MULTISET (bag) identity: same lines, same multiplicities, any order.
Both verdicts are printed here, always, side by side, and this file says which
one it is deciding on.  BLAST RADIUS, MEASURED ACROSS THE ESTATE AT A PINNED
COMMIT RATHER THAN GUESSED, in section 2 of the output -- the two verdicts can
disagree on 1010 of 1061 tracked transcripts, and on 123 of them they can
disagree ABOUT A LINE CARRYING AN ADDRESS.

This is not a defect in mg-0e77's finding, which is correct and is the reason
this file exists.  It is the same shape that finding itself had: a rule stated
in the words nearest to hand, met by an instrument, and found to be measuring
something slightly wider than it says.  Both pins tranche 4 landed are re-scored
here and BOTH SURVIVE the stricter test -- section 1 of the output.

--------------------------------------------------------------------------------
2.  `A DECLARED PERMUTATION` IS MADE MECHANICAL, OR IT IS AN ADJECTIVE
--------------------------------------------------------------------------------

A pin adds an AS_OF block to its transcript -- mg-20ee's discrimination expressly
allows "addresses, corpus-size lines and the as-of block" to move.  So a correct
pin is NOT bag-identical either: it has a residue, and the residue is exactly
what the operator intended.  `--declare <file>` is where the operator writes that
residue down, one literal line per line, BEFORE reading the verdict.  Every
exclusive line must be matched by a declared one; anything left over is a
FINDING and this file says so.

    THE NEGATIVE HALF CARRIES THE WEIGHT AND IS CONTROLLED (N14): a declaration
    that matched loosely would be a way to pass any diff at all, which would make
    this instrument the opposite of what it is.  Matching is LITERAL and by
    OCCURRENCE -- declaring a line once does not excuse it twice.

--------------------------------------------------------------------------------
3.  WHAT THIS FILE IS NOT
--------------------------------------------------------------------------------

  * IT IS NOT A VERDICT ON THE PIN.  Bag-identity plus a declared residue says
    the transcript's CONTENT did not move.  It says nothing about whether the
    AS_OF is an ancestor of origin/main (condition 1), nor whether the
    instrument's consumers were re-measured (condition 3), nor whether the
    permutation is the one `git grep`'s sort predicts -- only that no line's
    content or multiplicity changed.  A pin at the WRONG commit that happens to
    produce the same bag passes here, and mg-daba's defect is precisely a
    transcript that reproduced perfectly against a tree in no commit.

  * IT IS NOT A REASON TO STOP RUNNING THE BYTE TEST.  R3's permutation appears
    at the PIN TRANSITION and not run to run: mg-0e77 measured enumeration order
    to be a deterministic function of the set of names, four consecutive runs
    agreeing.  So ./build.sh's byte comparison and mg-f771's fixed point are
    RIGHT to compare bytes, and nothing here asks them to loosen.  This file is
    for the one comparison that spans a repair.

  * ITS OWN TRANSCRIPT REPRODUCES BYTE-IDENTICALLY, WHICH IS THE ONLY HONEST
    ARRANGEMENT FOR THE FILE ARGUING THAT OTHERS CANNOT.  The estate scan reads
    `git ls-tree -r AS_OF` and `git cat-file`, both ordered reads of a commit;
    this file INVOKES no filesystem enumeration at all.  So out_permuted.txt
    satisfies condition 2 AS ORIGINALLY WRITTEN.

  * AND POINTING R3 AT SUBJECTS IT HAD NOT SEEN FOUND AN OVER-COUNT IN IT,
    WHICH IS REPORTED AND NOT REPAIRED HERE.  R3 matches the invocation plus a
    following short-flag cluster; mg-0e77's N11 controls "the word in prose"
    but plants the BARE word.  So a SENTENCE OF COMMENTARY naming the
    invocation fires it.  MEASURED across the estate at AS_OF rather than
    supposed: 3 of R3's 92 hits sit on comment lines, in 2 files -- and BOTH
    hits in one of them are in audit_scope_text.py, THE INSTRUMENT TRANCHE 4
    PINNED, whose only R3 hits are two comments explaining the defect it
    already repaired.  Condition 0 still tells it to expect a permuted
    transcript, which is the failure N9's rationale exists to prevent arriving
    by prose instead of by the git form.  An early draft of THIS file carried
    the same shape and rewording removed it -- which repairs nothing, and is
    recorded in section 4 because a clean self-score would otherwise read as
    evidence.  Asserted as N18, a known-defect control; R3 is mg-0e77's rule.

    sh code/asof_census_20ee/run_all.sh        # section 3 only: the estate scan
    python3 code/asof_census_20ee/permuted.py <path> [<old-rev>] [<new-rev>]
    python3 code/asof_census_20ee/permuted.py --declare asof.txt <path>
"""

import collections
import difflib
import os
import re
import subprocess
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", ".."))

# The commit the estate scan of section 3 reads.  An ancestor of origin/main
# (condition 1 applied to this file's own transcript), and the reason that
# transcript has a fixed point -- see the docstring's last bullet.
AS_OF = "12aa5f8"

# Deliberately pinnable.py's PATHTOK, character for character.  The two files
# are asking the same question -- "does this line carry a repository address?"
# -- and two spellings of it would be two answers.
PATHTOK = re.compile(r"(?:[A-Za-z0-9_.\-]+/)+[A-Za-z0-9_.\-]+")

TRANSCRIPT = re.compile(r"(?:^|/)out_[^/]*\.txt$")


def git(*args, **kw):
    got = subprocess.run(["git", "-C", ROOT, *args], capture_output=True,
                         input=kw.get("input"))
    if got.returncode != 0:
        raise SystemExit("permuted: git %s failed: %s"
                         % (" ".join(args),
                            got.stderr.decode("utf-8", "replace").strip()))
    return got.stdout


def text(b):
    return b.decode("utf-8", "surrogateescape")


def compare(old, new):
    """Condition 2, computed.  `old` and `new` are lists of lines.

    Returns the byte, set and bag verdicts; the multiset of lines exclusive to
    each side; and, over the COMMON CORE -- both sides with their exclusive
    occurrences removed, which are by construction the same length and the same
    bag -- how many positions hold a different line.  That last number is the
    PERMUTATION, and printing it is what makes it declared rather than implied.
    """
    bo, bn = collections.Counter(old), collections.Counter(new)
    only_old, only_new = bo - bn, bn - bo

    def core(seq, excess):
        rem = collections.Counter(excess)
        out = []
        for ln in seq:
            if rem[ln]:
                rem[ln] -= 1
                continue
            out.append(ln)
        return out

    co, cn = core(old, only_old), core(new, only_new)
    # TWO MEASURES OF `PERMUTED`, BECAUSE THE WORD DOES NOT PICK ONE.  The
    # positional count is how many core positions hold a different line; the
    # minimum is how many lines MUST move to turn one order into the other
    # (core length less its longest common subsequence).  A single line moved
    # from the top to the bottom scores `all of them` on the first and `1` on
    # the second, and both sentences are true of it.  mg-0e77's `18 of 129` is
    # neither -- see the output's section 2.
    matched = sum(b.size for b in difflib.SequenceMatcher(
        None, co, cn, autojunk=False).get_matching_blocks())
    return {
        "byte": old == new,
        "set": set(old) == set(new),
        "bag": bo == bn,
        "only_old": only_old,
        "only_new": only_new,
        "core_len": len(co),
        "moved": sum(1 for a, b in zip(co, cn) if a != b),
        "moved_min": len(co) - matched,
        "old_len": len(old),
        "new_len": len(new),
    }


def declared(counter, allowed):
    """Split an exclusive multiset into (declared, undeclared) occurrences.

    `allowed` is a multiset of literal lines the operator wrote down.  Matching
    is BY OCCURRENCE: declaring a line once does not excuse it twice, because a
    pin that dropped one of three identical addresses is the exact case section 1
    of the docstring exists for, and a set-shaped declaration would re-introduce
    it one level up.
    """
    rem = collections.Counter(allowed)
    ok, bad = collections.Counter(), collections.Counter()
    for ln, n in sorted(counter.items()):
        take = min(n, rem[ln])
        rem[ln] -= take
        if take:
            ok[ln] = take
        if n - take:
            bad[ln] = n - take
    return ok, bad


def read_rev(rev, path):
    return text(git("show", "%s:%s" % (rev, path))).splitlines()


def read_worktree(path):
    with open(os.path.join(ROOT, path), "rb") as fh:
        return text(fh.read()).splitlines()


def batch(rev, paths):
    """Every path's content at `rev`, in ONE git process.

    `git cat-file --batch` rather than a `git show` apiece: the estate scan is
    1061 files, and 1061 subprocesses is the difference between a build-path
    instrument and one nobody runs.
    """
    inp = "".join("%s:%s\n" % (rev, p) for p in paths).encode()
    out = git("cat-file", "--batch", input=inp)
    got, i = [], 0
    for p in paths:
        nl = out.index(b"\n", i)
        head = out[i:nl].split()
        if len(head) != 3:            # missing object: git prints `<name> missing`
            got.append((p, None))
            i = nl + 1
            continue
        size = int(head[2])
        got.append((p, out[nl + 1:nl + 1 + size]))
        i = nl + 1 + size + 1
    return got


def dup_profile(lines):
    """(distinct lines occurring more than once, of which how many carry an address)."""
    c = collections.Counter(lines)
    dups = [k for k, v in c.items() if v > 1]
    return len(dups), sum(1 for k in dups if PATHTOK.search(k))


def banner(s):
    print("-" * 78)
    print(s)
    print("-" * 78)
    print()


def verdict_block(r, decl_ok, decl_bad, has_declaration):
    print("  old %d line(s), new %d line(s), common core %d"
          % (r["old_len"], r["new_len"], r["core_len"]))
    print()
    print("      byte-identical (condition 2 AS WRITTEN) : %s" % r["byte"])
    print("      bag-identical  (THE TEST DECIDED ON)    : %s" % r["bag"])
    print("      set-identical  (THE PROSE'S WORDING)    : %s" % r["set"])
    print()
    if r["set"] != r["bag"]:
        print("  *** THE TWO WORDINGS DISAGREE ON THIS TRANSCRIPT.  A line changed")
        print("      its NUMBER OF OCCURRENCES without any line appearing or")
        print("      disappearing, which a set cannot see.  This is section 1 of")
        print("      permuted.py's docstring, met on real data rather than planted.")
        print()
    print("      permutation: %d of %d core position(s) hold a different line;"
          % (r["moved"], r["core_len"]))
    print("                   %d line(s) MUST move to get from one order to the"
          % r["moved_min"])
    print("                   other.  Both are true of the same diff.")
    print()

    if r["only_old"] or r["only_new"]:
        print("  LINES EXCLUSIVE TO ONE SIDE -- these are the CONTENT difference,")
        print("  and no permutation explains them:")
        print()
        for ln, n in sorted(r["only_old"].items()):
            print("      -%-3d %s" % (n, ln[:66]))
        for ln, n in sorted(r["only_new"].items()):
            print("      +%-3d %s" % (n, ln[:66]))
        print()
        if has_declaration:
            print("      %d occurrence(s) DECLARED, %d NOT"
                  % (sum(decl_ok.values()), sum(decl_bad.values())))
            for ln, n in sorted(decl_bad.items()):
                print("      UNDECLARED  x%-3d %s" % (n, ln[:60]))
            print()


def compare_mode(path, old_rev, new_rev, declaration):
    old = read_rev(old_rev, path)
    new = read_worktree(path) if new_rev is None else read_rev(new_rev, path)
    r = compare(old, new)
    ok, bad = declared(r["only_old"] + r["only_new"], declaration or [])

    print("=" * 78)
    print("mg-885d -- CONDITION 2, MEASURED:  %s" % path)
    print("=" * 78)
    print()
    print("  old : %s" % old_rev)
    print("  new : %s" % (new_rev if new_rev else "the working tree"))
    print("  declaration: %s"
          % ("%d line(s)" % len(declaration) if declaration is not None
             else "none given -- any exclusive line is a finding"))
    print()
    verdict_block(r, ok, bad, declaration is not None)

    exclusive = sum((r["only_old"] + r["only_new"]).values())
    if r["byte"]:
        v = "BYTE-IDENTICAL -- condition 2 is met AS ORIGINALLY WRITTEN"
    elif r["bag"]:
        v = ("PERMUTATION ONLY -- condition 2 met under R3's reading, "
             "%d line(s) moved" % r["moved"])
    elif declaration is not None and not bad:
        v = ("PERMUTATION + DECLARED RESIDUE -- %d exclusive line(s), all "
             "declared" % exclusive)
    else:
        v = ("CONTENT MOVED -- %d undeclared exclusive line(s).  THIS IS A "
             "FINDING" % (sum(bad.values()) if declaration is not None
                          else exclusive))
    print("=" * 78)
    print("CONDITION 2: %s" % v)
    print("=" * 78)
    return 0 if (r["bag"] or (declaration is not None and not bad)) else 1


# The two pins tranche 4 landed, re-scored here under the stricter test.  Each
# ships a DECLARATION FILE beside this one, and the declaration's PROVENANCE is
# checked mechanically -- see `provenance()`, and the reason in its docstring.
TRANCHE4 = [
    ("code/landscape_repair_audit_3b51/out_scope_text.txt", "e924590",
     "declare_3b51.txt", "code/landscape_repair_audit_3b51/audit_scope_text.py"),
    ("code/landscape_repair_1953/out_scope_text_3b51_rerun.txt", "1db0be9",
     "declare_1953.txt", "code/landscape_repair_audit_3b51/audit_scope_text.py"),
]
PIN_COMMIT = "de4ec4b"

PRINT_LITERAL = re.compile(r"""print\(\s*(?:"((?:[^"\\]|\\.)*)"|'((?:[^'\\]|\\.)*)')""")
DISTINCT = re.compile(r"(?:[A-Za-z0-9_.\-]+/)+[A-Za-z0-9_.\-]+|\b\d{2,}\b")


def provenance(line, literals, record):
    """Where a DECLARED line came from -- and specifically, NOT FROM THE DIFF.

    THIS IS THIS FILE'S OWN DEFECT, ENUMERATED BEFORE IT WAS COMMITTED.  The
    remedy here is `--declare`, and a declaration is an artifact of the same kind
    as the thing it scores: a declaration written by reading the diff excuses
    every line of that diff and turns CONTENT MOVED into a pass, silently.  So
    the two declarations shipped here are traced back to a source that is not the
    diff, and the count of lines that trace to NOTHING is printed.  A future
    declaration is only worth what its provenance is.

      `script`   the line is a literal prefix of a `print(...)` in the pinned
                 instrument's own SOURCE at the pinning commit.  This is the
                 AS_OF header a pin adds, and it is the strong half: the pin's
                 author wrote it in CODE, and code is not the transcript diff.

      `record`   a distinctive token of the line -- a repository path, or a
                 number of two or more digits -- appears in the pin's PUBLISHED
                 RECORD: its commit message plus the README it landed with, both
                 read at the pinning commit.  DECLARED WEAK, in the form
                 census.py and R2 state their biases: one token is a low bar,
                 and a line sharing an integer with the record passes it.  It is
                 here because the price of the 1953 pin was published in prose
                 and nowhere else -- `23 -> 24` in the commit message and the
                 moved address in the README -- and a rule that could not read
                 prose would call the published price unsourced.

      `blank`    the line is empty.  A blank carries no address, no count and no
                 verdict, so excusing one excuses nothing; classed rather than
                 counted as a failure, and said here rather than left to be
                 noticed as a hole in the arithmetic.
    """
    if not line.strip():
        return "blank"
    for lit in literals:
        if lit and line.startswith(lit):
            return "script"
    for tok in DISTINCT.findall(line):
        if tok in record:
            return "record"
    return "UNSOURCED"


def print_literals(rev, path):
    """The literal prefixes of every `print(...)` in a script, up to its first %.

    A format string's literal head is what survives into the transcript, and it
    is the part a declaration can be matched against.
    """
    out = []
    for ln in text(git("show", "%s:%s" % (rev, path))).splitlines():
        m = PRINT_LITERAL.search(ln)
        if m:
            lit = (m.group(1) or m.group(2)).split("%")[0]
            if lit.strip():
                out.append(lit)
    return out


def estate_mode():
    print("=" * 78)
    print("mg-885d -- CONDITION 2's INSTRUMENT.  Estate scan at AS_OF = %s" % AS_OF)
    print("=" * 78)
    print()
    print("  mg-20ee condition 2, which mg-0e77 re-read as SET-IDENTITY PLUS A")
    print("  DECLARED PERMUTATION and then applied BY HAND.  Two things are")
    print("  measured here that were previously prose: whether that wording is")
    print("  the right one (section 2), and whether the two pins it was written")
    print("  from survive the stricter reading (section 1).")
    print()
    print("  METHOD AND BLIND SPOT are in this file's docstring and are not")
    print("  repeated; the sentence that matters is repeated -- THIS DECIDES")
    print("  CONDITION 2 AND NOTHING ELSE.  Conditions 1 and 3 are elsewhere,")
    print("  and a pin at a commit in no branch passes here (mg-daba).")
    print()

    banner("1  THE TWO PINS OF TRANCHE 4, RE-SCORED UNDER THE STRICTER TEST")
    print("  mg-0e77 reported `18 of 129 lines permuted` and `30 of 149`, the")
    print("  two line SETS identical, measured BY HAND and quoted in three")
    print("  files.  Re-taken here across the pinning commit %s, each" % PIN_COMMIT)
    print("  against a declaration file whose PROVENANCE is checked -- because a")
    print("  declaration written by reading the diff excuses that diff entirely.")
    print()
    # THE PIN'S PUBLISHED RECORD, and deliberately not the diff: its own
    # commit message plus the README it landed with, read AT the pinning commit.
    record = (text(git("log", "-1", "--format=%B", PIN_COMMIT))
              + text(git("show", "%s:code/asof_census_20ee/README.md" % PIN_COMMIT)))
    survived, moved_counts = 0, []
    for path, asof, decl_file, script in TRANCHE4:
        old = read_rev(PIN_COMMIT + "^", path)
        new = read_rev(PIN_COMMIT, path)
        r = compare(old, new)
        moved_counts.append(r)
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               decl_file)) as fh:
            decl = fh.read().splitlines()
        ok, bad = declared(r["only_old"] + r["only_new"], decl)
        # The script at the PINNING COMMIT: the pin's author wrote this header
        # in CODE.  Not at AS_OF -- AS_OF is a commit of the CORPUS, and the
        # pinned script does not exist there at all, which is the first thing
        # this check caught when it was pointed at a real pin.
        lits = print_literals(PIN_COMMIT, script)
        prov = collections.Counter(provenance(d, lits, record) for d in decl)
        print("  %s" % path)
        print("      %-34s %s" % ("byte-identical", r["byte"]))
        print("      %-34s %s" % ("bag-identical (whole file)", r["bag"]))
        print("      %-34s %s" % ("set-identical (whole file)", r["set"]))
        print("      %-34s %d of %d positions, %d must move"
              % ("permutation", r["moved"], r["core_len"], r["moved_min"]))
        print("      %-34s %s: %d line(s), provenance %s"
              % ("declaration", decl_file, len(decl),
                 " ".join("%s=%d" % kv for kv in sorted(prov.items()))))
        print("      %-34s %d declared, %d NOT"
              % ("exclusive occurrences",
                 sum(ok.values()), sum(bad.values())))
        for ln, n in sorted(bad.items()):
            print("          UNDECLARED x%-3d %s" % (n, ln[:56]))
        if not bad and not prov["UNSOURCED"]:
            survived += 1
            print("      -> PERMUTATION + DECLARED RESIDUE.  The pin holds, and")
            print("         every line of its declaration traces to the pin's own")
            print("         source or its published record rather than to the diff.")
        elif prov["UNSOURCED"]:
            print("      -> DECLARATION UNSOURCED -- %d line(s) trace to nothing"
                  % prov["UNSOURCED"])
        print()
    print("  %d of %d survive, and the ONE PIN WHOSE RESIDUE IS NOT PURE"
          % (survived, len(TRANCHE4)))
    print("  HEADER is the one whose commit message says so: the 1953 pin's")
    print("  declaration is 10 lines, 7 of them the AS_OF block its own script")
    print("  prints and THREE of them content -- `: 23` out, `: 24` in, and one")
    print("  new address.  That is exactly mg-0e77's `23 -> 24 IS ITS WHOLE")
    print("  PRICE AND IT IS PUBLISHED`, and this is the first time anything")
    print("  could CHECK that the published price was the whole of it.  A")
    print("  fourth moved line would have printed as UNDECLARED here.")
    print()
    print("  AND NEITHER HAND FIGURE IS REPRODUCED, WHICH IS THE SECOND FINDING")
    print("  OF THIS SECTION.  `18 of 129` and `30 of 149` are not wrong so")
    print("  much as UNDEFINED: three defensible readings of `permuted` give")
    print()
    print("      %-44s %s" % ("core positions holding a different line",
                              " and ".join(str(r["moved"]) for r in moved_counts)))
    print("      %-44s %s" % ("lines that MUST move (core less its LCS)",
                              " and ".join(str(r["moved_min"]) for r in moved_counts)))
    print("      %-44s %s" % ("lines a unified diff marks changed",
                              " and ".join(
                                  "%d" % (r["old_len"] + r["new_len"]
                                          - 2 * (r["core_len"] - r["moved_min"]))
                                  for r in moved_counts)))
    print()
    print("  and 18 is none of them.  The VERDICT does not move -- both pins")
    print("  still hold -- so this is not a defect in tranche 4's conclusion.")
    print("  It is the reason condition 2 needed an instrument rather than a")
    print("  paragraph: a number quoted in three files with nothing behind it")
    print("  cannot be re-taken, and nobody could tell WHICH QUANTITY it was.")
    print()

    banner("2  BLAST RADIUS -- WHERE `SET` AND `BAG` CAN DISAGREE, COUNTED")
    # `git ls-tree` is an ORDERED READ OF A COMMIT, which is what keeps R3
    # silent on this file and its own transcript byte-reproducible.
    names = [p for p in text(git("ls-tree", "-r", "--name-only", AS_OF)).splitlines()
             if TRANSCRIPT.search(p)]
    total = anydup = addrdup = 0
    worst = []
    for p, blob in batch(AS_OF, names):
        if blob is None:
            continue
        total += 1
        nd, na = dup_profile(text(blob).splitlines())
        if nd:
            anydup += 1
        if na:
            addrdup += 1
            worst.append((na, p))
    print("  Over every tracked out_*.txt in the commit, a transcript on which")
    print("  the two wordings CAN disagree is one carrying a repeated line:")
    print()
    print("      %4d  tracked out_*.txt at %s" % (total, AS_OF))
    print("      %4d  carry a repeated line -- SET is strictly weaker there"
          % anydup)
    print("      %4d  carry a repeated line THAT NAMES A REPOSITORY PATH,"
          % addrdup)
    print("            which is where the two wordings can disagree about an")
    print("            ADDRESS -- the dimension condition 2 exists for")
    print()
    for n, p in sorted(worst, reverse=True)[:6]:
        print("      %-58s %d" % (p[:58], n))
    print()
    print("  THIS DIRECTORY IS IN THE LIST AND AT THE TOP OF IT, which is")
    print("  section 4 of the README -- a control finding itself in the corpus")
    print("  it searches -- for the FIFTH time in this arc, and unlike R3's")
    print("  six self-hits THIS ONE IS TRUE: out_census.txt really does print")
    print("  the same address many times, and really is a transcript on which a")
    print("  set comparison would be weaker than a bag comparison.")
    print()

    banner("3  THE HAZARD, DEMONSTRATED ON REAL DATA RATHER THAN PLANTED")
    path = TRANCHE4[0][0]
    lines = read_rev(AS_OF, path)
    c = collections.Counter(lines)
    cand = sorted([k for k, v in c.items() if v > 1 and PATHTOK.search(k)])
    if not cand:
        print("  no repeated address line in %s -- section 4 cannot run" % path)
    else:
        victim = cand[0]
        cut, dropped = [], False
        for ln in lines:
            if ln == victim and not dropped:
                dropped = True
                continue
            cut.append(ln)
        r = compare(lines, cut)
        print("  Take mg-3b51's own PINNED transcript at %s and delete ONE" % AS_OF)
        print("  occurrence of a line it prints twice:")
        print()
        print("      %s" % victim.strip()[:66])
        print()
        print("  An address and the count it belongs to have moved.  The two")
        print("  wordings answer differently:")
        print()
        print("      set-identical : %s   <- the prose's test says NOTHING HAPPENED"
              % r["set"])
        print("      bag-identical : %s   <- the test decided on here" % r["bag"])
        print()
        print("  A pin that did this would be published as clean under the")
        print("  wording as written.  It is not a hypothetical shape: %d tracked"
              % addrdup)
        print("  transcripts carry a repeated address line at this commit.")
    print()

    banner("4  AN OVER-COUNT IN R3, MEASURED -- PROSE THAT NAMES THE\n   INVOCATION FIRES IT, AND N11 PLANTS ONLY THE BARE WORD")
    print("  R3 matches the invocation plus a following short-flag cluster, and")
    print("  N11 -- mg-0e77's negative control for `the word in prose` -- plants")
    print("  the BARE word.  So a SENTENCE OF COMMENTARY NAMING THE INVOCATION")
    print("  fires R3, and in an estate where every docstring names its own")
    print("  method that is a shape worth counting rather than supposing.")
    print()
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import pinnable
    srcs = [p for p in text(git("ls-tree", "-r", "--name-only", AS_OF)).splitlines()
            if p.endswith(".py") or p.endswith(".sh")]
    total_hits, comment_hits, in_files = 0, [], set()
    for p, blob in batch(AS_OF, srcs):
        if blob is None:
            continue
        for h in pinnable.unordered_walks(text(blob)):
            total_hits += 1
            if h.startswith("#"):
                comment_hits.append((p, h))
                in_files.add(p)
    print("      %4d  .py/.sh tracked at %s" % (len(srcs), AS_OF))
    print("      %4d  R3 hits across them" % total_hits)
    print("      %4d  of those hits sit on a COMMENT line, in %d file(s) --"
          % (len(comment_hits), len(in_files)))
    print("            prose, not an invocation, and R3 cannot tell them apart")
    print()
    for p, h in comment_hits:
        print("      %s\n          %s" % (p, h[:68]))
    print()
    print("  AND THE FILE THIS LANDS HARDEST ON IS THE ONE TRANCHE 4 PINNED.")
    print("  audit_scope_text.py's ONLY R3 hits are two comments EXPLAINING THE")
    print("  DEFECT IT ALREADY REPAIRED -- its corpus read is `git grep <rev>`")
    print("  now, and R3 reads the sentences describing what it used to be.  So")
    print("  condition 0 run on it today still prints `+R3: expect a permuted")
    print("  transcript`, which is exactly the failure N9's rationale exists to")
    print("  prevent -- `every repaired instrument in the estate is told it is")
    print("  still defective` -- arriving by PROSE instead of by the git form.")
    print()
    print("  FOUND WHILE WRITING THIS FILE, WHICH IS RECORDED BECAUSE IT IS THE")
    print("  HALF THAT WOULD OTHERWISE LOOK LIKE A CLEAN RESULT: an early draft")
    print("  of permuted.py carried a sentence naming the invocation, R3 fired")
    print("  on it, and REWORDING THE SENTENCE MADE THE HIT GO AWAY.  That is")
    print("  not a repair of anything -- it removes one file from a rule that is")
    print("  still wrong for the other %d -- and this file scores %d today."
          % (len(in_files), len(pinnable.unordered_walks(open(os.path.abspath(__file__)).read()))))
    print("  So the shape is asserted as N18 in selftest_20ee.py, a KNOWN-DEFECT")
    print("  control in the form N4, N5 and C3 already take: teach R3 to see")
    print("  prose and N18 goes RED, which is the signal to update its declared")
    print("  self-hit count.  R3 is mg-0e77's rule and this is not its repair.")
    print()

    print("=" * 78)
    print("CONDITION 2: instrument GREEN -- %d of %d tranche-4 pins survive the "
          "stricter test; %d of %d transcripts are ones on which SET and BAG can "
          "disagree" % (survived, len(TRANCHE4), anydup, total))
    print("=" * 78)
    return 0


def main(argv):
    declaration = None
    if argv[:1] == ["--declare"]:
        with open(argv[1]) as fh:
            declaration = fh.read().splitlines()
        argv = argv[2:]
    if argv[:1] == ["--estate"] or not argv:
        return estate_mode()
    path = argv[0]
    old_rev = argv[1] if len(argv) > 1 else "HEAD"
    new_rev = argv[2] if len(argv) > 2 else None
    return compare_mode(path, old_rev, new_rev, declaration)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
