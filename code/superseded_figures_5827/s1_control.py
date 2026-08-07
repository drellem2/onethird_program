#!/usr/bin/env python3
"""s1 — THE POSITIVE CONTROL AND THE MUTATION TEST (mg-5827).

A sweep that finds nothing and has never been seen to find anything is indistinguishable from a
broken one. This step plants known-stale figures in a THROWAWAY tree and watches the detector
fire, then proves the firing is not vacuous by showing that two CONSTANT detectors — one that
always says CLEAN and one that always says DEFECT — both fail the control set.

Runs entirely under a temporary directory. Touches nothing in the repository.

Exit 0 iff every construction lands on its declared expectation.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib5827 as L                                                  # noqa: E402

FAILURES: list[str] = []
COUNT = 0


def check(name: str, got, want, note: str = "") -> None:
    global COUNT
    COUNT += 1
    ok = got == want
    print("  [%s] %-58s got=%r want=%r%s"
          % ("PASS" if ok else "FAIL", name, got, want, ("  -- " + note) if note else ""))
    if not ok:
        FAILURES.append(name)


def build_tree(root: str, files: dict[str, str]) -> None:
    subprocess.run(["git", "init", "-q", root], check=True, capture_output=True)
    for rel, body in files.items():
        full = os.path.join(root, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(body)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
                    "commit", "-qm", "control"], cwd=root, check=True, capture_output=True)


def run(root: str, reg: L.Registry):
    """Scan `root` as its own repository, with the registry's own directory NOT excluded —
    the control tree has no such directory, so nothing is laundered away."""
    cwd = os.getcwd()
    try:
        os.chdir(root)
        return L.scan(rev=None, root=root, reg=reg)
    finally:
        os.chdir(cwd)


def main() -> int:
    reg = L.Registry.load()
    tmp = tempfile.mkdtemp(prefix="mg5827-control-")
    try:
        # ------------------------------------------------------------------ C1: THE LIVE FIRE
        print(L.banner("C1 — POSITIVE CONTROL: a planted stale figure, in a throwaway tree"))
        print("  The plant is the EXACT sentence that was live in the primary doc tonight.")
        a = os.path.join(tmp, "arm_defect")
        build_tree(a, {
            "docs/paper.md":
                "# A document\n\nWe hold eps_spec < 1 and need "
                "$\\varepsilon_{\\mathrm{spec}}\\approx2\\times10^{-4}$\n"
                "— a factor of roughly $5\\times10^{3}$, with no $n$ in it anywhere.\n",
        })
        occs = run(a, reg)
        d = L.defects(occs)
        check("C1 fires", len(d), 2, "the budget AND the gap factor, both flat text")
        check("C1 exit code", L.main_exit(occs), 1)
        check("C1 entry ids", sorted({o.entry_id for o in d}),
              ["eps_spec_budget", "gap_factor"])

        # ------------------------------------------------------------- C2: THE NEGATIVE ARM
        print(L.banner("C2 — NEGATIVE ARM: the same document, repaired"))
        print("  Same tree, same detector; only the text is repaired. It must go quiet.")
        b = os.path.join(tmp, "arm_clean")
        build_tree(b, {
            "docs/paper.md":
                "# A document\n\nWe hold eps_spec < 1 and need "
                "~~$\\varepsilon_{\\mathrm{spec}}\\approx2\\times10^{-4}$~~ **2×10⁻²**\n"
                "— a factor of roughly ~~$5\\times10^{3}$~~ **50**, with no $n$ in it anywhere.\n",
        })
        occs_b = run(b, reg)
        check("C2 silent", len(L.defects(occs_b)), 0)
        check("C2 exit code", L.main_exit(occs_b), 0)
        check("C2 still SEES them", len(occs_b), 2, "classified REPAIRED, not dropped")
        check("C2 bucket", sorted({o.bucket for o in occs_b}), [L.REPAIRED])

        # ------------------------------------------------- C3: THE MUTATION TEST (2 mutants)
        print(L.banner("C3 — MUTATION TEST: two constant detectors, both must FAIL C1/C2"))
        print("  The C1/C2 pair is only evidence if a detector that ignores its input fails it.")

        always_defect = [L.Occurrence(o.path, o.lineno, o.entry_id, o.matched, o.line,
                                      bucket=L.DEFECT, why="mutant") for o in occs_b]
        check("mutant ALWAYS-DEFECT fails C2", len(L.defects(always_defect)) == 0, False,
              "it reports 2 defects in a clean document")

        always_clean = [L.Occurrence(o.path, o.lineno, o.entry_id, o.matched, o.line,
                                     bucket=L.REPAIRED, why="mutant") for o in occs]
        check("mutant ALWAYS-CLEAN fails C1", len(L.defects(always_clean)) > 0, False,
              "it reports 0 defects in a document with a live stale figure")

        # ------------------------------------------- C4: STRIKETHROUGH MUST BE A CLOSED SPAN
        print(L.banner("C4 — a lone `~~` must not launder a live figure into REPAIRED"))
        c = os.path.join(tmp, "arm_lone_tilde")
        build_tree(c, {
            "docs/paper.md":
                "# A document\n\nSomething ~~struck~~ over here, and the budget is "
                "`2×10⁻⁴` over there.\n",
        })
        occs_c = run(c, reg)
        check("C4 fires", len(L.defects(occs_c)), 1,
              "the value sits OUTSIDE the closed span")

        # ------------------------------------------ C5: RECURSION — the mg-1d6c blind spot
        print(L.banner("C5 — the file list must RECURSE (docs/*.md is os.listdir-shaped)"))
        e = os.path.join(tmp, "arm_nested")
        build_tree(e, {"docs/state-history/deep/note.md": "budget `2×10⁻⁴` as flat text\n"})
        occs_e = run(e, reg)
        check("C5 sees a nested file", len(L.defects(occs_e)), 1,
              "a non-recursive glob would report 0 and look identical to clean")

        # ---------------------------------------- C6: THE INDEX, NOT THE WORKING TREE ALONE
        print(L.banner("C6 — an UNTRACKED file must not be scanned (it is not published)"))
        f = os.path.join(tmp, "arm_untracked")
        build_tree(f, {"docs/tracked.md": "nothing here\n"})
        with open(os.path.join(f, "docs/untracked.md"), "w") as fh:
            fh.write("budget `2×10⁻⁴` as flat text\n")
        occs_f = run(f, reg)
        check("C6 ignores untracked", len(L.defects(occs_f)), 0,
              "scratch files must not fail a published-corpus gate")

        # ------------------------------------- C7: A HISTORICAL REVISION IS READABLE AT ALL
        print(L.banner("C7 — the detector can be pointed at a REVISION, not only at HEAD"))
        occs_g = run(a, reg)
        cwd = os.getcwd()
        try:
            os.chdir(a)
            occs_rev = L.scan(rev="HEAD", root=a, reg=reg)
        finally:
            os.chdir(cwd)
        check("C7 revision scan matches index scan", len(L.defects(occs_rev)),
              len(L.defects(occs_g)),
              "without this the retrospective at mg-2860's base commit is impossible")

        # ------------------------------- C8: A DECLARED AUTHORITY IS NOT FLAGGED, BUT IS SEEN
        print(L.banner("C8 — a declared authority is EXEMPT but still COUNTED"))
        h = os.path.join(tmp, "arm_authority")
        build_tree(h, {
            "docs/state-history/attempt-mg-88bd.md":
                "do not carry `2×10⁻⁴` as flat text; the repaired value is `2×10⁻²`\n",
        })
        occs_h = run(h, reg)
        check("C8 not a defect", len(L.defects(occs_h)), 0)
        check("C8 still counted", len(occs_h), 1, "exempt is not the same as invisible")
        check("C8 bucket", occs_h[0].bucket if occs_h else None, L.AUTHORITY)

        # ----------------------------------- C9: PREFIX MATCHING MUST NOT SWALLOW SIBLINGS
        print(L.banner("C9 — `code/` must not swallow `codex/`, and `a/b` must not swallow `a/bc`"))
        check("_under exact", L._under("code/x.py", "code/"), True)
        check("_under sibling", L._under("codex/x.py", "code/"), False)
        check("_under bare prefix is a path boundary", L._under("docs/ab.md", "docs/a"), False)
        check("_under path segment", L._under("docs/a/b.md", "docs/a"), True)

        # --------------------- C10: THE BLOCKQUOTE RULE MUST BE BOUNDED BY THE BLOCKQUOTE
        print(L.banner("C10 — one blockquote must not launder a value in a DIFFERENT one"))
        print("  The blockquote rule is the widest exemption this detector grants. If its span")
        print("  leaked past a blank line, a single SUPERSEDED anywhere in a file would silence")
        print("  the whole file -- a clean bill of health over a population it never checked.")
        i = os.path.join(tmp, "arm_two_quotes")
        build_tree(i, {
            "docs/paper.md":
                "> **SUPERSEDED** — this block is annotated.\n"
                "> and it says so.\n"
                "\n"
                "Plain prose in between.\n"
                "\n"
                "> the budget is `2×10⁻⁴` and this block says nothing about it\n",
        })
        occs_i = run(i, reg)
        check("C10 second block still fires", len(L.defects(occs_i)), 1,
              "the exemption is bounded by the blank line")

        print(L.banner("C11 — the blockquote span must not run to end-of-file"))
        check("C11 span of a non-quote line", L._blockquote_span(
            ["> a", "", "b", "> c"], 3), (None, None), "line 3 is 'b', not a quote")
        check("C11 span is maximal but bounded", L._blockquote_span(
            ["> a", "> b", "", "> c"], 2), (0, 2))

        # ------------------- C12: THE CENSUS MUST BE A FIXED POINT UNDER ITS OWN TRANSCRIPT
        print(L.banner("C12 — the census must not change because the census was written down"))
        print("  THIS IS A REPAIR OF A DEFECT THIS INSTRUMENT HAD. out_gate.txt records every")
        print("  occurrence found, so on the next run the gate found all of them AGAIN inside")
        print("  the transcript: 691 self-occurrences against 46 real ones, and a total that")
        print("  grew with the number of times anyone had run it. A census that is not a fixed")
        print("  point is not a census.")
        j = os.path.join(tmp, "arm_fixedpoint")
        build_tree(j, {"docs/paper.md": "the budget is `2×10⁻⁴` as flat text\n"})
        before = run(j, reg)
        # Write a transcript INTO the tree, exactly as run_all.sh does, and re-census.
        os.makedirs(os.path.join(j, "code/superseded_figures_5827"), exist_ok=True)
        with open(os.path.join(j, "code/superseded_figures_5827/out_gate.txt"), "w") as fh:
            fh.write(L.render(before, L.DEFECT) + "\n")
        subprocess.run(["git", "add", "-A"], cwd=j, check=True, capture_output=True)
        subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
                        "commit", "-qm", "transcript"], cwd=j, check=True, capture_output=True)
        after = run(j, reg)
        check("C12 total is unchanged by its own transcript", len(after), len(before),
              "before=%d after=%d" % (len(before), len(after)))
        check("C12 defect count unchanged", len(L.defects(after)), len(L.defects(before)))
        check("C12 the transcript is OUT OF THE POPULATION, not merely exempt",
              L.excluded_from_population("code/superseded_figures_5827/out_gate.txt"), True)
        check("C12 the registry stays IN the population",
              L.excluded_from_population("code/superseded_figures_5827/registry.json"), False,
              "the instrument must remain visible to itself")

        print(L.banner("CONTROL SUMMARY"))
        print("  %d constructions, %d failure(s): %s"
              % (COUNT, len(FAILURES), ", ".join(FAILURES) if FAILURES else "none"))
        return 1 if FAILURES else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
