"""t1 -- THE POPULATION AND ITS LINEAGE, before any verdict is taken about it.

Every count this census prints is a count over one of the populations defined
here.  They are defined in their own script, and printed before anything is
measured, so that a reader can reject the population without having to reverse
out the arithmetic.

It also settles one thing the ticket asks about directly: THE CARRYING COMMIT
IS NOT WHAT THE TRANSCRIPT NAMES.  The ticket's widened question is "FOR EACH
COMMITTED FIGURE, WHICH REVISION IS IT A FACT ABOUT, AND IS THAT THE REVISION
IT NAMES?"  t1 measures the second half of that -- what the revision NAMED is,
where anything is named at all -- and leaves the first half to t2, which has to
re-run things to answer it.
"""

import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_1abe as L                                          # noqa: E402


def main():
    rev = L.main_rev()
    head = L.resolve(rev)
    led = L.Ledger("t1 -- THE POPULATIONS OF THIS CENSUS, AND THEIR LINEAGE")
    print("    as-of      %s  (%s)" % (head, rev))

    led.head("T1a -- THE CLASS 2 POPULATION: COMMITTED TRANSCRIPTS")
    print("""
DEFINITION  every tracked path matching `code/<dir>/out_*.txt` at the revision
            above.  One level of directory, `out_` prefix, `.txt` suffix.
WHY THIS    it is the arc's own naming convention for a committed run: every
            `run_all.sh` in this repository redirects into exactly this shape.
            The definition is mechanical, so a reader can recompute the
            denominator with one `git ls-tree` and no reference to this script.
WHAT IT     a transcript kept under another name.  `selfcheck_output.txt` in
MISSES      code/counterexample_audit_a7b4/ is one, named here rather than
            silently absorbed or silently dropped.
""")
    population = L.transcripts(rev)
    dirs = collections.Counter(p.split("/")[1] for p in population)
    carry = {p: L.carrying_commit(p, rev) for p in population}
    groups = {(p.split("/")[1], carry[p]) for p in population}
    print("    transcripts                       %d" % len(population))
    print("    directories holding one           %d" % len(dirs))
    print("    distinct carrying commits         %d" % len({c for c in
                                                            carry.values()}))
    print("    distinct (directory, commit) pairs %d" % len(groups))
    print("    commits on %s in all              %d"
          % (rev, len(L.git("rev-list", head).split())))
    led.record(None,
               "T1a the CLASS 2 denominator is %d transcripts over %d "
               "directories and %d carrying commits.  Every CLASS 2 count in "
               "this census is over this population and no other"
               % (len(population), len(dirs), len({c for c in carry.values()})))

    others = [p for p in L.git("ls-tree", "-r", "--name-only", rev,
                               "code/").split("\n")
              if p.endswith(".txt") and p not in population and p.strip()]
    print()
    print("    tracked `.txt` under code/ that this definition EXCLUDES: %d"
          % len(others))
    for p in sorted(others):
        print("      %s" % p)
    led.record(None,
               "T1a' %d tracked `.txt` files under code/ are outside the "
               "population, named above.  A denominator whose exclusions are "
               "not printed is a denominator nobody can argue with"
               % len(others))

    led.head("T1b -- WHAT THE TRANSCRIPTS THEMSELVES NAME")
    print("""
The ticket's widened question, asked of the record rather than of a re-run.
GRAIN one verdict per transcript.
""")
    named, unnamed = 0, 0
    mismatch = 0
    for p in population:
        blob = L.blob_at(carry[p], p)
        text = blob.decode("utf-8", "replace") if blob else ""
        import re
        found = None
        for m in re.finditer(r"(?<![0-9A-Za-z])([0-9a-f]{7,40})(?![0-9A-Za-z])",
                             text):
            if L.resolve(m.group(1)):
                found = L.resolve(m.group(1))
                break
        if found is None:
            unnamed += 1
        else:
            named += 1
            if found != carry[p]:
                mismatch += 1
    print("    name at least one resolvable commit   %d of %d" % (named,
                                                                  len(population)))
    print("    name none                             %d of %d" % (unnamed,
                                                                  len(population)))
    print("    name a commit OTHER than the one carrying them   %d of %d named"
          % (mismatch, named))
    led.record(None,
               "T1b %d of %d transcripts name no commit at all, so for those "
               "the question `is it the revision it names` HAS NO ANSWER -- "
               "not a good one and not a bad one.  That is the largest single "
               "obstacle to the ticket's framing and it is a property of the "
               "record, not of the rebase" % (unnamed, len(population)))

    led.head("T1c -- LINEAGE: WHOSE NUMBERS THIS CENSUS REPEATS")
    print("""
Every figure this census takes from somebody else, named, with whether it was
re-derived here.  A number carried forward without this line cannot be chased.

  mg-f3ff / mg-fcb2 / mg-65eb pre-registration displacements
        WHOSE   the mayor's, quoted in the mg-1abe brief.
        HERE    RE-DERIVED in t4d from the object store, not repeated.

  "the ten figures of mg-b2af's transcript reproduce at b94cb1e"
        WHOSE   mg-b2af, via the ticket.
        HERE    NOT re-derived.  b94cb1e is checked for existence in this
                object store and nothing more; the ten figures are not re-run.

  "the six c067 transcripts do not reproduce from the code committed with them"
        WHOSE   mg-c3a2, via the ticket.
        HERE    RE-DERIVED in t2: those six are in the CLASS 2 population and
                were re-run at their carrying commit like every other member.

  "unreachable[:3] is a silent cap in c2_anchors.py"
        WHOSE   mg-c3a2, via the ticket.
        HERE    RE-DERIVED in t6a, and found ALREADY FIXED on main by mg-c3a2
                itself in 5bd0d71.  Disclosed as D3 in PREDICTIONS.md.

  "a publisher is not a pin"
        WHOSE   mg-bf79.  Its finding is not re-derived here; its LESSON is
                built into the convention in t5, where the code-digest excludes
                the transcripts precisely so that publishing cannot invalidate
                the declaration.
""")
    b94 = L.resolve("b94cb1e")
    led.record(None,
               "T1c b94cb1e %s in this object store.  That is the ONLY claim "
               "this census makes about mg-b2af's sighting; its ten figures "
               "are not re-derived here and any reader treating this row as "
               "confirmation of them is reading more than is written"
               % ("resolves" if b94 else "DOES NOT resolve"))
    return led.done()


if __name__ == "__main__":
    sys.exit(main())
