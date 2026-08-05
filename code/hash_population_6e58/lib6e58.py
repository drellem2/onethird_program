"""lib6e58.py -- the apparatus for the repair of THE ARC'S DENOMINATOR.

mg-0ba7's verdict on mg-b2af, filed as mg-6e58:

    lib330a._HASH_FORMATS is ("--format=%H", "--pretty=%H",
    "--format=format:%H").  `--format=%h` -- LOWERCASE -- is not in it.  The
    population every count in this lineage is taken over is therefore defined
    by a CAPITAL LETTER.

WHAT IS WRITTEN FRESH HERE, AND WHY

  * THE ENUMERATION IS READ, NOT RECALLED.  The brief forbids listing the
    flags I happen to remember.  `documented_*()` below parse `man git-log`
    on this machine and return what git's own documentation says addresses a
    commit.  The parse is printed by p1 so a reader can check the reading
    rather than the memory.  If man is unavailable the functions RAISE; a
    documentation population that could not be read is not a population that
    agreed.

  * THE SPELLING TEST IS A PARSE, NOT A LITERAL SET.  `_HASH_FORMATS` is a
    tuple of three exact strings and `f in strs` is equality.  That is the
    defect's real shape: `--format=%h` is missed because of its CASE, and
    `--format=%H %s` is missed because of its LENGTH -- a FULL-hash site,
    lowercase nowhere in it, invisible to the same tuple.  Adding a fourth
    literal repairs one instance of a class with at least two members.
    `hash_emitters()` walks the format string with git's own escape rule
    (`%%` is a literal percent) and reports WHICH placeholders it found.

  * EVERY COUNT NAMES ITS POPULATION AND ITS GRAIN.  There are four nested
    populations here (POP_A..POP_D) and a count is meaningless without one.
    That is this ticket's entire subject, so no function returns a bare int:
    `census(pop)` is keyed and `pop` is not optional.

  * THE CLASSIFIER IS NOT IMPORTED.  `classify_call` below is written from
    mg-330a's DOCSTRING -- the taxonomy in prose -- and mg-330a's own
    `lib330a.classify_call` is imported ONLY as the thing being compared
    against.  p2 runs both over the same ast.Call nodes and prints the
    difference.  Two readers that share an implementation share a blind spot;
    that sentence is mg-330a's and this ticket is what happens when it is
    ignored one generation later.

NOTHING HERE WRITES INTO code/audit_330a/ OR code/repair_b2af/*.py.
mg-330a's `_HASH_FORMATS` is deliberately LEFT AS IT IS: its committed
transcripts are evidence of a run, and widening the constant behind them
would make every figure in that directory unreproducible while still looking
reproducible.  The correction is published beside those figures, not over
them.  The one file of another ticket's this branch edits is
`code/repair_b2af/README.md`, whose STILL-OPEN list states a live false
sentence that mg-0ba7's verdict names.

Every mutation happens in a clone under the system temp directory.

Pure Python 3, no dependencies, NO NETWORK.
"""

import ast
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

# mg-330a's classifier, imported ONLY as the subject of the comparison.
sys.path.insert(0, os.path.join(REPO, "code", "audit_330a"))
import lib330a as A330                                    # noqa: E402


# ---------------------------------------------------------------------------
# THE DOCUMENTATION POPULATION.  git's own man page, parsed.
# ---------------------------------------------------------------------------

MANPAGE = "git-log"


def man_text(page=MANPAGE):
    """The rendered text of `man <page>`, with backspace overstrike removed.

    Raises if the page cannot be read.  A ways-of-addressing-a-commit
    enumeration that silently falls back to a hard-coded list is the defect
    this instrument exists to repair, one level up.
    """
    p = subprocess.run(["man", page], capture_output=True, text=True,
                       env=dict(os.environ, MANWIDTH="100", MANPAGER="cat",
                                PAGER="cat"))
    if p.returncode != 0 or len(p.stdout) < 5000:
        raise RuntimeError(
            "could not read `man %s` (rc=%d, %d bytes).  This instrument "
            "enumerates from git's documentation and must not fall back to a "
            "remembered list." % (page, p.returncode, len(p.stdout)))
    # man overstrikes for bold/underline: "X\bX" and "_\bX".
    return re.sub(r".\x08", "", p.stdout)


def documented_placeholders(text=None):
    """[(placeholder, description)] for every `%<x>` git documents.

    Read from the "Placeholders that expand to information extracted from the
    commit" list: a line that is exactly a `%...` token, then the indented
    description beneath it.

    MULTI-CHARACTER placeholders are included (`%ad`, `%an`, `%cr`).  The
    first form of this regex matched single letters only, on the reasoning
    that a commit hash is `%H` or `%h` and nothing longer -- which is true,
    and which is exactly why it was wrong: `selftest_6e58` compares the
    placeholders USED IN THIS TREE against the documented set, and a tree
    using `--format=%h %ad %s` then reported `%a` as undocumented.  A
    single-character documented set and a single-character tokeniser agreed
    with each other and disagreed with git.  The failing run is kept at
    `out_selftest_6e58_FIRSTFORM_exit1.txt`.
    """
    text = man_text() if text is None else text
    out, lines = [], text.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^\s+(%[A-Za-z]{1,3})\s*$", line)
        if not m:
            continue
        desc = []
        for nxt in lines[i + 1:]:
            if not nxt.strip():
                break
            if re.match(r"^\s+%", nxt):
                break
            desc.append(nxt.strip())
        if desc:
            out.append((m.group(1), " ".join(desc)))
    return out


def documented_commit_hash_placeholders(text=None):
    """The placeholders whose documented description is a COMMIT hash.

    `tree hash` and `parent hashes` are documented in the same list and are
    excluded HERE, by reading the description, rather than by my knowing
    which ones they are.  This is where the population is defined, and it is
    defined by git.
    """
    out = {}
    for ph, desc in documented_placeholders(text):
        d = desc.lower()
        if "hash" not in d:
            continue
        if "tree" in d or "parent" in d:
            continue
        if not d.startswith("commit hash") and not d.startswith(
                "abbreviated commit hash"):
            continue
        out[ph] = "FULL" if d.startswith("commit hash") else "ABBREV"
    return out


# Built-in formats that DO print a commit identifier and that
# `documented_builtin_formats()` cannot see, each with the documentation
# sentence that puts it here.  A DECLARED EXEMPTION, not a silent one: the
# closure test in the selftest requires every handled format to be either
# found by the extractor or listed here, so the list cannot grow by neglect.
EXTRACTOR_BLIND = {
    "raw": "documented in prose with no sample block: \"the hashes are "
           "displayed in full, regardless of whether --abbrev or --no-abbrev "
           "are used\"",
    "mboxrd": "documented only by reference to another format: \"Like email, "
              "but lines in the commit message starting with 'From ' ... are "
              "quoted\"",
}


def documented_builtin_formats(text=None):
    """{name: grain} for the built-in `--pretty=<name>` formats whose
    documented sample output shows a commit identifier.

    Read from the bulleted format list: a bullet naming the format, then its
    indented sample.  A sample containing `<abbrev-hash>` is ABBREV; one
    containing a bare `<hash>` token is FULL.

    THE RULE WAS WIDENED AFTER IT FIRED ON ME.  Its first form required the
    literal `commit <hash>` / `From <hash>`, and so missed `oneline`, whose
    documented sample is `<hash> <title-line>` with no prefix -- one of the
    two formats PREDICTIONS.md P1-c named in the list this rule was supposed
    to produce.  The first form's transcript is kept at
    `out_p1_builtins_FIRSTFORM.txt` rather than deleted.  `raw` and `mboxrd`
    are still not found, and are declared in `EXTRACTOR_BLIND` above with the
    sentence that exempts them.
    """
    text = man_text() if text is None else text
    lines = text.splitlines()
    out, cur, buf = {}, None, []

    def flush():
        if cur is None:
            return
        blob = " ".join(buf)
        if "<abbrev-hash>" in blob:
            out[cur] = "ABBREV"
        elif "<hash>" in blob:
            out[cur] = "FULL"

    for line in lines:
        m = re.match(r"^\s+•\s+([a-z][a-z0-9]*)\s*$", line)
        if m:
            flush()
            cur, buf = m.group(1), []
            continue
        if re.match(r"^\s+•", line) or re.match(r"^[A-Z ]{4,}$", line):
            flush()
            cur, buf = None, []
            continue
        if cur is not None:
            buf.append(line.strip())
    flush()
    return out


def documented_hash_options(text=None):
    """{option: what the documentation says} for the `git log` options that
    turn a commit identifier on, off, or short.
    """
    text = man_text() if text is None else text
    lines, out = text.splitlines(), {}
    for i, line in enumerate(lines):
        m = re.match(r"^\s{4,10}(--[a-z][a-z-]*)(\[?=[^\s]*)?\s*$", line)
        if not m:
            continue
        opt = m.group(1)
        desc = []
        for nxt in lines[i + 1:]:
            if not nxt.strip():
                break
            desc.append(nxt.strip())
        d = " ".join(desc).lower()
        if not d:
            continue
        if opt in ("--abbrev-commit", "--no-abbrev-commit", "--oneline"):
            out[opt] = " ".join(desc)
    return out


# ---------------------------------------------------------------------------
# THE SPELLING TEST.  A parse of the format string, with git's escape rule.
# ---------------------------------------------------------------------------

FORMAT_FLAGS = ("--format=", "--pretty=")
FORMAT_PREFIXES = ("format:", "tformat:")

# Filled from the documentation by `load_documented()`; the module-level
# defaults are what the CLOSURE test in the selftest compares AGAINST, so a
# disagreement between these and `man git-log` is a red test rather than a
# silent widening.
HASH_PLACEHOLDERS = {"%H": "FULL", "%h": "ABBREV"}
BUILTIN_FORMATS = {"oneline": "FULL", "short": "FULL", "medium": "FULL",
                   "full": "FULL", "fuller": "FULL", "reference": "ABBREV",
                   "email": "FULL", "raw": "FULL", "mboxrd": "FULL"}
HASH_OPTIONS = {"--oneline": "ABBREV"}
DEFAULT_FORMAT = "medium"       # documented default when no --format is given


def placeholders_in(fmt):
    """Every `%<x>` placeholder in a git format string, left to right.

    `%%` is a literal percent and consumes both characters -- so `%%h` is the
    text "%h" and NOT an abbreviated hash.  `%x1f` is a hex byte, not a
    placeholder.  Both rules are git's; both are why a substring search for
    "%h" is not the same thing as this function.
    """
    out, i = [], 0
    while i < len(fmt) - 1:
        if fmt[i] != "%":
            i += 1
            continue
        c = fmt[i + 1]
        if c == "%":
            i += 2
            continue
        if c == "x":
            i += 4 if len(fmt) >= i + 4 else 2
            continue
        out.append("%" + c)
        i += 2
    return out


def hash_emitters(strs):
    """[(spelling, grain, why)] -- every documented way THIS call's own string
    arguments make git print a commit identifier.

    `strs` is one call's direct string arguments.  Grain is FULL (a 40-byte
    object name) or ABBREV (a unique prefix).  `why` names the documentation
    row the decision came from, so a reader can check the rule and not the
    result.
    """
    out = []
    for s in strs:
        if s in HASH_OPTIONS:
            out.append((s, HASH_OPTIONS[s], "option: %s" % s))
            continue
        for flag in FORMAT_FLAGS:
            if not s.startswith(flag):
                continue
            val = s[len(flag):]
            for pre in FORMAT_PREFIXES:
                if val.startswith(pre):
                    val = val[len(pre):]
                    break
            if val in BUILTIN_FORMATS:
                out.append((s, BUILTIN_FORMATS[val],
                            "built-in format: %s" % val))
                break
            for ph in placeholders_in(val):
                if ph in HASH_PLACEHOLDERS:
                    out.append((s, HASH_PLACEHOLDERS[ph],
                                "placeholder: %s" % ph))
            break
    # `--abbrev-commit` demotes every FULL emitter in the SAME call.
    if any(s == "--abbrev-commit" for s in strs):
        out = [(sp, "ABBREV" if g == "FULL" else g, w + " +--abbrev-commit")
               for sp, g, w in out]
    return out


def has_format_arg(strs):
    """Does this call give git a format at all?  If not, git's documented
    default (`medium`) applies and a commit identifier IS printed.
    """
    return any(s.startswith(f) for s in strs for f in FORMAT_FLAGS) or \
        any(s in HASH_OPTIONS for s in strs)


# ---------------------------------------------------------------------------
# THE FOUR POPULATIONS.  Nested, named, and never optional.
# ---------------------------------------------------------------------------

POP_A = "POP-A"     # mg-330a's _HASH_FORMATS, verbatim.  3 literals, exact.
POP_B = "POP-B"     # POP-A + the literal "--format=%h".  The one-line repair.
POP_C = "POP-C"     # doc-derived: any %H/%h placeholder, any built-in format,
                    # --oneline.  THIS TICKET'S DENOMINATOR.
POP_D = "POP-D"     # POP-C + calls with NO format at all (default `medium`).

POPULATIONS = (POP_A, POP_B, POP_C, POP_D)

POP_WHAT = {
    POP_A: "mg-330a's `_HASH_FORMATS`, verbatim: 3 literals, exact match",
    POP_B: "POP-A + the literal `--format=%h` -- the one-line repair, "
           "measured to price it",
    POP_C: "doc-derived: any `%H`/`%h` placeholder in any `--format=`/"
           "`--pretty=` value, any built-in format documented to print a "
           "commit identifier, and `--oneline`",
    POP_D: "POP-C + `git log` with NO format argument, whose documented "
           "default `medium` prints `commit <hash>`",
}

_B_LITERALS = tuple(A330._HASH_FORMATS) + ("--format=%h",)


def is_revision_producing(strs, pop):
    """Does this call produce a revision, under population `pop`?

    The `log` half is mg-330a's and unchanged: a string argument that IS
    "log" or ENDS in "log".  Only the format half moves between populations,
    which is the point -- one variable at a time.
    """
    if not any(s == "log" or s.endswith("log") for s in strs):
        return False
    if pop == POP_A:
        return any(f in strs for f in A330._HASH_FORMATS)
    if pop == POP_B:
        return any(f in strs for f in _B_LITERALS)
    if pop == POP_C:
        return bool(hash_emitters(strs))
    if pop == POP_D:
        return bool(hash_emitters(strs)) or not has_format_arg(strs)
    raise ValueError("unnamed population: %r" % (pop,))


def classify_call(strs, pop):
    """mg-330a's taxonomy, written from its DOCSTRING and not imported,
    applied under an explicitly named population.

    Returns a kind or None.  The kind rules are mg-330a's, deliberately
    unchanged: this ticket moves the DENOMINATOR and nothing else, so that a
    difference in the counts cannot be attributed to a re-taxonomy.
    """
    if not is_revision_producing(strs, pop):
        return None
    has_path = "--" in strs
    if any(".." in s for s in strs):
        return "RANGE"
    if any(s in ("-S", "-G") or s.startswith("-S") or s.startswith("-G")
           for s in strs):
        return "PICKAXE"
    if "--reverse" in strs:
        return "OLDEST"
    if "-1" in strs:
        return "NEWEST" if has_path else "NEWEST-norestrict"
    if has_path:
        return "INDEXED"
    return "UNRESTRICTED"


HISTORY_KINDS = ("NEWEST", "NEWEST-norestrict", "INDEXED", "UNRESTRICTED")
ALL_KINDS = ("NEWEST", "NEWEST-norestrict", "INDEXED", "UNRESTRICTED",
             "OLDEST", "PICKAXE", "RANGE")


# ---------------------------------------------------------------------------
# THE SWEEP.  Same ast walk, same file population, four classifications.
# ---------------------------------------------------------------------------

def all_calls(repo=REPO, subdir="code"):
    """[{file, line, strs, src}] for EVERY ast.Call in every `*.py` under
    `<repo>/<subdir>`, unfiltered.

    Unfiltered on purpose: the four populations must be four filters over ONE
    set of nodes, or a count difference could be a walk difference.
    `strs` comes from mg-330a's own `_strings_of`, imported, for the same
    reason.
    """
    rows, unparsed = [], []
    root = os.path.join(repo, subdir)
    for dirpath, _dirs, files in os.walk(root):
        for fn in sorted(files):
            if not fn.endswith(".py"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, repo)
            try:
                with open(full) as fh:
                    src = fh.read()
                tree = ast.parse(src)
            except (SyntaxError, UnicodeDecodeError) as exc:
                unparsed.append((rel, str(exc)))
                continue
            lines = src.splitlines()
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                rows.append({
                    "file": rel, "line": node.lineno,
                    "strs": A330._strings_of(node),
                    "src": lines[node.lineno - 1].strip()
                           if node.lineno <= len(lines) else "",
                })
    return rows, unparsed


def census(pop, calls=None, repo=REPO):
    """{kind: n} plus ALL/HISTORY, over population `pop`.

    `pop` has no default.  A census whose denominator is implicit is the
    thing this ticket is about.
    """
    if calls is None:
        calls, _ = all_calls(repo=repo)
    out = {"ALL": 0, "HISTORY": 0, "_rows": []}
    for k in ALL_KINDS:
        out[k] = 0
    for c in calls:
        kind = classify_call(c["strs"], pop)
        if kind is None:
            continue
        out["ALL"] += 1
        out[kind] += 1
        if kind in HISTORY_KINDS:
            out["HISTORY"] += 1
        row = dict(c)
        row["kind"] = kind
        out["_rows"].append(row)
    return out


def site_key(row):
    return "%s:%d" % (row["file"], row["line"])


def sites(cen):
    return {site_key(r) for r in cen["_rows"]}


# ---------------------------------------------------------------------------
# git, and the clone.
# ---------------------------------------------------------------------------

def git(*args, **kw):
    repo = kw.pop("repo", REPO)
    return subprocess.run(["git", "-C", repo] + list(args),
                          capture_output=True, text=True).stdout


def clone_repo(dest, repo=REPO):
    """A working clone of the repo at its CURRENT worktree state.

    Copies rather than `git clone` so that UNCOMMITTED work -- this
    instrument, while it is being written -- is present in the clone.  The
    clone is what gets mutated; nothing here edits the repo.
    """
    shutil.copytree(os.path.join(repo, "code"), os.path.join(dest, "code"))
    return dest


def tmpdir(prefix="mg6e58_"):
    return tempfile.mkdtemp(prefix=prefix)


# ---------------------------------------------------------------------------
# reporting.  The exit convention is mg-b2af's, which took it from mg-e34a:
# exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
# ---------------------------------------------------------------------------

class Report(object):
    """SELF-ERRORS and FINDINGS, kept apart and each with its population.

    A non-zero exit means THIS SCRIPT HAS SOMETHING TO REPORT, never that it
    is broken.
    """

    def __init__(self, selfpop, findpop):
        self.selfpop, self.findpop = selfpop, findpop
        self.self_errors, self.findings = [], []

    def selferr(self, msg):
        self.self_errors.append(msg)

    def finding(self, msg):
        self.findings.append(msg)

    def gate(self, ok, msg):
        if not ok:
            self.finding(msg)
        return ok

    def check(self, ok, msg):
        if not ok:
            self.selferr(msg)
        return ok

    def emit(self):
        print("-" * 74)
        print("SELF-ERRORS: %d, population: %s"
              % (len(self.self_errors), self.selfpop))
        for x in self.self_errors:
            print("   SELF-ERROR: " + x)
        print("FINDINGS: %d, population: %s"
              % (len(self.findings), self.findpop))
        for x in self.findings:
            print("   FINDING: " + x)
        print("TOTAL BAD: %d" % (len(self.self_errors) + len(self.findings)))
        return 1 if (self.self_errors or self.findings) else 0


def score(report, tag, predicted, actual, note=""):
    """Print one PREDICTIONS.md row scored against what was measured.

    A miss is PRINTED, never corrected.  It is a result.  Copied from
    mg-b2af's `lib_b2af.score` so that the ruler for a hit is not one this
    ticket invented for itself.
    """
    hit = predicted == actual if not callable(predicted) else predicted(actual)
    print("   %-6s predicted %-30s measured %-18s %s%s"
          % (tag, predicted if not callable(predicted) else note,
             actual, "HIT" if hit else "*** MISS",
             "" if hit else "  <- kept as written"))
    return hit
