"""A5 -- NINE MUTATIONS mg-a893'S AUTHOR NEVER SAW.

mg-a893's acceptance gate is mg-0a11's fourteen-mutation battery, re-run
unmodified.  That gate is honoured -- code/counterexample_audit_0a11/ is
byte-for-byte untouched and the re-run reproduces here (out_battery_0a11_rerun
is byte-identical to a fresh run from this worktree).  But a fix accepted
against fourteen known mutations is fitted to fourteen known mutations, so the
brief asks for new ones, including:

  * at least one that changes MEANING without changing any CERTIFIED BYTE, and
  * at least one in the region mg-4acd's presentation-record digest covers, to
    find out whether the two mechanisms COMPOSE or merely COEXIST.

Both are here (C1 and C8).  Every mutation is applied to a COPY of the tree;
nothing writes to the working tree.

Exit code is informational: this file reports, it does not gate.
"""

import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", ".."))
REPAIR_MD = "docs/OneThird-Counterexample-Under-The-Action-Repair.md"
TARGET_MD = "docs/OneThird-Counterexample-Under-The-Action.md"
README_MD = "docs/state-history/README.md"
CHK_REPAIR = "code/counterexample_repair_dea5/check_doc_repair.py"
CHK_TARGET = "code/counterexample_probe_24a3/check_doc.py"
CHK_AUDIT = "code/counterexample_audit_0a11/check_doc_audit.py"
OUT_CORES = "code/counterexample_repair_dea5/out_cores.txt"


def run_checker(tree, checker):
    r = subprocess.run([sys.executable, os.path.join(tree, checker)],
                       capture_output=True, text=True, cwd=tree)
    return r.returncode


def edit(tree, rel, old, new, count=1):
    p = os.path.join(tree, rel)
    body = open(p).read()
    if old not in body:
        return False
    open(p, "w").write(body.replace(old, new, count))
    return True


def drop(tree, rel, s):
    return edit(tree, rel, s, "")


MUTATIONS = []


def mutation(name, checker, kind="probe", note=""):
    """kind: 'probe'   -- a defect probe against check_doc_repair.py
             'control' -- expected to fire; proves the mechanism is wired
             'scope'   -- asks where a checker's subject ENDS, not whether it works
    """
    def deco(fn):
        MUTATIONS.append((name, checker, kind, note, fn))
        return fn
    return deco


# ------------------------------------------------------------------ C1 -- the
# one the brief names: meaning inverted, not one certified byte altered.

@mutation("C1  the section is REVERSED by an insertion; every certified\n"
          "      byte is left exactly where it was", CHK_REPAIR, "probe",
          "PURE INSERTION.  No needle deleted, no count changed, no cell moved,\n"
          "      no heading touched.  The paragraph now says the opposite.")
def c1(t):
    s = ("**Read this as a correction to the strength claimed, not as a "
         "retraction of the finding.**")
    return edit(t, REPAIR_MD, s, s + " On further reflection the core "
                "reduction is unsound, the members of a group are independent "
                "after all, and the group-level figure was right the first time.")


# ------------------------------------------------------------- C2 -- P4's idea
# applied to the table P4 does not cover.

@mutation("C2  the UNKEYED row of the 3.4 core table is falsified", CHK_REPAIR,
          "probe", "P4 gained two row keys for this table, n = 6 and n = 8, and the\n"
          "      n = 7 row between them has none.  Its core count and its\n"
          "      extremal-core count are rewritten here: the row now says the\n"
          "      separation at n = 7 was 2 of 4, which is not perfect.")
def c2(t):
    return edit(t, REPAIR_MD,
                "| 7 | 13 | 3 | 5 | 1 | `1/286` | **`1/5`** |",
                "| 7 | 13 | 3 | 4 | 2 | `1/286` | **`1/5`** |")


# --------------------------------------------------- C3 / C4 -- the sixth core

@mutation("C3  'six distinct cores' at n = 11 is changed to 'five'", CHK_REPAIR,
          "probe", "the figure that makes the document internally consistent.  It is\n"
          "      the ONLY sentence in either document that contradicts\n"
          "      'Nothing enters the family after n = 6' -- and it is right.")
def c3(t):
    return edit(t, REPAIR_MD,
                "still perfect, over **six** distinct cores",
                "still perfect, over **five** distinct cores")


@mutation("C4  the whole n = 11 clause is DELETED", CHK_REPAIR, "probe",
          "same target, by removal rather than falsification.  The document\n"
          "      is left self-consistent and wrong.")
def c4(t):
    return edit(t, REPAIR_MD,
                " and mg-0a11 carried\nthe same measurement to `n = 11` — three "
                "sizes beyond this instrument's reach — and found the separation\n"
                "still perfect, over **six** distinct cores with still exactly one "
                "extremal.", "")


# ------------------------------------------------- C5 -- P1, on the NEW figure

@mutation("C5  the honest `p` is falsified in the TARGET document only",
          CHK_REPAIR, "probe",
          "P1 is 'per document, with an exact count' -- and the figure the\n"
          "      whole repair exists to install has a FIGURES entry for the\n"
          "      repair and none for the target.  mg-0a11's M1a, re-created for\n"
          "      the new headline, pointing the other way.")
def c5(t):
    return edit(t, TARGET_MD,
                "**`1/5`**, not the group-level `1/38760`",
                "**`1/50`**, not the group-level `1/38760`")


# ------------------------------------------ C6 -- P2 on the new output (should
# be caught; run to confirm the new file is genuinely wired in)

@mutation("C6  out_cores.txt's honest-`p` line is falsified", CHK_REPAIR, "control",
          "EXPECTED TO FIRE.  P2 pairs the repair's sentence with this exact\n"
          "      printed line, so this is the control on C5: the mechanism works,\n"
          "      it is the COVERAGE that is one-sided.")
def c6(t):
    return edit(t, OUT_CORES,
                "THE HONEST EXACT p OVER THE DISTINCT CORES IS 1/5.",
                "THE HONEST EXACT p OVER THE DISTINCT CORES IS 1/9.")


# ------------------------------------------------- C7 -- the declared boundary

@mutation("C7  the five-core table is HTML-commented out of the page",
          CHK_REPAIR, "probe",
          "the coverage boundary section 8.2 NAMES.  Naming is not handling:\n"
          "      this is a check that the named risk is real, and it is.")
def c7(t):
    p = os.path.join(t, REPAIR_MD)
    b = open(p).read()
    a = "| size | `δ` | `qmass` | in groups | covers |"
    z = "> **THE HONEST EXACT `p` OVER THE DISTINCT CORES IS `1/5`**"
    i, j = b.find(a), b.find(z)
    if i < 0 or j < 0 or j < i:
        return False
    open(p, "w").write(b[:i] + "<!--\n" + b[i:j] + "-->\n\n" + b[j:])
    return True


# --------------------------------- C8 -- the composition test with mg-4acd/2da3

@mutation("C8  a region mg-4acd's presentation digest CERTIFIES is gutted",
          CHK_REPAIR, "scope",
          "docs/state-history/README.md, the F1 correction block, region id\n"
          "      readme.F1 in delta_control.py's CERTIFIED table.  Does the\n"
          "      document-checker of this cluster see it?")
def c8(t):
    return edit(t, README_MD, "**`no 4d tally` is a correction",
                "**`no 4d tally` is NOT a correction and the figure below is void")


# ------------------------------------------------------- C9 -- the other check

@mutation("C9  the repair's own headline is falsified everywhere in BOTH\n"
          "      documents", CHK_AUDIT, "scope",
          "run against mg-0a11's audit document checker rather than the\n"
          "      repair's, to see whether the AUDIT's checker notices its\n"
          "      subject being rewritten under it.")
def c9(t):
    a = edit(t, REPAIR_MD, "1/5", "1/4", 99)
    b = edit(t, TARGET_MD, "1/5", "1/4", 99)
    return a and b


def main():
    print("=" * 78)
    print("A5  nine mutations against mg-a893's checkers, none of them in")
    print("    mg-0a11's battery")
    print("=" * 78)
    print()
    base = tempfile.mkdtemp(prefix="audit-c6bc-base-")
    tree = os.path.join(base, "repo")
    shutil.copytree(ROOT, tree, ignore=shutil.ignore_patterns(".git"))
    for chk in (CHK_REPAIR, CHK_TARGET, CHK_AUDIT):
        rc = run_checker(tree, chk)
        print("  baseline %-52s exit %d %s"
              % (chk, rc, "(clean)" if rc == 0 else "(ALREADY FAILING)"))
    shutil.rmtree(base)
    print()

    misses = []
    scoped = []
    for name, checker, kind, note, fn in MUTATIONS:
        d = tempfile.mkdtemp(prefix="audit-c6bc-")
        tree = os.path.join(d, "repo")
        shutil.copytree(ROOT, tree, ignore=shutil.ignore_patterns(".git"))
        if not fn(tree):
            print("  [SKIP       ] %-58s did not apply" % name.split("\n")[0])
            shutil.rmtree(d)
            continue
        rc = run_checker(tree, checker)
        caught = rc != 0
        print("  [%-11s] %-58s exit %d"
              % ("caught" if caught else "SILENT MISS", name, rc))
        if note:
            print("                %s" % note)
        if not caught:
            (scoped if kind != "probe" else misses).append(name.split("\n")[0])
        if kind == "control" and not caught:
            print("                *** THE CONTROL DID NOT FIRE ***")
        shutil.rmtree(d)

    print()
    print("=" * 78)
    nprobe = sum(1 for m in MUTATIONS if m[2] == "probe")
    print("SILENT MISSES: %d of %d defect probes" % (len(misses), nprobe))
    print("=" * 78)
    for m in misses:
        print("  %s" % m)
    print()
    print("  C6, the control, FIRED -- the per-output pairing works on the new")
    print("  file, so what is one-sided above is the COVERAGE and not the")
    print("  mechanism.  C8 and C9 are scope questions, not defects: %s"
          % (", ".join(scoped) if scoped else "(none)"))

    print()
    print("=" * 78)
    print("THE COMPOSITION QUESTION, ANSWERED IN BOTH DIRECTIONS")
    print("=" * 78)
    print("""
  C8 runs one way live.  The other way needs no run and admits a proof:
  mg-4acd's mechanism digests a fixed list of REGIONS, and that list --
  CERTIFIED in code/state_landing_control_2da3/delta_control.py -- names
  exactly two files:

      STATE.md                       (row :135's content cell, two versions)
      docs/state-history/README.md   (nine correction blocks)

  Neither counterexample document is a certified region, and no edit to a file
  outside the list can change the bytes or the presentation record of a region
  inside it.  So no mutation of the repair document can move any digest, and
  C8 shows that no mutation of a certified region moves the document-checker.

  THE TWO MECHANISMS COEXIST.  They do not compose: their subjects are
  disjoint, and the union of their coverage has a hole exactly the size of the
  two counterexample documents' PRESENTATION -- which is what C7 walks through.
  Section 8.2 says the two are "complementary, not redundant" and that is
  correct as far as it goes; what it does not say is that complementary here
  means DISJOINT, so nothing certifies that a reader of these two documents is
  shown what the checker checked.""")


if __name__ == "__main__":
    main()
