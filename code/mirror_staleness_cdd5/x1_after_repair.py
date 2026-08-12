"""mg-cdd5 x1 -- THE REMEDY, DEMONSTRATED RATHER THAN ASSERTED.

Run AFTER the one-shot fast-forward of `main-mirror` onto `origin/main`.  A
repair that is only described is a claim; this reads the working copy back and
prints what a reader now sees.

It is deliberately the ONE place in this instrument that opens a file on disk,
because the disk is exactly the thing the repair was for.  Everywhere else
that would be the defect (E1); here it is the measurement.

Three things:
  (1) the checkout's ahead/behind, now
  (2) the struck bullet AS IT NOW APPEARS ON DISK, and §5.0' now resolving
  (3) the same for the two OTHER documents the sweep found, so the repair is
      shown to have covered them and not just the headline file

Exit 1 if the repair did not take.
"""
import os
import sys

import lib_cdd5 as L

MIRROR_PIN = "912f1b1"

#: The documents s2 found: cited from STATE.md or the twin (tier 1) or from
#: elsewhere in this repo (tier 2), and rewritten-with-strikes after 912f1b1.
FOUND = [
    ("docs/OneThird-L1b-Reverse-Cheeger-Proof-Attempt.md",
     "λ_std ≤ λ₂^{BK}", "STATE.md:78, STATE.md:112"),
    ("docs/OneThird-Spectral-NearOrdinalSum-KillShot-Probe.md",
     None, "STATE.md:112, docs/...mg-bb60.md:126"),
    ("docs/OneThird-StandardDominance-ComparisonRoute.md",
     None, "code/row3b_audit_eba7/OUTCOMES.md:72, docs/state-history/...:112"),
]


def main():
    L.banner("mg-cdd5 x1 -- THE REMEDY, READ BACK OFF THE REPAIRED WORKING COPY")
    mirror = L.find_mirror()
    if mirror is None:
        L.die_unreadable("one_third_width_three not found")
        print("== x1 exit: 1 ==")
        return 1

    st = L.read_state(mirror)
    print("(1) THE CHECKOUT NOW")
    print("    branch            %s" % st.branch)
    print("    HEAD              %s" % L.short(st.head))
    print("    origin/main       %s" % L.short(st.origin_main))
    print("    ls-remote main    %s" % L.short(st.remote_main))
    print("    ahead / behind    %d / %d" % (st.ahead, st.behind))
    print("    working tree      %s" % ("DIRTY" if st.dirty else "clean"))
    print()
    print("    was, before the repair: HEAD %s, 0 ahead / 76 behind" % MIRROR_PIN)
    print("    UNDO, exactly:  git -C %s reset --hard %s" % (mirror, MIRROR_PIN))
    print("    The fast-forward moved a branch pointer.  It created no commit,")
    print("    rewrote no history, and touched nothing on any other branch --")
    print("    a pre-existing stash on `mayor-a5-g2-status` is untouched.")
    print()

    ok = (st.behind == 0 and st.ahead == 0 and not st.dirty)

    print("(2) AND (3) WHAT A READER NOW SEES.  Read OFF DISK -- the one place")
    print("    in this instrument where that is the measurement and not the")
    print("    defect, because the disk is what the repair was for.")
    print()
    for path, needle, cited_from in FOUND:
        full = os.path.join(mirror, path)
        print("    %s" % path)
        print("      cited from: %s" % cited_from)
        if not os.path.isfile(full):
            print("      NOT PRESENT ON DISK -- the repair did not cover it")
            ok = False
            continue
        with open(full, encoding="utf-8", errors="replace") as fh:
            disk = fh.read()
        before = L.blob_at(mirror, MIRROR_PIN, path)
        marks_now = L.added_markers(before, disk)
        print("      strike markup the reader gains vs %s: %s"
              % (MIRROR_PIN,
                 ", ".join("%s x%d" % (k, v)
                           for k, v in sorted(marks_now.items())) or "none"))
        if not marks_now:
            print("      !! the repair did not bring the withdrawal to this file")
            ok = False
        if needle:
            for n, ln in enumerate(disk.splitlines(), 1):
                if needle in ln:
                    struck = "~~" in ln
                    print("      line %d struck on disk: %s   %s"
                          % (n, struck, ln.strip()[:80]))
                    if not struck:
                        ok = False
                    break
            print("      §5.0' resolves on disk: %s"
                  % L.section_present(disk, "5.0'"))
            if not L.section_present(disk, "5.0'"):
                ok = False
        print()

    print("    NOT FIXED BY THIS, AND SAID PLAINLY: nothing advances")
    print("    `main-mirror`.  It was created once from origin/main and never")
    print("    moved; this is a one-shot and it will go stale again.  README §4")
    print("    names the structural options and why none of them is landed from")
    print("    a branch that targets a different repository.")

    print("== x1 exit: %d ==" % (0 if ok else 1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
