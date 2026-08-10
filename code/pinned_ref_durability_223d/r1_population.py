"""mg-223d / R1 -- THE SWEEP.  THE POPULATION IS NAMED BEFORE THE COUNT IS.

The ticket's instruction is exact: *state the population you searched; cfd9c's
finding was a single instance found incidentally, NOT a survey -- do not report
a clean result without naming what you examined.*

So this probe prints, in order: the DENOMINATOR, the RULE, WHAT THE RULE CANNOT
SEE, the FALSE-POSITIVE RATE of the rule, and only then the count.
"""
import sys

import lib223d as L

led = L.Ledger("mg-223d / R1 -- EVERY PINNED REF IN THE ARC, AND ITS ANCESTRY")

# ---------------------------------------------------------------------------
led.head("R1a  THE DENOMINATOR")
# ---------------------------------------------------------------------------
allfiles = L.tracked("HEAD")
code = [p for p in allfiles if p.endswith(".py") or p.endswith(".sh")]
other = [p for p in allfiles if p not in set(code)]
dirs = L.suite_dirs("HEAD")
print()
print("      tracked files at HEAD                             %5d" % len(allfiles))
print("        of which `*.py` / `*.sh`  (the pin population)  %5d" % len(code))
print("        of which everything else  (records)             %5d" % len(other))
print("      `code/*` directories holding tracked code         %5d" % len(dirs))
print("      ^ one unit of each of the first three is one FILE; of the last, one DIRECTORY")

# ---------------------------------------------------------------------------
led.head("R1b  THE TWO RULES, AND WHAT EACH CANNOT SEE")
# ---------------------------------------------------------------------------
print("""
  RULE A -- A PIN.  A 7-40 character hex run BETWEEN MATCHING QUOTES in a
  tracked `*.py` or `*.sh`, that resolves to a commit.  A pin is a DEPENDENCE:
  the object must still be there or the instrument does not run.

  RULE B -- A SIGHTING.  Any 7-40 character hex run in ANY tracked file, that
  resolves to a commit.  A sighting is a RECORD: a transcript saying what a
  commit was.  If the object dies the claim becomes uncheckable and nothing
  stops running.

  THE DISTINCTION IS THE WHOLE OF THE RESTRAINT IN THIS TREE, and the two
  numbers are both printed so a reader can see the one I did not report.

  WHAT RULE A CANNOT SEE, stated here rather than left in a docstring:
      - a rev built by concatenation or `.format()`
      - a rev read at run time out of a `.md` / `.json` / `.txt`
      - a rev taken from `sys.argv` or the environment
      - a rev in a language this arc does not use
  Each of those is a pin my count omits.  I did not find one; I also did not
  build a rule that could.""")

# ---------------------------------------------------------------------------
led.head("R1c  THE FALSE-POSITIVE RATE, MEASURED, NOT ASSUMED")
# ---------------------------------------------------------------------------
for ln in (7, 8, 12, 40):
    hit, n = L.collision_rate(600, ln)
    print("      %3d random %2d-hex tokens                 resolving: %d"
          % (n, ln, hit))
hit7, n7 = L.collision_rate(600, 7)
led.record(None, "at 7 hex -- the shortest form the arc uses -- %d of %d random "
           "tokens resolve" % (hit7, n7))
print("""
      SO `IT RESOLVES` IS NEARLY A DECISIVE TEST, and P5 -- my own bet that
      the wide count would be mostly coincidence -- is heading for a LOSS.
      The reason the wide number still is not the headline is NOT that it is
      false.  It is that a record and a dependence are different things.""")

# ---------------------------------------------------------------------------
led.head("R1d  RULE A: EVERY PIN, AND WHETHER IT IS AN ANCESTOR OF HEAD")
# ---------------------------------------------------------------------------
ps = L.pins()
res = L.commits(ps.keys())
anc = {s: L.is_ancestor(f, "HEAD") for s, f in res.items()}
off = sorted(s for s in res if not anc[s])
offfull = sorted(set(res[s] for s in off))
print()
print("      quoted hex literals in tracked code               %5d  tokens" % len(ps))
print("        of which resolve to a commit                    %5d  tokens" % len(res))
print("          of which ARE ancestors of HEAD                %5d  tokens"
      % sum(1 for s in res if anc[s]))
print("          of which are NOT ancestors of HEAD            %5d  tokens" % len(off))
print("      the same, counted as COMMITS rather than tokens   %5d  commits" % len(offfull))
print("      ^ E2: `3738079` and `37380799` are two tokens and one commit.  Both")
print("        numbers are true of different things and this tree says which.")

print()
print("      %-9s %-13s %-34s %s" % ("SHORT", "FULL", "DIRECTORIES THAT PIN IT", "SITES"))
bydir = {}
for s in off:
    ds = sorted(set(p.split("/")[1] if p.startswith("code/") else p.split("/")[0]
                    for p, _i, _t in ps[s]))
    bydir[s] = ds
    print("      %-9s %-13s %-34s %d"
          % (s, res[s][:12], ", ".join(ds)[:34], len(ps[s])))

pin_dirs = sorted(set(d for ds in bydir.values() for d in ds))
print()
led.record(None, "the %d off-history pins live in %d of the %d `code/*` "
           "directories" % (len(off), len(pin_dirs), len(dirs)))

# ---------------------------------------------------------------------------
led.head("R1e  ARE ANY OF THEM ALREADY DEAD?")
# ---------------------------------------------------------------------------
dead = [s for s in ps if s not in res and len(s) >= 8]
led.record(None, "quoted literals >=8 hex that do NOT resolve to a commit: %d"
           % len(dead))
for s in sorted(dead)[:12]:
    print("        %-10s  %s" % (s, ps[s][0][0]))
print("      ^ these are NOT necessarily dead refs.  A quoted hex run of 8+ is")
print("        far more often a digest, a colour, or a fixture than a sha, and")
print("        this tree does not claim otherwise.  R1f is where death is decided.")

# ---------------------------------------------------------------------------
led.head("R1f  WHAT HOLDS THE OFF-HISTORY PINS ALIVE -- THE FINDING")
# ---------------------------------------------------------------------------
print("""
  TWO COLUMNS, AND THE FIRST ONE IS THE FINDING.  `mg-223d` is the ticket that
  put the tags there, so once it has run, a table of `what holds this alive`
  reports DURABLE for everything and the defect vanishes from its own
  transcript.  That is a real failure mode for a repair that ships with its own
  audit, so both states are printed:

      AS FOUND  -- holders EXCLUDING `refs/tags/pin/*`.  This is the state
                   the arc was in when cfd9c filed D10, and it is what the
                   arc returns to the moment these tags are deleted.
      NOW       -- holders as they actually are on this run.""")
print()
print("      %-9s %-9s %-9s %s"
      % ("SHORT", "AS FOUND", "NOW", "HOLDING REFS (own branch excluded)"))
atrisk, tagged, noref, atrisk_asfound = [], [], [], []
holdercount = {}
for s in off:
    full = res[s]
    hs = L.holders(full)
    holdercount[s] = hs
    dh = L.durable_holders(full)
    pre = [h for h in dh if not h.startswith("refs/tags/pin/")]
    was = "NO-REF" if not hs else ("DURABLE" if pre else "AT-RISK")
    if not hs:
        cls = "NO-REF"
        noref.append(s)
    elif dh:
        cls = "DURABLE"
        tagged.append(s)
    else:
        cls = "AT-RISK"
        atrisk.append(s)
    if was == "AT-RISK":
        atrisk_asfound.append(s)
    print("      %-9s %-9s %-9s %s"
          % (s, was, cls, ", ".join(h.replace("refs/remotes/", "")
                                    .replace("refs/tags/", "tag:")
                                    for h in hs) or "*** NONE ***"))

branches = sorted(set(h for s in off for h in holdercount[s]))
remote = [b for b in branches if b.startswith("refs/remotes/")]
local = [b for b in branches if b.startswith("refs/heads/")]
print()
print("      distinct refs holding the whole off-history set   %5d" % len(branches))
print("        remote-tracking `origin/polecat-*`              %5d" % len(remote))
print("        local `refs/heads/polecat-*`                    %5d" % len(local))
print("        tags                                            %5d"
      % len([b for b in branches if b.startswith("refs/tags/")]))
print("      ^ one unit of each is one REF")

led.record(False, "AS FOUND -- off-history pins whose only holders were "
           "prunable branches: %d of %d.  THIS IS THE FINDING, and it is "
           "reported as one on every run, including runs where the repair has "
           "already landed" % (len(atrisk_asfound), len(off)))
led.record(len(atrisk) == 0,
           "NOW -- off-history pins still held only by prunable branches: "
           "%d of %d" % (len(atrisk), len(off)))
led.record(len(noref) == 0,
           "off-history pins held by NO ref at all (already floating): %d" % len(noref))

print("""
  WHY `AT-RISK` IS NOT ALARMISM.  Each of those refs is a MERGED polecat
  branch.  `pogo refinery prune` exists to delete merged branches; GitHub
  offers to do it on every merge; and a `git fetch --prune` afterwards drops
  the local remote-tracking ref.  Three ordinary, sanctioned, individually
  correct operations, in that order, and the object is unreferenced.  The
  next `git gc` collects it.  Nothing in the arc records that anything
  depends on it.""")

# ---------------------------------------------------------------------------
led.head("R1g  RULE B, FOR CONTRAST -- THE NUMBER I AM NOT REPORTING")
# ---------------------------------------------------------------------------
sg = L.sightings("HEAD")
sres = L.commits(sg.keys())
soff = sorted(s for s, f in sres.items() if not L.is_ancestor(f, "HEAD"))
soff_only = [s for s in soff if s not in set(off)]
print()
print("      hex tokens anywhere in any tracked file           %5d  tokens" % len(sg))
print("        resolving to a commit                           %5d  tokens" % len(sres))
print("          NOT ancestors of HEAD                         %5d  tokens" % len(soff))
print("            of those, RECORD only (no code pins them)   %5d  tokens" % len(soff_only))
print("            of those, REQUIRED (rule A found them too)  %5d  tokens"
      % (len(soff) - len(soff_only)))
print()
print("      THE HEADLINE THIS TREE DOES **NOT** RUN: `%d BROKEN PINS`." % len(soff))
print("      The honest headline is `%d`, and the difference is %d records that"
      % (len(off), len(soff_only)))
print("      name a commit without depending on it.  A dead record is a claim")
print("      you can no longer check; a dead pin is a program that no longer runs.")

sys.exit(led.done())
