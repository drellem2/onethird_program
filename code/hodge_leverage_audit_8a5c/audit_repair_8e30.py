#!/usr/bin/env python3
"""mg-8a5c -- INDEPENDENT AUDIT of `e16e41c` + `61de121` (mg-8e30), the repair
that landed mg-f922 findings B, C, E, F and G.

WHAT mg-8e30 REPAIRED.  `bbe83b5` (mg-e1d0) measured the `STATE.md` cell A5 is
about, wrote −875 into three documents in the present tense as the CURRENT gap,
and in the same commit added +1 630 characters to that cell.  The observation
was correct when made and false when committed.  mg-8e30 re-measured, wrote
+2 069 / +20 662 at all three sites, said at each that the figure is measured
AFTER its own edit, replaced the string-matching gate with one that FORMATS
what it measured, and put the general rule in `STATE.md` Appendix A.

WHAT THIS AUDIT DOES, AND WHY IT IS NOT A RE-READING.  The defect class is
"a number that was true when measured and false when committed", so the ONLY
audit that means anything is a re-measurement taken from the POST-commit tree.
Every figure below is measured here, from the tree, by code that shares nothing
with `verify_landing.py`: the two documents' rows are located by `re.findall`
over the whole file with the match count reported, not by a `startswith` scan
that raises on ambiguity, and every length is reported in BOTH Unicode
codepoints AND UTF-8 bytes because the documents say "characters" and the two
readings differ by 222.

PREDICTED EXIT CODE, WRITTEN BEFORE THE FIRST RUN: 1.  This instrument exits
non-zero whenever any FINDING is present.  The prediction was NOT that the
three figures would be stale -- T1 was expected to CONFIRM, and did.  It was
that a gate built in one pass would have a hole, because the repair's own
correction deliberately prints the figure chain `2 928 -> 6 069 -> −875 ->
+755 -> +2 069` beside the live figure, and the chain's tail IS the live
figure.  T3 is that prediction, tested on disk against the real gate.

T1  THE THREE FIGURES, RE-MEASURED FROM THE POST-COMMIT TREE.
T2  THE SEAM CHECK.  Two repairs (`bbe83b5`, `e16e41c`) edited the same three
    passages.  Three sweeps, every threshold and every population reported,
    including what WOULD have counted where nothing was found.
T3  THE FIGURE GATE, MUTATED ON DISK.  SEVEN mutations against the REAL gate
    -- not a re-implementation of it -- each with its verdict written first.
T4  SELF-REFERENTIAL ANCHORS.  The repair's chosen convention for saying which
    side of an edit a figure is on is the phrase "this commit".  Does it
    compose when one file accumulates several of them?
T5  DECLARED-NOT-HIDDEN.  The three dispositions `e16e41c` declares, checked.
T6  THE RE-BASELINE COMMIT, LINE BY LINE.  `61de121` is literally "regenerate
    the committed output", which is the specific way this defect class hides:
    a document left wrong and its evidence file bent to agree with it presents
    identically in a diff to a document corrected and its evidence file
    regenerated to follow.  Every changed line is taken individually and the
    discriminator applied is whether the figure is right NOW, measured here --
    not whether the two files agree, which is guaranteed and proves nothing.

REPRODUCTION CONTRACT, stated in terms of the FILES READ rather than a commit.
This transcript regenerates byte-identically for any tree in which STATE.md,
docs/OneThird-Hodge-Side-Leverage.md, docs/state-history/attempt-mg-a3d4.md,
docs/OneThird-Hodge-Side-Leverage-Mg3c24Repair-IndependentAudit.md and
code/hodge_leverage_landing_e1d0/ are unchanged.  It embeds NO sha of its own.

IT MUTATES THE TREE AND RESTORES IT.  T3 writes to the three documents, runs
`code/hodge_leverage_landing_e1d0/run_all.sh`, and `git checkout --`s every
file back.  It REFUSES TO RUN if any file it will restore is already dirty --
scoped to those files, which is `negative_control.py`'s own convention and the
invariant that actually matters: a `git checkout --` over an uncommitted edit to
one of them destroys it.  Restoration is CHECKED by sha256, not asserted.

Pure Python 3 + git.  No third-party packages.  Runtime ~4 s.
"""

import hashlib
import itertools
import difflib
import os
import re
import subprocess
import sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

STATE = "STATE.md"
DELIV = "docs/OneThird-Hodge-Side-Leverage.md"
HIST = "docs/state-history/attempt-mg-a3d4.md"
AUDIT = "docs/OneThird-Hodge-Side-Leverage-Mg3c24Repair-IndependentAudit.md"
LANDING_RUN = "code/hodge_leverage_landing_e1d0/run_all.sh"
LANDING_OUT = "code/hodge_leverage_landing_e1d0/out_verify.txt"

MUTABLE = [STATE, DELIV, HIST, LANDING_OUT]

RESULTS = []
FINDINGS = []


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True, check=True).stdout


def read(path):
    with open(os.path.join(REPO, path), encoding="utf-8") as fh:
        return fh.read()


def write(path, text):
    with open(os.path.join(REPO, path), "w", encoding="utf-8") as fh:
        fh.write(text)


def sha(path):
    return hashlib.sha256(read(path).encode("utf-8")).hexdigest()


def flat(s):
    return " ".join(s.split())


def record(ok, detail):
    RESULTS.append((detail, ok))
    mark = {True: "[CONFIRMED]", False: "[REFUTED  ]", None: "[MEASURED ]"}[ok]
    print(f"  {mark} {detail}")


def finding(tag, detail):
    FINDINGS.append((tag, detail))
    print(f"  [FINDING  ] {tag} -- {detail}")


def head(title):
    print()
    print(title)
    print("-" * len(title))


def doc_num(v, signed=False):
    s = f"{v:+,}" if signed else f"{v:,}"
    return s.replace(",", " ").replace("-", "−")


# --------------------------------------------------------------------------
def rows_by_regex(text, pattern, label):
    """Located by findall over the WHOLE file, and the match COUNT is printed.
    verify_landing.py scans line prefixes and raises unless there is exactly
    one; this route reports the population instead of asserting it."""
    hits = re.findall(pattern, text, re.M)
    print(f"    population: lines matching {label}: {len(hits)}")
    return hits


def t1():
    head("T1 -- THE THREE FIGURES, RE-MEASURED FROM THE POST-COMMIT TREE")
    print("""The defect mg-8e30 repaired was a PRE-EDIT number published as current, so
the repair's own numbers are exposed to exactly the same mechanism: writing a
cell's length into that cell changes it.  The only check that means anything is
a re-measurement taken AFTER the repair's own commit.  That is this.
""")
    st, dl, hs = read(STATE), read(DELIV), read(HIST)
    cell_l = rows_by_regex(st, r"^\| \*\*AMBER-POSITIVE.*$", "'^| **AMBER-POSITIVE'")
    d14_l = rows_by_regex(dl, r"^> \*\*AMBER-POSITIVE.*$", "'^> **AMBER-POSITIVE'")
    record(len(cell_l) == 1 and len(d14_l) == 1,
           "each row is located by exactly 1 line -- the population is 1, stated "
           "rather than assumed")
    cell, d14 = cell_l[0], d14_l[0]

    a, b, h = len(cell), len(d14), len(hs)
    ab, bb, hb = (len(x.encode("utf-8")) for x in (cell, d14, hs))
    print()
    print(f"    {'quantity':<40}{'codepoints':>14}{'UTF-8 bytes':>14}")
    print(f"    {'STATE.md A5 cell':<40}{a:>14,}{ab:>14,}")
    print(f"    {'relocated row history (whole file)':<40}{h:>14,}{hb:>14,}")
    print(f"    {'§14 frozen copy':<40}{b:>14,}{bb:>14,}")
    print(f"    {'gap, cell only':<40}{a - b:>+14,}{ab - bb:>+14,}")
    print(f"    {'gap, cell + relocated history':<40}{a + h - b:>+14,}{ab + hb - bb:>+14,}")
    print()
    record(a == 12692 and h == 18593 and b == 10623,
           f"the three published parts reproduce from the tree: cell {a:,}, "
           f"relocated history {h:,}, §14 copy {b:,}")
    record(a - b == 2069 and a + h - b == 20662,
           f"and so do the two published gaps: cell-only {a - b:+,}, "
           f"cell + history {a + h - b:+,} -- THE REPAIR'S FIGURES DID NOT GO "
           "STALE, which was this audit's primary target")
    record(a - b > 0,
           f"the withdrawn 'flipped sign' claim stays withdrawn: the cell-only "
           f"gap is POSITIVE ({a - b:+,}), the sign it had when A5 was opened")

    print()
    print("    the three disclosure sites, and what each carries:")
    where = {"STATE.md row": flat(cell), "§14 (whole deliverable)": flat(dl),
             "row history H8": flat(hs)}
    side = "measured AFTER this commit's own edit"
    for n, t in where.items():
        print(f"      {n:<26} gap {str(doc_num(a - b, True) in t):<6} "
              f"cell+hist {str(doc_num(a + h - b, True) in t):<6} "
              f"side-of-edit {side in t}")
    record(all(doc_num(a - b, True) in t for t in where.values())
           and all(doc_num(a + h - b, True) in t for t in where.values())
           and all(side in t for t in where.values()),
           "all 3 sites carry both live figures AND say which side of the edit "
           "they are on -- mg-f922 B and C are LANDED")

    print()
    print("    the unit the documents do NOT name: 'characters' means CODEPOINTS")
    print(f"    here ({a:,}), not bytes ({ab:,}) -- a {ab - a} difference.  The arc's own")
    print("    out_control.txt names both ('183253 bytes, 180093 characters'); the")
    print("    three disclosure sites name neither.")
    record(None,
           f"NOTE, not a finding: the three sites say '{a:,} characters' without "
           f"naming the unit; the byte reading is {ab:,} and the gap under it is "
           f"{ab - bb:+,} rather than {a - b:+,}")
    return a, b, h


# --------------------------------------------------------------------------
def t2():
    head("T2 -- THE SEAM CHECK (two repairs, one artifact)")
    print("""`bbe83b5` and `e16e41c` both edited the STATE.md cell, §14 and H8.  A seam
defect is a STALE COPY of a passage the earlier repair also touched, surviving
where the later one did not reach.  It compounds: the next edit builds on
whichever copy it reaches.  Two sweeps, both thresholds stated.
""")
    docs = [STATE, DELIV, HIST, AUDIT]
    fig = re.compile(r"−875|\+755|\+2 069|\+9 608|\+17 023|\+20 662|2 928|6 069"
                     r"|flipped sign|SIGN FLIPPED|13 551|16 692|10 623|12 692"
                     r"|18 593|11 378|16 268|9 748|10 483")

    # ---- sweep 1: quoted units
    units = []
    for d in docs:
        t = read(d)
        for line in t.split("\n"):
            if line.startswith("> ") and len(line) >= 120:
                units.append((d, "blockquote-line", flat(line)))
        ft = flat(t)
        for pat in (r'\*"(.+?)"\*', r"\*'(.+?)'\*"):
            for m in re.finditer(pat, ft):
                if len(m.group(1)) >= 60:
                    units.append((d, "marked-quote", m.group(1)))
    print("    SWEEP 1 -- POPULATION: quoted units in the 4 documents both repairs")
    print("    touched.  Floors: blockquote lines >= 120 chars, marked quotes >= 60.")
    for (d, k), n in sorted(Counter((d, k) for d, k, _ in units).items()):
        print(f"      {os.path.basename(d):<58} {k:<16} {n:>3}")
    npairs = len(units) * (len(units) - 1) // 2
    print(f"      TOTAL units {len(units)};  pairs compared {npairs}")
    print("      similarity: difflib.SequenceMatcher.ratio() on flattened text")
    print("      THRESHOLD: 0.80.  1.00 = exact duplicate, 0.80 <= r < 1.00 = near.")
    exact, near = [], []
    for (d1, k1, t1), (d2, k2, t2) in itertools.combinations(units, 2):
        if abs(len(t1) - len(t2)) > max(len(t1), len(t2)) * 0.5:
            continue
        r = difflib.SequenceMatcher(None, t1, t2).ratio()
        if r >= 1.0:
            exact.append((t1, t2))
        elif r >= 0.80:
            near.append((r, d1, t1, d2, t2))
    bad = [(r, d1, t1, d2, t2) for r, d1, t1, d2, t2 in near
           if sorted(set(fig.findall(t1))) != sorted(set(fig.findall(t2)))]
    badx = [(t1, t2) for t1, t2 in exact if fig.search(t1)]
    print(f"      exact duplicates: {len(exact)}, of which figure-bearing: {len(badx)}")
    print(f"      near duplicates : {len(near)}, of which FIGURES DIFFER: {len(bad)}")
    for r, d1, t1, d2, t2 in near:
        print(f"        [{r:.3f}] {os.path.basename(d1)} / {os.path.basename(d2)}: "
              f"{t1[:70]}...")

    # ---- sweep 2: figure-bearing sentences, no floor
    sents = []
    for d in docs:
        ft = flat(read(d))
        for s in re.split(r"(?<=\.)\s+(?=[A-Z*`⚠️])", ft):
            if fig.search(s):
                sents.append((d, s))
    print()
    print("    SWEEP 2 -- POPULATION: every FIGURE-BEARING sentence in the same 4")
    print("    documents, NO length floor, threshold LOWERED to 0.60.")
    for d, n in sorted(Counter(d for d, _ in sents).items()):
        print(f"      {os.path.basename(d):<58} {n:>3}")
    p2 = len(sents) * (len(sents) - 1) // 2
    print(f"      TOTAL sentences {len(sents)};  pairs compared {p2}")
    hits2 = [(difflib.SequenceMatcher(None, s1, s2).ratio(), s1, s2)
             for (_, s1), (_, s2) in itertools.combinations(sents, 2)]
    over = [x for x in hits2 if x[0] >= 0.60]
    print(f"      pairs at or above 0.60: {len(over)}")
    mean = sum(len(s) for _, s in sents) // max(1, len(sents))
    record(not bad and not badx and not over,
           f"NO seam defect at either threshold.  WHAT WOULD HAVE COUNTED, so the "
           f"null result is checkable: sweep 1, any two quoted units above the "
           f"floors at ratio >= 0.80 carrying DIFFERENT figures; sweep 2, any two "
           f"figure-bearing sentences (mean length {mean} chars) sharing 60% of "
           f"their characters -- a stale copy differing only in its figure (5-7 "
           f"chars) scores ~0.97 and would be reported")

    # ---- sweep 3: the one that DOES find something
    print()
    print("    SWEEP 3 -- the same seam question asked a different way, because a")
    print("    similarity sweep cannot see two copies of a figure inside ONE line.")
    print("    POPULATION: the 5 needles the T1 figure gate tests x the 3 texts it")
    print("    tests them in = 15 cells.  Multiplicity 1 = the gate is load-bearing;")
    print("    >= 2 = the gate passes on ANY ONE copy and cannot see the others.")
    st, dl, hs = read(STATE), read(DELIV), read(HIST)
    cell = re.findall(r"^\| \*\*AMBER-POSITIVE.*$", st, re.M)[0]
    d14 = re.findall(r"^> \*\*AMBER-POSITIVE.*$", dl, re.M)[0]
    a, b, h = len(cell), len(d14), len(hs)
    texts = {"STATE.md row": flat(cell), "§14 (whole file)": flat(dl),
             "H8": flat(hs)}
    needles = {f"gap {doc_num(a - b, True)}": doc_num(a - b, True),
               f"cell+hist {doc_num(a + h - b, True)}": doc_num(a + h - b, True),
               f"cell {doc_num(a)}": doc_num(a),
               f"hist {doc_num(h)}": doc_num(h),
               "side-of-edit phrase": "measured AFTER this commit's own edit"}
    print()
    print(f"      {'needle':<26}" + "".join(f"{k:>20}" for k in texts))
    dup = []
    for ln, n in needles.items():
        counts = [t.count(n) for t in texts.values()]
        print(f"      {ln:<26}" + "".join(f"{c:>20}" for c in counts))
        for (site, _), c in zip(texts.items(), counts):
            if c >= 2:
                dup.append((ln, site, c))
    print()
    record(None,
           f"15 cells; {len(dup)} carry the SAME needle more than once: "
           + "; ".join(f"{ln} x{c} in {site}" for ln, site, c in dup))
    return dup


# --------------------------------------------------------------------------
def t3(dup):
    head("T3 -- THE FIGURE GATE, MUTATED ON DISK AGAINST THE REAL GATE")
    print("""mg-8e30's gate FORMATS what it has just measured, which is the right shape and
is a real improvement on the string-match it replaced.  The question this target
asks is narrower: is the formatted needle looked for in a place where exactly ONE
copy of it lives?  A presence test over a text holding two copies of the same
figure passes on either one alone.

The mutations run the REAL runner, `code/hodge_leverage_landing_e1d0/run_all.sh`,
against a mutated tree, and read its EXIT CODE.  Nothing is re-implemented.
Every verdict is written here before the run.
""")
    # SCOPED TO THE FILES THIS INSTRUMENT WILL `git checkout --`, which is the
    # invariant that actually matters and is `negative_control.py`'s own
    # convention: a `checkout` over an uncommitted edit to one of THESE files
    # destroys it.  A dirty file this run never touches is not that hazard, and
    # blocking on it would make the instrument un-runnable in the commit that
    # introduces it.
    dirty = "\n".join(l for l in git("status", "--porcelain", "--", *MUTABLE)
                      .strip().split("\n") if l.strip())
    if dirty:
        print("  REFUSING TO RUN: a file this run will restore is already dirty.")
        print("  A restore that cannot be distinguished from your own edit is not")
        print("  a restore.  git status over the files this run mutates:")
        for l in dirty.split("\n"):
            print("    " + l)
        raise SystemExit(2)
    before = {p: sha(p) for p in MUTABLE}

    def run_gate():
        r = subprocess.run(["sh", os.path.join(REPO, LANDING_RUN)],
                           capture_output=True, text=True)
        return r.returncode

    def restore():
        git("checkout", "--", *MUTABLE)

    def nth(path, old, new, n):
        t = read(path)
        i = -1
        for _ in range(n + 1):
            i = t.find(old, i + 1)
        if i < 0:
            return False
        write(path, t[:i] + new + t[i + len(old):])
        return True

    st = read(STATE)
    cell = re.findall(r"^\| \*\*AMBER-POSITIVE.*$", st, re.M)[0]
    dl = read(DELIV)
    d14 = re.findall(r"^> \*\*AMBER-POSITIVE.*$", dl, re.M)[0]
    gap = doc_num(len(cell) - len(d14), signed=True)
    both = doc_num(len(cell) + len(read(HIST)) - len(d14), signed=True)

    def m_live_state():
        nth(STATE, gap, "+9 999", 0)

    def m_chain_state():
        nth(STATE, gap, "+9 999", 1)

    def m_both_state():
        nth(STATE, gap, "+9 999", 0)
        nth(STATE, gap, "+9 999", 0)

    def m_live_deliv():
        nth(DELIV, gap, "+9 999", 0)

    def m_live_hist():
        nth(HIST, gap, "+9 999", 0)

    def m_both_fig():
        nth(HIST, both, "+9 998", 0)

    def m_relocate():
        lines = read(DELIV).split("\n")
        i = [k for k, l in enumerate(lines)
             if l.startswith("⚠️ **THAT FIGURE WAS THIS PARAGRAPH'S OWN PARENT'S")][0]
        j = i
        while j < len(lines) and lines[j].strip():
            j += 1
        para = lines[i:j]
        del lines[i:j]
        write(DELIV, "\n".join(lines) + "\n\n## APPENDIX Z (mutation)\n\n"
              + "\n".join(para) + "\n")

    cases = [
        ("N1  STATE.md row: corrupt the LIVE gap figure only", 1, m_live_state),
        ("N2  STATE.md row: corrupt the CHAIN-TAIL copy only", 1, m_chain_state),
        ("N3  STATE.md row: corrupt BOTH copies", 1, m_both_state),
        ("N4  §14: corrupt the LIVE gap figure only", 1, m_live_deliv),
        ("N5  H8: corrupt the LIVE gap figure only", 1, m_live_hist),
        ("N6  H8: corrupt cell+history (1 copy per site)", 1, m_both_fig),
        ("N7  §14: move the whole disclosure OUT of §14", 1, m_relocate),
    ]
    print(f"    {'mutation':<54}{'predicted':<14}{'observed'}")
    holes = []
    for name, predicted, fn in cases:
        fn()
        got = 1 if run_gate() != 0 else 0
        restore()
        agree = got == predicted
        print(f"    {name:<54}{'exit ' + str(predicted):<14}"
              f"{'exit ' + str(got)}{'' if agree else '   <-- GATE DID NOT FIRE'}")
        if not agree:
            holes.append(name)
    print()
    after = {p: sha(p) for p in MUTABLE}
    record(before == after,
           f"restoration CHECKED, not asserted: all {len(MUTABLE)} mutated files "
           "are byte-identical to their pre-run sha256")

    if holes:
        finding("F-1", "THE FIGURE GATE PASSES WHEN THE FIGURE A READER READS IS "
                       "WRONG.  The gate is a substring-PRESENCE test, and the "
                       "corrected wording prints the live gap TWICE at each site "
                       "-- once as the live figure and once as the tail of the "
                       "chain `2 928 → 6 069 → −875 → +755 → +2 069`, which ends "
                       "at the current gap BY CONSTRUCTION.  So corrupting the "
                       "sentence a reader actually reads leaves the gate green at "
                       "all three sites: " + "; ".join(h.split("  ")[0] for h in holes)
                       + ".  Corrupting BOTH copies fires (N3), so the gate is "
                         "alive -- it just cannot tell the copies apart.  Self-"
                         "perpetuating: every future correction appends the new "
                         "gap to the chain and re-creates the pair.")
        finding("F-2", "AND THE REPAIR'S OWN NEGATIVE CONTROL CANNOT SEE IT.  "
                       "`verify_landing.py`'s M3 is `docs['H8'].replace(gap, '')` "
                       "-- `str.replace` with no count, so it removes EVERY copy "
                       "and the gate necessarily fires.  A single-copy corruption, "
                       "which is the realistic edit, is not in the battery.")
    else:
        record(True, "no hole: every single-copy corruption fires the gate")
    return holes


# --------------------------------------------------------------------------
def t4():
    head("T4 -- DOES 'THIS COMMIT' COMPOSE?")
    print("""mg-8e30's general rule requires a document to say WHICH SIDE OF THE EDIT its
figure is on, and the convention it chose is the phrase "this commit" / "this
repair".  That is right for one anchor in one file.  This target asks what
happens when a file accumulates several, written by different commits.
""")
    st = read(STATE)
    lines = st.split("\n")
    hits = []
    for i, l in enumerate(lines, 1):
        for m in re.finditer(r"th(?:is) (?:commit|repair)(?:'s)?(?: own)?"
                             r"(?: edit| leaves the file)?", l, re.I):
            hits.append((i, m.group(0)))
    ln = sorted(set(i for i, _ in hits))
    print(f"    population: all {len(lines)} lines of STATE.md")
    print(f"    first-person anchors ('this commit' / 'this repair'): {len(hits)}")
    print(f"    on {len(ln)} distinct lines: {', '.join(str(x) for x in ln)}")
    blames = {}
    for i in ln:
        out = git("blame", "-L", f"{i},{i}", "--porcelain", STATE).split("\n")[0]
        blames[i] = out.split()[0][:7]
    print()
    for i in ln:
        print(f"      L{i:<5} written by {blames[i]}")
    distinct = sorted(set(blames.values()))
    print()
    record(None,
           f"{len(hits)} anchors on {len(ln)} lines, written by "
           f"{len(distinct)} DIFFERENT commits ({', '.join(distinct)}) -- and "
           "nothing in the prose distinguishes them")

    # the concrete cost: a self-referential LINE NUMBER, measured post-commit
    # by the commit that wrote it, and stale now.
    want = "Does a REPAIR need a fresh audit? The narrowing test"
    now = [i for i, l in enumerate(lines, 1) if l.startswith("**" + want)]
    claimed = re.search(r"`STATE\.md:(\d+)` as this repair leaves the file", flat(st))
    if claimed and now:
        c, n = int(claimed.group(1)), now[0]
        origin = git("log", "--format=%h", "-S", "`STATE.md:%d`" % c, "--",
                     STATE).split()
        was = None
        if origin:
            src = git("show", f"{origin[-1]}:{STATE}").split("\n")
            wl = [k for k, l in enumerate(src, 1) if l.startswith("**" + want)]
            was = wl[0] if wl else None
        drift = git("log", "--format=%h", f"{origin[-1]}..HEAD", "--", STATE).split() \
            if origin else []
        print(f"    the concrete cost -- STATE.md's ONE self-referential line number:")
        print(f"      claim in the tree      : `STATE.md:{c}` as this repair leaves the file")
        print(f"      the heading is actually: line {n}")
        print(f"      correct when written   : line {was} at `{origin[-1] if origin else '?'}`")
        print(f"      commits to STATE.md since: {len(drift)}")
        if c != n:
            finding("F-3", f"`STATE.md:{c}` is `STATE.md:{n}` in the tree -- off by "
                           f"{n - c}, stale since the heading moved, across "
                           f"{len(drift)} later commits to this file, one of which "
                           "is mg-8e30 itself.  It is the SAME defect class the "
                           "repair's new rule names: a measurement of something "
                           "the file also modifies, published post-commit by its "
                           "author (`as this repair leaves the file` -- which was "
                           "correct) and then silently falsified by later edits. "
                           "The rule covers the moment of writing and says nothing "
                           "about the anchor rotting afterwards; the paragraph "
                           "itself already says *'Locate it by that heading and "
                           "not by the number'*, so the fix is to drop the number.")
        else:
            record(True, "the self-referential line number is still correct")


# --------------------------------------------------------------------------
def t5():
    head("T5 -- THE THREE DISPOSITIONS `e16e41c` DECLARES")
    print("""'DECLARED, NOT HIDDEN' is the cheapest sentence in a commit message to write
and the most expensive to check.  All three are checked here.
""")
    # (1) the f922 instrument still reports F-B and F-C, STATE.md dropped off
    src = read("code/hodge_leverage_audit_f922/audit_repair.py")
    record("flipped the cell-only figure to **−875**" in src
           and "flipped sign** (`+2 928 → −875`)" in src,
           "declaration 1: F-B's site list is built by STRING-MATCHING three "
           "literal strings -- confirmed by reading the instrument, not the "
           "commit message")
    st, dl, hs = flat(read(STATE)), flat(read(DELIV)), flat(read(HIST))
    still = {"STATE.md cell": "flipped the cell-only figure to **−875**" in st,
             "§14 paragraph": "flipped sign** (`+2 928 → −875`)" in dl,
             "row history H8": "−875" in hs}
    record(still["STATE.md cell"] is False and still["§14 paragraph"] is True
           and still["row history H8"] is True,
           "and the declared outcome holds: the STATE.md cell HAS dropped off "
           "that list; §14 and H8 still match because the struck wording "
           "survives inside the correction's marked quotation ("
           + ", ".join(f"{k} {'still matches' if v else 'DROPPED'}"
                       for k, v in still.items()) + ")")

    # (2) every finding of the f922 audit document carries a disposition
    ft = flat(read(AUDIT))
    ids = re.findall(r"\|\s*\*\*([A-H])\*\*\s*\|\s*\*{0,2}"
                     r"(?:MODERATE|MINOR[–\-—]MODERATE|MINOR|MAJOR)\*{0,2}\s*\|", ft)
    disp = re.findall(r"\|\s*\*\*([A-H][A-H, ]*)\*\*\s*\|\s*\*\*(LANDED|NOT landed)",
                      ft)
    cov = sorted({x for g, _ in disp for x in re.findall(r"[A-H]", g)})
    print(f"    population: rows of the audit's findings table -- {len(ids)} "
          f"findings, ids {ids}")
    print(f"    disposition rows: {len(disp)}; ids they cover: {cov}")
    record(sorted(ids) == cov and len(ids) == 8,
           f"declaration 2: all {len(ids)} findings of the mg-f922 audit "
           f"document carry an in-place disposition ({len(disp)} rows covering "
           f"{len(cov)} ids); UNCOVERED: "
           + (", ".join(sorted(set(ids) - set(cov))) or "none"))

    # (3) verify_relocation.py FAIL is pre-existing
    r = subprocess.run(["python3", os.path.join(REPO, "code/state_restructure_34bf/"
                                                      "verify_relocation.py")],
                       capture_output=True, text=True, cwd=REPO)
    tail = [l for l in r.stdout.strip().split("\n") if l.startswith("FAIL")
            or l.startswith("PASS")]
    record(r.returncode != 0 and tail and "2 problem" in tail[-1],
           f"declaration 3: verify_relocation.py exits {r.returncode} with "
           f"'{tail[-1] if tail else '?'}' -- and it is PRE-EXISTING: the same "
           "run in a throwaway worktree at `f4eaea6`, before any edit of this "
           "cluster, produces BYTE-IDENTICAL output (checked out of band; "
           "re-run it yourself with `git worktree add --detach <dir> f4eaea6`)")


# --------------------------------------------------------------------------
CONTROL_OUT = "code/state_landing_control_2da3/out_control.txt"
REBASELINE = "61de121"


def t6():
    head("T6 -- THE RE-BASELINE COMMIT, LINE BY LINE")
    print("""mg-8e30's second commit is literally 'regenerate the committed output'.  Two
things present identically in that diff:

  (1) a number in the document was CORRECTED and the output regenerated to
      follow -- legitimate;
  (2) a number was left WRONG and the output regenerated to stop disagreeing
      with it -- the defect.

Agreement between a document and an output regenerated from it is guaranteed and
proves nothing.  The discriminator is whether the figure is right NOW, measured
here.  Every changed line is taken individually.
""")
    diff = git("show", REBASELINE, "--", CONTROL_OUT)
    body = diff.split("@@", 1)[1] if "@@" in diff else ""
    adds = [l[1:] for l in body.split("\n")
            if l.startswith("+") and not l.startswith("+++")]
    dels = [l[1:] for l in body.split("\n")
            if l.startswith("-") and not l.startswith("---")]
    print(f"    population: lines of {CONTROL_OUT} changed by `{REBASELINE}`")
    print(f"      insertions {len(adds)}, deletions {len(dels)}")
    stat = git("show", "--stat", "--format=", REBASELINE).strip().split("\n")[-1]
    print(f"      git's own --stat for the commit: {stat.strip()}")
    msg = git("log", "-1", "--format=%B", REBASELINE)
    claims = sorted(set(re.findall(r"\b(thirteen|13|eleven|11)\b", msg, re.I)))
    print(f"      the commit message's own count words: {claims}")
    if len(adds) != 13:
        finding("F-4", f"the commit says '13 lines' in its subject and 'All "
                       f"thirteen changed lines' in its body; the diff changes "
                       f"{len(adds)}, and `git show --stat` in the same commit "
                       f"says {len(adds)} insertions / {len(dels)} deletions. "
                       "The population is 'lines of out_control.txt changed by "
                       "this commit' and under it the count is "
                       f"{len(adds)}, not 13.  Nothing downstream depends on "
                       "the number -- every line is accounted for below -- but "
                       "a total that disagrees with the same commit's own "
                       "--stat is the shape this arc keeps paying for.")
    else:
        record(True, f"the commit's '13 changed lines' matches the diff ({len(adds)})")

    print()
    print("    each changed line, re-derived HERE from the post-commit tree:")
    st = read(STATE)
    stb = st.encode("utf-8")
    edge = " \t\r\n"
    rows = [l for l in st.split("\n") if l.startswith("|")]
    delim = [l for l in rows if re.fullmatch(r"\|[\s\-:|]+\|?", l)]

    def cells_of(l):
        p = l.split("|")
        return p[1:-1] if len(p) > 2 else []

    allc = [c.strip(edge) for l in rows for c in cells_of(l)]
    datac = [c.strip(edge) for l in rows if l not in delim for c in cells_of(l)]
    biggest_all = max(len(c) for c in allc)
    biggest_data = max(len(c) for c in datac)
    sha16 = hashlib.sha256(stb).hexdigest()[:16]
    nl = st.count("\n")
    sp = len(st.split("\n"))

    derived = [
        ("STATE.md bytes 183253", len(stb) == 183253, f"len(utf-8) = {len(stb):,}"),
        ("STATE.md characters 180093", len(st) == 180093, f"len(str) = {len(st):,}"),
        ("STATE.md 384 lines (header)", nl == 384, f"count('\\n') = {nl}"),
        ("STATE.md 385 lines (guard)", sp == 385, f"len(split('\\n')) = {sp}"),
        ("62 table rows", len(rows) == 62, f"lines starting '|' = {len(rows)}"),
        ("largest stripped cell 11384", biggest_all == 11384 and biggest_data == 11384,
         f"max over all '|' lines = {biggest_all:,}; over data rows only = "
         f"{biggest_data:,} -- SAME under both rules"),
        ("largest cell is in the mg-a3d4 row",
         "mg-a3d4" in max(allc, key=len), "the widest cell names mg-a3d4"),
        ("7876 < 11384", 7876 < biggest_all, f"7876 < {biggest_all:,}"),
        ("STATE.md at-rest sha 6129b1bc8b7bf774", sha16 == "6129b1bc8b7bf774",
         f"sha256(STATE.md)[:16] = {sha16}"),
        ("NC1 gutted: 385 -> 185 lines", sp - 200 == 185,
         f"{sp} - 200 deleted = {sp - 200}"),
    ]
    for label, ok, how in derived:
        print(f"      [{'ok ' if ok else 'NO '}] {label:<40} {how}")
    record(all(ok for _, ok, _ in derived),
           f"{sum(1 for _, ok, _ in derived if ok)} of {len(derived)} "
           "independently re-derivable figures in the changed lines reproduce "
           "from the post-commit tree -- so each of those lines is case (1), a "
           "document corrected and the output regenerated to FOLLOW, not case "
           "(2)")

    print()
    print("    the changed lines NOT independently re-derivable here, named rather")
    print("    than counted as confirmed:")
    print("      - '210 cells': neither of two natural cell rules reproduces it")
    print(f"        (all '|' lines -> {len(allc)}; data rows only -> {len(datac)}).")
    print("        The control names it 'the population every whole-file tally")
    print("        below is over' but does not define the rule.  THE FIGURE THIS")
    print("        COMMIT ACTUALLY CHANGED (11 384) reproduces under BOTH rules,")
    print("        so no conclusion here rests on the 210.")
    print("      - '115 rendered blocks in 11 sections' and NC1's '42438 bytes':")
    print("        produced by the control's own parser and its own mutation.")
    print("        Checked indirectly instead: this commit's parent adds exactly")
    print("        ONE prose line to STATE.md outside the A5 cell, which is the")
    print("        Appendix A rule paragraph -- so 114 -> 115 is +1, as declared.")
    plus = [l for l in git("show", "e16e41c", "--", STATE).split("\n")
            if l.startswith("+") and not l.startswith("+++") and l.strip() != "+"]
    record(len(plus) == 2
           and any("MUST PUBLISH THE POST-COMMIT MEASUREMENT" in l for l in plus),
           f"e16e41c changes exactly {len(plus)} content lines of STATE.md -- the "
           "A5 cell and ONE new Appendix A paragraph -- so the rendered-block "
           "count moving by exactly +1 is consequential, as the re-baseline "
           "commit declares")
    record(None,
           "and the two line counts for one file in one transcript -- 384 in the "
           "header, 385 in the guard section -- are count('\\n') and "
           "len(split('\\n')); both are right, neither says which. NOTE, not a "
           "finding: pre-existing, not introduced by this commit.")


# --------------------------------------------------------------------------
def main():
    print("mg-8a5c -- INDEPENDENT AUDIT OF THE mg-8e30 REPAIR")
    print("=" * 78)
    print("""Every figure below is measured HERE, from the working tree, by code sharing
nothing with `verify_landing.py`.  The mg-8e30 repair's central claim is that
its numbers are the POST-commit ones; that claim is only checkable by
re-measuring after its commit, which is T1.  Nothing here re-opens mg-3c24's or
mg-e1d0's mathematics: 0 mathematical statements are touched.""")
    t1()
    dup = t2()
    holes = t3(dup)
    t4()
    t5()
    t6()

    head("BOTTOM LINE")
    conf = sum(1 for _, ok in RESULTS if ok is True)
    ref = sum(1 for _, ok in RESULTS if ok is False)
    meas = sum(1 for _, ok in RESULTS if ok is None)
    print(f"  checks recorded : {len(RESULTS)}")
    print(f"  confirmed       : {conf}")
    print(f"  measurements    : {meas}")
    print(f"  refuted         : {ref}")
    print(f"  findings        : {len(FINDINGS)}")
    print()
    for tag, d in FINDINGS:
        print(f"    FINDING  {tag}: {d[:140]}")
    print()
    print("  THE PRIMARY TARGET IS CONFIRMED: the repair's three figures are the")
    print("  POST-commit ones and reproduce exactly from the tree.  What is open is")
    print("  the GATE that is supposed to keep them that way, and one stale")
    print("  self-referential line number of the same defect class.")
    return 1 if (FINDINGS or ref) else 0


if __name__ == "__main__":
    sys.exit(main())
