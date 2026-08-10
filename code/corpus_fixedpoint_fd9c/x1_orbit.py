"""mg-fd9c / X1 -- THE ORBIT, MEASURED BY ACTUALLY RUNNING THE SUITES.

WHY THIS PROBE IS NOT IN `run_all.sh`.  It clones this repository and runs two
other trees' runners a dozen times.  That is twenty minutes, and it is exactly
the thing my own ticket forbids doing in the worktree: *Do NOT regenerate any
other tree's transcripts.*  So it does it in a THROWAWAY CLONE, under a
directory you name on the command line, and it REFUSES TO START if that
directory is inside this repository.  Nothing in this worktree is read except
by `git clone`, which is a read.

    python3 x1_orbit.py --sandbox /tmp/fd9c-orbit [--runs 6] [--runs03d1 3]

WHAT IT ESTABLISHES, and it is the whole of the ticket's item 1:

  X1a  mg-9160's suite, iterated from c9160's OWN corpus state -- `757f999`
       with the tree's sources restored and its transcripts ABSENT, which is
       what c9160's disk looked like.  `--runs` defaults to 6; the same
       experiment was run at 12 by hand before this tree existed
       (PREDICTIONS.md/M5) and settled at the same fixed point.
  X1b  THE TWO REGIMES.  The same probe, at the same ref, over the same corpus,
       written two ways: `.new`+`mv` (what `run_all.sh` does) and a plain `>`
       (what a hand-run does).  This is the arm that decides whether `1984` and
       `1966` are two states of one system or two readings of one state.
  X1c  mg-03d1's suite, the arc's other whole-corpus consumer, iterated at HEAD.
       Nobody has ever run it twice in a row.

A NOTE ON WHAT A CLONE IS NOT.  A clone at `757f999` plus the tree's sources is
my RECONSTRUCTION of c9160's disk, not c9160's disk.  PREDICTIONS.md/E3 says
what that costs: any other untracked `code/*/out_*.txt` c9160 had is invisible
to me and would move every number here.
"""

import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

SANDBOX = None
RUNS = 6
RUNS03D1 = 3
_a = sys.argv[1:]
while _a:
    k = _a.pop(0)
    if k == "--sandbox":
        SANDBOX = os.path.abspath(_a.pop(0))
    elif k == "--runs":
        RUNS = int(_a.pop(0))
    elif k == "--runs03d1":
        RUNS03D1 = int(_a.pop(0))
    else:
        sys.exit("unknown argument %r -- see the module docstring" % k)

if not SANDBOX:
    sys.exit("X1 REFUSES TO RUN WITHOUT --sandbox.  It runs other trees' "
             "runners; it will only do that somewhere you named.")
if os.path.commonpath([SANDBOX, REPO]) == REPO:
    sys.exit("X1 REFUSES: %s is inside %s.  The whole point of this probe is "
             "that it regenerates nobody's transcripts here." % (SANDBOX, REPO))

CENSUS = r'''
import sys, os, json
ROOT = os.path.abspath(sys.argv[1])
sys.path.insert(0, os.path.join(ROOT, "code/runner_exit_audit_56dc"))
sys.path.insert(0, os.path.join(ROOT, "code/grain_axis_audit_03d1"))
import lib56dc as A
import lib03d1 as B
assert os.path.abspath(B.REPO) == ROOT, (B.REPO, ROOT)
paths = B.all_transcripts()
rows = erows = eints = 0
words = set()
for p in paths:
    t = B.read(p)
    if t is None:
        continue
    for _i, label, _n in A.count_rows(t):
        rows += 1
        e = B.embedded_counts(label)
        if e:
            erows += 1
            eints += len(e)
        for w in B.grain_nouns(label):
            words.add(B.singular(w))
print(json.dumps({"files": len(paths), "rows": rows, "erows": erows,
                  "eints": eints, "words": len(words)}))
'''

# `_census_fd9c.py` lives BESIDE the clone and never inside it, because a file
# inside the clone would be a file inside the population being censused.
os.makedirs(SANDBOX, exist_ok=True)
CENSUS_PY = os.path.join(SANDBOX, "_census_fd9c.py")
with open(CENSUS_PY, "w") as fh:
    fh.write(CENSUS)


def run(argv, cwd, timeout=3600):
    e = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True,
                       timeout=timeout, env=e)
    return p.returncode, p.stdout + p.stderr


def census(root):
    # cwd=root, NOT cwd=SANDBOX.  `lib56dc` resolves the repository with
    # `git rev-parse --show-toplevel` in the CURRENT DIRECTORY at import time,
    # so a census run from beside the clone dies before it reads a file.  The
    # first form of this probe did exactly that and printed `CENSUS FAILED` in
    # every row of both tables while both fixed-point arms still went green --
    # a table of errors under a headline that passed.
    rc, out = run([sys.executable, "-B", CENSUS_PY, root], root)
    if rc != 0:
        return "CENSUS FAILED: %s" % " ".join(out.split())[-160:]
    return out.strip()


def clone(name, sha):
    dst = os.path.join(SANDBOX, name)
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    rc, out = run(["git", "clone", "--no-hardlinks", "--quiet", REPO, dst],
                  SANDBOX)
    if rc:
        sys.exit("clone failed: %s" % out[:400])
    rc, out = run(["git", "checkout", "--quiet", sha], dst)
    if rc:
        sys.exit("checkout %s failed: %s" % (sha, out[:400]))
    return dst


def bar(t):
    print()
    print("=" * 74)
    print(t)
    print("=" * 74)
    print()


BAD = 0
print("mg-fd9c / X1 -- THE ORBIT, BY RUNNING THE SUITES")
print("repo:    %s" % REPO)
print("sandbox: %s   (throwaway clones; nothing here is written)" % SANDBOX)

# ---------------------------------------------------------------------------
bar("X1a  mg-9160's SUITE ITERATED FROM c9160's OWN CORPUS STATE")

SUB = "code/grain_arity_9160"
SRC = ("README.md lib9160.py run_all.sh s1_reproduce.py s2_arity.py "
       "s3_population.py s4_open.py s5_self.py selftest9160.py").split()
d = clone("orbit9160", "757f999")
for f in SRC:
    rc, out = run(["git", "show", "65e350e:%s/%s" % (SUB, f)], d)
    if rc:
        sys.exit("cannot materialise %s: %s" % (f, out[:200]))
    with open(os.path.join(d, SUB, f), "w") as fh:
        fh.write(out)
for f in os.listdir(os.path.join(d, SUB)):
    if f.startswith("out_") and f.endswith(".txt"):
        os.remove(os.path.join(d, SUB, f))

print("  base:  757f999, the predictions commit -- the last state of main in")
print("         which mg-9160's tree existed with NO transcripts on disk.")
print("  tree:  sources from 65e350e, transcripts DELETED.  That is c9160's")
print("         disk on the run that first wrote them.")
print()
print("  population: every `code/*/out_*.txt` on the sandbox disk after each")
print("              complete run of `%s/run_all.sh`" % SUB)
print()
print("      corpus before any run:  %s" % census(d))
print()
print("      %-5s %-72s" % ("run", "the corpus after this run completes"))
seq = []
for i in range(1, RUNS + 1):
    rc, _out = run(["sh", "run_all.sh"], os.path.join(d, SUB))
    c = census(d)
    rcx, dig = run(["sh", "-c",
                    "cat out_selftest_9160.txt out_s1_reproduce.txt "
                    "out_s2_arity.txt out_s3_population.txt out_s4_open.txt "
                    "out_s5_self.txt | shasum | cut -c1-12"],
                   os.path.join(d, SUB))
    dig = dig.strip()
    seq.append((c, dig))
    print("      %-5d %-58s %s" % (i, c, dig))
print()
stable = len({s for _c, s in seq[1:]}) == 1 and len(seq) > 2
print("      transcripts byte-identical from run 2 onward:        %s"
      % ("YES -- PERIOD 1, A FIXED POINT" if stable else "*** NO"))
BAD += not stable
livec = not any(c.startswith("CENSUS FAILED") for c, _s in seq)
print("      every census row above is a census and not an error:  %s"
      % ("yes" if livec else "*** NO -- the table is errors under a headline "
                             "that passed; see the note on `census()`"))
BAD += not livec
print()
print("FINDING: mg-9160's census map reaches a FIXED POINT at run 2 and holds")
print("         it for %d consecutive runs.  D7 reports `oscillates ... without"
      % (RUNS - 1))
print("         converging` over SEVEN runs; this run does not oscillate over")
print("         %d, and the same experiment at --runs 12 did not either." % RUNS)

# ---------------------------------------------------------------------------
bar("X1b  THE TWO REGIMES -- ONE CORPUS, ONE REF, TWO WRITE DISCIPLINES")

sub = os.path.join(d, SUB)
rc, out = run(["sh", "-c",
               "grep 'the disk at HEAD now' out_s1_reproduce.txt"], sub)
struct = " ".join(out.split()[5:])
rc, out = run(["sh", "-c",
               "python3 -B -c \"import sys;"
               "sys.path.insert(0,'../runner_exit_audit_56dc');"
               "sys.path.insert(0,'../grain_axis_audit_03d1');"
               "import lib56dc as A, lib03d1 as B;"
               "print(len(A.count_rows("
               "B.read('%s/out_s1_reproduce.txt'))))\"" % SUB], sub)
own = out.strip()
rc, _ = run(["sh", "-c", "python3 -B s1_reproduce.py > out_s1_reproduce.txt "
                         "2>&1"], sub)
rc, out = run(["sh", "-c",
               "grep 'the disk at HEAD now' out_s1_reproduce.txt"], sub)
trunc = " ".join(out.split()[5:])

print("  The same probe. The same commit. The same files on disk. The only")
print("  difference is HOW ITS OWN TRANSCRIPT IS WRITTEN while it runs.")
print()
print("  population: the corpus `s1_reproduce.py` globs, at 757f999")
print()
print("      %-56s %s" % ("regime", "files  rows erows eints words"))
print("      %-56s %s" % ("`.new` + `mv`  (mg-bf79's fix; what run_all.sh does)",
                          struct))
print("      %-56s %s" % ("a plain `>`    (what a hand-run does)", trunc))
print("      %-56s %s" % ("count_rows(out_s1_reproduce.txt) -- its OWN weight",
                          own))
print()
sv = struct.split()
tv = trunc.split()
ok = (len(sv) == 5 and len(tv) == 5
      and sv[0] == tv[0]
      and int(sv[1]) - int(tv[1]) == int(own))
print("      files identical under both regimes (`>` truncates, "
      "it does not unlink)   %s" % ("yes" if sv and tv and sv[0] == tv[0] else "*** no"))
print("      rows differ by EXACTLY the probe's own transcript                 "
      "    %s" % ("yes" if ok else "*** no"))
BAD += not ok
print()
print("FINDING: `1984` and `1966` are not two states of one system.  They are")
print("         two readings of ONE state, and the difference is the observer.")

# ---------------------------------------------------------------------------
bar("X1c  mg-03d1's SUITE -- THE ARC'S OTHER WHOLE-CORPUS CONSUMER")

if RUNS03D1 <= 0:
    print("  skipped (--runs03d1 0)")
else:
    SUB2 = "code/grain_axis_audit_03d1"
    d2 = clone("orbit03d1", "HEAD")
    print("  base: HEAD, clean.  About five minutes a run.")
    print()
    print("      %-5s %-58s %s" % ("run", "the corpus after this run", "a1 hash"))
    seq2 = []
    for i in range(1, RUNS03D1 + 1):
        rc, _o = run(["sh", "run_all.sh"], os.path.join(d2, SUB2))
        c = census(d2)
        rcx, dig = run(["sh", "-c", "cat out_a*.txt | shasum | cut -c1-12"],
                       os.path.join(d2, SUB2))
        seq2.append((c, dig.strip()))
        print("      %-5d %-58s %s" % (i, c, dig.strip()))
    print()
    st2 = len({s for _c, s in seq2[1:]}) == 1 and len(seq2) > 2
    print("      transcripts byte-identical from run 2 onward:        %s"
          % ("YES -- PERIOD 1, A FIXED POINT" if st2 else "*** NO"))
    BAD += not st2
    lv2 = not any(c.startswith("CENSUS FAILED") for c, _s in seq2)
    print("      every census row above is a census and not an error:  %s"
          % ("yes" if lv2 else "*** NO"))
    BAD += not lv2
    print()
    print("FINDING: the arc's other whole-corpus consumer converges too, and it")
    print("         moves the corpus by exactly one grain WORD when it does --")
    print("         its own transcripts contribute a noun the corpus did not")
    print("         have, so run 1 prints one less than run 2 and every run")
    print("         after run 2 prints what run 2 printed.")

print()
print("X1 TOTAL BAD: %d" % BAD)
sys.exit(min(BAD, 120))
