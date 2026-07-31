"""W4 -- F3: does the line added to check_doc.py actually fire?

F3 of mg-5800 is not a wrong number.  It is a control that could not fire on
the thing it appeared to certify: `check_doc.py` certified
`code/branching_af28/out_young.txt`'s n = 8 row against a constant typed into
`check_doc.py` itself, while out_young.txt's own 360 came from `cited_skew`
typed into `code/branching_af28/t_young.py`.  Nothing compared the computed 360
with the published 360.

mg-dffa adds the comparison.  ADDING A CONTROL IS WORTHLESS IF THE NEW CONTROL
CANNOT FIRE EITHER, and this repair's whole subject is claims stated with more
warrant than their evidence carries -- so the new line is exercised in BOTH
directions here, on the real `check_doc.py`, run as a subprocess:

  W4a  UNMUTATED.  A faithful copy of the three inputs check_doc.py reads
       (the document, out_young.txt, out_r1b_skew8.txt) in a temporary tree.
       Expect exit 0.

  W4b  MUTATED.  The same tree with `SKEW8 360` rewritten to `SKEW8 361` in
       out_r1b_skew8.txt -- exactly F3's hypothetical, "if r1b_skew8.py
       returned 361 tomorrow".  Expect exit 1, and expect the FAILURE NAMED to
       be the new one and no other: a mutation that trips some unrelated check
       would prove nothing about this line.

  W4c  MISSING INPUT.  out_r1b_skew8.txt deleted.  Expect exit 1.  A control
       that silently skips when its input is absent is the same defect wearing
       a different hat.

  W4d  THE PRE-REPAIR PREDICATE.  The mutation is replayed against the
       PRE-REPAIR check_doc.py, taken from git at the commit that introduced it
       (mg-41aa, 504ab6c).  It MUST pass -- exit 0 on `SKEW8 361` -- because
       that is what F3 asserts.  If the old file also failed, F3 would be
       wrong and this repair would be fixing nothing.

FALSIFIERS.  Exit 0 in W4b or W4c; exit 1 in W4a or W4d; a W4b failure list
that names anything other than the new check.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

OUT = sys.stdout
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
REPAIR = os.path.join(ROOT, "code", "branching_repair_41aa")
DOCNAME = "OneThird-Branching-Graphs-Where-This-Lives.md"
PRE_REPAIR_REV = "504ab6c"
NEW_CHECK = "the COMPUTED n=8 skew count equals the one out_young.txt PUBLISHES"

BAD = [0]


def verdict(label, ok, detail=""):
    if not ok:
        BAD[0] += 1
    print("  %-58s %s%s" % (label, "ok" if ok else "BAD", detail), file=OUT)


def build_tree(tmp, check_doc_source, skew8_text=None):
    """A minimal copy of the three paths check_doc.py reads, at the relative
    positions it reads them from."""
    rep = os.path.join(tmp, "code", "branching_repair_41aa")
    af28 = os.path.join(tmp, "code", "branching_af28")
    docs = os.path.join(tmp, "docs")
    for d in (rep, af28, docs):
        os.makedirs(d, exist_ok=True)
    with open(os.path.join(rep, "check_doc.py"), "w", encoding="utf-8") as fh:
        fh.write(check_doc_source)
    shutil.copy(os.path.join(ROOT, "code", "branching_af28", "out_young.txt"),
                af28)
    shutil.copy(os.path.join(ROOT, "docs", DOCNAME), docs)
    if skew8_text is not None:
        with open(os.path.join(rep, "out_r1b_skew8.txt"), "w",
                  encoding="utf-8") as fh:
            fh.write(skew8_text)
    return os.path.join(rep, "check_doc.py")


def run(path):
    p = subprocess.run([sys.executable, path], capture_output=True, text=True,
                       cwd=os.path.dirname(path))
    return p.returncode, p.stdout + p.stderr


def failures(text):
    return re.findall(r"^  FAILED: (.*)$", text, re.M)


def main():
    print("=" * 78, file=OUT)
    print("W4  F3: the added control, exercised in both directions on the", file=OUT)
    print("    real check_doc.py.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)

    live = open(os.path.join(REPAIR, "check_doc.py"), encoding="utf-8").read()
    skew8 = open(os.path.join(REPAIR, "out_r1b_skew8.txt"),
                 encoding="utf-8").read()
    verdict("the repaired check_doc.py names the new check",
            NEW_CHECK in live)
    verdict("out_r1b_skew8.txt carries its machine-readable line",
            bool(re.search(r"^SKEW8 360\s*$", skew8, re.M)))
    print(file=OUT)

    tmp = tempfile.mkdtemp(prefix="w4_control_")
    try:
        # -- W4a  unmutated -------------------------------------------------
        p = build_tree(os.path.join(tmp, "a"), live, skew8)
        rc, txt = run(p)
        verdict("W4a  unmutated tree: check_doc.py exits 0", rc == 0,
                " (exit %d, failures %r)" % (rc, failures(txt)))

        # -- W4b  SKEW8 360 -> 361 ------------------------------------------
        mut = re.sub(r"^SKEW8 360\s*$", "SKEW8 361", skew8, flags=re.M)
        verdict("the mutation changed the file", mut != skew8)
        p = build_tree(os.path.join(tmp, "b"), live, mut)
        rc, txt = run(p)
        f = failures(txt)
        verdict("W4b  SKEW8 361: check_doc.py exits 1", rc == 1,
                " (exit %d)" % rc)
        verdict("W4b  and the ONLY failure named is the new check",
                f == [NEW_CHECK], " (%r)" % (f,))

        # -- W4c  input missing ---------------------------------------------
        p = build_tree(os.path.join(tmp, "c"), live, None)
        rc, txt = run(p)
        verdict("W4c  out_r1b_skew8.txt absent: check_doc.py exits 1", rc == 1,
                " (exit %d, failures %r)" % (rc, failures(txt)))

        # -- W4d  the pre-repair predicate ----------------------------------
        try:
            old = subprocess.run(
                ["git", "show",
                 "%s:code/branching_repair_41aa/check_doc.py" % PRE_REPAIR_REV],
                capture_output=True, text=True, cwd=ROOT, check=True).stdout
        except Exception as exc:
            old = ""
            print("  (git show failed: %s)" % exc, file=OUT)
        verdict("the pre-repair check_doc.py was recovered from git",
                bool(old))
        verdict("and it does NOT contain the new check", NEW_CHECK not in old)
        if old:
            p = build_tree(os.path.join(tmp, "d"), old, mut)
            rc, txt = run(p)
            verdict("W4d  pre-repair file passes on SKEW8 361 -- F3 confirmed",
                    rc == 0, " (exit %d, failures %r)" % (rc, failures(txt)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(file=OUT)
    print("  READING.  Before this repair the chain from the ENUMERATED n = 8", file=OUT)
    print("  count to the PUBLISHED one was open: the pre-repair check_doc.py", file=OUT)
    print("  passes with the computed count set to 361 while out_young.txt", file=OUT)
    print("  still prints 360.  After it, that same mutation fails, and fails", file=OUT)
    print("  on the new check alone.  The published number never moved: 360", file=OUT)
    print("  is what r1b_skew8.py computed and what W2's skew class count", file=OUT)
    print("  agrees with at every n it reaches.  What changed is whether", file=OUT)
    print("  anything would notice if it did move.", file=OUT)
    print(file=OUT)
    print("=" * 78, file=OUT)
    print("SUMMARY w4_control: failures %d" % BAD[0], file=OUT)
    print("=" * 78, file=OUT)
    return 1 if BAD[0] else 0


if __name__ == "__main__":
    sys.exit(main())
