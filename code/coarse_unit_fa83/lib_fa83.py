"""mg-fa83 — THE FRAME, THE SANDBOX AND THE ARM RUNNER.  One definition of each, here.

WHAT THE FRAME IS.  A control `C` guards a property `P` of a corpus.  `C` decides over a
CONTROL UNIT — the granularity at which it compares — and `P` is a property of a GUARDED
UNIT.  When the control unit is strictly coarser, `C`'s fibres contain corpora that differ in
`P`, so `C` is necessary and cannot be sufficient.  A WITNESS is a pair of trees with

    C(base) == C(mutant)        the control's own decision is unmoved, and
    P(mutant) is false          by a measurement that does not go through C.

That second line is the half that is easy to skip and the half that makes this a measurement
rather than an opinion, so every recipe here carries a `damage()` that returns a NUMBER
computed from the tree — never from the arm's output.

THE ARMS ARE RUN, NOT RE-SPELLED (mg-d2c2).  Every verdict below comes from executing the
real `.py` file as a subprocess against a tree the arm resolves for itself.  Nothing here
imports an arm, re-implements its rule, or reads its committed transcript: a re-spelling makes
every finding a statement about the re-spelling, and a committed transcript is an answer about
some other tree.

THE SANDBOX IS SYMLINKS, AND THE REASON IS AN ARITHMETIC ONE.  The corpus is 41 MB over 3 216
files and every recipe needs its own tree.  `build_tree` materialises real directories only
along the paths a recipe mutates and symlinks everything else, so a tree costs milliseconds
and the mutated files are the only real bytes in it.  Each arm derives its own ROOT from
`os.path.abspath(__file__)` of the path it was INVOKED with — `abspath` does not resolve
symlinks, `realpath` would — so an arm invoked at `<sandbox>/code/<dir>/<arm>.py` reads
`<sandbox>/STATE.md`, which is the whole trick.

THE HAZARD THAT CREATES, NAMED AND CONTROLLED.  A symlinked file written through is the REAL
file written.  Nothing here runs an arm that writes (the four are report-only; the runners
that write are `run_all.sh`, which is not invoked), and `w0` asserts the four documents'
digests are unmoved across the whole run — the check, not the intention, is what makes it
true.

WHAT THIS SANDBOX CANNOT DO, so that a green is not over-read: it carries no `.git`, so an arm
that asks git anything cannot be exercised here.  `twin_pin.py` section 7 says so itself and
grades that REPORTED, NOT GRADED; sections 1-6 and 8 ask git nothing and are exercised.  An
arm whose decision is ENTIRELY git-valued is out of this population and is named in `w1` §0
rather than silently omitted.
"""

import hashlib
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
HERE = os.path.dirname(os.path.abspath(__file__))

STATE_REL = "STATE.md"
FACTS_REL = "docs/FACTS.md"
CONCEPTS_REL = "docs/CONCEPTS.md"

# The four documents whose bytes this directory must never move.  `w0` digests them before and
# after the whole run.
GUARDED_DOCS = (STATE_REL, FACTS_REL, CONCEPTS_REL, "docs/state-of-the-wall.html")


class Refusal(Exception):
    """This instrument could not reach its own decision.  Never mapped onto a verdict."""


# ---------------------------------------------------------------------------------------
# reading the real corpus
# ---------------------------------------------------------------------------------------

def read(rel):
    path = os.path.join(ROOT, rel)
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        raise Refusal("cannot read %s: %s" % (rel, exc))


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def doc_digests():
    """The four guarded documents, keyed by repository-relative path."""
    out = {}
    for rel in GUARDED_DOCS:
        p = os.path.join(ROOT, rel)
        out[rel] = digest(open(p, encoding="utf-8").read()) if os.path.exists(p) else "(absent)"
    return out


# ---------------------------------------------------------------------------------------
# the sandbox
# ---------------------------------------------------------------------------------------

def build_tree(dest, mutations):
    """A tree identical to the corpus except at `mutations` — {relpath: text or None}.

    None deletes.  Directories along a mutated path are REAL; everything else is a symlink
    into the corpus, so this costs milliseconds rather than 41 MB.
    """
    if os.path.exists(dest):
        shutil.rmtree(dest)
    materialise = {""}
    for rel in mutations:
        parts = rel.split("/")
        for i in range(len(parts)):
            materialise.add("/".join(parts[:i]))

    def rec(rel):
        src = os.path.join(ROOT, rel) if rel else ROOT
        dst = os.path.join(dest, rel) if rel else dest
        os.makedirs(dst, exist_ok=True)
        for name in sorted(os.listdir(src)):
            if not rel and name == ".git":
                continue          # a sandbox that can reach the real .git is not a sandbox
            crel = (rel + "/" + name) if rel else name
            if crel in mutations:
                continue          # written below, as a real file
            child = os.path.join(src, name)
            if os.path.isdir(child) and crel in materialise:
                rec(crel)
            else:
                os.symlink(child, os.path.join(dst, name))

    rec("")
    for rel, content in sorted(mutations.items()):
        path = os.path.join(dest, rel)
        if content is None:
            if os.path.lexists(path):
                os.remove(path)
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
    return dest


# ---------------------------------------------------------------------------------------
# running an arm
# ---------------------------------------------------------------------------------------

# THE ARMS, and what each one's decision is.  `verdict_re` picks the ONE line that carries the
# arm's own decision; `subject` is the document the arm's docstring says it is about, and it is
# what makes the in-subject / out-of-subject split below a reading of the arm rather than mine.
ARMS = (
    ("e331", "code/state_ratchet_e331/ratchet.py", STATE_REL,
     re.compile(r"^RATCHET VERDICT: (\S+)")),
    ("03cf", "code/facts_registry_03cf/f0_registry_discipline.py", FACTS_REL,
     re.compile(r"^VERDICT: (\S+)")),
    ("602d", "code/concepts_gate_602d/c0_concept_discipline.py", CONCEPTS_REL,
     re.compile(r"^VERDICT: (\S+)")),
    ("9bc2", "code/rendered_twin_pin_9bc2/twin_pin.py", STATE_REL,
     re.compile(r"^VERDICT: (\S+)")),
)

ARM_BY_ID = {a[0]: a for a in ARMS}

# Wall-clock, sandbox paths and absolute paths are scrubbed out of every quoted line.  An
# instrument whose transcript carries the operator's temp directory reproduces for exactly one
# operator and for nobody else, ever (mg-bdb0).
_SECONDS = re.compile(r"\b\d+\.\d+\s*s\b")


def scrub(text, sandbox=None):
    if sandbox:
        text = text.replace(sandbox, "<sandbox>")
    text = text.replace(ROOT, "<repo>")
    return _SECONDS.sub("<t>s", text)


def run_arm(arm_id, tree):
    """Execute the real arm against `tree`.  Returns (exit, grade, decision_line)."""
    _, rel, _subject, verdict_re = ARM_BY_ID[arm_id]
    path = os.path.join(tree, rel)
    if not os.path.exists(path):
        raise Refusal("%s is not in the tree at %s" % (rel, tree))
    proc = subprocess.run([sys.executable, "-u", path], capture_output=True, text=True)
    body = proc.stdout + proc.stderr
    line, grade = None, None
    for raw in body.splitlines():
        m = verdict_re.match(raw)
        if m:
            line, grade = raw, m.group(1)
    if grade is None:
        # A TRACEBACK AND A FINDING LEAVE THE SAME EXIT CODE (mg-9876), so a missing decision
        # line is its own class — and it is TWO classes, not one, which is the distinction
        # that decides whether the estate caught something or merely fell over:
        #
        #   REFUSED  the arm printed a refusal and declined to decide.  That is a DESIGNED
        #            default-deny — c0's `a rename must be LOUD` — and it blocks the merge on
        #            purpose.  It counts as the estate catching the mutation.
        #   CRASH    an uncaught exception.  It blocks too, and it is NOT a catch: nothing
        #            detected anything, and crediting it would let any control claim coverage
        #            it does not have.
        refused = any(l.lstrip().startswith("REFUSED") or l.startswith("VERDICT: REFUSED")
                      for l in body.splitlines())
        tail = [l for l in body.strip().splitlines() if l.strip()][-1:]
        return (proc.returncode, "REFUSED" if refused else "CRASH",
                scrub(tail[0] if tail else "(no output)", tree))
    return proc.returncode, grade.rstrip(".,"), scrub(line, tree)


def decision(arm_id, tree):
    """THE UNIT A WITNESS IS COMPARED IN, and it is three fields rather than one.

    Exit code, grade word AND THE WHOLE SCRUBBED DECISION LINE.  The first draft of this
    directory compared (exit, grade) and `w0` D6 is the witness against it: `f0` prints
    `VERDICT: GREEN — 26 entries`, so a tree that GAINS a valid entry leaves the pair
    (0, GREEN) exactly where it was while the arm's own sentence moves.  A `WITNESS` declared
    in that unit would have been this directory's own subject, in this directory, so the unit
    was made finer rather than the finding softened.

    It is still coarser than the arm's whole output, which is said here rather than implied:
    a change confined to a line the arm does not carry into its decision is invisible in this
    unit, exactly as `w1` §5 item 1 says of the population.
    """
    rc, grade, line = run_arm(arm_id, tree)
    return (rc, grade, line), line


# ---------------------------------------------------------------------------------------
# the fine-unit measurements — `wrong` is a number, never an adjective
# ---------------------------------------------------------------------------------------

def token_stats(text):
    lines = text.split("\n")
    return {
        "words": len(text.split()),
        "bytes": len(text.encode("utf-8")),
        "lines": len(lines),
        "max_line_chars": max((len(l) for l in lines), default=0),
        "max_token_chars": max((len(t) for t in text.split()), default=0),
    }


def inflate_preserving_words(text, width=2000, filler="x"):
    """Same token COUNT, every token `width` characters.  `len(text.split())` is unmoved and
    everything a reader cares about is not."""
    n = len(text.split())
    return "\n".join([filler * width] * n) + "\n"


LEDGER_ROW = re.compile(r"^\|\s*(\d+[ab]?)\s*\|")


def ledger_line_numbers(text):
    """0-based indices of STATE.md lines that are ledger table rows.  The ledger is what
    `twin_pin.py` section 2 digests per row; everything else in the file is not."""
    return [i for i, l in enumerate(text.split("\n")) if LEDGER_ROW.match(l)]


def replace_words_outside(text, keep_line_numbers, filler="lorem"):
    """Every line NOT in `keep_line_numbers` has its words replaced by `filler`, one for one.

    Per-line word preservation, not whole-file: it keeps the total unmoved (so the ratchet
    cannot see it) without depending on where the difference lands.
    """
    keep = set(keep_line_numbers)
    out = []
    for i, line in enumerate(text.split("\n")):
        if i in keep:
            out.append(line)
        else:
            out.append(" ".join([filler] * len(line.split())))
    return "\n".join(out)


def surviving_word_share(original, mutant):
    """The share of the original's tokens that the mutant still carries, position by position.
    1.0 means nothing moved; 0.0 means the document is gone."""
    a, b = original.split(), mutant.split()
    if not a:
        raise Refusal("surviving_word_share() was handed an empty original")
    same = sum(1 for x, y in zip(a, b) if x == y)
    return same / float(len(a))
