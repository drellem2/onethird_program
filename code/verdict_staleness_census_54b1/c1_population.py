"""mg-54b1 C1 -- THE POPULATION, AND WHO IS WATCHING IT.

The expensive half of this ticket's question is `how many are stale?` and needs
a run per instrument.  The CHEAP half is `how many is nobody asking?`, and it
is exact, needs no runs at all, and is the half that does not go stale between
one commit and the next -- it is recomputed from `git ls-files` every time.

Three populations, and this arm's whole content is that they are different:

  ALL         every directory under code/ carrying a tracked out_*.txt
  GATED       the suites ./build.sh loops, whose transcripts mg-f771 regrades
              on every merge.  By that gate's OWN construction -- quoted in
              its transcript -- `a transcript no suite rewrites is never
              modified and therefore never appears`
  CENSUSED    the 44 candidates mg-20ee's ground_truth.sh re-ran

Everything else is the blind spot, and `code/species_extent_audit_6cb9` sat in
it until a polecat happened to run it for an unrelated reason.
"""

import os
import re
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip()
HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)), REPO)


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=REPO,
                          capture_output=True, text=True).stdout


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
    print()


bad = 0

# --- ALL -------------------------------------------------------------------
transcripts = [p for p in git("ls-files", "code/").splitlines()
               if re.match(r'code/.*/out_[^/]*\.txt$', p)]
all_dirs = sorted({os.path.dirname(p) for p in transcripts})
runnable = sorted(d for d in all_dirs
                  if os.path.isfile(os.path.join(REPO, d, "run_all.sh")))

# --- GATED: read out of build.sh rather than written down here -------------
build = open(os.path.join(REPO, "build.sh"), encoding="utf-8").read()
loop = re.search(r'^for suite in\s*\\?\n(.*?)^do', build, re.S | re.M)
gated = sorted(set(re.findall(r'(code/[a-z0-9_]+)/', loop.group(1) if loop else "")))
# the gate's own runner is invoked after the loop, by name
gated = sorted(set(gated) | set(re.findall(
    r'sh (code/[a-z0-9_]+)/run_all\.sh', build)))

# --- CENSUSED: read out of mg-20ee's own transcript ------------------------
gt = os.path.join(REPO, "code/asof_census_20ee/out_ground_truth.txt")
censused = sorted(set(re.findall(r'^\s+(code/[a-z0-9_/]+) (?:DIFFERS|REPRODUCES|NO_RUN_ALL)',
                                 open(gt, encoding="utf-8").read(), re.M)))

covered_early = set(gated) | set(censused)
blind_runnable_early = [d for d in runnable if d not in covered_early]

if len(sys.argv) > 2 and sys.argv[1] == "--sample":
    # THE SAMPLE IS A FUNCTION OF THE PATH AND OF NOTHING ELSE, so it is the
    # same 40 on every host and in every clone, and it cannot have been chosen
    # after the answers were known.  Ordering by md5 rather than by name
    # because the names are alphabetical by topic and a prefix of that is not
    # a sample of anything.  There is no seed to lose and no shuffle to
    # reproduce.  `sweep_54b1.sh` takes its work list from exactly here, so
    # the population and the sweep cannot drift apart.
    import hashlib
    for _d in sorted(blind_runnable_early,
                     key=lambda p: hashlib.md5(p.encode()).hexdigest()
                     )[:int(sys.argv[2])]:
        print(_d)
    sys.exit(0)

hdr("mg-54b1 C1  THE POPULATION, AND THE SIZE OF THE BLIND SPOT")

print("  Recomputed from `git ls-files` and from build.sh and mg-20ee's own")
print("  transcript on every run.  Nothing below is a written-in number.")
print()
print("  tracked transcripts under code/ (out_*.txt)      %5d" % len(transcripts))
print("  directories carrying at least one                %5d" % len(all_dirs))
print("      of those, with a run_all.sh to re-take them  %5d" % len(runnable))
print("      with NO runner at all                        %5d"
      % (len(all_dirs) - len(runnable)))
print()
print("  WATCHED BY ./build.sh's LOOP (mg-f771 regrades these)")
for d in gated:
    print("      %s" % d)
print("      %5d directories" % len(gated))
print()
# THIS PARSE IS THE ONE THING HERE THAT CAN FAIL SILENTLY.  A build.sh whose
# loop is written differently would match nothing, `gated` would be empty, and
# the blind spot would be reported LARGER than it is -- a finding manufactured
# by a regex.  So every entry is resolved to a file on disk, and finding none
# at all is scored.  It is NOT scored against a fixed count: 9cee8b0 took this
# loop from nine suites to eight, and a control that reddens when the gate
# legitimately shrinks is the wrong-direction shape mg-686c landed a commit
# about.
unresolved = [d for d in gated
              if not os.path.isfile(os.path.join(REPO, d, "run_all.sh"))
              and not os.path.isfile(os.path.join(REPO, d, "run_a4_census.sh"))]
if unresolved or not gated:
    bad += 1
    print("      *** THE build.sh PARSE DID NOT RESOLVE: %s ***"
          % (unresolved or "no suites matched at all"))
else:
    print("      every entry resolves to a runner on disk              ok")
print()
print("  RE-RUN BY mg-20ee's ground_truth.sh                %5d candidates"
      % len(censused))
print()

covered = set(gated) | set(censused)
blind = [d for d in all_dirs if d not in covered]
blind_runnable = [d for d in runnable if d not in covered]

print("  THE BLIND SPOT -- in NEITHER population")
print("      directories carrying a transcript            %5d" % len(blind))
print("      of those, runnable                           %5d" % len(blind_runnable))
print("      of those, with no runner                     %5d"
      % (len(blind) - len(blind_runnable)))
print()
print("      %.0f%% of every transcript-carrying directory in this repository"
      % (100.0 * len(blind) / max(1, len(all_dirs))))
print("      is re-taken by nothing on any schedule.")
print()

hdr("§2  THE INSTANCE THAT PROVES THE TWO POPULATIONS ARE DIFFERENT")

SUBJ = "code/species_extent_audit_6cb9"
rows = [("in ./build.sh's loop", SUBJ in gated, False),
        ("in mg-20ee's 44 candidates", SUBJ in censused, False),
        ("carries tracked transcripts", any(p.startswith(SUBJ + "/")
                                            for p in transcripts), True),
        ("has a run_all.sh", SUBJ in runnable, True)]
for label, got, expect in rows:
    ok = (got == expect)
    bad += (not ok)
    print("  %-36s %-5s %s" % (label, "yes" if got else "no",
                               "ok" if ok else "*** FAILED ***"))
print()
print("""  mg-20ee's census.py is a classifier for FOREIGN ADDRESSES -- a transcript
  that names a file or a commit outside the instrument that wrote it.  6cb9
  carries none, so it was never nominated, and `A1 TOTAL BAD: 1` -> `0` is a
  verdict that moved without any address moving at all.  That is the whole
  argument that the strong sense needs its own census: the classifier that
  produced the 44 cannot in principle find this population.""")
print()

hdr("§3  THIS INSTRUMENT IS IN ITS OWN BLIND SPOT, AND IT IS NOT EXEMPT")

here_transcripts = sorted(p for p in transcripts if p.startswith(HERE + "/"))
print("  %s" % HERE)
print("      in ./build.sh's loop          %s" % ("yes" if HERE in gated else "no"))
print("      in mg-20ee's 44               %s" % ("yes" if HERE in censused else "no"))
print("      counted in the blind spot     %s"
      % ("yes" if HERE in blind else "*** NO -- EXEMPTED ITSELF ***"))
for p in here_transcripts:
    print("      carries %s" % p)
print()
print("""  THE EXPENSIVE ARM OF THIS INSTRUMENT IS ITSELF A TRANSCRIPT NO RUNNER
  REWRITES.  out_sweep_54b1.txt records ONE DATED RUN of sweep_54b1.sh over a
  sample; run_all.sh does not re-take it, because it costs about an hour and
  executes every instrument in the sample.  So this directory's own sweep
  transcript will go stale in exactly the sense it was built to count, and
  saying so here is the only thing that distinguishes it from the 137.

  mg-20ee's out_ground_truth.txt has the same property and says so in its own
  header: `It is NOT a fixed point and does not claim to be`.  The two cheap
  arms -- c0 and this one -- ARE re-taken by run_all.sh and are fixed points.""")

# A row that fails the day this directory quietly exempts itself.
if HERE not in blind:
    bad += 1

print()
print("=" * 78)
print("C1 TOTAL BAD: %d" % bad)
print("=" * 78)

# The list itself, so a successor can sweep the rest.
print()
print("THE %d RUNNABLE DIRECTORIES IN THE BLIND SPOT:" % len(blind_runnable))
for d in blind_runnable:
    print("  %s" % d)

sys.exit(1 if bad else 0)
