"""mg-79ba A3 -- THE REPAIR OF A1's FINDING IS BLOCKED BY mg-17aa's OWN CONTROL.

mg-17aa re-aimed three instruments belonging to other tickets, and said in its
own `unverified` list that "neither re-aim was reviewed by the tickets that own
those instruments".  One of them is the reason this section exists.

`code/face_geometry_landing_da45/verify_landing.py` TARGET 3 used to score
three SOURCE LITERALS of `controls.py`, and mg-17aa correctly diagnosed the
shape: they froze the DEFERRAL, so the verifier necessarily went red the day
the deferred item landed.  mg-17aa replaced them.  With three more source
literals -- of the post-mg-17aa state.  One of them is

    "theorem_absorb == 0 and theorem_blocked == theorem_app" in src

which is a VERBATIM FREEZE OF THE CONJUNCT A1 SHOWS IS A TAUTOLOGY.  So the
minimal honest repair of A1's finding -- delete the tautological conjunct, or
replace it with a contingent one -- turns that check BROKEN.

That is my ticket's own question with the polarity my ticket asked for, and the
answer is YES: an added control goes RED when the underlying defect is FIXED.
It is not in `controls.py`'s battery, which is where mg-17aa looked and where
A2 finds nothing; it is in the foreign instrument mg-17aa re-aimed while
repairing exactly this shape in that instrument's previous version.  The
instrument's own defect class, one generation on, in the same file.

WHAT IS RUN.  A staged tree: `code/face_geometry/` with the repair applied and
`code/face_geometry_landing_da45/` beside it, so `verify_landing.py`'s own
`REPO`/`FG` resolution reaches the repaired copy and nothing writes to the real
one.  Three repairs are tried, because a finding that depends on one spelling
of the fix is a finding about the spelling.

ALSO IN THIS FILE, and both are SMALLER than they look -- see README.md:

  A3.2  `d4_auditor_rerun.py` scores `n == want_broken`, an exact two-sided
        freeze on another audit's BROKEN count.  mg-17aa moved the literal
        4 -> 5 rather than the shape.  Structural check only; not demonstrated.
  A3.3  P8 SCORED AS A MISS.  `out_e3_seams.txt` IS stale against a live run,
        and mg-17aa neither caused it nor hid it: the transcript was last
        written at mg-d0e2's own commit, `controls_output.txt` has moved seven
        times since, and mg-17aa states its policy for that file in terms.

Run: python3 a3_repair_blocked.py
"""

import ast
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern79ba import (                                          # noqa: E402
    ANCHOR_COND, BAR, FG, REPO, Score, head, run, sandbox,
)

S = Score()

# Three spellings of the minimal honest repair of A1's finding.  Each removes
# the tautological conjunct; none touches the routing, the row's other
# conjunct, or any count the row prints.
REPAIRS = {
    "drop the tautological conjunct":
        "              theorem_absorb == 0,",
    "keep it but say what it is":
        "              theorem_absorb == 0    # theorem_blocked == theorem_app\n"
        "              and True,             # is FORCED by `forced = "
        "(blocked == app)`",
    "replace it with a contingent one":
        "              theorem_absorb == 0 and theorem_blocked <= theorem_app,",
}


def staged(repair_src):
    """A tree in which verify_landing.py's own REPO/FG resolution reaches a
    repaired copy of code/face_geometry/ and the real tree is untouched."""
    fgtmp = sandbox(repair_src)
    root = os.path.join(os.path.dirname(fgtmp), os.path.basename(fgtmp) + "_repo")
    code = os.path.join(root, "code")
    os.makedirs(code, exist_ok=True)
    shutil.copytree(fgtmp, os.path.join(code, "face_geometry"))
    shutil.copy(os.path.join(FG, "controls_output.txt"),
                os.path.join(code, "face_geometry", "controls_output.txt"))
    for d in ("face_geometry_landing_da45", "face_geometry_audit_fcf1"):
        src = os.path.join(REPO, "code", d)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(code, d))
    shutil.rmtree(fgtmp, ignore_errors=True)
    return root


def target3_lines(out):
    """The claims TARGET 3 scored, and their verdicts."""
    keep, on = [], False
    for line in out.split("\n"):
        if "TARGET 3" in line:
            on = True
        elif line.startswith("=") or "TARGET 4" in line:
            on = False
        if on and line.strip().startswith(("[ok]", "[BROKEN]", "[OK]", "[FAIL]",
                                           "  [")):
            keep.append(line.strip())
    return keep


def section_1():
    head("A3.1 -- THE MINIMAL REPAIR OF A1's FINDING, RUN THROUGH mg-17aa's "
         "OWN RE-AIMED VERIFIER")
    ctl = open(os.path.join(FG, "controls.py")).read()
    vl = open(os.path.join(REPO, "code", "face_geometry_landing_da45",
                           "verify_landing.py")).read()
    S.claim("verify_landing.py TARGET 3 freezes the conjunct A1 shows is a "
            "tautology, as a source literal",
            '"theorem_absorb == 0 and theorem_blocked == theorem_app" in src'
            in vl)
    S.claim("and it freezes two more of mg-17aa's own source literals beside "
            "it -- the routing quantity and the clause's new home",
            '"forced = (blocked == app)" in src' in vl
            and '\'st["absorb"] == 0\' in src' in vl,
            "so a THIRD forced gate, or any renaming of `blocked`, breaks it "
            "too -- the routing quantity is exactly what mg-17aa itself "
            "widened from one gate to two")
    S.claim("mg-17aa re-aimed this target because its PREVIOUS three literals "
            "had the same shape, and says so in the file",
            "it froze the DEFERRAL itself" in vl
            and "necessarily goes red the day it" in vl,
            "the diagnosis is right and is written down one screen above the "
            "three new literals")

    # baseline: does the unrepaired staged tree pass?
    root = staged(None)
    p = subprocess.run([sys.executable, "verify_landing.py"],
                       cwd=os.path.join(root, "code",
                                        "face_geometry_landing_da45"),
                       capture_output=True, text=True)
    base_out = p.stdout + p.stderr
    S.claim("baseline: the staged (unrepaired) tree runs verify_landing.py to "
            "exit %d, so the staging itself is not what breaks it"
            % p.returncode, p.returncode == 0,
            "%d line(s) of output" % len(base_out.split("\n")))
    shutil.rmtree(root, ignore_errors=True)

    broke = []
    for label, new in REPAIRS.items():
        src = ctl.replace(ANCHOR_COND, new)
        if src == ctl:
            S.claim("repair %r applies" % label, False, "anchor not found")
            continue
        root = staged(src)
        fgdir = os.path.join(root, "code", "face_geometry")
        code, out = run(fgdir)
        S.claim("repair %r leaves the BATTERY green (exit %d) -- the repair is "
                "honest and changes no verdict" % (label, code), code == 0)
        p = subprocess.run([sys.executable, "verify_landing.py"],
                           cwd=os.path.join(root, "code",
                                            "face_geometry_landing_da45"),
                           capture_output=True, text=True)
        vout = p.stdout + p.stderr
        red = [l for l in target3_lines(vout) if "BROKEN" in l or "FAIL" in l]
        hit = ("theorem_absorb == 0 and theorem_blocked == theorem_app"
               in vout and p.returncode != 0)
        broke.append(hit)
        print("    %-38s verify_landing exit %d" % (label[:38], p.returncode))
        for l in red[:3]:
            print("      %s" % l[:150])
        S.claim("...and it turns verify_landing.py RED (exit %d).  The battery "
                "the repair is FOR stays green; the instrument mg-17aa "
                "re-aimed goes red BECAUSE the repair happened"
                % p.returncode, p.returncode != 0)
        shutil.rmtree(root, ignore_errors=True)

    S.claim("ALL THREE SPELLINGS OF THE REPAIR ARE BLOCKED, so this is a "
            "property of the freeze and not of one wording.  A control that "
            "goes red the day its own ticket's defect is fixed is the shape "
            "mg-e35b named, the shape mg-17aa found four instances of, and "
            "the shape mg-17aa wrote a fifth instance of while removing the "
            "fourth", all(broke) and len(broke) == len(REPAIRS),
            "blocked: %d of %d" % (sum(broke), len(REPAIRS)))


def section_2():
    head("A3.2 -- THE OTHER RE-AIM: AN EXACT TWO-SIDED FREEZE ON ANOTHER "
         "AUDIT'S BROKEN COUNT")
    p = os.path.join(REPO, "code", "face_geometry_instr_5f9a",
                     "d4_auditor_rerun.py")
    src = open(p).read()
    S.claim("d4_auditor_rerun.py scores another audit's BROKEN count with "
            "EXACT equality against a literal (`n == want_broken`)",
            "n == want_broken" in src)
    lits = [n.value for n in ast.walk(ast.parse(src))
            if isinstance(n, ast.Constant) and isinstance(n.value, int)
            and n.value in (4, 5, 6)]
    S.claim("and mg-17aa moved the literal 4 -> 5 rather than the shape, so "
            "the next person to FIX one more of e3_seams.py's flagged claims "
            "makes it 6 and this instrument goes red on the improvement",
            "(\"e3_seams.py\", 5," in src,
            "the file's own comment for the change says exactly that: 'the "
            "claim is false BECAUSE THE DEFECT IT FLAGGED WAS FIXED -- an "
            "audit record going red the day its finding is acted on'")
    S.claim("THIS IS REPORTED, NOT DEMONSTRATED.  Turning it red needs an edit "
            "to code/face_geometry_audit_d0e2/e3_seams.py, which is a frozen "
            "audit document belonging to a third ticket, and mg-17aa's own "
            "reason for not editing it is a good one.  So the claim here is "
            "structural: `==` on a literal, moved by mg-17aa, two-sided",
            True,
            "and the shape is INHERITED from mg-5f9a rather than introduced "
            "by mg-17aa -- what mg-17aa did was keep it while writing a "
            "paragraph about why the same shape elsewhere was a defect")


def section_3():
    head("A3.3 -- P8 SCORED AS A MISS: THE TRANSCRIPT IS STALE AND mg-17aa "
         "IS NOT WHY")
    d0e2 = os.path.join(REPO, "code", "face_geometry_audit_d0e2")
    committed = open(os.path.join(d0e2, "out_e3_seams.txt")).read()
    p = subprocess.run([sys.executable, "e3_seams.py"], cwd=d0e2,
                       capture_output=True, text=True)
    live = p.stdout + p.stderr
    S.claim("code/face_geometry_audit_d0e2/out_e3_seams.txt DISAGREES with "
            "what e3_seams.py prints today", committed.strip() != live.strip(),
            "committed %d bytes, live %d bytes"
            % (len(committed), len(live)))
    last = subprocess.run(
        ["git", "log", "-1", "--format=%h %s",
         "--", "code/face_geometry_audit_d0e2/out_e3_seams.txt"],
        cwd=REPO, capture_output=True, text=True).stdout.strip()
    sha = last.split(" ")[0] if last else ""
    since = subprocess.run(
        ["git", "log", "--oneline", "%s..HEAD" % sha, "--",
         "code/face_geometry/controls_output.txt"],
        cwd=REPO, capture_output=True, text=True).stdout.strip()
    n_since = len([l for l in since.split("\n") if l.strip()])
    S.claim("and it was ALREADY stale before mg-17aa: it was last written at "
            "%s, and the artifact it records has moved %d times since -- "
            "mg-17aa is one of those %d and not the first"
            % (sha, n_since, n_since), n_since > 1,
            last[:110])
    d4 = open(os.path.join(REPO, "code", "face_geometry_instr_5f9a",
                           "d4_auditor_rerun.py")).read()
    S.claim("mg-17aa also did not HIDE it: the subject line names the change, "
            "d4's literal is moved to match, and the file states the policy "
            "in terms -- 'e3 is NOT edited: a document written to record a "
            "tree is corrected by saying which tree it recorded'",
            "e3 is NOT edited" in d4,
            "MY PREDICTION P8 GUESSED AT AN EDIT THAT WAS NEVER MADE OR A "
            "CONCEALMENT THAT DID NOT HAPPEN.  It is scored a MISS.  The "
            "underlying staleness is real and belongs to mg-d0e2's directory, "
            "not to this ticket")


def section_4():
    head("A3.4 -- P9: THE PRINTED `on shape` COUNT")
    art = open(os.path.join(FG, "controls_output.txt")).read()
    S.claim("the [CANNOT FAIL] row prints a per-gate split ending `%d on "
            "shape` and the shipped value is 0",
            "0 on shape)" in art or ", 0 on shape" in art,
            "the literal `0 on shape` appears %d times in the artifact"
            % art.count("0 on shape"))
    S.claim("and it is FORCED to 0 by the same argument the file already uses "
            "two screens away, where it classes `shape_ok == app` as FORCED BY "
            "CONSTRUCTION -- no `incidence_mode` changes the facet count, so "
            "no shipped pair can violate the shape gate.  The count is not "
            "named as forced where it is printed",
            "shape_ok == app [FORCED BY CONSTRUCTION]" in art
            and "`shape_ok == app` is forced by construction at every n" in art,
            "this is the SMALLEST finding in the suite and is listed as such: "
            "the row does say FORCED of the whole clause it belongs to, so a "
            "careful reader is not misled -- only an incurious one")


def main():
    print(BAR)
    print("mg-79ba A3 -- THE FOREIGN RE-AIMS, AND WHAT THEY BLOCK")
    print(BAR)
    section_1()
    section_2()
    section_3()
    section_4()
    return S.report()


if __name__ == "__main__":
    sys.exit(main())
