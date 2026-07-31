"""k1_grain.py -- THE TWO SITES, REPAIRED, AND SHOWN FIRING.

mg-321d's G-1 and G-2 are two spellings of one error: a provenance question
asked at the grain of a CONTAINER (a file; "whatever is not yet committed")
where the property is about a MEASUREMENT and about a COMMIT.

A repair for that could be made to look right two cheap ways, and this script
exists to close both:

  * g1 could be made to exit 0 by DELETING the finding.  So g1 is run,
    unmodified and in place, against a tree where the measuring half really
    did move, and it must go red.  A gate that cannot fire is not a gate, and
    "g1 stopped exiting 1" is exactly what silencing looks like from outside.
  * g4 could be made to print the right two numbers by writing the right two
    numbers.  So the attribution is re-derived HERE by two routes that share
    no code with g4 -- `git log -- <path>` and `git show --name-only` -- and
    compared cell by cell against what g4 prints.

The BEFORE state is not quoted from mg-321d either.  It is reproduced: a clone
checked out at ef38841 runs the unrepaired g1 and g4 and their own output is
read.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import re
import sys

import lib7e58 as L

R = L.Report("k1", "the 2 sites, each measured BEFORE and AFTER at its own "
                   "grain, the 3 deletion probes that must make the repaired "
                   "g1 fire, and the 2 independent derivations of g4's "
                   "attribution compared against every one of the five")

L.banner("K1", "THE TWO PROVENANCE SITES, REPAIRED AT THE GRAIN OF THE PROPERTY")

HEAD = L.head_rev()
print()
print("   worktree HEAD          : %s" % HEAD)
print("   the audit being answered: %s (mg-321d)" % L.REV_321D[:12])
print("   the repair it audits    : %s (mg-58da)" % L.REV_58DA[:12])
print("   the reproduction's home : %s (mg-a218)" % L.REV_A218[:12])

# ---------------------------------------------------------------------------
L.rule("(i) THE BEFORE STATE, REPRODUCED RATHER THAN QUOTED")
print("""   A clone of this worktree is checked out at %s -- the tree mg-321d
   audited -- and g1 and g4 are run there, unmodified.  Whatever they print is
   what the defect actually was."""
      % L.REV_321D[:8])
print()


def at_revision(rev, scripts):
    tmp, tree = L.scratch_clone(carry=False)   # the tree as committed, not mine
    try:
        L.git("checkout", "-q", rev, repo=tree)
        got = {}
        for s in scripts:
            out, rc = L.run_script(L.S58DA_DIR, s, repo=tree)
            got[s] = (out, rc)
        return got
    finally:
        L.destroy(tmp)


before = at_revision(L.REV_321D, ["g1_provenance.py", "g4_fleet.py"])

b1_out, b1_rc = before["g1_provenance.py"]
b1_self, b1_find = L.totals_of(b1_out)
b1_grain = [x for x in L.findings_of(b1_out)
            if "measuring half of the reproduction is not the same code" in x]
print("   g1 @ %s : SELF %s  FINDINGS %s  exit %d"
      % (L.REV_321D[:8], b1_self, b1_find, b1_rc))
for x in b1_grain:
    print("      FINDING: %s" % x[:150])
R.check(bool(b1_grain) and b1_rc == 1,
        "the BEFORE state does not reproduce: g1 at %s does not exit 1 with "
        "the file-grain finding mg-321d's G-1 reports (exit %d, findings %s)"
        % (L.REV_321D[:8], b1_rc, b1_find))

b4_out, b4_rc = before["g4_fleet.py"]
b4_said = {}
for line in b4_out.splitlines():
    t = line.strip()
    if t.startswith("of the five, touched by ed9cde4"):
        b4_said["mg-13b2"] = t.split(":", 1)[1].strip()
    elif t.startswith("of the five, touched by mg-58da"):
        b4_said["mg-58da"] = t.split(":", 1)[1].strip()
print()
print("   g4 @ %s attribution summary, as printed there:" % L.REV_321D[:8])
for k in ("mg-13b2", "mg-58da"):
    print("      %-8s : %s" % (k, b4_said.get(k, "(line not found)")))
R.check("c1_branching.py" in b4_said.get("mg-13b2", ""),
        "the BEFORE state does not reproduce: g4 at %s does not attribute "
        "c1_branching.py to ed9cde4, which is mg-321d's G-2"
        % L.REV_321D[:8])

# ---------------------------------------------------------------------------
L.rule("(ii) SITE 1 AFTER -- THE QUESTION ASKED OF THE MEASUREMENT")
print("""   The claim g1 used to make is 'the measuring half of the reproduction
   is not the same code', on the evidence that c1_branching.py's sha moved.
   It is re-derived here, in this script, on this script's own reader: run
   BOTH script revisions against THE SAME target -- both target forms -- and
   compare c1's own sections (i)+(ii) and the 24 vertex cells parsed out of
   them.""")
print()

MARK = "(iii) EVERY CELL, AGAINST"
old_c1 = L.git_show(L.REV_A218, L.A218_DIR + "/c1_branching.py")
head_c1 = L.git_show(HEAD, L.A218_DIR + "/c1_branching.py")
old_target = L.git_show(L.REV_A218, L.TARGET_REL)
head_target = L.read_worktree(L.TARGET_REL)
R.check(old_target != head_target,
        "the two target forms are the same text, so running the check on "
        "'both' of them is one check reported twice")


def measure(c1_src, target_text, kern_rev=L.REV_A218):
    """c1's measuring half only -- everything it prints before it compares."""
    import shutil
    import subprocess
    import tempfile
    tmp = tempfile.mkdtemp(prefix="mg7e58-m-")
    try:
        a = os.path.join(tmp, "a218")
        d = os.path.join(tmp, "branching_locate_db09")
        os.makedirs(a)
        os.makedirs(d)
        with open(os.path.join(a, "c1_branching.py"), "w") as fh:
            fh.write(c1_src)
        with open(os.path.join(a, "kern_a218.py"), "w") as fh:
            fh.write(L.git_show(kern_rev, L.A218_DIR + "/kern_a218.py"))
        with open(os.path.join(d, "out_t1_tl.txt"), "w") as fh:
            fh.write(target_text)
        p = subprocess.run(["python3", "c1_branching.py"], cwd=a,
                           capture_output=True, text=True)
        out = p.stdout + p.stderr
        return out.split(MARK)[0], L.c1_cells(out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


print("   target form                     c1 @ %s   c1 @ %s   cells"
      % (L.REV_A218[:8], HEAD[:8]))
meas_same = True
for tname, ttext in [("the %s target (COUNT)" % L.REV_A218[:8], old_target),
                     ("the HEAD target (SET)", head_target)]:
    ma, ca = measure(old_c1, ttext)
    mb, cb = measure(head_c1, ttext)
    ok = ma == mb and ca == cb and len(ca) == 24
    meas_same &= ok
    print("     %-30s %-16s %-16s  %d/%d  %s"
          % (tname, L.sha(ma)[:16], L.sha(mb)[:16], len(ca), len(cb),
             "IDENTICAL" if ok else "MOVED"))
print()
print("   the file grain, for contrast:")
for f in ("c1_branching.py", "kern_a218.py"):
    p = L.A218_DIR + "/" + f
    print("     %-20s %s"
          % (f, "CHANGED" if L.sha(L.git_show(L.REV_A218, p))
             != L.sha(L.git_show(HEAD, p)) else "SAME"))
print()
print("   THE FILE MOVED AND THE MEASUREMENT DID NOT -- so g1's old finding")
print("   was false of the property it names, and the section that refutes it")
print("   was right.  The disposition is: THE SECTION IS RIGHT AND g1 SHOULD")
print("   NOT FIRE, and the way it is made not to fire is (iii).")
print()

g1_out, g1_rc = L.run_script(L.S58DA_DIR, "g1_provenance.py")
g1_self, g1_find = L.totals_of(g1_out)
print("   g1 on the repaired tree, run in place : SELF %s  FINDINGS %s  exit %d"
      % (g1_self, g1_find, g1_rc))
still = [x for x in L.findings_of(g1_out)
         if "measuring half of the reproduction is not the same code" in x]
R.check(meas_same and g1_rc == 0 and g1_find == 0 and not still,
        "the repaired g1 does not settle at exit 0 with 0 findings on a tree "
        "where the measurement provably did not move (exit %d, findings %s)"
        % (g1_rc, g1_find))
R.check(not meas_same or not still,
        "the repaired g1 still books the file-grain finding")

# ---------------------------------------------------------------------------
L.rule("(iii) SITE 1 DELETION TEST -- g1 ITSELF, MADE TO GO RED")
print("""   This is the check that separates a repair from a silencing.  g1 is
   NOT modified and NOT called with arguments: it is run in place, in a clone
   whose c1_branching.py carries a real regression in the MEASURING half, and
   it must exit 1 and say the measurement moved.  A hook planted for a probe
   to find would not survive this, because the mutation is made to c1 -- the
   thing g1 measures -- and never to g1.""")
print()


def mutate_dims(tree):
    """Every simple's dimension off by one: the shape a kernel regression
    takes, applied to the file g1 reads at HEAD."""
    p = os.path.join(tree, L.A218_DIR, "c1_branching.py")
    with open(p) as fh:
        src = fh.read()
    with open(p, "w") as fh:
        fh.write(L.replace_once(
            src,
            "        mine_vertices[(beta, n)] = algebras[(n, beta)].vertices()",
            "        mine_vertices[(beta, n)] = [(p, d + 1) for p, d in "
            "algebras[(n, beta)].vertices()]"))


def mutate_comment(tree):
    """A comment added to c1: the file moves, the measurement cannot."""
    p = os.path.join(tree, L.A218_DIR, "c1_branching.py")
    with open(p) as fh:
        src = fh.read()
    with open(p, "w") as fh:
        fh.write(src + "\n# mg-7e58 null probe: this line measures nothing\n")


def mutate_compare(tree):
    """An edit confined to the COMPARING half -- mg-58da's own edit class."""
    p = os.path.join(tree, L.A218_DIR, "c1_branching.py")
    with open(p) as fh:
        src = fh.read()
    with open(p, "w") as fh:
        # AFTER the (iii) header, which is where the comparing half starts;
        # inserting before it would land inside the measuring half and the
        # probe would be testing the opposite of what it claims to test.
        fh.write(L.replace_once(
            src, 'print("(iii) EVERY CELL, AGAINST mg-e8b8\'s COMMITTED '
                 'out_t1_tl.txt")\n',
            'print("(iii) EVERY CELL, AGAINST mg-e8b8\'s COMMITTED '
            'out_t1_tl.txt")\n'
            'print("   [mg-7e58 probe: comparing half touched]")\n'))


PROBES = [
    ("UNMODIFIED clone (NULL PROBE)", None, 0,
     "nothing moved; g1 must stay green"),
    ("c1's vertex DIMENSIONS off by one", mutate_dims, 1,
     "the measuring half really moved; g1 must go red"),
    ("a comment appended to c1", mutate_comment, 0,
     "the file sha moves and the measurement does not -- the exact case the "
     "old g1 got wrong"),
    ("an edit inside c1's comparing half", mutate_compare, 0,
     "mg-58da's own edit class; g1 must stay green"),
]
print("   clone                                   predicted   g1 exit  finding")
nhit = 0
for pname, mut, pred_rc, why in PROBES:
    tmp, tree = L.scratch_clone(mutate=mut)
    try:
        out, rc = L.run_script(L.S58DA_DIR, "g1_provenance.py", repo=tree)
    finally:
        L.destroy(tmp)
    says = [x for x in L.findings_of(out) if "measurement is not the same" in x]
    ok = rc == pred_rc and bool(says) == bool(pred_rc)
    nhit += ok
    print("     %-38s exit %d      exit %-3d %s   %s"
          % (pname[:38], pred_rc, rc, "YES" if says else "no ",
             "HIT" if ok else "MISS"))
    print("       why: %s" % why)
    if says:
        print("       %s" % says[0][:140])
    if not ok:
        R.finding("the repaired g1 on the %r clone: predicted exit %d, got "
                  "exit %d (measurement finding %s). Either the repair "
                  "silenced g1 or its new predicate does not discriminate"
                  % (pname, pred_rc, rc, "raised" if says else "absent"))
print()
print("   probes whose direction was predicted correctly : %d of %d"
      % (nhit, len(PROBES)))
print("   population: the %d clones above, each running g1 UNMODIFIED in place."
      % len(PROBES))

# ---------------------------------------------------------------------------
L.rule("(iv) SITE 2 AFTER -- ATTRIBUTION DERIVED TWICE, INDEPENDENTLY OF g4")
print("""   Two routes to the same fact, neither of them g4's:

     A. `git log %s..HEAD -- <path>` per member
     B. `git show --name-only <commit>` per commit, filtered to the directory

   If they disagree, this script says so about ITSELF and compares nothing.
   Only when they agree is the result put beside what g4 prints.""" % L.REV_A218[:8])
print()
route_a = {}
for f in L.FIVE:
    route_a[f] = sorted(L.commits_touching(L.A218_DIR + "/" + f,
                                           L.REV_A218, HEAD))
range_commits = L.commits_touching(L.A218_DIR, L.REV_A218, HEAD)
route_b = {f: [] for f in L.FIVE}
for h in range_commits:
    for p in L.names_in(h):
        base = p.split("/")[-1]
        if p.startswith(L.A218_DIR + "/") and base in route_b:
            route_b[base].append(h)
for f in L.FIVE:
    route_b[f] = sorted(route_b[f])

print("   member                  route A (git log)     route B (name-only)")
for f in L.FIVE:
    print("     %-22s %-21s %s"
          % (f, ", ".join(x[:8] for x in route_a[f]) or "none",
             ", ".join(x[:8] for x in route_b[f]) or "none"))
    if route_a[f] != route_b[f]:
        R.selferr("this script's two routes disagree about %s (%s vs %s); it "
                  "compares nothing until they agree"
                  % (f, [x[:8] for x in route_a[f]],
                     [x[:8] for x in route_b[f]]))
print()

TRUTH = {}
for f in L.FIVE:
    for h in route_a[f]:
        TRUTH.setdefault(h, []).append(f)
for h in TRUTH:
    TRUTH[h] = sorted(TRUTH[h])
def ticket_of(rev):
    """The mg-id the commit's own subject carries.  Derived, not written."""
    m = re.search(r"\(mg-([0-9a-f]{4})\)\s*$", L.subject(rev).strip())
    return "mg-" + m.group(1) if m else "?"


print("   the truth, inverted -- one row per commit in the range:")
for h in range_commits:
    print("     %-8s %-9s touches %s"
          % (h[:8], ticket_of(h), ", ".join(TRUTH.get(h, [])) or "none"))
print()

g4_out, g4_rc = L.run_script(L.S58DA_DIR, "g4_fleet.py")
said = {}
for line in g4_out.splitlines():
    m = re.match(r"\s*of the five, touched by (\S+)(?: \((mg-\S+)\))?\s*:\s*"
                 r"(\d+) -- (.*)$", line)
    if m:
        key = m.group(2) or m.group(1)
        members = [] if m.group(4).strip() == "none" else [
            x.strip() for x in m.group(4).split(",")]
        said[key] = (int(m.group(3)), sorted(members))

print("   what g4 prints, against the truth derived above:")
print("     ticket    g4 says                        truth")
for ticket, rev in (("mg-13b2", L.REV_13B2), ("mg-58da", L.REV_58DA)):
    truth = TRUTH.get(rev, [])
    got = said.get(ticket)
    print("     %-9s %-30s %s"
          % (ticket,
             "%d -- %s" % (got[0], ", ".join(got[1]) or "none")
             if got else "(line not found)",
             "%d -- %s" % (len(truth), ", ".join(truth) or "none")))
    R.check(got is not None and got[1] == truth and got[0] == len(truth),
            "g4's attribution for %s does not match the history: g4 says %s, "
            "`git log` and `git show --name-only` both say %s"
            % (ticket, got, truth))
print()
print("   g4 on the repaired tree : exit %d, and it is PREDICTED to exit 1 --"
      % g4_rc)
print("   c3_withdrawal.py is red (mg-d330's second finding, OPEN) and the e4")
print("   presence-test finding is booked and not worked around.  Neither is")
print("   an attribution finding; both are checked by name in k3.")

sys.exit(R.emit())
