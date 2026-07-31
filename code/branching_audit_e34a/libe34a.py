"""libe34a.py -- the apparatus for the independent audit of mg-76cc (4755d02).

mg-76cc repaired mg-957f's F-1: the kernel half of g1_provenance.py's
measurement-invariance predicate.  This ticket audits that repair, and the
first instruction it carries is the one that found F-1 in the first place:

    take the predicate AS IT STOOD BEFORE THIS REPAIR, run it against the same
    inputs, and compare what each catches.

So the load-bearing tool here is `install_pinned`, not any reader.  Everything
else exists to make its answer trustworthy.

WHAT IS WRITTEN FRESH, AND WHY

  * `PRE_REV` is DERIVED FROM THE PROPERTY, PINNED, AND THE TWO ARE COMPARED
    (mg-8d5e, on mg-2c77's OPEN 1).  lib76cc.py carries
    `REV_957F = "e006581c..."` as a literal beside the comment "g1 BEFORE
    mg-76cc".  A literal is a claim that stops being checked the moment the
    file moves, and that is why this file derived instead.  It derived from
    the FILE'S HISTORY -- the last commit that touched g1_provenance.py, and
    then its first parent -- and mg-69d1 then touched g1_provenance.py to
    correct a SENTENCE.  The anchor followed the edit: REPAIR_REV moved
    4755d02 -> d01ff32, PRE_REV moved 3bc2cf76 -> e5787e11, and both sides of
    k1's comparison became mg-76cc's ALREADY-REPAIRED predicate.  Every number
    k1 prints was unchanged and every one of them was about a different pair
    of revisions.

    A derived anchor follows every edit to the file it derives from, including
    edits with nothing to do with the property.  That is the opposite of the
    literal's failure and it is quieter, because the number is identical and
    means something else.  So the anchor is now THREE things at once, and no
    two of them can fail the same way:

        DERIVED FROM THE PROPERTY -- `first_introducing(G1_REL, MARK_76CC)`,
          the first commit at which g1_provenance.py carries `kernel_source=`.
          That string IS the restored kernel half: the two-source signature
          mg-76cc added so that "this script with that kernel" could be
          asked at all.  A commit that edits prose does not move it.
        PINNED -- REPAIR_REV_PIN / PRE_REV_PIN, written down, with the reason
          written beside them.
        COMPARED -- ANCHOR_DRIFT holds one row per disagreement, and the
          selftest and k1 (i) both go red on a non-empty one.  A pin that
          rots and a derivation that re-points are both loud.

    The file-history derivation is KEPT and PRINTED, as LAST_TOUCHING_G1.  It
    is no longer the anchor; it is the quantity that moved, and deleting the
    evidence of the failure would be the third version of the same mistake.

  * `REV_A218` is READ OUT OF lib58da.py's own source rather than copied.
    Copying a pinned constant into a third file is how three files come to
    disagree about one revision.

  * The transcript readers here parse by SPLITTING ON A COLON and reading a
    leading integer.  lib76cc walks characters with `isdigit`; lib58da uses
    `re`.  Two readers that share an implementation share a blind spot.  And
    this one CROSS-CHECKS the printed count against the number of listed
    lines, which neither of the other two does: a script whose trailer says
    FINDINGS 3 and lists 2 is broken in a way a count-only reader cannot see.

  * Every mutation is a COMMIT in a temp clone, because g1 reads c1 and the
    kernel with `git show` and a working-tree edit reaches nothing at all.
    A probe that comes back silent because it never existed looks exactly
    like a probe that came back silent because the predicate is fine.

NOTHING HERE WRITES INTO code/branching_audit_58da/,
code/branching_audit_a218/, code/branching_audit_957f/ or
code/branching_repair_76cc/.  Every run happens in a clone under /tmp.
"""

import hashlib
import os
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

S58DA_DIR = "code/branching_audit_58da"
A218_DIR = "code/branching_audit_a218"
DB09_DIR = "code/branching_locate_db09"
R76CC_DIR = "code/branching_repair_76cc"

G1_REL = S58DA_DIR + "/g1_provenance.py"
LIB_REL = S58DA_DIR + "/lib58da.py"
C1_REL = A218_DIR + "/c1_branching.py"
KERN_REL = A218_DIR + "/kern_a218.py"
TARGET_REL = DB09_DIR + "/out_t1_tl.txt"

# the five files code/branching_audit_58da/run_all.sh writes -- enumerated
# from the runner's own source in k2, not from this list; this is the order
# they are reported in.
FIVE_OUTPUTS = ["out_selftest_58da.txt", "out_g1_provenance.txt",
                "out_g2_redo.txt", "out_g3_findings.txt", "out_g4_fleet.txt"]

UNTOUCHED_58DA = ["selftest_58da.py", "g2_redo.py", "g3_findings.py",
                  "g4_fleet.py"]

# c1's output splits here: everything before is what c1 COMPUTES, everything
# after is what it COMPARES.  The same split g1 uses, by the same marker.
C1_SPLIT = "(iii) EVERY CELL, AGAINST"


# ---------------------------------------------------------------------------
# git
# ---------------------------------------------------------------------------

def git(*args, **kw):
    repo = kw.pop("repo", REPO)
    return subprocess.run(["git", "-C", repo] + list(args), check=True,
                          capture_output=True, text=True).stdout


def git_show(rev, path, repo=REPO):
    return git("show", "%s:%s" % (rev, path), repo=repo)


def head_rev(repo=REPO):
    return git("rev-parse", "HEAD", repo=repo).strip()


def resolve(rev, repo=REPO):
    return git("rev-parse", rev, repo=repo).strip()


def subject(rev, repo=REPO):
    return git("log", "-1", "--format=%s", rev, repo=repo).strip()


def last_touching(path, rev="HEAD", repo=REPO):
    """The most recent commit at or before `rev` that touched `path`.

    NOT the anchor any more (mg-8d5e, on mg-2c77's OPEN 1).  Kept because the
    quantity that re-pointed is evidence: k1 (i) prints it beside the property
    anchor and the distance between them.
    """
    out = git("log", "-1", "--format=%H", rev, "--", path, repo=repo).strip()
    return out or None


def show_or_empty(rev, path, repo=REPO):
    """`path` at `rev`, or "" where it does not exist there.

    "" and not an exception, because `first_introducing` walks back to a
    commit where the file has not been created yet and "the marker is absent"
    is the right answer there, not a crash.
    """
    p = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, path)],
                       capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else ""


def parents(rev, repo=REPO):
    return [h for h in git("rev-parse", rev + "^@", repo=repo).split() if h]


def first_introducing(path, marker, rev="HEAD", repo=REPO):
    """The OLDEST commit at or before `rev` where `marker` enters `path`.

    "Enters" is the two-sided test and both sides are needed: the marker is
    in `path` at the commit AND not in `path` at its first parent.  A
    one-sided test ("the oldest commit where it is present") would answer with
    the file's creation whenever the marker was there from the start, which is
    a different claim.

    THIS IS THE ANCHOR (mg-8d5e).  `the predicate as it stood before the
    repair` is a claim about a PROPERTY -- the kernel half being present in
    the measurement -- and so it is derived from the property, not from the
    file's edit history.  A commit that corrects a sentence in the same file
    does not move it; that is exactly what moved the old anchor.
    """
    hist = [h for h in git("log", "--format=%H", "--reverse", rev, "--", path,
                           repo=repo).split() if h]
    for h in hist:
        if marker not in show_or_empty(h, path, repo=repo):
            continue
        ps = parents(h, repo=repo)
        if not ps or marker not in show_or_empty(ps[0], path, repo=repo):
            return h
    return None


def marker_is_monotone(path, marker, rev="HEAD", repo=REPO):
    """(ok, why) -- once `marker` is in `path`, is it in every later commit?

    A marker that appears, disappears and reappears makes `first_introducing`
    return the FIRST of two introductions, which is a different revision from
    the one a reader would mean.  Asserted rather than assumed, because the
    whole point of this repair is that an anchor should say so when it stops
    pointing where its own prose says.
    """
    hist = [h for h in git("log", "--format=%H", "--reverse", rev, "--", path,
                           repo=repo).split() if h]
    seen, bad = False, []
    for h in hist:
        here = marker in show_or_empty(h, path, repo=repo)
        if here:
            seen = True
        elif seen:
            bad.append(h[:8])
    return (not bad), ("present, then absent again at " + ", ".join(bad)
                       if bad else "")


def commits_touching(path, since, until="HEAD", repo=REPO):
    out = git("log", "--format=%H", "%s..%s" % (since, until), "--", path,
              repo=repo)
    return [h for h in out.split() if h]


def files_of(rev, repo=REPO):
    out = git("show", "--name-only", "--format=", rev, repo=repo)
    return [p for p in out.split("\n") if p.strip()]


def is_ancestor(a, b, repo=REPO):
    p = subprocess.run(["git", "-C", repo, "merge-base", "--is-ancestor",
                        a, b], capture_output=True, text=True)
    return p.returncode == 0


def distance(a, b, repo=REPO):
    return len([h for h in git("rev-list", "%s..%s" % (a, b),
                               repo=repo).split() if h])


def sha(text):
    if isinstance(text, str):
        text = text.encode()
    return hashlib.sha256(text).hexdigest()


def read_worktree(rel, repo=REPO):
    with open(os.path.join(repo, rel)) as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# the revisions, DERIVED
# ---------------------------------------------------------------------------

def read_literal(src, name):
    """The string literal assigned to `name` at the top level of `src`.

    Used to take REV_A218 out of lib58da.py rather than copying it here.  A
    pinned revision copied into a third file is how three files come to
    disagree about one revision, and this arc has already had that.
    """
    for line in src.splitlines():
        s = line.strip()
        if not s.startswith(name + " ="):
            continue
        rest = s.split("=", 1)[1].strip()
        if rest.startswith('"'):
            return rest[1:].split('"', 1)[0]
        if rest.startswith("'"):
            return rest[1:].split("'", 1)[0]
    raise ValueError("no top-level string literal %r in the source given"
                     % name)


REV_A218 = read_literal(read_worktree(LIB_REL), "REV_A218")

# THE REPAIR, AND THE PREDICATE AS IT STOOD BEFORE IT.
#
# Each anchor is a PROPERTY named by a marker string, a PIN, and a comparison
# between them (mg-8d5e, on mg-2c77's OPEN 1 -- see the module docstring).
#
# The markers are chosen to BE the repair, not to describe it:
#
#   MARK_76CC  `kernel_source=` -- mg-76cc's whole patch is that the measuring
#              half is TWO files and can be asked about separately, and the
#              signature change is where that becomes expressible.  Before it,
#              `run_c1(script_rev=REV_A218)` pinned the kernel on both sides
#              and a kernel that moved reached neither.
#   MARK_7E58  `def measurement(` -- mg-7e58 replaced a file-sha predicate
#              with one asked OF THE MEASUREMENT, and this function is that
#              measurement.
MARK_76CC = "kernel_source="
MARK_7E58 = "def measurement("

# The intended pair, written down.  Not instead of the derivation -- beside
# it, so that a derivation which has quietly started measuring something else
# has something to disagree with.
REPAIR_REV_PIN = "4755d0292fc9175815739e9a77fa24dc6b8baf48"   # mg-76cc
PRE_REV_PIN = "3bc2cf760ea28ddf6e4c3a9b73a89acc42a167a0"      # its parent
REV_7E58_PIN = "4372fae95881bb421099bc715d1924c37d98b7b3"     # mg-7e58
PRE_7E58_PIN = "52aeaf43015031e416d84cbc18d72ad2daa06f26"     # its parent

ANCHOR_DRIFT = []       # one human-readable row per disagreement; [] is green


def _anchored(name, marker, pin, pre_pin):
    """(repair rev, pre rev) for one anchor, derived AND pinned AND compared.

    The derived value is what is USED, so the instrument keeps the ability to
    notice that the file moved -- which is why mg-e34a derived in the first
    place.  The pin is what is ASSERTED, so the instrument also notices that
    the derivation has re-pointed -- which is what mg-69d1's sentence edit
    did.  Any disagreement lands in ANCHOR_DRIFT and is printed and gated; it
    is never silently resolved in favour of either side.

    When the marker cannot be found at all the pin is used and the fallback is
    recorded, because a run against a revision nobody chose is worse than a
    run that says out loud which revision it fell back to.
    """
    got = first_introducing(G1_REL, marker)
    if got is None:
        ANCHOR_DRIFT.append(
            "%s: the marker %r is in no commit of %s, so the PROPERTY anchor "
            "could not be derived at all and the pin %s is being used instead"
            % (name, marker, G1_REL, pin[:8]))
        got = pin
    elif got != pin:
        ANCHOR_DRIFT.append(
            "%s: derived from the property (%r) gives %s, the pin says %s.  "
            "One of the two is wrong and this run does not know which"
            % (name, marker, got[:8], pin[:8]))
    pre = resolve(got + "^")
    if pre != pre_pin:
        ANCHOR_DRIFT.append(
            "%s: the first parent of %s is %s, the pinned pre-repair revision "
            "is %s" % (name, got[:8], pre[:8], pre_pin[:8]))
    return got, pre


REPAIR_REV, PRE_REV = _anchored("mg-76cc", MARK_76CC,
                                REPAIR_REV_PIN, PRE_REV_PIN)
REV_7E58, PRE_7E58_REV = _anchored("mg-7e58", MARK_7E58,
                                   REV_7E58_PIN, PRE_7E58_PIN)

# THE ANCHOR THAT RE-POINTED, KEPT AS EVIDENCE.  This was REPAIR_REV until
# mg-8d5e.  It is printed beside the property anchor in k1 (i): when the two
# differ, the difference is the count of commits that touched the file without
# touching the property, and that number is the finding stated as a quantity.
LAST_TOUCHING_G1 = last_touching(G1_REL)


def nth_touching(path, n, repo=REPO):
    """The n-th most recent commit touching `path` (0 = most recent).

    The other half of the same defect (mg-8d5e).  `PRE_7E58_REV` used to be
    `nth_touching(G1_REL, 1)^`, and mg-69d1's edit pushed every index along by
    one: the column k1 labels `before mg-7e58` came to hold mg-76cc's parent.
    An index into a file's history is an anchor derived from the history, and
    it re-points for exactly the same reason.  Kept, unused by any anchor, and
    printed in k1 (i) beside the property answer.
    """
    out = git("log", "--format=%H", "--", path, repo=repo).split()
    return out[n] if n < len(out) else None


NTH_TOUCHING_1 = nth_touching(G1_REL, 1)


def anchor_rows():
    """The anchor table k1 (i) and selftest both print, from one source.

    One source, because two places that build the same table from the same
    values by different code are two places that can disagree about it.
    """
    rows = [
        ("mg-76cc repair, DERIVED from %r" % MARK_76CC, REPAIR_REV,
         REPAIR_REV_PIN),
        ("  its first parent -- THE PRE-REPAIR PREDICATE", PRE_REV,
         PRE_REV_PIN),
        ("mg-7e58 repair, DERIVED from %r" % MARK_7E58, REV_7E58,
         REV_7E58_PIN),
        ("  its first parent", PRE_7E58_REV, PRE_7E58_PIN),
    ]
    return [(label, got, pin, "agrees" if got == pin else "*** DISAGREES")
            for label, got, pin in rows]


# ---------------------------------------------------------------------------
# reading a transcript.  Split on the colon; cross-check the count against the
# lines.  No `re`, no character walking.
# ---------------------------------------------------------------------------

def _leading_int(s):
    out = ""
    for ch in s.strip():
        if ch.isdigit():
            out += ch
        else:
            break
    return int(out) if out else None


def trailer(out):
    """(SELF-ERRORS, FINDINGS) as the script's own trailer states them.

    None for a script that prints no such line -- which is NOT the same as 0
    and is never shown as 0.
    """
    s = f = None
    for line in out.splitlines():
        if line.startswith("SELF-ERRORS:"):
            s = _leading_int(line.split(":", 1)[1])
        elif line.startswith("FINDINGS:"):
            f = _leading_int(line.split(":", 1)[1])
    return s, f


def listed(out, kind):
    """The finding / self-error lines a script books AS ITS OWN.

    Two discriminators, and both are needed:

      * the line must come AFTER the trailer line that counts them, and
      * it must be indented by EXACTLY three spaces, which is the trailer's
        own indentation.

    Without them a `FINDING:` line QUOTED from a nested transcript is counted
    as the outer script's.  That is not hypothetical: out_g4_fleet.txt at HEAD
    quotes one at six spaces, in a section where g4 is reporting what another
    member's run said, and both lib58da's and lib76cc's readers count it.  k4
    (v) demonstrates it against that committed artifact.
    """
    tag = "   " + kind + ": "
    header = "%sS:" % kind if kind == "FINDING" else "SELF-ERRORS:"
    got, started = [], False
    for line in out.splitlines():
        if line.startswith(header):
            started = True
            continue
        if not started:
            continue
        if line.startswith(tag) and not line.startswith(tag[:3] + " "):
            got.append(line[len(tag):].strip())
    return got


def findings(out):
    return listed(out, "FINDING")


def selferrs(out):
    return listed(out, "SELF-ERROR")


def trailer_consistent(out):
    """(ok, why) -- the printed counts against the printed lines.

    Neither lib58da nor lib76cc asks this.  A trailer that says FINDINGS 3
    over a list of 2 is a defect no count-only reader can see.
    """
    s, f = trailer(out)
    bad = []
    if s is not None and s != len(selferrs(out)):
        bad.append("SELF-ERRORS says %d, %d lines listed"
                   % (s, len(selferrs(out))))
    if f is not None and f != len(findings(out)):
        bad.append("FINDINGS says %d, %d lines listed"
                   % (f, len(findings(out))))
    return (not bad), "; ".join(bad)


def names_files(text, pool=("c1_branching.py", "kern_a218.py",
                            "out_t1_tl.txt")):
    """Which of the reproduction's files a finding NAMES.

    The coverage question is not 'how many findings' but 'what did each one
    say'.  Two predicates that both exit 1 can still disagree about which file
    moved, and a count cannot see it.
    """
    return tuple(sorted(p for p in pool if p in text))


# ---------------------------------------------------------------------------
# clones.  Every mutation is a COMMIT.
# ---------------------------------------------------------------------------

def dirty_paths(repo=REPO):
    out = git("status", "--porcelain", "-z", "--untracked-files=all",
              repo=repo)
    return [e[3:] for e in out.split("\0") if len(e) > 3]


def clone(mutate=None, message="mg-e34a scratch commit", carry=True,
          commit=True):
    """A clone of this worktree with the working tree COMMITTED.

    Committed, because g1 reads c1 and the kernel with `git show`: an edit
    left in the working tree reaches nothing and the probe comes back silent
    for a reason that has nothing to do with the predicate.

    `commit=False` with `carry=False` gives a clone whose HEAD is EXACTLY this
    branch's HEAD -- used by k2, where the question is what the tree AS
    COMMITTED reproduces and an extra scratch commit would put the answer at a
    revision nobody can look up.

    Returns (tmpdir, tree).  The caller destroys tmpdir.
    """
    tmp = tempfile.mkdtemp(prefix="mge34a-")
    tree = os.path.join(tmp, "repo")
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", REPO, tree],
                   check=True, capture_output=True, text=True)
    if carry:
        for rel in dirty_paths():
            src, dst = os.path.join(REPO, rel), os.path.join(tree, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.isfile(src):
                shutil.copy(src, dst)
            elif os.path.isfile(dst):
                os.remove(dst)
    if mutate:
        mutate(tree)
    if commit:
        subprocess.run(["git", "-C", tree, "add", "-A"], check=True,
                       capture_output=True, text=True)
        subprocess.run(["git", "-C", tree, "-c", "user.name=mg-e34a",
                        "-c", "user.email=mg-e34a@local", "commit", "-q",
                        "--allow-empty", "-m", message],
                       check=True, capture_output=True, text=True)
    return tmp, tree


def destroy(tmp):
    shutil.rmtree(tmp, ignore_errors=True)


def install_pinned(tree, rev, name):
    """Put g1_provenance.py AND lib58da.py as of `rev` into `tree`, each under
    a name of its own, and repoint the pinned g1's import at the pinned lib.

    The library has to travel with the predicate.  mg-76cc changed
    lib58da.run_c1's signature in the same commit as g1, so a pre-repair g1
    run against the repaired library is not the pre-repair predicate -- it is
    a third thing that never existed.

    Exactly one substitution is made and it is asserted, so a silently
    unpatched import cannot pass for a pinned run.
    """
    libname = "lib58da_at_%s" % rev[:8]
    src = git_show(rev, G1_REL)
    old = "import lib58da as L"
    if src.count(old) != 1:
        raise ValueError("g1 at %s has %d %r lines, not 1"
                         % (rev[:8], src.count(old), old))
    src = src.replace(old, "import %s as L" % libname, 1)
    with open(os.path.join(tree, S58DA_DIR, libname + ".py"), "w") as fh:
        fh.write(git_show(rev, LIB_REL))
    with open(os.path.join(tree, S58DA_DIR, name), "w") as fh:
        fh.write(src)
    return name


def run_script(directory, name, repo=REPO, timeout=3600):
    p = subprocess.run(["python3", name], cwd=os.path.join(repo, directory),
                       capture_output=True, text=True, timeout=timeout)
    return p.stdout + p.stderr, p.returncode


def run_sh(directory, name, repo=REPO, timeout=3600):
    p = subprocess.run(["bash", name], cwd=os.path.join(repo, directory),
                       capture_output=True, text=True, timeout=timeout)
    return p.stdout + p.stderr, p.returncode


# ---------------------------------------------------------------------------
# running c1 with the script and the kernel as SEPARATE sources
# ---------------------------------------------------------------------------

def run_c1(target_text, c1_src, kern_src):
    """c1_branching.py with a chosen kernel, against a chosen target.

    Two sources, never one revision.  mg-957f's F-1 was exactly a signature
    that could not say "this script with that kernel", and an instrument that
    inherits the defect cannot measure it.
    """
    tmp = tempfile.mkdtemp(prefix="mge34a-c1-")
    try:
        a = os.path.join(tmp, A218_DIR.split("/")[-1])
        d = os.path.join(tmp, DB09_DIR.split("/")[-1])
        os.makedirs(a)
        os.makedirs(d)
        with open(os.path.join(a, "c1_branching.py"), "w") as fh:
            fh.write(c1_src)
        with open(os.path.join(a, "kern_a218.py"), "w") as fh:
            fh.write(kern_src)
        with open(os.path.join(d, "out_t1_tl.txt"), "w") as fh:
            fh.write(target_text)
        p = subprocess.run(["python3", "c1_branching.py"], cwd=a,
                           capture_output=True, text=True, timeout=1800)
        return p.stdout + p.stderr, p.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def measuring_half(out):
    return out.split(C1_SPLIT)[0]


def vertex_cells(out):
    """(beta, n) -> ((p, dim), ...) out of c1's section (i).

    Read by splitting on 'set {' and then on commas -- lib58da uses a regex
    per row, lib957f ast.literal_eval, lib76cc str.partition.  Returns {} on
    an absent form; every caller treats {} as a SELF-ERROR rather than as an
    empty agreement.
    """
    got, beta = {}, None
    for raw in out.splitlines():
        line = raw.strip()
        if line.startswith("beta = ") and line[7:].strip().isdigit():
            beta = int(line[7:].strip())
            continue
        if beta is None or not line.startswith("n=") or "set {" not in line:
            continue
        head, _, body = line.partition("set {")
        n = _leading_int(head[2:])
        body = body.rsplit("}", 1)[0]
        cells = []
        for item in body.split(","):
            item = item.strip()
            if not item.startswith("p="):
                continue
            plabel, _, dlabel = item.partition(":dim")
            pv, dv = _leading_int(plabel[2:]), _leading_int(dlabel)
            if pv is None or dv is None:
                return {}
            cells.append((pv, dv))
        if n is None:
            return {}
        got[(beta, n)] = tuple(cells)
    return got


# ---------------------------------------------------------------------------
# bends.  Every one refuses on zero occurrences and on many.
# ---------------------------------------------------------------------------

def replace_once(text, old, new):
    n = text.count(old)
    if n != 1:
        raise ValueError("expected exactly 1 occurrence of %r, found %d"
                         % (old[:60], n))
    return text.replace(old, new, 1)


KERN_V = ("        return [(p, self.dim_L(p)) for p in self.parts "
          "if self.dim_L(p) > 0]")
KERN_V_UP = ("        return [(p, self.dim_L(p) + 1) for p in self.parts "
             "if self.dim_L(p) > 0]")
C1_V = "        mine_vertices[(beta, n)] = algebras[(n, beta)].vertices()"
C1_V_UP = ("        mine_vertices[(beta, n)] = [(p, d + 1) for p, d in "
           "algebras[(n, beta)].vertices()]")
C1_V_DOWN = ("        mine_vertices[(beta, n)] = [(p, d - 1) for p, d in "
             "algebras[(n, beta)].vertices()]")


def bend_kern_up(src):
    """kern_a218.py: every simple's dimension one too big."""
    return replace_once(src, KERN_V, KERN_V_UP)


def bend_c1_up(src):
    """c1_branching.py: the same regression one file up -- mg-7e58's probe."""
    return replace_once(src, C1_V, C1_V_UP)


def bend_c1_down(src):
    """c1_branching.py: dimensions one too SMALL.

    The half of the cancelling pair.  Paired with bend_kern_up the printed
    measurement is restored exactly, which is the input mg-76cc's own
    rationale for the `both together` row names and which nothing in that
    repair ever built.
    """
    return replace_once(src, C1_V, C1_V_DOWN)


def comment_c1(src):
    return src + "\n# mg-e34a control: a comment, and nothing more\n"


def comment_kern(src):
    """A comment appended to the KERNEL.

    mg-76cc's input list has a byte-only control for c1_branching.py and none
    for kern_a218.py -- the file the repair is about.  A restored half that
    fires on a comment is not restored.
    """
    return src + "\n# mg-e34a control: a comment in the kernel, and nothing more\n"


def touch_c1_compare(src):
    return src + '\nprint("   [mg-e34a control: comparing half touched]")\n'


# ---------------------------------------------------------------------------
# the report footer every script here shares
# ---------------------------------------------------------------------------

def banner(tag, title):
    print("=" * 74)
    print("%s  %s" % (tag, title))
    print("=" * 74)


def rule(title):
    print("-" * 74)
    print(title)
    print("-" * 74)


class Report(object):
    """SELF-ERRORS and FINDINGS, kept apart and each with its population.

    A script here exits 0 iff both are 0.  A non-zero exit means THIS SCRIPT
    HAS SOMETHING TO REPORT, never that it is broken.
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
