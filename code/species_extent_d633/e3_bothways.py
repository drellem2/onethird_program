"""E3 -- EVERY EXTENT PROBED IN BOTH DIRECTIONS, PER CHECKER.

The brief that commissioned mg-7dd3 put it in one sentence: *"plant a mutation
in something the extent claims to cover and confirm the checker FIRES; mutate
something the extent does NOT claim and confirm it stays silent."*  An extent
that names a region the checker does not reach is the BROKEN finding, and only
a mutation inside the claimed region exposes it.  An extent narrower than
reality is a lesser fault and still a false statement, and only a mutation
outside it exposes that.

Every probe runs against a SANDBOX COPY of docs/ and the trees the checkers
read.  Nothing here can leave the repository changed, which matters more than
usual because these probes deliberately plant forbidden sentences into files
that the checkers read.

21 probes, 5 checkers, EXIT CODES PREDICTED IN PREDICTIONS.md BEFORE THE RUN.
The finding text is recorded separately from the exit code, because a checker
reporting a finding and exiting 0 is a thing that has happened three times in
this arc (mg-7dd3 C2).

    python3 code/species_extent_d633/e3_bothways.py
"""

import os
import re
import shutil
import sys
import tempfile

from kernd633 import hdr, REPO, sandbox, run_checker

bad = 0
DOC = "docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md"
REPAIR = "docs/OneThird-Species-Hopf-Monoids-Repair.md"
REMAINDER = "docs/OneThird-Species-Hopf-Monoids-Repair-Remainder.md"

X3 = ("That same concatenation IS mu_{S,T}, and T5 measured it against every "
      "Hopf monoid axiom with 0 failures on 4399 basis elements.")
X4 = "T3d: four candidate identifications, three of the four columns are the control."
X7 = ('Recall from Section 17.4 that `K̄(Π)` is the algebra of symmetric '
      'functions in noncommuting variables and `K(Π)` is the familiar Hopf '
      'algebra of symmetric functions')


# ---------------------------------------------------------------------------
# mutations.  Each takes the sandbox root and edits it in place.
# ---------------------------------------------------------------------------
def _read(root, rel):
    return open(os.path.join(root, rel), encoding="utf-8").read()


def _write(root, rel, text):
    with open(os.path.join(root, rel), "w", encoding="utf-8") as fh:
        fh.write(text)


def _append(root, rel, text):
    with open(os.path.join(root, rel), "a", encoding="utf-8") as fh:
        fh.write(text)


def unstrike_x7(root):
    t = _read(root, DOC)
    m = re.search(r"~~(\*\"Recall from Section 17\.4.*?)~~", t, re.S)
    _write(root, DOC, t[:m.start()] + m.group(1) + t[m.end():])


def break_repair_doc(root):
    t = _read(root, REPAIR)
    _write(root, REPAIR, t.replace("WHAT THIS REPAIR DID NOT DO",
                                   "WHAT THIS REPAIR LEFT ALONE"))


def plant(rel, text, header="\n\n"):
    def go(root):
        _append(root, rel, header + text + "\n")
    return go


def plant_near(rel, marker, text, header="\n"):
    """Plant `text` immediately after the line carrying `marker`.

    mg-4adb.  P11b is a probe OF THE EXONERATION RULE: it needs its plant to
    land within `kerna4ef.WINDOW` lines of a ticket id `NAMES_A_REPAIR`
    matches, and it said so in its own label -- "six lines from an unrelated
    `mg-73df`".  It got there by APPENDING TO THE END of a file that happened
    to end with a sentence naming mg-73df, which is a property of where that
    sentence sat and not of the rule.  mg-4adb moved the cross-section call to
    the end of that runner, the sentence moved up with everything else, and
    the plant stopped landing near the marker -- so the probe measured the
    extent while its label still said the rule, and reported a MISS.

    Keying the site on the MARKER instead of on the end of the file is the
    same correction mg-7522's S3 made for line numbers: a probe that names a
    property should locate itself by that property.  It raises if the marker
    is absent, because a plant that lands somewhere unintended is worse than
    a probe that stops.
    """
    def go(root):
        lines = _read(root, rel).splitlines(True)
        hits = [i for i, ln in enumerate(lines) if marker in ln]
        if not hits:
            raise RuntimeError("%r does not appear in %s" % (marker, rel))
        i = hits[0]
        lines.insert(i + 1, header + text + "\n")
        _write(root, rel, "".join(lines))
    return go


def plant_new_md(tree, text):
    def go(root):
        _write(root, "code/%s/planted_d633.md" % tree,
               "# planted\n\n" + text + "\n")
    return go


# --- s2_seam passage probes -------------------------------------------------
def _norm(s):
    s = re.sub(r"[*`~>|#]", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def _blocks(lines, pred):
    out, cur, start = [], [], None
    for i, ln in enumerate(lines):
        if pred(ln):
            if start is None:
                start = i + 1
            cur.append(ln)
        else:
            if cur:
                out.append((start, i, "\n".join(cur)))
            cur, start = [], None
    if cur:
        out.append((start, len(lines), "\n".join(cur)))
    return out


def _passages(text):
    lines = text.splitlines()
    quotes = _blocks(lines, lambda ln: ln.startswith(">"))
    prose = _blocks(lines, lambda ln: ln.strip() and not ln.startswith(">")
                    and not ln.startswith("#") and not ln.startswith("|"))
    return quotes, prose


def _insert_before_heading(text, block):
    """Put `block` in its own passage, before the last `## ` heading, so it
    cannot merge with the passage it was copied from."""
    m = list(re.finditer(r"(?m)^## ", text))[-1]
    return text[:m.start()] + block + "\n\n" + text[m.start():]


def dup_quote(shortest):
    def go(root):
        t = _read(root, DOC)
        quotes, _ = _passages(t)
        pool = [q for q in quotes
                if (len(_norm(q[2])) <= 300 if shortest
                    else len(_norm(q[2])) > 300)
                and len(_norm(q[2])) > 60]
        pick = min(pool, key=lambda q: len(_norm(q[2]))) if shortest \
            else max(pool, key=lambda q: len(_norm(q[2])))
        _write(root, DOC, _insert_before_heading(t, pick[2]))
    return go


def dup_m16_quote(root):
    """mg-7dd3's M16, anchored on CONTENT rather than on line numbers.

    M16 slices `_lines[471:473]` -- the 139-character block quote as it stood
    at `798afb7`.  Any edit above line 472 moves it, and mg-d633's own §0
    repair added ten lines above it, so M16 re-run unmodified now duplicates
    whatever has arrived at those two lines and measures nothing.  Same
    passage, located by a phrase in it, so this probe cannot drift.
    """
    t = _read(root, DOC)
    quotes, _ = _passages(t)
    pick = next(q for q in quotes if "and it is self dual, since" in q[2])
    _write(root, DOC, _insert_before_heading(t, pick[2]))


def dup_tiny_prose(root):
    t = _read(root, DOC)
    _, prose = _passages(t)
    pool = [p for p in prose if 0 < len(_norm(p[2])) <= 60
            and _norm(p[2]) != "---"]
    pick = min(pool, key=lambda p: -len(_norm(p[2])))
    _write(root, DOC, _insert_before_heading(t, pick[2]))


def dup_table_row(root):
    t = _read(root, DOC)
    rows = [ln for ln in t.splitlines()
            if ln.startswith("|") and len(_norm(ln)) > 60
            and not set(ln) <= set("|- ")]
    m = list(re.finditer(r"(?m)^## ", t))[-1]
    _write(root, DOC, t[:m.start()] + rows[0] + "\n\n" + t[m.start():])


# --- e2 probes --------------------------------------------------------------
B1 = ('Aguiar–Mahajan §17.5, quoting their own §17.4: '
      '*"`K̄(Π)` is the algebra of\nsymmetric functions in noncommuting '
      'variables and `K(Π)` is the familiar Hopf algebra of\nsymmetric '
      'functions."*')
CORRECTION = re.compile(r"(?s)Aguiar–Mahajan §17\.5, quoting their own "
                        r"§17\.4, records both values.*?"
                        r"rest of its own document\.\n")


def restore_b1(root):
    t = _read(root, DOC)
    _write(root, DOC, CORRECTION.sub(lambda _m: B1 + "\n", t, count=1))


def _longest_strike(text):
    return max((m.group(1) for m in re.finditer(r"~~(.+?)~~", text, re.S)),
               key=lambda s: len(s.split()))


def restate_in_other_doc(with_retraction):
    def go(root):
        t = _read(root, REPAIR)
        s = re.sub(r"\s+", " ", _longest_strike(t)).strip()
        lead = ("This sentence is struck above and is quoted here only as the "
                "retracted form: " if with_retraction
                else "A further note on the smallest witness. ")
        _write(root, REPAIR, t + "\n\n" + lead + s + "\n")
    return go


def restate_in_code(root):
    p = "code/species_7d75/t1_grading.py"
    t = _read(root, p)
    s = re.sub(r"\s+", " ", _longest_strike(_read(root, REPAIR))).strip()
    _write(root, p, t + '\n\nRESTATED = """%s"""\n' % s)


# ---------------------------------------------------------------------------
# the probe table.  (id, checker, rel path, direction, what, mutation,
#                    predicted exit)
# ---------------------------------------------------------------------------
CD = "code/species_repair_6f61/check_doc.py"
W3 = "code/species_remainder_f8fa/w3_scope.py"
S1 = "code/species_repair_a4ef/s1_extent.py"
S2 = "code/species_repair_a4ef/s2_seam.py"
E2 = "code/species_extent_d633/e2_crosssection.py"

PROBES = [
    ("P0a", "check_doc.py", CD, "-", "unmutated", None, 0),
    ("P1", "check_doc.py", CD, "IN", "un-strike X7 in the document",
     unstrike_x7, 1),
    ("P2", "check_doc.py", CD, "IN", "break C4's anchor in the repair document",
     break_repair_doc, 1),
    ("P3", "check_doc.py", CD, "OUT", "X7 live in the remainder document",
     plant(REMAINDER, X7), 0),
    ("P4", "check_doc.py", CD, "OUT", "X3 live in species_7d75/t6",
     plant("code/species_7d75/t6_fock_and_record.py", '"""%s"""' % X3), 0),

    ("P0b", "w3_scope.py", W3, "-", "unmutated", None, 0),
    ("P5", "w3_scope.py", W3, "IN", "X4 in species_7d75/run_all.sh",
     plant("code/species_7d75/run_all.sh", "# " + X4), 1),
    ("P6", "w3_scope.py", W3, "IN", "X4 in species_7d75/README.md",
     plant("code/species_7d75/README.md", X4), 1),
    ("P7", "w3_scope.py", W3, "OUT", "X4 in species_repair_6f61/README.md",
     plant("code/species_repair_6f61/README.md", X4), 0),
    ("P8", "w3_scope.py", W3, "OUT", "X3 in species_7d75/README.md -- "
     "a statement not on this list",
     plant("code/species_7d75/README.md", X3), 0),

    ("P0c", "s1_extent.py", S1, "-", "unmutated", None, 0),
    ("P9", "s1_extent.py", S1, "IN", "X3 in species_7d75/run_all.sh "
     "(mg-7dd3's M12, which exited 0)",
     plant("code/species_7d75/run_all.sh", "# " + X3), 1),
    ("P10", "s1_extent.py", S1, "IN", "X3 in a NEW .md in species_7d75",
     plant_new_md("species_7d75", X3), 1),
    # P11 as PREDICTED (see PREDICTIONS.md) planted X3 at the END of
    # code/species_repair_a4ef/run_all.sh and expected 1.  IT EXITED 0, and
    # the prediction is kept as written and scored in OUTCOMES.md.  The reason
    # is not the extent: the file IS read (E1 measures that, and P11b below
    # shows the same statement being read there).  Line 18 of that file says
    # "mg-73df's MAJOR", and kerna4ef exonerates any hit within six lines of a
    # ticket id -- so the probe was measuring the EXONERATION RULE while
    # claiming to measure the extent.  The two are split rather than the probe
    # retuned to pass: P11 moves to a run_all.sh whose ticket id is far from
    # the plant, and P11b keeps the original site as a probe of the rule.
    ("P11", "s1_extent.py", S1, "IN",
     "X3 in species_remainder_f8fa/run_all.sh",
     plant("code/species_remainder_f8fa/run_all.sh", "# " + X3), 1),
    # mg-4adb: the site is now located BY THE MARKER and no longer by the end
    # of the file -- see plant_near's docstring.  The probe is unchanged in
    # what it asks; only the way it finds the site it always meant is.
    ("P11b", "s1_extent.py", S1, "OUT",
     "X3 six lines from an unrelated `mg-73df` -- the rule, not the extent",
     plant_near("code/species_repair_a4ef/run_all.sh", "mg-73df",
                "# " + X3), 0),
    ("P12", "s1_extent.py", S1, "OUT", "X3 in species_audit_73df -- a tree "
     "the extent declares silent",
     plant("code/species_audit_73df/README.md", X3), 0),
    ("P13", "s1_extent.py", S1, "OUT", "X3 in a NAMED exclusion "
     "(species_repair_a4ef/OUTCOMES.md)",
     plant("code/species_repair_a4ef/OUTCOMES.md", X3), 0),

    ("P0d", "s2_seam.py", S2, "-", "unmutated", None, 0),
    ("P14", "s2_seam.py", S2, "IN", "a SHORT block quote duplicated exactly "
     "(mg-7dd3's M16, which exited 0)", dup_quote(True), 1),
    ("P14b", "s2_seam.py", S2, "IN", "mg-7dd3's M16 exactly -- the 139-char "
     "quote, located by content", dup_m16_quote, 1),
    ("P15", "s2_seam.py", S2, "IN", "a LONG block quote duplicated exactly",
     dup_quote(False), 1),
    ("P16", "s2_seam.py", S2, "OUT", "a prose passage of <= 60 chars "
     "duplicated", dup_tiny_prose, 0),
    ("P17", "s2_seam.py", S2, "OUT", "a table row duplicated", dup_table_row,
     0),

    ("P0e", "e2_crosssection.py", E2, "-", "unmutated", None, 0),
    ("P18", "e2_crosssection.py", E2, "IN", "§0's misquotation restored "
     "(B1 itself)", restore_b1, 1),
    ("P19", "e2_crosssection.py", E2, "IN", "a struck claim restated in "
     "ANOTHER docs/*.md", restate_in_other_doc(False), 1),
    ("P20", "e2_crosssection.py", E2, "OUT", "the same restatement, in a "
     "paragraph that retracts it", restate_in_other_doc(True), 0),
    ("P21", "e2_crosssection.py", E2, "OUT", "a struck claim restated in a "
     ".py in a code tree", restate_in_code, 0),
]

FIRE_TEXT = re.compile(r"STILL ASSERTED|\*\*\*|FAIL|STANDING UN-STRUCK"
                       r"|SAID TWICE|NEAR-DUPLICATE")


hdr("E3  EVERY EXTENT PROBED IN BOTH DIRECTIONS")
print("  Exit codes were predicted in PREDICTIONS.md before this ran.")
print("  `finding` records whether the OUTPUT says something fired, which is")
print("  a different claim from the exit code -- three scripts in this arc")
print("  reported a finding and exited 0.")
print()
print("  %-5s %-20s %-4s %-52s %-4s %-4s %-8s"
      % ("id", "checker", "dir", "mutation", "exp", "got", "finding"))

results = []
for pid, name, rel, direction, what, mut, expect in PROBES:
    tmp = tempfile.mkdtemp(prefix="d633_probe_")
    try:
        root = sandbox(os.path.join(tmp, "repo"))
        if mut is not None:
            mut(root)
        code, out = run_checker(root, rel)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    fired = bool(FIRE_TEXT.search(out))
    ok = (code == expect)
    bad += (not ok)
    results.append((pid, name, direction, what, expect, code, fired, ok))
    print("  %-5s %-20s %-4s %-52s %-4d %-4s %-8s %s"
          % (pid, name, direction, what[:52], expect, code,
             "yes" if fired else "no", "" if ok else "*** MISSED ***"))
print()

# per checker, both directions, as the brief requires
hdr("E3b  PER CHECKER, BOTH DIRECTIONS")
for name in ["check_doc.py", "w3_scope.py", "s1_extent.py", "s2_seam.py",
             "e2_crosssection.py"]:
    rs = [r for r in results if r[1] == name]
    ins = [r for r in rs if r[2] == "IN"]
    outs = [r for r in rs if r[2] == "OUT"]
    base = [r for r in rs if r[2] == "-"]
    print("  %-20s baseline %s | INSIDE the claimed extent %d/%d fired | "
          "OUTSIDE it %d/%d stayed silent"
          % (name, "clean" if base and base[0][5] == 0 else "*** DIRTY ***",
             sum(1 for r in ins if r[5] == 1), len(ins),
             sum(1 for r in outs if r[5] == 0), len(outs)))
print()
print("  A checker with a green INSIDE column and a green OUTSIDE column has")
print("  had its printed extent MEASURED, in both directions, rather than")
print("  read.  That is the sentence mg-7dd3 asked for and it is the whole")
print("  deliverable of this file.")
print()

print("=" * 78)
print("E3 TOTAL BAD: %d" % bad)
print("=" * 78)
print()
print("EXTENT OF THIS NUMBER.  %d probes over 5 checkers, each a SINGLE"
      % len(PROBES))
print("mutation against a fresh sandbox copy of docs/ and 6 code trees.  It")
print("says nothing about mutations nobody planted: an extent probed at two")
print("points is not an extent verified at every point, and the choice of")
print("points is mine.  Each probe tests ONE statement in ONE file -- no probe")
print("here plants two at once, and none tests a checker against a mutation")
print("of ITSELF.  The probes are listed above by name so a successor can see")
print("which regions were and were not touched.")
sys.exit(1 if bad else 0)
