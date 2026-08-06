"""mg-ec63 -- shared machinery for the ARC-WIDE truncate-before-probe sweep.

THREE THINGS LIVE HERE AND NOTHING ELSE:

  1. `parse_runner` -- a shell-lite resolver that answers, for one `run_all.sh`,
     WHICH PROBE'S OUTPUT GOES INTO WHICH FILE AND BY WHICH OPERATOR.  It is not
     a regex over the runner text.  mg-03d1's sweep used one, and the arc has at
     least four runner idioms (a direct `python3 X.py > out`, a `run <probe>
     <out>` helper, a `run <out> <probe>` helper with the arguments in the OTHER
     ORDER, and an `expect <code> <probe>` helper that DERIVES the out name from
     the probe stem) -- so a text rule gets the argument order wrong on some and
     cannot see the derived name at all.  Anything this resolver cannot decide
     comes back as UNRESOLVED and is printed as UNRESOLVED.

  2. `trace_opens` -- the empirical answer to "does this probe read its own
     transcript".  A `sys.addaudithook` on the `open` audit event records every
     path the PROCESS actually opens.  This replaces asking whether the SOURCE
     TEXT spells `out_`, which is false in both directions: a probe can mention
     `out_` in a docstring and never open one, and a probe can open one through
     a variable, a `Path` join, or a `subprocess` without the literal appearing.

  3. `run_probe` -- runs one probe TWICE AT THE SAME TREE STATE:
        A  the defect reproduced: its own out target emptied first, exactly as
           `>` does, so what A reports is what the arc has been publishing.
        B  the same probe with that transcript holding its committed bytes.
     `diff(A, B)` is then attributable to the shape and to nothing else.  Both
     runs restore the tree in a `finally` and the restore is asserted.

THE ORDER MATTERS AND IS NOT NEGOTIABLE.  The sweep runs AGAINST the defect.
Fixing the runners first and measuring afterwards cannot recover what the probe
used to miss, because once the probe reads a full transcript there is nothing
left to compare it to.
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MINE = "code/%s" % os.path.basename(HERE)

# --------------------------------------------------------------------------
# printing conventions, copied from this arc's other instruments so the
# transcripts read the same way: every number carries its population and the
# unit one of it counts.
# --------------------------------------------------------------------------


def hdr(t):
    print()
    print("=" * 74)
    print(t)
    print("=" * 74)


def plain(label, n, unit=None):
    print("      %-58s %6s" % (label, n))
    if unit:
        print("          ^ one unit of that number is %s" % unit)


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=REPO, capture_output=True,
                          text=True).stdout


def head():
    return git("rev-parse", "HEAD").strip()[:7]


def read(rel):
    with open(os.path.join(REPO, rel), errors="replace") as f:
        return f.read()


def trees():
    """Every directory under `code/` holding a `run_all.sh`.

    A PROPERTY, not a list.  109 at fe6a495; the number is re-derived on every
    run and printed with the glob that produced it.
    """
    import glob
    out = []
    for p in sorted(glob.glob(os.path.join(REPO, "code", "*", "run_all.sh"))):
        out.append(os.path.relpath(os.path.dirname(p), REPO))
    return sorted(out)


# ==========================================================================
# 1.  THE RUNNER RESOLVER
# ==========================================================================

# A step is (probe_relpath, out_name, operator).  operator is one of:
#   "TRUNC"      plain `>` straight onto the transcript -- the defect
#   "APPEND"     `>>`
#   "STRUCT"     writes `X.new` and `mv`s it -- mg-bf79's structural fix
#   "STREAM"     the probe is run with no redirect at all
Step = tuple


def _strip_comments(src):
    """Drop comment lines and trailing comments.

    KNOWN LIMIT, stated rather than hidden: a `#` inside a single- or
    double-quoted shell string is dropped too.  `unresolved_reason` reports any
    runner whose parse comes out empty, which is where that would show up.
    """
    out = []
    raw, buf = [], ""
    for ln in src.splitlines():          # join `\`-continued lines first
        if ln.rstrip().endswith("\\"):
            buf += ln.rstrip()[:-1] + " "
            continue
        raw.append(buf + ln)
        buf = ""
    if buf:
        raw.append(buf)
    for ln in raw:
        s = ln.strip()
        if s.startswith("#"):
            continue
        # trailing comment: only when preceded by whitespace and not inside
        # an obvious quote pair on that line
        if " #" in ln and ln.count('"') % 2 == 0 and ln.count("'") % 2 == 0:
            ln = ln.split(" #", 1)[0]
        out.append(ln)
    return out


_FUNC = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(\)\s*\{?\s*$")
_PY = re.compile(r"\bpython3?\b(?P<rest>[^>]*?)(?P<op>>>|>)\s*(?P<tgt>[^\s;&|]+)")
_PY_NORED = re.compile(r"\bpython3?\b(?P<rest>.*)$")


def _funcs(lines):
    """name -> body lines, for `name() { ... }` blocks."""
    out, i = {}, 0
    while i < len(lines):
        m = _FUNC.match(lines[i])
        if m and (lines[i].rstrip().endswith("{")
                  or (i + 1 < len(lines) and lines[i + 1].strip() == "{")):
            name = m.group(1)
            j = i + 1 if lines[i].rstrip().endswith("{") else i + 2
            depth, body = 1, []
            while j < len(lines) and depth:
                if lines[j].strip() == "}":
                    depth -= 1
                    if not depth:
                        break
                body.append(lines[j])
                j += 1
            out[name] = body
            i = j
        i += 1
    return out


def _unq(s):
    return s.strip().strip('"').strip("'")


class _Sym(object):
    """A shell WORD, as a template over the enclosing function's call arguments.

    A word is a list of parts.  A part is either literal text or a reference to
    one call argument, possibly with `.py` stripped and/or `basename` applied.
    This is a template rather than a single symbol because the arc's runners
    BUILD their targets: `out_${name%.py}.txt`, `"$HERE/out_$name.txt"`,
    `out_$(basename "$1" .py).txt`.  A rule that only understands `$1` and
    `$out` sees none of those and reports the tree as having no steps.
    """

    def __init__(self, parts):
        self.parts = parts                # [("lit", s)] / [("arg", n, flags)]

    def resolve(self, args):
        out = []
        for p in self.parts:
            if p[0] == "lit":
                out.append(p[1])
                continue
            n, flags = p[1], p[2]
            if n - 1 >= len(args) or n < 1:
                return None
            v = args[n - 1]
            if "base" in flags:
                v = os.path.basename(v)
            if "nopy" in flags:          # `${x%.py}`, `${1%.*}`, `basename .py`
                v = os.path.splitext(v)[0]
            out.append(v)
        return "".join(out)

    def append(self, lit):
        return _Sym(self.parts + [("lit", lit)])


_TOK = re.compile(r"""
    \$\(basename\s+"?\$\{?(?P<bn>\w+)\}?"?\s+\.py\)     # $(basename "$1" .py)
  | \$\{(?P<pv>\w+)%\.(?:py|\*)\}                       # ${name%.py} ${1%.*}
  | \$\{(?P<cv>\w+)\}                                   # ${name}
  | \$(?P<dv>\w+)                                       # $name / $1
""", re.X)


def _sym(expr, shift, env, depth=0):
    """Turn a shell word into a _Sym, resolving through local assignments.

    Returns None if any `$`-reference cannot be traced to a call argument or a
    literal -- which is what makes a step UNRESOLVED rather than guessed at.
    """
    e = expr.strip()
    if e[:1] in ('"', "'") and e[-1:] == e[:1]:
        e = e[1:-1]
    e = e.replace('"', "")
    if depth > 6:
        return None
    parts, pos = [], 0
    for m in _TOK.finditer(e):
        if m.start() > pos:
            parts.append(("lit", e[pos:m.start()]))
        pos = m.end()
        name = m.group("bn") or m.group("pv") or m.group("cv") or m.group("dv")
        flags = set()
        if m.group("bn"):
            flags |= {"base", "nopy"}
        if m.group("pv"):
            flags |= {"nopy"}
        if name.isdigit():
            parts.append(("arg", int(name) + shift, flags))
        elif name in env:
            for p in env[name].parts:
                if p[0] == "lit":
                    parts.append(p)
                else:
                    parts.append(("arg", p[1], p[2] | flags))
        elif e[pos:pos + 1] == "/":
            # An UNTRACEABLE DIRECTORY PREFIX, and only that.  `"$HERE/out_$s"`
            # and `"$D/probe.py"` name a directory this resolver never learned,
            # but every consumer here takes `os.path.basename`, so the prefix
            # cannot change the answer.  A `$VAR` NOT followed by `/` is a
            # different thing and still returns None.
            parts.append(("lit", "@OPAQUE"))
        else:
            return None
    if pos < len(e):
        parts.append(("lit", e[pos:]))
    return _Sym(parts)


def _stmts(lines):
    """Split each line on `;` so `want="$1"; shift` is two statements.

    Without this the `shift` in a one-line helper preamble is invisible and
    every argument position after it is off by one -- which is exactly the
    argument-order error a regex sweep makes, one layer down.
    """
    out = []
    for ln in lines:
        if ln.count('"') % 2 or ln.count("'") % 2:
            out.append(ln)
            continue
        for part in ln.split(";"):
            if part.strip():
                out.append(part)
    return out


def _body_shape(body):
    """Walk a helper-function body and work out, in terms of ITS OWN call
    arguments, which argument is the probe and which is the out file.

    Returns (probe_sym, out_sym, operator) or None.
    """
    shift, env, mvs = 0, {}, []
    for ln in _stmts(body):
        s = ln.strip()
        if re.fullmatch(r"shift(\s+\d+)?", s):
            shift += int(s.split()[1]) if len(s.split()) > 1 else 1
            continue
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)=(.+)$', s)
        if m and not s.startswith("if"):
            v = _sym(m.group(2), shift, env)
            if v:
                env[m.group(1)] = v
            continue
        if s.startswith("mv "):
            mvs.append(s)
        m = _PY.search(s)
        if m:
            tgt = _sym(m.group("tgt"), shift, env)
            probe = _probe_word(m.group("rest"), shift, env)
            if tgt is None or probe is None:
                return ("UNRESOLVED", None, None)
            struct = any(p[0] == "lit" and ".new" in p[1] for p in tgt.parts)
            if struct and any(".new" in x for x in mvs + body_tail(body, ln)):
                return (probe, tgt, "STRUCT")
            return (probe, tgt,
                    "APPEND" if m.group("op") == ">>" else "TRUNC")
        m = _PY_NORED.search(s)
        if m and ">" not in s and "|" not in s:
            probe = _probe_word(m.group("rest"), shift, env)
            if probe is not None:
                return (probe, None, "STREAM")
    return None


def _probe_word(rest, shift, env):
    """The word naming the script, out of `python3 -B -W ignore <word> ...`.

    `"$@"` means "everything left after the shifts", so the script is the FIRST
    of those -- argument `1 + shift` at the call site.  Getting this wrong is
    how a text rule reports `run out_d1.txt d1_trace.py` as running the
    TRANSCRIPT and writing the PROBE.
    """
    for tok in rest.split():
        if tok.startswith("-"):
            continue
        if tok.strip('"') == "$@":
            return _Sym([("arg", 1 + shift, set())])
        cand = _sym(tok, shift, env)
        if cand is None:
            continue
        lits = "".join(p[1] for p in cand.parts if p[0] == "lit")
        has_arg = any(p[0] == "arg" for p in cand.parts)
        if lits.endswith(".py") or has_arg:
            return cand
    return None


def locate(tree, word):
    """A word naming a file -> a path relative to the REPO, or None.

    Tried against the tree first and the repo root second, because a runner may
    run ANOTHER TREE'S probe (`python3 code/state_delegation_audit_16eb/
    claims16eb.py` in mg-0120's runner is one), and a rule that only looks
    inside the tree reports those as missing rather than as cross-tree.
    """
    if not word:
        return None
    w = word.replace("@OPAQUE/", "")
    for cand in (os.path.join(tree, w), w, os.path.join(tree,
                                                        os.path.basename(w))):
        c = os.path.normpath(cand)
        if os.path.exists(os.path.join(REPO, c)):
            return c
    return os.path.normpath(os.path.join(tree, os.path.basename(w)))


def body_tail(body, after):
    hit = False
    out = []
    for ln in body:
        if hit:
            out.append(ln)
        if ln is after or ln.strip() == after.strip():
            hit = True
    return out


_FOR = re.compile(r"^\s*for\s+([A-Za-z_]\w*)\s+in\s+(.+?)\s*(?:;\s*do)?\s*$")


def _unroll_for(lines):
    """`for s in a b c; do python3 "$s.py" > "out_$s.txt"; done` -> three steps.

    A loop is the shape that most looks like ONE step in a text sweep and is in
    fact N.  Unrolled literally, with the loop variable substituted, so the
    steps it contributes are counted individually.
    """
    out, i = [], 0
    while i < len(lines):
        m = _FOR.match(lines[i])
        if not m or "$(" in m.group(2) or "*" in m.group(2):
            out.append(lines[i])
            i += 1
            continue
        var, words = m.group(1), [w.strip('"').strip("'")
                                  for w in m.group(2).split() if w != ";"]
        j = i + 1
        if lines[j].strip() == "do":
            j += 1
        body = []
        while j < len(lines) and lines[j].strip() != "done":
            body.append(lines[j])
            j += 1
        for w in words:
            for b in body:
                out.append(re.sub(r"\$\{?%s\}?" % re.escape(var), w, b))
        i = j + 1
    return out


def parse_runner(tree):
    """-> (steps, unresolved) for one tree.

    steps: list of (probe_file, out_file_or_None, operator)
    unresolved: list of source lines the resolver refused to guess at
    """
    src = read("%s/run_all.sh" % tree)
    lines = _unroll_for(_strip_comments(src))
    funcs = _funcs(lines)
    shapes = {}
    for name, body in funcs.items():
        sh = _body_shape(body)
        if sh:
            shapes[name] = sh

    # A helper's own body must not be scanned again at top level -- its
    # `python3 "$1" > "$out"` is a TEMPLATE, not a step, and counting it as one
    # both invents a step and reports a spurious UNRESOLVED.
    inbody = set()
    for body in funcs.values():
        for ln in body:
            inbody.add(id(ln))

    steps, unresolved = [], []
    fnames = set(funcs)
    for ln in lines:
        if id(ln) in inbody:
            continue
        s = ln.strip()
        if not s:
            continue
        head_tok = s.split()[0] if s.split() else ""
        if head_tok in ("echo", "printf", "grep", "cat", "sed"):
            continue          # PROSE.  A line that TALKS about python is not a
            # step, and counting it as one is how a text rule
            # invents probes called `can`, `the` and `ridge`.
        if head_tok in shapes:
            probe, out, op = shapes[head_tok]
            if probe == "UNRESOLVED":
                unresolved.append(s)
                continue
            args = _split_args(s)[1:]
            p = probe.resolve(args)
            o = out.resolve(args) if out is not None else None
            if p is None:
                unresolved.append(s)
                continue
            if o and o.endswith(".new"):
                o = o[:-4]
            steps.append((locate(tree, p), locate(tree, o), op))
            continue
        if head_tok in fnames:
            continue                      # a helper with no python in it
        m = _PY.search(s)
        if m:
            probe = _first_py(m.group("rest"))
            tgt = _unq(m.group("tgt"))
            if re.search(r"\bcd\s", s):
                # `( cd elsewhere && python3 p.py ) > out.txt` -- the probe is
                # resolved against a directory this resolver did not follow, so
                # the pair is UNRESOLVED rather than guessed at the wrong tree.
                unresolved.append(s)
                continue
            if probe is None:
                unresolved.append(s)
                continue
            op = "APPEND" if m.group("op") == ">>" else "TRUNC"
            if tgt.endswith(".new"):
                op = "STRUCT"
                tgt = tgt[:-4]
            steps.append((locate(tree, probe), locate(tree, tgt), op))
            continue
        if re.search(r"\bpython3?\b", s) and ".py" in s:
            probe = _first_py(s.split("python", 1)[1])
            if probe is None:
                unresolved.append(s)
            elif re.search(r"(?<!\|)\|(?!\|)", s):
                unresolved.append(s)      # a real pipeline, not a `||` guard
            else:
                steps.append((locate(tree, probe), None, "STREAM"))
    return steps, unresolved


def _split_args(s):
    """Shell word splitting that RESPECTS QUOTES.

    `step "F2: can the V6 row go red?  five constructions" f2_probe.py` has TWO
    arguments, not ten.  Splitting on whitespace makes argument 2 the word
    `can`, and then the resolver reports a probe called `can` writing a
    transcript called `the`.  That is not a hypothetical: it is what this
    resolver did before this function used `shlex`.
    """
    import shlex
    try:
        return [a for a in shlex.split(s, comments=False, posix=True)]
    except ValueError:
        return [a.strip('"').strip("'") for a in s.split()]


def _first_py(rest):
    for tok in rest.split():
        t = _unq(tok)
        if t.endswith(".py"):
            return t
    return None


# ==========================================================================
# 2.  THE OPEN TRACE
# ==========================================================================

SHIM = r'''
import os, sys
_fd = os.open(os.environ["EC63_TRACE"], os.O_WRONLY | os.O_CREAT | os.O_APPEND)


def _hook(event, args):
    try:
        if event == "open":
            p, mode, flags = args[0], args[1], args[2]
            if isinstance(p, (bytes, bytearray)):
                p = p.decode("utf-8", "replace")
            if isinstance(p, str):
                # THE MODE MATTERS AS MUCH AS THE PATH.  A probe that WRITES its
                # own transcript opens exactly the same path as one that READS
                # it, and only one of those is reading an empty file.
                if isinstance(mode, str):
                    rd = ("r" in mode) or ("+" in mode)
                elif isinstance(flags, int):
                    rd = (flags & 3) in (0, 2)      # O_RDONLY / O_RDWR
                else:
                    rd = True                       # unknown: counted as read
                # THE PID IS RECORDED, NOT JUST THE PATH.  `EC63_TRACE` and
                # `PYTHONPATH` are inherited by every child process, and the
                # arc's probes re-run other probes as subprocesses -- so a
                # child's opens land in the parent's trace file and were being
                # attributed to the parent.  With the pid the two can be told
                # apart, and they are counted apart.
                os.write(_fd, ("%s\t%d\t%s\n"
                               % ("R" if rd else "W", os.getpid(), p))
                         .encode("utf-8", "replace"))
        elif event in ("subprocess.Popen", "os.system"):
            os.write(_fd, ("X\t%s\n" % (args,)).encode("utf-8", "replace")[:400])
    except Exception:
        pass


sys.addaudithook(_hook)
'''


def shim_dir():
    d = os.path.join(HERE, ".ec63_shim")
    if not os.path.isdir(d):
        os.makedirs(d)
    p = os.path.join(d, "sitecustomize.py")
    cur = open(p).read() if os.path.exists(p) else None
    if cur != SHIM:
        with open(p, "w") as f:
            f.write(SHIM)
    return d


# ==========================================================================
# 3.  RUNNING ONE PROBE, BOTH WAYS, AND RESTORING
# ==========================================================================

def _porcelain(paths=("code",)):
    return git("status", "--porcelain", "--", *paths).strip()


import threading

_GITLOCK = threading.Lock()


def _snapshot(d):
    out = {}
    if os.path.isdir(d):
        for f in os.listdir(d):
            p = os.path.join(d, f)
            try:
                st = os.stat(p)
                out[f] = (st.st_size, st.st_mtime_ns)
            except OSError:
                pass
    return out


def _restore(tree, before=None):
    """Put the tree back.

    `git checkout` is only invoked when something in the directory actually
    changed, because 422 unconditional checkouts serialise the whole sweep on
    the index lock for no reason.  The lock is still taken when it IS invoked,
    so parallel workers cannot collide there.  S6e checks the whole of `code/`
    at the end, which is what catches anything this scoped restore missed.
    """
    d = os.path.join(REPO, tree)
    if before is not None and _snapshot(d) == before:
        return
    with _GITLOCK:
        subprocess.run(["git", "checkout", "--", tree], cwd=REPO,
                       capture_output=True, text=True)
    if os.path.isdir(d):
        for f in os.listdir(d):
            if f.endswith(".new"):
                try:
                    os.remove(os.path.join(d, f))
                except OSError:
                    pass


def run_probe(tree, probe, out_name, empty_first, timeout=90, trace=False,
              slot=0):
    """Run one probe once.

    empty_first=True  reproduces the defect: truncate `out_name` the way `>`
                      does, then run.  This is run A.
    empty_first=False leaves the committed transcript in place.  This is run B.

    The probe's stdout+stderr is captured to memory; it is NEVER redirected onto
    a transcript, so nothing in the subject tree is rewritten by the sweep
    itself.  The tree is restored in a `finally` either way and the restore is
    checked by the caller.
    """
    d = os.path.join(REPO, tree)
    env = dict(os.environ)
    tracefile = None
    before = _snapshot(d)
    if trace:
        # one trace file PER SLOT: workers run concurrently and a shared path
        # would attribute one probe's opens to another
        tracefile = os.path.join(HERE, ".ec63_trace_%d.txt" % slot)
        if os.path.exists(tracefile):
            os.remove(tracefile)
        open(tracefile, "w").close()
        env["EC63_TRACE"] = tracefile
        env["PYTHONPATH"] = shim_dir() + os.pathsep + env.get("PYTHONPATH", "")
    rec = {"tree": tree, "probe": probe, "out": out_name,
           "empty_first": empty_first}
    # KEEP THE BYTES WE ARE ABOUT TO DESTROY, and put them back ourselves.
    # The first version of this relied on `git checkout --` for the restore,
    # and T4 of the selftest caught it: git cannot restore a file it does not
    # track, so on an untracked fixture the transcript stayed empty.  Every
    # tree in the real sweep is tracked, so the sweep's numbers were never
    # affected -- but "the restore works because the files happen to be
    # tracked" is a guarantee resting on a coincidence, and this ticket is
    # about exactly that shape.
    saved = None
    if empty_first and out_name:
        try:
            with open(os.path.join(d, out_name), "rb") as f:
                saved = f.read()
        except OSError:
            saved = None
    try:
        if empty_first and out_name:
            with open(os.path.join(d, out_name), "w"):
                pass
        proc = subprocess.Popen([sys.executable, "-B", probe], cwd=d, env=env,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True,
                                errors="replace")
        pid = proc.pid
        rec["pid"] = pid
        try:
            out, _ = proc.communicate(timeout=timeout)
            rec["exit"] = proc.returncode
            rec["text"] = out or ""
            rec["timeout"] = False
        except subprocess.TimeoutExpired:
            proc.kill()
            out, _ = proc.communicate()
            rec["exit"] = None
            rec["text"] = out or ""
            rec["timeout"] = True
        if trace:
            opened, written, child = [], [], []
            with open(tracefile, errors="replace") as f:
                for ln in f:
                    parts = ln.rstrip("\n").split("\t", 2)
                    if len(parts) != 3:
                        continue
                    kind, spid, path = parts
                    mine = (spid == str(pid))
                    if kind == "R":
                        (opened if mine else child).append(path)
                    elif kind == "W" and mine:
                        written.append(path)
            rec["opened"] = opened
            rec["written"] = written
            rec["child_read"] = child
    finally:
        if saved is not None:
            p = os.path.join(d, out_name)
            try:
                cur = open(p, "rb").read()
            except OSError:
                cur = None
            if cur != saved:
                with open(p, "wb") as f:
                    f.write(saved)
        _restore(tree, None if empty_first else before)
    return rec


def opened_own(rec, tree, out_name, key="opened"):
    """Did the process actually READ the transcript its own run empties?

    `key="written"` asks the other question.  Both are needed: a probe that
    WRITES its own transcript opens the identical path, and an earlier version
    of this counted those as reads.  Two trees whose probes write their own
    transcript were reported as biting when they are not reading anything at
    all -- and the tell was that the sweep left those two files modified.
    """
    if not out_name:
        return False
    want = os.path.normpath(os.path.join(REPO, tree, out_name))
    for p in rec.get(key, []):
        ap = p if os.path.isabs(p) else os.path.normpath(
            os.path.join(REPO, tree, p))
        if os.path.normpath(ap) == want:
            return True
    return False


def opened_other_outs(rec, tree, out_name, key="opened"):
    seen = set()
    base = os.path.join(REPO, tree)
    for p in rec.get(key, []):
        ap = p if os.path.isabs(p) else os.path.normpath(
            os.path.join(base, p))
        b = os.path.basename(ap)
        if (os.path.dirname(os.path.normpath(ap)) == os.path.normpath(base)
                and b.startswith("out_") and b.endswith(".txt")
                and b != out_name):
            seen.add(b)
    return sorted(seen)


def restore_arc():
    """Put every tree BUT THIS ONE back, tracked and untracked alike.

    The per-probe restore is scoped to the probe's own tree and only touches
    tracked files.  That is not enough, and the sweep proved it: several of the
    arc's probes PLANT FIXTURES IN OTHER TREES (`species_7d75/leak6ef4.py`, an
    `_inject7522/` directory, a `probe_strike_*.md`) and remove them in a
    `finally` -- which never runs when this sweep's timeout KILLS the probe.
    So a timeout does not merely lose an answer; it leaves another ticket's
    fixture on disk.

    This tree is excluded by name because its own transcripts are written by
    the runner as the suite goes, and a blanket `git clean` would delete the
    output of the probe that called this.
    """
    left = []
    # `docs/` too, and not as an afterthought: two of the arc's probes append a
    # section to `docs/OneThird-*-Where-This-Lives.md` and remove it in a
    # `finally` that a killed probe never reaches.  A sweep scoped to `code/`
    # leaves the arc's PROSE edited, which is the one place nobody would think
    # to look for damage done by a measurement.
    for t in trees() + ["docs"]:
        if t == MINE:
            continue
        with _GITLOCK:
            subprocess.run(["git", "checkout", "--", t], cwd=REPO,
                           capture_output=True, text=True)
            r = subprocess.run(["git", "clean", "-fdq", t], cwd=REPO,
                               capture_output=True, text=True)
        if r.returncode:
            left.append(t)
    return left


LEDGER = os.path.join(HERE, "ledger_ec63.json")


def save(name, obj):
    d = {}
    if os.path.exists(LEDGER):
        try:
            with open(LEDGER) as f:
                d = json.load(f)
        except ValueError:
            d = {}
    d[name] = obj
    with open(LEDGER, "w") as f:
        json.dump(d, f, indent=1, sort_keys=True)


def load(name, default=None):
    if not os.path.exists(LEDGER):
        return default
    with open(LEDGER) as f:
        return json.load(f).get(name, default)
