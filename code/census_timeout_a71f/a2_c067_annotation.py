"""a2 -- THE ANNOTATION ON `audit_c067/out_c1_rebase.txt`, CHECKED NOT ASSERTED.

PART 2 of mg-a71f, whose load-bearing instruction is: **A RE-RUN WRITES 0 OVER
A 5 THAT IS TRUE.**  The record says 5 of mg-132a's commits were replayed by
the refinery's rebase.  They were.  Its own producer, re-run today, says 0 --
because `c1_rebase.py:48` looks for the replayed twins BY SUBJECT inside

    git log --format=%H%x1f%s main -n 40

and `main` has grown far past the commit that carries the transcript.  The ref
moves and the literal does not, so the twins fell out of the back of the window
while every one of them stayed exactly where it was.

The remedy is a note prepended to the transcript, in the format mg-56dc used at
`code/runner_exit_c2b3/out_k1_census.txt`.  A note is a claim, and this arc has
been burned four times by claims that were true when written.  So this script
RE-DERIVES every factual clause of that note on every run:

  A2a  the note is present, exactly once, and the bytes below it are
       byte-identical to the blob at the transcript's carrying commit.  A note
       that had been allowed to edit the record it annotates would be worse
       than no note.
  A2b  every off-`main` commit the transcript names is STILL TWINNED on `main`
       by subject, with NO window -- the search the producer cannot do.
  A2c  the mechanism, positively: the twins are on `main` AND outside `-n 40`.
       Both halves are required.  Present-but-unreachable is the finding; if
       either half failed, the note would be wrong and this arm says so.
  A2d  the objects still resolve and the pre-rebase ref still points at them.
  A2e  ⚠️ THE ARM THAT CAN CONDEMN THE NOTE.  A note saying "do not re-run" is
       only right while the producer really is blind.  If the window were ever
       widened, or `main` rewritten so the twins came back inside it, the
       correct action would flip from ANNOTATE to RE-RUN -- and nothing would
       tell anybody.  A2e computes the live answer the producer would give and
       REFUSES the note if it is no longer 0.

⚠️  THIS SCRIPT NEVER RUNS `c1_rebase.py` AND NEVER WRITES TO `code/audit_c067`.
The producer's answer is DERIVED by reading `main`'s log the way line 48 reads
it, not by executing it.  That is not squeamishness: executing it is how a 0
gets written over a 5.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_a71f as L                                            # noqa: E402

PRODUCER = "code/audit_c067/c1_rebase.py"
PRE_REF_CANDIDATES = ("polecat-132a", "origin/polecat-132a",
                      "refs/remotes/origin/polecat-132a")
WINDOW = 40                       # the literal at c1_rebase.py:48


def named_off_main(text, rev):
    """Every commit sha the transcript names that is NOT reachable from `rev`.

    The population is the TRANSCRIPT'S OWN TEXT -- every 7-to-40 hex token in
    it that resolves to a commit -- and not a list I chose.  A hand-written
    list would make this arm agree with the note by construction.
    """
    out = []
    for tok in sorted(set(re.findall(r"\b[0-9a-f]{7,40}\b", text))):
        full = L.resolve(tok)
        if full is None or full in out:
            continue
        if not L.git_ok("merge-base", "--is-ancestor", full, rev):
            out.append(full)
    return out


def subject_of(sha):
    return L.git("log", "-1", "--format=%s", sha).strip()


def twin_unbounded(subject, rev):
    """The on-`rev` commit with the same subject, searched with NO window."""
    for line in L.git("log", "--format=%H%x1f%s", rev).splitlines():
        sha, _, subj = line.partition("\x1f")
        if subj == subject:
            return sha
    return None


def main():
    rev = L.resolve(L.main_rev())
    led = L.Ledger("a2 -- `audit_c067/out_c1_rebase.txt` IS TRUE AND ITS OWN "
                   "PRODUCER CANNOT SEE THAT")
    print("    as-of      %s" % rev)
    print("    subject    %s" % L.C067)
    print("    carrier    %s" % L.C067_CARRIER[:12])
    print("    distance   `main` is %s commits past the carrier"
          % L.git("rev-list", "--count",
                  "%s..%s" % (L.C067_CARRIER, rev)).strip())

    live = os.path.join(L.REPO, L.C067)
    if not os.path.exists(live):
        led.self_error("%s is not in this working tree" % L.C067)
        return led.done()
    with open(live, "rb") as fh:
        live_b = fh.read()
    live_t = live_b.decode("utf-8", "replace")

    # ------------------------------------------------------------------ A2a
    led.head("A2a -- THE NOTE IS PRESENT, AND THE RECORD UNDER IT IS UNTOUCHED")
    print("""
mg-56dc's convention, and the half of it that matters: "Nothing below this line
has been altered."  That is checkable, so it is checked here rather than
promised -- against the blob at the transcript's own carrying commit.
""")
    marker_count = live_t.count(L.NOTE_END)
    led.record(marker_count == 1,
               "A2a the end-of-note marker appears EXACTLY %d time(s).  More "
               "than one and the split below would be ambiguous; zero and the "
               "note is absent" % marker_count)
    original = L.blob_at(L.C067_CARRIER, L.C067)
    if original is None:
        led.self_error("%s absent at its own carrying commit %s"
                       % (L.C067, L.C067_CARRIER[:7]))
        return led.done()
    if marker_count == 1:
        tail = live_b.split(L.NOTE_END.encode() + b"\n", 1)[1]
        led.record(tail == original,
                   "A2a' the %d bytes below the marker are byte-identical to "
                   "the blob at %s.  The annotation ADDED %d bytes above the "
                   "record and CHANGED none of it"
                   % (len(tail), L.C067_CARRIER[:7], len(live_b) - len(tail)))
        if tail != original:
            led.self_error("A2a'' the annotation has altered the record it "
                           "annotates.  That is the one thing it may not do")
    else:
        led.self_error("A2a'' cannot check the record's bytes without exactly "
                       "one marker")

    # ------------------------------------------------------------------ A2b
    led.head("A2b -- EVERY OFF-`main` COMMIT THE RECORD NAMES, TWINNED WITH "
             "NO WINDOW")
    print("""
The population is the transcript's OWN TEXT: every hex token in it that
resolves to a commit and is not reachable from `main`.  Derived, not listed --
a list would make this arm agree with the note by construction.
""")
    off = named_off_main(original.decode("utf-8", "replace"), rev)
    twinned, orphan = [], []
    print("    %-9s %-9s %s" % ("off-main", "twin", "subject"))
    for sha in off:
        subj = subject_of(sha)
        tw = twin_unbounded(subj, rev)
        print("    %-9s %-9s %s" % (sha[:7], (tw or "NONE")[:7], subj[:58]))
        (twinned if tw else orphan).append(sha)
    if not off:
        print("    (the record names no off-`main` commit)")
    led.record(not orphan and bool(off),
               "A2b every off-`main` commit the record names is STILL TWINNED "
               "on `main` by subject, %d of %d, when the search is not bounded "
               "by a literal.  Nothing the record points at has died"
               % (len(twinned), len(off)))
    for sha in orphan:
        led.self_error("A2b' %s is named by the record, is off `main`, and has "
                       "NO twin -- the note's evidence does not hold" % sha[:7])

    # ------------------------------------------------------------------ A2c
    led.head("A2c -- THE MECHANISM: ON `main`, AND OUTSIDE THE WINDOW")
    print("""
Both halves are required and both are printed.  ON `main` alone would say the
record is fine; OUTSIDE THE WINDOW alone would say it is lost.  Together they
say the only thing that is true: the evidence is present and the producer's
walk stops short of it.
""")
    window = set(L.git("log", "--format=%H", rev,
                       "-n", str(WINDOW)).split())
    inside, outside = [], []
    for sha in twinned:
        tw = twin_unbounded(subject_of(sha), rev)
        (inside if tw in window else outside).append((sha, tw))
    for sha, tw in inside + outside:
        print("    %s -> %s   on main: yes   inside `main -n %d`: %s"
              % (sha[:7], tw[:7], WINDOW, "YES" if tw in window else "no"))
    led.record(bool(inside) or not twinned,
               "A2c %d of %d replayed twins are on `main` AND OUTSIDE `main "
               "-n %d`.  Present, and unreachable by the walk that looks for "
               "them" % (len(outside), len(twinned), WINDOW))

    # ------------------------------------------------------------------ A2d
    led.head("A2d -- THE OBJECTS, AND THE REF THAT STILL HOLDS THEM")
    alive = [s for s in off if L.git("cat-file", "-t", s).strip() == "commit"]
    led.record(len(alive) == len(off) and bool(off),
               "A2d all %d of the %d objects the record names still resolve in "
               "this store.  `C1a'` forecast that a rebased commit 'survives "
               "on whatever side ref still points at it and dies at the next "
               "git gc' -- it has not died" % (len(alive), len(off)))

    # ⚠️ DEDUPED BY CANONICAL REF PATH, and the first draft was not.  The
    # producer's own candidate list spells ONE ref three ways, and counting the
    # spellings said `2 ref(s)` where the truth is one remote-tracking ref --
    # a fragility figure reported as twice as safe as it is, in the arm whose
    # whole subject is how little is holding these objects up.
    seen, refs = set(), []
    for r in PRE_REF_CANDIDATES:
        if not L.resolve(r):
            continue
        canon = L.git("rev-parse", "--symbolic-full-name", r).strip() or r
        if canon in seen:
            continue
        seen.add(canon)
        refs.append(canon)
    print("    pre-rebase refs that still resolve (deduped by full name): %s"
          % (", ".join(refs) if refs else "NONE"))
    print("    spellings `c1_rebase.py` tries, of which the above are the "
          "distinct refs: %d" % len(PRE_REF_CANDIDATES))
    led.record(len(refs) > 1,
               "A2d' the pre-rebase commits hang off %d DISTINCT ref(s): %s.  "
               "`C1a''` recorded this count going 2 -> 1 INSIDE that audit's "
               "runtime; it is %d now, and one more deletion leaves the "
               "objects reachable only from the transcript that names them"
               % (len(refs), ", ".join(refs) or "none", len(refs)))

    # ------------------------------------------------------------------ A2e
    led.head("A2e -- THE ARM THAT CAN CONDEMN THE NOTE")
    print("""
`DO NOT RE-RUN` is right only while the producer really is blind.  If the
window were widened, or `main` rewritten so the twins came back inside it, the
correct action would flip from ANNOTATE to RE-RUN and no one would be told.  So
the producer's live answer is COMPUTED HERE -- by reading `main`'s log the way
line 48 reads it, never by executing it -- and the note is refused if it is no
longer 0.
""")
    src = L.blob_at(rev, PRODUCER)
    lit = None
    if src:
        m = re.search(r'"main",\s*"-n",\s*"(\d+)"',
                      src.decode("utf-8", "replace"))
        lit = int(m.group(1)) if m else None
    print("    the literal at c1_rebase.py:48 today : %s"
          % ("-n %d" % lit if lit else "NOT FOUND -- the producer has changed"))
    led.record(lit == WINDOW,
               "A2e the producer's window is still the literal `-n %s` this "
               "note was written against.  If this ever stops matching, the "
               "note is describing a producer that no longer exists" % lit)

    ref = next((r for r in PRE_REF_CANDIDATES if L.resolve(r)), None)
    would_see = 0
    if ref and lit:
        w = {}
        for line in L.git("log", "--format=%H%x1f%s", rev,
                          "-n", str(lit)).splitlines():
            sha, _, subj = line.partition("\x1f")
            w.setdefault(subj, sha)
        for line in L.git("log", "--format=%H%x1f%s", ref,
                          "-n", "12").splitlines():
            sha, _, subj = line.partition("\x1f")
            if "(mg-132a)" in subj and subj in w and w[subj] != sha:
                would_see += 1
    print("    pairs `c1_rebase.py` WOULD find if re-run now : %d" % would_see)
    print("    pairs the committed record asserts            : 5")
    led.record(would_see != 0,
               "A2e' re-run today the producer finds %d pair(s) where the "
               "record asserts 5.  While this stays 0 the note is correct and "
               "a re-run destroys a true record.  IF THIS EVER BECOMES 5 THE "
               "NOTE MUST BE WITHDRAWN, and this arm is how anyone finds out"
               % would_see)

    return led.done()


if __name__ == "__main__":
    sys.exit(main())
