"""A4 -- string-checkers do not check claims.  A mutation battery against the
repair's two doc-checkers.

    code/counterexample_repair_dea5/check_doc_repair.py   (new)
    code/counterexample_probe_24a3/check_doc.py           (extended with STRUCK)

mg-a7b4's finding 1 was that check_doc.py verified "rank 1 of 5 tied with 4" --
a TRUE string about a VACUOUS group.  The repair's answer is a STRUCK set with
an inverted assertion.  The question this battery asks is not whether the new
mechanism works on the case it was built for (it does) but what it still misses:
each mutation below changes the MEANING of a certified passage and the battery
records whether the checker exits non-zero.

A mutation that exits 0 is a silent miss.  Every mutation is applied to a
COPY of the repository tree; nothing here writes to the working tree.

The last four mutations are aimed at THIS audit's own checker.  A control
validated by its own author is not a control, so check_doc_audit.py is shown
failing on four different kinds of damage to this audit's own document.

NOTE on ordering: this script's own stdout is out_locator.txt, which
check_doc_audit.py reads.  run_all.sh therefore writes it via a temporary file
and moves it into place, so the tree copies made here always contain a COMPLETE
out_locator.txt.  Redirecting straight onto out_locator.txt truncates it and the
CHK_AUDIT baseline will report a spurious failure.
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
CHK_REPAIR = "code/counterexample_repair_dea5/check_doc_repair.py"
CHK_TARGET = "code/counterexample_probe_24a3/check_doc.py"
CHK_AUDIT = "code/counterexample_audit_0a11/check_doc_audit.py"
AUDIT_MD = "docs/OneThird-Counterexample-Under-The-Action-IndependentAudit-mg0a11.md"
OUT_S4 = "code/counterexample_repair_dea5/out_section4.txt"


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


def delete_between(tree, rel, start, end):
    p = os.path.join(tree, rel)
    body = open(p).read()
    i = body.find(start)
    j = body.find(end, i + 1)
    if i < 0 or j < 0:
        return False
    open(p, "w").write(body[:i] + body[j:])
    return True


MUTATIONS = []


def mutation(name, checker, expect, note=""):
    def deco(fn):
        MUTATIONS.append((name, checker, expect, note, fn))
        return fn
    return deco


# ---------------------------------------------------------------- must fail

@mutation("M1a the headline p-value is wrong THROUGHOUT the repair doc",
          CHK_REPAIR, "?",
          "the target document carries its own copy of the same string, and the\n"
          "                two documents are concatenated before matching")
def m1a(t):
    return edit(t, REPAIR_MD, "1/38760", "1/38761", 99)


@mutation("M1b the headline p-value is wrong in BOTH documents", CHK_REPAIR,
          "FAIL", "the mechanism the checker exists for")
def m1b(t):
    a = edit(t, REPAIR_MD, "1/38760", "1/38761", 99)
    b = edit(t, TARGET_MD, "1/38760", "1/38761", 99)
    return a and b


@mutation("M2  a struck sentence is put back into live prose", CHK_REPAIR, "FAIL",
          "the inverted STRUCK assertion")
def m2(t):
    return edit(t, TARGET_MD,
                "> **STRUCK (mg-dea5, landing mg-a7b4 finding 1).** This paragraph previously continued:",
                "Note that:")


@mutation("M3  the instrument's own output is altered", CHK_REPAIR, "FAIL",
          "prose is checked against the printed quantity")
def m3(t):
    return edit(t, OUT_S4, "1/38760", "1/38761", 99)


@mutation("M4  a replacement sentence is removed", CHK_REPAIR, "FAIL",
          "the LIVE set")
def m4(t):
    return edit(t, TARGET_MD,
                "The smallest `n` carrying a majority cycle is exactly 9.",
                "A majority cycle exists somewhere above n = 8.")


# ------------------------------------------------- meaning-changing probes

@mutation("M5  the n=8 and n=6 rho|e figures are SWAPPED", CHK_REPAIR, "?",
          "same strings, different rows -- is the ASSOCIATION checked?")
def m5(t):
    p = os.path.join(t, REPAIR_MD)
    b = open(p).read()
    b = b.replace("| 6 | 88 | 27 | **−0.287**", "| 6 | 88 | 27 | **@@A@@**")
    b = b.replace("| 8 | 6420 | 670 | **−0.273**", "| 8 | 6420 | 670 | **−0.287**")
    b = b.replace("**@@A@@**", "**−0.273**")
    open(p, "w").write(b)
    return "−0.273" in b


@mutation("M6  a NON-VACUOUS group is relabelled VACUOUS", CHK_REPAIR, "?",
          "the exact defect being repaired, in the repair's own table")
def m6(t):
    return edit(t, REPAIR_MD,
                "| 8 | **9** | 20 | 6 | 6 | 2 | **non-vacuous** |",
                "| 8 | **9** | 20 | 6 | 6 | 2 | *VACUOUS* |")


@mutation("M7a the whole multiple-comparison section is DELETED", CHK_REPAIR, "?",
          "'is the post-hoc position stated?' -- the brief's second target")
def m7a(t):
    return delete_between(t, REPAIR_MD,
                          "### 3.3 What is a hypothesis and what is a test of it",
                          "## 4. THE POWERED TEST")


@mutation("M7b the post-hoc FRAMING is deleted, the numbers left in place",
          CHK_REPAIR, "?",
          "the same section with only its prose removed: does the checker\n"
          "                protect the FRAMING, or only the figures inside it?")
def m7b(t):
    return edit(t, REPAIR_MD,
                "**The `n = 7` group is where mg-a7b4 found this, and the `n = 6` group was in the same table. Those two are\nthe generating observations, and their `p`-values are not evidence** \u2014 they are the reason the hypothesis\nexists. `1/286` found after the fact among the groups that happened to be non-vacuous is a hypothesis.",
                "The `n = 6` and `n = 7` groups separate perfectly, with exact `p`-values `1/7` and `1/286`.")


@mutation("M8  'pre-specified' is upgraded to a confirmed discovery", CHK_REPAIR, "?",
          "status language, checked in the overclaiming direction")
def m8(t):
    return edit(t, REPAIR_MD,
                "**The `n = 8` group is a pre-specified test in a new population.**",
                "**The `n = 8` group CONFIRMS the separation as an established fact.**")


@mutation("M9  'n = 8 is now settled' is restated as 'no cycle exists at any n'",
          CHK_REPAIR, "?", "the open -> absent drift the brief asks to flag")
def m9(t):
    return edit(t, REPAIR_MD,
                "> **So the smallest `n` carrying a majority cycle is exactly 9.**",
                "> **So no majority cycle exists, at any `n`.**")


@mutation("M10 the 'not a filter' caveat is deleted", CHK_REPAIR, "?",
          "a caveat removed while the claim it qualifies stays")
def m10(t):
    return delete_between(t, REPAIR_MD,
                          "* **Not a filter.**", "* **Not explained.**")


@mutation("M11 a figure is deleted from the repair but survives in the target",
          CHK_REPAIR, "?", "the two documents are concatenated before matching")
def m11(t):
    return edit(t, REPAIR_MD, "`1/38760 = 2.6 × 10⁻⁵`", "an exact p-value")


@mutation("M12 the repair's own text asserts a struck claim", CHK_REPAIR, "?",
          "STRUCK regions are located in the TARGET only")
def m12(t):
    p = os.path.join(t, REPAIR_MD)
    b = open(p).read()
    b = b.replace("## 9. What this does NOT show",
                  "## 8.9 Addendum\n\nWithin a fixed `e(P)` the statistic does not "
                  "distinguish the extremal posets from anything at all -- not weakly, "
                  "but by an exact tie.\n\n## 9. What this does NOT show")
    open(p, "w").write(b)
    return True


@mutation("M13 the target's headline is silently un-repaired", CHK_TARGET, "?",
          "does the EXTENDED check_doc.py notice its own subject changing?")
def m13(t):
    return edit(t, TARGET_MD,
                "`qmass = 1` picks out **exactly** the `δ`-extremal\n   posets",
                "`qmass = 1` picks out **some of** the `δ`-extremal\n   posets")


# ---------------------------------------- this audit's own checker must fire

@mutation("S1  MY OWN figure is wrong in MY OWN document", CHK_AUDIT, "FAIL",
          "a control validated by its own author is not a control")
def s1(t):
    return edit(t, AUDIT_MD, "1/C(6,1) = 1/6", "1/C(6,1) = 1/9", 99)


@mutation("S2  MY OWN figure is moved OUT of its declared section", CHK_AUDIT,
          "FAIL", "the property M1a showed the subject's checker lacks")
def s2(t):
    return edit(t, AUDIT_MD,
                "The whole `e = 9` family from `n = 5` to `n = 11` \u2014 160 group memberships \u2014 has **six** distinct cores:",
                "The whole `e = 9` family has this shape:")


@mutation("S3  MY OWN 'could not establish' section is emptied", CHK_AUDIT,
          "FAIL", "the guard on this audit's own limits")
def s3(t):
    return delete_between(t, AUDIT_MD, "* **Theorem 4's generalisation",
                          "## 8. Files")


@mutation("S4  a silent miss I found is dropped from my write-up", CHK_AUDIT,
          "FAIL", "the guard tying the battery's output to the prose")
def s4(t):
    return edit(t, AUDIT_MD, "| **M9** |", "| M9-removed |")


def main():
    print("=" * 78)
    print("A4  mutation battery against the repair's doc-checkers,")
    print("    and four self-mutations against this audit's own")
    print("=" * 78)
    print()
    # baseline
    base = tempfile.mkdtemp(prefix="audit0a11-base-")
    tree = os.path.join(base, "repo")
    shutil.copytree(ROOT, tree, ignore=shutil.ignore_patterns(".git"))
    for chk in (CHK_REPAIR, CHK_TARGET, CHK_AUDIT):
        rc = run_checker(tree, chk)
        print("  baseline %-52s exit %d %s"
              % (chk, rc, "(clean)" if rc == 0 else "(ALREADY FAILING)"))
    shutil.rmtree(base)
    print()

    misses = []
    for name, checker, expect, note, fn in MUTATIONS:
        d = tempfile.mkdtemp(prefix="audit0a11-")
        tree = os.path.join(d, "repo")
        shutil.copytree(ROOT, tree, ignore=shutil.ignore_patterns(".git"))
        applied = fn(tree)
        if not applied:
            print("  [SKIP] %-58s mutation did not apply" % name)
            shutil.rmtree(d)
            continue
        rc = run_checker(tree, checker)
        caught = rc != 0
        if expect == "FAIL":
            verdict = "ok  " if caught else "BROKEN"
        else:
            verdict = "caught" if caught else "SILENT MISS"
            if not caught:
                misses.append((name, note))
        print("  [%-11s] %-58s exit %d" % (verdict, name, rc))
        if note:
            print("                %s" % note)
        shutil.rmtree(d)

    print()
    print("=" * 78)
    print("SILENT MISSES: %d" % len(misses))
    print("=" * 78)
    for name, note in misses:
        print("  %s" % name)
        print("      %s" % note)


if __name__ == "__main__":
    main()
