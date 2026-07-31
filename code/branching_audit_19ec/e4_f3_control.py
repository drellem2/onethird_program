"""E4 -- F3's replacement: the control that was closed, fired in
configurations mg-dffa did not run.

mg-dffa closed the one open link in the n = 8 provenance chain by making
`check_doc.py` read the machine-readable `SKEW8` line out of
`out_r1b_skew8.txt` and compare it with the row of `out_young.txt` it
certifies, and it exercised the new check in four configurations (W4a-W4d).

The question mg-19ec asks is different: F3's own defect was A CONTROL THAT
COULD NOT FIRE.  A repair for that defect is worth exactly as much as the
number of ways it CAN fire.  So the new check is put in seven configurations
here, four of which mg-dffa did not build, and the two ends of the chain are
mutated INDEPENDENTLY and TOGETHER:

  C1  faithful copy                                       expect exit 0
  C2  computed 360 -> 361 (mg-dffa's W4b)                 expect exit 1, new check alone
  C3  out_r1b_skew8.txt deleted (mg-dffa's W4c)           expect exit 1
  C4  out_r1b_skew8.txt present but EMPTY                 expect exit 1  [new]
  C5  TWO SKEW8 lines, both 360                           expect exit 1  [new]
  C6  SKEW8 line non-numeric                              expect exit 1  [new]
  C7  BOTH ends moved to 361 together                     expect exit 1  [new]

C7 is the one that decides how much the repair bought.  If a reader moves the
computed count and the published row together, the new check AGREES -- it
compares the two ends with each other and not with anything outside.  What
catches C7 is the OLDER typed constant in check_doc.py, which F3 correctly
identified as not a control on provenance.  So the two checks are complements,
and neither alone closes the chain.  Reported, because "the control is closed"
is the sentence under audit.

EXIT 1 if any configuration does not behave as stated above.  PREDICTED 0.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

OUT = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.join(HERE, "..")
ROOT = os.path.join(CODE, "..")
DOCNAME = "OneThird-Branching-Graphs-Where-This-Lives.md"
BAD = [0]


def ck(label, ok, detail=""):
    if not ok:
        BAD[0] += 1
    print("  %-58s %s%s" % (label, "ok" if ok else "BAD", detail), file=OUT)
    return ok


def build_tree(tmp):
    """A faithful copy of exactly the three inputs check_doc.py reads, plus
    check_doc.py itself."""
    for d in ("code/branching_repair_41aa", "code/branching_af28", "docs"):
        os.makedirs(os.path.join(tmp, d), exist_ok=True)
    shutil.copy(os.path.join(CODE, "branching_repair_41aa", "check_doc.py"),
                os.path.join(tmp, "code/branching_repair_41aa/check_doc.py"))
    shutil.copy(os.path.join(CODE, "branching_repair_41aa", "out_r1b_skew8.txt"),
                os.path.join(tmp, "code/branching_repair_41aa/out_r1b_skew8.txt"))
    shutil.copy(os.path.join(CODE, "branching_af28", "out_young.txt"),
                os.path.join(tmp, "code/branching_af28/out_young.txt"))
    shutil.copy(os.path.join(ROOT, "docs", DOCNAME),
                os.path.join(tmp, "docs", DOCNAME))
    return tmp


def run(tmp):
    p = subprocess.run([sys.executable, "check_doc.py"],
                       cwd=os.path.join(tmp, "code/branching_repair_41aa"),
                       capture_output=True, text=True)
    fails = re.findall(r"^\s*BAD\s+(.*?)\s*$", p.stdout, re.M)
    if not fails:
        fails = [l.strip() for l in p.stdout.split("\n")
                 if l.strip().startswith("BAD")]
    named = re.findall(r"FAILED:\s*(.*)", p.stdout)
    return p.returncode, p.stdout, fails, named


def failed_labels(stdout):
    """check_doc.py prints `  NN  <label>  PASS|FAIL <detail>`.  Collect the
    labels of the checks it marked FAIL."""
    out = []
    for line in stdout.split("\n"):
        m = re.match(r"\s*\d+\s+(.*?)\s+FAIL(\s|$)", line)
        if m:
            out.append(m.group(1).strip())
    return out


def config(name, mutate, expect_exit, expect_labels=None):
    tmp = tempfile.mkdtemp(prefix="e4_19ec_")
    try:
        build_tree(tmp)
        note = mutate(tmp) if mutate else "unmutated"
        rc, stdout, _, _ = run(tmp)
        labels = failed_labels(stdout)
        ok = rc == expect_exit
        ck("%s: exit %d" % (name, expect_exit), ok, " (got %d; %s)" % (rc, note))
        if expect_labels is not None:
            ck("  %s: the failures named are exactly what is expected" % name,
               labels == expect_labels, " (%r)" % (labels,))
        else:
            print("      failures named: %r" % (labels,), file=OUT)
        return rc, labels
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def edit(path, old, new):
    with open(path, encoding="utf-8") as f:
        s = f.read()
    assert old in s, (path, old)
    with open(path, "w", encoding="utf-8") as f:
        f.write(s.replace(old, new))


def main():
    print("=" * 78, file=OUT)
    print("E4  mg-19ec: the F3 control, fired in seven configurations.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    NEW = "the COMPUTED n=8 skew count equals the one out_young.txt PUBLISHES"
    ONE = "out_r1b_skew8.txt carries exactly one SKEW8 line"

    ck("the repaired check_doc.py names the new check",
       NEW in open(os.path.join(CODE, "branching_repair_41aa", "check_doc.py"),
                   encoding="utf-8").read())
    ck("out_r1b_skew8.txt carries its machine-readable line",
       bool(re.search(r"^SKEW8 360\s*$",
                      open(os.path.join(CODE, "branching_repair_41aa",
                                        "out_r1b_skew8.txt"),
                           encoding="utf-8").read(), re.M)))
    print(file=OUT)

    config("C1  faithful copy", None, 0, [])
    config("C2  computed 360 -> 361",
           lambda t: (edit(os.path.join(t, "code/branching_repair_41aa",
                                        "out_r1b_skew8.txt"),
                           "SKEW8 360", "SKEW8 361"), "SKEW8 361")[1],
           1, [NEW])
    config("C3  out_r1b_skew8.txt deleted",
           lambda t: (os.remove(os.path.join(t, "code/branching_repair_41aa",
                                             "out_r1b_skew8.txt")),
                      "deleted")[1],
           1, [ONE, NEW])
    config("C4  out_r1b_skew8.txt present but EMPTY",
           lambda t: (open(os.path.join(t, "code/branching_repair_41aa",
                                        "out_r1b_skew8.txt"), "w").close(),
                      "emptied")[1],
           1, [ONE, NEW])
    config("C5  TWO SKEW8 lines, both 360",
           lambda t: (edit(os.path.join(t, "code/branching_repair_41aa",
                                        "out_r1b_skew8.txt"),
                           "SKEW8 360", "SKEW8 360\nSKEW8 360"),
                      "duplicated")[1],
           1, [ONE, NEW])
    config("C6  SKEW8 line non-numeric",
           lambda t: (edit(os.path.join(t, "code/branching_repair_41aa",
                                        "out_r1b_skew8.txt"),
                           "SKEW8 360", "SKEW8 threehundredandsixty"),
                      "SKEW8 <word>")[1],
           1, [ONE, NEW])
    rc7, lab7 = config("C7  BOTH ends moved to 361 together",
                       lambda t: (edit(os.path.join(t, "code/branching_repair_41aa",
                                                    "out_r1b_skew8.txt"),
                                       "SKEW8 360", "SKEW8 361"),
                                  edit(os.path.join(t, "code/branching_af28",
                                                    "out_young.txt"),
                                       "360*", "361*"),
                                  "computed AND published both 361")[2],
                       1)
    print(file=OUT)
    ck("C7: the NEW check does NOT fire when both ends move together",
       NEW not in lab7)
    ck("C7: something else does, so the tree is still caught",
       len(lab7) > 0, " (%r)" % (lab7,))
    print(file=OUT)
    print("  READING E4.  The added check fires in six of the seven", file=OUT)
    print("  configurations, including four mg-dffa did not build, and a", file=OUT)
    print("  missing, empty, duplicated or unparseable input is a FAILURE in", file=OUT)
    print("  every one of them rather than a skip.  That is what F3 asked", file=OUT)
    print("  for and it is what was delivered.", file=OUT)
    print(file=OUT)
    print("  AND THE ONE IT DOES NOT CATCH, NAMED.  C7 moves BOTH ends of the", file=OUT)
    print("  chain together.  The new check compares the two ends with each", file=OUT)
    print("  OTHER, so it agrees; what catches C7 is check_doc.py's older", file=OUT)
    print("  typed constant, which F3 correctly said was not a provenance", file=OUT)
    print("  control.  The two are complements: neither alone closes the", file=OUT)
    print("  chain, and the account document's sentence -- 'the control was", file=OUT)
    print("  closed instead of the sentence' -- is true of the pair and not", file=OUT)
    print("  of the new line by itself.  No number moves either way.", file=OUT)
    print(file=OUT)
    print("=" * 78, file=OUT)
    print("SUMMARY e4_f3_control: findings %d" % BAD[0], file=OUT)
    print("=" * 78, file=OUT)
    return 1 if BAD[0] else 0


if __name__ == "__main__":
    sys.exit(main())
