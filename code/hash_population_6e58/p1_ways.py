"""p1_ways.py -- THE WAYS A `git log` CALL ADDRESSES A COMMIT, ENUMERATED
FROM GIT'S OWN DOCUMENTATION.

The brief: "ENUMERATE THE WAYS, not the flags you happen to recall, and say
how you enumerated them (git's own documentation is a population you can
read)."

So this script reads `man git-log` on this machine and parses it.  Every row
below is printed with the documentation text it came from, because the claim
being made is about a READING, and a reading that cannot be checked is a
recollection with a citation stapled to it.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import subprocess

import lib6e58 as L

R = L.Report(selfpop="this script's own reading of `man git-log`",
             findpop="the ways git documents for printing a commit "
                     "identifier from `git log`")

ver = subprocess.run(["git", "--version"], capture_output=True,
                     text=True).stdout.strip()
text = L.man_text()

print("=" * 74)
print("p1 -- THE WAYS, READ FROM `man git-log`")
print("=" * 74)
print()
print("   git             : %s" % ver)
print("   documentation   : `man %s`, %d bytes after overstrike removal"
      % (L.MANPAGE, len(text)))
print("   NOT a population: the flags I remember.  Nothing below is typed")
print("                     from memory; every row names the line it is on.")
print()

# ---------------------------------------------------------------------------
print("-- (i) PLACEHOLDERS.  Population: every `%<x>` in the placeholder")
print("       list of `man git-log`.  Grain: one placeholder.")
print()

allph = L.documented_placeholders(text)
print("   placeholders parsed from the man page : %d" % len(allph))
hashish = [(p, d) for p, d in allph if "hash" in d.lower()]
print("   of those, whose description says HASH : %d" % len(hashish))
for p, d in hashish:
    print("      %-4s %s" % (p, d))
print()

commit = L.documented_commit_hash_placeholders(text)
print("   OF THOSE, A **COMMIT** HASH           : %d" % len(commit))
for p in sorted(commit):
    print("      %-4s %-8s" % (p, commit[p]))
print()
print("   The exclusions are made by READING the description, not by my")
print("   knowing which ones are trees and parents:")
for p, d in hashish:
    if p not in commit:
        print("      %-4s EXCLUDED -- %s" % (p, d))
print()

R.check(len(commit) >= 1, "no commit-hash placeholder was parsed out of the "
                          "man page; the parse is broken, not git")
R.check("%H" in commit and "%h" in commit,
        "the parse did not find both %H and %h; a reading that cannot see "
        "both cases is the defect under repair")

print("   THE TWO ARE THE SAME LETTER IN TWO CASES.  That is the whole")
print("   ticket: `_HASH_FORMATS` lists three spellings of the upper-case")
print("   one and none of the lower-case one, so the population every count")
print("   in this lineage was taken over is defined by a CAPITAL LETTER.")
print()

# ---------------------------------------------------------------------------
print("-- (ii) BUILT-IN FORMATS.  Population: the bulleted `--pretty=<name>`")
print("        list of `man git-log`.  Grain: one format name.")
print()

found = L.documented_builtin_formats(text)
for n in sorted(found):
    print("      %-12s %-8s (documented sample shows a commit identifier)"
          % (n, found[n]))
print()
print("   FOUND BY THE EXTRACTOR : %d" % len(found))
print("   DECLARED BLIND SPOTS   : %d -- handled by this instrument, NOT"
      % len(L.EXTRACTOR_BLIND))
print("                            found by the extractor, each with the")
print("                            documentation sentence that exempts it:")
for n in sorted(L.EXTRACTOR_BLIND):
    print("      %-12s %s" % (n, L.EXTRACTOR_BLIND[n]))
print()
print("   The blind spots are DECLARED rather than silent.  The closure test")
print("   in selftest_6e58.py requires handled == found + declared, so this")
print("   list cannot grow by neglect: a format that stops being found and")
print("   is not declared turns the selftest red.")
print()

R.check(set(found) <= set(L.BUILTIN_FORMATS),
        "the man page documents a hash-printing format this instrument does "
        "not handle: %s" % sorted(set(found) - set(L.BUILTIN_FORMATS)))
R.check(set(L.BUILTIN_FORMATS) - set(found) == set(L.EXTRACTOR_BLIND),
        "handled minus found is %s, and the declared blind spots are %s; "
        "an undeclared gap is an undocumented population"
        % (sorted(set(L.BUILTIN_FORMATS) - set(found)),
           sorted(L.EXTRACTOR_BLIND)))

# ---------------------------------------------------------------------------
print("-- (iii) OPTIONS.  Population: the option list of `man git-log`.")
print("         Grain: one option.")
print()

opts = L.documented_hash_options(text)
for o in sorted(opts):
    print("      %-20s %s" % (o, opts[o][:80]))
print()
print("   `--oneline` is `--pretty=oneline --abbrev-commit` by git's own")
print("   words, so it is a spelling of a hash and this instrument counts it.")
print("   `--abbrev-commit` does not by itself make a hash appear -- it")
print("   changes the GRAIN of one that already does -- so it demotes FULL")
print("   to ABBREV within the same call and is never an emitter alone.")
print()

R.check(set(opts) >= {"--oneline", "--abbrev-commit"},
        "the man page no longer documents --oneline / --abbrev-commit where "
        "this parse looks: %s" % sorted(opts))

# ---------------------------------------------------------------------------
print("-- (iv) THE DEFAULT.  A `git log` with NO format argument.")
print()

dflt = [ln.strip() for ln in text.splitlines()
        if "medium" in ln and "default" in ln.lower()]
for ln in dflt[:4]:
    print("      %s" % ln[:96])
print()
print("   git's documented default is `medium`, whose sample is")
print("   `commit <hash>`.  So a bare `git log ... ` PRINTS A FULL COMMIT")
print("   HASH AND IS REVISION-PRODUCING, and mg-330a's classifier returns")
print("   None for it.  This instrument keeps that call OUT of its headline")
print("   denominator (POP-C) and measures it separately as POP-D, because")
print("   whether an unformatted `git log` is an ANCHOR is a judgement and")
print("   not a reading -- so it is published as its own number rather than")
print("   folded into somebody else's.")
print()

R.check(bool(dflt), "the man page no longer states `medium` as the default "
                    "where this parse looks")

# ---------------------------------------------------------------------------
print("-- (v) WHAT IS OUTSIDE THIS POPULATION, NAMED RATHER THAN DROPPED")
print()
print("   The population above is `git log` calls.  These also address a")
print("   commit and are NOT counted anywhere in this instrument, because")
print("   mg-330a's taxonomy is about `git log` and changing the subcommand")
print("   set would make the before/after incomparable:")
print("      git rev-parse --short <rev>      an abbreviated object name")
print("      git rev-parse <rev>              a full object name")
print("      git show -s --format=%H          the same placeholders, elsewhere")
print("      git describe                     a name relative to a tag")
print("      git rev-list                     the same placeholders again")
print("      git for-each-ref --format=%(objectname)")
print("   Each is a real way to address a commit.  Naming them is what this")
print("   ticket does; absorbing them into a count whose label says `git log`")
print("   would be the same defect with the sign flipped.")
print()

# ---------------------------------------------------------------------------
print("-- SCORING PREDICTIONS.md")
print()
L.score(R, "P1-a", 2, len(commit), note="exactly two commit-hash placeholders")
L.score(R, "P1-b", True, len(hashish) > len(commit),
        note="tree/parent match a naive hash grep and are excluded")
L.score(R, "P1-c", lambda n: n >= 7, len(found),
        note=">= 7 built-in formats")
L.score(R, "P1-c*", True, "oneline" in found and "raw" not in found,
        note="named oneline AND raw; the widened rule finds oneline, raw is "
             "prose-only and stays a DECLARED blind spot -- PARTIAL MISS, "
             "and out_p1_builtins_FIRSTFORM.txt keeps the run where it "
             "missed both")
L.score(R, "P1-d", True, "mboxrd" not in found,
        note="predicted against myself: the extractor misses mboxrd")
L.score(R, "P1-e", True, set(opts) >= {"--oneline", "--abbrev-commit",
                                       "--no-abbrev-commit"},
        note="all three options documented")
L.score(R, "P1-f", True, bool(dflt) and
        L.BUILTIN_FORMATS.get(L.DEFAULT_FORMAT) == "FULL",
        note="the default `medium` prints a full commit hash")
print()

raise SystemExit(R.emit())
