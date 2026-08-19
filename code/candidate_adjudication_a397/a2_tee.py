#!/usr/bin/env python3
"""a2 — THE 19 `| tee` SITES, ADJUDICATED BY RUNNING EACH RUNNER TWO WAYS.

WHY THESE FIRST.  They are instance 1's exact construction and instance 1 was a real laundered
green: `cmd | tee f` makes `$?` TEE's status, tee succeeds whatever it is fed, and POSIX sh
has no PIPESTATUS.  Smallest population, highest prior — the ticket's order.

THE MEASUREMENT, AND WHY THE KNOWN-BAD IS THE ONE IT IS.  The property under test is exactly
one bit: DOES THIS RUNNER REPORT A FAILING ARM?  So the known-bad world differs from the
known-good world in exactly that bit and in nothing else.  The mutation appends

    import sys as _a397_sys; _a397_sys.exit(1)

to the END of the first tee'd producer.  The producer still runs, still computes, still prints
every byte it printed before; only its exit status changes.  A mutation that broke the
producer would confound "the runner cannot see a failing arm" with "the runner cannot see a
CRASHING arm", and those have different answers under `set -e`.

TWO ARMS, BECAUSE ONE OF THEM CANNOT REACH EVERY DIRECTORY.

  T1  THE REAL SUITE, BOTH WAYS.  The producers are the real ones and the runner is the real
      file.  This is the measurement.  It costs whatever the suite costs, and some of these
      suites cost minutes, so it carries a budget and reports TIMED-OUT as a first-class
      outcome — mg-a71f's lesson, in this arc, three days ago: a killed run is a statement
      about where the axe fell and not a verdict about the subject.

  T2  THE RUNNER WITH STUB PRODUCERS, BOTH WAYS.  A byte-identical copy of the runner in a
      scratch tree, with every producer replaced by a stub.  It answers for every directory
      including the ones T1 cannot afford, and it isolates the shell construction, which is
      where the bit lives.  IT IS THE WEAKER ARM AND IS LABELLED AS ONE: it cannot see a
      runner whose exit status depends on what a producer PRINTED.  Where T1 and T2 both
      answer, they are required to agree, and a disagreement is a finding against T2.

T2 HAS A TWO-SIDED CONTROL OF ITS OWN (§3), because a harness that only ever reports
LAUNDERED has not been shown to discriminate — which is mg-9876's §4 requirement and this
whole line's subject.  A synthetic runner using `> file` instead of `| tee` must come back
DISCRIMINATES, and a synthetic runner using `| tee` must come back LAUNDERED, in the same
run, printed side by side.

SCOPE.  Nothing outside this directory is edited.  The producers are mutated IN PLACE for the
length of one subprocess and restored under a checked sha256; every tracked file the runs
touch is restored with `git checkout --` and the worktree is required to be clean at the end
(§4).  If the restore ever fails, this arm says so and exits 2 rather than leaving the tree
dirty and the transcript green.
"""

import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import liba397 as L  # noqa: E402

MUTATION = "\n\n# mg-a397 known-bad: the arm FAILED.  Output byte-identical, status 1.\n" \
           "import sys as _a397_sys; _a397_sys.exit(1)\n"

# The budget for one T1 run.  MEASURED, not rounded: on this host `lstar_789d` was still
# inside `s1_hunt.py` after 10 minutes and `l2_conditionality_28ff` was still inside
# `b2_census.py` after 12, so covering them means 30-60 minutes PER DIRECTORY for the two
# runs T1 needs — and T1 needs both, because a non-zero on the known-bad world is only
# attributable if the good world came back zero.  300 s buys three of the five directories
# in full and names the other two as TIMED-OUT, which is a first-class outcome here for
# mg-a71f's reason: a kill is a statement about where the axe fell.  T2 answers all five.
T1_BUDGET_S = 300

STUB_GOOD = "import sys\nprint('a397 stub: arm ran, arm is fine')\nsys.exit(0)\n"
STUB_BAD = "import sys\nprint('a397 stub: arm ran, arm FAILED')\nsys.exit(1)\n"


# ----------------------------------------------------------------------------------------
# reading the runner
# ----------------------------------------------------------------------------------------

_TEE_CMD = re.compile(r"^(?P<cmd>.*?)\|\s*tee\b")
_PY = re.compile(r"([A-Za-z0-9_./$\"{}]*?([A-Za-z0-9_]+\.py))")


def producer_of(line):
    """The .py basename on the left of the pipe, or None (e.g. `echo ... | tee -a`)."""
    m = _TEE_CMD.match(line.strip())
    if not m:
        return None
    hits = _PY.findall(m.group("cmd"))
    return hits[0][1] if hits else None


def interpreter(runner_path):
    first = L.read(runner_path).split("\n", 1)[0]
    return "bash" if "bash" in first else "sh"


def runners():
    """{dirname: {"path": runner, "tee_lines": [(lineno, src, producer_basename)]}}"""
    out = {}
    for s in L.tee_sites():
        d = out.setdefault(s["dir"], {"path": os.path.join(L.ROOT, s["file"]),
                                      "tee_lines": []})
        d["tee_lines"].append((s["line"], s["src"], producer_of(s["src"])))
    return out


def find_producer(dirname, basename):
    for root, _dn, fns in os.walk(os.path.join(L.CODE, dirname)):
        if basename in fns:
            return os.path.join(root, basename)
    return None


def run(cmd, cwd, budget):
    """Run a runner under a budget, and KILL THE WHOLE PROCESS GROUP when the budget is spent.

    D1, KEPT: my first version was `subprocess.run(..., timeout=budget)`.  That kills the
    direct child — `sh run_all.sh` — and NOTHING ELSE.  The producer it had launched
    (`python3 -u b2_census.py | tee out_b2_census.txt`) is a different process, survives, and
    goes on writing tracked transcripts into the tree for as long as it likes.  I watched it
    do exactly that: `out_b2_census.txt` was still being modified after this arm had moved on
    to the next directory, so a later measurement would have been contaminated by an earlier
    directory's orphan and the worktree would have been left dirty by a run whose own §4 says
    it is clean.  This is mg-a71f's finding — a killed run is not a verdict, and a kill that
    does not land is not even a kill — committed inside the arm whose subject is what a runner
    does with a status it cannot see.  `start_new_session=True` + `killpg` is that ticket's
    own repair, adopted rather than re-invented (`t2_census.py:128`).
    """
    t0 = time.time()
    proc = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, start_new_session=True)
    try:
        proc.communicate(timeout=budget)
        return proc.returncode, round(time.time() - t0, 1), False
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except OSError:
            pass
        proc.wait()
        return None, round(time.time() - t0, 1), True


def restore(dirname):
    L.git("checkout", "--", os.path.join("code", dirname))


# ----------------------------------------------------------------------------------------
# T1 — the real suite, both ways
# ----------------------------------------------------------------------------------------

def t1(dirname, info):
    runner = info["path"]
    lineno, src, base = next(((a, b, c) for a, b, c in info["tee_lines"] if c), (None,) * 3)
    if not base:
        return {"verdict": "NO-PRODUCER", "detail": "no .py on the left of any pipe"}
    prod = find_producer(dirname, base)
    if not prod:
        return {"verdict": "NO-PRODUCER", "detail": f"{base} not found under code/{dirname}"}

    sh = interpreter(runner)
    rc_good, secs_good, to_good = run([sh, runner], L.ROOT, T1_BUDGET_S)
    restore(dirname)
    if to_good:
        return {"verdict": "TIMED-OUT", "detail":
                f"the unmutated suite did not finish in {T1_BUDGET_S}s ({secs_good}s spent); "
                f"a kill is not a verdict, so this directory is UNMEASURED by T1",
                "secs_good": secs_good}
    if rc_good != 0:
        return {"verdict": "RED-ON-ARRIVAL", "detail":
                f"the unmutated suite exits {rc_good}, so a non-zero on the known-bad world "
                f"would not be attributable to the mutation", "secs_good": secs_good}

    before = L.sha256(prod)
    original = L.read(prod)
    try:
        with open(prod, "a", encoding="utf-8") as fh:
            fh.write(MUTATION)
        rc_bad, secs_bad, to_bad = run([sh, runner], L.ROOT, T1_BUDGET_S)
    finally:
        with open(prod, "w", encoding="utf-8") as fh:
            fh.write(original)
        restore(dirname)
        after = L.sha256(prod)
    if after != before:
        return {"verdict": "BROKEN", "detail":
                f"RESTORE FAILED for {L.rel(prod)}: {before} -> {after}"}
    if to_bad:
        return {"verdict": "TIMED-OUT", "detail":
                f"the mutated suite did not finish in {T1_BUDGET_S}s", "secs_good": secs_good}
    return {"verdict": "LAUNDERED" if rc_bad == 0 else "DISCRIMINATES",
            "detail": f"{sh} {L.rel(runner)}: good exit {rc_good} ({secs_good}s), "
                      f"known-bad exit {rc_bad} ({secs_bad}s); mutated {base}",
            "rc_good": rc_good, "rc_bad": rc_bad,
            "secs_good": secs_good, "secs_bad": secs_bad}


# ----------------------------------------------------------------------------------------
# T2 — the byte-identical runner over stub producers
# ----------------------------------------------------------------------------------------

def t2_on_text(runner_text, runner_name, producer_names, bad_producer, sh, dirname="the_dir"):
    """Build a scratch tree holding the runner verbatim and one stub per producer, run it,
    return the exit code.  `git init` is done because one of these runners resolves its own
    working directory with `git rev-parse --show-toplevel` — a runner that navigates by git
    is a fact about the runner and is preserved rather than edited around."""
    tmp = tempfile.mkdtemp(prefix="a397_t2_")
    try:
        subprocess.run(["git", "init", "-q"], cwd=tmp, capture_output=True)
        # producers are referenced by paths relative to the runner's own cd; the safest
        # scratch layout is the one that satisfies BOTH `cd $(dirname $0)` and a
        # `code/<dir>/x.py` path from a repository root, so we plant each stub twice.
        here = os.path.join(tmp, "code", dirname)
        os.makedirs(here, exist_ok=True)
        for name in producer_names:
            body = STUB_BAD if name == bad_producer else STUB_GOOD
            for target in (os.path.join(tmp, name), os.path.join(here, name)):
                os.makedirs(os.path.dirname(target), exist_ok=True)
                with open(target, "w", encoding="utf-8") as fh:
                    fh.write(body)
        rp = os.path.join(here, runner_name)
        with open(rp, "w", encoding="utf-8") as fh:
            fh.write(runner_text)
        p = subprocess.run([sh, rp], cwd=tmp, capture_output=True, text=True, timeout=120)
        return p.returncode, p.stdout + p.stderr
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def rewrite_producer_paths(text, names):
    """Point every producer reference at a bare basename, so the scratch layout above
    resolves it.  THE PIPE, THE REDIRECTION, `set -e`, PIPESTATUS AND THE EXIT LINE ARE NOT
    TOUCHED — those are the construction under test and rewriting them would make T2 a test
    of this function."""
    for n in names:
        text = re.sub(r'"?[^\s"|]*' + re.escape(n) + r'"?', n, text)
    return text


def t2(dirname, info):
    runner = info["path"]
    names = [c for _a, _b, c in info["tee_lines"] if c]
    if not names:
        return {"verdict": "NO-PRODUCER", "detail": "no .py on the left of any pipe"}
    text = rewrite_producer_paths(L.read(runner), names)
    sh = interpreter(runner)
    rc_good, out_good = t2_on_text(text, os.path.basename(runner), names, None, sh, dirname)
    rc_bad, out_bad = t2_on_text(text, os.path.basename(runner), names, names[0], sh, dirname)
    if rc_good != 0:
        return {"verdict": "SETUP-FAILED", "detail":
                f"the all-good stub world exits {rc_good}; T2 cannot attribute a non-zero. "
                f"tail: {out_good.strip().splitlines()[-1:] }"}
    return {"verdict": "LAUNDERED" if rc_bad == 0 else "DISCRIMINATES",
            "detail": f"{sh}, stubs: all-good exit {rc_good}, "
                      f"{names[0]} exiting 1 -> runner exit {rc_bad}",
            "rc_good": rc_good, "rc_bad": rc_bad}


# ----------------------------------------------------------------------------------------
# who reads these exit codes?
# ----------------------------------------------------------------------------------------

_READS_STATUS = re.compile(r"(\.returncode|proc\.wait\(|\brc\b|\$\?|failed:%d)")


def _launch_calls(path):
    """Real `subprocess.run/Popen(["sh", "run_all.sh"], ...)` CALLS, by parser.

    D2, KEPT, AND IT IS THIS TICKET'S OWN SUBJECT: my first version grepped for the string
    `run_all.sh` plus a `for` loop and listed 30-odd "consumers", three of them README.md
    files and one a committed transcript.  My second version required a status read too, and
    still listed `census_remainder_f8e5/d5_timeout.py:87` — which is the string
    `'subprocess.Popen(["sh", "run_all.sh"]'` INSIDE A MEMBERSHIP TEST, i.e. one of the 209
    candidates this very directory is adjudicating, counted as a consumer by the arm doing
    the adjudicating.  A detector for `who reads this exit code` that answers `everyone who
    types the words` is mg-9876's 597 one layer up.  Only a parsed Call counts now."""
    import ast
    try:
        tree = ast.parse(L.read(os.path.join(L.ROOT, path)))
    except (SyntaxError, UnicodeDecodeError):
        return []
    out = []
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        fn = getattr(n.func, "attr", None)
        if fn not in ("run", "Popen") or not n.args:
            continue
        a0 = n.args[0]
        if not isinstance(a0, ast.List) or len(a0.elts) < 2:
            continue
        vals = [e.value for e in a0.elts[:2] if isinstance(e, ast.Constant)]
        if vals[:2] != ["sh", "run_all.sh"]:
            continue
        cwd = None
        for kw in n.keywords:
            if kw.arg == "cwd":
                cwd = kw.value
        fixed = isinstance(cwd, ast.Constant)
        out.append((n.lineno, "cwd is a literal path" if fixed
                    else "cwd is not a literal — a population, or a module constant"))
    return out


def consumers(dirname):
    """A laundered exit code with no reader is a construction; with a reader it is a live
    defect.  Both are reported, because the second is what makes the first worth repairing."""
    found = []
    build = os.path.join(L.ROOT, "build.sh")
    if os.path.exists(build) and f"code/{dirname}/run_all.sh" in L.read(build):
        found.append("build.sh — the merge gate (mg-724a) names this runner")
    _rc, out, _e = L.git("grep", "-l", "-e", "run_all.sh", "--", "code/")
    for f in sorted(set(out.split())):
        if f.startswith(f"code/{dirname}/") or not f.endswith(".py"):
            continue
        body = L.read(os.path.join(L.ROOT, f))
        if not _READS_STATUS.search(body):
            continue
        for lineno, how in _launch_calls(f):
            src = body.split("\n")[lineno - 1].strip()
            found.append(f"{f}:{lineno}  ({how})  {src[:56]}")
    return sorted(set(found))


def main():
    print("=" * 92)
    print("mg-a397 a2 — THE `| tee` SITES, ADJUDICATED BY RUNNING THEM TWO WAYS")
    print("=" * 92)
    print()

    rs = runners()
    tee = L.tee_sites()
    print(f"population: {len(tee)} tee sites in {len(rs)} directories "
          f"(the ticket was filed on 18 in 4)")
    print()

    print("§1  THE SITES, AND THE PRODUCER EACH ONE PIPES")
    print("-" * 92)
    for d in sorted(rs):
        print(f"    {d}")
        for lineno, src, base in rs[d]["tee_lines"]:
            print(f"        {L.rel(rs[d]['path'])}:{lineno}  {src[:78]}")
            print(f"            producer: {base or '(none — nothing to fail)'}")
    print()

    print("§2  THE TWO-WAY RUNS")
    print("-" * 92)
    print(f"    T1 budget per run: {T1_BUDGET_S}s.  T2 is the runner verbatim over stubs.")
    print()
    results = {}
    for d in sorted(rs):
        r1 = t1(d, rs[d])
        r2 = t2(d, rs[d])
        results[d] = (r1, r2)
        print(f"    {d}")
        print(f"        T1 (real suite)  {r1['verdict']:16}  {r1['detail']}")
        print(f"        T2 (stub arms)   {r2['verdict']:16}  {r2['detail']}")
        agree = (r1["verdict"] == r2["verdict"]) if r1["verdict"] in ("LAUNDERED",
                                                                     "DISCRIMINATES") else None
        if agree is False:
            print(f"        !! T1 AND T2 DISAGREE — that is a finding against T2, which is")
            print(f"           the weaker arm.  T1's answer stands.")
        elif agree:
            print(f"        both arms agree")
        else:
            print(f"        T1 did not reach a scorable answer; T2's answer is what this")
            print(f"        directory has, and it is the weaker of the two.")
        for c in consumers(d):
            print(f"        consumer: {c}")
        if not consumers(d):
            print(f"        consumer: none found")
        print()

    print("§3  T2's OWN TWO-SIDED CONTROL")
    print("-" * 92)
    print("    A harness that only ever answers LAUNDERED has not been shown to discriminate.")
    print("    Two synthetic runners, identical but for the construction under test:")
    print()
    synth = [("`| tee` under set -e",
              "#!/bin/sh\nset -e\ncd \"$(dirname \"$0\")\"\npython3 p.py | tee o.txt\n",
              "LAUNDERED"),
             ("`> file` under set -e",
              "#!/bin/sh\nset -e\ncd \"$(dirname \"$0\")\"\npython3 p.py > o.txt\n",
              "DISCRIMINATES"),
             ("`| tee` with PIPESTATUS, as state_restructure_ea0e writes it",
              "#!/bin/bash\nset -uo pipefail\ncd \"$(dirname \"$0\")\"\n"
              "python3 p.py | tee o.txt\nrc=${PIPESTATUS[0]}\nexit \"$rc\"\n",
              "DISCRIMINATES")]
    ok = True
    for label, text, want in synth:
        sh = interpreter_text(text)
        rc_g, _ = t2_on_text(text, "run_all.sh", ["p.py"], None, sh)
        rc_b, _ = t2_on_text(text, "run_all.sh", ["p.py"], "p.py", sh)
        got = "LAUNDERED" if rc_b == 0 else "DISCRIMINATES"
        mark = "ok " if (got == want and rc_g == 0) else "BROKEN"
        ok = ok and mark == "ok "
        print(f"      {mark}  {label:58} good={rc_g} bad={rc_b} -> {got} (want {want})")
    print()
    if not ok:
        print("    T2's control did not answer both ways.  Its verdicts above are WITHDRAWN.")
    print()

    print("§4  THE TREE IS AS IT WAS")
    print("-" * 92)
    rc, out, _ = L.git("status", "--porcelain")
    dirty = [ln for ln in out.split("\n")
             if ln.strip() and "candidate_adjudication_a397" not in ln]
    print(f"    tracked files differing outside this directory: {len(dirty)}")
    for ln in dirty:
        print(f"      {ln}")
    print()

    print("§5  VERDICT")
    print("-" * 92)
    laundered = [d for d, (r1, r2) in results.items()
                 if (r1["verdict"] if r1["verdict"] in ("LAUNDERED", "DISCRIMINATES")
                     else r2["verdict"]) == "LAUNDERED"]
    discr = [d for d, (r1, r2) in results.items()
             if (r1["verdict"] if r1["verdict"] in ("LAUNDERED", "DISCRIMINATES")
                 else r2["verdict"]) == "DISCRIMINATES"]
    n_sites_l = sum(len(rs[d]["tee_lines"]) for d in laundered)
    n_sites_d = sum(len(rs[d]["tee_lines"]) for d in discr)
    print(f"    LAUNDERED      {len(laundered)} directories, {n_sites_l} sites: "
          f"{', '.join(sorted(laundered))}")
    print(f"    DISCRIMINATES  {len(discr)} directories, {n_sites_d} sites: "
          f"{', '.join(sorted(discr))}")
    print(f"    T1-UNMEASURED  {sum(1 for d, (r1, _r2) in results.items() if r1['verdict'] not in ('LAUNDERED', 'DISCRIMINATES'))}"
          f" directories fell back to T2 — named in §2 with the reason")
    print()
    print("    THE INDEX SAID 19 CANDIDATES.  IT IS NOT 19 DEFECTS AND IT IS NOT 0.")
    if dirty or not ok:
        return 2
    return 1 if laundered else 0


def interpreter_text(text):
    return "bash" if "bash" in text.split("\n", 1)[0] else "sh"


if __name__ == "__main__":
    sys.exit(main())
