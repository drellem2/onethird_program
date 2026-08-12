"""mg-cdd5 s1 -- WHAT BRINGING THE MIRROR CURRENT ACTUALLY BRINGS IN.

Ticket step 2 says do not assume a fetch is safe or sufficient without looking
at what else moved.  So this section does not argue; it enumerates.

Three questions, answered separately because they have different answers:

  (a) Is the update MECHANICALLY safe?  0 ahead + clean tree + ancestor =>
      `merge --ff-only` cannot lose a commit or a file.  Reported as the three
      facts, not as the word "safe".
  (b) What COMMITS does it bring?  All of them, by date, with the strike
      located inside the list rather than described as being in it.
  (c) What FILES does it touch?  Added vs modified, by directory, with the
      modified ones named in full -- a modification can withdraw a claim, an
      addition cannot withdraw one that is already being read.

Exit 1 only if the repo could not be read.
"""
import sys

import lib_cdd5 as L

STRIKE_COMMIT = "bde9610"
MIRROR_PIN = "912f1b1"


def main():
    L.banner("mg-cdd5 s1 -- WHAT THE MIRROR UPDATE BRINGS IN BESIDES THE STRIKE")
    mirror = L.find_mirror()
    if mirror is None:
        L.die_unreadable("one_third_width_three not found")
        print("== s1 exit: 1 ==")
        return 1
    st = L.read_state(mirror)

    print("(a) IS THE FAST-FORWARD MECHANICALLY SAFE?  Three facts, not a word.")
    print("    commits ahead of origin/main        : %d" % st.ahead)
    print("    uncommitted state in the working tree: %s"
          % ("YES -- DO NOT FAST-FORWARD" if st.dirty else "none"))
    print("    HEAD is an ancestor of origin/main   : %s"
          % ("YES" if L.is_ancestor(mirror, st.head, "origin/main") else "NO"))
    ff_ok = (st.ahead == 0) and (not st.dirty) and \
        L.is_ancestor(mirror, st.head, "origin/main")
    print("    => `git merge --ff-only origin/main` can lose nothing: %s"
          % ("YES" if ff_ok else "NO -- STOP"))
    if st.behind == 0:
        print("    ALREADY APPLIED: the checkout is level with origin/main, so")
        print("    the fast-forward this section costed has been done (x1).")
    print()
    print("    Note what this does NOT say.  It says the fast-forward destroys")
    print("    no work.  It does not say the 133 files it rewrites are ones a")
    print("    reader wanted rewritten; that is (c), and it is a judgement.")
    print()

    log = L.git(["log", "--reverse", "--format=%h|%ad|%s", "--date=short",
                 "%s..origin/main" % MIRROR_PIN], cwd=mirror).splitlines()
    # The count comes from the LIST, not from `behind`.  Those are different
    # quantities the moment the repair lands -- `behind` is a fact about the
    # checkout NOW, the list is a fact about the pinned range -- and the
    # header once read `0 of them` above 76 printed rows because it took the
    # number from one source and the rows from the other (README §6, D3).
    print("(b) THE COMMITS.  %d of them, %s..origin/main."
          % (len(log), MIRROR_PIN))
    print("    (the checkout is %d behind origin/main right now; before the"
          % st.behind)
    print("     repair those two numbers coincided, and they no longer must.)")
    print("    oldest first; the strike is marked.")
    print()
    for i, ln in enumerate(log, 1):
        h, d, s = ln.split("|", 2)
        mark = "  <== THE STRIKE (mg-d1be)" if h.startswith(STRIKE_COMMIT) else ""
        print("    %3d  %s  %s  %s%s" % (i, h, d, s[:96], mark))
    print()
    if not any(h.split("|")[0].startswith(STRIKE_COMMIT) for h in log):
        print("    !! THE STRIKE IS NOT IN THIS RANGE -- the ticket's premise")
        print("       does not hold as stated.  Report, do not proceed.")
    print()

    print("(c) THE FILES.  What the working copy would gain, lose, or have")
    print("    rewritten under the fast-forward.")
    ns = L.git(["diff", "--name-status", MIRROR_PIN, "origin/main"],
               cwd=mirror).splitlines()
    added = [l.split("\t", 1)[1] for l in ns if l.startswith("A")]
    modified = [l.split("\t", 1)[1] for l in ns if l.startswith("M")]
    deleted = [l.split("\t", 1)[1] for l in ns if l.startswith("D")]
    renamed = [l for l in ns if l.startswith("R")]
    print("    added    %3d" % len(added))
    print("    modified %3d" % len(modified))
    print("    deleted  %3d" % len(deleted))
    print("    renamed  %3d" % len(renamed))
    print("    total    %3d" % len(ns))
    print()
    bydir = {}
    for l in ns:
        p = l.split("\t", 1)[1]
        bydir[p.split("/")[0]] = bydir.get(p.split("/")[0], 0) + 1
    print("    by top-level directory:")
    for k in sorted(bydir, key=lambda k: -bydir[k]):
        print("      %-12s %3d" % (k, bydir[k]))
    print()
    print("    THE MODIFIED ONES, NAMED IN FULL.  These are the ones that can")
    print("    have withdrawn something a reader is currently reading as live;")
    print("    an ADDED file cannot retract a claim nobody has been sent to.")
    for p in sorted(modified):
        old = L.blob_at(mirror, MIRROR_PIN, p)
        new = L.blob_at(mirror, "origin/main", p)
        marks = L.added_markers(old, new)
        tag = ("  [strike markers added: %s]"
               % ", ".join("%s x%d" % (k, v) for k, v in sorted(marks.items()))
               ) if marks else ""
        print("      %s%s" % (p, tag))
    if deleted:
        print()
        print("    DELETED.  A citation pointing at one of these stops")
        print("    resolving entirely once the mirror is current:")
        for p in sorted(deleted):
            print("      %s" % p)
    print()
    print("    NOT MEASURED HERE: whether any of these files is cited.  That is")
    print("    s2, and keeping it separate is deliberate -- 'the update touches")
    print("    133 files' and 'the update touches a file we point readers at'")
    print("    are different claims and only the second one is a hazard.")

    print("== s1 exit: 0 ==")
    return 0


if __name__ == "__main__":
    sys.exit(main())
