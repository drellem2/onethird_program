"""s3_kernel_half.py -- THE CONFIRMATION MUST BE A DIFFERENCE, NOT A ZERO.

The parent finding: under the drifted anchor, BOTH sides of k1's pre-repair
comparison were mg-76cc's ALREADY-REPAIRED predicate.  A comparison of a
predicate with itself cannot show a difference -- it was not merely wrong, it
was VACUOUS BY CONSTRUCTION, and it printed a plausible number while being so.

So this script does not read k1's table.  It builds the two columns itself:

  (i)   ARE THE TWO COLUMNS TWO PREDICATES?  Established before either is
        run, at the source grain, on the property that IS the repair.
  (ii)  WHAT THE DRIFTED ANCHOR COMPARED.  The two revisions the OLD anchor
        would have picked, at the same grain.  If those two are one
        predicate, the vacuity is demonstrated rather than recalled.
  (iii) BOTH COLUMNS, RE-DERIVED.  The kernel bend, committed in a clone, run
        against g1 at 3bc2cf76 with ITS OWN lib58da and against g1 at HEAD.
        exit / self / findings for each.  The claim is 0/0/0 against 1/1/3.
  (iv)  AND THE SAME PAIR UNDER THE DRIFTED ANCHOR, RUN.  Not argued: the two
        drifted revisions are installed and run against the same bend, and
        what they print is put beside (iii).
  (v)   k1_prerepair.py itself, re-run, and its kernel-bend row read out of
        its own transcript -- so that (iii) has something INDEPENDENT to
        agree or disagree with.

Nothing here writes into code/branching_audit_e34a/ or
code/branching_audit_58da/.  Every run is in a clone under the system temp
directory.  The pinned installation is written FRESH here rather than by
calling libe34a.install_pinned: an audit that checks an apparatus by calling
that apparatus has checked nothing.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib330a as L                                          # noqa: E402

S58DA_DIR = "code/branching_audit_58da"

# The kernel bend, character for character out of libe34a's own constants --
# copied so the INPUT is the same input, while the machinery around it is not.
KERN_V = ("        return [(p, self.dim_L(p)) for p in self.parts "
          "if self.dim_L(p) > 0]")
KERN_V_UP = ("        return [(p, self.dim_L(p) + 1) for p in self.parts "
             "if self.dim_L(p) > 0]")

R = L.Report(
    selfpop="every clone, git read and subprocess run this script performs, "
            "plus the requirement that the kernel bend really change "
            "kern_a218.py, that each pinned g1 really import its OWN "
            "lib58da, and that each pinned source really differ from the "
            "repaired one",
    findpop="the two columns of the kernel-half confirmation, each "
            "RE-DERIVED here by installing the pinned predicate with its own "
            "library and running it against a committed kernel bend -- at "
            "the exit grain, the self-error grain and the finding grain; the "
            "same two columns under the anchor as it stood BEFORE the "
            "repair; and the source-grain question of whether either pair is "
            "one predicate twice")

L.banner("S3", "BOTH COLUMNS, RE-DERIVED -- IS THE CONFIRMATION A DIFFERENCE?")


def install_pinned(tree, rev, name):
    """g1 AND lib58da as of `rev`, into `tree`, with g1's import repointed.

    Written fresh from the sentence in libe34a's docstring: *the library has
    to travel with the predicate, because mg-76cc changed lib58da.run_c1's
    signature in the same commit as g1.*  Exactly one substitution, asserted.
    """
    libname = "lib58da_at_%s" % rev[:8]
    src = L.show_or_empty(rev, L.G1_REL)
    old = "import lib58da as L"
    if src.count(old) != 1:
        raise ValueError("g1 at %s has %d %r lines, not 1"
                         % (rev[:8], src.count(old), old))
    src = src.replace(old, "import %s as L" % libname, 1)
    with open(os.path.join(tree, S58DA_DIR, libname + ".py"), "w") as fh:
        fh.write(L.show_or_empty(rev, L.LIB58DA_REL))
    with open(os.path.join(tree, S58DA_DIR, name), "w") as fh:
        fh.write(src)
    return name


def trailer(out):
    """(SELF-ERRORS, FINDINGS) as the script's own trailer states them, and
    the count of listed FINDING lines beside it.

    The cross-check is deliberate: a script whose trailer says FINDINGS 3 and
    lists 2 is broken in a way a count-only reader cannot see.
    """
    s = f = None
    listed = 0
    for line in out.splitlines():
        if line.startswith("SELF-ERRORS:"):
            s = _lead(line.split(":", 1)[1])
        elif line.startswith("FINDINGS:"):
            f = _lead(line.split(":", 1)[1])
        elif line.strip().startswith("FINDING:"):
            listed += 1
    return s, f, listed


def _lead(s):
    out = ""
    for ch in s.strip():
        if ch.isdigit():
            out += ch
        else:
            break
    return int(out) if out else None


# The four revisions in play, derived here.
PROP_REPAIR = L.my_first_introducing(L.G1_REL, L.MARK_76CC)
PROP_PRE = L.resolve(PROP_REPAIR + "^")
DRIFT_REPAIR = L.my_last_touching(L.G1_REL)
DRIFT_PRE = L.resolve(DRIFT_REPAIR + "^")

# ---------------------------------------------------------------------------
L.rule("(i) ARE THE TWO COLUMNS TWO PREDICATES?  AT THE SOURCE GRAIN")
# ---------------------------------------------------------------------------

print("""   Asked BEFORE either column is run, because a comparison of a
   predicate with itself will print numbers whatever they are.  The
   property that IS mg-76cc's repair is the two-source signature
   `kernel_source=`: before it, the kernel was pinned on both sides of
   `run_c1` and a kernel that moved reached neither half.
""")

pairs = [("THE REPAIRED ANCHOR (property-derived)", PROP_PRE, "HEAD"),
         ("THE DRIFTED ANCHOR (history-derived)", DRIFT_PRE, DRIFT_REPAIR)]
print("   %-40s %-9s %-9s %s" % ("comparison", "OLD side", "NEW side", ""))
srcs = {}
for label, a, b in pairs:
    sa = L.show_or_empty(a, L.G1_REL)
    sb = L.show_or_empty(b, L.G1_REL)
    srcs[label] = (sa, sb)
    print("   %-40s %-9s %-9s" % (label, L.resolve(a)[:8], L.resolve(b)[:8]))
    print("      %-24s OLD: %-9s NEW: %-9s"
          % ("carries %r?" % L.MARK_76CC,
             "YES" if L.MARK_76CC in sa else "no",
             "YES" if L.MARK_76CC in sb else "no"))
    print("      %-24s %s"
          % ("g1 source sha differs?",
             "yes" if L.sha(sa) != L.sha(sb) else "*** IDENTICAL"))
    print("      %-24s %s"
          % ("lib58da source differs?",
             "yes" if L.sha(L.show_or_empty(a, L.LIB58DA_REL))
             != L.sha(L.show_or_empty(b, L.LIB58DA_REL))
             else "*** IDENTICAL"))
    same_pred = ((L.MARK_76CC in sa) == (L.MARK_76CC in sb))
    print("      %-24s %s" % ("SAME PREDICATE?",
                              "*** YES -- VACUOUS" if same_pred
                              else "no -- two predicates"))

pa, pb = srcs["THE REPAIRED ANCHOR (property-derived)"]
R.gate((L.MARK_76CC not in pa) and (L.MARK_76CC in pb),
       "the repaired comparison's two columns are NOT two predicates on the "
       "property that is mg-76cc's repair: %r is %s at the OLD side and %s "
       "at the NEW side.  The confirmation would be vacuous by construction"
       % (L.MARK_76CC, "present" if L.MARK_76CC in pa else "absent",
          "present" if L.MARK_76CC in pb else "absent"))

da, db = srcs["THE DRIFTED ANCHOR (history-derived)"]
print("""
   AND THE VACUITY, STATED AS A MEASUREMENT.  The drifted anchor's two
   sides both %s carry %r, so both were mg-76cc's ALREADY-REPAIRED
   predicate.  Their sources are %s -- which is why nothing looked
   wrong: it was not a comparison of a file with itself, it was a
   comparison of a predicate with itself, and only the SECOND of those
   is visible to a sha.
""" % ("DO" if (L.MARK_76CC in da and L.MARK_76CC in db) else "do NOT both",
       L.MARK_76CC,
       "different" if L.sha(da) != L.sha(db) else "identical"))

R.selfgate(L.MARK_76CC in da and L.MARK_76CC in db,
           "the drifted pair does not both carry the marker, so this tree "
           "cannot demonstrate the vacuity the parent finding is about")

# ---------------------------------------------------------------------------
L.rule("(iii) BOTH COLUMNS, RE-DERIVED -- THE KERNEL BEND, RUN")
# ---------------------------------------------------------------------------

print("""   The kernel bend is mg-957f's F-1: `dim L(n,p)` one too big in
   kern_a218.py -- the measuring half, IN THE KERNEL.  It is committed
   in a clone, because g1 reads the kernel with `git show` and an edit
   left in the working tree reaches nothing at all.

   Each pinned g1 travels with ITS OWN lib58da under a module name of
   its own.  A pre-repair g1 run against the repaired library is a
   third thing that never existed.
""")

# The fourth field is `must differ from HEAD`.
#
# DEFECT #3 OF THIS INSTRUMENT, KEPT.  The guard was first applied to EVERY
# pinned column, and s3's first run booked a SELF-ERROR saying `g1 at d01ff32d
# is byte-identical to g1 at HEAD, so the pinned column is not a different
# predicate`.  The guard is right for the two PROPERTY columns -- if the
# pre-repair source equalled HEAD's there would be no predicate to run -- and
# wrong for the drifted `the repair` column, whose whole point is that it IS
# the current predicate.  The instrument was scoring a fact as a fault.
#
# And the fact is worth more than the guard was: g1 at d01ff32d is BYTE-
# IDENTICAL to g1 at HEAD, so under the drifted anchor the column labelled
# `the predicate before this repair`s repair` was not merely the same
# predicate as HEAD's -- it was the same FILE.  Promoted from a self-error to
# evidence below.
COLUMNS = [
    ("BEFORE THE REPAIR (property)", PROP_PRE, "pinned", True),
    ("THIS REPAIR (HEAD)", None, "worktree", False),
    ("before the repair (DRIFTED)", DRIFT_PRE, "pinned", False),
    ("the repair (DRIFTED)", DRIFT_REPAIR, "pinned", False),
]

tree = L.clone_at("HEAD")
results = {}
try:
    ksrc = L.show_or_empty("HEAD", L.KERN_REL, repo=tree)
    R.selfgate(KERN_V in ksrc,
               "the kernel bend's target line is not in kern_a218.py at HEAD "
               "-- the input cannot be built")
    bent = ksrc.replace(KERN_V, KERN_V_UP, 1)
    R.selfgate(bent != ksrc, "the kernel bend did not change kern_a218.py")
    L.commit_in(tree, L.KERN_REL, bent,
                "probe: kern_a218.py dim L(n,p) one too big (mg-330a)")
    R.selfgate(L.show_or_empty("HEAD", L.KERN_REL, repo=tree) == bent,
               "the kernel bend did not reach git in the clone")

    d58 = os.path.join(tree, S58DA_DIR)
    print("   %-32s %-9s %-6s %-6s %-6s %s"
          % ("column", "revision", "exit", "self", "find", "listed"))
    for label, rev, how, must_differ in COLUMNS:
        if how == "worktree":
            name = "g1_provenance.py"
            shown = "HEAD"
        else:
            name = "g1_at_%s.py" % rev[:8]
            install_pinned(tree, rev, name)
            shown = rev[:8]
            same_as_head = (L.show_or_empty(rev, L.G1_REL)
                            == L.show_or_empty("HEAD", L.G1_REL))
            if must_differ:
                R.selfgate(not same_as_head,
                           "g1 at %s is byte-identical to g1 at HEAD, so the "
                           "pre-repair column is not a different predicate "
                           "and there is nothing to compare" % shown)
            elif same_as_head:
                print("   note: g1 at %s is BYTE-IDENTICAL to g1 at HEAD -- "
                      "this column\n         is not a comparison, it is the "
                      "current file under an old label" % shown)
        rc, out = L.run_py(name, d58, timeout=3600)
        s, f, listed = trailer(out)
        results[label] = (rc, s, f, listed, out)
        print("   %-32s %-9s %-6s %-6s %-6s %s"
              % (label, shown, rc,
                 "-" if s is None else s, "-" if f is None else f, listed))
        R.selfgate(f is None or f == listed,
                   "%s: the trailer says FINDINGS %s and %d FINDING line(s) "
                   "are listed" % (label, f, listed))

    old = results["BEFORE THE REPAIR (property)"]
    new = results["THIS REPAIR (HEAD)"]
    print("""
   THE CONFIRMATION, AS A DIFFERENCE:
     at %s the pre-repair predicate is  exit %s / self %s / find %s
     at HEAD     the repaired predicate is  exit %s / self %s / find %s
""" % (PROP_PRE[:8], old[0], old[1], old[2], new[0], new[1], new[2]))

    silent = (old[0] == 0 and old[1] == 0 and old[2] == 0)
    fires = (new[0] != 0 and (new[2] or 0) > 0)
    print("     the OLD column is %s"
          % ("SILENT (0/0/0) -- as the repair claims"
             if silent else "*** NOT SILENT (%s/%s/%s)"
             % (old[0], old[1], old[2])))
    print("     the NEW column %s"
          % ("FIRES (%s/%s/%s) -- as the repair claims"
             % (new[0], new[1], new[2]) if fires
             else "*** DOES NOT FIRE (%s/%s/%s)"
             % (new[0], new[1], new[2])))

    R.gate(silent,
           "the pre-repair predicate is NOT silent on the kernel bend "
           "(%s/%s/%s) -- the confirmation the repair rests on does not "
           "reproduce" % (old[0], old[1], old[2]))
    R.gate(fires,
           "the repaired predicate does NOT fire on the kernel bend "
           "(%s/%s/%s) -- there is no difference to confirm"
           % (new[0], new[1], new[2]))
    R.gate((old[0], old[1], old[2]) != (new[0], new[1], new[2]),
           "the two columns print THE SAME triple (%s/%s/%s) on the kernel "
           "bend -- the confirmation is a zero and not a difference"
           % (old[0], old[1], old[2]))
    R.gate((new[0], new[1], new[2]) == (1, 1, 3),
           "the repaired column prints %s/%s/%s on the kernel bend where the "
           "repair's own transcript prints 1/1/3"
           % (new[0], new[1], new[2]))

    # ---------------------------------------------------------------------
    L.rule("(iv) AND THE SAME BEND UNDER THE DRIFTED ANCHOR, RUN")
    # ---------------------------------------------------------------------
    dold = results["before the repair (DRIFTED)"]
    dnew = results["the repair (DRIFTED)"]
    print("""   The two revisions the OLD anchor picks, run against the SAME
   committed kernel bend.  Not argued from the source -- run.

     drifted `before the repair` %s : exit %s / self %s / find %s
     drifted `the repair`        %s : exit %s / self %s / find %s
""" % (DRIFT_PRE[:8], dold[0], dold[1], dold[2],
       DRIFT_REPAIR[:8], dnew[0], dnew[1], dnew[2]))
    vac = (dold[0], dold[1], dold[2]) == (dnew[0], dnew[1], dnew[2])
    print("""     the two drifted columns print %s

   THAT IS THE VACUITY, MEASURED.  Both sides carry the kernel half,
   so both FIRE, and the comparison `is the new one ever silent where
   the old one fires?` answers 0 -- a plausible number produced by
   asking a question of one predicate twice.  The repaired pair
   answers the same question with a genuine 0, and the two zeros are
   not the same zero: one is a fact about coverage and the other is a
   fact about the anchor.
""" % ("THE SAME TRIPLE -- one predicate asked twice"
       if vac else "DIFFERENT triples"))
    R.selfgate(vac,
               "the two drifted columns print different triples, so this "
               "tree does not exhibit the vacuity the parent finding names; "
               "the demonstration in (iv) is not available here")

    print("""   AND ONE STEP FURTHER THAN THE PARENT STATES IT.  The drifted
   `this repair` column resolves to %s, and g1_provenance.py there is
   %s to g1_provenance.py at HEAD.  So the drifted comparison was not
   only a predicate against itself -- on one side it was THE VERY FILE
   the run was measuring, under a label reading `the repair`.  The
   parent's report says the two sides became `mg-76cc's ALREADY-
   REPAIRED predicate`; the byte identity is the sharper form of the
   same statement and is measured here rather than inferred.
""" % (DRIFT_REPAIR[:8],
       "BYTE-IDENTICAL" if L.show_or_empty(DRIFT_REPAIR, L.G1_REL)
       == L.show_or_empty("HEAD", L.G1_REL) else "not identical"))
finally:
    L.rm_tree(tree)

# ---------------------------------------------------------------------------
L.rule("(v) k1_prerepair.py, RE-RUN -- SOMETHING INDEPENDENT TO AGREE WITH")
# ---------------------------------------------------------------------------

print("""   (iii) is worth nothing if it is the only measurement of itself.
   k1 is re-run here, unmodified, in a clone at HEAD, and its
   kernel-bend row is read out of its own output and put beside the
   triples above.
""")

tree2 = L.clone_at("HEAD")
try:
    rc_k1, out_k1 = L.run_py("k1_prerepair.py",
                             os.path.join(tree2, L.E34A_DIR), timeout=3600)
    print("   k1_prerepair.py, re-run : exit %d" % rc_k1)
    row = None
    for ln in out_k1.splitlines():
        if "dim L(n,p) one too big" in ln and "YES" in ln:
            row = ln
    if row:
        print("   its kernel-bend row, verbatim:")
        print("     %s" % row.strip())
        nums = [t for t in row.split() if t.isdigit()]
        # before mg-7e58 (3) | BEFORE REPAIR (3) | this repair (3)
        R.selfgate(len(nums) >= 9,
                   "k1's kernel-bend row does not carry 9 numbers: %r"
                   % row.strip())
        if len(nums) >= 9:
            pre = tuple(int(x) for x in nums[3:6])
            now = tuple(int(x) for x in nums[6:9])
            print("\n     k1 says   BEFORE REPAIR : %s/%s/%s" % pre)
            print("     k1 says   this repair   : %s/%s/%s" % now)
            print("     s3 (iii) says           : %s/%s/%s  and  %s/%s/%s"
                  % (old[0], old[1], old[2], new[0], new[1], new[2]))
            R.gate(pre == (old[0], old[1], old[2]),
                   "k1's `BEFORE REPAIR` kernel-bend cell is %s/%s/%s and "
                   "this script's independent re-derivation is %s/%s/%s"
                   % (pre + (old[0], old[1], old[2])))
            R.gate(now == (new[0], new[1], new[2]),
                   "k1's `this repair` kernel-bend cell is %s/%s/%s and this "
                   "script's independent re-derivation is %s/%s/%s"
                   % (now + (new[0], new[1], new[2])))
    else:
        R.selferr("k1's kernel-bend row was not found in its output; a row "
                  "this script could not locate is a fact about this script "
                  "and is never scored as agreement")

    ts, tf, tl = trailer(out_k1)
    print("\n   k1's own trailer on this run : SELF-ERRORS %s, FINDINGS %s "
          "(%d listed), exit %d" % (ts, tf, tl, rc_k1))
    R.selfgate(tf is None or tf == tl,
               "k1's trailer says FINDINGS %s and lists %d" % (tf, tl))
    committed = L.read_worktree(L.E34A_DIR + "/out_k1_prerepair.txt")
    cs, cf, cl = trailer(committed)
    print("   its COMMITTED transcript says: SELF-ERRORS %s, FINDINGS %s "
          "(%d listed)" % (cs, cf, cl))
    R.gate((ts, tf) == (cs, cf),
           "k1 re-run prints SELF-ERRORS %s / FINDINGS %s where its own "
           "committed transcript prints %s / %s -- the record and the tree "
           "disagree" % (ts, tf, cs, cf))
finally:
    L.rm_tree(tree2)

R.done()
