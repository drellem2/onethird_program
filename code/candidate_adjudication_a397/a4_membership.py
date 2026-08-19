#!/usr/bin/env python3
"""a4 — THE MEMBERSHIP CANDIDATES, ADJUDICATED.  EXPECT MOST TO BE FINE.

THE TICKET PUT THESE LAST AND SAID WHY: a membership test is not a defect, it is a
construction that CAN be one, and 202 reported as defects would be a count off a pattern
sieve.  So this arm reports a SPLIT, and `CANNOT TELL WITHOUT RUNNING` is one of its cells
rather than a rounding to clean.

TWO LAYERS, AND THEY ANSWER DIFFERENT QUESTIONS.

§1  ANATOMY (structural, complete, no run).  A parser is pointed at each of c9876's sites and
    asked what is actually there.  Three answers need no measurement at all:

      NOT-A-MEMBERSHIP-TEST  — the regex matched PROSE or a QUOTED EXAMPLE.  c9876's own
          `a4_sweep.py:208` is in the index because its docstring-adjacent control quotes
          `if "8 9" in out:` as a string, and this file's §4 quotes it again.  A count that
          includes them is a count of TEXT, which is the error the 597 -> 202 repair fixed
          one layer down; this is the residue of it.
      SECOND-LINE-OF  — the regex fires once per LINE, so a membership expression spread over
          two lines is two candidates and one construction.
      NOT-VERDICT-BEARING — the answer reaches a print and nothing else.  A diagnostic
          nobody branches on cannot certify anything, so it cannot launder a green.

§2  THE MEASUREMENT (what was the check's ANSWER on the healthy tree?).  mg-9876's own
    adopted guard is that A PROBE ALREADY SATISFIED BY THE GOOD INPUT IS UNFALSIFIABLE.  That
    is a property of the site's VALUE on the good world, and it is measurable directly: every
    membership expression in a directory is wrapped, in place, in a recorder; the directory's
    own runner is then run ONCE, unmutated; and the recorder says, per site, whether the test
    came back TRUE, FALSE, or was NEVER REACHED.

      BOTH-WAYS       — the site answered TRUE at one evaluation and FALSE at another inside
                        the SAME healthy run.  This is the strongest cell in the arm and it
                        costs nothing: the directory's own harness ran its subject two ways
                        and the site discriminated, demonstrated rather than inferred.
      ALWAYS-FALSE    — the needle was never present.  This is the shape a working
                        negative-control expectation has, and it CANNOT be instance 3, which
                        is a check satisfied by the good world.
      ALWAYS-TRUE     — satisfied at every evaluation.  For an arm whose job is to notice a
                        bad-world marker this is instance 3's shape; for one asserting a
                        healthy invariant it is the correct answer.  WHICH depends on the
                        arm's POLARITY, which is READ and not measured — and a site evaluated
                        exactly ONCE cannot be told apart from a correct predicate applied to
                        a harness's own planted world, so those are counted CANNOT-TELL.
      NEVER-REACHED   — the check did not execute on the healthy run.  A check nobody runs is
                        weaker than a check that cannot fail, and it is invisible to every
                        pattern sieve.
      NOT-REACHED-BY-a4 — the directory was not run: no runner, over budget, or the
                        instrumentation changed the run (see the guard below).

    THE INSTRUMENTATION HAS A GUARD, because a rewritten file that behaves differently would
    make this arm measure ITSELF.  Each directory is run twice: once untouched for a baseline
    exit code, once instrumented.  If the two disagree the directory is reported
    NOT-REACHED-BY-a4 with the reason, and nothing from it is counted.

§3  THE POSITIVE CONTROL IS THE KNOWN INSTANCE, PINNED BY BLOB SHA.  `"8 9" in out` at
    9efb3df:code/rendered_twin_pin_9bc2/negative_control.py:168 is a REAL laundered green
    that a real ticket found by hand.  It is fetched out of git by blob, not by path on a
    moving ref — mg-a71f's lesson — and run through this arm's own classifier, which must
    call it TRUE-ON-GOOD against that era's committed report.  The repaired line at HEAD must
    not be called the same thing.  A FIXTURE TAKEN FROM HISTORY SURVIVES ITS SUBJECT BEING
    REPAIRED, which is the question mg-188d D3 says to score; a fixture read out of the live
    tree would have died when c2f44 fixed it.
"""

import json
import shutil
import signal
import os
import re
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import liba397 as L  # noqa: E402

# TWO BUDGETS, AND BOTH ARE STATED BEFORE THE RUN RATHER THAN DISCOVERED AFTER IT.  The
# per-directory one bounds a single suite; the sweep one bounds the arm.  Directories are
# taken most-sites-first, so what a budget costs is the TAIL of the population and the tail
# is named in the transcript.  A sweep that silently stopped early would report `measured` of
# a population it never reached, which is the shape this whole line is correcting.
BUDGET_S = 45
SWEEP_BUDGET_S = 1500
REC_ENV = "A397_REC"

SITECUSTOMIZE = '''
import builtins, json, os
_p = os.environ.get("A397_REC")
def _rec(key, val):
    try:
        with open(_p, "a") as fh:
            fh.write(json.dumps([key, bool(val)]) + "\\n")
    except Exception:
        pass
    return val
builtins._a397R = _rec
'''


# ----------------------------------------------------------------------------------------
# §1 anatomy
# ----------------------------------------------------------------------------------------

def anatomy(sites):
    """Attach the parser's reading to every one of c9876's sites, and separate the ones the
    parser says are not membership tests at all from the ones it simply places elsewhere."""
    import ast
    cache, spans = {}, {}
    out = []
    for s in sites:
        path = os.path.join(L.ROOT, s["file"])
        if path not in spans:
            try:
                tree = ast.parse(L.read(path))
            except SyntaxError:
                spans[path] = {}
                cache[path] = {}
            else:
                sp = {}
                for n in ast.walk(tree):
                    if not isinstance(n, ast.Compare):
                        continue
                    for op, right in zip(n.ops, n.comparators):
                        if isinstance(op, (ast.In, ast.NotIn)) and \
                                L._basename(right) in L.HAYSTACKS:
                            for ln in range(n.lineno, (n.end_lineno or n.lineno) + 1):
                                sp.setdefault(ln, []).append(n)
                spans[path] = sp
                cache[path] = L.classify_file(path)
        rec = dict(s)
        c = L.classify_site(s, cache)
        rec.update(c)
        covering = spans[path].get(s["line"], [])
        if c["role"] != "unplaced":
            rec["anatomy"] = "SITE"
        elif covering:
            rec["anatomy"] = "SECOND-LINE-OF"
            rec["primary_line"] = min(n.lineno for n in covering)
        else:
            rec["anatomy"] = "NOT-A-MEMBERSHIP-TEST"
        out.append(rec)
    return out


def _spans_for_file(path):
    import ast
    try:
        tree = ast.parse(L.read(path))
    except SyntaxError:
        return []
    out = []
    for n in ast.walk(tree):
        if not isinstance(n, ast.Compare):
            continue
        for op, right in zip(n.ops, n.comparators):
            if isinstance(op, (ast.In, ast.NotIn)) and L._basename(right) in L.HAYSTACKS:
                out.append((n.lineno, n.col_offset, n.end_lineno, n.end_col_offset))
    return sorted(set(out))


# ----------------------------------------------------------------------------------------
# §2 the measurement
# ----------------------------------------------------------------------------------------

def instrument_text(text, spans, path_key):
    """Wrap each membership expression's exact source span in a recorder call.  A TEXT edit
    over the parser's own offsets, not an `ast.unparse` round trip: unparsing would rewrite
    every line of the file, and several instruments in this corpus READ THEIR OWN SOURCE."""
    lines = text.split("\n")
    for (l1, c1, l2, c2) in sorted(spans, reverse=True):
        key = f"{path_key}:{l1}:{c1}"
        if l1 == l2:
            ln = lines[l1 - 1]
            lines[l1 - 1] = (ln[:c1] + "_a397R(" + json.dumps(key) + ", (" +
                             ln[c1:c2] + "))" + ln[c2:])
        else:
            first, last = lines[l1 - 1], lines[l2 - 1]
            lines[l1 - 1] = first[:c1] + "_a397R(" + json.dumps(key) + ", (" + first[c1:]
            lines[l2 - 1] = last[:c2] + "))" + last[c2:]
    return "\n".join(lines)


def runner_for(dirname):
    p = os.path.join(L.CODE, dirname, "run_all.sh")
    return p if os.path.exists(p) else None


def run_dir(dirname, env=None, budget=BUDGET_S):
    """Same process-group kill as a2's `run()`, and for the same reason it is written there:
    killing `sh run_all.sh` leaves its producer alive and writing into the tree, so the next
    directory measured would be measuring the previous one's orphan."""
    r = runner_for(dirname)
    if not r:
        return None, 0.0, "no run_all.sh"
    e = dict(os.environ)
    e.update(env or {})
    t0 = time.time()
    proc = subprocess.Popen(["sh", r], cwd=L.ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, env=e,
                            start_new_session=True)
    try:
        proc.communicate(timeout=budget)
        return proc.returncode, round(time.time() - t0, 1), None
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except OSError:
            pass
        proc.wait()
        return None, round(time.time() - t0, 1), f"over {budget}s budget"


MINE = "candidate_adjudication_a397"


def restore_all():
    """Put every tracked file back, not just this directory's.  SOME SUITES IN THIS CORPUS
    WRITE OUTSIDE THEMSELVES — the ones that verify STATE.md, for instance — and a sweep that
    restored only the directory it was running would leave those edits behind and then blame
    the next directory for them.  Returns the paths that were written outside the directory
    under test, because that is worth knowing rather than merely undoing."""
    _rc, out, _e = L.git("status", "--porcelain")
    touched = []
    for ln in out.split("\n"):
        if not ln.strip() or MINE in ln:
            continue
        path = ln[3:].strip()
        if ln[:2].strip() in ("M", "D", "MM", "AM"):
            L.git("checkout", "--", path)
            touched.append(path)
    return touched


def measure_dir(dirname, files, sitedir):
    """-> (dict key->bool, note).  `files` are the .py paths in this directory holding sites."""
    base_rc, base_s, base_note = run_dir(dirname)
    outside = [p for p in restore_all() if not p.startswith(f"code/{dirname}/")]
    if outside:
        return {}, f"baseline WROTE OUTSIDE ITS DIRECTORY: {outside[:4]} — not counted"
    if base_note:
        return {}, f"baseline: {base_note}"

    originals = {f: L.read(f) for f in files}
    digests = {f: L.sha256(f) for f in files}
    recfile = tempfile.mktemp(prefix="a397_rec_", suffix=".jsonl")
    try:
        for f in files:
            sp = _spans_for_file(f)
            if not sp:
                continue
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(instrument_text(originals[f], sp, L.rel(f)))
        env = {REC_ENV: recfile,
               "PYTHONPATH": sitedir + os.pathsep + os.environ.get("PYTHONPATH", "")}
        rc, secs, note = run_dir(dirname, env)
    finally:
        for f, body in originals.items():
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(body)
        restore_all()
        bad = [L.rel(f) for f in files if L.sha256(f) != digests[f]]
    if bad:
        return {}, f"RESTORE FAILED: {bad}"
    if note:
        return {}, f"instrumented run: {note}"
    if rc != base_rc:
        return {}, (f"instrumentation changed the run (baseline exit {base_rc}, "
                    f"instrumented exit {rc}) — nothing counted")
    # EVERY EVALUATION IS KEPT, NOT OR-ed TOGETHER.  D6, kept: my first version folded the
    # values with `or`, so a site that answered TRUE once and FALSE ten times read as TRUE —
    # and the eleven "laundered" candidates it produced included four lambdas inside
    # `control_audit_9876/a2_discriminate.py`, which are predicates a two-way harness applies
    # to its own KNOWN-BAD world and which are SUPPOSED to be true there.  An aggregate that
    # cannot tell a bad-world evaluation from a good-world one reports a working negative
    # control as a laundered green, which is this ticket's error with the sign flipped.
    # Counting both ways instead makes the sharpest cell available: a site that answered BOTH
    # ways inside one healthy run has been DEMONSTRATED to discriminate, by the directory's
    # own harness, with no mutation of mine.
    seen = {}
    if os.path.exists(recfile):
        for ln in L.read(recfile).split("\n"):
            if not ln.strip():
                continue
            k, v = json.loads(ln)
            t, f = seen.get(k, (0, 0))
            seen[k] = (t + 1, f) if v else (t, f + 1)
        os.unlink(recfile)
    return seen, f"ok (baseline {base_s}s exit {base_rc}, instrumented {secs}s)"


# polarity: does the enclosing source treat a MATCH as the healthy answer or the bad one?
_BAD_MARKER = re.compile(r"(Traceback|FAIL|ERROR|REFUS|BROKEN|MISMATCH|WRONG|DEFECT|"
                         r"UNFALSIFIABLE|DRIFT|DISAGREE|HOLE)", re.I)


def polarity(rec):
    """POSITIVE = the site expects the needle PRESENT on a healthy run (an invariant).
    NEGATIVE = the site expects it ABSENT on a healthy run (a bad-world marker).
    Read off the needle and the negation, and reported as a READING — it is the one column
    here that a parser cannot settle, and it is exactly the class of question the ticket says
    stays a human reading."""
    if rec.get("needle_kind") != "literal" or rec.get("needle") is None:
        return "unknown"
    bad = bool(_BAD_MARKER.search(rec["needle"]))
    if rec.get("negated"):
        return "negative" if not bad else "positive"
    return "negative" if bad else "positive"


def main():
    print("=" * 92)
    print("mg-a397 a4 — THE MEMBERSHIP CANDIDATES, ADJUDICATED")
    print("=" * 92)
    print()

    sites = L.sites()
    recs = anatomy(sites)
    print(f"population: {len(sites)} candidate sites in "
          f"{len({s['dir'] for s in sites})} directories "
          f"(the ticket was filed on 202 in 66)")
    print()

    print("§1  ANATOMY — WHAT IS ACTUALLY AT EACH SITE")
    print("-" * 92)
    kinds = {}
    for r in recs:
        kinds[r["anatomy"]] = kinds.get(r["anatomy"], 0) + 1
    for k in sorted(kinds):
        print(f"    {k:24} {kinds[k]:4}")
    print()
    for k in ("NOT-A-MEMBERSHIP-TEST", "SECOND-LINE-OF"):
        rs = [r for r in recs if r["anatomy"] == k]
        if not rs:
            continue
        print(f"    {k} ({len(rs)}):")
        for r in rs:
            extra = f" (expression starts at line {r['primary_line']})" if \
                r.get("primary_line") else ""
            print(f"      {r['file']}:{r['line']}{extra}")
            print(f"          {r['src'].strip()[:82]}")
        print()

    real = [r for r in recs if r["anatomy"] == "SITE"]
    vb = [r for r in real if r["role"] in L.VERDICT_ROLES]
    nvb = [r for r in real if r["role"] not in L.VERDICT_ROLES]
    print(f"    of the {len(real)} real, distinct membership expressions:")
    print(f"      verdict-bearing      {len(vb):4}  (assert/branch/return/lambda/argument/"
          f"accumulated/used)")
    print(f"      NOT verdict-bearing  {len(nvb):4}  (the answer reaches a print and stops)")
    roles = {}
    for r in real:
        roles[r["role"]] = roles.get(r["role"], 0) + 1
    print("      by role: " + "  ".join(f"{k}={v}" for k, v in sorted(roles.items())))
    lits = [r for r in real if r["needle_kind"] == "literal"]
    print(f"      needle typed as a literal : {len(lits)}   derived from a value : "
          f"{len(real) - len(lits)}")
    print()

    print("§2  THE MEASUREMENT — WHAT DID EACH CHECK ANSWER ON THE HEALTHY TREE?")
    print("-" * 92)
    sitedir = tempfile.mkdtemp(prefix="a397_site_")
    with open(os.path.join(sitedir, "sitecustomize.py"), "w", encoding="utf-8") as fh:
        fh.write(SITECUSTOMIZE)
    bydir = {}
    for r in real:
        bydir.setdefault(r["dir"], set()).add(os.path.join(L.ROOT, r["file"]))
    mine = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    print(f"    budget: {BUDGET_S}s per directory, twice (baseline + instrumented).")
    print(f"    directories holding a real site: {len(bydir)}")
    print()
    values, notes = {}, {}
    order = sorted(bydir, key=lambda d: (-len([r for r in real if r["dir"] == d]), d))
    t0 = time.time()
    for d in order:
        if d == mine:
            notes[d] = "skipped: this arm's own directory — a4 running itself from inside"
            print(f"      {d:36} {notes[d]}")
            continue
        if time.time() - t0 > SWEEP_BUDGET_S:
            notes[d] = f"NOT RUN: the sweep's own {SWEEP_BUDGET_S}s budget was spent"
            continue
        seen, note = measure_dir(d, sorted(bydir[d]), sitedir)
        values.update(seen)
        notes[d] = note
        print(f"      {d:36} {note}")
    skipped = [d for d in order if notes.get(d, "").startswith("NOT RUN")]
    print()
    print(f"    reached {len(order) - len(skipped)} of {len(order)} directories in "
          f"{round(time.time() - t0)}s.")
    if skipped:
        print(f"    THE TAIL THE BUDGET COST, NAMED ({len(skipped)} directories, "
              f"{sum(1 for r in real if r['dir'] in skipped)} sites):")
        for i in range(0, len(skipped), 3):
            print("      " + "  ".join(n.ljust(34) for n in skipped[i:i + 3]))
    print()

    for r in real:
        key = None
        for k in values:
            f, l1, _c = k.rsplit(":", 2)
            if f == r["file"] and int(l1) == r["line"]:
                key = k
                break
        if key is not None:
            nt, nf = values[key]
            r["evals"] = (nt, nf)
            if nt and nf:
                r["answer"] = "BOTH-WAYS"
            elif nf:
                r["answer"] = "ALWAYS-FALSE"
            else:
                r["answer"] = "ALWAYS-TRUE"
        elif notes.get(r["dir"], "").startswith("ok"):
            r["answer"] = "NEVER-REACHED"
        else:
            r["answer"] = "NOT-REACHED-BY-a4"
    tally = {}
    for r in real:
        tally[r["answer"]] = tally.get(r["answer"], 0) + 1
    print("    " + "   ".join(f"{k}={v}" for k, v in sorted(tally.items())))
    print()

    print("§3  THE SPLIT THE TICKET ASKED FOR")
    print("-" * 92)
    laundered, discr, cannot, cant_launder = [], [], [], []
    for r in recs:
        if r["anatomy"] != "SITE":
            cant_launder.append((r, r["anatomy"]))
            continue
        if r["role"] not in L.VERDICT_ROLES:
            cant_launder.append((r, "answer reaches a print and stops"))
            continue
        pol = polarity(r)
        a = r.get("answer")
        if a == "BOTH-WAYS":
            # the sharpest cell in this arm: the site answered TRUE and FALSE inside ONE
            # healthy run, so the directory's own harness has already shown it discriminating
            # and no mutation of mine is needed to establish it.
            discr.append(r)
        elif a == "ALWAYS-FALSE":
            discr.append(r)
        elif a == "ALWAYS-TRUE" and pol == "negative" and sum(r.get("evals", (0, 0))) > 1:
            laundered.append(r)
        else:
            cannot.append(r)
    print(f"    CANNOT-LAUNDER-A-GREEN         {len(cant_launder):4}  structural, no run needed")
    print(f"    DISCRIMINATES                  {len(discr):4}  measured: answered the way a")
    print(f"                                         working check answers on a healthy tree")
    print(f"    LAUNDERED (candidate)          {len(laundered):4}  measured TRUE on the good")
    print(f"                                         world while naming a bad-world marker")
    print(f"    CANNOT-TELL-WITHOUT-RUNNING    {len(cannot):4}  NOT rounded to clean")
    print(f"                                   ----")
    print(f"                                   {len(recs):4}")
    print()
    if laundered:
        print("    THE LAUNDERED CANDIDATES, NAMED, WITH THEIR EVALUATION COUNTS:")
        for r in laundered:
            nt, nf = r.get("evals", (0, 0))
            print(f"      {r['file']}:{r['line']}  [{r['role']}]  "
                  f"true {nt}x / false {nf}x  needle={r['needle']!r}")
            print(f"          {r['src'].strip()[:82]}")
        print()
    both = [r for r in discr if r.get("answer") == "BOTH-WAYS"]
    print(f"    OF THE {len(discr)} `DISCRIMINATES`, {len(both)} ANSWERED BOTH WAYS INSIDE ONE")
    print("    HEALTHY RUN — the directory's own harness ran its subject two ways and the")
    print("    site answered differently.  That is a demonstration, not an inference, and it")
    print("    needed no mutation of mine.  The remaining ones answered FALSE every time,")
    print("    which is the weaker claim: the check is not ALREADY satisfied by the good")
    print("    world (mg-9876's own guard, and what kills instance 3) — it is NOT a")
    print("    demonstration that the check would fire.")
    print()
    print("    AND THE LIMITATION THAT PUTS A FLOOR UNDER `CANNOT-TELL`: this arm sees every")
    print("    evaluation the runner performs, including the ones a two-way harness makes")
    print("    against ITS OWN known-bad world.  A site evaluated exactly once, TRUE, may be")
    print("    a laundered green or may be a correct predicate applied to a planted world.")
    print("    Those are counted CANNOT-TELL and the evaluation counts are printed above so")
    print("    the distinction is visible rather than assumed.")
    print()
    print("    A NOTE ON `NEVER-REACHED`, WHICH IS THE CELL A PATTERN SIEVE CANNOT HAVE:")
    nr = [r for r in real if r.get("answer") == "NEVER-REACHED"]
    print(f"    {len(nr)} sites are in a directory whose own runner completed and did not")
    print("    execute them.  A check that does not run on the healthy tree has never been")
    print("    asked anything.")
    for r in nr[:15]:
        print(f"      {r['file']}:{r['line']}  {r['src'].strip()[:70]}")
    if len(nr) > 15:
        print(f"      … and {len(nr) - 15} more")
    print()

    print("§4  THE POSITIVE CONTROL — THE KNOWN INSTANCE, OUT OF GIT BY BLOB")
    print("-" * 92)
    ok = control_instance3()
    print()
    if not ok:
        print("    THE CONTROL DID NOT REPRODUCE.  §3's verdicts are WITHDRAWN.")
        return 2

    print("§5  THE TREE IS AS IT WAS — AND WHAT RUNNING 44 SUITES LEFT BEHIND")
    print("-" * 92)
    print("    D7, KEPT: the first version of this section counted `git status --porcelain`")
    print("    lines and called all of them `tracked files differing`.  Seven of them were")
    print("    `??` — UNTRACKED files that the suites this arm ran created in OTHER people's")
    print("    directories, which `git checkout --` cannot undo because git was never told")
    print("    about them.  A restoration check that reports untracked litter as a tracked")
    print("    modification is wrong in both directions: it fails a clean tree and it would")
    print("    have passed a dirty one had the litter been the only difference.  The two are")
    print("    now separated, and the litter is REMOVED rather than described.")
    print()
    _rc, out, _e = L.git("status", "--porcelain")
    lines = [ln for ln in out.split("\n")
             if ln.strip() and "candidate_adjudication_a397" not in ln]
    modified = [ln for ln in lines if not ln.startswith("??")]
    litter = [ln[3:].strip() for ln in lines if ln.startswith("??")]
    print(f"    tracked files still MODIFIED outside this directory: {len(modified)}  "
          f"(must be 0)")
    for ln in modified:
        print(f"      {ln}")
    print(f"    UNTRACKED files created by the suites this arm ran: {len(litter)}")
    removed = 0
    for p in litter:
        full = os.path.join(L.ROOT, p.rstrip("/"))
        try:
            if os.path.isdir(full):
                subprocess.run(["chmod", "-R", "u+rwx", full], capture_output=True)
                shutil.rmtree(full, ignore_errors=True)
            else:
                os.unlink(full)
            removed += 1
            print(f"      removed  {p}")
        except OSError as e:
            print(f"      COULD NOT REMOVE  {p}: {e}")
    print(f"    removed {removed} of {len(litter)}")
    if modified or removed < len(litter):
        return 2
    return 1 if laundered else 0


def control_instance3():
    """THREE SIDES, because a classifier that only ever says LAUNDERED has said nothing.

    (a) the known instance, out of git by blob, must come back TRUE-ON-GOOD;
    (b) the SAME needle against a report with the unconditional line removed must come back
        FALSE-ON-GOOD — otherwise (a) is a constant, not a measurement;
    (c) the repaired file at HEAD quotes the defect in its own docstring, and the anatomy
        layer must call that quotation NOT-A-MEMBERSHIP-TEST.  A sieve counts it as a site;
        this arm is required not to.
    """
    ok = True
    blob = "9efb3df:code/rendered_twin_pin_9bc2/negative_control.py"
    rc, src, err = L.git("show", blob)
    if rc != 0:
        print(f"    SETUP FAILED: {blob} unreadable: {err.strip()}")
        return False
    print("    (a) THE KNOWN INSTANCE, by blob and not by path on a moving ref")
    print(f"        {blob}:168")
    print(f"        {src.split(chr(10))[167].strip()[:80]}")
    rc, rep, _e = L.git("show", "9efb3df:code/rendered_twin_pin_9bc2/out_control.txt")
    if rc != 0:
        print("        SETUP FAILED: no baseline report committed at that commit")
        return False
    hits = [(i, ln) for i, ln in enumerate(rep.split("\n"), 1) if "8 9" in ln]
    print(f"        the UNMUTATED report committed in the same tree contains `8 9` "
          f"{len(hits)} times:")
    for i, ln in hits:
        print(f"          line {i}: {ln.strip()[:76]}")
    print(f"        -> answer on the GOOD world: "
          f"{'TRUE-ON-GOOD' if hits else 'FALSE-ON-GOOD'}  (want TRUE-ON-GOOD)")
    print("        the arm is NEGATIVE polarity — a positive control expecting a DRIFT")
    print("        worklist — so TRUE-ON-GOOD is mg-2f44's finding, re-measured.  The two")
    print("        occurrences are the whole defect: one is the worklist it meant, the")
    print("        other is section 1's row-set listing, printed on every healthy run.")
    ok = ok and bool(hits)

    print("    (b) THE SAME NEEDLE, AGAINST A REPORT WITHOUT THE UNCONDITIONAL LINE")
    stripped = "\n".join(ln for ln in rep.split("\n") if "row sets agree" not in ln
                         and "since the twin was last reconciled" not in ln)
    h2 = stripped.count("8 9")
    print(f"        occurrences: {h2} -> "
          f"{'TRUE-ON-GOOD' if h2 else 'FALSE-ON-GOOD'}  (want FALSE-ON-GOOD)")
    ok = ok and h2 == 0

    print("    (c) THE REPAIRED FILE AT HEAD QUOTES THE DEFECT — a sieve counts the quote")
    head = os.path.join(L.CODE, "rendered_twin_pin_9bc2", "negative_control.py")
    a4 = L.load_c9876()
    quoted = [(i, ln) for i, ln in enumerate(L.read(head).split("\n"), 1)
              if a4.SMELL_MEMBERSHIP.search(ln.strip())
              and not a4._FOR_BINDING.search(ln.strip())
              and '"8 9"' in ln]
    verdicts = []
    for i, _ln in quoted:
        r = anatomy([{"dir": "rendered_twin_pin_9bc2", "file": L.rel(head), "line": i,
                      "src": _ln}])[0]
        verdicts.append((i, r["anatomy"]))
        print(f"        line {i}: c9876's regex says CANDIDATE, this arm says {r['anatomy']}")
    ok = ok and bool(verdicts) and all(v == "NOT-A-MEMBERSHIP-TEST" for _i, v in verdicts)

    print("    THE FIXTURE IS A HISTORICAL BLOB, so it survives its own subject being")
    print("    repaired — the question mg-188d D3 says to score.  Read from the live tree")
    print("    it would have died at cdec2e8, when c9876 rewrote the line.")
    return ok


if __name__ == "__main__":
    sys.exit(main())
