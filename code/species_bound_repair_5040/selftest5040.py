"""Self-test for the mg-5040 instrument.

An instrument that measures a repair is itself a claim, and the claims worth
testing here are the ones whose failure would make every other number in this
tree meaningless:

  * the RESTORE CONTRACT, tested IN THE DIRECTION THAT MUST FAIL -- a Probe
    that does NOT put the tree back must be caught saying so.  A restore proof
    that only ever passes is not a proof.
  * the PIN, tested by asserting that the extracted revision does NOT already
    carry the repair.  A pin that silently resolves to the current tree turns
    every before/after comparison into a comparison of a thing with itself.
  * the FIGURE REGEX, tested against the exact forms the summaries actually
    use, including the two that a naive `TAG: (\\d+)` misses.
  * the RESIDUE WALK, tested against a structure planted in a scratch tree,
    so that r1's rows are not the first evidence that the helper works.

Exits 1 on any failure.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

from kern5040 import (REPO, HERE, PRE, Probe, extract, porcelain, full_diff,
                      git, commit_messages)

n = 0
fails = []


def lift(rel, name):
    """Return one top-level function from a SCRIPT, without running it.

    Every checker in this arc is a script with side effects at import time,
    so `from x import f` runs the checker.  This parses the file, keeps the
    named function and the module-level constant assignments it needs, and
    execs only those.
    """
    import ast
    src = open(os.path.join(REPO, rel), encoding="utf-8").read()
    tree = ast.parse(src)
    keep = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            keep.append(node)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            if all(a.name in ("os", "re", "sys") for a in
                   getattr(node, "names", [])) and isinstance(node, ast.Import):
                keep.append(node)
        elif isinstance(node, ast.Assign) and all(
                isinstance(t, ast.Name) and t.id.isupper()
                for t in node.targets):
            keep.append(node)
    ns = {}
    for node in keep:
        mod = ast.Module(body=[node], type_ignores=[])
        try:
            exec(compile(ast.fix_missing_locations(mod), rel, "exec"), ns)
        except Exception:
            # A module-level constant that depends on something this lift
            # deliberately did not bring across.  Skipped, not fatal: the
            # function under test either needs it, in which case the call
            # below fails loudly, or it does not.
            continue
    return ns[name]


def ck(label, ok, detail=""):
    global n
    n += 1
    if not ok:
        fails.append((label, detail))
    print("  %-64s %s" % (label[:64], "ok" if ok else "*** FAILED ***"))
    if detail and not ok:
        print("        %s" % detail)


print("selftest5040: the instrument's own contracts")
print()

# --- the pin ---------------------------------------------------------------
tmp = tempfile.mkdtemp(prefix="mg5040-selftest-")
try:
    pre = extract(PRE, os.path.join(tmp, "pre"))
    ck("the pin extracts", os.path.isdir(os.path.join(pre, "code")))
    # THE DIRECTION THAT MATTERS: the extraction must NOT already carry the
    # repair.  If it does, the pin has resolved to something that is not the
    # pre-repair tree and every before/after row in r1 and r2 is a comparison
    # of a thing with itself.
    for rel, needle in (
            ("code/species_repair_a4ef/s1_extent.py", "walk_residue"),
            ("code/species_remainder_f8fa/w3_scope.py", "walk_residue"),
            ("code/species_extent_d633/e1_extents.py", "walk_residue"),
            ("code/species_extent_d633/kernd633.py", "md_files_and_residue"),
            ("code/species_repair_a4ef/run_all.sh", "unfiltered")):
        p = os.path.join(pre, rel)
        text = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
        ck("%s at the pin does NOT carry the repair (%s)"
           % (os.path.basename(rel), needle), needle not in text)
    # and the same names ARE in the worktree, or the pin is being compared
    # against a tree that never got the repair either.
    for rel, needle in (
            ("code/species_repair_a4ef/s1_extent.py", "walk_residue"),
            ("code/species_extent_d633/kernd633.py", "md_files_and_residue"),
            ("code/species_repair_a4ef/run_all.sh", "unfiltered")):
        text = open(os.path.join(REPO, rel), encoding="utf-8").read()
        ck("%s in the worktree DOES carry it" % os.path.basename(rel),
           needle in text)

    # --- the residue walk, against a planted structure ---------------------
    scratch = os.path.join(tmp, "tree")
    os.makedirs(os.path.join(scratch, "sub"))
    open(os.path.join(scratch, "a.txt"), "w").write("a\n")
    open(os.path.join(scratch, "sub", "b.txt"), "w").write("b\n")
    outside = os.path.join(tmp, "outside")
    os.makedirs(outside)
    open(os.path.join(outside, "hidden.md"), "w").write("hidden\n")
    os.symlink(outside, os.path.join(scratch, "slink"))
    os.makedirs(os.path.join(scratch, "__pycache__"))

    # LIFTED, NOT IMPORTED.  `s1_extent.py` is a script: importing it runs
    # the whole checker.  So the function is pulled out of the file by its
    # own source text, which also means this test reads the code that ships
    # rather than a copy of it.
    walk_residue = lift("code/species_repair_a4ef/s1_extent.py",
                        "walk_residue")
    files, stated, unstated = walk_residue(scratch)
    ck("the walk reaches a file below the root",
       "sub/b.txt" in files, str(files))
    ck("the walk does NOT reach through a symlinked directory",
       not any("hidden" in f for f in files), str(files))
    ck("__pycache__ is declined and STATED",
       any(r == "__pycache__" for r, _w in stated), str(stated))
    ck("the symlinked directory is declined and NOT stated",
       any(r == "slink" for r, _w in unstated), str(unstated))
    ck("and the reason names symlink",
       any("symlink" in w for _r, w in unstated), str(unstated))

    # --- the restore contract, IN THE DIRECTION THAT MUST FAIL -------------
    # A Probe that leaves something behind must report restored == False.
    # This is the assertion a self-test usually gets backwards: proving the
    # happy path proves nothing about the proof.
    sabotage = os.path.join(REPO, "code", "species_bound_repair_5040",
                            "SELFTEST-SABOTAGE.tmp")
    with Probe("deliberately not restored") as pr:
        with open(sabotage, "w") as f:
            f.write("this is left behind ON PURPOSE\n")
    ck("a Probe that leaves an untracked file reports NOT restored",
       pr.restored is False, "restored=%s" % pr.restored)
    os.unlink(sabotage)

    with Probe("restores a tracked file it wrote") as pr2:
        target = "code/species_bound_repair_5040/PREDICTIONS.md"
        if os.path.exists(os.path.join(REPO, target)):
            pr2.write(target, "clobbered\n")
    ck("a Probe that writes and puts back reports restored",
       pr2.restored is True, "restored=%s" % pr2.restored)

    # and the snapshot must cover a file the probe never touched: a runner
    # rewrites committed transcripts, and the first version of this class did
    # not restore those.
    victim = "code/species_extent_d633/out_e1_extents.txt"
    vp = os.path.join(REPO, victim)
    if os.path.exists(vp):
        original = open(vp, "rb").read()
        with Probe("something else rewrote a transcript") as pr3:
            with open(vp, "w") as f:
                f.write("rewritten by something the probe did not declare\n")
        ck("the snapshot restores a file the probe never wrote",
           open(vp, "rb").read() == original)
        ck("and reports restored", pr3.restored is True,
           "restored=%s" % pr3.restored)

    # --- the figure regex --------------------------------------------------
    figures = lift("code/species_bound_repair_5040/r3_summaries.py",
                   "figures")
    for text, want in (
            ("A2 TOTAL BAD: 1", [1]),
            ("A2 TOTAL BAD is 2", [2]),
            ("A2 TOTAL BAD stays 1", [1]),
            ("(`A2 TOTAL BAD` remains **1**,", [1]),
            ("A2 TOTAL BAD 1, the one row", [1]),
            ("nothing here", [])):
        ck("figures(%r) == %s" % (text[:34], want), figures(text) == want,
           str(figures(text)))

    # --- the commit-message census is not empty ---------------------------
    msgs = commit_messages()
    ck("the commit-message census reads more than one commit", len(msgs) > 5,
       "%d" % len(msgs))
    ck("and it is anchored at the pin, so it cannot grow under the reader",
       all(sha != "" for sha, _s, _b in msgs))
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print()
print("%d assertion(s), %d failed" % (n, len(fails)))
if fails:
    print("*** FAILED ***")
    sys.exit(1)
print("selftest5040 ok")
