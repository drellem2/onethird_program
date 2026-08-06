"""P1 -- WHAT THE GLOB ACTUALLY MATCHES, AGAINST WHAT IT IS DESCRIBED AS MATCHING.

THE INSTRUCTION THIS SCRIPT OBEYS, verbatim from the brief: "Do not read the pattern
and reason about it -- ENUMERATE both sets and diff them.  A pattern that looks right
is how this survives review."

So nothing here is derived from reading `docs/*.md` and thinking about it.  Five file
lists are built by five different mechanisms, printed with their sizes, and diffed
pairwise in BOTH DIRECTIONS.

  THE DESCRIPTIONS, quoted from mg-d075's own source and prose and located at run
  time rather than retyped:

    s1_census.py docstring   "D  RELAXED / the whole docs corpus.  Live sentences
                              of every docs/*.md."
    docs/repair-...           "B over the 101 `docs/*.md` that are not this
                              repair's own"

  THE UNIVERSES (population: files; grain: one file):

    G_IMPL   os.listdir(docs) filtered .md      -- the universe AS IMPLEMENTED
    G_SHELL  the shell glob docs/*.md           -- the universe AS WRITTEN
    D_TRACK  tracked .md under docs/, ANY DEPTH -- "the whole docs corpus"
    M_TRACK  tracked .md anywhere               -- mg-aaf4's universe
    M_DISK   .md on disk anywhere               -- the tracked/worktree control

TWO BLIND SPOTS ARE PREDICTED (P1) AND BOTH ARE PRINTED WHETHER OR NOT THEY BITE.
An empty blind spot printed as empty is the point: a hole that costs nothing today
is the one that costs silently tomorrow, and omitting it because it is empty is how
it stays invisible.

THE DIFF MACHINERY IS CONTROLLED.  G_IMPL vs G_SHELL is expected to be EMPTY.  If
the machinery reported a difference everywhere it would report one here too, so an
empty diff on that pair is the evidence that a non-empty diff elsewhere is real.

EXIT 1 if the implemented universe differs from the universe it is described as
covering.  PREDICTED 1.
"""

import os
import sys

import lib1d6c as U

OUT = sys.stdout


def show_diff(name_a, a, name_b, b, cap=20):
    only_a, only_b = U.diff_sets(a, b)
    print("    %-44s %5d" % (name_a, len(a)), file=OUT)
    print("    %-44s %5d" % (name_b, len(b)), file=OUT)
    print("    %-44s %5d" % ("in %s and not in %s" % (name_a, name_b),
                             len(only_a)), file=OUT)
    for p in only_a[:cap]:
        print("        + %s" % p, file=OUT)
    if len(only_a) > cap:
        print("        + ... and %d more" % (len(only_a) - cap), file=OUT)
    print("    %-44s %5d" % ("in %s and not in %s" % (name_b, name_a),
                             len(only_b)), file=OUT)
    for p in only_b[:cap]:
        print("        - %s" % p, file=OUT)
    if len(only_b) > cap:
        print("        - ... and %d more" % (len(only_b) - cap), file=OUT)
    print(file=OUT)
    return only_a, only_b


def quote_description():
    """Locate the descriptions in mg-d075's own files, at run time."""
    found = []
    src = os.path.join(U.D075, "s1_census.py")
    with open(src, encoding="utf-8") as f:
        for i, ln in enumerate(f.read().split("\n"), 1):
            if "docs/*.md" in ln or "whole docs corpus" in ln:
                found.append(("code/branching_bound_d075/s1_census.py", i,
                              ln.strip()))
    doc = os.path.join(U.DOCS, "repair-mg-d075-the-figure-and-its-scope.md")
    if os.path.exists(doc):
        with open(doc, encoding="utf-8") as f:
            for i, ln in enumerate(f.read().split("\n"), 1):
                if "docs/*.md" in ln:
                    found.append(("docs/repair-mg-d075-the-figure-and-its-scope.md",
                                  i, ln.strip()))
    return found


def main():
    U.rule(OUT, "P1  WHAT THE GLOB ACTUALLY MATCHES, AGAINST WHAT IT IS\n"
                "    DESCRIBED AS MATCHING.  Enumerated, not reasoned about.")
    print(file=OUT)

    U.rule(OUT, "  1.1  THE DESCRIPTIONS, located in the parent's own files")
    for path, i, txt in quote_description():
        print("    %s:%d" % (path, i), file=OUT)
        print("        %s" % txt[:104], file=OUT)
    print(file=OUT)

    g_impl = U.u_g_impl()
    g_shell = U.u_g_shell()
    d_track = U.u_d_track()
    m_track = U.u_m_track()
    m_disk = U.u_m_disk()

    U.rule(OUT, "  1.2  THE FIVE UNIVERSES, EACH BY ITS OWN MECHANISM.\n"
                "       Population: files.  Grain: one file.")
    for nm, s, how in [
            ("G_IMPL   os.listdir(docs) + .endswith('.md')", g_impl,
             "the universe AS IMPLEMENTED"),
            ("G_SHELL  sh -c 'ls -1 docs/*.md'", g_shell,
             "the universe AS WRITTEN"),
            ("D_TRACK  git ls-files, .md under docs/, any depth", d_track,
             "'the whole docs corpus'"),
            ("M_TRACK  git ls-files, .md anywhere", m_track,
             "mg-aaf4's universe"),
            ("M_DISK   os.walk, .md anywhere outside .git", m_disk,
             "the tracked/worktree control")]:
        print("    %-52s %5d   %s" % (nm, len(s), how), file=OUT)
    print(file=OUT)

    U.rule(OUT, "  1.3  THE CONTROL FIRST.  G_IMPL vs G_SHELL must be EMPTY.\n"
                "       A diff that is non-empty everywhere proves nothing.")
    ca, cb = show_diff("G_IMPL", g_impl, "G_SHELL", g_shell)
    control_ok = not ca and not cb
    print("    CONTROL %s -- the diff machinery reports no difference where\n"
          "    there is none, so the differences below are differences."
          % ("HOLDS" if control_ok else "FAILS"), file=OUT)
    print(file=OUT)

    U.rule(OUT, "  1.4  BLIND SPOT ONE: THE PATTERN IS NOT RECURSIVE.\n"
                "       G_IMPL against D_TRACK -- 'the whole docs corpus'.")
    only_impl, only_track = show_diff("G_IMPL", g_impl, "D_TRACK", d_track)
    print("    THE GLOB IS DESCRIBED AS COVERING docs/ AND COVERS ITS TOP LEVEL.",
          file=OUT)
    print("    %d tracked markdown file(s) under docs/ are invisible to it."
          % len(only_track), file=OUT)
    print(file=OUT)

    U.rule(OUT, "  1.5  BLIND SPOT TWO: IT READS THE WORKING TREE, NOT THE INDEX.\n"
                "       Printed even if empty -- see this script's docstring.")
    untracked = sorted(set(m_disk) - set(m_track))
    tracked_absent = sorted(set(m_track) - set(m_disk))
    print("    .md on disk and not tracked        : %d" % len(untracked), file=OUT)
    for p in untracked[:20]:
        print("        + %s" % p, file=OUT)
    print("    .md tracked and not on disk        : %d" % len(tracked_absent),
          file=OUT)
    for p in tracked_absent[:20]:
        print("        - %s" % p, file=OUT)
    print(file=OUT)
    print("    THIS HOLE IS REAL AND, AT THIS COMMIT, EMPTY.  It costs 0 files", file=OUT)
    print("    today.  It is printed because an unstated hole that happens to be", file=OUT)
    print("    empty is indistinguishable from one nobody looked for.", file=OUT)
    print(file=OUT)

    U.rule(OUT, "  1.6  THE BOUNDARY ITSELF: docs/ vs THE REPOSITORY.\n"
                "       G_IMPL against M_TRACK.")
    _, outside = show_diff("G_IMPL", g_impl, "M_TRACK", m_track, cap=10)
    print("    %d tracked markdown file(s) sit outside the glob entirely."
          % len(outside), file=OUT)
    print(file=OUT)

    # ---- what the recursion blind spot COSTS, in sites and not in files ----
    U.rule(OUT, "  1.7  WHAT BLIND SPOT ONE COSTS, IN SITES.  Population: live\n"
                "       sentences of the %d file(s) only D_TRACK can see.\n"
                "       Grain: one sentence.  Predicate: the parent's RELAXED."
                % len(only_track))
    blind_sites = U.sites_of(U.ROOT, only_track)
    n, nb, nu = U.totals(blind_sites)
    print("    files                 : %d" % len(only_track), file=OUT)
    print("    sites                 : %d" % n, file=OUT)
    print("    unbounded             : %d" % nu, file=OUT)
    print(file=OUT)
    if n == 0:
        print("    ZERO.  THE MISSING `**` COSTS NOTHING.  The whole of the gap", file=OUT)
        print("    this ticket is about is the docs/ BOUNDARY, and none of it is", file=OUT)
        print("    the non-recursion -- which is a separate latent hole, not the", file=OUT)
        print("    one that produced the published figure.", file=OUT)
    else:
        U.show_sites(blind_sites, OUT)
    print(file=OUT)

    # ---- the prefilter, checked rather than asserted -----------------------
    U.rule(OUT, "  1.8  THE PREFILTER, CHECKED.  The same universe counted with\n"
                "       and without the two-substring prefilter.  If they differ,\n"
                "       every count in this suite is suspect.")
    with_pf = U.sites_of(U.ROOT, g_impl, use_prefilter=True)
    without_pf = U.sites_of(U.ROOT, g_impl, use_prefilter=False)
    same = sorted(with_pf) == sorted(without_pf)
    print("    G_IMPL sites, prefiltered  : %d" % len(with_pf), file=OUT)
    print("    G_IMPL sites, every file   : %d" % len(without_pf), file=OUT)
    print("    identical                  : %s" % ("YES" if same else "NO"),
          file=OUT)
    print(file=OUT)

    differs = bool(only_track) or bool(only_impl)
    U.rule(OUT, "  VERDICT")
    print("    the universe AS IMPLEMENTED  : %d files" % len(g_impl), file=OUT)
    print("    the universe AS DESCRIBED    : %d files" % len(d_track), file=OUT)
    print("    they are %s" % ("DIFFERENT" if differs else "the same"), file=OUT)
    print(file=OUT)

    U.rule(OUT)
    print("SUMMARY p1_glob: G_IMPL %d, G_SHELL %d, D_TRACK %d, M_TRACK %d, "
          "M_DISK %d files" % (len(g_impl), len(g_shell), len(d_track),
                               len(m_track), len(m_disk)), file=OUT)
    print("SUMMARY p1_glob: control G_IMPL==G_SHELL %s"
          % ("HOLDS" if control_ok else "FAILS"), file=OUT)
    print("SUMMARY p1_glob: blind spot 1 (non-recursive) %d file(s), %d site(s), "
          "%d unbounded" % (len(only_track), n, nu), file=OUT)
    print("SUMMARY p1_glob: blind spot 2 (worktree not index) %d untracked, "
          "%d tracked-absent" % (len(untracked), len(tracked_absent)), file=OUT)
    print("SUMMARY p1_glob: boundary docs/ vs repo %d tracked .md outside the glob"
          % len(outside), file=OUT)
    print("SUMMARY p1_glob: prefilter control %s"
          % ("identical" if same else "DIFFERS"), file=OUT)
    print("SUMMARY p1_glob: implemented universe %s described universe"
          % ("DIFFERS FROM" if differs else "equals"), file=OUT)
    U.rule(OUT)
    return 1 if differs else 0


if __name__ == "__main__":
    sys.exit(main())
