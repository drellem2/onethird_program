"""lib_1abe -- shared machinery for the mg-1abe transcript-reproduction census.

THE ONE RULE THIS LIBRARY EXISTS TO ENFORCE:

    ANCESTRY ANSWERS "IS THIS COMMIT ON MAIN".
    PATCH-ID ANSWERS "DID THIS CONTENT SURVIVE".

They are different questions and the arc has already confused them once.  After
a refinery rebase, `git merge-base --is-ancestor <recorded> main` returns FALSE
for a commit whose diff is on `main` byte-for-byte.  Anything in this census
that asks "did the content survive" calls `patch_id()`; `is_ancestor()` is used
only where the question really is about reachability, and every caller of it
says so.

VOCABULARY, fixed here so that every script of this census means the same thing:

  CARRYING COMMIT   for a tracked path, `git log -1 --format=%H <rev> -- <path>`
                    -- the commit whose tree the file currently sits in on the
                    named revision.  This is the commit a reader would check
                    out to "see the transcript in context", so it is the commit
                    the transcript is implicitly claiming to be a fact about.

  PRODUCER          the command that `run_all.sh` AT THE CARRYING COMMIT spells
                    for that transcript, including its flags and whether it
                    folds stderr in.  Taken from the suite's own runner rather
                    than guessed from the filename, because 62 of the 504
                    transcript names do not match `out_<stem>.txt -> <stem>.py`.

  REPRODUCES        the producer, run in a detached worktree at the carrying
                    commit, emits bytes identical to the committed blob.

  CLASS 1           a recorded SHA that no longer resolves or is not an
                    ancestor of `main`.  Bookkeeping.
  CLASS 2           a transcript that does not reproduce from its carrying
                    commit.  This is the one that corrupts the evidence base.
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

# The census's own producer.  Re-entering it from inside itself would recurse,
# so it is bucketed as SELF and NEVER silently dropped -- see t2_census.py.
SELF_DIR = "transcript_census_1abe"


# --------------------------------------------------------------------- git

def git(*args, cwd=None, binary=False, check=False):
    """Run git and return stdout.  Never raises unless check=True."""
    r = subprocess.run(["git"] + list(args), cwd=cwd or REPO,
                       capture_output=True)
    if check and r.returncode != 0:
        raise RuntimeError("git %s failed: %s"
                           % (" ".join(args), r.stderr.decode("utf-8", "replace")))
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def git_ok(*args, cwd=None):
    """True iff git exits 0.  For questions whose answer IS the exit code."""
    return subprocess.run(["git"] + list(args), cwd=cwd or REPO,
                          capture_output=True).returncode == 0


_RESOLVE_CACHE = {}
_CARRY_CACHE = {}


def resolve(rev):
    """Full sha for a rev, or None if it does not resolve in this object store.

    Memoised.  This census resolves the same abbreviations tens of thousands of
    times across the arc's transcripts, and one `git rev-parse` per occurrence
    turns a two-minute script into a twenty-minute one.
    """
    if rev in _RESOLVE_CACHE:
        return _RESOLVE_CACHE[rev]
    out = git("rev-parse", "--verify", "--quiet", "%s^{commit}" % rev).strip()
    _RESOLVE_CACHE[rev] = out or None
    return _RESOLVE_CACHE[rev]


def is_ancestor(a, b):
    """REACHABILITY ONLY.  Not a test of whether content survived -- see the
    module docstring.  Every call site must be about reachability."""
    return git_ok("merge-base", "--is-ancestor", a, b)


def patch_id(rev):
    """The stable patch-id of a commit's diff, or None for a root/merge commit
    with no single diff.  THIS is the survival test."""
    p1 = subprocess.Popen(["git", "diff-tree", "-p", "--no-color", rev],
                          cwd=REPO, stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL)
    p2 = subprocess.Popen(["git", "patch-id", "--stable"], cwd=REPO,
                          stdin=p1.stdout, stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL)
    p1.stdout.close()
    out = p2.communicate()[0].decode("utf-8", "replace").split()
    return out[0] if out else None


def blob_at(rev, path):
    """Bytes of a path at a rev, or None if absent."""
    r = subprocess.run(["git", "show", "%s:%s" % (rev, path)], cwd=REPO,
                       capture_output=True)
    return r.stdout if r.returncode == 0 else None


def carrying_commit(path, rev="main"):
    key = (path, rev)
    if key in _CARRY_CACHE:
        return _CARRY_CACHE[key]
    out = git("log", "-1", "--format=%H", rev, "--", path).strip()
    _CARRY_CACHE[key] = out or None
    return _CARRY_CACHE[key]


def transcripts(rev="main"):
    """THE POPULATION.  Every tracked `code/*/out_*.txt` at `rev`, sorted."""
    out = git("ls-tree", "-r", "--name-only", rev, "code/")
    return sorted(p for p in out.split("\n")
                  if re.match(r"^code/[^/]+/out_[^/]*\.txt$", p))


# ------------------------------------------------------------- producers

# `python3 -u foo.py 6 > out_foo.txt 2>&1`, `sh ./b.sh > out_b.txt`, and the
# `|| { ... }` / `|| status=$?` tails the arc's runners hang off them.
_RE_RED = re.compile(
    r"^[ \t]*(?:python3|python|sh)[ \t]+(?P<cmd>[^>\n]*?)[ \t]*"
    r">[ \t]*\"?(?P<out>out_[^\"\s]+\.txt)\"?[ \t]*(?P<comb>2>&1)?",
    re.M)

_RE_FOR = re.compile(
    r"for[ \t]+(?P<var>\w+)[ \t]+in[ \t]+(?P<items>(?:[^\n;]|\\\n)*?)"
    r"[ \t]*(?:;|\n)[ \t]*do(?P<body>.*?)\bdone\b", re.S)

# `run() { python3 -u "$1" > "out_${1%.*}.txt" 2>&1; ... }` followed by
# `run s1_anchors.py`.  Ten of this arc's runners are written this way and a
# parser that only reads straight-line redirections loses all of them.
_RE_FUNC = re.compile(r"^(?P<name>\w+)[ \t]*\(\)[ \t]*\{(?P<body>.*?)^\}",
                      re.M | re.S)


def _subst(text, var, value):
    """Substitute a positional/loop variable, including the `${1%.*}` and
    `${name%.py}` strip-suffix forms the arc's runners use to name transcripts.
    Both forms are live in this repo and a parser that knows only one loses six
    transcripts to a bucket that would have read `CANNOT BE RUN`."""
    def strip_suffix(m):
        suf = m.group(1)
        if suf == ".*":
            return value.rsplit(".", 1)[0]
        return value[:-len(suf)] if suf and value.endswith(suf) else value
    text = re.sub(r"\$\{%s%%([^}]*)\}" % re.escape(var), strip_suffix, text)
    for form in ('"$%s"' % var, "${%s}" % var, "$%s" % var):
        text = text.replace(form, value)
    return text


def parse_producers(sh_text):
    """{out_name: {'cmd': str, 'combined': bool}} from a run_all.sh's text.

    Three forms, in precedence order: straight-line redirections, then `for`
    loops, then shell functions applied to their own call sites.  Earlier forms
    win, so a loop or function body can never overwrite an explicit line.
    Returns {} for a runner that redirects nothing -- that is CANNOT BE RUN,
    not an empty success.
    """
    found = {}
    for m in _RE_RED.finditer(sh_text):
        out = m.group("out")
        if "$" in out:           # an unexpanded template, not a transcript name
            continue
        found[out] = {"cmd": m.group("cmd").strip(),
                      "combined": bool(m.group("comb"))}
    for lm in _RE_FOR.finditer(sh_text):
        var = lm.group("var")
        items = lm.group("items").replace("\\\n", " ").split()
        bm = _RE_RED.search(lm.group("body"))
        if not bm:
            continue
        for it in items:
            if it in ("do", "in"):
                continue
            key = _subst(bm.group("out"), var, it)
            if "$" in key or key in found:
                continue
            found[key] = {"cmd": _subst(bm.group("cmd").strip(), var, it),
                          "combined": bool(bm.group("comb"))}
    for fm in _RE_FUNC.finditer(sh_text):
        name, body = fm.group("name"), fm.group("body")
        # `name="$1"` then `> "out_${name%.py}.txt"`.  Without resolving the
        # alias the redirect target reads as a template, the transcript
        # resolves to no producer, and six of this repo's transcripts would be
        # labelled unproducible for a reason that is purely syntactic.
        for alias in re.findall(r'(\w+)="\$1"', body):
            body = re.sub(r"\$\{%s(%%[^}]*)?\}" % re.escape(alias),
                          lambda m: "${1%s}" % (m.group(1) or ""), body)
            body = body.replace('"$%s"' % alias, '"$1"')
        bm = _RE_RED.search(body)
        if not bm:
            continue
        calls = re.findall(r"^[ \t]*%s[ \t]+(\S+\.(?:py|sh))" % re.escape(name),
                           sh_text, re.M)
        for arg in calls:
            key = _subst(bm.group("out"), "1", arg)
            if "$" in key or key in found:
                continue
            found[key] = {"cmd": _subst(bm.group("cmd").strip(), "1", arg),
                          "combined": bool(bm.group("comb"))}
    return found


def producer_for(path, commit):
    """The producing command for `path` as its OWN carrying commit spells it.

    Returns (spec, reason).  Exactly one is None.
    """
    d = os.path.dirname(path)
    name = os.path.basename(path)
    sh = blob_at(commit, d + "/run_all.sh")
    if sh is None:
        return None, "no run_all.sh in %s at %s" % (d, commit[:7])
    spec = parse_producers(sh.decode("utf-8", "replace")).get(name)
    if spec is None:
        return None, "run_all.sh at %s does not redirect anything to %s" % (
            commit[:7], name)
    script = None
    for tok in spec["cmd"].split():
        tok = tok.strip('"\'')
        if tok.endswith(".py") or tok.endswith(".sh"):
            script = tok[2:] if tok.startswith("./") else tok
            break
    if script is None:
        return None, "producer command has no script: %r" % spec["cmd"]
    if blob_at(commit, "%s/%s" % (d, script)) is None:
        return None, "%s absent from the tree at %s" % (script, commit[:7])
    spec["script"] = script
    spec["dir"] = d
    return spec, None


# ------------------------------------------------------------ conclusions

# A verdict line is one this arc's own runners treat as a result: a bracketed
# tag at line start, or one of the three totals its run_all.sh files grep for.
_RE_VERDICT = re.compile(
    r"^\s*(?:\[[A-Za-z][A-Za-z /-]*\]|TOTAL BAD:|SELF-ERRORS|FINDINGS)")


def verdict_lines(text):
    """The conclusion-bearing lines of a transcript, whitespace-normalised.

    GRAIN: one entry per verdict-bearing line, in order.  Whitespace inside a
    line is collapsed because this arc pads verdict tags to column width and a
    column shift is not a changed conclusion.
    """
    out = []
    for line in text.splitlines():
        if _RE_VERDICT.match(line):
            out.append(" ".join(line.split()))
    return out


def verdict_tags(text):
    """The DECISIONS a transcript records, stripped of the figures inside them.

    For a bracketed row the decision is the bracket -- `[OK]`, `[FINDING]`,
    `[REFUTED]` -- and the sentence after it is commentary that routinely
    carries a count.  For the three totals the arc's runners grep for, the
    NUMBER IS THE DECISION, so the whole line is kept.

    This distinction is the whole of mg-1abe's step 2.  A transcript whose
    `[OK]` became `[FINDING]` is a FALSE RECORD; one where `[OK]` stayed `[OK]`
    while the count inside it moved is DISPLACED.  Comparing raw lines cannot
    tell them apart and calls both a flip.
    """
    out = []
    for line in verdict_lines(text):
        if line.startswith("["):
            out.append(line[:line.index("]") + 1] if "]" in line else line)
        else:
            out.append(line)
    return out


def conclusion_verdict(committed, rerun):
    """The three-way answer to "does the recorded conclusion still hold?".

      FLIPS         a decision changed, or a decision row appeared or vanished.
                    A FALSE RECORD at its carrying commit -- mg-c3a2's class.
      HELD-DRIFTED  every decision is the same, but a FIGURE INSIDE one of them
                    moved.  The verdict stands and a stated number does not.
      HELD          every decision and every figure inside one is unchanged;
                    only surrounding prose or non-verdict rows moved.  True of
                    the tree it measured -- mg-b2af's class.
      NO-VERDICT    the transcript states no conclusion this instrument reads.
    """
    la, lb = verdict_lines(committed), verdict_lines(rerun)
    if not la and not lb:
        return "NO-VERDICT"
    if verdict_tags(committed) != verdict_tags(rerun):
        return "FLIPS"
    return "HELD" if la == lb else "HELD-DRIFTED"


# -------------------------------------------------- the proposed convention

CODE_SUFFIXES = (".py", ".sh")
DECLARE_PREFIX = "code-digest:"
REACH_PREFIX = "reads-outside-tree:"


def code_digest(directory, rev):
    """A digest over the PRODUCING CODE of a directory at a revision.

    Only `.py` and `.sh` blobs are included.  `out_*.txt` and `.md` are
    excluded ON PURPOSE and the exclusion is the whole design: a digest that
    covered the transcripts would be invalidated by the act of committing them,
    so every transcript would ship already stale and the check would be a
    ritual.  That is mg-bf79's "a publisher is not a pin", and it is the trap
    this convention is shaped to avoid.

    Returns None if the directory holds no producing code at that revision.
    """
    import hashlib
    rows = []
    for line in git("ls-tree", "-r", "%s:%s" % (rev, directory)).split("\n"):
        if not line.strip():
            continue
        meta, name = line.split("\t", 1)
        sha = meta.split()[2]
        if name.endswith(CODE_SUFFIXES):
            rows.append("%s %s" % (name, sha))
    if not rows:
        return None
    return hashlib.sha256("\n".join(sorted(rows)).encode()).hexdigest()[:16]


def declared_digest(text):
    """The `code-digest:` a transcript declares about itself, or None."""
    m = re.search(r"^\s*%s\s*([0-9a-f]{8,64})" % re.escape(DECLARE_PREFIX),
                  text, re.M)
    return m.group(1) if m else None


def provenance_block(directory, rev="HEAD"):
    """The header this census proposes every transcript should carry.

    It states WHAT CODE produced the transcript, in a form that survives a
    rebase (blob shas, not commit shas) and is not disturbed by committing the
    transcript itself.  It deliberately does NOT state a commit sha: a commit
    sha is displaced by every rebase and is exactly the recording this arc has
    now been burned by four times.
    """
    dig = code_digest(directory, rev) or "(no producing code at %s)" % rev
    return ("%s %s   (sha256/16 over the sorted `.py`/`.sh` blob shas of "
            "%s;\n    NOT a commit sha -- a commit sha is displaced by every "
            "rebase, a blob digest is not)"
            % (DECLARE_PREFIX, dig, directory))


# ----------------------------------------------------------------- output

class Ledger(object):
    """The arc's exit convention, taken from code/repair_b2af/run_all.sh:
    exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.  A FINDING is a fact about
    the SUBJECT; a SELF-ERROR is a fault in THIS instrument.  They are counted
    apart because a script that exits 1 for both cannot distinguish `I found
    what I was sent to find` from `I am broken`.
    """

    def __init__(self, title, reads_outside_tree=True):
        self.findings = 0
        self.self_errors = 0
        print("=" * 78)
        print(title)
        print("=" * 78)
        # FIRST ADOPTER.  This census proposes the convention in t5 and obeys
        # it here, in its own transcripts, before asking anything else to.
        print("    " + provenance_block("code/" + SELF_DIR, "HEAD"))
        print("    %s %s" % (REACH_PREFIX, "yes" if reads_outside_tree else "no"))
        if reads_outside_tree:
            print("    ^ THIS TRANSCRIPT IS NOT PINNABLE BY ANY TREE.  It reads"
                  " repository-global state\n      -- refs, history, the file "
                  "list of `main` -- so it is a fact about the object store as"
                  " it\n      stood at the run, and the NEXT commit anyone "
                  "makes displaces it.  Declaring that\n      is the only "
                  "honest thing an instrument in this class can do.")

    def head(self, s):
        print()
        print("-" * 78)
        print(s)
        print("-" * 78)

    def record(self, ok, msg):
        """ok=True passes, ok=False is a FINDING about the subject, ok=None is
        a measurement with no pass/fail attached."""
        if ok is None:
            tag = "[MEASURED ]"
        elif ok:
            tag = "[OK       ]"
        else:
            tag = "[FINDING  ]"
            self.findings += 1
        print("%s %s" % (tag, msg))

    def self_error(self, msg):
        self.self_errors += 1
        print("[SELF-ERR ] %s" % msg)

    def done(self):
        print()
        print("SELF-ERRORS %d" % self.self_errors)
        print("FINDINGS %d" % self.findings)
        print("TOTAL BAD: %d" % (self.self_errors + self.findings))
        return 1 if (self.findings or self.self_errors) else 0


def main_rev(argv=None):
    """`--at <rev>` so every script of this census can be run as of any commit.
    Defaults to `main`, NOT to HEAD: the census is about what is published."""
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--at" in argv:
        i = argv.index("--at")
        return argv[i + 1]
    return "main"
