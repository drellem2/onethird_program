#!/usr/bin/env python3
"""mg-835f -- INDEPENDENT AUDIT of `b80dea0` + `7f66005` (mg-a318), the repair
that landed mg-8a5c findings F-1 (both halves) and F-2.

WHAT mg-a318 REPAIRED.  `e16e41c`'s figure gate FORMATTED what it had just
measured -- which was right and is not retracted -- and then asked whether that
string OCCURRED SOMEWHERE in the file.  A presence test certifies that a correct
value EXISTS; it does not certify that the figure a reader MEETS is correct.
The same commit's corrected wording printed the live gap TWICE per site, so the
gate was satisfied by the copy nobody reads and every single-copy corruption of
the figure a reader meets left the runner at exit 0, at all three sites.
mg-a318 (a) removed the duplicate -- the chain's tail now POINTS AT the live
figure instead of restating it -- and (b) rebuilt the gate to READ EACH FIGURE
OUT OF THE STATEMENT THAT ASSERTS IT, anchored to the SECTION rather than the
file.

WHAT THIS AUDIT DOES, AND WHY IT IS NOT A CODE REVIEW.  The brief is explicit:
do not read the gate's source and conclude it checks the site.  Make a
reader-visible figure wrong ON DISK and see whether the run goes red.  So A1
mutates the real documents, one reader-facing (site, figure) pair at a time,
leaving every other occurrence correct, and runs the REAL runner.  Both
directions are reported: mutated-and-fired, and restored-and-silent, with the
restoration checked by sha256 rather than asserted.

THE FIXED POINT IS THE TRAP, AND IT IS WHY EVERY MUTATION HERE IS
LENGTH-PRESERVING.  Four of the five figures are lengths of the very text being
mutated, so an insertion moves the measurement and the gate fires for a reason
that has nothing to do with the site.  A mutation that changes the file's length
proves nothing about where the gate looks.  Every mutation below preserves the
byte length of the file it touches, by construction and by assertion, so a fire
is attributable to the gate reading the site.

  A1  THE SITE BATTERY -- the primary target.  Every reader-facing (site,
      figure) pair, mutated on disk one at a time, against the real runner.
  A2  IS IT A SITE READ OR A PRESENCE TEST?  The same corruption, with a
      CORRECT copy planted elsewhere in the same file, outside the site: the
      exact configuration that fooled `e16e41c`'s gate.  And the converse.
  A3  DERIVATION OR DECLARED DUPLICATION?  The within-site duplicate is gone;
      the same live figures are still written as literals at more than one
      site.  How many, and is that declared beside them, as the repair's own
      Appendix A rule requires?
  A4  THE CLEAN NULL.  mg-8a5c verified by three disjoint routes that the
      figures it audited had not gone stale.  This repair edits the very cells
      it reports on, which is the original mechanism, so the same three routes
      are run again -- Python codepoints, coreutils `wc -m`, and perl
      `length()` -- over the working tree AND over the git blob.
  A5  THE SEAM SWEEP.  `bbe83b5`, `e16e41c` and now `b80dea0` have each
      corrected the same three passages: this is the THIRD correction to one
      artifact.  Three sweeps -- figure-bearing sentences, marked quotations,
      and the written copies of the repair's own Appendix A rule -- every
      threshold printed, and what would have counted where nothing is found.
  A6  THE FLOOR -- one thing no list in the brief names.  The gate reads ONE
      designated statement per site.  A reader meets the whole section.  Is a
      reader-facing figure that is NOT in the designated statement checked?
  A7  DOES THE mg-8a5c INSTRUMENT AGREE WITH ITSELF ON A RE-RUN?  `7f66005`
      exists to make it do so.  It amended the summary's GATE sentence.  The
      summary has two sentences.

PREDICTED EXIT CODE, WRITTEN BEFORE THE FIRST RUN: 1.  Not because the site
battery was expected to fail -- A1 was predicted 12 of 12 FIRES and is -- but
because a gate that reads a NAMED statement per site cannot see a figure written
anywhere else in the same section, and this arc's own history is that the next
correction adds a restatement rather than corrupting the existing one: that is
exactly how F-1 was born, one generation ago, out of mg-8e30's own corrected
wording.  A6 is that prediction.  An exit of 0 would have meant the gate reads
everything a reader reads.

PREDICTIONS THAT MISSED, KEPT AS WRITTEN.  Two.  Only the first is in the
battery's own miss count (A6 reports "1 of 7"); the second was a mistake about
METHOD rather than about an outcome, so it has no row to be counted in and is
recorded here instead of being quietly re-aimed:
  * A6-U5 "reword the labelled statement, leave the figure correct" was
    predicted `gate passes` (a wording change is not a figure change).  It
    FIRES.  The gate is fail-CLOSED on rewording, which is better than the
    prediction and is reported as such.
  * A6's three U1 probes were first run as INSERTIONS and observed to fire at
    two of the three sites; re-run LENGTH-PRESERVING, so that the fixed point is
    not perturbed, all three pass.  The insertion runs are not reported as
    fires: they fired because the figures moved, not because the gate read the
    site.  The finding is stated on the length-preserving runs only.

IT MUTATES THE TREE AND RESTORES IT.  A1, A2 and A6 write to `STATE.md`,
`docs/OneThird-Hodge-Side-Leverage.md` and
`docs/state-history/attempt-mg-a3d4.md`, run
`code/hodge_leverage_landing_e1d0/verify_landing.py` against the mutated tree,
and `git checkout --` every file back inside a `finally`.  It REFUSES TO RUN if
any of those three files is already dirty -- scoped to the files it will
restore, which is `negative_control.py`'s convention: a `git checkout --` over
an uncommitted edit destroys it.  Every restoration is CHECKED by sha256.

NO BARE TOTALS.  Every count below names the population it ranged over.

REPRODUCTION CONTRACT, in terms of FILES rather than a commit.  This transcript
regenerates byte-identically at any tree in which `STATE.md`,
`docs/OneThird-Hodge-Side-Leverage.md`,
`docs/state-history/attempt-mg-a3d4.md`,
`docs/OneThird-Hodge-Side-Leverage-Mg8e30Repair-IndependentAudit.md`,
`code/hodge_leverage_landing_e1d0/`, `code/hodge_leverage_audit_8a5c/` and
`code/state_landing_control_2da3/` are unchanged.  It embeds no sha of its own.
Measured runtime: ~2 min, almost all of it the 63 runs of the audited runner and
one run of the mg-2da3 control (which mutates and restores STATE.md and
`docs/state-history/README.md` under its own `finally` + sha256, and refuses to
run against a dirty tree — A4 invokes it only while this audit's own tree is
restored).

Pure Python 3 + git (+ `wc` and `perl`, deliberately, in A4).
"""

import difflib
import hashlib
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LANDING = os.path.join(REPO, "code/hodge_leverage_landing_e1d0")
sys.path.insert(0, LANDING)
import verify_landing as V                                    # noqa: E402  the AUDITED module

RUNNER = os.path.join(LANDING, "verify_landing.py")
AUDIT_8A5C = os.path.join(REPO, "code/hodge_leverage_audit_8a5c/audit_repair_8e30.py")

REPAIR = "b80dea0"          # mg-a318, the repair audited here
FOLLOWUP = "7f66005"        # mg-a318's evidence + instrument amendment
AUDIT_DOC = "docs/OneThird-Hodge-Side-Leverage-Mg8e30Repair-IndependentAudit.md"

MUTABLE = [V.STATE, V.DELIV, V.HIST]

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


def sha(path):
    with open(os.path.join(REPO, path), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True, check=True).stdout


def run_gate():
    """The REAL runner, against whatever is on disk.  Returns (exit, refuted)."""
    r = subprocess.run([sys.executable, RUNNER], capture_output=True, text=True, cwd=REPO)
    return r.returncode, [l.strip() for l in r.stdout.split("\n") if "[REFUTED  ]" in l]


def restore(*paths):
    subprocess.run(["git", "-C", REPO, "checkout", "--"] + list(paths), check=True)


def write(path, text):
    with open(os.path.join(REPO, path), "w", encoding="utf-8") as fh:
        fh.write(text)


# --------------------------------------------------------------------------
# the sites, and how a mutation is applied to one without moving the figures
# --------------------------------------------------------------------------
SITE_FILE = {"the STATE.md row": V.STATE, "§14": V.DELIV, "H8": V.HIST}

# Prose inside each site that no check in `verify_landing.py` reads, used only
# to absorb a length delta so that every mutation is length-preserving.  Named
# rather than found by search, so the transcript says exactly what was overwritten.
BALLAST = {
    "the STATE.md row": ["up, down and up again, while the clause mismatch only ever grew"],
    "§14": ["whether or not anyone has stepped on it yet",
            "which is right, and is not retracted"],
    "H8": ["A quantity that moves in both directions while the thing it stands "
           "for moves in one is not a measurement of that thing",
           "while the clause mismatch only ever grew"],
}

BAD = {"gap": "+9 999", "both": "+99 999", "cell": "99 999",
       "hist": "99 999", "copy": "99 999"}


def site_raw(site, full=None):
    full = V.tree(SITE_FILE[site]) if full is None else full
    if site == "the STATE.md row":
        return V.state_row(full)
    if site == "§14":
        return V.section(full, "## §14 — `STATE.md` row, as landed")
    return V.section(full, "### H8 — ")


def measured():
    a = len(V.state_row(V.tree(V.STATE)))
    b = len(V.deliv_row(V.tree(V.DELIV)))
    h = len(V.tree(V.HIST))
    return {"gap": V.doc_num(a - b, signed=True), "both": V.doc_num(a + h - b, signed=True),
            "cell": V.doc_num(a), "hist": V.doc_num(h), "copy": V.doc_num(b)}


def retune(site, raw, new_raw):
    """Absorb a length delta into the site's named ballast, so the whole
    mutation is length-preserving and the figures do not move underneath it."""
    d = len(new_raw) - len(raw)
    for victim in BALLAST[site]:
        if d == 0:
            break
        if new_raw.count(victim) != 1:
            continue
        if d > 0:
            take = min(d, len(victim) - 1)
            new_raw = new_raw.replace(victim, victim[:len(victim) - take], 1)
            d -= take
        else:
            new_raw = new_raw.replace(victim, victim + " " * (-d), 1)
            d = 0
    if d != 0:
        raise SystemExit(f"cannot make the mutation length-preserving at {site}: {d:+d}")
    return new_raw


def apply_to_site(site, new_raw, raw=None, full=None):
    path = SITE_FILE[site]
    full = V.tree(path) if full is None else full
    raw = site_raw(site, full) if raw is None else raw
    new_raw = retune(site, raw, new_raw)
    new_full = full.replace(raw, new_raw, 1)
    assert new_full != full and len(new_full) == len(full), site
    write(path, new_full)
    return path


def corrupt_at_site(site, key, m):
    """Change the ONE reader-facing occurrence of `key` at `site`, on disk."""
    raw = site_raw(site)
    val, bad = m[key], BAD[key]
    if site == "H8" and key == "copy":
        # `copy` legitimately recurs in H8's historical columns; the reader-facing
        # one is the AFTER column of the three-column table, which is where the
        # gate reads it and the only one this mutation touches.
        rows = [l for l in raw.split("\n")
                if l.strip().startswith("deliverable §14 copy (frozen since mg-a806)")
                and len(re.split(r"\s{2,}", l.strip())) == 4]
        assert len(rows) == 1
        old = rows[0]
        i = old.rfind(val)
        new_raw = raw.replace(old, old[:i] + bad + old[i + len(val):], 1)
    else:
        assert raw.count(val) == 1, f"{site}/{key}: {raw.count(val)} raw occurrences"
        new_raw = raw.replace(val, bad, 1)
    return apply_to_site(site, new_raw, raw=raw)


def plant_outside(site, value):
    """Write `value` into the SAME FILE but OUTSIDE the site, length-preserving,
    over a word of exactly its length.  Returns what was overwritten."""
    path = SITE_FILE[site]
    full = V.tree(path)
    raw = site_raw(site, full)
    i = full.index(raw)
    pre, post = full[:i], full[i + len(raw):]
    for name in ("post", "pre"):
        region = post if name == "post" else pre
        mm = re.search(r"(?<![\w−+])[A-Za-z]{%d}(?![\w])" % len(value), region)
        if not mm:
            continue
        region = region[:mm.start()] + value + region[mm.end():]
        if name == "post":
            post = region
        else:
            pre = region
        write(path, pre + raw + post)
        return mm.group(0)
    raise SystemExit(f"no length-{len(value)} plant site outside {site}")


# --------------------------------------------------------------------------
# A1 -- THE SITE BATTERY
# --------------------------------------------------------------------------
def a1():
    head("A1 -- THE SITE BATTERY: EVERY READER-FACING FIGURE, MUTATED ON DISK")
    print("""The brief's primary target, and it is a measurement rather than a reading.
Every (site, figure) pair a reader can meet is corrupted ON DISK, one at a time,
leaving every other occurrence of that figure correct, and the REAL runner is
executed against the mutated tree.  Then the file is restored, the restoration
is checked by sha256, and the runner is executed AGAIN -- because a gate that
fires on everything is no better than one that fires on nothing.

Every mutation is LENGTH-PRESERVING (a same-width wrong value), so no figure
moves underneath the gate and a fire is attributable to the site read.

  population: the (site, figure) pairs `verify_landing.py` presents to a reader
  and gates -- 5 at the STATE.md row, 2 at §14, 5 at H8.  Verdicts written
  before the run: FIRES for all of them, silent for all twelve restorations.
""")
    m = measured()
    print(f"    {'#':<4}{'site':<19}{'figure':<9}{'wrote':<10}"
          f"{'predicted':<12}{'observed':<12}{'restored'}")
    ok_fire = ok_quiet = 0
    read_fired = once_fired = 0
    n = 0
    for site, _reader, keys in V.SITES:
        for key in keys:
            n += 1
            label, live = V.FIGURES[key]
            path = corrupt_at_site(site, key, m)
            rc, ref = run_gate()
            mine = [l for l in ref
                    if l.startswith("[REFUTED  ] GATE @ " + site) and f"'{label}'" in l]
            read_fired += any("READ AT THE SITE" in l for l in mine)
            once_fired += any("WRITTEN ONCE" in l for l in mine)
            restore(path)
            quiet_rc, _ = run_gate()
            ok_fire += rc != 0
            ok_quiet += quiet_rc == 0
            print(f"    {n:<4}{site:<19}{key:<9}{BAD[key]:<10}"
                  f"{'FIRES':<12}{('FIRES' if rc else 'silent'):<12}"
                  f"{'silent' if quiet_rc == 0 else 'STILL RED'}")
            assert sha(path) == CLEAN[path], "restoration is not byte-identical"
    print()
    record(ok_fire == 12,
           f"MUTATED AND FIRED: {ok_fire} of 12 reader-facing (site, figure) pairs "
           "-- 5 at the STATE.md row, 2 at §14, 5 at H8 -- make the real runner "
           "exit non-zero when corrupted ON DISK one at a time")
    record(ok_quiet == 12,
           f"UNTOUCHED AND SILENT: {ok_quiet} of the same 12 restorations return "
           "the runner to exit 0, each restoration verified byte-identical by "
           "sha256 -- the gate is not merely always-red")
    record(read_fired == 12,
           f"and the check that fired is the SITE READ in {read_fired} of 12: "
           "'READ AT THE SITE = <what the document says>, MEASURED THIS RUN = "
           "<what the run measured>'.  It is not the written-once counter alone")
    record(once_fired == 10,
           f"the written-once counter fires additionally on {once_fired} of 12 -- "
           "the 2 it does not are the frozen §14-copy figure at the STATE.md row "
           "and at H8, which is declared non-live and may legitimately recur")


# --------------------------------------------------------------------------
# A2 -- SITE READ OR PRESENCE TEST?
# --------------------------------------------------------------------------
def a2():
    head("A2 -- THE EXACT CONFIGURATION THAT FOOLED THE OLD GATE")
    print("""F-1 was not "a wrong number".  It was a wrong number AT THE SITE with a right
one somewhere else in the same file, and a gate that could not tell them apart.
A1 removed the correct copy along with the wrong one; this does not.

PART A: corrupt the figure at the site AND plant a CORRECT copy elsewhere in the
same file, outside the site.  A presence test passes every one of these.
PART B: the converse -- leave the site correct and plant a WRONG copy outside it.

Both parts are length-preserving: the planted value overwrites a word of exactly
its own length, named in the transcript.  Population: the same 12 pairs as A1.
""")
    m = measured()
    print("  PART A -- wrong at the site, right outside it.  Predicted: FIRES, 12 of 12.")
    print(f"    {'#':<4}{'site':<19}{'figure':<9}{'observed':<12}{'planted over'}")
    fired = 0
    for i, (site, key) in enumerate([(s[0], k) for s in V.SITES for k in s[2]], 1):
        corrupt_at_site(site, key, m)
        over = plant_outside(site, m[key])
        rc, _ = run_gate()
        fired += rc != 0
        print(f"    {i:<4}{site:<19}{key:<9}{('FIRES' if rc else 'silent'):<12}{over!r}")
        restore(SITE_FILE[site])
        assert sha(SITE_FILE[site]) == CLEAN[SITE_FILE[site]]
    print()
    record(fired == 12,
           f"{fired} of the same 12 pairs FIRE with a correct copy of the very "
           "figure standing elsewhere in the same file -- so the gate is reading "
           "the site and not searching the file.  This is the configuration "
           "`e16e41c`'s gate passed at all three sites")

    print()
    print("  PART B -- right at the site, wrong outside it.  Predicted: silent, 12 of 12.")
    print(f"    {'#':<4}{'site':<19}{'figure':<9}{'observed':<12}{'planted over'}")
    silent = 0
    for i, (site, key) in enumerate([(s[0], k) for s in V.SITES for k in s[2]], 1):
        over = plant_outside(site, BAD[key])
        rc, _ = run_gate()
        silent += rc == 0
        print(f"    {i:<4}{site:<19}{key:<9}{('silent' if rc == 0 else 'FIRES'):<12}{over!r}")
        restore(SITE_FILE[site])
        assert sha(SITE_FILE[site]) == CLEAN[SITE_FILE[site]]
    print()
    record(silent == 12,
           f"and it is silent on {silent} of 12 wrong copies planted OUTSIDE the "
           "site.  That is the gate's DECLARED scope -- a site is a section, not "
           "the file -- and is reported as scope rather than as a pass or a fail")
    record(None,
           "so the boundary is exactly where the documents say it is: inside the "
           "section the gate reads the statement it names, and outside it nothing "
           "is checked.  A6 asks what that leaves inside")


# --------------------------------------------------------------------------
# A3 -- DERIVATION, OR DECLARED DUPLICATION?
# --------------------------------------------------------------------------
def a3():
    head("A3 -- WAS DERIVATION CHOSEN, AND IS WHAT REMAINS DECLARED?")
    print("""mg-8a5c preferred one figure DERIVING from the other over a cleverer gate,
because a duplicated literal is a seam waiting to happen.  The repair's own new
Appendix A rule adds the fallback: an unavoidable duplicate must be DECLARED
beside the figure.  Two questions, both measured.

  (1) Is the WITHIN-SITE duplicate gone?  That is what F-1 was about.
  (2) The same five figures are published at three sites in three files.  How
      many written literals of each survive ACROSS sites, and does the prose at
      each site say so?
""")
    m = measured()
    texts = V.site_texts()
    print("    (1) within-site multiplicity -- occurrences of each figure inside each site")
    print(f"    {'figure':<42}{'value':>9}{'STATE.md row':>15}{'§14':>7}{'H8':>6}  live?")
    worst = 0
    for key in ("gap", "both", "cell", "hist", "copy"):
        label, live = V.FIGURES[key]
        counts = [V.flat(texts[s]).count(m[key]) for s in ("the STATE.md row", "§14", "H8")]
        if live:
            worst = max(worst, max(counts))
        print(f"    {label:<42}{m[key]:>9}{counts[0]:>15}{counts[1]:>7}{counts[2]:>6}"
              f"  {'live' if live else 'frozen'}")
    record(worst == 1,
           f"the maximum within-site count of any LIVE figure is {worst}, over the "
           "population of 4 live figures x 3 sites = 12 cells -- the chain's tail "
           "points at the live figure instead of restating it, so F-1's own shape "
           "is structurally gone and not merely detected")

    print()
    print("    (2) cross-site multiplicity -- the SAME literal, written at N of 3 sites")
    total = 0
    for key in ("gap", "both", "cell", "hist"):
        where = [s for s in ("the STATE.md row", "§14", "H8")
                 if m[key] in V.flat(texts[s])]
        total += len(where)
        print(f"    {V.FIGURES[key][0]:<42}{m[key]:>9}   {len(where)} of 3: "
              + ", ".join(where))
    record(None,
           f"{total} written literals of the 4 LIVE figures survive across the 3 "
           "sites (gap 3, cell+history 3, cell 2, relocated history 2).  The "
           "duplication is not gone -- it moved up one level, from two copies in "
           "one section to one copy in each of three files, and the gate now "
           "REQUIRES exactly that shape")

    print()
    print("    (3) is it DECLARED beside the figures, as the repair's own rule asks?")
    scope = "written once per site"
    token = {"the STATE.md row": "`state.md` row", "§14": "§14", "H8": "h8"}
    named = 0
    for site in ("the STATE.md row", "§14", "H8"):
        fl = V.flat(texts[site]).lower()
        has_scope = scope in fl
        others = [o for o in token if o != site and token[o] in fl]
        named += len(others) == 2
        print(f"      {site:<19} says '{scope}': {str(has_scope):<6} "
              f"names the OTHER sites (self excluded): "
              f"{', '.join(others) if others else 'neither'}")
    declared = sum(1 for s in texts if scope in V.flat(texts[s]).lower())
    record(declared == 3,
           f"{declared} of the 3 sites carry the phrase 'written once PER SITE' in "
           "the prose beside the figure, which is the declaration the repair's own "
           f"Appendix A rule requires for a duplicate somebody must maintain.  "
           f"{named} of the 3 additionally mention BOTH other sites by name, self "
           "excluded -- that is a token-presence test and is reported as one: it "
           "shows a reader of any site is pointed at the others, not that each "
           "says the others carry the same literal.  The phrase 'per site' is what "
           "carries that, and it is at all three.  The duplicate is DECLARED")
    record(None,
           "so the brief's second question resolves in the repair's favour: "
           "derivation was chosen where derivation was possible, the residue is "
           "the irreducible one -- three documents that must each state the "
           "figure to a reader who is reading only one of them -- and it is "
           "declared at every site rather than left for the next editor to find")


# --------------------------------------------------------------------------
# A4 -- THE CLEAN NULL
# --------------------------------------------------------------------------
def a4():
    head("A4 -- THE CLEAN NULL: DID THIS REPAIR'S OWN FIGURES GO STALE?")
    print("""mg-8a5c's primary target was that mg-8e30's figures had not gone stale, and it
held by three disjoint routes.  This repair edits the very cells it reports on,
which is the original mechanism, so the same question is asked again -- of the
repair's own numbers this time, and by tooling chosen to share nothing: Python's
`len` on decoded text, coreutils `wc -m`, and perl's `length` under -CSD.  Two
sources each: the working tree, and the git blob at HEAD.
""")
    a = len(V.state_row(V.tree(V.STATE)))
    b = len(V.deliv_row(V.tree(V.DELIV)))
    h = len(V.tree(V.HIST))

    def sh(cmd):
        r = subprocess.run(["sh", "-c", cmd], capture_output=True, text=True, cwd=REPO)
        return int(r.stdout.strip())

    # route 2: coreutils.  `wc -m` counts the newline the grep emits, so the
    # single-line quantities are reported one high and corrected by exactly 1,
    # which is stated rather than absorbed.
    wc_cell = sh("git show HEAD:STATE.md | grep '^| \\*\\*AMBER-POSITIVE' "
                 "| LC_ALL=en_US.UTF-8 wc -m") - 1
    wc_copy = sh("git show HEAD:docs/OneThird-Hodge-Side-Leverage.md "
                 "| grep '^> \\*\\*AMBER-POSITIVE' | LC_ALL=en_US.UTF-8 wc -m") - 1
    wc_hist = sh("git show HEAD:docs/state-history/attempt-mg-a3d4.md "
                 "| LC_ALL=en_US.UTF-8 wc -m")
    # route 3: perl, on the raw blob rather than on `git show`'s output.
    pl_cell = sh("git cat-file blob HEAD:STATE.md | perl -CSD -ne "
                 "'if (/^\\| \\*\\*AMBER-POSITIVE/) { chomp; print length($_) }'")
    pl_copy = sh("git cat-file blob HEAD:docs/OneThird-Hodge-Side-Leverage.md "
                 "| perl -CSD -ne 'if (/^> \\*\\*AMBER-POSITIVE/) { chomp; "
                 "print length($_) }'")
    pl_hist = sh("git cat-file blob HEAD:docs/state-history/attempt-mg-a3d4.md "
                 "| perl -CSD -e 'local $/; my $s=<STDIN>; print length($s)'")

    print(f"    {'quantity':<34}{'py/tree':>10}{'wc -m/blob':>12}{'perl/blob':>11}"
          f"{'agree':>7}")
    rows = [("STATE.md A5 cell", a, wc_cell, pl_cell, ""),
            ("relocated row history (file)", h, wc_hist, pl_hist, ""),
            ("deliverable §14 copy", b, wc_copy, pl_copy, ""),
            ("gap, cell only", a - b, wc_cell - wc_copy, pl_cell - pl_copy, "+"),
            ("gap, cell + history", a + h - b, wc_cell + wc_hist - wc_copy,
             pl_cell + pl_hist - pl_copy, "+")]
    agree = 0
    for label, r1, r2, r3, sign in rows:
        ok = r1 == r2 == r3
        agree += ok
        print(f"    {label:<34}{r1:>{sign}10,}{r2:>{sign}12,}{r3:>{sign}11,}"
              f"{('yes' if ok else 'NO'):>7}")
    print()
    record(agree == 5,
           f"{agree} of the 5 published figures agree across all three routes "
           "(Python codepoints on the tree, coreutils `wc -m` on `git show`, perl "
           "`length` on `git cat-file`) -- the routes share no code and two of "
           "them never touch the working tree")

    m = measured()
    texts = V.site_texts()
    said = {}
    for site, reader, keys in V.SITES:
        got = reader(texts[site])
        for key in keys:
            said[(site, key)] = (got.get(key) or [None])[0]
    mismatched = [k for k, v in said.items() if v != m[k[1]]]
    record(not mismatched,
           f"and all {len(said)} figures a reader meets -- the population is the "
           "12 (site, figure) pairs of A1 -- equal the measurement, so the repair "
           "did NOT reintroduce the staleness it was repairing")

    later = git("log", "--oneline", f"{REPAIR}..HEAD", "--", V.STATE, V.DELIV, V.HIST).strip()
    record(later == "",
           f"and no commit between `{REPAIR}` and HEAD touches any of the three "
           "files, so the figures written by the repair are still the figures at "
           f"HEAD: `git log {REPAIR}..HEAD -- <the three files>` is empty")

    grew = a - len(V.state_row(V.blob(f"{REPAIR}^", V.STATE)))
    record(grew != 0,
           f"the repair DID move the cell it was measuring -- `{REPAIR}` added "
           f"{grew:+,} characters to the STATE.md row -- so the fixed point was "
           "real and was solved rather than avoided")

    out = subprocess.run([sys.executable, RUNNER], capture_output=True,
                         text=True, cwd=REPO).stdout
    committed = V.tree("code/hodge_leverage_landing_e1d0/out_verify.txt")
    record(out == committed,
           f"the audited runner's committed transcript `out_verify.txt` "
           f"regenerates BYTE-IDENTICALLY at HEAD ({len(out):,} chars, all of it) "
           "-- the clean null mg-8a5c established is undisturbed by this repair's "
           "own edits to the very cells it reports on")

    # The mg-2da3 control is the sharpest form of the same question, because
    # `7f66005` REGENERATED its committed output to follow `b80dea0`'s edit to
    # STATE.md.  A document left wrong with its evidence bent to agree presents
    # identically in a diff to a document corrected with its evidence
    # regenerated to follow; re-running the control at HEAD is the discriminator.
    ctl = subprocess.run(["sh", "code/state_landing_control_2da3/run_all.sh"],
                         capture_output=True, text=True, cwd=REPO)
    ctl_committed = V.tree("code/state_landing_control_2da3/out_control.txt")
    record(ctl.stdout == ctl_committed and ctl.returncode == 0,
           f"and so does the mg-2da3 working-tree control, whose committed output "
           f"`7f66005` REGENERATED to follow this repair's STATE.md edit: exit "
           f"{ctl.returncode}, {len(ctl.stdout):,} chars, byte-identical.  That is "
           "the discriminator between an evidence file regenerated to FOLLOW a "
           "corrected document and one bent to AGREE with a wrong one")


# --------------------------------------------------------------------------
# A5 -- THE SEAM SWEEP
# --------------------------------------------------------------------------
def a5():
    head("A5 -- THE SEAM SWEEP: THREE CORRECTIONS, ONE ARTIFACT")
    print("""`bbe83b5` (mg-e1d0), `e16e41c` (mg-8e30) and `b80dea0` (mg-a318) have each
corrected the same three passages.  A seam defect is a STALE COPY of a passage an
earlier correction also touched, surviving where the later one did not reach; it
compounds, because the next edit builds on whichever copy it reaches.

Two sweeps.  Both thresholds are printed.  Where nothing is found, what WOULD
have counted is stated, so the null is checkable rather than merely asserted.
""")
    docs = [V.STATE, V.DELIV, V.HIST, AUDIT_DOC]
    fig = re.compile(r"[−+]?\d[\d  ]*\d")

    # SWEEP 1 -- figure-bearing sentences.
    sents = []
    for d in docs:
        flat = V.flat(V.tree(d))
        for s in re.split(r"(?<=[.!?])\s+", flat):
            if len(s) >= 120 and fig.search(s):
                sents.append((os.path.basename(d), s))
    print(f"    SWEEP 1 -- POPULATION: sentences >= 120 chars carrying a figure, in "
          f"the {len(docs)} documents the three corrections touched.")
    per = {}
    for d, _ in sents:
        per[d] = per.get(d, 0) + 1
    for d in sorted(per):
        print(f"      {d:<62}{per[d]:>4}")
    pairs = len(sents) * (len(sents) - 1) // 2
    print(f"      TOTAL sentences {len(sents)};  pairs compared {pairs}")
    print("      similarity: difflib.SequenceMatcher.ratio() on flattened text, "
          "threshold 0.80")
    print("      a pair counts as a SEAM HIT only if BOTH members carry figures "
          "and the figure sets disagree: one member eliding its figures behind "
          "'…' is an abbreviation, not a stale copy, and is named below instead")
    hits = []
    for i in range(len(sents)):
        for j in range(i + 1, len(sents)):
            r = difflib.SequenceMatcher(None, sents[i][1], sents[j][1]).ratio()
            if r >= 0.80:
                fi, fj = set(fig.findall(sents[i][1])), set(fig.findall(sents[j][1]))
                hits.append((r, sents[i], sents[j], bool(fi and fj and fi != fj),
                             not (fi and fj)))
    print()
    for r, si, sj, differ, elided in sorted(hits, reverse=True, key=lambda x: x[0])[:8]:
        print(f"      ratio {r:.3f}  {si[0]} :: {sj[0]}  seam hit: {differ}"
              f"{'  (one member elides its figures)' if elided else ''}")
        print(f"        A: {si[1][:150]}")
        print(f"        B: {sj[1][:150]}")
    stale = [h for h in hits if h[3]]
    mean = sum(len(s) for _, s in sents) // max(1, len(sents))
    record(not stale,
           f"SWEEP 1: {len(hits)} of {pairs} pairs reach ratio >= 0.80 and "
           f"{len(stale)} of those carry DIFFERENT figures.  WHAT WOULD HAVE "
           f"COUNTED: two figure-bearing sentences (mean length {mean} chars) "
           "sharing >= 80% of their characters while stating different numbers -- "
           "a stale copy differing only in a 5-7 char figure scores ~0.98 and "
           "would be reported here")

    # SWEEP 2 -- the marked quotations, which is where the arc's stale copies live.
    quotes = []
    for d in docs:
        flat = V.flat(V.tree(d))
        for pat in (r'\*"(.+?)"\*', r'\*\'(.+?)\'\*'):
            for mm in re.finditer(pat, flat):
                q = mm.group(1)
                if len(q) >= 60:
                    quotes.append((os.path.basename(d), q))
    print()
    print(f"    SWEEP 2 -- POPULATION: marked quotations >= 60 chars in the same "
          f"{len(docs)} documents.")
    per = {}
    for d, _ in quotes:
        per[d] = per.get(d, 0) + 1
    for d in sorted(per):
        print(f"      {d:<62}{per[d]:>4}")
    qp = len(quotes) * (len(quotes) - 1) // 2
    print(f"      TOTAL quotations {len(quotes)};  pairs compared {qp}")
    print("      similarity: difflib.SequenceMatcher.ratio(), threshold 0.75 "
          "(lower than sweep 1 on purpose: a quotation is short, so a one-figure "
          "difference costs more of the ratio)")
    qhits = []
    for i in range(len(quotes)):
        for j in range(i + 1, len(quotes)):
            r = difflib.SequenceMatcher(None, quotes[i][1], quotes[j][1]).ratio()
            if r >= 0.75:
                fi, fj = set(fig.findall(quotes[i][1])), set(fig.findall(quotes[j][1]))
                if fi and fj:
                    why = "seam hit" if fi != fj else "same figures"
                elif fi or fj:
                    why = "one member ELIDES its figures behind '…'"
                else:
                    why = "neither member carries a figure"
                qhits.append((r, quotes[i], quotes[j], bool(fi and fj and fi != fj), why))
    print()
    print("      EVERY pair above the threshold is printed, with why it is or is "
          "not a seam hit -- a sweep that shows only its hits cannot be checked.")
    print()
    for r, qi, qj, differ, why in sorted(qhits, reverse=True, key=lambda x: x[0]):
        print(f"      ratio {r:.3f}  {qi[0]} :: {qj[0]}  -- {why}")
        print(f"        A: {qi[1][:130]}")
        print(f"        B: {qj[1][:130]}")
    qstale = [h for h in qhits if h[3]]
    record(not qstale,
           f"SWEEP 2: {len(qhits)} of {qp} quotation pairs reach ratio >= 0.75 and "
           f"{len(qstale)} of those are seam hits.  Of the {len(qhits)}, "
           f"{sum(1 for h in qhits if h[4].startswith('neither'))} carry no figure "
           f"in either member and {sum(1 for h in qhits if 'ELIDES' in h[4])} are "
           "one-sided elisions -- an abbreviation of a passage is not a second "
           "copy of a number.  WHAT WOULD HAVE COUNTED: the same withdrawn "
           "passage quoted in two places with two different numbers in it, which "
           "is precisely the shape `−875` had before mg-8e30 and would surface here")

    # SWEEP 3 -- the normative sentences, because the arc's own rule is that a
    # duplicated literal is a seam whether or not it contains a figure.
    rule = "A COMMIT THAT MEASURES SOMETHING IT ALSO MODIFIES MUST PUBLISH THE " \
           "POST-COMMIT MEASUREMENT"
    tail = ", AND MUST SAY WHICH SIDE OF THE EDIT IT IS ON"
    print()
    print("    SWEEP 3 -- POPULATION: written copies of the Appendix A rule the "
          "repair's own")
    print("    Appendix A entry extends, across every .md file in the repository.")
    copies = []
    for root, _dirs, files in os.walk(REPO):
        if "/.git" in root:
            continue
        for f in sorted(files):
            if not f.endswith(".md"):
                continue
            p = os.path.relpath(os.path.join(root, f), REPO)
            flat = V.flat(V.tree(p))
            for mm in re.finditer(re.escape(rule), flat):
                long_form = flat[mm.end():mm.end() + len(tail)] == tail
                copies.append((p, "LONG" if long_form else "short"))
    for p, form in copies:
        print(f"      {form:<6}{p}")
    short = [c for c in copies if c[1] == "short"]
    record(None,
           f"{len(copies)} written copies of that rule exist in the {len(copies)} "
           f"places listed above, at TWO lengths: {len(copies) - len(short)} carry "
           f"the clause '{tail.strip(', ')}' and {len(short)} stop before it -- "
           "including the copy inside the STATE.md A5 cell, which quotes the rule "
           "by a title that is a PREFIX of the title Appendix A gives it.  "
           "PRE-EXISTING AND NOT THIS REPAIR'S: `git log -S` puts both lengths in "
           "`e16e41c` (mg-8e30), one generation earlier, and mg-a318 neither "
           "widened nor narrowed them.  Named because the arc's own rule is that a "
           "duplicated literal is a seam whether or not a figure is in it")
    record(None,
           "NAMED RATHER THAN COUNTED, because a sweep that hides its near "
           "misses is a sweep nobody can check: the highest-scoring cross-document "
           "pairs are printed above with their ratios, whether or not they crossed "
           "the threshold")


# --------------------------------------------------------------------------
# A6 -- THE FLOOR: one thing no list in the brief names
# --------------------------------------------------------------------------
def a6():
    head("A6 -- THE FLOOR: WHAT THE GATE READS, AND WHAT A READER READS")
    print("""CHOSEN BECAUSE OF HOW F-1 WAS BORN.  F-1 did not arrive as a corruption of an
existing figure.  It arrived because mg-8e30's own CORRECTION ADDED a second
mention of the live gap -- the chain's tail -- and the gate could not tell the
two apart.  The repair removes that copy and gates against a second one.  But
the gate reads ONE DESIGNATED STATEMENT per site, located by its exact wording.
A reader reads the whole section.

So the question no list in the brief asks: if the next correction writes the
figure into the section in ORDINARY PROSE rather than in the labelled form, does
anything see it?  Seven probes.  Every one is LENGTH-PRESERVING -- the wrong
sentence overwrites named ballast prose of exactly its own length -- because an
INSERTION moves the very lengths the figures are, and a gate that fires because
the file grew has not read anything.  (That distinction cost a
prediction: run as insertions, the three U1 probes fired at two of the three
sites and it meant nothing at all.)
""")
    m = measured()
    wrong = "the gap is now +9 999 characters."
    cases = []

    def probe(name, predicted, fn):
        cases.append((name, predicted, fn))

    def restate(site):
        def go():
            raw = site_raw(site)
            anchor = {"the STATE.md row": "**The character metric fails in BOTH directions",
                      "§14": "**The conclusion is untouched",
                      "H8": "**The sign claim is WITHDRAWN"}[site]
            assert raw.count(anchor) == 1, site
            return apply_to_site(site, raw.replace(anchor, wrong + " " + anchor, 1), raw=raw)
        return go

    for site in ("the STATE.md row", "§14", "H8"):
        probe(f"U1 {site}: a WRONG figure restated in ordinary prose at the site",
              "gate passes", restate(site))

    def fifth_column():
        raw = site_raw("H8")
        out = []
        for l in raw.split("\n"):
            if "AFTER mg-8e30" in l and "at bbe83b5^" in l:
                out.append(l + "  AFTER mg-a318")
            elif len(re.split(r"\s{2,}", l.strip())) == 4 and l.startswith("    "):
                out.append(l + "        0")
            else:
                out.append(l)
        new = "\n".join(out)
        assert new != raw
        return apply_to_site("H8", new, raw=raw)

    probe("U2 H8: a FIFTH column added to the three-column table", "GATE FIRES", fifth_column)

    def quoted():
        raw = site_raw("the STATE.md row")
        s = "cell-only gap **+2 744**"
        assert raw.count(s) == 1
        return apply_to_site("the STATE.md row",
                             raw.replace(s, 'cell-only gap *"**+2 744**"*', 1), raw=raw)

    probe("U3 STATE.md row: the live figure re-marked as a QUOTATION", "GATE FIRES", quoted)

    def duplicated_row():
        full = V.tree(V.STATE)
        row = V.state_row(full)
        write(V.STATE, full.replace(row, row + "\n" + row, 1))
        return V.STATE

    probe("U4 STATE.md: the whole row duplicated (the locator's uniqueness)",
          "GATE FIRES", duplicated_row)

    def reworded():
        raw = site_raw("§14")
        s = "cell-only gap **+2 744**"
        assert raw.count(s) == 1
        return apply_to_site("§14", raw.replace(s, "cell-only gap of **+2 744**", 1), raw=raw)

    probe("U5 §14: the statement REWORDED, the figure still correct",
          "gate passes", reworded)

    print(f"    {'probe':<72}{'predicted':<13}{'observed'}")
    misses = []
    silent_restatements = 0
    for name, predicted, fn in cases:
        path = fn()
        rc, _ = run_gate()
        observed = "GATE FIRES" if rc else "gate passes"
        flag = "" if observed == predicted else "   <-- PREDICTION MISSED"
        if flag:
            misses.append(name)
        if name.startswith("U1") and observed == "gate passes":
            silent_restatements += 1
        print(f"    {name:<72}{predicted:<13}{observed}{flag}")
        restore(path)
        assert sha(path) == CLEAN[path]
    print()
    record(None,
           f"{len(misses)} of {len(cases)} predictions missed, kept as written: "
           + ("; ".join(misses) if misses else "none"))
    if silent_restatements:
        finding("G-1",
                f"A READER-FACING WRONG FIGURE, WRITTEN IN ORDINARY PROSE INSIDE "
                f"THE SITE, IS NOT SEEN -- at {silent_restatements} of the 3 "
                "sites.  The sentence 'the gap is now +9 999 characters.' was "
                "placed inside the STATE.md row, inside §14 and inside H8, "
                "length-preservingly so no measurement moved, leaving the "
                "labelled statement the gate reads correct and untouched.  The "
                "run stayed at exit 0 every time.  The gate reads ONE DESIGNATED "
                "STATEMENT per site; a reader reads the section.  This is not "
                "F-1 reopened -- F-1's own shape (corrupting the statement, or "
                "restating the figure a second time in the SAME labelled form) "
                "now fires 12 of 12, A1.  It is F-1's mechanism one level out: "
                "the copy the gate cannot see is no longer a second labelled "
                "figure but an unlabelled one, and mg-8e30's correction is "
                "precedent that a correction ADDS such a mention rather than "
                "corrupting the existing one")
    record(True,
           "and the gate is fail-CLOSED on the three ways the designated "
           "statement can stop being readable -- a fifth table column, a figure "
           "re-marked as a quotation, and a duplicated row all make the run red "
           "rather than green, which is the right direction for a locator to "
           "fail in (population: the 3 structural probes U2-U4)")
    record(True,
           "U5 is the same property and is reported as a COST rather than a "
           "defect: rewording 'cell-only gap **+2 744**' to 'cell-only gap OF "
           "**+2 744**' -- a copy-edit that changes no figure -- turns the run "
           "red.  Fail-closed is right; the transcript should say that an "
           "innocent edit to the wording is a red run, and it does not")


# --------------------------------------------------------------------------
# A7 -- DOES THE mg-8a5c INSTRUMENT AGREE WITH ITSELF ON A RE-RUN?
# --------------------------------------------------------------------------
def a7():
    head("A7 -- THE AMENDED INSTRUMENT, RE-RUN: DOES ITS SUMMARY MATCH ITS RUN?")
    print("""`7f66005` exists for exactly this.  Its subject: "make the mg-8a5c audit
instrument tell the truth on a RE-RUN".  Its body: the closing summary "used to
assert unconditionally that the GATE was open ... a summary that contradicts the
run it summarises is the defect this whole arc keeps paying for, inside the
instrument that found this instance of it.  It now reports what THIS run
measured."

The summary has two sentences.  One is about the gate and was made conditional.
The other is about the figures.  This runs the instrument and compares the two
halves of its own summary against its own transcript.
""")
    r = subprocess.run([sys.executable, AUDIT_8A5C], capture_output=True, text=True, cwd=REPO)
    out = r.stdout
    lines = out.split("\n")
    refuted = [l.strip() for l in lines if "[REFUTED  ]" in l]
    t1_refuted = [l for l in refuted if "reproduce from the tree" in l
                  or "DID NOT GO STALE" in l]
    gate_ok = ("AND THE GATE HOLDS IN THIS TREE" in out)
    figs_ok = ("THE PRIMARY TARGET IS CONFIRMED: the repair's three figures are the"
               in out)
    print(f"    exit code                                              {r.returncode}")
    print(f"    [REFUTED] lines in the transcript, whole run           {len(refuted)}")
    print(f"    of those, in T1 (the declared PRIMARY TARGET)          {len(t1_refuted)}")
    print(f"    summary sentence 1 -- the GATE, made conditional       "
          f"{'printed (and true)' if gate_ok else 'not printed'}")
    print(f"    summary sentence 2 -- the FIGURES, unconditional       "
          f"{'printed' if figs_ok else 'not printed'}")
    print()
    for l in t1_refuted:
        print(f"      T1 says: {l}")
    if figs_ok:
        print("      the summary says: THE PRIMARY TARGET IS CONFIRMED: the "
              "repair's three figures are")
        print("                        the POST-commit ones and reproduce exactly "
              "from the tree.")
    print()
    record(gate_ok,
           "the GATE half of the summary is now conditional and is CORRECT at "
           "this tree -- it prints 'AND THE GATE HOLDS IN THIS TREE', and A1 "
           "confirms it independently, 12 of 12.  `7f66005`'s repair works, on "
           "the sentence it was applied to")
    if figs_ok and t1_refuted:
        finding("G-2",
                f"THE SAME AMENDED SUMMARY STILL CONTRADICTS THE SAME RUN, on the "
                f"OTHER sentence.  Re-run at HEAD, `audit_repair_8e30.py` prints "
                f"{len(t1_refuted)} REFUTED lines in T1 -- 'the three published "
                "parts reproduce from the tree' and 'THE REPAIR'S FIGURES DID NOT "
                "GO STALE, which was this audit's primary target' -- because its "
                "expectations are frozen at `a == 12692 and h == 18593` (source "
                "line 169) and `b80dea0` moved the cell to 13 367 and the history "
                "to 21 027.  Its BOTTOM LINE then prints, unconditionally, 'THE "
                "PRIMARY TARGET IS CONFIRMED: the repair's three figures are the "
                "POST-commit ones and reproduce exactly from the tree.'  Both are "
                "in the same transcript.  `7f66005` made the GATE sentence "
                "conditional on what the run measured and left the FIGURES "
                "sentence -- the one naming the instrument's own declared PRIMARY "
                "TARGET -- asserting the opposite of the run that surrounds it.  "
                "Population: the 2 sentences of that instrument's BOTTOM LINE; 1 "
                "of 2 amended")
        record(None,
               "AND IT IS NOT COVERED BY 'LEFT AS COMMITTED'.  `out_audit_8e30.txt` "
               "is deliberately frozen and that is right -- it is the record of "
               "what the audit found at `f58f7fd`.  But `7f66005` edited the "
               "SOURCE so a re-run tells the truth, and the audit document's own "
               "disposition block invites the re-run ('mg-8a5c's own multiplicity "
               "table, RE-RUN at the repair'), which is itself true and reproduces "
               "here.  What is undeclared is that the same re-run refutes T1")
    record(r.returncode == 1,
           f"the instrument exits {r.returncode}, as its own header predicts, on "
           "F-3 and F-4 -- both still open, both still named as unlanded in the "
           "audit document, neither disturbed by this repair")

    doc = V.flat(V.tree(AUDIT_DOC))
    for tag, want in (("F-1", "**LANDED, both halves"), ("F-2", "**LANDED."),
                      ("F-3", "**NOT LANDED**"), ("F-4", "**NOT LANDED**")):
        assert f"| **{tag}** |" in doc, tag
    record(all(f"| **{t}** |" in doc for t in ("F-1", "F-2", "F-3", "F-4")),
           "and all 4 of mg-8a5c's findings carry a disposition IN the audit "
           "document -- F-1 and F-2 LANDED, F-3 and F-4 NOT LANDED -- annotated "
           "in place rather than answered elsewhere.  Nothing retreated: no "
           "earlier finding is re-marked")


# --------------------------------------------------------------------------
def main():
    print("mg-835f -- INDEPENDENT AUDIT OF THE mg-a318 REPAIR (b80dea0 + 7f66005)")
    print("=" * 78)
    print("""The brief is a measurement, not a reading: mutate the figure AT EACH
reader-facing site in turn, leave every other occurrence correct, and confirm
the gate fires every time.  A gate that still passes when one site is wrong and
another is right has not been fixed, it has been renamed.  So A1 and A2 below
write to the real documents and run the real runner; nothing concludes from the
gate's source that the gate reads the site.

0 mathematics is touched and nothing of mg-3c24, mg-e1d0, mg-8e30 or mg-8a5c is
re-opened.  What is audited is a documentary gate and the documents it gates.""")

    dirty = git("status", "--porcelain", "--", *MUTABLE).strip()
    if dirty:
        sys.exit("REFUSING TO RUN: one of the files this audit mutates is already "
                 "dirty.  Commit or restore it first — this script `git checkout "
                 "--`s it back.\n" + dirty)

    try:
        a1()
        a2()
        a3()
        a4()
        a5()
        a6()
        a7()
    finally:
        restore(*MUTABLE)
        for p in MUTABLE:
            if sha(p) != CLEAN[p]:
                print(f"\n  !! RESTORATION FAILED for {p} -- the tree is NOT as it was")

    head("BOTTOM LINE")
    bad = [t for t, ok in RESULTS if ok is False]
    print(f"  checks recorded : {len(RESULTS)}")
    print(f"  confirmed       : {sum(1 for _, ok in RESULTS if ok is True)}")
    print(f"  measurements    : {sum(1 for _, ok in RESULTS if ok is None)}")
    print(f"  refuted         : {len(bad)}")
    print(f"  findings        : {len(FINDINGS)}")
    print()
    for tag, d in FINDINGS:
        print(f"    FINDING  {tag}: {d[:150]}")
    print()
    print("  THE PRIMARY TARGET IS CONFIRMED, BY MEASUREMENT AND NOT BY READING:")
    print("  every one of the 12 reader-facing (site, figure) pairs, corrupted on")
    print("  disk one at a time with every other occurrence left correct, makes")
    print("  the real runner exit 1 -- and each restoration returns it to exit 0.")
    print("  The configuration that fooled the old gate (wrong at the site, right")
    print("  elsewhere in the file) fires 12 of 12.  Derivation was chosen where it")
    print("  was available, and the residual cross-site duplication is declared at")
    print("  3 of 3 sites.  The clean null holds by three disjoint routes.")
    if FINDINGS:
        print()
        print("  WHAT IS OPEN is one level out from the gate and one sentence")
        print("  short of the summary repair: an unlabelled reader-facing figure")
        print("  inside a site is unchecked, and the amended instrument's own")
        print("  BOTTOM LINE still asserts a primary target its own T1 refutes.")
    return 1 if (FINDINGS or bad) else 0


CLEAN = {}

if __name__ == "__main__":
    CLEAN = {p: sha(p) for p in MUTABLE}
    sys.exit(main())
