"""mg-585e — shared plumbing for "can a self-exempting transcript be made non-oscillating?"

THE SUBJECT IS ONE FILE AND A PROPERTY THAT IS NOT ABOUT THAT FILE.

⚠ READ THIS DIRECTORY AS A RECORD OF A QUESTION AND ITS ANSWER, NOT AS A DESCRIPTION OF THE
TREE.  Everything below is written in the present tense about an exemption that mg-c15e has
since DELETED: `lib_f771.SELF_EXCLUDED` no longer exists, `g0`'s watched class is total, and
`g0`'s §2 is the rule inventory this directory proposed.  The prose is left as it was written
because it is the argument that produced the change; the three places where it had to become
an EDIT rather than a note are INVENTORY below, `v0`'s R1/R3 (the refusal moved to stderr with
the outcome) and `v2` §3 (the surface it locates is gone).  §6 of the README is where the
question was put; mg-c15e is the answer.

`code/gate_fixed_point_f771/out_g0_fixed_point.txt` is mg-f771's single self-exemption from
its own watched class.  `lib_f771.SELF_EXCLUDED` gives the reason as: the transcript is
written AFTER the measurement and its text depends on the verdict, so a red run's transcript
is committed alongside the refresh that makes the tree green, and the next run grades it
DISAGREES.

THAT REASON IS TRUE AND IT IS A SYMPTOM.  The operative property is sharper and it is not
about verdicts at all:

    g0 is run at tree T and its output is committed into tree T'.
    The repair that produces T' from T is "commit the regenerated transcripts".
    g0's §2 reports D(T) — the set of transcripts whose committed copy disagrees.
    D(T') = {} BY DEFINITION OF THE REPAIR.
    So whenever D(T) is non-empty, the committed text is false about the tree it is
    committed into, and it is false BECAUSE the commit repaired it.

A transcript cannot record a quantity that its own commit sets to zero.  Nothing about
"verdict" is needed to say that, and stating it that way is what makes it decidable which
OTHER content is safe: content survives if it is INVARIANT UNDER THE REPAIR, and the repair
rewrites transcript BYTES and nothing else.  So the membership of the watched class survives,
the normaliser's source survives, and the disagreement set is exactly what does not.

THIS IS WHY `g0`'s OWN DOCSTRING RULE IS THE MISTAKE.  It says "Only the DISAGREES list,
which is repo state, is on stdout".  The DISAGREES list IS a function of repo state — of the
tree at run time, which is not the tree the file is committed into.  "Is it repo state" is the
wrong test; "does the repair move it" is the right one, and they disagree on exactly one item,
which happens to be the whole of §2.

WHAT IS IN HERE.  Three things and no verdicts:

  1.  A SANDBOX BUILDER.  Two (three) miniature repositories that differ only in whether a
      watched transcript disagrees.  The real `g0_fixed_point.py` and `lib_f771.py` are COPIED
      IN and run as subprocesses against them.  Copying rather than importing is deliberate:
      `lib_f771.ROOT` is computed from the module's own location, so a copy at
      `<sandbox>/code/gate_fixed_point_f771/` is the only way to point the real arm at a tree
      that is not this one, and re-implementing its decision here would make every finding a
      statement about the re-implementation (mg-d2c2's rule, and mg-f771's own g1 obeys it).

  2.  A TIMING SCRUB, WRITTEN HERE RATHER THAN IMPORTED, AND THE REASON IS NOT PURITY.
      Comparing two `g0` stdouts requires eating the `%.2fs` field, and `lib_f771.N2` eats
      exactly that.  Importing it would make "the two runs agree" a statement computed with
      the subject's own normaliser — a consistency check wearing a measurement's clothes.  So
      `scrub_seconds` is four lines written here.  IT IS NOT INDEPENDENT IN SHAPE, and that is
      said rather than glossed: there is one obvious regex for "a decimal followed by s" and
      both files contain it.  What independence buys is that a widening of N2 cannot silently
      widen this arm's agreement test; it buys nothing else, and is not claimed to.

  3.  THE PROPOSED WRITER, `invariant_report`.  The candidate answer to the ticket: a
      transcript whose text is a function of the verdict's INPUTS rather than its OUTCOME.
      Its content is the watched-class rule, the exemption list, the normaliser's rule
      inventory in readable form, and a digest of the four functions that actually decide.
      Every one of those is invariant under the repair, and none of them is constant.
"""

import hashlib
import os
import re
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

F771_DIR = os.path.join(ROOT, "code", "gate_fixed_point_f771")
F771_REL = "code/gate_fixed_point_f771"
F771_TRANSCRIPT = "code/gate_fixed_point_f771/out_g0_fixed_point.txt"

# The freshness handshake g0 demands.  Named here because the sandbox runs must set it or
# every sandbox run is a REFUSED and this whole directory measures nothing.
FRESH_ENV = "BUILD_SH_RAN_THE_SUITES"

# AS_OF.  v1 walks the history of ONE file, and that history GROWS with every landing —
# including this branch's own.  Walked from HEAD, v1's transcript would move on every future
# commit to the file it measures, which is this directory reproducing its own subject one
# estate over.  So the walk is pinned, and the pin is CHECKED at run time: it must resolve and
# it must be an ancestor of origin/main (mg-e8b0's condition 1 applied to this arm's own
# provenance).  Everything v1 prints is then a function of two commits and cannot go stale.
AS_OF = "0cb0fa4c143f84ffc6d5b4e2284e7dbd780b95ce"

# A decimal second.  See §2 of the module docstring for why this is not imported.
SECONDS = re.compile(r"\b\d+\.\d+\s*s\b")


class Refused(Exception):
    """Raised when this instrument cannot reach a verdict, which is not a finding."""


def scrub_seconds(text):
    return SECONDS.sub("<t>s", text)


def scrub_roots(text, *roots):
    """Sandbox paths must never reach a tracked transcript — that is mg-f771's own defect and
    this directory would be committing it while describing it.  Applied to every captured
    stdout before anything is printed."""
    for r in sorted(roots, key=len, reverse=True):
        if r:
            text = text.replace(r, "<SANDBOX>")
    return text


def git(root, *args, **kw):
    try:
        return subprocess.run(("git", "-C", root) + args, capture_output=True, text=True, **kw)
    except OSError as exc:                                  # pragma: no cover - no git
        raise Refused("git is not runnable: %s" % exc)


def require_git(root=ROOT):
    p = git(root, "rev-parse", "--is-inside-work-tree")
    if p.returncode != 0 or p.stdout.strip() != "true":
        raise Refused("%s is not inside a git work tree" % root)


def require_as_of(root=ROOT):
    """The pin must resolve AND be reachable from origin/main.  A pin that resolves only in
    this worktree is a pin to a commit that may never land, and every figure hanging off it
    would be unreproducible for the next reader — which is the class of defect mg-e8b0's
    row-by-row sweep spent a tranche on."""
    require_git(root)
    p = git(root, "rev-parse", "--verify", "%s^{commit}" % AS_OF)
    if p.returncode != 0:
        raise Refused("AS_OF %s does not resolve in this repository" % AS_OF[:8])
    q = git(root, "merge-base", "--is-ancestor", AS_OF, "origin/main")
    if q.returncode != 0:
        raise Refused("AS_OF %s is not an ancestor of origin/main — a pin to a commit that "
                      "may never land is not a pin" % AS_OF[:8])
    return AS_OF


# ---------------------------------------------------------------------------------------
# THE SANDBOXES
# ---------------------------------------------------------------------------------------

_SAMPLE_GREEN = """\
sample suite transcript
  entries          20
  total       12.30s
VERDICT: GREEN — 20 entries
"""

# The RED tree's worktree copy asserts a DIFFERENT COUNT.  A count and not a timing, because
# a timing is N2 and would come back NOISE — the sandbox has to produce the verdict it claims
# to produce, which is what world C2 in v0 checks rather than assumes.
_SAMPLE_RED = """\
sample suite transcript
  entries          23
  total       12.30s
VERDICT: GREEN — 23 entries
"""

# The NOISE tree moves ONLY the wall clock.  It exists so that "green" is exercised in both
# of its shapes: nothing moved, and something moved that the normaliser forgives.
_SAMPLE_NOISE = """\
sample suite transcript
  entries          20
  total       11.70s
VERDICT: GREEN — 20 entries
"""

WORLDS = {"green": None, "noise": _SAMPLE_NOISE, "red": _SAMPLE_RED}


def build_sandbox(tmp, world, normaliser_patch=None):
    """A miniature repository holding a copy of the real g0 and one watched transcript.

    `world` is one of green / noise / red.  `normaliser_patch` is (old, new) applied to the
    copied `lib_f771.py`, used by the non-vacuity control to show that the proposed writer
    moves when the normaliser moves.  Returns the sandbox root.
    """
    if world not in WORLDS:
        raise Refused("unknown world %r" % (world,))
    dst = os.path.join(tmp, "code", "gate_fixed_point_f771")
    os.makedirs(dst)
    for name in ("lib_f771.py", "g0_fixed_point.py"):
        src = os.path.join(F771_DIR, name)
        if not os.path.exists(src):
            raise Refused("cannot find %s — this directory's whole subject is that file" % src)
        shutil.copyfile(src, os.path.join(dst, name))
    if normaliser_patch:
        old, new = normaliser_patch
        path = os.path.join(dst, "lib_f771.py")
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        if old not in text:
            raise Refused("normaliser patch anchor not present in lib_f771.py: %r" % old)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text.replace(old, new, 1))

    sample_dir = os.path.join(tmp, "code", "sample_suite")
    os.makedirs(sample_dir)
    sample = os.path.join(sample_dir, "out_sample.txt")
    with open(sample, "w", encoding="utf-8") as fh:
        fh.write(_SAMPLE_GREEN)

    for args in (("init", "-q", "-b", "main"),
                 ("add", "-A"),
                 ("-c", "user.email=mg-585e@local", "-c", "user.name=mg-585e",
                  "commit", "-q", "-m", "sandbox")):
        p = git(tmp, *args)
        if p.returncode != 0:
            raise Refused("sandbox git %s failed: %s" % (args[0], (p.stderr or "").strip()))

    replacement = WORLDS[world]
    if replacement is not None:
        with open(sample, "w", encoding="utf-8") as fh:
            fh.write(replacement)
    return tmp


def run_g0(sandbox):
    """Run the REAL arm against a sandbox.  Returns (rc, stdout, stderr), roots scrubbed."""
    env = dict(os.environ)
    env[FRESH_ENV] = "1"
    arm = os.path.join(sandbox, "code", "gate_fixed_point_f771", "g0_fixed_point.py")
    import sys
    p = subprocess.run([sys.executable, arm], capture_output=True, text=True, env=env)
    return (p.returncode,
            scrub_roots(p.stdout, sandbox, ROOT),
            scrub_roots(p.stderr, sandbox, ROOT))


# ---------------------------------------------------------------------------------------
# THE PROPOSED WRITER
# ---------------------------------------------------------------------------------------

# The four names that actually decide.  A digest over their SOURCE, because the readable
# inventory below can only show rules that are spelled as constants, and N3 is spelled as
# control flow.  A digest catches a widening it cannot describe; the inventory describes a
# widening it can.  Neither alone is enough and the pair is stated as a pair.
# THE PAREN IS LOAD-BEARING and it was not there in the first draft: D1 plants
# `def verdict_for_RENAMED(` and `"def verdict_for"` is a PREFIX of it, so the digest came
# back covering a function that no longer exists under the name it was asked about.  The
# plant fired on this library's own construction and the matcher was tightened rather than
# the plant relaxed.
#
# mg-05c6 LANDED WHILE THIS BRANCH WAS IN THE MERGE QUEUE AND WIDENED THE DECIDING SURFACE.
# `verdict_for` gained a third argument and two helpers — `corpus_pin` and `producer_pin` —
# and a whole class of transcript is now graded against a PIN rather than against the tree.
# They are added here rather than left out, because a digest that covers four of six deciding
# functions is D1's failure mode with a bigger blast radius: it reports the same field name
# while covering less.  That this list had to move IS the demonstration — the inventory tracks
# the instrument, which is the entire claim being made for it.
DECIDING = ("def normalise(", "def lines_equivalent(", "def texts_equivalent(",
            "def corpus_pin(", "def producer_pin(", "def verdict_for(")

# The constants that ARE spelled as constants, so a widening of them lands in a diff a reader
# can read rather than as a moved hash.  `CORPUS_SCOPED` and `CORPUS_DRIFT_LIMIT` are
# mg-05c6's, and they DECIDE — a path in that set is forgiven a difference that IS a function
# of repo state — so an inventory without them would be describing the instrument as it was
# yesterday.  Multi-line statements are carried WHOLE (see `_blocks`) rather than by their
# first line, or `CORPUS_SCOPED = {` would print as `{` and its membership would be invisible
# in both the inventory and the digest.
#
# `SELF_EXCLUDED` WAS IN THIS TUPLE AND IS NOT ANY MORE (mg-c15e).  It was removed here by the
# branch that removed the constant, because a list of rules that names one the instrument no
# longer has is not a shorter list, it is a REFUSAL: `read_inputs` raises, `v3` reaches no
# verdict and this suite exits 2.  The removal is the answer this directory asked for — §6
# put "should the exemption go?" to pm-onethird and mg-c15e landed the yes — so the tuple is
# the one place where the answer had to arrive as an edit rather than as prose.
INVENTORY = ("FS_ROOTS", "ABS_TO_REPO", "ABS_ANY", "SECONDS",
             "CORPUS_SCOPED", "CORPUS_DRIFT_LIMIT")


def _blocks(source, prefixes, what):
    """The full text of every top-level statement whose first line starts with one of
    `prefixes`, in file order.

    A top-level line ENDS the previous block, so a multi-line `def` or a multi-line literal is
    carried whole.  Nothing here nests; if that ever changes the block gets LARGER rather than
    smaller, which fails safe.  Missing exactly one prefix is a REFUSAL and not a shorter
    digest — a digest that silently covers less while printing the same field name is D1.
    """
    lines = source.splitlines(True)
    found = {}
    for i, ln in enumerate(lines):
        for pfx in prefixes:
            if ln.startswith(pfx) and pfx not in found:
                found[pfx] = i
    missing = [p for p in prefixes if p not in found]
    if missing:
        raise Refused("lib_f771.py does not define %s: %s — the instrument has been "
                      "restructured and this report is no longer about what it says it is "
                      "about" % (what, ", ".join(missing)))
    out = []
    for pfx in prefixes:
        s = found[pfx]
        e = s + 1
        while e < len(lines) and not (lines[e].strip() and not lines[e][:1].isspace()):
            e += 1
        out.append((pfx, "".join(lines[s:e])))
    return out


def _flatten(text, limit):
    """A multi-line statement on one line, so the inventory stays a table."""
    one = " ".join(x.strip() for x in text.splitlines() if x.strip())
    if "=" in one:
        one = one.split("=", 1)[1].strip()
    return one[:limit] + ("…" if len(one) > limit else "")


def read_inputs(root):
    """Everything the verdict is a function of, read off the instrument's source.

    EVERY FIELD HERE IS INVARIANT UNDER THE REPAIR, and that is the whole selection rule:
    the repair rewrites transcript bytes, and none of these is a transcript byte.
    """
    path = os.path.join(root, "code", "gate_fixed_point_f771", "lib_f771.py")
    try:
        with open(path, encoding="utf-8") as fh:
            source = fh.read()
    except OSError as exc:
        raise Refused("cannot read %s: %s" % (path, exc))
    constants = [(name, _flatten(text, 72))
                 for name, text in _blocks(source, tuple(n + " =" for n in INVENTORY),
                                           "inventory constant(s)")]
    deciding = _blocks(source, DECIDING, "deciding function(s)")
    digest = hashlib.sha256(
        "".join(t for _, t in deciding).encode("utf-8")).hexdigest()
    return {"constants": constants, "digest": digest}


def invariant_report(root, width=92):
    """THE CANDIDATE ANSWER.  A transcript whose text is a function of the verdict's inputs.

    It says what is watched, what is exempt and by what rule the decision is made — and it
    does NOT say how the decision came out.  The outcome is on stderr and in the exit status,
    which is where `g0` already puts the other half of its run-dependent state and which is
    what the gate actually reads.
    """
    inputs = read_inputs(root)
    L = []
    add = L.append
    add("=" * width)
    add("mg-f771  THE GATE'S OWN FIXED POINT — WHAT IS WATCHED AND HOW IT IS DECIDED")
    add("=" * width)
    add("")
    add("§1  THE WATCHED CLASS")
    add("-" * width)
    add("  every tracked file under code/ named out_*.txt, compared against HEAD.")
    add("  Nothing is regenerated by this arm; it only reads.")
    add("")
    add("§2  THE INPUTS THE VERDICT IS A FUNCTION OF")
    add("-" * width)
    add("  THIS TRANSCRIPT RECORDS THE INPUTS AND NOT THE OUTCOME, and the reason is not")
    add("  taste.  This arm's output is committed by the same act that repairs what it")
    add("  reports, and the repair sets the disagreement set to empty — so a transcript")
    add("  naming that set is false about the tree it lands in, BECAUSE it landed there.")
    add("  The verdict is on stderr and in the exit status, which is what the gate reads.")
    add("")
    for name, value in inputs["constants"]:
        add("  %-20s %s" % (name.rstrip(" ="), value[:width - 24]))
    add("")
    add("  deciding functions (%s)"
        % ", ".join(d.split()[1].rstrip("(") for d in DECIDING))
    add("  sha256 of their source: %s" % inputs["digest"])
    add("")
    add("  A WIDER NORMALISER IS AN UNFALSIFIABLE ESCAPE HATCH — lib_f771's own words about")
    add("  its own main risk.  With this file inside the watched class, widening it without")
    add("  re-running the gate is caught by the control the widening would have silenced.")
    add("")
    return "\n".join(L) + "\n"
