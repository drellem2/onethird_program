#!/usr/bin/env python3
"""mg-16eb — EVERY CHECKABLE CLAIM mg-0049 ADDED, checked against the tree.

WHY THIS FILE EXISTS, AND WHY IT IS NOT coverage218d.py.  mg-218d built `coverage218d.py` to
check `COVERAGE.md`'s sentences against the code.  It does that by reading `delta_control.py`
AS THE GROUND TRUTH BOX — so by construction it cannot check a claim made INSIDE
`delta_control.py`.  mg-0049 put fifty-seven lines of new load-bearing prose into exactly
that file's header.  Nothing in this repository can check them, and this file is the check.

THE SCOPE IS THE DIFF, not the repository: every claim below is one mg-0049 ADDED at 9ca11c4
or 5594c69.  A claim inherited from an earlier generation is that generation's to answer for.

Nothing here mutates anything.  The claims whose test is a mutation are cross-referenced
to `battery16eb.py` and `render16eb.py`, which do the mutating, and their observed values are
restated here rather than re-derived, with the file that produced them named on the row.
"""
import os
import re
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()
CTL_DIR = "code/state_landing_control_2da3"
R0049 = "code/state_delegation_repair_0049"

sys.path.insert(0, os.path.join(REPO, CTL_DIR))
import delta_control as DC          # noqa: E402  — imported, never run
import presentation as PRES         # noqa: E402

_held, _rows = [], []


def read(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
        return fh.read()


def blob(rev, rel):
    return subprocess.run(["git", "-C", REPO, "show", f"{rev}:{rel}"],
                          capture_output=True, text=True, check=True).stdout


def claim(where, text, ok, detail=""):
    _held.append(bool(ok))
    _rows.append((where, text, bool(ok), detail))
    print(f"  [{'holds' if ok else 'BROKEN'}] {where}")
    print(f"           {text}")
    if detail:
        for line in detail.split("\n"):
            print(f"           {line}")


def main():
    print("=" * 96)
    print("mg-16eb — THE CLAIMS mg-0049 ADDED, CHECKED.  Scope: the 9ca11c4 + 5594c69 diff.")
    print("=" * 96)
    print()

    ctl = read(f"{CTL_DIR}/delta_control.py")
    cov = read(f"{CTL_DIR}/COVERAGE.md")
    runsh = read(f"{R0049}/run_all.sh")

    # ---------------------------------------------------------------------------------
    print("1. delta_control.py's HEADER AND TABLE COMMENTS — the file no checker in this")
    print("   repository can check, because every checker reads it as the ground truth.")
    print()

    m = re.search(r"(code/state_delegation_repair_0049/\S+\.py) runs the guards-only\s+"
                  r"control against\s+all (\w+) rows", ctl)
    if m is None:
        claim("delta_control.py", "the guards-only sentence is still in the file",
              False, "the sentence this audit found is gone — re-read the diff")
    else:
        named, count = m.group(1), m.group(2)
        exists = os.path.exists(os.path.join(REPO, named))
        claim("delta_control.py:233",
              f"the guards-only decomposition lives in `{named}`",
              exists,
              f"os.path.exists -> {exists}.  The script that does this is "
              f"{R0049}/split_0049.py.\n"
              f"COVERAGE.md, {R0049}/README.md and {CTL_DIR}/run_all.sh all name it\n"
              f"correctly; delta_control.py is the one document of the four that does not,\n"
              f"and it is the one no checker reads as a claim.")
        pop = len(re.findall(r'^\s*\("R\d+"', read(f"{R0049}/mutations_0049.py"), re.M))
        claim("delta_control.py:233",
              f"that decomposition runs against \"all {count} rows\"",
              count == {6: "six", 9: "nine"}.get(pop, str(pop)),
              f"mutations_0049.ROWS has {pop} rows and split_0049.py runs all of them; "
              f"COVERAGE.md says\n\"all nine rows\" and README.md's table says 9.  "
              f"delta_control.py says \"{count}\", which is mg-5644's population, not this "
              f"one's.")

    claim("delta_control.py:757 (the DELEGATED_PRESENTATION comment)",
          "\"the two tables cannot drift apart quietly in EITHER direction\"",
          False,
          "battery16eb.py A3: a row in DELEGATED and absent here -> exit 2.  That "
          "direction holds.\n"
          "battery16eb.py A1: a row HERE and in nothing else            -> exit 0.\n"
          "battery16eb.py A2: a whole TARGET FILE here and in nothing else -> exit 0.\n"
          "Nothing iterates DELEGATED_PRESENTATION; section 2c iterates DELEGATED and "
          "looks\nrows up in it with .get(..., \"\").  A5 shows mg-bee1's table does NOT "
          "have this\nhole — its keys are cross-checked against the sections the certified "
          "text cites.")

    # `position` is inert and says so on every row — measured over the population.
    target = "docs/state-history/attempt-mg-276d.md"
    tdoc = PRES.Doc(read(target))
    positions = []
    for name in sorted(DC.DELEGATED[target], key=lambda s: (len(s), s)):
        s, e, _b = DC.named_section(read(target), name)
        positions.append(dict(PRES.region_record(tdoc, s - 1, e - 1))["position"])
    claim("delta_control.py:748 (the DELEGATED_PRESENTATION comment)",
          "`position` \"reads 'no block (the span opens on an ATX heading ...)' on every row\"",
          all(p.startswith("no block (the span opens on an ATX heading") for p in positions),
          f"population: all {len(positions)} delegated sections; "
          f"{sum(p.startswith('no block (the span opens on an ATX heading') for p in positions)}"
          f" of {len(positions)} read that way.")

    # The stated baseline commit.
    m = re.search(r"Baselined by mg-0049 against the working tree at (\w+)\.", ctl)
    rev = m.group(1) if m else None
    ok = False
    detail = "the provenance sentence is gone"
    if rev:
        old = blob(rev, target)
        odoc = PRES.Doc(old)
        recomputed = {}
        for name in sorted(DC.DELEGATED[target], key=lambda s: (len(s), s)):
            s, e, _b = DC.named_section(old, name)
            recomputed[name] = PRES.record_digest(PRES.region_record(odoc, s - 1, e - 1))
        ok = recomputed == DC.DELEGATED_PRESENTATION[target]
        detail = (f"all {len(recomputed)} records recomputed from {rev}:{target} and "
                  f"compared to the pinned table.\n"
                  f"({rev} is two commits before mg-0049's parent db2b77d; the target file "
                  f"is byte-identical\nat 8ce78fb, db2b77d and HEAD, so the sentence is "
                  f"imprecise about the base and true about the bytes.)")
    claim("delta_control.py:753", f"\"Baselined by mg-0049 against the working tree at "
          f"{rev}\"", ok, detail)

    # The exit-code semantics against the row that meets them.
    claim("delta_control.py:346 (the EXIT CODES table)",
          "exit 1 is \"a region ... NO LONGER PRESENTED TO A READER\"; exit 2 is drift, "
          "\"re-baseline this instrument\"",
          False,
          "render16eb.py: with `<details>` at the top of the target, both renderers put all\n"
          "5 cited sections inside a never-closed <details> carrying no `open` attribute, so\n"
          "0 of 5 are shown to a reader.  That is R1's and R8's outcome, which the same\n"
          "table classifies exit 1.  battery16eb.py B3 and mg-0049's own R5: exit 2.\n"
          "The instruction attached to exit 2 is to re-baseline — that is, to accept it.")
    print()

    # ---------------------------------------------------------------------------------
    print("2. presentation.py's HEADER — same file class, same absence of a checker.")
    print()
    claim("presentation.py:24",
          "\"NOTHING IN THIS FILE CHANGED EXCEPT ONE MESSAGE AND FOUR SELF-TEST CASES\"",
          True,
          "the 11 certified presentation digests in PRESENTATION are byte-identical to "
          "db2b77d's\n(git diff over the table is empty) and delta_control.py exits 0 on the "
          "clean tree, so the\nnew `opens_on_heading` branch changes no certified record: no "
          "certified region's span\nopens on an ATX heading.")
    print()

    # ---------------------------------------------------------------------------------
    print("3. COVERAGE.md — the ONE added document that has an external checker "
          "(coverage218d.py).")
    print()
    split_out = read(f"{R0049}/out_split.txt")
    pop = len(re.findall(r'^\s*\("R\d+"', read(f"{R0049}/mutations_0049.py"), re.M))
    claim("COVERAGE.md:276", "\"split_0049.py measures this over all nine rows\"",
          "all nine rows" in cov and pop == 9, f"mutations_0049.ROWS has {pop} rows.")
    for figure in ("— 8 of 9", "— 4 of 9", "— 2 of 9"):
        claim("COVERAGE.md:276-278", f"the regime figure \"{figure.strip('— ')}\"",
              figure in split_out,
              "found in out_split.txt, which this audit reproduced byte-identically "
              "from its own run.")
    claim("COVERAGE.md:243-244",
          "the R1/R2 table: exit 0 against mg-bee1, exit 1 against mg-0049",
          True,
          "mg-5644's own battery re-run UNMODIFIED by this audit prints "
          "\"expected exit 0 ... got exit 1\"\nfor Q1 and Q2, and the re-run is "
          "byte-identical to the committed out_5644_rerun.txt.")
    print()

    # ---------------------------------------------------------------------------------
    print("4. THE mg-0049 README's 'What is NOT undone' TABLE — the table that answers the")
    print("   over-correction question, so a wrong cross-reference in it is load-bearing.")
    print()
    sections = dict((int(n), t) for n, t in
                    re.findall(r'^echo "### (\d+)\. (.+)$', runsh, re.M))
    n_218d = [n for n, t in sections.items() if "coverage218d" in t]
    n_5644 = [n for n, t in sections.items() if "mg-5644's OWN battery" in t]
    claim(f"{R0049}/README.md:105-106",
          "mg-218d's and mg-5644's batteries are \"re-run in section 7 of run_all.sh\"",
          False,
          f"run_all.sh's section 7 is {sections.get(7, '(absent)')!r}.\n"
          f"mg-5644's battery is section {n_5644[0] if n_5644 else '?'}, and mg-218d's "
          f"sixteen are re-run\ninside it (mg-5644's own run_all.sh section 5).  Both rows "
          f"of the table say 7.\nThe re-runs THEMSELVES happen and this audit reproduced "
          f"both byte-identically;\nwhat is wrong is only the pointer.")
    rnd = read(f"{R0049}/out_render.txt")
    claim(f"{R0049}/README.md:152", "render0049.py: \"100 comparisons\"",
          "100 comparisons" in rnd, "found in out_render.txt, reproduced by this audit.")
    covout = read(f"{R0049}/out_coverage218d.txt")
    claim(f"{R0049}/README.md:110", "coverage218d.py: \"40 of 40\"",
          "40 of 40" in covout, "found in out_coverage218d.txt, reproduced by this audit.")
    claim(f"{R0049}/README.md:23", "mg-5644's renderers agreed \"over 60 comparisons\"",
          "60 comparisons" in read("code/state_delegation_audit_5644/out_render.txt"),
          "found in mg-5644's own committed out_render.txt, which this audit reproduced.")
    print()

    # ---------------------------------------------------------------------------------
    print("5. render0049.py's OWN VERDICT — the repair's instrument for 'what a reader is")
    print("   shown', on the one row where it is asked about a container.")
    print()
    claim(f"{R0049}/render0049.py:11 and out_render.txt",
          "R5: \"`<details>` at the top SUPPRESSES NOTHING: every cited section is still on "
          "the page as the document's own prose\" — 5/5 ANY, 5/5 HEADING, both renderers",
          False,
          "render16eb.py, same two renderers, same mutation: 5 of 5 cited sections have "
          "their\nTEXT IN THE HTML — which is the number render0049.py measures — and 0 of "
          "5 are SHOWN\nto a reader, because every one is a descendant of a <details> that "
          "is never closed and\ncarries no `open` attribute.  `</details>` occurrences in "
          "the rendered page: 0.\n"
          "\"Is the text in the artefact?\" versus \"is a reader shown it?\" is the exact "
          "distinction\nmg-4acd was landed to draw.  It is the repair's own visibility "
          "instrument that does not\ndraw it, on the one row of the five where the mutation "
          "is a CONTAINER rather than a\nsuppressor.")
    print()

    print("=" * 96)
    held = sum(_held)
    print(f"{held} of {len(_held)} checkable claims mg-0049 ADDED hold against the tree.")
    broken = [(w, t) for w, t, ok, _d in _rows if not ok]
    print(f"{len(broken)} do not:")
    for where, text in broken:
        print(f"    {where}\n        {text}")
    print()
    inside = [w for w, _t, ok, _d in _rows if not ok and "delta_control.py" in w]
    print(f"WHERE THE BROKEN ONES ARE.  {len(inside)} of the {len(broken)} are in")
    print("delta_control.py, the file coverage218d.py reads as the ground truth box and")
    print("therefore cannot check.  0 are in COVERAGE.md, the one added document that has an")
    print("external checker — and COVERAGE.md names split_0049.py and 'all nine rows'")
    print("correctly in the same paragraph where delta_control.py does not.")
    print("=" * 96)
    return 0


if __name__ == "__main__":
    sys.exit(main())
