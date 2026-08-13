"""W3 -- THE CHECKER THAT MG-6F61 DID NOT BUILD: the INSTRUMENT, not the
document.

mg-6f61 built `code/species_repair_6f61/check_doc.py`, which requires every
false sentence to survive only inside the strike that replaces it -- IN
`docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md`.  It reads one file.
That is why three of mg-a61f's findings were repaired in the prose and left
standing in `code/species_7d75/`, where a successor re-runs them:

  X4  `t3_bidigare.py` headed T3d "four candidate identifications, three are
      controls" and its vacuity branch read "the three controls did not fire".
  X5  `code/species_7d75/README.md` presented control (ii)'s 1 442 / 252 /
      11 020 under "Conventions that have bitten this repo before" as
      measuring "how differently" the two products behave -- the near-miss
      reading the audit refuted.
  S4  `t4_one_operation.py` printed "Sol(S_n) / rad = k^{Pi_n / S_n} = the
      character ring of S_n" and `t6_fock_and_record.py` printed "K(Pi) =
      symmetric functions, whose degree-n component is the character ring of
      S_n", both unmarked, both inside a run that ends TOTAL BAD: 0.  The
      second equality in each is ledger S4 / S5: cited to Solomon and to
      Garsia-Reutenauer/Atkinson, neither read here or by the audit.  A
      reader is given no way to tell the measured half from the cited one.

THIS FILE IS THE DETECTOR FOR ALL THREE, AND IT WAS RUN AGAINST THE
PRE-REPAIR TREE FIRST: it reported 12 problems there.  A checker written after
the fix and never seen to fail is not a checker.  `out_w3_scope_before.txt`
is the failing run, committed beside the passing one.

(That number read "6" until mg-a4ef, on mg-73df's Y5, against its own
evidence file's `FAIL (12 problems)` and against sections 14.3 and S14, which
both say 12.  A checker's own account of the run that falsified it told a
successor the falsification was half the size it was.)

ITS EXTENT, STATED, WHICH IS mg-73df's MAJOR (see section 14.4).  This file
enforces TWO of the eleven corrections -- X4 and X5 -- over ONE tree, plus the
character-ring rule.  `check_doc.py` enforces ten of them over ONE file.  So
between them every file was covered and every statement was covered, and NO
STATEMENT WAS COVERED IN EVERY FILE -- which is how X3 stayed in force in
`t6_fock_and_record.py` inside a run ending `T6 TOTAL BAD: 0`.  The union of
the two lists over all trees is `code/species_repair_a4ef/s1_extent.py`.
A PASS HERE IS NOT COVERAGE OF THAT EXTENT.

    python3 code/species_remainder_f8fa/w3_scope.py

AS-OF PINNING, mg-6e4f (mg-20ee tranche 2).  Every hit below is `path:NNN` or
`path line NNN` INTO A FILE THIS INSTRUMENT DOES NOT OWN -- addresses into
`code/species_7d75`, which mg-a4ef, mg-821e, mg-5040 and mg-4adb have all
amended since this transcript was written.  The corpus is now read AT A
DECLARED COMMIT via `git ls-tree`/`git cat-file` rather than from the working
tree, so the sha determines the addresses rather than annotating them.

AND THE DEFECT HERE WAS NOT ONLY THE ADDRESS.  The committed transcript
recorded `declined, STATED: __pycache__` -- a directory git has never tracked.
It is written by running any script in the target tree, so the committed run
was reproducible for an operator who had run `code/species_7d75` and for
nobody who had not.  Reading at a commit removes it: a pinned run cannot see
an untracked directory, and the residue block therefore reports `nothing at
all`.  That is an EXTENT line, not a verdict -- `bad` counts NOT-STATED
declines only, and no NOT-STATED decline exists at either reading.
"""

import os
import re
import subprocess
import sys

from kernf8fa import hdr

bad = 0
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TARGET = os.path.join("code", "species_7d75")

# The commit whose `code/species_7d75` this transcript addresses.
#
# CHOSEN UNDER mg-20ee's TWO CONDITIONS, IN ORDER.  (1) `git merge-base
# --is-ancestor e337f23 origin/main` is YES -- it was origin/main's tip when
# this pin was made, so no rebase can strand it, which is mg-daba's defect and
# was committed deliberately once already in tranche 1.  (2) at that commit
# the previously-committed transcript reproduces except for the two
# `__pycache__` residue lines described above, which no commit can reproduce
# because git has never held that directory.
#
# THE CHOICE IS NOT LOAD-BEARING ACROSS ITS RANGE, AND THAT IS MEASURED
# RATHER THAN ASSUMED: `code/species_7d75` last moved at 52aeaf4, and
# `git rev-parse 52aeaf4:code/species_7d75` and `e337f23:code/species_7d75`
# are the SAME TREE 1e007b47.  Every commit in that range gives byte-identical
# addresses.  The newest main-reachable one is taken, per mg-20ee's rule 1.
AS_OF = "e337f231f3bcde6cfa935eb6a2751bd27608ff3f"

# Override, for re-measuring against a different corpus: any commit-ish, or
# the literal WORKTREE, which restores the pre-pin live read exactly.  Unset
# is the pinned default and is the only value that reproduces the committed
# transcript.
AT = os.environ.get("W3_SCOPE_AT", "").strip() or AS_OF

# The directory under test defaults to the source instrument, READ AT `AT`.
# It is overridable so the SAME checker can be pointed at the pre-repair tree
# -- which is how `out_w3_scope_before.txt` is produced, and the reason that
# file is evidence rather than decoration:
#
#     git worktree list                      # from this repo
#     mkdir -p /tmp/pre && git archive 83ac472 code/species_7d75 \
#         | tar -x -C /tmp/pre
#     python3 w3_scope.py /tmp/pre/code/species_7d75
#
# AN EXPLICIT PATH IS READ OFF DISK AND IS NOT ROUTED THROUGH THE PIN.  That
# is mg-20ee's own hazard, met in tranche 1 by pairbias_indep_audit_6bd1: a
# fixture looked for in a commit that never contained it took a transcript
# from 226 lines to 2.  Only the corpus DEFAULT is pinned.
EXPLICIT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None
SRC = EXPLICIT or os.path.join(ROOT, TARGET)


# mg-6e4f.  A COPY OF THIS TREE HAS NO OBJECT STORE, AND NINE INSTRUMENTS RUN
# THIS FILE INSIDE ONE.
#
# `w3_scope.py` is not only a transcript producer.  It is a SHARED CHECKER:
# species_audit_7dd3, species_extent_d633, species_extent_audit_6cb9,
# species_gate_audit_d53d, species_depth_audit_4700, species_rung_repair_4adb,
# species_sites_821e and species_audit_73df all execute it.  Most of them work
# the same way -- `shutil.copytree` the repo into a tempdir, mutate the copy,
# run the checker there -- and THAT COPY HAS NO `.git`.  A pinned read cannot
# be performed in it BY CONSTRUCTION, and the first version of this pin turned
# mg-7dd3's D5 control M0d, `no mutation`, into `exit 1, predicted 0
# *** PREDICTION MISSED ***`, MEASURED before this paragraph existed.
#
# SO THE PIN IS CONDITIONED ON BEING IN THE REPOSITORY IT PINS, AND THE TEST IS
# IDENTITY, NOT PRESENCE: `git rev-parse --show-toplevel` must come back equal
# to this file's own ROOT.  A tempdir that happens to sit inside some other
# checkout would otherwise resolve to that checkout and read a corpus from a
# repository nobody named.
#
# THIS IS NOT A SILENT FALLBACK, WHICH IS WHAT mg-20ee's TRANCHE 1 REFUSED.
# The two cases it refused are still refused: if this IS the repository and
# AS_OF is unreachable, the run EXITS NON-ZERO rather than reading live, and a
# pin resolving to an empty tree exits non-zero rather than reporting a vacuous
# PASS.  What is allowed is the case those rules do not cover -- a tree that is
# not a git repository at all, where the caller can only have meant the tree in
# front of it -- and it is ANNOUNCED in the stamp, at the top of the run, in
# the same block that would otherwise name the commit.
def _in_own_repo():
    got = subprocess.run(["git", "-C", ROOT, "rev-parse", "--show-toplevel"],
                         capture_output=True)
    if got.returncode != 0:
        return False
    top = got.stdout.decode("utf-8", "replace").strip()
    return bool(top) and os.path.realpath(top) == os.path.realpath(ROOT)


DETACHED = EXPLICIT is None and AT != "WORKTREE" and not _in_own_repo()
PINNED = EXPLICIT is None and AT != "WORKTREE" and not DETACHED
print("# target: %s" % os.path.join(*SRC.split(os.sep)[-2:]))
print()
print("# AS OF %s (mg-6e4f, mg-20ee tranche 2)." % (AT if PINNED else "-"))
if PINNED:
    print("# The corpus is read from git at that commit, NOT from the working")
    print("# tree.  EVERY `file:NNN` and `file line NNN` below is an ADDRESS")
    print("# into code/species_7d75 and is a property of THAT COMMIT.  The")
    print("# file count and the residue block are corpus-valued in the same")
    print("# way.  WHAT IS NOT: every ok / STILL ASSERTED / marked / UNMARKED")
    print("# / MISSING word, and the W3 SCOPE verdict -- those are findings")
    print("# about code/species_7d75 and do not move with the addresses.")
    print("# A pinned run cannot see an untracked directory, so the")
    print("# __pycache__ rule below is stated and never fires.")
elif DETACHED:
    print("# NOT PINNED, AND THE PIN WAS NOT DECLINED -- IT WAS IMPOSSIBLE.")
    print("# This copy of the tree is not the repository the pin names, so")
    print("# there is no object store to read %s from and the" % AS_OF[:7])
    print("# live tree is the only corpus there is.  That is the case a")
    print("# scratch-copy harness creates and it is the reading such a harness")
    print("# wants; it is announced here rather than left to be inferred from")
    print("# addresses that quietly stopped meaning anything.")
else:
    print("# NOT PINNED: this run read %s live."
          % ("an explicit path" if EXPLICIT else "the working tree"))
    print("# Its addresses are offsets into whatever that tree holds now and")
    print("# reproduce nothing.  W3_SCOPE_AT=%r." % os.environ.get(
        "W3_SCOPE_AT", ""))
print()

# mg-d633, on mg-7dd3's A1: this listing filtered on `.py/.txt/.md`, so
# "over ONE tree" in the extent below covered every file in the tree EXCEPT
# `run_all.sh`, which is in it.  Same defect as `s1_extent.py`'s, one tree
# narrower, and repaired the same way: THE CODE IS WIDENED, not the claim
# narrowed.  Every regular file is read; anything undecodable is NAMED in the
# output rather than dropped by a rule no sentence carries.
#
# mg-821e, on mg-6cb9's F1: and it now RECURSES.  `os.listdir` plus a
# `continue` past anything that is not a file dropped every SUBDIRECTORY --
# again by a rule no sentence carried, and again invisible, because
# `code/species_7d75` has never had one.  "Every regular file in it" was a
# true sentence resting on an unstated condition; X4 planted in
# `code/species_7d75/sub/leak.md` left this checker silent (mg-6cb9 Q10).  The
# walk is now `os.walk`, so the sentence is true BY CONSTRUCTION.  ONE
# directory rule remains and it is PRINTED: `__pycache__` is not descended
# into, because it holds bytecode these runs write themselves.
#
# mg-5040, on mg-4700's OPEN 1: AND THAT WAS THE SECOND GENERATION OF THE SAME
# ACCIDENT.  "True BY CONSTRUCTION" held only while no tree contained a
# SYMLINKED DIRECTORY: os.walk puts one in `dirnames` and does not descend
# without `followlinks=True`, so a statement planted behind a link left this
# checker silent again, word for word the paragraph above with one rule
# substituted.  Each widening buys exactly one generation -- depth, symlinks,
# then mount points, then a directory this process cannot read.
#
# So it is NOT widened a third time.  Of mg-5040's two options this takes the
# FIRST -- state the walk's actual bound, so the claim and the code describe
# the same set -- and states it in CODE rather than in prose: the walk returns
# EVERY ENTRY IT DECLINED with the reason, whether or not the reason was
# thought of in advance, the residue is printed, and anything in it that is
# not the stated `__pycache__` rule is a finding.  The silence is what
# generated the generations, and the silence is what is removed.
PYCACHE = "__pycache__"
STATED_DIR_RULES = (PYCACHE,)


def walk_residue(root, stated_dirs=STATED_DIR_RULES):
    """(files, stated, unstated) -- nothing is dropped without landing in one
    of the last two.  `stated`/`unstated` are (relpath, reason) pairs.

    Written out here rather than imported, for the reason e1_extents.py gives
    for its own copy: three trees that must agree, computed independently, can
    disagree, and a shared enumerator cannot disagree with itself.
    """
    files, stated, unstated = [], [], []
    if not os.path.isdir(root):
        return files, stated, unstated

    def onerror(err):
        p = getattr(err, "filename", None) or root
        unstated.append((os.path.relpath(p, root),
                         "os.walk raised %s and would otherwise have "
                         "dropped it in silence" % err.__class__.__name__))

    for dirpath, dirnames, filenames in os.walk(root, onerror=onerror):
        keep = []
        for d in sorted(dirnames):
            p = os.path.join(dirpath, d)
            rel = os.path.relpath(p, root)
            if d in stated_dirs:
                stated.append((rel, "directory rule, STATED: %s/" % d))
            elif os.path.islink(p):
                unstated.append((rel, "symlinked directory -- os.walk does "
                                      "not descend without followlinks"))
            else:
                keep.append(d)
        dirnames[:] = keep
        for f in sorted(filenames):
            p = os.path.join(dirpath, f)
            rel = os.path.relpath(p, root)
            if os.path.isfile(p):
                files.append(rel)
            elif os.path.islink(p):
                unstated.append((rel, "symlink that does not resolve to a "
                                      "regular file"))
            else:
                unstated.append((rel, "not a regular file"))
    return sorted(files), sorted(set(stated)), sorted(set(unstated))


# mg-4adb, on mg-6ef4's F1.  THE SET IS BUILT IN TWO LAYERS AND ONLY THE
# FIRST HAD A RESIDUE.  `walk_residue` above decides what is REACHED and names
# everything it declined.  `open().read()` below decides which reached entries
# are READ -- and until this ticket it declined under ONE
# `except (UnicodeDecodeError, OSError)` whose printed sentence said the
# reason was the file's ENCODING.  A REGULAR FILE THIS PROCESS CANNOT OPEN
# passes layer 1 (isfile true, residue empty), fails layer 2 with
# PermissionError, and was filed under a bucket naming a cause it does not
# have: printed, NOT COUNTED, contents never scanned, this checker exit 0 with
# a live X4 statement inside it.
#
# UNREADABLE IS NOT MIS-ENCODED, and the classification is repaired FIRST
# because a wrong bucket sends every later reader to the wrong hypothesis --
# a worse failure than no bucket at all.  The two are separated by the
# exception that produced them, each is named with that exception's class, and
# they are counted DIFFERENTLY, by the same rule layer 1 already uses:
#
#   ENCODING     STATED.  Not counted.  A sentence carries it and has since
#                mg-d633: the printed extent says the run is over every
#                regular file LESS the ones named as undecodable, and the
#                names are printed here.  Like `__pycache__/`, it is a rule a
#                reader can see before meeting a surprise.
#   UNREADABLE   NOT STATED.  COUNTED.  No sentence in this file, or in any
#                extent line in this repository, has ever said that a regular
#                file this process cannot open is outside the claim.  So it is
#                a finding, and it arrives as RED rather than as a printed
#                aside under somebody else's reason.
def read_residue(root, reached):
    """(files, text, stated, unstated) for LAYER 2.

    Nothing reached is dropped without landing in `stated` or `unstated`,
    which is `walk_residue`'s contract applied to the layer below it.  The
    file is read ONCE: the previous version tested decodability with one
    `open` and then re-opened every survivor to build the text, so a file that
    became unreadable between the two opens raised out of a dict
    comprehension with no bucket at all.
    """
    files, text, stated, unstated = [], {}, [], []
    for rel in reached:
        p = os.path.join(root, rel)
        try:
            with open(p, encoding="utf-8") as fh:
                text[rel] = fh.read()
        except UnicodeDecodeError:
            stated.append((rel, "file rule, STATED: bytes are not valid "
                                "UTF-8 text (UnicodeDecodeError)"))
            continue
        except OSError as err:
            unstated.append((rel, "REACHED AND NOT READ: open() raised %s.  "
                                  "This is NOT an encoding problem -- the "
                                  "file's bytes were never seen"
                                  % err.__class__.__name__))
            continue
        files.append(rel)
    return sorted(files), text, sorted(set(stated)), sorted(set(unstated))


# mg-6e4f.  THE PINNED READER, AND IT KEEPS BOTH LAYERS AND BOTH RESIDUES.
# The two functions above decide what is REACHED and what is READ, and each
# names everything it declined; a pinned read that collapsed them into one
# `git ls-tree | cat-file` loop would have quietly deleted the finding channel
# this file spent four tickets building.  So the same contract is implemented
# against the object store:
#
#   LAYER 1, reached.  `git ls-tree -r` at the commit.  A blob is reached.  A
#     SYMLINK (mode 120000) and a GITLINK (mode 160000) are declined NOT
#     STATED -- no sentence here has ever put them outside the claim, and
#     under the live walk a symlink to a regular file was READ, so declining
#     one silently would be a rule arriving as silence.  Neither exists in
#     this tree; the point is that the next one arrives as RED.
#   LAYER 2, read.  `git cat-file blob` then decode.  Not-UTF-8 is the SAME
#     STATED decline, worded identically so a future diff means something.  A
#     blob that cannot be read back is NOT STATED.
#
# `__pycache__` CANNOT APPEAR HERE and the stated rule is kept anyway: it is
# the rule the extent line names, it still governs the WORKTREE and explicit-
# path readings, and deleting it would make the two readings disagree about
# what they are doing rather than about what they found.
def git_residue(rev, prefix):
    """(files, text, stated, unstated) for the tree at `rev` under `prefix`.

    Same 4-tuple, same wording, same contract as walk_residue+read_residue.
    """
    files, text, stated, unstated = [], {}, [], []
    got = subprocess.run(
        ["git", "-C", ROOT, "ls-tree", "-r", "-z", "--full-tree", rev,
         "--", prefix], capture_output=True)
    if got.returncode != 0:
        raise SystemExit(
            "w3_scope: cannot read %s at %s: %s\n"
            "  (W3_SCOPE_AT=%r; unset it for the pinned run, or set it to\n"
            "   WORKTREE for the pre-pin live read.)"
            % (prefix, rev, got.stderr.decode("utf-8", "replace").strip(),
               os.environ.get("W3_SCOPE_AT", "")))
    for ent in got.stdout.decode("utf-8", "surrogateescape").split("\0"):
        if not ent:
            continue
        meta, path = ent.split("\t", 1)
        mode, _kind, sha = meta.split(" ", 2)
        rel = os.path.relpath(path, prefix)
        if mode == "120000":
            unstated.append((rel, "symlink in the pinned tree -- the live "
                                  "walk read a symlink to a regular file and "
                                  "this reading does not"))
            continue
        if mode == "160000":
            unstated.append((rel, "gitlink (submodule) -- its bytes are not "
                                  "in this repository at all"))
            continue
        blob = subprocess.run(["git", "-C", ROOT, "cat-file", "blob", sha],
                              capture_output=True)
        if blob.returncode != 0:
            unstated.append((rel, "REACHED AND NOT READ: git cat-file failed "
                                  "on %s.  This is NOT an encoding problem "
                                  "-- the file's bytes were never seen"
                                  % sha[:12]))
            continue
        try:
            text[rel] = blob.stdout.decode("utf-8")
        except UnicodeDecodeError:
            stated.append((rel, "file rule, STATED: bytes are not valid "
                                "UTF-8 text (UnicodeDecodeError)"))
            continue
        files.append(rel)
    if not files:
        raise SystemExit(
            "w3_scope: %s is EMPTY at %s -- refusing to report a vacuous "
            "PASS.\n  A pin that resolves to a tree the corpus was never in "
            "is mg-20ee's own\n  hazard (tranche 1, pairbias_indep_audit_6bd1"
            ": 226 lines to 2)." % (prefix, rev))
    return sorted(files), text, sorted(set(stated)), sorted(set(unstated))


if PINNED:
    FILES, TEXT, DECLINED_STATED, DECLINED_UNSTATED = git_residue(AT, TARGET)
    _READ_STATED, _READ_UNSTATED = [], []
else:
    _REACHED, DECLINED_STATED, DECLINED_UNSTATED = walk_residue(SRC)
    FILES, TEXT, _READ_STATED, _READ_UNSTATED = read_residue(SRC, _REACHED)
DECLINED_STATED = sorted(set(DECLINED_STATED) | set(_READ_STATED))
DECLINED_UNSTATED = sorted(set(DECLINED_UNSTATED) | set(_READ_UNSTATED))
NESTED = [f for f in FILES if os.sep in f]
print("# files read: %d, %d of them below the tree root   (%d reached and not"
      % (len(FILES), len(NESTED), len(_READ_STATED) + len(_READ_UNSTATED)))
print("# read, listed by reason below; skipped as %s: the whole directory"
      % PYCACHE)
print("# rule)")
if NESTED:
    for _f in NESTED:
        print("#   below the root: %s" % _f)
print("# THE BOUND (mg-5040): 'every regular file' means every regular file")
print("# THIS WALK REACHED.  It is os.walk without followlinks, so it enters")
print("# no symlinked directory and reads no entry that is not a regular")
print("# file -- and it now RETURNS what it declined, so that bound is a")
print("# measurement and not a promise about the tree's shape.")
print("# AND THE SECOND LAYER IS IN THE SAME LIST (mg-4adb, on mg-6ef4's F1):")
print("# reaching an entry and reading it are different acts and both can")
print("# decline.  A file whose bytes are not UTF-8 is a STATED decline -- the")
print("# extent below says so.  A regular file this process cannot OPEN is")
print("# NOT: no sentence here has ever put it outside the claim, so it lands")
print("# in the second list and is counted.  Both layers, one residue:")
for _r, _why in DECLINED_STATED:
    print("#   declined, STATED:     %s   %s" % (_r, _why))
for _r, _why in DECLINED_UNSTATED:
    print("#   declined, NOT STATED: %s   %s" % (_r, _why))
if not DECLINED_STATED and not DECLINED_UNSTATED:
    print("#   declined: nothing at all")
if DECLINED_UNSTATED:
    print("#   ^ NOT STATED is a FINDING.  The extent line below claims every")
    print("#     regular file at any depth and those entries are not in it.")
bad += len(DECLINED_UNSTATED)
print()
LINES = {f: TEXT[f].splitlines() for f in FILES}


# ---------------------------------------------------------------------------
# A.  The corrected statements must not still be ASSERTED at source.
# ---------------------------------------------------------------------------
FORBIDDEN = [
    ("X4  T3d's control count",
     [r"three\s+are\s+controls", r"the\s+three\s+controls",
      r"three\s+of\s+the\s+four\s+(?:columns\s+)?are\s+the\s+control"]),
    ("X5  control (ii) read as a near miss",
     [r"measures\s+how\s+differently"]),
]

# Deliberately NARROW.  An earlier version of this file accepted a bare
# "REPAIRED" or "CORRECTED" nearby, and the pre-repair README disarmed it by
# accident: an unrelated "the error mg-1953 repaired" four lines above the
# near-miss bullet made the bullet read as already corrected.  A marker has to
# name THIS repair, or say in so many words that the sentence no longer holds.
QUOTED_AS_CORRECTED = re.compile(r"mg-f8fa|used\s+to|no\s+longer", re.I)
QWINDOW = 4

hdr("W3a  the corrected statements are not still ASSERTED in the instrument")
print()
print("  This is the negative half, and it is the load-bearing one -- the")
print("  same shape as check_doc.py's strike test, moved from the document to")
print("  the code.  A corrected statement may survive ONLY where it is being")
print("  quoted as corrected: within %d lines of a marker saying so.  Anywhere"
      % QWINDOW)
print("  else it is still in force, whatever the prose elsewhere says.")
print()
for label, pats in FORBIDDEN:
    asserted, quoted = [], []
    for f in FILES:
        for i, ln in enumerate(LINES[f]):
            if not any(re.search(p, ln, re.I) for p in pats):
                continue
            lo, hi = max(0, i - QWINDOW), min(len(LINES[f]), i + QWINDOW + 1)
            near = "\n".join(LINES[f][lo:hi])
            (quoted if QUOTED_AS_CORRECTED.search(near)
             else asserted).append("%s:%d" % (f, i + 1))
    ok = not asserted
    bad += (not ok)
    print("  %-46s %s" % (label, "ok" if ok else "*** STILL ASSERTED ***"))
    for h in asserted:
        print("        STILL ASSERTED AT  %s" % h)
    for h in quoted:
        print("        quoted as corrected at %s" % h)
print()


# ---------------------------------------------------------------------------
# B.  EVERY occurrence of the cited identification carries its ledger row.
# ---------------------------------------------------------------------------
CITED = re.compile(r"character\s+ring", re.I)
MARKER = re.compile(r"ledger\s+S[45]|CITED,?\s+NOT\s+(?:DERIVED|VERIFIED)"
                    r"|NOT\s+VERIFIED\s+HERE", re.I)
WINDOW = 8

hdr("W3b  EVERY occurrence of the CITED identification is marked, not only"
    " the ledger")
print()
print("  Rule: any line in code/species_7d75 that identifies the semisimple")
print("  quotient with the CHARACTER RING of S_n must have the scope marker")
print("  within %d lines of it, in the same file.  The step from k^{Pi_n/S_n}"
      % WINDOW)
print("  to the character ring is ledger S4; the Fock-functor statement is")
print("  S5.  Neither Solomon nor Garsia-Reutenauer/Atkinson was read, here")
print("  or by mg-a61f.")
print()
found = 0
for f in FILES:
    for i, ln in enumerate(LINES[f]):
        if not CITED.search(ln):
            continue
        found += 1
        lo, hi = max(0, i - WINDOW), min(len(LINES[f]), i + WINDOW + 1)
        near = "\n".join(LINES[f][lo:hi])
        ok = bool(MARKER.search(near))
        bad += (not ok)
        print("  %-38s line %-5d %s"
              % (f, i + 1, "marked" if ok else "*** UNMARKED ***"))
if not found:
    bad += 1
    print("  *** NO OCCURRENCE FOUND -- the detector is looking at the wrong")
    print("      tree, or the identification was deleted rather than scoped ***")
else:
    print()
    print("  %d occurrence(s) checked." % found)
print()


# ---------------------------------------------------------------------------
# C.  The positive half: the corrected readings are present at source.
# ---------------------------------------------------------------------------
REQUIRED = [
    ("t3_bidigare.py", "X4  two statements, each computed twice",
     r"two\s+statements,?\s+each\s+computed\s+twice"),
    ("t3_bidigare.py", "X4  and the count is COMPUTED, not asserted",
     r"T3e"),
    ("t5_hopf_monoid.py", "X5  control (ii) reads as a type mismatch",
     r"type\s+mismatch"),
    ("t5_hopf_monoid.py", "X5  and its conclusion is stated to survive",
     r"NOT\s+withdrawn|is\s+not\s+withdrawn"),
    ("README.md", "X5  the conventions bullet is repaired",
     r"type\s+mismatch"),
    ("README.md", "S4  the S_n half is named as unverified",
     r"ledger\s+S4"),
]

hdr("W3c  the corrected readings are present at source")
print()
for f, label, pat in REQUIRED:
    ok = f in TEXT and bool(re.search(pat, TEXT[f], re.I))
    bad += (not ok)
    print("  %-14s %-46s %s" % (f, label, "ok" if ok else "*** MISSING ***"))
print()

print("=" * 78)
print("W3 SCOPE: %s   (%d problem(s))" % ("PASS" if bad == 0 else "FAIL", bad))
print("=" * 78)
print()
print("EXTENT OF THAT VERDICT (added mg-a4ef).  MEASURED mg-d633.  DEEPENED")
print("mg-821e.  This enforces TWO corrected statements -- X4 and X5 -- plus")
print("the character-ring rule, over ONE tree of %d file(s)." % len(FILES))
# The next line is ONE line on purpose.  mg-6cb9's A1g asks whether the
# committed output SAYS that the repair widened the code, and it looks for the
# phrases `every regular file in it` and `no extension rule`.  Wrapping this
# sentence across two prints splits both, and A1g went *** SILENT *** against
# a file that says so more loudly than before.  A label check that reads the
# artifact is worth keeping; the artifact is what moves to suit it.
print("It reads every regular file in it, AT ANY DEPTH: no extension rule")
print("and no depth rule.  The extension rule existed until mg-d633 and")
print("dropped run_all.sh while this line said 'over ONE tree'; the depth")
print("rule existed until mg-821e and dropped every subdirectory while this")
print("line made the same claim -- true, and true only because the tree had")
print("no subdirectory (mg-6cb9 F1).  The one directory rule left is %s/,"
      % PYCACHE)
print("and it is named here rather than left to be inferred from the code.")
print("AND THE BOUND OF THAT SENTENCE IS STATED (mg-5040, on mg-4700's OPEN")
print("1): it is every regular file THIS WALK REACHED.  A third rule was in")
print("force and carried by no sentence -- os.walk does not follow a")
print("SYMLINKED DIRECTORY -- so the claim was true a SECOND time only")
print("because of a shape the tree happened to have.  It is not widened a")
print("third time: the walk returns what it declined (%d stated, %d not"
      % (len(DECLINED_STATED), len(DECLINED_UNSTATED)))
print("stated, both listed at the head of this run) and a not-stated entry")
print("is a finding, so the next rule nobody thought of arrives as RED")
print("rather than as silence.")
print("mg-6f61 enumerated ten stricken sentences; eight of")
print("them are NOT on this list, and X3 and the AM 17.5 quotation were in")
print("force in code/species_7d75 for the whole time this file reported")
print("PASS.  A PASS HERE IS NOT COVERAGE OF THE OTHER NINE STATEMENTS.")
print("The union of both lists over all trees is:")
print("    python3 code/species_repair_a4ef/s1_extent.py")
# mg-a4ef: this was `sys.exit(0)` unconditionally, so a run reporting
# `FAIL (12 problems)` still exited 0 -- the same shape as the finding this
# file exists to carry.  Beyond mg-73df's five; recorded in the repair doc.
sys.exit(1 if bad else 0)
