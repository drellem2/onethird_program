"""k4_cancel.py -- THE FLOOR: one thing no list in this ticket names.

WHAT I CHOSE, AND WHY

mg-76cc added a third row to g1's section (v) -- `both together` -- and gave
it a reason.  The reason is printed in g1's own output, written in g1's
docstring, written in the commit message of the repair and written in the
document the repair ships:

    "then both are moved together, because two changes that cancel would
     pass each half on its own."

A rationale is a claim.  This one names a specific input -- a pair of changes
that cancel -- and states what that input does to the two half rows.  Nothing
in mg-76cc ever built one.  So it is built here, and the sentence is scored
against it.

  kern_a218.py's dim L(n,p) one too BIG, c1_branching.py's vertex dims one
  too SMALL.  Each file's own measurement moves; the two together restore the
  printed measurement exactly.

That input is also why k1 books its finding, and this is where the finding is
demonstrated rather than asserted.

AND A SECOND, CHEAPER THING NOBODY READS: mg-76cc's own PREDICTIONS.md.  It
is prose that nothing executes, which is exactly the shape of a claim that
drifts from what its transcripts say.  Every predicted exit code in it is
scored against the committed transcript of the script it names.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import sys

import libe34a as L

R = L.Report(
    selfpop="every git read, c1 run and source read this script performs, "
            "plus the requirement that each bend really change the file it "
            "names and that the sentence under test really be in the tree",
    findpop="the 3 half-rows of section (v) evaluated on a cancelling pair, "
            "the rationale sentence scored against them wherever it is "
            "written, and every predicted exit code in mg-76cc's "
            "PREDICTIONS.md against the transcript it names")

L.banner("K4", "THE CANCELLING PAIR -- THE INPUT THE RATIONALE NAMES")
print("""
The floor says: audit at least one thing no list here names, and say what was
chosen.  Chosen: the sentence mg-76cc uses to justify the row it added.
""")

# ---------------------------------------------------------------------------
L.rule("(i) THE SENTENCE, ENUMERATED FROM THE TREE RATHER THAN QUOTED")
print("""   A claim written in four places is four claims.  Every copy is
   found with `git grep`, so a copy this script did not remember is
   still in the population.""")
print()
CLAIM = "changes that cancel would pass"          # the claim under test
MENTION = "a cancelling pair cannot pass"         # a DIFFERENT claim, not this


def grep(needle):
    out = L.git("grep", "-n", "-F", needle, "HEAD")
    got = []
    for line in out.splitlines():
        if not line.strip():
            continue
        _, _, rest = line.partition(":")
        path, _, tail = rest.partition(":")
        got.append((path, tail.split(":", 1)[0]))
    return got


claims = grep(CLAIM)
msg = L.git("log", "-1", "--format=%B", L.REPAIR_REV)
in_msg = "cancelling pair would pass each half" in msg
print("   THE CLAIM -- `%s ...`:" % CLAIM)
for path, lineno in claims:
    print("     %-52s line %s" % (path, lineno))
print("   in the COMMIT MESSAGE of %s : %s"
      % (L.REPAIR_REV[:8], "yes" if in_msg else "no"))
print()
total_copies = len(claims) + (1 if in_msg else 0)
print("   %d place(s) in the tree, plus the commit message : %d in all"
      % (len(claims), total_copies))
print()
print("   AND WHAT IS NOT SCORED, named so that a reader can see the line")
print("   was drawn on purpose -- `%s`:" % MENTION)
for path, lineno in grep(MENTION):
    print("     %-52s line %s" % (path, lineno))
print("   That is a DIFFERENT sentence and it is TRUE: a cancelling pair")
print("   cannot get through section (v), because the two halves catch it.")
print("   Only the sentence about which ROW catches it is under test.")
print()
R.check(total_copies > 0,
        "the sentence under test is not in the tree or the commit message; "
        "there is nothing to score and every row below is withdrawn")
print()

# ---------------------------------------------------------------------------
L.rule("(ii) THE CANCELLING PAIR, BUILT")
print("""   Both bends refuse on zero occurrences and on many, so a bend that
   silently did nothing cannot make the rows below say whatever they
   like.  And the pair is shown to really cancel BEFORE it is used.""")
print()
old_c1 = L.git_show(L.REV_A218, L.C1_REL)
old_k = L.git_show(L.REV_A218, L.KERN_REL)
head_c1 = L.git_show("HEAD", L.C1_REL)
head_k = L.git_show("HEAD", L.KERN_REL)
target = L.git_show("HEAD", L.TARGET_REL)

try:
    bent_c1 = L.bend_c1_down(head_c1)
    bent_k = L.bend_kern_up(head_k)
except ValueError as e:
    R.selferr("the cancelling pair could not be built (%s); sections (ii) and "
              "(iii) are DROPPED rather than counted as passing" % e)
    bent_c1 = bent_k = None

if bent_c1 is not None:
    print("   c1_branching.py : vertex dims one too SMALL  (%d byte(s) "
          "changed)" % abs(len(bent_c1) - len(head_c1)))
    print("   kern_a218.py    : dim L(n,p) one too BIG     (%d byte(s) "
          "changed)" % abs(len(bent_k) - len(head_k)))
    print()

    def measure(c1s, ks):
        out, rc = L.run_c1(target, c1s, ks)
        m = L.measuring_half(out)
        v = L.vertex_cells(out)
        return L.sha(m)[:16], v, len(m.splitlines())

    ref_sha, ref_v, ref_lines = measure(old_c1, old_k)
    R.check(len(ref_v) == 24,
            "the baseline run produced %d vertex cells, not the 24 c1 prints; "
            "the comparison below is against a parse and not a measurement"
            % len(ref_v))
    print("   the baseline -- c1 and its kernel both at %s : sha %s, %d lines"
          % (L.REV_A218[:8], ref_sha, ref_lines))
    print()

    # ---------------------------------------------------------------------
    L.rule("(iii) SECTION (v)'S THREE HALVES, ON THAT PAIR")
    print("""   The same three (script, kernel) pairs g1's HALVES uses, with
   HEAD carrying the cancelling pair.  Each is diffed against the
   baseline exactly as g1 diffs it: sections (i)+(ii) byte for byte,
   and c1's own 24 vertex sets parsed back out of them.""")
    print()
    HALVES = [("c1_branching.py", "the script", bent_c1, old_k),
              ("kern_a218.py", "its kernel", old_c1, bent_k),
              ("both together", "cancellation", bent_c1, bent_k)]
    print("     half moved to HEAD              baseline         moved"
          "            verdict")
    verdict = {}
    for hname, hwhat, c1s, ks in HALVES:
        s, v, _ = measure(c1s, ks)
        same = (s == ref_sha and v == ref_v and len(v) == 24)
        verdict[hname] = same
        print("     %-30s %-16s %-16s %s"
              % (hname + " (%s)" % hwhat, ref_sha, s,
                 "IDENTICAL" if same else "MOVED"))
    print()
    print("""   THE ROW NAMED `cancellation` IS THE ONE ROW A CANCELLING PAIR
   PASSES.  The two halves it was added to backstop are the two that
   catch it.""")
    print()
    rationale_holds = (verdict.get("c1_branching.py") and
                       verdict.get("kern_a218.py") and
                       not verdict.get("both together"))
    print("     the sentence says the halves PASS and the together row is")
    print("     what notices    : halves %s / together %s"
          % ("pass" if verdict.get("c1_branching.py") and
             verdict.get("kern_a218.py") else "FIRE",
             "fires" if not verdict.get("both together") else "PASSES"))
    print("     measured        : c1 half %s, kern half %s, both together %s"
          % ("IDENTICAL" if verdict.get("c1_branching.py") else "MOVED",
             "IDENTICAL" if verdict.get("kern_a218.py") else "MOVED",
             "IDENTICAL" if verdict.get("both together") else "MOVED"))
    print("     the sentence holds : %s" % ("yes" if rationale_holds else "NO"))
    R.gate(rationale_holds,
           "the rationale mg-76cc gives for the `both together` row is "
           "INVERTED, in %d place(s) -- g1's docstring, g1's printed text, "
           "the repair's document and the commit message of %s.  A pair of "
           "changes that cancel MOVES both half rows and leaves `both "
           "together` IDENTICAL: the row named `cancellation` is the only one "
           "of the three that a cancelling pair passes, and the two halves it "
           "was added to backstop are the two that catch it.  Measured above "
           "on a pair built for the purpose, not argued"
           % (total_copies, L.REPAIR_REV[:8]))
    print()
    print("""   WHAT THE ROW IS ACTUALLY FOR, since the finding is against the
   sentence and not against the row: a CONSPIRING pair -- each file's
   change harmless on its own, the two together moving the measurement
   -- is caught by `both together` and by neither half.  The row is
   load-bearing.  Its reason is backwards.""")
    print()
    print("""   AND WHAT THE HALVES COST.  On this input g1 books a finding per
   moved half, each saying the 198 cells "have to be re-taken", while
   its own `both together` row -- the only one that asks what the tree
   as it stands actually measures -- prints IDENTICAL on the same run.
   That is the grain error mg-7e58 was repairing, relocated from the
   FILE to a half-moved tree that exists nowhere.  k1 (v) books it.""")
    print()
    print("   population: the %d half rows of section (v), each evaluated on "
          "the one" % len(HALVES))
    print("   cancelling pair built in (ii), against the same baseline g1 "
          "uses.")
    print()

# ---------------------------------------------------------------------------
L.rule("(iv) mg-76cc's OWN PREDICTIONS.md, WHICH NOTHING READS")
print("""   A prediction file is prose.  Its `Exit codes` table is read here --
   the ROWS, not a list written in this script -- and both of its
   columns are scored against the committed transcript of the script
   each row names.  TOTAL BAD 0 means that script exited 0.

   The `actual` column matters as much as the `predicted` one: an
   `actual` that disagrees with the transcript is a record of a run
   that did not happen the way it is written down.""")
print()
pred = L.read_worktree(L.R76CC_DIR + "/PREDICTIONS.md")
ROWS = []
for line in pred.splitlines():
    s = line.strip()
    if not s.startswith("|") or s.count("|") < 3:
        continue
    cols = [c.strip() for c in s.strip("|").split("|")]
    if len(cols) != 3:
        continue
    name = cols[0].strip("`").strip()
    if not name.endswith(".py"):
        continue
    said = L._leading_int(cols[1].replace("*", ""))
    actual = L._leading_int(cols[2].replace("*", ""))
    if said is None or actual is None:
        continue
    ROWS.append((name, said, actual))
R.check(bool(ROWS),
        "no exit-code rows could be read out of mg-76cc's PREDICTIONS.md; "
        "(iv) is about nothing and is withdrawn")
print("     script                predicted  written    transcript  agrees")
for name, said, written in ROWS:
    stem = name.rsplit(".", 1)[0]
    tpath = L.R76CC_DIR + "/out_%s.txt" % stem
    try:
        text = L.read_worktree(tpath)
    except IOError:
        R.selferr("PREDICTIONS.md has a row for %s and there is no committed "
                  "%s; the row is DROPPED rather than scored" % (name, tpath))
        continue
    tb = None
    for line in text.splitlines():
        if line.startswith("TOTAL BAD:"):
            tb = L._leading_int(line.split(":", 1)[1])
    if tb is None:
        R.selferr("%s prints no TOTAL BAD line, so its exit code cannot be "
                  "read off it; the row is DROPPED rather than scored" % tpath)
        continue
    from_tx = 0 if tb == 0 else 1
    ok = (written == from_tx)
    print("     %-21s %-10s %-10s %-11s %s"
          % (name, said, written, "exit %d (TOTAL BAD %d)" % (from_tx, tb),
             "yes" if ok else "NO"))
    R.gate(ok, "mg-76cc's PREDICTIONS.md records `actual` exit %s for %s and "
               "its own committed transcript reports TOTAL BAD %s, i.e. exit "
               "%s" % (written, name, tb, from_tx))
print()
print("   population: the %d `.py` rows of PREDICTIONS.md's own exit-code"
      % len(ROWS))
print("   table -- read from the table, not listed here -- each against the")
print("   committed out_<script>.txt in the same directory.  The `run_all.sh")
print("   (worst)` row is excluded BY NAME: it has no transcript of its own.")
print()

# ---------------------------------------------------------------------------
L.rule("(v) mg-76cc'S OWN FINDING READER, RUN UNMODIFIED ON A COMMITTED FILE")
print("""   Found by accident and kept, because a reader is a population and
   this arc has already paid for two populations inflated by prose.

   lib76cc.findings_of() takes every line containing the substring
   `   FINDING: ` as one of the script's own findings.  A transcript
   that QUOTES another script's finding at a deeper indentation
   contains that substring too.  So the reader is run here UNMODIFIED,
   against a file committed at HEAD, beside the count that file's own
   trailer prints.""")
print()
LIB76 = L.REPO + "/" + L.R76CC_DIR + "/lib76cc.py"
their = None
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("lib76cc_asis", LIB76)
    their = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(their)
except Exception as e:                                   # noqa: BLE001
    R.selferr("mg-76cc's lib76cc.py could not be loaded (%s); (v) is DROPPED "
              "rather than counted as passing" % e)

if their is not None:
    print("     file                        trailer says  their reader  mine")
    disagree = []
    for rel in [L.S58DA_DIR + "/out_g4_fleet.txt",
                L.S58DA_DIR + "/out_g1_provenance.txt",
                L.S58DA_DIR + "/out_g3_findings.txt",
                L.R76CC_DIR + "/out_r1_kernel.txt",
                L.R76CC_DIR + "/out_r3_prerepair.txt"]:
        text = L.git_show("HEAD", rel)
        _, said = L.trailer(text)
        theirs = len(their.findings_of(text))
        mine = len(L.findings(text))
        print("     %-27s %-13s %-13s %s"
              % (rel.split("/")[-1], said, theirs, mine))
        if said is not None and theirs != said:
            disagree.append((rel.split("/")[-1], said, theirs))
    print()
    print("   files where their reader's count differs from the trailer the")
    print("   file itself prints : %d of 5" % len(disagree))
    for name, said, theirs in disagree:
        print("      %s -- trailer %d, reader %d" % (name, said, theirs))
    R.gate(not disagree,
           "mg-76cc's own findings_of() over-counts on %d of the 5 committed "
           "transcripts read here (%s): it matches the substring "
           "`   FINDING: `, so a finding QUOTED from a nested run at deeper "
           "indentation is counted as the outer script's own.  r3 uses this "
           "reader for its `names kern_a218.py` column, which is the column "
           "the whole OPEN 1 verdict turns on -- it happens not to bite there "
           "because g1 quotes no nested transcript, so this is a live defect "
           "with no live consequence rather than a wrong answer"
           % (len(disagree),
              "; ".join("%s trailer %d vs reader %d" % d for d in disagree)))
    print()
    print("   population: the 5 committed transcripts above -- 3 from")
    print("   code/branching_audit_58da/ and 2 from")
    print("   code/branching_repair_76cc/ -- each read by mg-76cc's reader")
    print("   unmodified and by this one, against the count the file itself")
    print("   prints.  Demonstrated at HEAD, where the defect is present.")
    print()

# ---------------------------------------------------------------------------
L.rule("VERDICT")
print("""   THE CHOSEN THING: the rationale mg-76cc gives for the row it added.

   It is checkable because it names an input, and the input can be
   built.  Built, it says the opposite of the sentence: a cancelling
   pair MOVES both half rows and leaves `both together` IDENTICAL.

   The row survives the finding; the sentence does not.  And the two
   findings the halves book on that input assert that 198 cells must be
   re-taken while the row that measures the tree as it stands says they
   need not be.
""")

sys.exit(R.emit())
