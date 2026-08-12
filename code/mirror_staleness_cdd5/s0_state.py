"""mg-cdd5 s0 -- ESTABLISH THE COMMIT STATE FROM THE REMOTE AND NOT FROM THE
WORKING COPY.

Ticket step 1.  Three things are confirmed here, each with the command that
confirms it printed beside the answer:

  (1) `origin/main` of one_third_width_three really is what the tracking ref
      says -- checked against `git ls-remote`, which asks the REMOTE and not
      the local ref.  This matters: a tracking ref is itself a cached copy,
      and confirming staleness with a cached copy is the ticket's own defect
      one level up.
  (2) `bde9610` (mg-d1be's strike) is an ancestor of that.
  (3) `912f1b1` is what the checked-out `main-mirror` has, is an ancestor of
      origin/main, and is 0 ahead / N behind.

Then the consequence, read AT BOTH REVISIONS and never off disk: the struck
bullet, and whether §5.0' exists at all.

Exit 1 only if a repo could not be read.  A finding about the mirror does not
set it.
"""
import sys

import lib_cdd5 as L

STRIKE_COMMIT = "bde9610"
MIRROR_PIN = "912f1b1"
CHEEGER = "docs/OneThird-L1b-Reverse-Cheeger-Proof-Attempt.md"
CLAIM = "λ_std ≤ λ₂^{BK}"


def main():
    L.banner("mg-cdd5 s0 -- THE COMMIT STATE, ESTABLISHED FROM THE REMOTE")

    prog = L.program_root()
    mirror = L.find_mirror()

    print("REPOS")
    print("  onethird_program       %s" % prog)
    print("  one_third_width_three  %s" % (mirror or "NOT FOUND"))
    print()
    if mirror is None:
        L.die_unreadable("one_third_width_three not found; tried %r"
                         % [c for c in L.MIRROR_CANDIDATES if c])
        print("== s0 exit: 1 ==")
        return 1

    st = L.read_state(mirror)
    ps = L.read_state(prog)
    if not st.ok or st.error:
        L.die_unreadable(st.error or "unknown")
        print("== s0 exit: 1 ==")
        return 1

    print("COMMANDS AND THEIR ANSWERS  (mirror repo = one_third_width_three)")
    print("  git ls-remote origin refs/heads/main")
    print("      %s      <-- THE REMOTE'S OWN ANSWER" % (st.remote_main or "UNREADABLE"))
    print("  git rev-parse origin/main")
    print("      %s      <-- the local tracking ref" % st.origin_main)
    agree = (st.remote_main == st.origin_main)
    print("  agree: %s%s" % (
        "YES" if agree else "NO",
        "" if agree else "   <-- the tracking ref is itself stale; every figure"
                         " below is against the tracking ref and is suspect"))
    print()
    print("  git rev-parse --abbrev-ref HEAD")
    print("      %s" % st.branch)
    print("  git rev-parse HEAD")
    print("      %s" % st.head)
    print("  git rev-list --left-right --count HEAD...origin/main")
    print("      %d ahead, %d behind" % (st.ahead, st.behind))
    print("  git status --porcelain")
    print("      %s" % ("DIRTY -- uncommitted state present" if st.dirty
                        else "clean (no output)"))
    print()

    anc_strike = L.is_ancestor(mirror, STRIKE_COMMIT, "origin/main")
    anc_pin = L.is_ancestor(mirror, MIRROR_PIN, "origin/main")
    pin_is_head = st.head.startswith(MIRROR_PIN)
    print("  git merge-base --is-ancestor %s origin/main   -> %s"
          % (STRIKE_COMMIT, "YES" if anc_strike else "NO"))
    print("  git merge-base --is-ancestor %s origin/main   -> %s"
          % (MIRROR_PIN, "YES" if anc_pin else "NO"))
    print("  HEAD starts with %s                            -> %s"
          % (MIRROR_PIN, "YES" if pin_is_head else "NO"))
    print()

    for rev, tag in ((STRIKE_COMMIT, "the strike"), (MIRROR_PIN, "the mirror"),
                     ("origin/main", "the tip")):
        subj = L.git(["log", "-1", "--format=%h %ad  %s", "--date=short", rev],
                     cwd=mirror).strip()
        print("  %-12s %s" % (tag, subj[:150]))
    print()

    print("THE CONSEQUENCE, READ AT BOTH REVISIONS AND NEVER OFF DISK")
    print("  file: %s" % CHEEGER)
    old = L.blob_at(mirror, MIRROR_PIN, CHEEGER)
    new = L.blob_at(mirror, "origin/main", CHEEGER)
    if old is L.MISSING or new is L.MISSING:
        print("  UNREADABLE at one of the two revisions -- refusing to compare.")
        print("== s0 exit: 1 ==")
        return 1

    def find_claim(text):
        for n, ln in enumerate(text.splitlines(), 1):
            if CLAIM in ln:
                return n, ln.strip()
        return None, None

    n_old, ln_old = find_claim(old)
    n_new, ln_new = find_claim(new)
    print("    at %s (WHAT A READER OF THE CHECKED-OUT TREE SEES):" % MIRROR_PIN)
    print("      line %s: %s" % (n_old, (ln_old or "")[:110]))
    print("      struck? %s" % ("YES" if ln_old and "~~" in ln_old else
                                "NO  <-- THE CLAIM STANDS UNSTRUCK"))
    print("    at origin/main:")
    print("      line %s: %s" % (n_new, (ln_new or "")[:110]))
    print("      struck? %s" % ("YES" if ln_new and "~~" in ln_new else "NO"))
    print()

    for label in ("5", "5.0'"):
        print("    section %-5s present at %s: %-5s   at origin/main: %s"
              % ("§" + label, MIRROR_PIN,
                 L.section_present(old, label),
                 L.section_present(new, label)))
    print()
    print("    §5.0' IS THE SECTION STATE.md:78 CITES.  It does not occur in the")
    print("    mirror's copy at all -- so the citation does not merely land on")
    print("    stale text, HALF OF IT DOES NOT RESOLVE.")
    print()

    print("THIS REPOSITORY (onethird_program) -- stated so the pin is checkable")
    print("  HEAD            %s  (branch %s)" % (L.short(ps.head), ps.branch))
    print("  origin/main     %s" % L.short(ps.origin_main))
    print()
    print("PIN.  Every figure in this instrument is measured against")
    print("  one_third_width_three origin/main = %s" % L.short(st.origin_main))
    print("  If that ref moves, THIS TRANSCRIPT GOES STALE -- which is the defect")
    print("  it is about (PREDICTIONS.md E2).  Re-run rather than quote.")

    print("== s0 exit: 0 ==")
    return 0


if __name__ == "__main__":
    sys.exit(main())
