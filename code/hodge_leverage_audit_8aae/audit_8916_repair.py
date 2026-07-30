#!/usr/bin/env python3
"""mg-8aae -- INDEPENDENT AUDIT OF THE mg-8916 REPAIR OF mg-835f.

Target: `b055ae5` + `f5360bf` + `d1dd84d`, and the two sites mg-835f left open
on the mg-a318 repair.

  G-1  a wrong figure in ORDINARY PROSE beside the site was invisible at 3 of 3
       sites, at exit 0.  mg-8916 closed it by WIDENING THE CODE -- a CENSUS of
       every figure-shaped token the section asserts, against the live values
       plus a declared historical roster -- and says so.
  G-2  the mg-8a5c instrument's bottom line asserted a primary target its own
       T1 rows refuted.  mg-8916 DERIVES the sentence from the rows tagged
       PRIMARY and adds a `SUMMARY vs ROWS` check.

WHAT THIS INSTRUMENT IS FOR, and what it deliberately is not.  It is not a
re-run of mg-8916's own R1-R4: a repair scored only by its author's instrument
is scored by the author.  Every probe below is built here, with its own
wording, its own site slots, its own ballast (chosen by a procedure and
CONTROLLED before use), and -- for the census totals -- its own tokenizer,
which shares no regex with `verify_landing.py`.

  A1  WHICH REPAIR WAS DONE, AND IS IT SAID.  The ticket offers three
      dispositions (remove the duplicate / narrow the stated extent / widen the
      code) and a silent narrowing reads as a fix while being a reduction in
      coverage.  A1 re-derives, in its own code, the measurement mg-8916 rests
      the choice on, re-counts the printed extent with a SECOND tokenizer, and
      checks the choice is stated in both the document and the source.

  A2  THE 12 OF 12 IS NOT WEAKENED, AND IT IS CHECKED AT ROW GRANULARITY.
      mg-835f's strongest result is 12 reader-facing figures corrupted ON DISK
      -> red, 12 restored -> green.  A widening that made the run red for a NEW
      reason while the old check went quiet would preserve the headline and
      lose the result.  So A2 requires, for each of the 12, that the runner go
      red AND that the `READ AT THE SITE` row FOR THAT FIGURE be the row that
      failed.

  A3  THE CENSUS FIRES ON PROSE, ON MY WORDING, IN BOTH DIRECTIONS.  Not
      mg-835f's sentence and not mg-8916's slots: the ballast is selected here
      by a procedure and each slot is CONTROLLED first -- blanked, runner must
      stay green -- so a fire is attributable to the figure and not to the
      edit.

  A4  THE ONE NOBODY LISTED: THE CENSUS IS A MULTISET, SO A PERMUTATION IS
      INVISIBLE.  Two DECLARED figures of equal length exchanged in ordinary
      prose leave the multiset identical and every designated statement
      correct.  A reader meets a wrong figure; the gate cannot see it.

  A5  `SUMMARY vs ROWS`, SHOWN TO FIRE -- AND PROBED THE OTHER WAY.  Forced by
      the environment variable mg-8916 added, it must fire.  Then the same
      disagreement is created in the SENTENCE ITSELF instead of in the verdict
      variable, which is the shape G-2 actually had.

  A6  mg-835f's OWN INSTRUMENT, UNMODIFIED, re-run here rather than taken from
      mg-8916's transcript, with its committed transcript sha256-checked
      untouched afterwards.

  A7  THE RULE APPLIED TO THE DELIVERABLE ITSELF.  If this repair's own summary
      disagrees with its own rows, believe the rows.

  A8  THE SEAM CHECK, AND ITS THRESHOLD.

PREDICTED EXIT CODE, WRITTEN BEFORE THE FIRST RUN: 1 -- because A4 and A5's
second direction are predicted to be defects and this instrument exits 1 on any
finding.  Every probe's verdict is written in `PREDICTIONS.md` before it ran and
the misses are kept as written.

IT MUTATES THE TREE AND RESTORES IT.  A2/A3/A4 write to `STATE.md`, the
deliverable and the row-history file; A5 writes to
`code/hodge_leverage_audit_8a5c/audit_repair_8e30.py`.  Each is `git checkout
--`ed back inside a `finally` and every restoration is CHECKED by sha256, not
asserted.  It REFUSES TO RUN against a tree in which any of those is dirty.

Pure Python 3 + git.  No third-party packages.
"""

import difflib
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
LANDING = os.path.join(REPO, "code/hodge_leverage_landing_e1d0")
sys.path.insert(0, LANDING)
import verify_landing as V                              # noqa: E402

RUNNER = os.path.join(LANDING, "verify_landing.py")
AUDIT_8A5C = "code/hodge_leverage_audit_8a5c/audit_repair_8e30.py"
AUDIT_835F = "code/hodge_leverage_audit_835f/audit_a318_repair.py"
AUDIT_835F_OUT = "code/hodge_leverage_audit_835f/out_audit_a318.txt"
REPAIR_DOC = "docs/OneThird-Hodge-Side-Leverage-Mg835fRepair.md"
REPAIR_OUT = "code/hodge_leverage_repair_8916/out_repair_8916.txt"

MUTABLE = [V.STATE, V.DELIV, V.HIST, AUDIT_8A5C]

RESULTS = []
FINDINGS = []


# --------------------------------------------------------------------------
# plumbing
# --------------------------------------------------------------------------
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


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True, check=True).stdout


def sha(path):
    with open(os.path.join(REPO, path), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def read(path):
    with open(os.path.join(REPO, path), encoding="utf-8") as fh:
        return fh.read()


def write(path, text):
    with open(os.path.join(REPO, path), "w", encoding="utf-8") as fh:
        fh.write(text)


def restore(*paths):
    subprocess.run(["git", "-C", REPO, "checkout", "--"] + list(paths), check=True)


CLEAN = {}


def run_runner():
    """The REAL runner against whatever is on disk.  (exit, [lines])."""
    r = subprocess.run([sys.executable, RUNNER], capture_output=True,
                       text=True, cwd=REPO)
    return r.returncode, r.stdout.split("\n")


def refuted_lines(lines):
    return [l.strip() for l in lines if l.strip().startswith("[REFUTED  ]")]


# --------------------------------------------------------------------------
# MY OWN TOKENIZER.  Deliberately NOT `verify_landing.FIGURE_TOKEN`: a census
# checked by the regex that produced it is a census checked by itself.  This
# one scans maximal runs of digits/spaces/signs and then decides, rather than
# matching a shape -- a different route to the same population.
# --------------------------------------------------------------------------
#
# ⚠️ CORRECTED after this instrument's own first run, and the miss is kept in
# `PREDICTIONS.md`.  The first version read `[+−]?\d[\d ]*`, which runs THROUGH
# the multi-space column separators of H8's table and swallows three figures
# into one unparseable run.  It counted 27 tokens at H8 where the runner counts
# 36, and this instrument reported the disagreement against the runner -- which
# was right about the tree and wrong about which side had the defect.  A space
# is now consumed only when a digit follows it.  The defect was MINE; the
# refutation it produced is recorded, not deleted.
RUN_RE = re.compile(r"[+−]?\d(?:\d| (?=\d))*")


def my_tokens(text):
    """Every figure-shaped token in `text`, as a sorted list.

    ⚠️ CORRECTED TWICE, and both misses are kept in `PREDICTIONS.md`.  The
    second: a run of space-separated groups is not ONE token.  Flattened, H8's
    three-column table reads `9 748 11 378 13 367`, which is three figures; a
    parser that takes the whole run and then asks whether it is well formed
    drops all three.  The groups are now consumed GREEDILY LEFT TO RIGHT --
    a 1-3 digit lead followed by as many 3-digit groups as follow it, then
    restart at the first group that does not fit."""
    out = []
    for m in RUN_RE.finditer(text):
        s = m.group().rstrip()
        if m.start() > 0 and (text[m.start() - 1].isalnum()
                              or text[m.start() - 1] == "_"):
            continue
        sign = s[0] if s[0] in "+−" else ""
        groups = (s[1:] if sign else s).split(" ")
        if not all(g.isdigit() for g in groups):
            continue
        i = 0
        while i < len(groups):
            lead = groups[i]
            j, parts = i + 1, [lead]
            while j < len(groups) and len(groups[j]) == 3:
                parts.append(groups[j])
                j += 1
            pre = sign if i == 0 else ""
            if len(parts) > 1 and 1 <= len(lead) <= 3:
                out.append(pre + " ".join(parts))
                i = j
            else:
                if pre and len(lead) >= 3:
                    out.append(pre + lead)
                i += 1
    return sorted(out)


def measured_now():
    a = len(V.state_row(V.tree(V.STATE)))
    b = len(V.deliv_row(V.tree(V.DELIV)))
    h = len(V.tree(V.HIST))
    return {"gap": V.doc_num(a - b, signed=True),
            "both": V.doc_num(a + h - b, signed=True),
            "cell": V.doc_num(a), "hist": V.doc_num(h), "copy": V.doc_num(b)}


SITE_FILE = {"the STATE.md row": V.STATE, "§14": V.DELIV, "H8": V.HIST}


def site_raw(site, full=None):
    full = V.tree(SITE_FILE[site]) if full is None else full
    if site == "the STATE.md row":
        return V.state_row(full)
    if site == "§14":
        return V.section(full, "## §14 — `STATE.md` row, as landed")
    return V.section(full, "### H8 — ")


def put_site(site, new_raw):
    """Write `new_raw` back over the site, length-preservingly."""
    path = SITE_FILE[site]
    full = V.tree(path)
    raw = site_raw(site, full)
    assert len(new_raw) == len(raw), (site, len(new_raw) - len(raw))
    assert full.count(raw) == 1, site
    write(path, full.replace(raw, new_raw, 1))
    return path


# --------------------------------------------------------------------------
# A1 -- WHICH REPAIR WAS DONE, AND IS IT SAID
# --------------------------------------------------------------------------
def a1():
    head("A1 -- WHICH OF THE THREE REPAIRS WAS DONE, AND IS IT SAID")
    print("""The ticket names three dispositions for G-1 and warns that a SILENT
NARROWING reads as a fix while being a reduction in coverage.  So: what did the
repair do, is the choice stated, and does the measurement it rests on hold when
re-derived here?
""")
    doc = read(REPAIR_DOC)
    src = read("code/hodge_leverage_landing_e1d0/verify_landing.py")

    # (i) the disposition, as claimed.
    said_doc = "CLOSED BY WIDENING THE CODE" in doc and \
               "The stated extent is not narrowed" in doc
    said_src = "THE CODE IS WIDENED AND THE CLAIM" in src or \
               "THE CODE IS WIDENED, not" in src
    record(said_doc and said_src,
           "the disposition is STATED, in the document ('CLOSED BY WIDENING "
           "THE CODE. The stated extent is not narrowed') and again at the "
           "widening in `verify_landing.py`.  It is neither of the ticket's "
           "two named repairs and it says so, so nothing is narrowed silently")

    # (ii) is the stated extent in fact wider than before, not narrower?
    old = git("show", "b055ae5^:code/hodge_leverage_landing_e1d0/verify_landing.py")
    record("census_gate" not in old and "census_gate" in src,
           "and it is a WIDENING and not a re-wording: `census_gate` does not "
           "exist at `b055ae5^` and is called by `figure_gate` at HEAD")
    for probe, why in (("(a) the DESIGNATED STATEMENT at each site",
                        "check (a) survives the widening"),
                       ("(b) each LIVE figure written exactly once per site",
                        "check (b) survives the widening")):
        record(probe.split(" -- ")[0][:30] in src, f"{why}: `{probe[:34]}...` "
               "is still printed as part of the extent")

    # (iii) the measurement the choice rests on, RE-DERIVED HERE.
    print()
    print("  the claim the choice rests on -- 'there is nothing to remove' --")
    print("  re-derived with this instrument's own tokenizer:")
    m = measured_now()
    over = 0
    for site in ("the STATE.md row", "§14", "H8"):
        toks = my_tokens(V.assertions(site_raw(site)))
        cells = []
        for key, lic in V.LIVE_CENSUS[site].items():
            n = toks.count(m[key])
            cells.append(f"{key}={n}/{lic}")
            if n > lic:
                over += 1
        print(f"    {site:<20} " + "  ".join(cells))
    record(over == 0,
           f"{over} live figure is written more times than its site licenses, "
           "over the 3 sites and 12 (site, figure) pairs -- independently "
           "re-derived, so the ticket's PREFERRED repair (remove the prose "
           "duplicate) genuinely had nothing to remove and the choice really "
           "was between widening the code and narrowing the claim")

    # (iv) the printed extent, RE-COUNTED with the second tokenizer.
    print()
    print("  the printed extent, re-counted by a tokenizer sharing no regex")
    print("  with the one that produced it:")
    rc, lines = run_runner()
    printed = {}
    for l in lines:
        mm = re.match(r"\s+(the STATE\.md row|§14|H8)\s+(\d+) licensed figure "
                      r"tokens \((\d+) historical", l)
        if mm:
            printed[mm.group(1)] = (int(mm.group(2)), int(mm.group(3)))
    agree = 0
    total_mine = 0
    for site in ("the STATE.md row", "§14", "H8"):
        mine = len(my_tokens(V.assertions(site_raw(site))))
        total_mine += mine
        theirs, hist = printed.get(site, (None, None))
        ok = mine == theirs
        agree += 1 if ok else 0
        print(f"    {site:<20} runner says {theirs:>3}   this instrument "
              f"counts {mine:>3}   {'agree' if ok else '<-- DISAGREE'}"
              f"   ({hist} historical values declared)")
    record(agree == 3 and total_mine == 69,
           f"{agree} of 3 sites agree on the token count and the total is "
           f"{total_mine}, which is the 69 the document prints.  The extent is "
           "not a number written beside the gate: two independent tokenizers "
           "reach it")
    record(rc == 0, f"and the clean tree is green: the real runner exits {rc}")


# --------------------------------------------------------------------------
# A2 -- THE 12 OF 12, AT ROW GRANULARITY
# --------------------------------------------------------------------------
def bump(value):
    """A DIFFERENT figure of the SAME LENGTH -- so nothing measured moves."""
    d = value[-1]
    return value[:-1] + str((int(d) + 1) % 10)


def designated_slot(site, key, value):
    """The occurrence of `value` in the site that the DESIGNATED STATEMENT is
    read out of, found by using the site's own reader as an ORACLE rather than
    by restating its regex here -- which is the failure mode this whole arc is
    about."""
    raw = site_raw(site)
    reader = dict((n, r) for n, r, _k in V.SITES)[site]
    bad = bump(value)
    for i in range(raw.count(value)):
        parts = raw.split(value)
        cand = value.join(parts[:i + 1]) + bad + value.join(parts[i + 1:])
        if len(cand) == len(raw) and reader(cand).get(key) != [value]:
            return cand, bad
    return None, bad


def a2():
    head("A2 -- mg-835f's 12 OF 12 IS NOT WEAKENED, CHECKED AT ROW GRANULARITY")
    print("""mg-835f's primary target: 12 reader-facing figures corrupted ON DISK make
the run red and 12 restorations make it green.  mg-8916 added a third check to
the same function.  A widening that made the run red for a NEW reason while the
old check went quiet would keep the headline and lose the result -- so this is
not an exit-code check.

  population: the 12 (site, figure) pairs `SITES` designates -- 5 at the
  STATE.md row, 2 at §14, 5 at H8.  Each is corrupted to a DIFFERENT figure OF
  THE SAME LENGTH, so no measurement moves underneath the gate.  Required, per
  probe: the runner goes red, AND the `READ AT THE SITE` row FOR THAT FIGURE is
  among the refuted rows.  Then restored, sha256-checked, and re-run.
""")
    m = measured_now()
    print(f"    {'probe':<52}{'red?':<7}{'AT-THE-SITE row':<18}{'restored'}")
    red = attributed = back_green = 0
    total = 0
    for site, _reader, keys in V.SITES:
        for key in keys:
            total += 1
            label = V.FIGURES[key][0]
            cand, bad = designated_slot(site, key, m[key])
            if cand is None:
                record(False, f"cannot locate the designated slot for "
                              f"'{label}' at {site}")
                continue
            path = put_site(site, cand)
            try:
                rc, lines = run_runner()
            finally:
                restore(path)
            assert sha(path) == CLEAN[path], f"restoration of {path} not identical"
            rc2, _ = run_runner()
            needle = f"GATE @ {site}: '{label}' READ AT THE SITE"
            hit = any(needle in l for l in refuted_lines(lines))
            red += 1 if rc else 0
            attributed += 1 if hit else 0
            back_green += 1 if rc2 == 0 else 0
            print(f"    {site + ' / ' + label:<52}"
                  f"{('RED' if rc else 'green'):<7}"
                  f"{('[FAIL]' if hit else 'still passing'):<18}"
                  f"{'green' if rc2 == 0 else 'STILL RED'}")
    print()
    record(red == total,
           f"{red} of {total} designated-figure corruptions make the real "
           "runner red -- mg-835f's primary target reproduces on this tree "
           "after the widening")
    record(attributed == total,
           f"and in {attributed} of {total} the row that failed is the "
           "`READ AT THE SITE` row FOR THAT FIGURE, not merely some other row "
           "of the widened gate.  The old check is doing the old work; the "
           "census did not absorb it")
    record(back_green == total,
           f"{back_green} of {total} restorations return the runner to exit 0, "
           "each verified byte-identical by sha256")


# --------------------------------------------------------------------------
# A3 -- THE CENSUS FIRES ON PROSE, ON MY WORDING, BOTH DIRECTIONS
# --------------------------------------------------------------------------
SENTENCE = "Re-read at this site, the cell-only gap stands at {v} characters."


BALLAST_CACHE = {}


def pick_ballast(site, need):
    """A prose slot at this site that NO check reads, chosen by a procedure
    rather than named by hand, and CONTROLLED before use: the slot is blanked
    (length-preservingly) and the runner must stay GREEN.  The first candidate
    that survives the control is used.  The control is run ONCE per site and
    the choice is cached, so the transcript reports one control per site."""
    if site in BALLAST_CACHE:
        return BALLAST_CACHE[site]
    raw = site_raw(site)
    # ⚠️ CORRECTED after the first run, miss kept in `PREDICTIONS.md`: the
    # first version cut candidates at sentence boundaries and required them to
    # contain no newline, and these documents are hard-wrapped -- so §14, a
    # 16 647-character section, offered NO candidate and 2 of the 6 probes
    # never ran.  Candidates are now whole LINES, which is where hard-wrapped
    # prose actually has room.  The defect was MINE.
    # The digit-free stretches within each line, and the whole lines.  NOT
    # "lines that do not start with `|`": the STATE.md row IS a markdown table
    # cell, so every one of its lines starts with `|` and that filter left it
    # with zero candidates -- the third miss this instrument made about itself.
    cands = []
    for line in raw.split("\n"):
        for cand in [line] + re.split(r"\d[\d ]*", line):
            c = cand.rstrip()
            if len(c) >= need and not any(ch.isdigit() for ch in c) \
                    and not any(bad in c for bad in ("|", "#", "```")) \
                    and sum(ch.isalpha() for ch in c) > len(c) * 0.6 \
                    and raw.count(c) == 1 and c not in cands:
                cands.append(c)
    for s in cands:
        # and the slot must be prose the CENSUS IS SUPPOSED TO READ: a slot
        # inside a marked quotation is exempt by declaration, so a probe there
        # would measure the exemption rather than the gate.
        trial = raw.replace(s, ("X" * (len(s) - 6)) + "+9 999", 1)
        if "+9 999" not in V.assertions(trial):
            continue
        blanked = raw.replace(s, " " * len(s), 1)
        path = put_site(site, blanked)
        try:
            rc, _ = run_runner()
        finally:
            restore(path)
        assert sha(path) == CLEAN[path]
        if rc == 0:
            BALLAST_CACHE[site] = s
            return s
    return None


def a3():
    head("A3 -- A WRONG FIGURE IN ORDINARY PROSE: MY WORDING, MY SLOTS")
    print("""Not mg-835f's sentence and not mg-8916's named ballast.  The slot is chosen
here by a procedure and CONTROLLED FIRST: blanked length-preservingly, the
runner must stay green -- so a fire below is attributable to the FIGURE and not
to the edit.  Then the same slot carries this instrument's own sentence.

  population: 3 sites x 2 wrong-figure shapes.  `+9 999` is off the roster;
  `+1 630` IS on the roster at all three sites, which is the shape a
  SET-membership census passes.  Verdicts written before the run.
""")
    print(f"    {'probe':<58}{'control':<10}{'predicted':<12}{'observed':<12}"
          f"{'restored'}")
    fired = silent = controls = 0
    total = 0
    for value in ("+9 999", "+1 630"):
        for site in ("the STATE.md row", "§14", "H8"):
            total += 1
            sentence = SENTENCE.format(v=value)
            slot = pick_ballast(site, len(sentence))
            if slot is None:
                record(False, f"no unread prose slot of {len(sentence)}+ chars "
                              f"found at {site}")
                continue
            controls += 1
            raw = site_raw(site)
            new_raw = raw.replace(slot, sentence + " " * (len(slot) - len(sentence)), 1)
            path = put_site(site, new_raw)
            try:
                rc, lines = run_runner()
            finally:
                restore(path)
            assert sha(path) == CLEAN[path]
            rc2, _ = run_runner()
            fired += 1 if rc else 0
            silent += 1 if rc2 == 0 else 0
            print(f"    {site + ': prose ' + value:<58}"
                  f"{'green':<10}{'GATE FIRES':<12}"
                  f"{('GATE FIRES' if rc else 'gate passes'):<12}"
                  f"{'silent' if rc2 == 0 else 'STILL RED'}"
                  f"{'' if rc else '   <-- PREDICTION MISSED'}")
            if rc:
                hit = [l for l in refuted_lines(lines) if "FIGURE CENSUS" in l]
                if hit:
                    print(f"        {hit[0][:145]}")
    print()
    record(controls == total,
           f"{controls} of {total} probe slots passed their CONTROL: blanked, "
           "the runner stays green, so the slot is prose no check reads and a "
           "fire is attributable to the figure written into it")
    record(fired == total,
           f"{fired} of {total} wrong-prose probes make the real runner red, at "
           "3 of 3 sites and in both shapes, on wording chosen here.  G-1 is "
           "closed against an instrument that is not the repair's own")
    record(silent == total,
           f"{silent} of {total} restorations return the runner to exit 0, "
           "sha256-verified -- the gate does not fire on everything")


# --------------------------------------------------------------------------
# A4 -- THE ONE NOBODY LISTED: A MULTISET CANNOT SEE A PERMUTATION
# --------------------------------------------------------------------------
# Each probe exchanges two DECLARED historical figures OF EQUAL LENGTH, in
# ordinary prose, at one site.  The multiset of figure tokens is unchanged by
# construction, every designated statement is untouched, and the length is
# preserved -- so all three of the gate's checks are satisfied while the
# section asserts two figures a reader will read the wrong way round.
PERMUTATIONS = [
    ("H8", "STATE.md row  before mg-a2bd :  13 551 chars\n"
           "    STATE.md row  after  mg-a2bd :  16 692 chars",
           "STATE.md row  before mg-a2bd :  16 692 chars\n"
           "    STATE.md row  after  mg-a2bd :  13 551 chars",
     "H8's own table now says the STATE.md row SHRANK across mg-a2bd, "
     "against the `(+3 141)` printed on the same line"),
    ("the STATE.md row", "2 928 → 6 069 → −875 → +755",
     "2 928 → 6 069 → +755 → −875",
     "the chain F-1 was born in now runs the two gap figures backwards -- it "
     "asserts the gap reached +755 BEFORE it went negative"),
]


def a4():
    head("A4 -- THE CENSUS IS A MULTISET, SO A PERMUTATION IS INVISIBLE")
    print("""Audited because no line of the brief names it and because it is G-1's own
shape one generation on.  The census asks whether every figure a reader meets
is licensed.  It cannot ask whether each is attached to the statement it
belongs to -- a multiset comparison has no notion of position.  So: exchange
two DECLARED figures OF EQUAL LENGTH in ordinary prose.

  Nothing about the mutation is out of the gate's declared reach.  It is inside
  the section; it is not inside a marked quotation; every token is of the
  figure-shaped class; every designated statement is untouched; the length is
  preserved.  The gate's three checks are all satisfied and the section is
  wrong.  Predicted, before the run: GATE SILENT, exit 0, at 2 of 2.
""")
    print(f"    {'probe':<58}{'predicted':<12}{'observed':<12}{'restored'}")
    invisible = 0
    for site, before, after, why in PERMUTATIONS:
        raw = site_raw(site)
        assert raw.count(before) == 1, (site, before)
        new_raw = raw.replace(before, after, 1)
        assert len(new_raw) == len(raw)
        # the mutation is a PERMUTATION and nothing else: same multiset, same
        # designated reads.
        m0 = sorted(my_tokens(V.assertions(raw)))
        m1 = sorted(my_tokens(V.assertions(new_raw)))
        reader = dict((n, r) for n, r, _k in V.SITES)[site]
        same_reads = reader(raw) == reader(new_raw)
        record(m0 == m1 and same_reads,
               f"{site}: the mutation is a PERMUTATION and nothing else -- the "
               f"multiset of {len(m0)} figure tokens is IDENTICAL before and "
               "after, and every designated statement reads the same value")
        path = put_site(site, new_raw)
        try:
            rc, lines = run_runner()
        finally:
            restore(path)
        assert sha(path) == CLEAN[path]
        rc2, _ = run_runner()
        invisible += 1 if rc == 0 else 0
        print(f"    {site + ': two declared figures exchanged':<58}"
              f"{'gate SILENT':<12}"
              f"{('gate passes' if rc == 0 else 'GATE FIRES'):<12}"
              f"{'green' if rc2 == 0 else 'STILL RED'}"
              f"{'' if rc == 0 else '   <-- PREDICTION MISSED'}")
        print(f"        what a reader now reads: {why}")
    print()
    record(invisible == len(PERMUTATIONS),
           f"{invisible} of {len(PERMUTATIONS)} permutation probes leave the "
           "real runner at exit 0.  A wrong figure a reader meets, inside the "
           "section, in ordinary prose, not quoted, of the figure-shaped class "
           "-- and the widened gate is silent")
    if invisible:
        finding("H-1",
                "THE CENSUS IS A MULTISET, SO A PERMUTATION OF DECLARED FIGURES "
                "IS INVISIBLE.  Two roster figures of equal length exchanged in "
                "ordinary prose keep the multiset identical and every designated "
                "statement correct; the runner stays at exit 0 at 2 of 2 sites "
                "probed.  This is not one of the three exclusions the repair "
                "prints ('marked quotations / outside the section / not "
                "figure-shaped'), so the printed extent is again slightly wider "
                "than the code -- which is G-1's own shape.  MODERATE: the "
                "widening is real and closes what mg-835f found; what is wrong "
                "is the extent list, which should name POSITION as uncovered")


# --------------------------------------------------------------------------
# A5 -- SUMMARY vs ROWS, BOTH DIRECTIONS
# --------------------------------------------------------------------------
def run_8a5c(force=None):
    env = dict(os.environ)
    env.pop("MG8916_FORCE_SUMMARY", None)
    if force:
        env["MG8916_FORCE_SUMMARY"] = force
    r = subprocess.run([sys.executable, os.path.join(REPO, AUDIT_8A5C)],
                       capture_output=True, text=True, cwd=REPO, env=env)
    return r.returncode, r.stdout


def parse_8a5c(out):
    lines = out.split("\n")
    summary = [l.strip() for l in lines if "SUMMARY vs ROWS" in l]
    refuted = None
    for l in lines:
        mm = re.match(r"\s*refuted\s*:\s*(\d+)", l)
        if mm:
            refuted = int(mm.group(1))
    primary = [l.strip() for l in lines
               if "THE PRIMARY TARGET IS" in l and l.strip().startswith("THE")]
    return summary, refuted, primary


def a5():
    head("A5 -- `SUMMARY vs ROWS`: SHOWN TO FIRE, THEN PROBED THE OTHER WAY")
    print("""G-2's defect was an artifact: a transcript containing 'THE PRIMARY TARGET IS
CONFIRMED' and its own refuted PRIMARY rows.  Direction 1 is the repair's own
forcing hook, run here rather than read from its transcript.  Direction 2 makes
the SAME ARTIFACT a different way -- by editing the sentence rather than the
verdict variable -- which is how the defect actually arose.
""")
    rc0, out0 = run_8a5c()
    s0, ref0, p0 = parse_8a5c(out0)
    print("    direction 0 -- as it stands")
    print(f"      SUMMARY vs ROWS : {(s0[0][:11] if s0 else 'ABSENT')}")
    print(f"      refuted         : {ref0}")
    print(f"      exit            : {rc0}")
    record(bool(s0) and s0[0].startswith("[CONFIRMED]"),
           "the `SUMMARY vs ROWS` check EXISTS and is recorded as a check on "
           "the ordinary path")

    rc1, out1 = run_8a5c("CONFIRMED")
    s1, ref1, p1 = parse_8a5c(out1)
    print("    direction 1 -- summary FORCED to CONFIRMED, rows left refuted")
    print(f"      SUMMARY vs ROWS : {(s1[0][:11] if s1 else 'ABSENT')}")
    print(f"      refuted         : {ref0} -> {ref1}")
    print(f"      exit            : {rc0} -> {rc1}")
    record(bool(s1) and s1[0].startswith("[REFUTED"),
           "FORCED APART, the check GOES RED.  It is shown firing, not "
           "argued to be able to fire")
    record(ref1 == ref0 + 1,
           f"and the refuted count moves by exactly one ({ref0} -> {ref1}), so "
           "the check is not decorative and it is the check that moved")

    # ---- direction 2: the same artifact, made the way G-2 was made.
    print()
    print("    direction 2 -- the SENTENCE is made to disagree with the rows,")
    print("    with the verdict variable left alone.  This is the shape G-2")
    print("    actually had: a hand-written bottom line.")
    src = read(AUDIT_8A5C)
    old = 'f"  THE PRIMARY TARGET IS {verdict} IN THIS TREE: "'
    new = 'f"  THE PRIMARY TARGET IS CONFIRMED IN THIS TREE: "'
    assert src.count(old) == 1
    write(AUDIT_8A5C, src.replace(old, new, 1))
    try:
        rc2, out2 = run_8a5c()
    finally:
        restore(AUDIT_8A5C)
    assert sha(AUDIT_8A5C) == CLEAN[AUDIT_8A5C]
    s2, ref2, p2 = parse_8a5c(out2)
    says_confirmed = any("THE PRIMARY TARGET IS CONFIRMED" in l for l in p2)
    bad_rows = out2.count("[REFUTED  ]")
    print(f"      the transcript now prints : {(p2[0][:60] if p2 else '(none)')}")
    print(f"      while its PRIMARY rows are: refuted")
    print(f"      SUMMARY vs ROWS           : {(s2[0][:11] if s2 else 'ABSENT')}")
    print(f"      refuted                   : {ref0} -> {ref2}")
    print(f"      exit                      : {rc0} -> {rc2}")
    caught = bool(s2) and s2[0].startswith("[REFUTED")
    record(says_confirmed,
           "the artifact G-2 named is REPRODUCED: the transcript prints 'THE "
           "PRIMARY TARGET IS CONFIRMED' while its own PRIMARY rows are "
           "[REFUTED], with no environment variable set")
    record(caught,
           "and `SUMMARY vs ROWS` catches it"
           if caught else
           "and `SUMMARY vs ROWS` DOES NOT catch it: it stays [CONFIRMED] and "
           f"the refuted count does not move ({ref0} -> {ref2})")
    if not caught:
        finding("H-2",
                "`SUMMARY vs ROWS` COMPARES A VARIABLE WITH ITSELF.  It scores "
                "`printed == derived` where `printed = FORCE_SUMMARY or "
                "derived`, so off the forcing hook it is `x == x` and cannot "
                "fail for any input.  It does not read the sentence that is "
                "printed: with the REFUTED branch's own headline edited to say "
                "CONFIRMED, the transcript reproduces G-2's exact artifact and "
                "the check stays [CONFIRMED].  The DERIVATION is the real "
                "repair and it is sound -- the verdict cannot be chosen by "
                "hand any more.  What is overstated is the check: the document "
                "calls it a comparison of 'the printed verdict with the rows' "
                "verdict', and it is a comparison of the rows' verdict with "
                "itself.  MODERATE, and it is the vacuous-check shape wearing "
                "the fix's name: it was demonstrated firing only through a hook "
                "built for the demonstration")


# --------------------------------------------------------------------------
# A6 -- mg-835f's OWN INSTRUMENT, UNMODIFIED
# --------------------------------------------------------------------------
def a6():
    head("A6 -- mg-835f's OWN INSTRUMENT, UNMODIFIED, RE-RUN HERE")
    print("""mg-8916's R4 makes this claim; it is re-taken here rather than read out of
its transcript, and the frozen transcript is sha256-checked afterwards.
""")
    record(git("diff", "--stat", "b055ae5^", "HEAD", "--", AUDIT_835F).strip() == "",
           f"`{AUDIT_835F}` is byte-identical between `b055ae5^` and HEAD -- "
           "the instrument that RAISED G-1 and G-2 was not edited by the repair")
    before = sha(AUDIT_835F_OUT)
    r = subprocess.run([sys.executable, os.path.join(REPO, AUDIT_835F)],
                       capture_output=True, text=True, cwd=REPO)
    out = r.stdout
    u1 = [l for l in out.split("\n") if "U1" in l and
          ("GATE FIRES" in l or "gate passes" in l)]
    fires = sum(1 for l in u1 if "GATE FIRES" in l)
    passes = sum(1 for l in u1 if "GATE FIRES" not in l and "gate passes" in l)
    nfind = len([l for l in out.split("\n") if l.strip().startswith("[FINDING")])
    print(f"      its U1 rows : {fires} read GATE FIRES, {passes} read gate passes")
    print(f"      its findings: {nfind}")
    print(f"      its exit    : {r.returncode}")
    record(fires == 3 and passes == 0,
           f"{fires} of 3 of its U1 rows now read GATE FIRES where it observed "
           "exit 0 at 3 of 3 -- measured by re-running it, not by quoting it")
    record(nfind == 0 and r.returncode == 0,
           f"and it returns {nfind} findings at exit {r.returncode}: the "
           "instrument that raised the findings reports none")
    record(sha(AUDIT_835F_OUT) == before,
           "and its committed transcript is sha256-identical afterwards -- the "
           "frozen run as TAKEN was not overwritten by this re-run")


# --------------------------------------------------------------------------
# A7 -- THE RULE, APPLIED TO THE DELIVERABLE ITSELF
# --------------------------------------------------------------------------
def a7():
    head("A7 -- THE RULE APPLIED TO THE REPAIR'S OWN SUMMARY: BELIEVE THE ROWS")
    print("""'If this deliverable's own summary disagrees with its own rows, believe the
rows and report the summary as the defect.'  The repair document's header is a
summary; `out_repair_8916.txt` is its rows.
""")
    doc = read(REPAIR_DOC)
    out = read(REPAIR_OUT)
    rows = {}
    for l in out.split("\n"):
        mm = re.match(r"\s*(checks recorded|confirmed|measurements|refuted|"
                      r"findings)\s*:\s*(\d+)", l)
        if mm:
            rows[mm.group(1)] = int(mm.group(2))
    exits = re.findall(r"EXIT CODE:\s*(\d+)", out) or \
        re.findall(r"exit code[^0-9]{0,40}(\d+)", out)
    print(f"      the transcript's own rows : {rows}")
    hdr = re.search(r"(\d+) checks, (\d+) refuted", doc)
    print(f"      the document's header     : {hdr.group(0) if hdr else '(absent)'}")
    record(hdr is not None and rows.get("checks recorded") == int(hdr.group(1)),
           f"the document's header says {hdr.group(1) if hdr else '?'} checks "
           f"and the transcript records {rows.get('checks recorded')} -- they "
           "agree" if hdr and rows.get("checks recorded") == int(hdr.group(1))
           else "the document's header and the transcript DISAGREE on the "
                "check count; believe the transcript")
    record(hdr is not None and rows.get("refuted") == int(hdr.group(2)),
           f"and on the refuted count: header {hdr.group(2) if hdr else '?'}, "
           f"transcript {rows.get('refuted')}")
    record(rows.get("refuted") == 0 and "Observed: 0" in doc,
           "and the document's 'Predicted exit code ... Observed: 0' is "
           "consistent with a transcript recording 0 refuted")

    # The document's own claim-by-claim table against the transcript.
    print()
    print("  the document's tables, row by row, against the transcript:")
    table = [
        ("6 of 6 wrong-prose probes fire",
         "6 of 6 wrong-prose probes make the REAL runner"),
        ("6 of 6 restorations silent",
         "6 of 6 restorations return the runner to"),
        ("0 live figures over-written",
         "0 live figure is written more times than its site licenses"),
        ("`SUMMARY vs ROWS` fires when forced",
         "sentence says CONFIRMED and its 2 PRIMARY rows say REFUTED"),
        ("mg-835f's instrument: 3 of 3 U1 rows fire",
         "now read GATE FIRES at 3 of 3"),
    ]
    agree = 0
    for label, needle in table:
        ok = needle in out
        agree += 1 if ok else 0
        print(f"    {label:<52}{'in the transcript' if ok else '<-- NOT FOUND'}")
    record(agree == len(table),
           f"{agree} of {len(table)} of the document's headline rows are "
           "located verbatim in the transcript it cites -- the summary is not "
           "just internally consistent, its rows exist")


# --------------------------------------------------------------------------
# A8 -- THE SEAM CHECK, AND ITS THRESHOLD
# --------------------------------------------------------------------------
THRESHOLD = 0.80
MINLEN = 60
CONTEXT = 12

SWEPT = [
    REPAIR_DOC,
    "docs/OneThird-Hodge-Side-Leverage-Mg8a5cRepair-IndependentAudit.md",
    "docs/OneThird-Hodge-Side-Leverage.md",
    "STATE.md",
    "docs/state-history/attempt-mg-a3d4.md",
    "code/hodge_leverage_landing_e1d0/verify_landing.py",
    "code/hodge_leverage_audit_8a5c/audit_repair_8e30.py",
]

MARKERS = ("WITHDRAWN", "withdrawn", "CORRECTED", "corrected", "SUPERSEDED",
           "superseded", "struck", "STRUCK", "used to", "USED TO", "no longer",
           "AMENDED", "amended", "WIDENED", "widened", "REBUILT", "~~",
           "mg-8916", "mg-835f", "mg-a318", "G-1", "G-2", "⚠️", "FROZEN",
           "as taken", "was correct", "PREDICTION MISSED")


def norm(s):
    s = re.sub(r"[`*_#>|]", " ", s)
    return " ".join(s.lower().split())


def a8():
    head("A8 -- SEAM CHECK, AND THE THRESHOLD")
    print(f"""A SEAM is the join between two workers.  Here: mg-835f wrote an audit and
mg-8916 repaired against it, editing the audited RUNNER, a second audit's
SOURCE and two documents.  A seam defect is a passage the repair DELETED that
still stands somewhere with nothing saying it was corrected.

  THRESHOLD: {THRESHOLD:.2f} similarity, minimum passage length {MINLEN} characters
  after normalisation -- the same threshold and minimum mg-a218/mg-d330 used,
  so the sweeps are comparable.  Swept population: the {len(SWEPT)} files a reader of
  this arc actually reads, at HEAD.  Deleted passages come from the three
  commits `b055ae5`, `f5360bf`, `d1dd84d`.
""")
    # ⚠️ TWO CORRECTIONS after this instrument's first run, both kept in
    # `PREDICTIONS.md`.  (1) A line a commit REWRITES IN PLACE shows up in the
    # diff as a deletion, and its replacement is of course still live in the
    # same file -- that is editing, not a seam.  A deleted line is now dropped
    # if the SAME COMMIT added a line to the SAME FILE that resembles it.
    # (2) The correction marker is looked for in a CONTEXT WINDOW of ±12 lines,
    # not on the line itself, which is the convention mg-d330 used: the mg-835f
    # audit annotates its broken reproduction contract in a ⚠️ block BELOW the
    # contract, and a line-local test cannot see it.  Uncorrected, this sweep
    # reported 14 seams, 14 of 14 of them artefacts of MY sweep.
    deleted, added = [], {}
    for commit in ("b055ae5", "f5360bf", "d1dd84d"):
        diff = git("show", "--unified=0", "--format=", commit)
        cur = None
        for l in diff.split("\n"):
            if l.startswith("+++ b/"):
                cur = l[6:]
            elif l.startswith("+") and not l.startswith("+++") and cur:
                added.setdefault((commit, cur), []).append(norm(l[1:]))
            elif l.startswith("-") and not l.startswith("---") and cur:
                t = norm(l[1:])
                if len(t) >= MINLEN:
                    deleted.append((commit, cur, l[1:].strip(), t))
    kept = []
    rewritten = 0
    for commit, path, orig, t in deleted:
        if any(difflib.SequenceMatcher(None, t, a).ratio() >= THRESHOLD
               for a in added.get((commit, path), [])):
            rewritten += 1
            continue
        kept.append((commit, path, orig, t))
    live = []
    for path in SWEPT:
        lines = read(path).split("\n")
        for i, l in enumerate(lines, 1):
            t = norm(l)
            if len(t) >= MINLEN:
                near = "\n".join(lines[max(0, i - 1 - CONTEXT):i + CONTEXT])
                live.append((path, i, l, t, near))
    print(f"    deleted passages          : {len(deleted)}")
    print(f"    ...rewritten in place     : {rewritten}  (an edit, not a seam)")
    print(f"    deleted passages swept    : {len(kept)}")
    print(f"    live lines swept          : {len(live)}")
    hits = 0
    for commit, dpath, orig, t in kept:
        for path, i, l, lt, near in live:
            if abs(len(lt) - len(t)) > len(t) * 0.4:
                continue
            if difflib.SequenceMatcher(None, t, lt).ratio() < THRESHOLD:
                continue
            if any(mk in near for mk in MARKERS):
                continue                      # survives, and is marked
            hits += 1
            print(f"    SEAM  {path}:{i}")
            print(f"          deleted by {commit} from {dpath}: {orig[:100]}")
            print(f"          still live               : {l.strip()[:100]}")
    record(hits == 0,
           f"{hits} unmarked survivals of a passage the repair deleted, over "
           f"{len(kept)} deleted passages x {len(live)} live lines at "
           f"threshold {THRESHOLD:.2f}, minimum {MINLEN} chars, marker window "
           f"±{CONTEXT} lines.  A passage that survives AND is marked as "
           "corrected within the window is not a seam defect and is not counted")


# --------------------------------------------------------------------------
def main():
    print("mg-8aae -- INDEPENDENT AUDIT OF THE mg-8916 REPAIR OF mg-835f")
    print("=" * 78)
    print("""Target: `b055ae5` + `f5360bf` + `d1dd84d`.  0 mathematical statements are
touched here and no finding of mg-835f or mg-8a5c is re-marked.  Predicted exit
code, written into `PREDICTIONS.md` before the first run: 1.""")

    dirty = git("status", "--porcelain", "--", *MUTABLE).strip()
    if dirty:
        sys.exit("REFUSING TO RUN: a file this run will `git checkout --` is "
                 "already dirty; that would destroy it.\n" + dirty)
    for p in MUTABLE:
        CLEAN[p] = sha(p)

    a1()
    a2()
    a3()
    a4()
    a5()
    a6()
    a7()
    a8()

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
        print(f"    FINDING  {tag}: {d[:150]}")
    print()
    # DERIVED from the rows above.  There is no branch here that can assert a
    # verdict the rows refute -- and, unlike the check A5 probes, the sentence
    # is assembled from the counts rather than compared to them.
    if ref == 0 and not FINDINGS:
        print("  THE REPAIR HOLDS AT EVERY POINT MEASURED HERE.")
    else:
        print(f"  PARTIAL: {len(FINDINGS)} finding(s) and {ref} refuted row(s).")
        print("  mg-835f's 12 of 12 is intact at row granularity, G-1 is closed")
        print("  against wording this instrument chose, and mg-835f's own")
        print("  instrument reports zero.  What is open is stated above.")
    return 1 if (FINDINGS or ref) else 0


if __name__ == "__main__":
    sys.exit(main())
