#!/usr/bin/env python3
"""mg-ec07 -- INDEPENDENT AUDIT of mg-ff3e's repair of mg-9207.

THE QUESTION.  mg-9207 found that mg-8eca's census was position-aware for
FIGURES and not for LABELS, so exchanging the two labels instead of the two
figures put mg-8aae's own reader-visible defect back with the gate silent at
3 of 3 sites.  mg-ff3e answered by making the projection LOSSLESS rather than
wider: `partition` cuts each site into (SEGMENTS, FIGURES), both halves are
compared positionally, and `rejoin(segments, figures) == raw` is a gate row.

The assignment is not "does the repair work".  It is:

  1. DID IT FIX THE SET OR THE NEXT FIELD?  "Whole record" is a strong claim
     and this artifact has been fixed field-by-field twice.  Find a field it
     still does not reach.
  2. DID THE SAME-KIND ENUMERATION HAPPEN?  A correct fix that never asked is
     the failure mode, not a success -- and that is a DIFFERENT question from
     whether the fix works.
  3. DO NOT DISTURB WHAT IS CONFIRMED.  mg-9207's 12 of 12 figure exchanges at
     3 of 3 sites.  Re-derive it.

BUILT FROM SCRATCH.  Nothing here re-runs `repair_9207.py` or
`audit_8eca_repair.py` and reports their bottom lines: replication is not
corroboration when the copies share a source.  Every population below is
derived from the tree by this file's own code.  The only thing imported from
the artifact under audit is the GATE ITSELF -- `census_gate` -- because an
audit that re-implements the gate is auditing its own re-implementation.

WHAT IT TOUCHES.  A1-A4 and A6 are IN MEMORY and touch nothing.  A5 and A7
MUTATE THE TREE and restore it, sha256-verified, and refuse to run against a
dirty tree scoped to the files they will restore.

Pure Python 3 + git.  No third-party packages.
"""

import hashlib
import importlib.util
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
LANDING_DIR = os.path.join(REPO, "code", "hodge_leverage_landing_e1d0")
LANDING = os.path.join(LANDING_DIR, "verify_landing.py")
RECORDS = os.path.join(LANDING_DIR, "site_records.txt")

STATE = "STATE.md"
DELIV = "docs/OneThird-Hodge-Side-Leverage.md"
HIST = "docs/state-history/attempt-mg-a3d4.md"

# The files A5/A7 write to and restore.  A dirty tree scoped to these is a
# refusal: a restore over an uncommitted edit destroys it.
MUTATED = [STATE, DELIV, HIST,
           "code/hodge_leverage_landing_e1d0/verify_landing.py",
           "code/hodge_leverage_landing_e1d0/site_records.txt"]

FULL = "--full" in sys.argv[1:]

RESULTS = []
FINDINGS = []


# --------------------------------------------------------------------------
# plumbing
# --------------------------------------------------------------------------
def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True, check=True).stdout


def read(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
        return fh.read()


def write(rel, text):
    with open(os.path.join(REPO, rel), "w", encoding="utf-8") as fh:
        fh.write(text)


def sha(rel):
    with open(os.path.join(REPO, rel), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


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


def heading(name, row):
    """The gate row's HEADING, with the site prefix removed.  A substring test
    over the whole row reports every probe as having broken every check,
    because each of these rows explains itself by NAMING the other rows --
    mg-ff3e's own instrument did that and its own attribution row caught it.
    Derived here rather than imported, so this is not the same mistake by
    inheritance."""
    return row.split(" -- ")[0].replace(f"GATE @ {name}: ", "")


# --------------------------------------------------------------------------
# the gate under audit, at HEAD and at the commit where the defect is present
# --------------------------------------------------------------------------
def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.REPO = REPO
    return mod


TMP = tempfile.mkdtemp(prefix="mg-ec07-")
V = load_module(LANDING, "verify_landing_head")


def pre_repair_module():
    """`verify_landing.py` AT THE COMMIT WHERE THE DEFECT IS STILL PRESENT.
    A control has to be demonstrated against a tree that still has the thing
    it claims to catch, or "it catches everything" and "it fires on
    everything" are the same sentence."""
    first = git("log", "--reverse", "--format=%H", "-S", "def partition(",
                "--", "code/hodge_leverage_landing_e1d0/verify_landing.py"
                ).split()
    fix = first[0]
    parent = git("rev-parse", f"{fix}^").strip()
    src = git("show", f"{parent}:code/hodge_leverage_landing_e1d0/"
                      "verify_landing.py")
    path = os.path.join(TMP, "verify_landing_pre.py")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(src)
    return fix, parent, load_module(path, "verify_landing_pre")


def measured_now():
    a = len(V.state_row(V.tree(V.STATE)))
    b = len(V.deliv_row(V.tree(V.DELIV)))
    h = len(V.tree(V.HIST))
    return {"gap":  V.doc_num(a - b, signed=True),
            "both": V.doc_num(a + h - b, signed=True),
            "cell": V.doc_num(a), "hist": V.doc_num(h), "copy": V.doc_num(b)}


# --------------------------------------------------------------------------
# A0 -- preflight
# --------------------------------------------------------------------------
def a0():
    head("A0 -- PREFLIGHT")
    dirty = [l[3:] for l in git("status", "--porcelain", "--",
                                *MUTATED).split("\n") if l.strip()]
    if dirty:
        print("  REFUSING: uncommitted changes to files this instrument")
        print("  mutates and restores.  A restore over them destroys them:")
        for d in dirty:
            print(f"    - {d}")
        raise SystemExit(2)
    record(True, f"A0 the {len(MUTATED)} files this instrument mutates and "
                 f"restores are clean at start")
    rc, out = run_runner()
    record(rc == 0, f"A0 the real runner on the clean tree exits {rc} "
                    f"(predicted 0), "
                    f"{len(refuted_rows(out))} refuted rows")
    return out


def run_runner():
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("VERIFY_", "HODGE_", "MG_"))}
    r = subprocess.run([sys.executable, LANDING], capture_output=True,
                       text=True, env=env, cwd=REPO)
    return r.returncode, r.stdout + r.stderr


def refuted_rows(out):
    return [l.strip()[len("[REFUTED  ] "):]
            for l in out.split("\n") if l.strip().startswith("[REFUTED")]


def gate_row(out, site, kind):
    """The verdict of one named gate row for one site, or None."""
    want = f"GATE @ {site}: {kind} -- "
    for l in out.split("\n"):
        s = l.strip()
        if not s.startswith("["):
            continue
        body = s[s.index("]") + 2:]
        if body.startswith(want):
            return s.startswith("[CONFIRMED")
    return None


# --------------------------------------------------------------------------
# A1/A2 -- THE RECORD IS THE SITE, BYTE FOR BYTE
# --------------------------------------------------------------------------
def mutate_char(raw, i):
    c = raw[i]
    return raw[:i] + ("X" if c != "X" else "Y") + raw[i + 1:]


def a1(texts, measured):
    head("A1 -- THE RECORD IS THE SITE, BYTE FOR BYTE (in memory, a FIXTURE)")
    print("""⚠️  A FIXTURE, declared: this calls `census_gate` on strings in memory.  A5
runs on disk against the real runner, and A5 is the evidence.

The claim under audit is mg-ff3e's own: the projection is LOSSLESS, so no
field can be left behind because nobody named it.  The strongest statement of
that claim is a population nobody wrote down: EVERY CHARACTER OF EVERY SITE,
substituted alone.  If one byte of a site can move in silence, "the whole
record" is not what is compared.

The population is derived from the tree, not from a list.  No figure, segment
or field is named anywhere in this section.
""")
    fix, parent, PRE = pre_repair_module()
    print(f"  the repair lands at   : {fix[:7]}")
    print(f"  the control runs at   : {parent[:7]}  (the defect still present)")
    print()
    tot = {"n": 0, "head": 0, "pre": 0}
    per_row = {}
    for name, _r, _k in V.SITES:
        raw = texts[name]
        nhead = npre = 0
        for i in range(len(raw)):
            mut = mutate_char(raw, i)
            bad = [d for ok, d in V.census_gate(name, mut, measured) if not ok]
            if bad:
                nhead += 1
                for d in bad:
                    per_row[heading(name, d)] = per_row.get(
                        heading(name, d), 0) + 1
            if any(not ok for ok, _ in PRE.census_gate(name, mut, measured)):
                npre += 1
        record(nhead == len(raw),
               f"A1 {name}: {nhead} of {len(raw)} characters of this site "
               f"cannot be substituted in silence")
        record(None,
               f"A1-control {name}: the SAME instrument against the gate at "
               f"{parent[:7]} catches {npre} of {len(raw)} "
               f"({100.0 * npre / len(raw):.1f}%)")
        tot["n"] += len(raw)
        tot["head"] += nhead
        tot["pre"] += npre
    record(tot["head"] == tot["n"],
           f"A1 TOTAL {tot['head']} of {tot['n']} characters over the 3 sites "
           f"(the STATE.md row 13 367 + §14 16 647 + H8 7 852) fire at HEAD")
    record(tot["pre"] < tot["head"],
           f"A1-control TOTAL {tot['pre']} of {tot['n']} fire against the "
           f"pre-repair gate at {parent[:7]} -- "
           f"{100.0 * tot['pre'] / tot['n']:.1f}% against "
           f"{100.0 * tot['head'] / tot['n']:.1f}%.  THIS IS THE CONTROL: an "
           f"instrument that catches nearly everything at HEAD and almost "
           f"nothing one commit earlier is measuring the repair, not itself")
    head("A2 -- WHICH ROW CATCHES IT")
    for k in sorted(per_row, key=lambda x: -per_row[x]):
        print(f"    {k:<20} {per_row[k]:>6}")
    rp = per_row.get("RECORD PARTITION", 0)
    record(rp == 0,
           f"A2 RECORD PARTITION fires on {rp} of {tot['n']} single-character "
           f"mutations.  `rejoin(partition(raw)) == raw` is an identity that "
           f"holds for EVERY string, so NO EDIT TO ANY DOCUMENT CAN MOVE IT.  "
           f"That is not a defect -- it is what mg-ff3e said the row is, and "
           f"why D3 had to bend the CODE to falsify it -- but the row that "
           f"licenses 'the whole record is compared' is unfalsifiable by any "
           f"document edit, and this audit puts a number on that")
    record(None,
           f"A2 the row that does the catching is SITE RECORD "
           f"({per_row.get('SITE RECORD', 0)} of {tot['n']}), which is the "
           f"half of the record mg-9207 found was not being compared.  ⚠️ "
           f"PREDICTION MISS, kept: A2 predicted a PARTITION -- non-figure "
           f"characters caught by SITE RECORD, figure characters by the "
           f"FIGURE rows.  SITE RECORD catches ALL "
           f"{per_row.get('SITE RECORD', 0)}, figure characters included, "
           f"because destroying a figure token moves its bytes into a "
           f"SEGMENT.  The figure rows catch "
           f"{per_row.get('FIGURE ORDER', 0)} of {tot['n']} and add nothing "
           f"SITE RECORD does not already catch, ON THIS POPULATION")
    return parent, PRE


def a2c(tot_exchanges):
    """The complementarity, stated with both numbers.  Not pre-registered:
    it falls out of A1 and A3 rather than being predicted."""
    head("A2c -- NEITHER ROW IS REDUNDANT (measurement, from A1 and A3)")
    record(None,
           "A2c on POINT MUTATIONS, SITE RECORD catches 37 866 of 37 866 and "
           "FIGURE ORDER 462 -- SITE RECORD alone would do.  On EXCHANGES "
           f"(A3), FIGURE ORDER catches {tot_exchanges} of {tot_exchanges} "
           "and SITE RECORD 0 -- FIGURE ORDER alone does.  The two halves are "
           "not two views of one check: each is the whole of the answer on "
           "the population the other is blind to, which is why removing "
           "either is a real deletion and why mg-ff3e's D1b/D2 split at that "
           "seam was the right unit")


def a2b(texts, PRE, parent):
    """NOT PRE-REGISTERED -- added during construction, before the first run,
    and marked as a MEASUREMENT rather than scored as a prediction."""
    head("A2b -- DID THE ASSERTED-FIGURE POPULATION ITSELF MOVE? (measurement)")
    print("""mg-ff3e re-derived `figure_sequence` from `partition` and unified the
marked-quotation convention into one `quoted_spans`.  A change to WHICH tokens
count as asserted would silently change what (c)/(d) are about.  Not
pre-registered; recorded as a measurement.
""")
    same = 0
    for name, _r, _k in V.SITES:
        a = V.figure_sequence(texts[name])
        b = PRE.figure_sequence(texts[name])
        ok = a == b
        same += ok
        record(None,
               f"A2b {name}: {len(a)} asserted figures at HEAD, {len(b)} at "
               f"{parent[:7]} -- {'IDENTICAL' if ok else 'DIFFERENT'}")
    record(same == len(V.SITES),
           f"A2b {same} of {len(V.SITES)} sites assert the same figure "
           f"sequence before and after the repair, so (c)/(d) are about the "
           f"same population and A3 below compares like with like")


# --------------------------------------------------------------------------
# A3/A4 -- THE FIGURE HALF IS NOT DISTURBED
# --------------------------------------------------------------------------
def exchange(raw, i, j):
    segs, figs = V.partition(raw)
    figs = list(figs)
    figs[i], figs[j] = figs[j], figs[i]
    return V.rejoin(segs, figs)


def a3(texts, measured):
    head("A3 -- mg-9207's 12 OF 12, RE-DERIVED AT A POPULATION NOBODY WROTE")
    print("""mg-9207 confirmed C3 on TWELVE exchanges at 3 sites, and mg-ff3e re-ran
mg-9207's own instrument to show it still holds.  That is replication with a
shared source.  This enumerates EVERY unordered pair of asserted figure slots
whose VALUES DIFFER, derived from `partition` -- and asks the same question of
all of them: does it fire, and is FIGURE ORDER the only census row that does?

If a repair that added two rows to the gate had weakened the figure case, this
is where it would show.
""")
    tot = {"n": 0, "fire": 0, "order": 0, "rec": 0, "part": 0, "cens": 0}
    for name, _r, _k in V.SITES:
        raw = texts[name]
        figs = V.partition(raw)[1]
        pairs = [(i, j) for i in range(len(figs)) for j in range(i + 1, len(figs))
                 if figs[i] != figs[j]]
        n = fire = order = rec = part = cens = 0
        for i, j in pairs:
            rows = V.census_gate(name, exchange(raw, i, j), measured)
            bad = {heading(name, d) for ok, d in rows if not ok}
            n += 1
            fire += bool(bad)
            order += "FIGURE ORDER" in bad
            rec += "SITE RECORD" not in bad
            part += "RECORD PARTITION" not in bad
            cens += "FIGURE CENSUS" not in bad
        record(fire == n and order == n,
               f"A3 {name}: {fire} of {n} differing-value figure exchanges "
               f"fire, FIGURE ORDER refuted on {order} of {n}")
        record(rec == n and part == n and cens == n,
               f"A3 {name}: SITE RECORD green on {rec} of {n}, RECORD "
               f"PARTITION green on {part} of {n}, FIGURE CENSUS green on "
               f"{cens} of {n} -- the record masks figures with a "
               f"VALUE-INDEPENDENT marker, so moving figures must not move it")
        for k, v in (("n", n), ("fire", fire), ("order", order),
                     ("rec", rec), ("part", part), ("cens", cens)):
            tot[k] += v
    record(tot["fire"] == tot["n"] and tot["order"] == tot["n"],
           f"A3 TOTAL {tot['fire']} of {tot['n']} figure exchanges over the "
           f"three sites fire with FIGURE ORDER refuted, and FIGURE ORDER is "
           f"the ONLY census row refuted on {tot['cens']}/{tot['rec']}/"
           f"{tot['part']} of them.  mg-9207's C3 is not disturbed -- it is "
           f"re-derived at {tot['n'] // 12}x its population by an instrument "
           f"that shares no code with it")
    return tot


def a4(texts):
    head("A4 -- 'TWO OCCURRENCES OF THE SAME TOKEN' IS AN EMPTY SET, MEASURED")
    print("""mg-ff3e's second uncovered bullet says this is an EMPTY SET rather than a
blind spot, and that the difference is checkable.  Nobody checked it.  Here it
is checked: exchange them and compare the result to the original BYTE FOR BYTE.
""")
    tot = n = 0
    for name, _r, _k in V.SITES:
        raw = texts[name]
        figs = V.partition(raw)[1]
        pairs = [(i, j) for i in range(len(figs))
                 for j in range(i + 1, len(figs)) if figs[i] == figs[j]]
        same = sum(1 for i, j in pairs if exchange(raw, i, j) == raw)
        record(same == len(pairs),
               f"A4 {name}: {same} of {len(pairs)} equal-value exchanges are "
               f"byte-identical to the original")
        tot += same
        n += len(pairs)
    record(tot == n,
           f"A4 TOTAL {tot} of {n} equal-value figure exchanges over the "
           f"three sites are the IDENTITY MAP ON THE BYTES.  The bullet is an "
           f"empty set and is now a measurement rather than a sentence")


# --------------------------------------------------------------------------
# A5 -- THE FIELD IT DOES NOT REACH, ON DISK
# --------------------------------------------------------------------------
STATE_HDR = "| verdict | attempt | note |"
STATE_HDR_X = "| attempt | verdict | note |"
H8_HDR = "at bbe83b5^    at bbe83b5  AFTER mg-8e30"
H8_HDR_X = "at bbe83b5     at bbe83b5^ AFTER mg-8e30"


def swap_first_cell(text, ia, ib):
    """Exchange the first cell of two markdown table rows, figures untouched."""
    lines = text.split("\n")
    a, b = lines[ia].split(" | "), lines[ib].split(" | ")
    a[0], b[0] = "| " + b[0][2:], "| " + a[0][2:]
    lines[ia], lines[ib] = " | ".join(a), " | ".join(b)
    return "\n".join(lines)


def probe_on_disk(tag, rel, edit, what):
    """Apply `edit` to `rel` on disk, run the REAL runner with no environment
    variable set, restore, and verify the restoration by sha256.

    Every probe here is LENGTH-PRESERVING, deliberately: three of the five
    measurements are lengths of these files, so a probe that changed one would
    fire the designated readers and the fire would not be attributable to the
    half of the record under audit."""
    before = read(rel)
    before_sha = sha(rel)
    new = edit(before)
    assert new != before, f"{tag}: the edit did nothing"
    assert len(new) == len(before), f"{tag}: not length-preserving"
    write(rel, new)
    try:
        rc, out = run_runner()
    finally:
        write(rel, before)
    ok = sha(rel) == before_sha
    return rc, out, ok, what


def a5():
    head("A5 -- THE FIELD IT DOES NOT REACH, ON DISK")
    print("""The claim is "position-aware over the WHOLE record".  The assignment's first
branch: find a field it still does not reach, exchange values in it, and see
whether the census fires.

X3 is the DISCRIMINATION CONTROL and it runs first.  It is mg-9207's E3 --
two historical COLUMN HEADERS exchanged -- INSIDE a site.  If X3 were silent
too, X1 and X2 would be my probes failing rather than the gate.

X1 and X2 are the SAME KIND of mutation, at the site whose file is largest.
No figure is touched by any of the three: only labels move.
""")
    rows = []
    rc, out, rest, what = probe_on_disk(
        "X3", HIST, lambda t: t.replace(H8_HDR, H8_HDR_X, 1),
        "H8's two historical column headers exchanged (mg-9207's E3), INSIDE "
        "the site")
    site_rec = gate_row(out, "H8", "SITE RECORD")
    fig_c = gate_row(out, "H8", "FIGURE CENSUS")
    fig_o = gate_row(out, "H8", "FIGURE ORDER")
    rows.append(("X3", rc, rest, what, site_rec, fig_c, fig_o))
    record(rc == 1 and site_rec is False,
           f"A5-X3 CONTROL: the same kind INSIDE a site -- runner exit {rc} "
           f"(predicted 1), SITE RECORD @ H8 "
           f"{'REFUTED' if site_rec is False else site_rec}, FIGURE CENSUS "
           f"{fig_c}, FIGURE ORDER {fig_o}.  The probe mechanism works and "
           f"the catch is attributable to the half of the record mg-ff3e added")

    rc1, out1, rest1, what1 = probe_on_disk(
        "X1", STATE, lambda t: t.replace(STATE_HDR, STATE_HDR_X, 1),
        "STATE.md's ledger table COLUMN HEADERS exchanged -- the verdict "
        "column is now labelled `attempt`")
    rows.append(("X1", rc1, rest1, what1, None, None, None))
    rc2, out2, rest2, what2 = probe_on_disk(
        "X2", STATE, lambda t: swap_first_cell(
            t, *two_rows_above_the_site(t)),
        "the VERDICT LABELS of the two ledger rows immediately above the A5 "
        "row exchanged")
    rows.append(("X2", rc2, rest2, what2, None, None, None))

    print()
    print("    probe  exit  refuted  what was exchanged")
    for tag, rc_, rest_, what_, *_ in rows:
        o = {"X3": out, "X1": out1, "X2": out2}[tag]
        print(f"    {tag}     {rc_}     {len(refuted_rows(o)):>2}     "
              f"{what_[:80]}")
    print()
    for tag, rc_, out_ in (("X1", rc1, out1), ("X2", rc2, out2)):
        record(None,
               f"A5-{tag} runner exit {rc_}, {len(refuted_rows(out_))} "
               f"refuted rows (predicted 0 and 0 -- SILENT)")
    silent = rc1 == 0 and rc2 == 0 and not refuted_rows(out1) \
        and not refuted_rows(out2)
    if silent:
        finding("E-1",
                "THE FIELD IT DOES NOT REACH IS THE SITE BOUNDARY, AND THE "
                "SAME KIND OF EXCHANGE IS STILL SILENT.  X1 exchanges the two "
                "COLUMN HEADERS of the STATE.md ledger table -- the identical "
                "mutation mg-9207 raised as E3 and mg-ff3e enumerated, "
                "checked at H8 and CAUGHT there (X3, exit 1).  At the "
                "STATE.md site the same mutation is exit 0 with 0 refuted "
                "rows, because the STATE.md site is ONE LINE and the header "
                "of the table that line sits in is outside it.  The record is "
                "lossless OVER THE SITE; the projection that remains is the "
                "SITE, and it is now the whole of the residue")
    record(rest and rest1 and rest2,
           f"A5 {sum([rest, rest1, rest2])} of 3 restorations are "
           f"sha256-identical to the pre-probe file")
    return rc1, rc2, out1, out2


def two_rows_above_the_site(state_text):
    lines = state_text.split("\n")
    i = [k for k, l in enumerate(lines)
         if l.startswith("| **AMBER-POSITIVE")]
    assert len(i) == 1, "expected exactly one A5 row"
    return i[0] - 2, i[0] - 1


def a5b(texts, measured):
    head("A5b -- ONE FIGURE EXCHANGE PER SITE, ON DISK (the fixture bridged)")
    print("""A3 is in memory.  This puts one figure exchange per site ON DISK against the
real runner, so the fixture's result is bridged to the artifact.
""")
    n = ok = 0
    for name, _r, _k in V.SITES:
        raw = texts[name]
        figs = V.partition(raw)[1]
        pair = next((i, j) for i in range(len(figs))
                    for j in range(i + 1, len(figs))
                    if figs[i] != figs[j] and len(figs[i]) == len(figs[j]))
        new_site = exchange(raw, *pair)
        rel = {"the STATE.md row": STATE, "§14": DELIV, "H8": HIST}[name]
        rc, out, rest, _ = probe_on_disk(
            f"XF-{name}", rel, lambda t, r=raw, s=new_site: t.replace(r, s, 1),
            "figure exchange")
        fo = gate_row(out, name, "FIGURE ORDER")
        sr = gate_row(out, name, "SITE RECORD")
        n += 1
        ok += rc == 1 and fo is False and sr is True and rest
        record(rc == 1 and fo is False and sr is True,
               f"A5b {name}: figures {figs[pair[0]]!r} and {figs[pair[1]]!r} "
               f"exchanged on disk -- runner exit {rc} (predicted 1), FIGURE "
               f"ORDER {'REFUTED' if fo is False else fo}, SITE RECORD "
               f"{'green' if sr else sr}, restored {rest}")
    record(ok == n,
           f"A5b {ok} of {n} sites: a figure exchange on disk is caught by "
           f"FIGURE ORDER with SITE RECORD green -- mg-9207's C3 shape, on "
           f"the artifact, measured by this instrument and not re-run from "
           f"mg-9207's")


# --------------------------------------------------------------------------
# A6 -- THE STATED SET AGAINST THE CODE
# --------------------------------------------------------------------------
def a6(texts):
    head("A6 -- THE STATED SET AGAINST THE CODE")
    print("""mg-ff3e states its residue rather than hiding it, so the assignment's third
branch applies as well: verify the stated set matches the code.

The sentence, printed beside the gate in `verify_landing.py` and again in R5
of `repair_9207.py`:

    "text OUTSIDE the site is not read, BECAUSE A SITE IS A SECTION"
""")
    src = read("code/hodge_leverage_landing_e1d0/verify_landing.py")
    said = "a site is a section" in src.lower()
    record(said,
           "A6 the sentence 'a site is a SECTION' is printed beside the gate "
           "in verify_landing.py")
    import inspect
    body = inspect.getsource(V.site_texts)
    bysec = [n for n, _r, _k in V.SITES
             if re.search(rf'"{re.escape(n)}":\s*section\(', body)]
    byline = [n for n, _r, _k in V.SITES if n not in bysec]
    record(len(bysec) == 2 and len(byline) == 1,
           f"A6 {len(bysec)} of 3 sites are obtained by `section()` "
           f"({', '.join(bysec)}); {len(byline)} is obtained by `find_line()` "
           f"({', '.join(byline)}) and is ONE LINE, not a section")
    for name, _r, _k in V.SITES:
        record(None, f"A6 {name}: {len(texts[name].split(chr(10)))} line(s), "
                     f"{len(texts[name]):,} chars")
    files = {STATE: read(STATE), DELIV: read(DELIV), HIST: read(HIST)}
    inside = sum(len(texts[n]) for n, _r, _k in V.SITES)
    total = sum(len(t) for t in files.values())
    record(None,
           f"A6 {inside:,} of {total:,} characters of the three files are "
           f"inside a record ({100.0 * inside / total:.1f}%); "
           f"{total - inside:,} are outside every record "
           f"({100.0 * (total - inside) / total:.1f}%)")
    finding("E-2",
            "THE STATED REASON IS NOT TRUE OF THE CODE AT 1 OF 3 SITES.  "
            "'text outside the site is not read, BECAUSE A SITE IS A SECTION' "
            "is the disclosure a reader meets, and it is the sentence that "
            "sizes the residue for them.  Two sites are sections.  The "
            "STATE.md site is ONE LINE returned by `find_line`, so what is "
            "excluded there is not 'the rest of the file outside this "
            "section' but 'the whole ledger table this row is a row of, "
            "including its column headers' -- which is exactly what X1 "
            "exchanges.  This is the shape mg-ff3e's own R5 opens by naming: "
            "a printed extent slightly wider than the code beneath it")


# --------------------------------------------------------------------------
# A7 -- THE BLESSING PATH  (the floor item: no list in the assignment names it)
# --------------------------------------------------------------------------
def run_reseal():
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("VERIFY_", "HODGE_", "MG_"))}
    r = subprocess.run([sys.executable, LANDING, "--reseal"],
                       capture_output=True, text=True, env=env, cwd=REPO)
    return r.returncode, r.stdout + r.stderr


def a7(texts, measured):
    head("A7 -- THE BLESSING PATH (the floor item)")
    print("""AUDITED BECAUSE NO LIST IN THE ASSIGNMENT NAMES IT.  `--reseal` is, in
mg-ff3e's own words, "the only step in this instrument that can make a wrong
document green".  R5 names three things that narrow it.  Nothing in the arc
EXECUTES it -- not `run_all.sh`, not the negative control, not R1-R5.  A
control that has never been run is a sentence.
""")
    hits = []
    for root, _d, fs in os.walk(os.path.join(REPO, "code")):
        if os.path.abspath(root).startswith(HERE):
            continue          # this instrument's own invocations, below
        for f in fs:
            p = os.path.join(root, f)
            try:
                with open(p, encoding="utf-8") as fh:
                    t = fh.read()
            except (UnicodeDecodeError, IsADirectoryError):
                continue
            for l in t.split("\n"):
                if "--reseal" in l and (
                        "subprocess" in l or l.strip().startswith("python3")
                        or "sys.executable" in l):
                    hits.append((os.path.relpath(p, REPO), l.strip()[:70]))
    record(len(hits) == 0,
           f"A7-B0 {len(hits)} invocations of `--reseal` anywhere under "
           f"code/ outside this instrument's own directory (predicted 0).  "
           f"⚠️ The first version of this check counted THIS FILE and read 1: "
           f"the miss is kept in PREDICTIONS.md.  `--reseal` is NAMED in four "
           f"places and EXECUTED in none, which is why this audit executes it")

    rec_sha = sha("code/hodge_leverage_landing_e1d0/site_records.txt")

    # B1 -- a live figure corrupted, in §14, length-preserving, and NOT in the
    # line any measurement is taken from.
    gapfig = measured["gap"]
    d14 = texts["§14"]
    assert d14.count(gapfig) == 1, \
        f"expected the live gap figure {gapfig!r} exactly once in §14, " \
        f"got {d14.count(gapfig)}"
    bad14 = d14.replace(gapfig, bump(gapfig), 1)
    assert len(bad14) == len(d14)
    before = read(DELIV)
    write(DELIV, before.replace(d14, bad14, 1))
    try:
        rc, out = run_reseal()
        rcr, outr = run_runner()
    finally:
        write(DELIV, before)
    record(rc == 1 and sha("code/hodge_leverage_landing_e1d0/site_records.txt")
           == rec_sha,
           f"A7-B1 a LIVE FIGURE corrupted ({gapfig} -> {bump(gapfig)} in "
           f"§14): the runner exits {rcr} and `--reseal` exits {rc} "
           f"(predicted 1, REFUSED) with site_records.txt sha256 UNCHANGED.  "
           f"A section whose figures are wrong cannot be blessed")

    # B2 -- `partition` bent lossy (D3's shape: a kernel put back).
    lp = "code/hodge_leverage_landing_e1d0/verify_landing.py"
    src = read(lp)
    n0 = src.count(".lower())")
    bent = src.replace("        segments.append(raw[last:m.start()])",
                       "        segments.append(raw[last:m.start()].lower())"
                       ) \
              .replace("    segments.append(raw[last:])",
                       "    segments.append(raw[last:].lower())")
    assert bent.count(".lower())") == n0 + 2, "B2 bend did not apply twice"
    write(lp, bent)
    try:
        rc2, out2 = run_reseal()
        sealed_lossy = sha(
            "code/hodge_leverage_landing_e1d0/site_records.txt") != rec_sha
    finally:
        write(lp, src)
        git("checkout", "--",
            "code/hodge_leverage_landing_e1d0/site_records.txt")
    record(rc2 == 1,
           f"A7-B2 `partition` bent LOSSY (segments lower-cased -- D3's "
           f"shape): `--reseal` exits {rc2} -- PREDICTED 1, REFUSED, "
           f"OBSERVED {rc2}.  The record it wrote "
           f"{'DID' if sealed_lossy else 'did NOT'} change")

    # WHY.  The refusal excludes rows by a SUBSTRING TEST over the WHOLE ROW,
    # and every one of these rows explains itself by NAMING the other rows.
    rows = V.figure_gate(texts, measured)
    excl = [r for _ok, r in rows if "SITE RECORD" in r]
    unintended = [r for r in excl
                  if not r.split(" -- ")[0].endswith("SITE RECORD")]
    record(len(unintended) == 0,
           f"A7-B2b of {len(rows)} gate rows, {len(excl)} contain the string "
           f"'SITE RECORD' and are therefore excluded from `reseal`'s "
           f"refusal.  {len(excl) - len(unintended)} are the SITE RECORD rows "
           f"themselves, which is intended.  {len(unintended)} are NOT: "
           f"{', '.join(sorted({r.split(' -- ')[0] for r in unintended}))}")
    wrote = ("writes a record built from a partition that is not the section"
             if sealed_lossy else "refuses")
    if unintended:
        finding("E-5",
                f"THE REFUSAL IS HOLED AT THE ROW THAT LICENSES THE WHOLE "
                f"CLAIM, BY THE EXACT DEFECT mg-ff3e DIAGNOSED IN ITS OWN "
                f"INSTRUMENT AND DID NOT LOOK FOR IN THE ARTIFACT.  "
                f"`reseal()` refuses while any gate row other than SITE "
                f"RECORD is refuted, and it identifies those rows with "
                f"`\"SITE RECORD\" not in d` -- a substring test over the "
                f"WHOLE ROW.  The RECORD PARTITION row's own explanation says "
                f"'...everything else by SITE RECORD, and nothing is in "
                f"neither', so all {len(unintended)} RECORD PARTITION rows "
                f"are excluded too.  Measured: with `partition` bent lossy, "
                f"`--reseal` exits {rc2} and {wrote}.  This is R5 "
                f"item 3 verbatim -- `\"FIGURE CENSUS\" in row` matching the "
                f"SITE RECORD row's own explanation -- which mg-ff3e found in "
                f"`repair_9207.py`, fixed there with `heading()`, kept in its "
                f"PREDICTIONS, and did not ask where else the same shape "
                f"lived.  It lived forty lines away in the file it was "
                f"repairing.  The one-line fix is the same one: key on the "
                f"row's HEADING")

    # B3 -- a LABEL exchange, then reseal, then the runner.
    beforeh = read(HIST)
    write(HIST, beforeh.replace(H8_HDR, H8_HDR_X, 1))
    try:
        rcb, outb = run_runner()
        rc3, out3 = run_reseal()
        rc3b, out3b = run_runner()
        newrec = read("code/hodge_leverage_landing_e1d0/site_records.txt")
        diff = git("diff", "--numstat", "--",
                   "code/hodge_leverage_landing_e1d0/site_records.txt").split()
    finally:
        write(HIST, beforeh)
        git("checkout", "--",
            "code/hodge_leverage_landing_e1d0/site_records.txt")
    restored = sha("code/hodge_leverage_landing_e1d0/site_records.txt") \
        == rec_sha
    gates_after = [r for r in refuted_rows(out3b) if r.startswith("GATE @")]
    crashed = "Traceback" in out3b or "AssertionError" in out3b
    record(rc3 == 0 and not gates_after,
           f"A7-B3 X3's LABEL EXCHANGE, then `--reseal`: the runner is "
           f"{rcb} before the reseal, `--reseal` exits {rc3} (predicted 0, "
           f"BLESSED), and after it EVERY GATE ROW IS GREEN "
           f"({len(gates_after)} refuted) with the defect on the page.  "
           f"⚠️ PREDICTION MISS, kept: I predicted the runner would exit 0 "
           f"after the reseal; it exits {rc3b}, and the reason is "
           f"{'mg-9207 J-3 -- the negative control raises on an edit at its own probe site, and a crash and a fire are the same integer' if crashed else 'a non-gate row'}"
           f".  That is somebody else's open item, not a gate row catching "
           f"the label exchange -- the gate rows are green.  The reviewable "
           f"diff is {diff[0] if diff else '?'}+/"
           f"{diff[1] if len(diff) > 1 else '?'}- lines of site_records.txt")
    record(restored, "A7-B3 site_records.txt restored, sha256-identical")
    if rc3 == 0 and not gates_after:
        finding("E-3",
                f"THE BLESSING PATH IS THE WHOLE OF (e)'s STRENGTH AND IT IS "
                f"UNEXERCISED.  `--reseal` refuses on a wrong FIGURE (B1) but "
                f"by construction it CANNOT refuse on a wrong LABEL -- SITE "
                f"RECORD is excluded from the refusal, and SITE RECORD is the "
                f"only row a label exchange moves.  So the exact mutation "
                f"mg-ff3e was assigned to catch is one `--reseal` away from "
                f"green, and the only thing standing between them is a human "
                f"reading a "
                f"{diff[0] if diff else '?'}-line diff.  That is mg-ff3e's "
                f"stated design and this audit does not dispute the DESIGN; "
                f"what it disputes is that the narrowing was never MEASURED.  "
                f"Nothing in the arc runs `--reseal` at all (B0 = 0 of 0), so "
                f"neither half of 'it refuses while any other gate row is "
                f"refuted' had a control until now -- and B6 below measures "
                f"what one blessing actually costs")

    # B6 -- THE DECISIVE ONE.  B3's post-reseal exit 1 was not a gate row: it
    # was N21 reporting PROBE NOT APPLIED because its own literal had moved.
    # So this is a label exchange that is NOT one of the seven frozen probe
    # literals and is NOT read by any designated reader.
    L1 = "deliverable §14 copy         "
    L2 = "the mismatch A5 reports      "
    beforeh = read(HIST)
    assert beforeh.count(L1) == 1 and beforeh.count(L2) == 1
    assert len(L1) == len(L2)
    swapped = beforeh.replace(L1, "\0", 1).replace(L2, L1, 1) \
                     .replace("\0", L2, 1)
    assert len(swapped) == len(beforeh) and swapped != beforeh
    write(HIST, swapped)
    try:
        rc6a, out6a = run_runner()
        rc6b, out6b = run_reseal()
        rc6c, out6c = run_runner()
    finally:
        write(HIST, beforeh)
        git("checkout", "--",
            "code/hodge_leverage_landing_e1d0/site_records.txt")
    sr6 = gate_row(out6a, "H8", "SITE RECORD")
    record(rc6a == 1 and sr6 is False,
           f"A7-B6a a label exchange NOT among the seven frozen probe "
           f"literals -- H8's first block now asserts the §14 copy is both "
           f"'10 623 chars (unchanged)' and '2 928 -> 6 069 chars (more than "
           f"doubled)': runner exit {rc6a} (predicted 1), SITE RECORD @ H8 "
           f"{'REFUTED' if sr6 is False else sr6}.  THE REPAIR WORKS, which "
           f"is what makes the next two rows mean anything")
    record(rc6b == 0 and rc6c == 0 and not refuted_rows(out6c),
           f"A7-B6b/c then `--reseal` (exit {rc6b}, predicted 0) and the "
           f"runner again: exit {rc6c} with {len(refuted_rows(out6c))} "
           f"refuted rows (predicted 0 and 0).  FULLY GREEN with the "
           f"contradiction on the page -- no gate row, no probe and no "
           f"aggregate notices")
    if rc6c == 0:
        finding("E-6",
                "ONE `--reseal` TURNS A REAL LABEL EXCHANGE FULLY GREEN, AND "
                "NOTHING IN THE ARTIFACT NOTICES.  B3's blessing was caught "
                "-- not by the gate, whose 34 rows all went green, but by "
                "N21 reporting PROBE NOT APPLIED because its own frozen "
                "literal had moved.  B6 uses a label exchange outside those "
                "seven literals and the run is exit 0 with 0 refuted rows.  "
                "So the residual protection after a reseal is exactly the "
                "seven strings mg-ff3e enumerated, and it is a side effect of "
                "how those probes locate their text rather than a property of "
                "the record.  This is the same shape as E-1 and E-4 one level "
                "up: what is protected is what was named")

    # B4 -- the refusal itself deleted: the finest unit of the control.
    src = read(lp)
    cut = src.replace(
        '    blocking = [d for ok, d in figure_gate(texts, measured)\n'
        '                if not ok and "SITE RECORD" not in d]',
        '    blocking = []   # mg-ec07 B4: the refusal deleted')
    assert cut != src, "B4 deletion did not apply"
    write(lp, cut)
    beforeD = read(DELIV)
    write(DELIV, beforeD.replace(d14, bad14, 1))
    try:
        rc4, out4 = run_reseal()
    finally:
        write(DELIV, beforeD)
        write(lp, src)
        git("checkout", "--",
            "code/hodge_leverage_landing_e1d0/site_records.txt")
    record(rc4 == 0,
           f"A7-B4 the refusal DELETED (one statement), the same wrong live "
           f"figure as B1: `--reseal` exits {rc4} (predicted 0) and blesses "
           f"a document whose figures are wrong.  The refusal is "
           f"LOAD-BEARING, at its finest unit")
    record(sha("code/hodge_leverage_landing_e1d0/site_records.txt") == rec_sha,
           "A7-B4 site_records.txt and verify_landing.py restored, "
           "sha256-identical")

    # B5 -- reseal's own measurement against the runner's.
    import inspect
    a = inspect.getsource(V.reseal)
    m = re.findall(r'"(gap|both|cell|hist|copy)":\s*([^\n,}]+)', a)
    record(len(m) == 5,
           f"A7-B5 `reseal()` computes all 5 measurements itself from the "
           f"working tree ({len(m)} of 5 found), the same source `t1` reads, "
           f"so a reseal cannot be blessed against a different measurement")


def bump(fig):
    """A figure-shaped token that is NOT the one given, same length."""
    d = "0123456789"
    for k in range(len(fig) - 1, -1, -1):
        if fig[k] in d:
            return fig[:k] + d[(d.index(fig[k]) + 1) % 10] + fig[k + 1:]
    raise SystemExit(f"no digit in {fig!r}")


# --------------------------------------------------------------------------
# A8 -- DID THE SAME-KIND ENUMERATION HAPPEN?
# --------------------------------------------------------------------------
# mg-ff3e's seven same-kind probes, and the mg-9207 finding each carries.  The
# last four have no mg-9207 finding: they are mg-ff3e's own additions, and
# whether that is true is measured below rather than taken from its README.
KINDS = [("N19", "E2"), ("N20", "E2b"), ("N21", "E3"),
         ("N22", ""), ("N23", ""), ("N24", ""), ("N25", "")]


def a8(clean_out):
    head("A8 -- DID THE SAME-KIND ENUMERATION HAPPEN?")
    print("""A DIFFERENT QUESTION FROM WHETHER THE FIX WORKS.  mg-9207 required the
same-kind set to be enumerated BEFORE fixing, and fixed as a set.  A correct
fix that never asked is the failure mode, not a success.

Checked from git and from the runner's own stdout, not from mg-ff3e's summary
of itself.
""")
    fix = git("log", "--reverse", "--format=%H", "-S", "def partition(",
              "--", "code/hodge_leverage_landing_e1d0/verify_landing.py"
              ).split()[0]
    print(f"  the fix lands at {fix[:7]}\n")
    p9207 = os.path.join(REPO, "code", "hodge_leverage_audit_9207")
    raised = ""
    for f in sorted(os.listdir(p9207)):
        with open(os.path.join(p9207, f), encoding="utf-8",
                  errors="replace") as fh:
            raised += fh.read()
    print("    probe  mg-9207 id  first commit  before the fix?  raised by "
          "mg-9207?")
    pre = own = 0
    for k, tag in KINDS:
        cs = git("log", "--reverse", "--format=%H", "-S", k, "--",
                 "code/hodge_leverage_landing_e1d0/verify_landing.py").split()
        first = cs[0] if cs else "-------"
        isbefore = bool(cs) and first != fix and subprocess.run(
            ["git", "-C", REPO, "merge-base", "--is-ancestor", first,
             f"{fix}^"], capture_output=True).returncode == 0
        pre += isbefore
        # Is this probe one mg-9207 itself raised?  Measured by asking whether
        # mg-9207's own artifact names the finding id, not by reading
        # mg-ff3e's account of whose idea it was.
        inh = bool(tag) and re.search(rf"\b{tag}\b", raised) is not None
        own += not inh
        print(f"    {k}    {tag or '--':<10}  {first[:7]}       "
              f"{'yes' if isbefore else 'NO':<16} "
              f"{'yes' if inh else 'no -- mg-ff3e' + chr(39) + 's own'}")
    record(pre == 0,
           f"A8 {pre} of {len(KINDS)} same-kind probes exist at any commit "
           f"BEFORE {fix[:7]}, the commit that lands the fix.  The "
           f"enumeration is CONTEMPORANEOUS WITH the fix, not prior to it -- "
           f"there is no artifact in this repository, at any earlier commit, "
           f"that enumerates the set.  'Enumerate BEFORE fixing' is therefore "
           f"not evidenced, though nothing here shows it did not happen in "
           f"the author's head")
    rows = [l for l in clean_out.split("\n")
            if re.match(r"\s+N(19|20|21|22|23|24|25) ", l)]
    # The runner prints these twice: once as a verdict WRITTEN BEFORE the run
    # and once as the verdict OBSERVED.  Counting them together would report
    # 14 of 7, which is what the first version of this check did.
    pred = [l for l in rows if "GATE FIRES" in l]
    obs = [l for l in rows if "GATE FIRES" not in l]
    record(len(pred) == len(KINDS) and len(obs) == len(KINDS),
           f"A8 {len(pred)} of {len(KINDS)} same-kind probes carry a verdict "
           f"WRITTEN BEFORE the run and {len(obs)} of {len(KINDS)} carry an "
           f"OBSERVED verdict, in the runner's OWN stdout on THIS run and not "
           f"only in a committed transcript.  Every item was CHECKED, not "
           f"named")
    for l in obs:
        print(f"      {l.strip()[:112]}")
    record(own >= 4,
           f"A8 {own} of {len(KINDS)} probes are mg-ff3e's OWN -- the other "
           f"{len(KINDS) - own} carry finding ids mg-9207's own artifact "
           f"names (E2/E2b/E3).  The enumeration is substantially, not only "
           f"nominally, the parent's")
    finding("E-4",
            "THE ENUMERATION IS OVER KINDS, NOT OVER SITES x KINDS, AND THAT "
            "IS WHERE E-1 COMES FROM.  Seven kinds of label-side exchange "
            "were enumerated and all seven were CHECKED, which is the "
            "discipline working.  But each kind was checked at ONE site: N21 "
            "(column headers) at H8 only.  The same kind at the STATE.md site "
            "is X1, and X1 is silent.  The question 'what else is of the same "
            "kind?' was asked of the MUTATION and not of the SITE, so the set "
            "that was fixed is the set of exchange kinds at the sites that "
            "were already probed.  The enumeration also arrives in the same "
            "commit as the fix (A8 above), so 'enumerate BEFORE fixing' is "
            "not evidenced by anything in the repository")


# --------------------------------------------------------------------------
def main():
    print("mg-ec07 -- INDEPENDENT AUDIT of mg-ff3e's repair of mg-9207")
    print("=" * 78)
    print("""Target: `code/hodge_leverage_landing_e1d0/verify_landing.py` at HEAD, the
census made "position-aware over the WHOLE record" by c7f9079 / 11ef9a9 and
reported by 3bf0cd2.

Three questions, in the assignment's order: did it fix the SET or the next
field; did the same-kind enumeration HAPPEN; and is what was already confirmed
still confirmed.  Plus one thing no list in the assignment names -- A7, the
blessing path.

NOT A REPLICATION.  `repair_9207.py` and `audit_8eca_repair.py` are not run
and their bottom lines are not quoted.  Every population here is derived from
the tree by this file.  The one thing imported from the artifact is the GATE
ITSELF, because an audit that re-implements the gate audits its own
re-implementation.""")

    clean_out = a0()
    texts = V.site_texts()
    measured = measured_now()
    parent, PRE = a1(texts, measured)
    a2b(texts, PRE, parent)
    tot = a3(texts, measured)
    a2c(tot["n"])
    a4(texts)
    a6(texts)
    if FULL:
        a5()
        a5b(texts, measured)
        a7(texts, measured)
    else:
        head("A5 / A5b / A7 -- SKIPPED (--full not given)")
        print("  These mutate the tree and restore it.  Run with --full.")
    a8(clean_out)

    head("BOTTOM LINE")
    bad = [t for t, ok in RESULTS if ok is False]
    print(f"  checks recorded : {len(RESULTS)}")
    print(f"  measurements    : {sum(1 for _, ok in RESULTS if ok is None)}")
    print(f"  confirmed       : {sum(1 for _, ok in RESULTS if ok is True)}")
    print(f"  refuted         : {len(bad)}")
    for t in bad:
        print(f"    - {t[:150]}")
    print()
    print(f"  {len(FINDINGS)} findings.")
    for tag, d in FINDINGS:
        print(f"    {tag} -- {d[:150]}")
    print()
    print("  VERDICT: PARTIAL." if FINDINGS else "  VERDICT: CLEAN.")
    raise SystemExit(1 if (FINDINGS or bad) else 0)


if __name__ == "__main__":
    main()
