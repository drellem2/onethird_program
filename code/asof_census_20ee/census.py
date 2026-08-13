#!/usr/bin/env python3
"""mg-20ee — THE COMPUTED-FOREIGN-ADDRESS CENSUS, AS AN INSTRUMENT RATHER THAN A NUMBER.

pc824 measured this population and mailed it.  mg-20ee exists because a census
that lives in one verdict mail has no owner and cannot be re-run: the numbers
104/64/40/54 could be quoted forever without anybody being able to check them or
watch them shrink.  This script IS the measurement.

WHAT IT COUNTS.  Over every tracked `code/**/out_*.txt`, an address `path:NNN`
counts as COMPUTED INTO A FOREIGN FILE when

  * the path resolves to a tracked file OUTSIDE the transcript's own instrument
    directory, and
  * the literal token does NOT occur in that instrument's own .py/.sh -- which
    would make it a HARDCODED CITATION: a stale-citation hazard, but not a
    reproducibility one, and a different repair, and
  * the instrument actually reads that file.

DECLARED BIAS, carried verbatim from pc824 because the number is only as good as
it.  It OVER-counts instruments that merely echo a foreign file's own prose
citation, and UNDER-counts addresses into files outside this repository, which
`git ls-files` cannot see at all.  So the instrument count is a FLOOR.

AND A SECOND BIAS, ADDED HERE BECAUSE THIS RUN MEASURED IT.  The classifier
cannot see that an instrument ALREADY reads its corpus at a declared commit --
code/state_audit_6a2f pins two literal revs and is counted anyway.  So the
census OVER-counts a second way, and the honest population is smaller than the
classifier's.  `out_ground_truth.txt` is the correction: it re-runs each
candidate and reports whether its committed transcripts actually still reproduce.
THAT is the number to quote; this one is the net that finds candidates for it.

AS-OF PINNING, WHICH THIS SCRIPT IS SUBJECT TO LIKE EVERY OTHER.  A census over
the corpus is CORPUS-VALUED: every count below moves when the corpus does.  So
the corpus is read at a declared commit, and the two conditions on that commit
are pm-onethird's, in this order:

  1. it MUST be an ancestor of origin/main -- a pin onto a polecat branch is
     valid only until somebody reaps the branch (mg-daba), and
  2. the transcript reproduces byte-identically at it.

Checking (2) first is what produces a bad pin, because it makes an unreachable
commit look like the only right answer.
"""
import collections
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))

#: The commit this census is taken over.  An ancestor of origin/main by
#: construction: it is main itself at the time of the run, recorded rather than
#: read live so that re-running this file cannot silently re-measure.
AS_OF = "5a62e8c88c4458453e47593d3474d584d2def8ff"

AT = os.environ.get("ASOF_CENSUS_AT", "").strip() or AS_OF

ADDR = re.compile(r"([A-Za-z0-9_][A-Za-z0-9_./\-]*"
                  r"\.(?:md|py|sh|tex|txt|json|yaml|yml|cfg|toml)):(\d+)")


def git(*args):
    got = subprocess.run(["git", "-C", REPO, *args], capture_output=True)
    if got.returncode != 0:
        raise SystemExit(
            "mg-20ee census: cannot read the corpus at %s: %s\n"
            "  (ASOF_CENSUS_AT=%r; unset it for the pinned run.)"
            % (AT, got.stderr.decode("utf-8", "replace").strip(), AT))
    return got.stdout.decode("utf-8", "replace")


def tracked():
    return sorted(p for p in git("ls-tree", "-r", "--name-only", AT).split("\n") if p)


def read(rel):
    return git("show", "%s:%s" % (AT, rel))


def main():
    files = tracked()
    tracked_set = set(files)
    by_suffix = collections.defaultdict(list)
    for t in files:
        parts = t.split("/")
        for i in range(len(parts)):
            by_suffix["/".join(parts[i:])].append(t)

    def resolve(path, owner):
        if path in tracked_set:
            return path
        cand = os.path.normpath(os.path.join(owner, path))
        if cand in tracked_set:
            return cand
        hits = by_suffix.get(path.lstrip("./"), [])
        return hits[0] if len(hits) == 1 else None

    transcripts = [p for p in files
                   if p.startswith("code/") and p.endswith(".txt")
                   and os.path.basename(p).startswith("out_")]

    # the instrument's own source, per directory
    src_of = {}
    for p in files:
        if p.startswith("code/") and p.endswith((".py", ".sh")):
            src_of.setdefault(os.path.dirname(p), []).append(p)

    rows = []
    for tr in transcripts:
        owner = os.path.dirname(tr)
        src = "".join(read(p) for p in sorted(src_of.get(owner, [])))
        found = collections.defaultdict(list)
        for m in ADDR.finditer(read(tr)):
            token, path, num = m.group(0), m.group(1), m.group(2)
            tgt = resolve(path, owner)
            if not tgt or os.path.dirname(tgt) == owner:
                continue
            if token in src:                     # hardcoded citation, not computed
                continue
            base = os.path.basename(tgt)
            if not (tgt in src or base in src or base.rsplit(".", 1)[0] in src
                    or os.path.dirname(tgt) in src):
                continue                         # the instrument does not read it
            found[tgt].append(int(num))
        if found:
            rows.append((tr, owner, dict(found)))

    inst = collections.defaultdict(list)
    for tr, owner, found in rows:
        inst[owner].append((tr, found))

    print("=" * 78)
    print("mg-20ee — TRANSCRIPTS CARRYING A COMPUTED FOREIGN ADDRESS")
    print("=" * 78)
    print("""
  corpus read at : %s
      %s

  THE COUNTS BELOW ARE CORPUS-VALUED.  They measure this repository, not this
  ticket, and they move whenever an instrument or a transcript is added.  That
  is why they are pinned: an unpinned census cannot be watched shrinking,
  because you could never tell a repair from a corpus that grew.

  THIS IS A NET, NOT A VERDICT.  It over-counts twice by construction -- once on
  instruments that merely echo a foreign file's own prose citation, and once on
  instruments that ALREADY read at a declared commit, which it cannot see.  It
  under-counts addresses into files outside this repository, which git cannot
  see at all.  out_ground_truth.txt is the correction and is the number to
  quote.
""" % (AT, "AS_OF, the pinned default" if AT == AS_OF
       else "OVERRIDE via ASOF_CENSUS_AT -- NOT the as-of stamp " + AS_OF[:7]))

    print("  %4d transcripts carry a computed foreign address" % len(rows))
    print("  %4d distinct instruments" % len(inst))
    naddr = sum(len(v) for _, _, f in rows for v in f.values())
    print("  %4d addresses in total" % naddr)
    print()
    print("-" * 78)
    print("BY INSTRUMENT -- transcripts, addresses, and the files addressed")
    print("-" * 78)
    for owner in sorted(inst):
        v = inst[owner]
        tgts = sorted({t for _, f in v for t in f})
        n = sum(len(a) for _, f in v for a in f.values())
        print("  %-42s %2d transcript(s)  %3d address(es)" % (owner, len(v), n))
        for t in tgts:
            print("        -> %s" % t)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
