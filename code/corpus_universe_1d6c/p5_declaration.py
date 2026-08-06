"""P5 -- THE GATE THAT DECLARES WHAT IT CANNOT REPAIR, WITH ITS SIZE.

THE ASK, verbatim from the ticket: "WHAT mg-d075 COULD HAVE DONE IS NAME THE
POPULATION AS EXCLUDED, INSTEAD OF DRAWING THE GLOB SO THAT IT NEVER APPEARED.
DECLARE the excluded population at the gate, with its size, so a reader sees a stated
exclusion rather than a clean sweep."

So this is that gate.  It differs from every check in this lineage in one way: IT
COUNTS THE WHOLE POPULATION AND THEN SAYS, BY NAME AND WITH A NUMBER, WHICH PARTS OF
IT IT WILL NOT ACT ON.  A gate that reports 12 because 12 is all it can see is
indistinguishable from a gate that reports 12 because 12 is all there is.  A gate
that reports 24, of which 10 are pre-registrations it will never reword and 12 are
dated records it will never edit, is not.

  G1  THE POPULATION.  Every `.md` tracked by git, via `git ls-files`.  Never
      `os.listdir`.  Grain: one live sentence.  Predicate: the arc's RELAXED.

  G2  THE PARTITION.  Every unbounded site is assigned exactly one class by a
      mechanical rule on its path.  A site matching no rule is UNCLASSIFIED and the
      gate FAILS -- that is the whole safety property: a population this gate has
      not thought about cannot pass through it silently.

        PRE-REGISTRATION   any `PREDICTIONS.md`.  This lineage never rewords one.
                           Repairing these would break a different invariant, and
                           mg-d075 could not have repaired them either.
        DATED RECORD       any `docs/` file that is an audit or repair account.
                           Editing one destroys the evidence trail the arc runs on.
        LIVING DOCUMENT    `docs/OneThird-Branching-Graphs-Where-This-Lives.md`.
                           Reworded freely; unbounded sites here ARE defects.
        INSTRUMENT README  `code/*/README.md`.  Ordinary prose about an instrument.
                           Unbounded sites here are REPAIRABLE.

  G3  THE ACTIONABLE SET -- what a reader is actually being asked to do.

  G4  THE DECLARATION, printed as a block, with a size on every line INCLUDING the
      file types outside the `.md` universe entirely.

  G5  THE CONTROLS.  The gate is run against constructed trees where it MUST fail
      and where the actionable set MUST grow.  A gate that has never been seen to
      fail has not been seen to pass.

EXIT 1 if any unbounded site of the full population falls in no declared class.
PREDICTED 0.
"""

import os
import re
import shutil
import sys
import tempfile

import lib1d6c as U

OUT = sys.stdout

LIVING = "docs/OneThird-Branching-Graphs-Where-This-Lives.md"
DATED = ("audit", "repair", "independentaudit", "landing", "-audit")


def classify(path):
    """Exactly one class, by a rule on the path.  None means UNCLASSIFIED."""
    base = os.path.basename(path)
    if base == "PREDICTIONS.md":
        return "PRE-REGISTRATION"
    if path == LIVING:
        return "LIVING DOCUMENT"
    if path.startswith("docs/"):
        low = base.lower()
        if any(t in low for t in DATED):
            return "DATED RECORD"
        return None
    if path.startswith("code/") and base == "README.md":
        return "INSTRUMENT README"
    return None


CLASSES = ["PRE-REGISTRATION", "DATED RECORD", "LIVING DOCUMENT",
           "INSTRUMENT README"]
ACTIONABLE = {"LIVING DOCUMENT", "INSTRUMENT README"}
REASON = {
    "PRE-REGISTRATION": "never reworded -- a pre-registration is a dated promise",
    "DATED RECORD": "never edited -- editing destroys the evidence trail",
    "LIVING DOCUMENT": "REPAIRABLE -- this file is reworded freely",
    "INSTRUMENT README": "REPAIRABLE -- ordinary prose about an instrument",
}


def gate(root, paths):
    sites = U.sites_of(root, paths)
    unb = [t for t in sites if not t[4]]
    buckets = {c: [] for c in CLASSES}
    unclassified = []
    for t in unb:
        c = classify(t[0])
        (buckets[c] if c else unclassified).append(t)
    return sites, unb, buckets, unclassified


def main():
    U.rule(OUT, "P5  THE GATE THAT DECLARES WHAT IT CANNOT REPAIR.\n"
                "    Population first, exclusions by name, sizes on every line.")
    print(file=OUT)

    paths = U.u_m_track()
    sites, unb, buckets, unclassified = gate(U.ROOT, paths)
    n, nb, nu = U.totals(sites)

    U.rule(OUT, "  G1  THE POPULATION.  git ls-files '*.md', never os.listdir.")
    print("    tracked .md                 : %d files" % len(paths), file=OUT)
    print("    files stating the figure    : %d" % len({t[0] for t in sites}),
          file=OUT)
    print("    sites            GRAIN S    : %d" % n, file=OUT)
    print("    bounded                     : %d" % nb, file=OUT)
    print("    UNBOUNDED                   : %d" % nu, file=OUT)
    print(file=OUT)
    glob_sites = U.sites_of(U.ROOT, U.u_g_impl())
    _, _, gnu = U.totals(glob_sites)
    print("    THE SAME COUNT THROUGH THE GLOB docs/*.md : %d" % gnu, file=OUT)
    print("    the difference is the universe and nothing else: same predicate,",
          file=OUT)
    print("    same parser, same grain, %d sites the pattern cannot reach."
          % (nu - gnu), file=OUT)
    print(file=OUT)

    U.rule(OUT, "  G2  THE PARTITION.  One class per site, by a rule on the path.")
    print("    %-20s %6s   %s" % ("class", "sites", "what the gate does with it"),
          file=OUT)
    for c in CLASSES:
        print("    %-20s %6d   %s" % (c, len(buckets[c]), REASON[c]), file=OUT)
    print("    %-20s %6d   %s" % ("UNCLASSIFIED", len(unclassified),
                                  "*** the gate FAILS on any of these ***"),
          file=OUT)
    print("    %-20s %6d" % ("TOTAL", sum(len(v) for v in buckets.values())
                             + len(unclassified)), file=OUT)
    total_ok = (sum(len(v) for v in buckets.values()) + len(unclassified)) == nu
    print(file=OUT)
    print("    partition is total : %s   (%d classified + %d unclassified = %d)"
          % ("YES" if total_ok else "NO", sum(len(v) for v in buckets.values()),
             len(unclassified), nu), file=OUT)
    print(file=OUT)
    for c in CLASSES:
        if not buckets[c]:
            continue
        print("    %s -- every site:" % c, file=OUT)
        for p, l, k, s, b in buckets[c]:
            print("      %-58s :%d" % (p[-58:], l), file=OUT)
        print(file=OUT)
    if unclassified:
        print("    UNCLASSIFIED -- every site:", file=OUT)
        U.show_sites(unclassified, OUT)

    U.rule(OUT, "  G3  THE ACTIONABLE SET.  What a reader is being asked to do.")
    act = [t for c in ACTIONABLE for t in buckets[c]]
    print("    unbounded sites in the whole population : %d" % nu, file=OUT)
    print("    of them ACTIONABLE                      : %d" % len(act), file=OUT)
    print(file=OUT)
    for p, l, k, s, b in act:
        print("      %s:%d" % (p, l), file=OUT)
        print("        %s" % re.sub(r"\s+", " ", s)[:94], file=OUT)
    print(file=OUT)
    print("    THESE %d ARE NOT REPAIRED HERE.  They belong to other tickets'"
          % len(act), file=OUT)
    print("    instruments, and this ticket repairs a UNIVERSE, not a sentence.",
          file=OUT)
    print("    They are named so that the backlog is a list and not a number.",
          file=OUT)
    print(file=OUT)

    U.rule(OUT, "  G4  THE DECLARATION.  This block is the deliverable: what a\n"
                "      reader sees instead of a clean sweep.")
    wide = U.u_wide()
    wsites = U.sites_of(U.ROOT, wide)
    wn, wnb, wnu = U.totals(wsites)
    print(file=OUT)
    print("    +---------------------------------------------------------------+",
          file=OUT)
    print("    | DECLARED SCOPE OF THIS GATE                                   |",
          file=OUT)
    print("    |                                                               |",
          file=OUT)
    print("    | POPULATION   every .md tracked by git      %4d files          |"
          % len(paths), file=OUT)
    print("    | GRAIN        one live sentence                                |",
          file=OUT)
    print("    | SITES        %3d, of which %3d are unbounded                   |"
          % (n, nu), file=OUT)
    print("    |                                                               |",
          file=OUT)
    print("    | ENFORCED ON                                                   |",
          file=OUT)
    for c in sorted(ACTIONABLE):
        print("    |   %-24s %3d unbounded site(s)              |"
              % (c, len(buckets[c])), file=OUT)
    print("    |                                                               |",
          file=OUT)
    print("    | DECLARED EXCLUSIONS -- counted, named, and NOT enforced        |",
          file=OUT)
    for c in CLASSES:
        if c in ACTIONABLE:
            continue
        print("    |   %-24s %3d unbounded site(s)              |"
              % (c, len(buckets[c])), file=OUT)
    print("    |   %-24s %3d unbounded site(s) in %3d files    |"
          % ("tracked .txt and .py", wnu, len({t[0] for t in wsites})), file=OUT)
    print("    |                                                               |",
          file=OUT)
    print("    | NOT A CLEAN SWEEP.  %3d of %3d unbounded sites are excluded    |"
          % (nu - len(act), nu), file=OUT)
    print("    | by a stated invariant, not by the shape of a pattern.         |",
          file=OUT)
    print("    +---------------------------------------------------------------+",
          file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------------ G5
    U.rule(OUT, "  G5  THE CONTROLS.  A gate nobody has seen fail has not been\n"
                "      seen to pass.  Three constructed trees.")
    tmp = tempfile.mkdtemp(prefix="p5_1d6c_")
    ctl = []
    try:
        # C1: a site in a path no rule covers -> UNCLASSIFIED -> the gate fails.
        os.makedirs(os.path.join(tmp, "notes"))
        body = ("The Young-Fibonacci intervals number 33 and this sentence "
                "carries no scope at all.\n")
        with open(os.path.join(tmp, "notes", "stray.md"), "w",
                  encoding="utf-8") as f:
            f.write(body)
        _, u1, b1, un1 = gate(tmp, ["notes/stray.md"])
        ctl.append(("a site in an unruled path is UNCLASSIFIED",
                    len(u1) == 1 and len(un1) == 1))

        # C2: the same sentence in an instrument README -> ACTIONABLE.
        os.makedirs(os.path.join(tmp, "code", "x"))
        with open(os.path.join(tmp, "code", "x", "README.md"), "w",
                  encoding="utf-8") as f:
            f.write(body)
        _, u2, b2, un2 = gate(tmp, ["code/x/README.md"])
        ctl.append(("the same sentence in a README is ACTIONABLE",
                    len(b2["INSTRUMENT README"]) == 1 and not un2))

        # C3: the same sentence in a PREDICTIONS.md -> DECLARED EXCLUSION.
        with open(os.path.join(tmp, "code", "x", "PREDICTIONS.md"), "w",
                  encoding="utf-8") as f:
            f.write(body)
        _, u3, b3, un3 = gate(tmp, ["code/x/PREDICTIONS.md"])
        ctl.append(("the same sentence in a PREDICTIONS.md is EXCLUDED",
                    len(b3["PRE-REGISTRATION"]) == 1 and not un3))

        # C4: a BOUNDED sentence is not a site of any class.
        with open(os.path.join(tmp, "code", "x", "bounded.md"), "w",
                  encoding="utf-8") as f:
            f.write("The Young-Fibonacci intervals number 33 to rank 6.\n")
        s4, u4, b4, un4 = gate(tmp, ["code/x/bounded.md"])
        ctl.append(("a BOUNDED sentence produces 0 unbounded sites",
                    len(s4) == 1 and len(u4) == 0))

        # C5: the exclusion cannot be gamed by moving a file into docs/.
        os.makedirs(os.path.join(tmp, "docs"))
        with open(os.path.join(tmp, "docs", "note.md"), "w",
                  encoding="utf-8") as f:
            f.write(body)
        _, u5, b5, un5 = gate(tmp, ["docs/note.md"])
        ctl.append(("a docs/ file that is NOT an audit record is UNCLASSIFIED",
                    len(un5) == 1))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    for name, ok in ctl:
        print("    %-56s %s" % (name, "FIRES" if ok else "*** FAILED ***"),
              file=OUT)
    controls_ok = all(ok for _, ok in ctl)
    print(file=OUT)
    print("    %d of %d controls fire." % (sum(1 for _, o in ctl if o), len(ctl)),
          file=OUT)
    print("    C5 IS THE ONE THAT MATTERS: a file cannot buy an exemption by", file=OUT)
    print("    living in docs/.  The exemption is for AUDIT RECORDS, and a", file=OUT)
    print("    docs/ file that is not one falls through to UNCLASSIFIED and", file=OUT)
    print("    fails this gate.", file=OUT)
    print(file=OUT)

    U.rule(OUT, "  VERDICT")
    print("    population %d unbounded; %d enforced; %d declared and excluded;"
          % (nu, len(act), nu - len(act) - len(unclassified)), file=OUT)
    print("    %d unclassified." % len(unclassified), file=OUT)
    print(file=OUT)

    U.rule(OUT)
    print("SUMMARY p5_declaration: G1 population %d tracked .md, %d sites, %d "
          "unbounded" % (len(paths), n, nu), file=OUT)
    print("SUMMARY p5_declaration: G1 the glob would report %d of the same %d"
          % (gnu, nu), file=OUT)
    for c in CLASSES:
        print("SUMMARY p5_declaration: G2 %-18s %d site(s)" % (c, len(buckets[c])),
              file=OUT)
    print("SUMMARY p5_declaration: G2 UNCLASSIFIED %d; partition total %s"
          % (len(unclassified), "YES" if total_ok else "NO"), file=OUT)
    print("SUMMARY p5_declaration: G3 actionable %d of %d" % (len(act), nu),
          file=OUT)
    print("SUMMARY p5_declaration: G4 declared exclusions %d .md site(s) plus %d "
          "site(s) in tracked .txt/.py" % (nu - len(act), wnu), file=OUT)
    print("SUMMARY p5_declaration: G5 controls %d of %d fire"
          % (sum(1 for _, o in ctl if o), len(ctl)), file=OUT)
    U.rule(OUT)
    return 1 if unclassified or not controls_ok or not total_ok else 0


if __name__ == "__main__":
    sys.exit(main())
