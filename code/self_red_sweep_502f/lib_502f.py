#!/usr/bin/env python3
"""mg-502f — THE DETECTOR, isolated so that `s0_controls.py` tests THIS and not a
re-spelling of it.

THE PRECONDITION, in the ticket's own words: "a tracked script that invokes `./build.sh`
(or any target that runs `gate_fixed_point_f771`), AND whose output is captured by a shell
redirect into a tracked `code/**/out_*.txt`."  Both halves are here, and they are NOT
symmetric in how well they can be answered:

  A  THE EXEC EDGE is IN THE SOURCE and is therefore decidable.  §A below.
  B  THE REDIRECT IS NOT IN ANY FILE.  This is the finding that shapes the whole
     instrument.  `x0_exhibit.py`'s redirect was never written down anywhere until
     mg-479c wrote it into `build.sh`'s header AFTER the repair; `x1_positive_control.py`'s
     is recorded only as an arrow in a README table, `x1_positive_control.py →
     out_x1_positive.txt`, which is a producer/artifact mapping and not a command.  A
     detector that greps for `> out_*.txt` therefore UNDER-COUNTS THE CLASS, and would
     have found ZERO of the two real instances.  §B replaces the grep with the question
     the grep was a proxy for: DOES A TRACKED TRANSCRIPT EXIST THAT THIS SCRIPT'S OUTPUT
     IS THE ONLY PLAUSIBLE SOURCE OF — i.e. one bound to it by name or by a documented
     arrow — AND DOES THE SCRIPT FAIL TO WRITE IT ITSELF?  If both, the only way the
     committed bytes can have got there is a capture, and a capture into a tracked
     transcript is the defect.

WHY `./build.sh` AND NOTHING ELSE IS THE TARGET.  `gate_fixed_point_f771` refuses without
`BUILD_SH_RAN_THE_SUITES=1`, and that variable is set on exactly one line in this
repository (`build.sh`, the line that runs it).  So "runs a target that runs f771" and
"runs ./build.sh" are the same set here, and `s1_sweep.py` §0 re-measures that rather than
inheriting it from this comment.
"""

import ast
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

GATE = "build.sh"
HANDSHAKE = "BUILD_SH_RAN_THE_SUITES"

# §A.  The exec primitives a python file can reach a subprocess through.  A NAME, not a
# resolved binding: `from subprocess import run` and `subprocess.run` must both count, and
# neither is worth a symbol table to tell apart when the cost of a false positive is that a
# human reads one more line of §2.
EXEC_NAMES = frozenset((
    "run", "call", "check_call", "check_output", "Popen",
    "system", "popen", "execv", "execvp", "execl", "execlp", "spawnv", "spawnl",
))


class Refused(Exception):
    """Raised when this instrument cannot reach a verdict, which is not a finding."""


def git(root, *args):
    try:
        p = subprocess.run(("git", "-C", root) + args, capture_output=True, text=True)
    except OSError as exc:                                  # pragma: no cover - no git
        raise Refused("git is not runnable: %s" % exc)
    if p.returncode != 0:
        raise Refused("git %s exited %d: %s" % (" ".join(args), p.returncode,
                                                p.stderr.strip()[:200]))
    return p.stdout


def tracked(root=ROOT):
    return git(root, "ls-files").splitlines()


def is_transcript(rel):
    """The class mg-f771 grades: a tracked `out_*.txt` under `code/`.  Spelled here rather
    than imported because `s0_controls.py` must be able to exercise the detector against
    PLANTED relative paths that no repository contains; `guard_502f.py`, which runs against
    a real repository and a real fd, imports f771's own copy instead."""
    return (rel.startswith("code/") and rel.endswith(".txt")
            and os.path.basename(rel).startswith("out_"))


# --------------------------------------------------------------------------- §A exec edge

def mentions(text):
    """Cheap prefilter: could this file possibly be a route or an exec edge?

    THE SWEEP PARSED ALL 1164 TRACKED .py FILES AND TOOK 8.74 s, WHICH IS 10% OF THIS
    REPOSITORY'S WHOLE MERGE GATE FOR A QUESTION ABOUT SIX FILES.  A file that does not
    contain the string `build.sh` or the handshake name ANYWHERE — comment, docstring or
    code — cannot satisfy either rule, because both rules require a literal occurrence and
    the prefilter is strictly weaker than both.  So the filter cannot change a verdict; it
    can only change the runtime, which is what §1's own timing line reports.
    """
    return GATE in text or HANDSHAKE in text


def _docstring_nodes(tree):
    out = set()
    for n in ast.walk(tree):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = getattr(n, "body", None)
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                out.add(id(body[0].value))
    return out


def _reporting_parents(tree):
    """id() of every string Constant that is an argument to `print(...)` or `X.write(...)`.

    A LITERAL THAT IS ONLY EVER PRINTED IS PROSE WITH A QUOTE ROUND IT.  Four tracked files
    name the gate in code; two of them do it exclusively inside `print(...)` calls that
    tell a human to run it, and one of those two is `g0_fixed_point.py` — mg-f771's own
    arm, whose docstring is about the gate it is the last suite of.  Without this rule they
    are exec-edge sites forever, and a sweep with two permanent known-benign rows is a
    sweep whose rows stop being read.
    """
    out = set()
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        f = n.func
        name = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else "")
        if name not in ("print", "write"):
            continue
        for a in ast.walk(n):
            if isinstance(a, ast.Constant) and isinstance(a.value, str):
                out.add(id(a))
    return out


def py_gate_edge(source):
    """(gate_literal_lines, exec_lines) for a python source.

    A GATE LITERAL IN CODE — not in a docstring — plus AN EXEC PRIMITIVE ANYWHERE IN THE
    FILE.  The obvious tighter rule, "a literal `build.sh` inside the argument of an exec
    call", WAS WRITTEN FIRST AND MISSED A REAL INSTANCE: `x1_positive_control.py` builds
    `["sh", os.path.join(L.ROOT, "build.sh")]` and hands it to a local helper, which is the
    one that calls `subprocess.run`.  One hop of indirection defeated it.  So the two
    conditions are decoupled and the cost is stated: this is an OVER-approximation, a file
    that prints the string and separately runs something else is flagged, and §2 resolves
    those by reading them rather than by tightening the rule into missing another hop.
    """
    tree = ast.parse(source)
    doc = _docstring_nodes(tree) | _reporting_parents(tree)
    lits = sorted({n.lineno for n in ast.walk(tree)
                   if isinstance(n, ast.Constant) and isinstance(n.value, str)
                   and GATE in n.value and id(n) not in doc})
    execs = sorted({n.lineno for n in ast.walk(tree) if isinstance(n, ast.Call)
                    and ((isinstance(n.func, ast.Attribute) and n.func.attr in EXEC_NAMES)
                         or (isinstance(n.func, ast.Name) and n.func.id in EXEC_NAMES))})
    return lits, execs


def sh_gate_edge(source):
    """Lines of a shell script that RUN the gate.  A `#` comment is not an invocation, and
    this estate's runners are more comment than command, so the whole of the evidence is in
    stripping them: 24 of the 26 tracked shell files that mention `build.sh` mention it
    only in prose."""
    out = []
    for i, line in enumerate(source.splitlines(), 1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        s = re.sub(r"#.*$", "", s)
        if re.search(r"(^|[\s;&|(])(\./|sh\s+|bash\s+|\S*/)?build\.sh(\s|$|[;&|)])", s):
            out.append(i)
    return out


# ------------------------------------------------------------------- §B transcript binding

ARROW = re.compile(r"([A-Za-z0-9_.]+\.py)\s*(?:->|→|\|)?[^|\n]*?(out_[A-Za-z0-9_]+\.txt)")
REDIRECT = re.compile(
    r"([A-Za-z0-9_./-]+\.(?:py|sh))[^\n>]*>>?\s*\"?([A-Za-z0-9_./$-]*out_[A-Za-z0-9_]+\.txt)")


def bindings(script_rel, tracked_files, texts):
    """Tracked transcripts bound to `script_rel`, with the rule that bound each.

    THREE RULES, WEAKEST LAST, because each catches an instance the one before it missed:

      NAME       `code/d/x0_exhibit.py` <-> `code/d/out_x0_exhibit.txt`.  Caught x0.
      REDIRECT   a literal `script ... > out_*.txt` in any tracked shell or markdown file.
                 Caught NEITHER real instance — see this module's docstring.
      ARROW      a documented pairing on one line of a tracked markdown file, e.g. a
                 README table row `| x1_positive_control.py -> out_x1_positive.txt |`.
                 Caught x1, whose transcript name is NOT its own stem and which no file
                 in this repository redirects into.
    """
    d = os.path.dirname(script_rel)
    stem = os.path.basename(script_rel)[:-3]
    found = {}
    by_name = "%s/out_%s.txt" % (d, stem)
    if by_name in tracked_files:
        found[by_name] = "NAME"
    for rel, text in texts.items():
        if not (rel.endswith(".md") or rel.endswith(".sh")):
            continue
        for line in text.splitlines():
            if os.path.basename(script_rel) not in line:
                continue
            for pat, rule in ((REDIRECT, "REDIRECT"), (ARROW, "ARROW")):
                for m in pat.finditer(line):
                    if os.path.basename(script_rel) not in m.group(1):
                        continue
                    cand = "%s/%s" % (d, os.path.basename(m.group(2)))
                    if cand in tracked_files and cand not in found:
                        found[cand] = rule
    return sorted((t, found[t]) for t in found)


def self_writes(source, transcript_rel):
    """Does the script write that transcript ITSELF?  The mg-479c repair shape: buffer the
    output and `open(...,'w')` the file after the last gate run.  A script that does this is
    SAFE ONLY IF nothing also redirects into the same file — which is why §2's verdict for a
    self-writer is GUARDED, not SAFE, unless it also refuses the redirect."""
    base = os.path.basename(transcript_rel)
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return False
    doc = _docstring_nodes(tree)
    named = any(isinstance(n, ast.Constant) and isinstance(n.value, str)
                and base in n.value and id(n) not in doc for n in ast.walk(tree))
    writes = any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                 and n.func.id == "open"
                 and any(isinstance(a, ast.Constant) and isinstance(a.value, str)
                         and "w" in a.value for a in n.args)
                 for n in ast.walk(tree))
    return named and writes


# THE ROUTE EXEMPTION.  TWO DIRECTORIES, NAMED, EACH WITH ITS REASON — f771's own
# `SELF_EXCLUDED` shape, which is one file rather than one directory and is held to one
# file by worlds E1-E7.  Same discipline, and `s0_controls.py` D16-D18 hold this list to
# exactly these two and check that a planted route outside them is still caught.
#
#   code/gate_fixed_point_f771/   THE CALLEE.  `lib_f771.py:73` is
#                                 `FRESH_ENV = "BUILD_SH_RAN_THE_SUITES"` — the control
#                                 naming the variable it refuses without.  Naming is not
#                                 setting, and the thing guarded against is a SECOND
#                                 CALLER, which by construction is not the callee.
#   code/self_red_sweep_502f/     THIS INSTRUMENT.  It cannot look for a string without
#                                 containing it, and `s0_controls.py` cannot plant a world
#                                 shaped like a route without the world being shaped like
#                                 a route.  THIS EXEMPTION WAS ADDED AFTER THE SWEEP
#                                 REFUSED ITSELF — and only after it was COMMITTED, because
#                                 until then its own files were untracked and `git ls-files`
#                                 did not show them to it.  An instrument that passes while
#                                 uncommitted and refuses once committed is worth the line
#                                 it takes to write down.
#
# WHAT THE EXEMPTION DOES NOT COVER, and this is why it is narrow enough to keep: it
# suppresses only §0's ROUTE question.  §1 scans both directories for exec edges to
# `./build.sh` exactly as it scans every other, so a self-red script placed inside either
# one is found by the same rule that found the two real instances.
ROUTE_EXEMPT = ("code/gate_fixed_point_f771/", "code/self_red_sweep_502f/")


def handshake_setters(texts, exempt=ROUTE_EXEMPT):
    """Tracked lines that could open a route to f771 other than `build.sh`.  Executable
    positions only, and the two file kinds need different rules:

      .sh   a non-comment line containing `HANDSHAKE=1` — the shell form of SETTING it.
      .py   a string literal in CODE, not in a docstring, containing the handshake name,
            outside the two declared directories in `ROUTE_EXEMPT`.

    TWO EXCLUSIONS, BOTH LEARNED BY BEING REFUSED BY THIS OWN INSTRUMENT ON ITS FIRST TWO
    RUNS AGAINST A CLEAN TREE, and both kept here rather than quietly folded in:

      MARKDOWN.  Run 1 found three "routes": build.sh, a README sentence, and a module
      docstring.  A document cannot execute anything.
      THE CALLEE AND THIS INSTRUMENT — `ROUTE_EXEMPT`, two directories, reasons above.
      Run 2 found `lib_f771.py`'s own `FRESH_ENV` constant; run 3 found THIS FILE and
      `s0_controls.py`, and found them only after the suite was COMMITTED, because until
      then `git ls-files` did not show this instrument to itself.

    All three refusals were the right BEHAVIOUR on a wrong rule, which is the order this
    estate prefers: the instrument declined to under-report rather than guessing, three
    times, and the rule was narrowed each time with the miss written down.  The exclusion
    is narrow enough to keep its teeth — a NEW file in any other directory that names the
    handshake in code takes this sweep to REFUSED, which is the right direction for a rule
    about second routes, and §1 still scans the exempt directories for exec edges.
    """
    out = []
    for rel, text in sorted(texts.items()):
        if rel.endswith(".sh"):
            for i, line in enumerate(text.splitlines(), 1):
                st = line.strip()
                if st and not st.startswith("#") and HANDSHAKE + "=1" in st:
                    out.append((rel, i, st))
        elif rel.endswith(".py") and not rel.startswith(tuple(exempt)):
            try:
                tree = ast.parse(text)
            except SyntaxError:
                continue
            doc = _docstring_nodes(tree)
            lines = text.splitlines()
            for n in ast.walk(tree):
                if (isinstance(n, ast.Constant) and isinstance(n.value, str)
                        and HANDSHAKE in n.value and id(n) not in doc):
                    out.append((rel, n.lineno, lines[n.lineno - 1].strip()))
    return out


def calls_guard(source):
    """Does the script call mg-502f's guard, which REFUSES the redirect rather than
    tolerating it?  This is the only condition under which the old invocation is safe."""
    return "refuse_if_self_red" in source
