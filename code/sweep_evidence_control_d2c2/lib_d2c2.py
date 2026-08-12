"""mg-d2c2 — shared plumbing for the control mg-9876's §4 does not have.

THE PREDICATE UNDER TEST IS IMPORTED, NEVER RE-SPELLED.  `a4_sweep.py` decides whether a
directory has "evidence of a falsification attempt" from two regexes and a three-line
combination.  If this file copied those regexes, every result below would be a statement
about the copy — and the copy would keep agreeing with a transcript long after the original
had changed.  So `NEGATIVE_NAMES`, `RED_TOKENS` and `files()` are pulled off the real module
by path, and `sweep_says_bare()` is the only thing here that is mine: the combination, three
lines, written once.

`p1_names.py` additionally CHECKS that combination against the sweep's own printed list.  A
reimplementation that agrees with the original on 201 directories and disagrees on one is
exactly the failure this arrangement is exposed to, so it is measured rather than assumed.
"""

import importlib.util
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CODE = os.path.join(ROOT, "code")

SWEEP_DIR = os.path.join(CODE, "control_audit_9876")
SWEEP_PY = os.path.join(SWEEP_DIR, "a4_sweep.py")
SWEEP_TRANSCRIPT = os.path.join(SWEEP_DIR, "out_a4_sweep.txt")
GATE_BASELINE = os.path.join(CODE, "control_gate_724a", "BASELINE.json")

# The two directories this ticket was filed about.  They are NOT used to find anything —
# p1 reads the names out of the sweep — they are the expectation p1 is required to confirm
# or contradict, so that "the sweep named the ones we thought" is a measurement.
TICKET_EXPECTS = ("audit_successor_consolidation_9134", "compression_novelty_623a")

SELF = os.path.basename(HERE)


class Refused(Exception):
    """Raised when this instrument cannot reach a verdict, which is not a finding."""


def _load_sweep():
    spec = importlib.util.spec_from_file_location("a4_sweep_under_test", SWEEP_PY)
    if spec is None or spec.loader is None:
        raise Refused(f"{SWEEP_PY} is not importable — there is nothing to test")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for attr in ("NEGATIVE_NAMES", "RED_TOKENS", "files", "dirs"):
        if not hasattr(mod, attr):
            raise Refused(f"a4_sweep.py no longer exposes `{attr}` — the probe this "
                          f"instrument tests has been restructured, and a transcript "
                          f"produced against the old shape would be a fiction")
    return mod


SWEEP = _load_sweep()


def read(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def probe(path):
    """The §3 evidence probe, applied to one directory.

    Returns (bare, why) where `why` records what each half of the probe saw.  This is
    a4_sweep.py's own decision, reached with a4_sweep.py's own objects.
    """
    srcs = list(SWEEP.files(path, (".py", ".sh")))
    txts = list(SWEEP.files(path, (".txt", ".md")))
    neg_hits = [os.path.basename(f) for f in srcs
                if SWEEP.NEGATIVE_NAMES.search(os.path.basename(f))]
    red_hits = []
    for f in txts:
        m = SWEEP.RED_TOKENS.search(read(f))
        if m:
            red_hits.append((os.path.basename(f), m.group(0)))
    bare = not neg_hits and not red_hits and bool(srcs)
    return bare, {
        "sources": [os.path.basename(f) for f in srcs],
        "transcripts": [os.path.basename(f) for f in txts],
        "filename_probe_hits": neg_hits,
        "token_probe_hits": red_hits,
    }


def sweep_says_bare(path):
    return probe(path)[0]


def all_dirs():
    return [(n, os.path.join(CODE, n)) for n in sorted(os.listdir(CODE))
            if os.path.isdir(os.path.join(CODE, n))]


def run_sweep_live():
    """Run a4_sweep.py and return its stdout.  Nothing in its directory is written."""
    proc = subprocess.run(["python3", "-u", SWEEP_PY], cwd=ROOT,
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise Refused(f"a4_sweep.py exited {proc.returncode}; its own §4 control did not "
                      f"answer both ways, so its counts must not be cited")
    return proc.stdout


BARE_LIST_MARKER = "directories with code and no evidence of a falsification attempt:"


def parse_bare_list(text, where):
    """Read the §3 name list and the two counts out of a sweep transcript.

    REFUSES rather than returning a short list.  The whole point of the ticket's first
    instruction — "the sweep names them, so read them out of it rather than inferring from
    the count" — is defeated by a parser that silently returns 24 of 25 names.
    """
    lines = text.split("\n")
    try:
        start = next(i for i, ln in enumerate(lines) if BARE_LIST_MARKER in ln)
    except StopIteration:
        raise Refused(f"{where}: no §3 name list — the sweep's output shape has changed")

    names = []
    for ln in lines[start + 1:]:
        if not ln.strip():
            break
        names.extend(ln.split())

    population = None
    stated = None
    for ln in lines:
        if ln.startswith("population: ") and "directories under code/" in ln:
            population = int(ln.split()[1])
        if ln.startswith("SWEEP ") and "no falsification evidence" in ln:
            stated = int(ln.split("tee sites,")[1].split("directories")[0].strip())

    if population is None:
        raise Refused(f"{where}: no `population:` line")
    if stated is None:
        raise Refused(f"{where}: no SWEEP decision line naming the count")
    if len(names) != stated:
        raise Refused(f"{where}: parsed {len(names)} names but the SWEEP line says "
                      f"{stated} — the list and the count disagree and neither can be used")
    return names, population, stated


def git_show(rev, relpath):
    """`git show rev:relpath`, or None if git or the path is unavailable."""
    try:
        out = subprocess.run(["git", "show", f"{rev}:{relpath}"], cwd=ROOT,
                             capture_output=True, text=True, timeout=30)
    except Exception:
        return None
    return out.stdout if out.returncode == 0 else None


def git_added(name):
    """The commit date on which code/<name> first appeared, or None."""
    try:
        out = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%cs", "--", f"code/{name}"],
            cwd=ROOT, capture_output=True, text=True, timeout=30)
    except Exception:
        return None
    if out.returncode != 0 or not out.stdout.strip():
        return None
    return out.stdout.split()[-1]


def find_literal(path, literal):
    """Return (lineno, line) for the first occurrence of `literal`, or None."""
    if not os.path.exists(path):
        return None
    for i, ln in enumerate(read(path).split("\n"), 1):
        if literal in ln:
            return i, ln.strip()
    return None
