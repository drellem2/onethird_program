"""mg-223d -- the instrument for THE DURABILITY OF THE ARC'S PINNED REFS.

WHAT THIS FILE MAY AND MAY NOT CONTAIN, GIVEN WHAT IT IS ABOUT.  The subject is
a dependence on git objects staying reachable.  A library for that must not
become a second opinion about what a commit is, what an ancestor is, or which
directories the arc has -- there are already answers to all three in this arc,
and a second definition that agrees today is worse than the first.  So:

  IMPORTED, NEVER RESTATED.
    `lib_1abe`  -- `resolve`, `is_ancestor`, `patch_id`, `git`, `git_ok`,
                   `Ledger`, `provenance_block`, `code_digest`,
                   `shas_named_in`.  mg-1abe worked out the R1/R2/R3
                   declaration and the sha-token rule; re-typing either would
                   turn a disagreement about REACHABILITY into a disagreement
                   about parsing.
    `lib_f8e5`  -- `suite_dirs`.  The arc's directory population, already
                   agreed at 174-179 depending on the rev, already used by the
                   census that adopted R3 over the whole arc.
    `lib9160`   -- `corpus`, `parent_corpus`, `PARENT_REV`, `PARENT_PUB`.  THE
                   SUBJECT.  Every number this tree prints about the
                   reconstruction is taken by CALLING it, never by re-deriving
                   what it does.  In particular `twin_swap()` monkeypatches
                   `PARENT_REV` and calls the SAME function, so the two rows it
                   prints differ in one constant and in nothing else.

  WRITTEN HERE, AND WHY EACH IS NOT A COPY.

    `pins`          THE POPULATION RULE, and the whole of the correction.  A
                    *pin* is a quoted hex literal in a tracked `*.py`/`*.sh`
                    that resolves to a commit.  Nothing in the arc has this
                    rule.  `lib_1abe.shas_named_in` is its nearest relative and
                    it is a different rule on purpose: that one reads a
                    TRANSCRIPT'S bytes and answers `what does this record
                    mention`, this one reads EXECUTABLE bytes and answers `what
                    must still resolve for this to run`.  A record naming a
                    dead commit is a broken claim; a pin naming a dead commit
                    is a broken instrument, and the remedies are not the same.
    `sightings`     the WIDEST rule, for contrast and for an upper bound: any
                    hex token 7-40 anywhere in any tracked file.  It exists so
                    that the number this tree reports can be compared with the
                    number it would have reported if it had not drawn the
                    distinction, and so that the gap is a measurement rather
                    than a claim about my own restraint.
    `holders`       which refs keep a commit alive, WITH THIS WORKTREE'S OWN
                    BRANCH EXCLUDED BY DEFAULT.  That exclusion is E7: a commit
                    whose only holder is the branch I am about to have merged
                    and pruned is not safe, and a checker that counts its own
                    ref reports safety it created.
    `collision_rate` the NEGATIVE CONTROL for the whole population rule.
                    Random hex tokens of the same length, resolved the same
                    way.  Without it, `it resolves, so it is a reference` is an
                    assumption; with it, it is a measured false-positive rate.
    `twin_of`       the on-main patch-id twin of an off-history commit, or
                    None.  Used to EXHIBIT the cause, never to substitute.
    `twin_swap`     the one probe that answers whether the twin IS a
                    substitute, by running `lib9160.parent_corpus` twice.
    `PIN_CLASS`     REQUIRED / RECORD, the two-tier verdict this tree adds.

WHAT THIS TREE NEVER DOES.  It writes nothing outside its own directory and it
CREATES NO REF -- not in `run_all.sh` and not in any probe here.  The tags this
ticket proposes are made by `mktags.sh`, which is NOT part of the suite, prints
the commands, and requires an explicit `--yes` to run them.  A suite that
silently mutated the ref namespace of the repository it is auditing would be
the same defect one level up.  `x1_gc.py` is the one probe that runs `git gc`,
it does it in a THROWAWAY CLONE under a path you name, and it refuses to start
if that path is inside this repository.
"""

import os
import random
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

for _p in ("code/transcript_census_1abe", "code/census_remainder_f8e5",
           "code/runner_exit_audit_56dc", "code/grain_axis_audit_03d1",
           "code/grain_arity_9160"):
    sys.path.insert(0, os.path.join(REPO, _p))

import lib_1abe as C          # noqa: E402  resolve / is_ancestor / patch_id / Ledger
import lib_f8e5 as F          # noqa: E402  suite_dirs

TREE = "code/pinned_ref_durability_223d"
SELF_DIR = "pinned_ref_durability_223d"

git = C.git
git_ok = C.git_ok
resolve = C.resolve
is_ancestor = C.is_ancestor
patch_id = C.patch_id
suite_dirs = F.suite_dirs


def bar(title, ch="="):
    print()
    print(ch * 74)
    print(title)
    print(ch * 74)


class Ledger(C.Ledger):
    """mg-1abe's ledger with the R1 declaration pointed at THIS directory.

    THE SUBCLASS IS NOT COSMETIC AND IT IS NOT MY IDEA.  `C.Ledger.__init__`
    calls `provenance_block("code/" + SELF_DIR)` with `SELF_DIR` bound in ITS
    module, so a tree that imports it unmodified declares
    `code/transcript_census_1abe`'s digest as its own -- a TRUE digest of the
    WRONG directory, which the R3 control would call green because it agrees.
    mg-f8e5 committed that defect, caught it, and wrote it up; inheriting the
    fix rather than rediscovering it is the point of importing.
    """

    def __init__(self, title, reads_outside_tree=True):
        self.findings = 0
        self.self_errors = 0
        print("=" * 78)
        print(title)
        print("=" * 78)
        print("    " + C.provenance_block("code/" + SELF_DIR, "HEAD"))
        print("    %s %s" % (C.REACH_PREFIX,
                             "yes" if reads_outside_tree else "no"))
        if reads_outside_tree:
            print("    ^ THIS TRANSCRIPT IS NOT PINNABLE BY ANY TREE.  It reads"
                  " repository-global state\n      -- refs, reachability, the "
                  "history of `main` -- so it is a fact about the object store"
                  "\n      as it stood at the run.  For THIS tree that is not "
                  "a caveat, it is the\n      subject: every number below is a"
                  " statement about what is reachable TODAY.")


# ---------------------------------------------------------------------------
# THE POPULATION RULES.  Two of them, and the difference between them is the
# finding this tree is here to keep from being over-reported.
# ---------------------------------------------------------------------------

_LITERAL = re.compile(r'''["']([0-9a-f]{7,40})["']''')
_TOKEN = re.compile(r'(?<![0-9a-zA-Z])([0-9a-f]{7,40})(?![0-9a-zA-Z])')


def tracked(rev="HEAD"):
    """Every tracked path at `rev`.  The denominator of both rules."""
    return sorted(p for p in git("ls-tree", "-r", "--name-only",
                                 rev).split("\n") if p.strip())


def _text(path):
    try:
        with open(os.path.join(REPO, path), "rb") as fh:
            return fh.read().decode("utf-8")
    except (IOError, OSError, UnicodeDecodeError):
        return None


def pins(rev="HEAD"):
    """{short: [(path, line, text)]} -- QUOTED hex literals in tracked code.

    THE RULE, STATED SO THAT WHAT IT CANNOT SEE IS VISIBLE (E1).  A pin is a
    7-40 character hex run between matching quotes in a tracked `*.py` or
    `*.sh`.  It therefore CANNOT SEE:

        - a rev built by concatenation (`"9f1ec" + "aa"`),
        - a rev read at run time out of a `.md`, `.json` or `.txt`,
        - a rev passed on a command line or taken from the environment,
        - a rev in a language this arc does not use.

    That list is the rule's blind side and it is printed by `r1` rather than
    left in a docstring, because a population whose limits are only in the
    source is a population nobody checked.
    """
    out = {}
    for p in tracked(rev):
        if not (p.endswith(".py") or p.endswith(".sh")):
            continue
        t = _text(p)
        if t is None:
            continue
        for i, line in enumerate(t.split("\n"), 1):
            for m in _LITERAL.finditer(line):
                out.setdefault(m.group(1), []).append((p, i, line.strip()))
    return out


def sightings(rev="HEAD"):
    """{short: [paths]} -- ANY hex token 7-40 in ANY tracked file.

    The widest rule the arc could apply, kept so the gap between it and `pins`
    is a printed number.  Most of what this returns is a RECORD -- a transcript
    saying what a commit was -- and a record is not a dependence.
    """
    out = {}
    for p in tracked(rev):
        t = _text(p)
        if t is None:
            continue
        for m in _TOKEN.finditer(t):
            out.setdefault(m.group(1), set()).add(p)
    return {k: sorted(v) for k, v in out.items()}


def commits(tokens):
    """{short: full} for every token that resolves to a COMMIT.

    One `git cat-file --batch-check` for the whole set, so a sweep over the
    corpus costs one subprocess rather than one per token.  Reading only.
    """
    toks = list(tokens)
    if not toks:
        return {}
    r = subprocess.run(["git", "cat-file", "--batch-check"], cwd=REPO,
                       input="\n".join(t + "^{commit}" for t in toks),
                       capture_output=True, text=True)
    out = {}
    for tok, line in zip(toks, r.stdout.split("\n")):
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "commit":
            out[tok] = parts[0]
    return out


def collision_rate(n=400, length=7, seed=223):
    """(hits, n) for `n` RANDOM hex tokens resolved exactly as `commits` does.

    THE NEGATIVE CONTROL FOR THE POPULATION RULE.  `it resolves, therefore it
    is a reference` is an assumption until this number is on the page.  The
    seed is fixed so the transcript reproduces; the length is a parameter
    because the rate is a function of it and a single number would hide that.
    """
    rnd = random.Random(seed)
    toks = ["".join(rnd.choice("0123456789abcdef") for _ in range(length))
            for _ in range(n)]
    return len(commits(toks)), n


# ---------------------------------------------------------------------------
# REACHABILITY.
# ---------------------------------------------------------------------------

def self_ref():
    """This worktree's own branch ref, or None if detached."""
    b = git("rev-parse", "--abbrev-ref", "HEAD").strip()
    return None if b in ("", "HEAD") else "refs/heads/" + b


def holders(full, exclude_self=True):
    """Every ref from which `full` is reachable.

    E7 IS WHY `exclude_self` DEFAULTS TO TRUE.  This runs on a polecat branch
    that is about to be merged and pruned.  A commit whose only holder is that
    branch is not durable, and a checker that counts its own ref reports a
    safety it manufactured.  The parameter exists so `r0` can show the answer
    changing when it is turned off, rather than my asserting that it would.
    """
    refs = [x for x in git("for-each-ref", "--contains", full,
                           "--format=%(refname)").split("\n") if x.strip()]
    if exclude_self:
        me = self_ref()
        refs = [r for r in refs if r != me]
    return refs


def durable_holders(full):
    """Holders that survive branch pruning: tags, and `main` itself."""
    return [r for r in holders(full)
            if r.startswith("refs/tags/") or r in ("refs/heads/main",
                                                   "refs/remotes/origin/main")]


PIN_REQUIRED = "REQUIRED"   # executable code resolves this or does not run
PIN_RECORD = "RECORD"       # a transcript or doc names it; nothing runs on it


def pin_class(short, pinset, sightset):
    if short in pinset:
        return PIN_REQUIRED
    if short in sightset:
        return PIN_RECORD
    return "UNSEEN"


# ---------------------------------------------------------------------------
# THE CAUSE: pre-rebase twins.
# ---------------------------------------------------------------------------

def main_patch_ids(n=400, rev="main"):
    """{patch_id: commit} over the last `n` commits of `rev`."""
    out = {}
    for r in git("rev-list", rev, "-n", str(n)).split():
        p = patch_id(r)
        if p:
            out.setdefault(p, r)
    return out


def twin_of(full, table=None):
    """The on-main patch-id twin of `full`, or None.

    EXHIBITS the cause.  It is NEVER used to substitute one ref for another --
    that is E4, it is what the ticket forbids in its own words, and `r3`
    measures what it would cost rather than doing it.
    """
    table = main_patch_ids() if table is None else table
    p = patch_id(full)
    return table.get(p) if p else None


# ---------------------------------------------------------------------------
# THE RECONSTRUCTION.  Called, never re-derived.
# ---------------------------------------------------------------------------

def _libs():
    """(lib9160, libfd9c) -- imported late so `r1`/`r2` cost nothing for them.

    BOTH ARE IMPORTED, NEITHER IS RESTATED.  `parent_corpus` is mg-9160's
    reconstruction and `census` is mg-fd9c's five-column composition of it.
    Writing either here would make a disagreement about REACHABILITY into a
    disagreement about who typed the census, which is the failure mg-9160's own
    header warns about at length.
    """
    sys.path.insert(0, os.path.join(REPO, "code/corpus_fixedpoint_fd9c"))
    import lib9160
    import libfd9c
    return lib9160, libfd9c


def reconstruction_row(parent_rev=None):
    """{files,rows,erows,eints,words} from mg-9160's OWN parent_corpus().

    `parent_rev` swaps `lib9160.PARENT_REV` for the duration of the call and
    puts it back in a `finally`.  The two rows `r3` prints therefore differ in
    ONE CONSTANT and in nothing else, which is the only way `the twin is not a
    substitute` is a measurement rather than an argument.

    NOTHING HERE WRITES THE FIGURE BACK.  The swap is in memory, the constant
    is restored, and `lib9160.py` is not edited by this tree -- E4.
    """
    G, U = _libs()
    old = G.PARENT_REV
    try:
        if parent_rev is not None:
            G.PARENT_REV = parent_rev
        pairs = G.parent_corpus()
        c = U.census(G.B.read(p, r) for p, r in pairs)
        return {k: c[k] for k in ("files", "rows", "erows", "eints", "words")}
    finally:
        G.PARENT_REV = old


# ---------------------------------------------------------------------------
# THE MANIFEST.  What the repair actually is.
# ---------------------------------------------------------------------------

MANIFEST = os.path.join(HERE, "PINS.tsv")


def manifest_rows():
    """[(short, full, tag, tree, note)] read from the committed PINS.tsv.

    The manifest is a TRACKED FILE, so `r4`'s control is a check of the
    repository against a declaration a human committed -- not a check of a
    sweep against itself, which is the shape that cannot fail.
    """
    rows = []
    if not os.path.exists(MANIFEST):
        return rows
    with open(MANIFEST, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            while len(parts) < 5:
                parts.append("")
            rows.append(tuple(parts[:5]))
    return rows


def tag_name(full):
    """The keep-alive tag for a pinned COMMIT.  Argument is the full sha.

    E3 IS WHY THE PREFIX IS `pin/`.  A tag named after this ticket would read
    as though mg-223d blessed the commit.  These are keep-alive anchors and
    nothing else; the name says only that something pins it.

    E2 IS WHY THE ARGUMENT IS THE FULL SHA AND NOT THE TOKEN.  `3738079` and
    `37380799` are two pin ROWS and one COMMIT; naming the tag after the token
    would put two tags on one object and quietly make the tag count a count of
    tokens.  One object, one anchor.
    """
    return "pin/" + full[:7]


def check_pins():
    """[(short, verdict, detail)] -- THE CONTROL.

    Verdicts, and each is a different remedy:

      OK-TAGGED    a tag holds it; gc cannot collect it.
      OK-ON-MAIN   it is an ancestor of main; nothing to do.
      AT-RISK      it resolves, and every holder is a prunable branch.
      DEAD         it does not resolve.  No remedy from inside this repo.
      UNDECLARED   the code pins it and `PINS.tsv` does not list it.
    """
    declared = {r[0]: r for r in manifest_rows()}
    ps = pins()
    res = commits(ps.keys())
    out = []
    for short in sorted(res):
        full = res[short]
        if is_ancestor(full, "main"):
            continue
        if short not in declared:
            out.append((short, "UNDECLARED",
                        "pinned at %s and absent from PINS.tsv" % ps[short][0][0]))
            continue
        dh = durable_holders(full)
        if dh:
            out.append((short, "OK-TAGGED", ", ".join(dh)))
        else:
            out.append((short, "AT-RISK",
                        ", ".join(holders(full)) or "NO REF AT ALL"))
    for short, row in sorted(declared.items()):
        full = resolve(short)
        if not full:
            out.append((short, "DEAD", "declared in PINS.tsv and unresolvable"))
    return out
