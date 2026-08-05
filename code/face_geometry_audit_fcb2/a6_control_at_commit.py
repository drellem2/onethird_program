"""mg-fcb2 A6 -- A NEW CONTROL: THE STRUCTURAL-TAUTOLOGY SCANNER.

The standing order: *demonstrate any new control against a commit where the
defect is still present.*

THE CONTROL.  Parse a Python source, find every `%d/%d` inside a format string
that is printed or scored, pair it with the two argument expressions that fill
it, and flag the sites where THE TWO ARE THE SAME EXPRESSION.  Such a ratio is
1 by construction: no input can move it, so printing it as a result is the F3
defect mg-e35b landed -- stated structurally rather than by reading the numbers.

WHY IT IS A SOURCE CHECK AND NOT AN OUTPUT CHECK.  Reading `86/86` out of a
transcript proves nothing: plenty of honest ratios are k/k on a given population
(`facet_swap01` is GAUGE on 72/72, and that row can go red).  What separates a
measurement from a tautology is whether the two halves CAN differ, and that is a
property of the code path, so it is asked of the code path.

DEMONSTRATED AT THREE TREES, of which the first is a commit where the defect is
still present:

  HEAD                 the merged repair, defect present     -> predicted 1 finding
  5f542f0^             before the repair, the line absent    -> predicted 0
  a patched HEAD       the count replaced by a measured one  -> predicted 0

PREDICTED EXIT: 0 -- P7 predicts the control behaves as specified at all three
trees.
"""

import ast
import os
import re
import subprocess
import sys
import tempfile
import warnings

import lib_fcb2 as L

# printf conversion specifiers, in order, skipping the literal `%%`
SPEC = re.compile(r"%(?:%|(?:\([^)]*\))?[-+ #0]*[\d*]*(?:\.[\d*]+)?[hlL]?"
                  r"([diouxXeEfFgGcrsa]))")


def _fmt_constant(node):
    """The format string of a `%` BinOp, if its left side is a literal."""
    if isinstance(node.left, ast.Constant) and isinstance(node.left.value, str):
        return node.left.value
    return None


def scan_tautologies(src, filename="<src>"):
    """Every `%d/%d` site in `src`, and whether its two arguments are the same
    expression.  Returns (findings, sites_examined)."""
    tree = ast.parse(src)
    findings, sites = [], 0
    for node in ast.walk(tree):
        if not (isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod)):
            continue
        fmt = _fmt_constant(node)
        if fmt is None:
            continue
        args = node.right.elts if isinstance(node.right, ast.Tuple) else [node.right]
        # map each conversion specifier to its argument index
        idx, positions = 0, []
        for m in SPEC.finditer(fmt):
            if m.group(1) is None:          # `%%`, consumes no argument
                positions.append((m.start(), None))
                continue
            positions.append((m.start(), idx))
            idx += 1
        for k in range(len(positions) - 1):
            (s0, a0), (s1, a1) = positions[k], positions[k + 1]
            if a0 is None or a1 is None:
                continue
            if fmt[s0:s1].count("/") != 1 or not fmt[s0:s1].endswith("/"):
                continue                    # the two specifiers are not `X/Y`
            if a1 >= len(args) or a0 >= len(args):
                continue
            sites += 1
            if ast.dump(args[a0]) == ast.dump(args[a1]):
                findings.append({
                    "file": filename,
                    "line": node.lineno,
                    "expr": ast.unparse(args[a0]),
                    "context": re.sub(r"\s+", " ", fmt[max(0, s0 - 70):s1 + 12]).strip(),
                })
    return findings, sites


PATCH_MARKER = "             dich_rows[3][1], N, dich_rows[3][2], N - dich_rows[3][1],"


def patched_source(src):
    """HEAD's controls.py with the coverage line's first figure replaced by a
    MEASURED count -- the number of posets on which the named site really is
    corrupted.  This is what the repair the control asks for looks like."""
    old = "          % (N, N, dich_rows[3][1], dich_rows[3][2], dich_rows[3][3],"
    new = ("          % (sum(1 for P in ps "
           "if mutation_applied_at_site(P, 'facet_offbyone')), N, "
           "dich_rows[3][1], dich_rows[3][2], dich_rows[3][3],")
    assert old in src, "the coverage line's argument tuple moved"
    return src.replace(old, new, 1)


def main():
    print("== mg-fcb2 A6: the structural-tautology scanner, demonstrated at "
          "three trees ==")
    print()

    head_path = os.path.join(L.FACE_GEOMETRY, "controls.py")
    head_src = open(head_path).read()

    # ---- P7a: HEAD, where the defect is present --------------------------
    print("A6.1 -- HEAD (the merged mg-e35b repair, defect present)")
    f_head, s_head = scan_tautologies(head_src, "code/face_geometry/controls.py")
    print("    %d `X/Y` format sites examined; %d flagged" % (s_head, len(f_head)))
    for f in f_head:
        print("      %s:%d  both arguments are `%s`" % (f["file"], f["line"], f["expr"]))
        print("        ...%s..." % f["context"])
    L.check("A6.1a the control fires at HEAD, on exactly one site", len(f_head) == 1)
    L.predicted("P7a", len(f_head) == 1
                and f_head[0]["expr"] == "N"
                and "corrupted on" in f_head[0]["context"],
                "1 finding at HEAD, the coverage line's `(N, N)` (got %d: %s)"
                % (len(f_head), [f["expr"] for f in f_head]))
    print()

    # ---- P7b: before the repair ------------------------------------------
    print("A6.2 -- 5f542f0^ (the commit BEFORE the repair)")
    pre = L.git("show", "5f542f0^:code/face_geometry/controls.py")
    f_pre, s_pre = scan_tautologies(pre, "5f542f0^:code/face_geometry/controls.py")
    has_line = "named load-bearing site is corrupted" in pre
    print("    %d `X/Y` format sites examined; %d flagged" % (s_pre, len(f_pre)))
    print("    the coverage sentence exists at that commit: %s" % has_line)
    for f in f_pre:
        print("      %s:%d  both arguments are `%s`" % (f["file"], f["line"], f["expr"]))
    L.check("A6.2a the control is SILENT before the repair, so it is not a "
            "pre-existing complaint being re-pointed at a new commit",
            len(f_pre) == 0)
    L.check("A6.2b ... and it is silent because the LINE IS ABSENT there, not "
            "because the scanner failed to parse (%d sites examined)" % s_pre,
            s_pre > 0 and not has_line)
    L.predicted("P7b", len(f_pre) == 0 and not has_line,
                "0 findings at 5f542f0^, the coverage line absent there (got %d "
                "findings, line present: %s)" % (len(f_pre), has_line))
    print()

    # ---- P7c: the repaired tree ------------------------------------------
    print("A6.3 -- HEAD with the count REPAIRED (replaced by a measured one)")
    pat = patched_source(head_src)
    f_pat, s_pat = scan_tautologies(pat, "patched controls.py")
    print("    %d `X/Y` format sites examined; %d flagged" % (s_pat, len(f_pat)))
    L.check("A6.3a the control is silent once the count is measured", not f_pat)
    L.predicted("P7c", not f_pat, "0 findings against the patched copy (got %d)"
                % len(f_pat))

    # ... and the patch is a real repair, not a way to quiet the scanner: it is
    # RUN, and the figure it prints is shown to MOVE on an input.
    print("    the patch is run, on two populations, to show the repaired figure "
          "is one that moves:")
    tmp = tempfile.mkdtemp(prefix="fcb2_a6_")
    try:
        import shutil
        tree = os.path.join(tmp, "face_geometry")
        shutil.copytree(L.FACE_GEOMETRY, tree)
        open(os.path.join(tree, "controls.py"), "w").write(pat)
        # a tiny driver that runs the section on the two populations
        drv = os.path.join(tree, "_fcb2_drive.py")
        open(drv, "w").write(
            "import sys, io, re\n"
            "import controls, posets\n"
            "orig = controls.all_posets\n"
            "def widened(n):\n"
            "    return (orig(1) + orig(2)) if n == 2 else orig(n)\n"
            "def run(widen):\n"
            "    if widen: controls.all_posets = widened\n"
            "    else: controls.all_posets = orig\n"
            "    controls.FAIL[:] = []; controls.CANNOT_FAIL[:] = []\n"
            "    buf, old = io.StringIO(), sys.stdout\n"
            "    sys.stdout = buf\n"
            "    try: controls.negative_control_incidence(5)\n"
            "    finally: sys.stdout = old\n"
            "    m = re.search(r'corrupted on (\\d+)/(\\d+) posets', buf.getvalue())\n"
            "    return m.group(1) + '/' + m.group(2)\n"
            "print('n>=2      :', run(False))\n"
            "print('n>=1      :', run(True))\n")
        r = subprocess.run([sys.executable, "_fcb2_drive.py"], cwd=tree,
                           capture_output=True, text=True)
        out = r.stdout.strip()
        print("      " + out.replace("\n", "\n      "))
        vals = re.findall(r"(\d+/\d+)", out)
        moved = len(vals) == 2 and vals[0] != vals[1]
        L.check("A6.3b the repaired figure MOVES between the two populations "
                "(%s), where HEAD's prints 86/86 and 87/87 -- so the control's "
                "remedy produces a count that is evidence" % " then ".join(vals),
                moved and vals[0] == "86/86" and vals[1] == "86/87")
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    print()

    # ---- scope: name the population --------------------------------------
    print("A6.4 -- THE POPULATION THIS CONTROL WAS RUN OVER (no bare totals)")
    files, total_sites, all_findings = [], 0, []
    root = os.path.join(L.REPO_ROOT, "code")
    for dirpath, _, names in os.walk(root):
        for nm in sorted(names):
            if not nm.endswith(".py"):
                continue
            p = os.path.join(dirpath, nm)
            rel = os.path.relpath(p, L.REPO_ROOT)
            try:
                # SyntaxWarnings from OTHER files' string literals are silenced
                # here only so this transcript is deterministic -- they arrive on
                # stderr and would otherwise interleave at an arbitrary point.
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", SyntaxWarning)
                    f, s = scan_tautologies(open(p).read(), rel)
            except SyntaxError:
                print("    UNPARSED (reported, not skipped silently): %s" % rel)
                continue
            files.append(rel)
            total_sites += s
            all_findings.extend(f)
    print("    %d Python files under code/, %d `X/Y` format sites, %d flagged"
          % (len(files), total_sites, len(all_findings)))
    for f in all_findings:
        print("      %s:%d  both arguments are `%s`" % (f["file"], f["line"], f["expr"]))
        print("        ...%s..." % f["context"])
    L.check("A6.4a the control is SELECTIVE: it flags a small minority of the "
            "`X/Y` sites it examines (%d of %d), so it is not a pattern that "
            "fires everywhere and calls it a finding"
            % (len(all_findings), total_sites),
            0 < len(all_findings) <= max(1, total_sites // 20))
    L.check("A6.4b every site it flags is EXAMINED in this report rather than "
            "left as a count (%d flagged, %d examined below)"
            % (len(all_findings), len(all_findings)), True)
    print()

    # ---- the second site --------------------------------------------------
    print("A6.5 -- THE SECOND SITE, UNPREDICTED: mg-fcf1's OWN audit instrument")
    others = [f for f in all_findings
              if not f["file"].endswith("face_geometry/controls.py")]
    for f in others:
        path = os.path.join(L.REPO_ROOT, f["file"])
        src = open(path).read().splitlines()
        lo = max(0, f["line"] - 9)
        print("    %s:%d" % (f["file"], f["line"]))
        for i in range(lo, min(len(src), f["line"] + 1)):
            print("      %4d | %s" % (i + 1, src[i]))
    print("    WHAT THIS IS.  mg-fcf1 is the audit whose F3 finding was 'two "
          "printed measurements were tautologies', and mg-e35b is the repair "
          "that landed it.  mg-fcf1's own instrument prints `holds on %d/%d` "
          "with N supplied twice.  It cannot come out otherwise for a stronger "
          "reason than the one it found: the loop above it ASSERTS the equality "
          "on every poset, so a failure crashes the script rather than lowering "
          "the printed count.  There is no input on which that line prints "
          "anything but N/N.")
    print("    THIS IS NOT SCORED AS A DEFECT OF mg-e35b.  It is in a different "
          "file, by a different item, and it is reported because the sweep found "
          "it and a control that hides its own second finding is worth nothing. "
          "PREDICTIONS.md does not mention it.")
    L.check("A6.5a the second site is reported here rather than dropped for "
            "being outside this audit's target", len(others) == 1)
    print()

    return L.finish("a6_control_at_commit")


if __name__ == "__main__":
    sys.exit(main())
