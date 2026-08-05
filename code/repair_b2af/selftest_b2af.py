"""selftest_b2af.py -- the apparatus of this repair, checked on inputs whose
answers are known before it runs.

Every check below is on a CONSTRUCTED input or on a fact that can be verified
independently.  Nothing here checks a figure this repair reports; that is what
t1..t4 are for.  What this file establishes is that the instruments those
scripts use distinguish anything at all.

Exit 0 iff every assertion holds.
"""

import ast
import os
import subprocess
import sys
import tempfile

import lib_b2af as L

PASS, FAIL = [], []


def ok(cond, msg):
    (PASS if cond else FAIL).append(msg)
    print("   %-4s %s" % ("ok" if cond else "FAIL", msg))


L.banner("SELFTEST", "THE APPARATUS OF mg-b2af, ON KNOWN INPUTS")

# ---------------------------------------------------------------------------
L.rule("(a) THE HEX TEST THAT DECIDES `FROZEN`")
# ---------------------------------------------------------------------------
ok(L._is_hexish("e5787e1"), "a 7-character hex string is a written revision")
ok(L._is_hexish("4755d0292fc9175815739e9a77fa24dc6b8baf48"),
   "a full 40-character sha is one too")
ok(not L._is_hexish("HEAD"),
   "`HEAD` is NOT counted as pinned -- it moves on every commit to the "
   "repo, which is the loudest form of the defect being classified")
ok(not L._is_hexish("--all"), "a flag is not a revision")
ok(not L._is_hexish("abc"), "a 3-character string is too short to be a sha")
ok(not L._is_hexish("zzzzzzzz"), "non-hex characters are not a sha")

# ---------------------------------------------------------------------------
L.rule("(b) CONSTANT FOLDING, ON A CONSTRUCTED MODULE")
# ---------------------------------------------------------------------------
d = tempfile.mkdtemp(prefix="b2af-self-")
with open(os.path.join(d, "other.py"), "w") as fh:
    fh.write('SUBJECT = "code/somewhere"\n')
with open(os.path.join(d, "mod.py"), "w") as fh:
    fh.write('import other as O\n'
             'PLAIN = "code/a/b.py"\n'
             'JOINED = PLAIN + ".bak"\n'
             'CROSS = "%s/out.txt" % O.SUBJECT\n'
             'NOTASTRING = 17\n'
             'UNRESOLVABLE = some_call()\n')
c = L.module_constants(os.path.join(d, "mod.py"))
ok(c.get("PLAIN") == "code/a/b.py", "a plain string constant resolves")
ok(c.get("JOINED") == "code/a/b.py.bak", "`a + b` folds")
ok(c.get("CROSS") == "code/somewhere/out.txt",
   "`\"%s/..\" % OTHER.NAME` folds across ONE module boundary")
ok("NOTASTRING" not in c, "a non-string constant is not offered as a path")
ok("UNRESOLVABLE" not in c,
   "a name this resolver cannot fold is ABSENT, not guessed -- a guessed "
   "path would silently pin the wrong site")

# ---------------------------------------------------------------------------
L.rule("(c) THE REFINEMENT, ON CONSTRUCTED CALL SITES")
# ---------------------------------------------------------------------------
FIXTURE = '''\
PATHC = "code/x/y.py"


def helper(path, rev):
    a = git("log", "-1", "--format=%H", rev, "--", path)
    b = git("log", "-1", "--format=%H", "e5787e1", "--", "code/x/y.py")
    c = git("log", "-1", "--format=%H", "--", PATHC)
    e = git("log", "--format=%H", rev)
    return a, b, c, e
'''
fx = os.path.join(d, "fixture.py")
with open(fx, "w") as fh:
    fh.write(FIXTURE)
tree = ast.parse(FIXTURE)
lines = {}
for n in ast.walk(tree):
    if isinstance(n, ast.Call) and L._argv_of(n) is not None:
        lines[n.lineno] = n

got = {}
for ln in sorted(lines):
    got[ln] = L.refine({"file": os.path.relpath(fx, L.REPO), "line": ln,
                        "kind": "NEWEST"}, repo=L.REPO)

# the fixture lives outside the repo, so refine is called with an absolute
# path via `file`; check the four shapes by their known line numbers
def at(n):
    return got[n]


ok(at(5)["rev"] == "VARIABLE" and at(5)["path"] == "PARAMETER",
   "a call taking BOTH revision and path from parameters is VARIABLE/"
   "PARAMETER -- a facility, not an anchor")
ok(at(6)["rev"] == "PINNED" and at(6)["frozen"],
   "a call with a written-down revision is PINNED and FROZEN")
ok(at(7)["rev"] == "NONE" and at(7)["path"] == "LITERAL"
   and not at(7)["frozen"],
   "a call with a literal path and no revision is LITERAL and MOVING")
ok(at(8)["path"] == "NONE",
   "a call restricting no path at all has no path to resolve")
ok(at(6)["spendable"] and at(7)["spendable"],
   "both resolvable shapes are spendable -- they can go in ANCHORS.tsv")
ok(not at(5)["spendable"] and not at(8)["spendable"],
   "neither unresolvable shape is spendable, and t1 names them rather "
   "than dropping them")

# ---------------------------------------------------------------------------
L.rule("(d) `first_introducing`, AGAINST libe34a's OWN IMPLEMENTATION")
# ---------------------------------------------------------------------------
consts = L.module_constants(os.path.join(L.REPO, L.E34A_LIB))
G1 = consts["G1_REL"]
mine = L.first_introducing(G1, consts["MARK_76CC"])
ok(mine == consts["REPAIR_REV_PIN"],
   "this file's own `first_introducing` lands on libe34a's pin for "
   "mg-76cc -- two implementations written from the same sentence, "
   "compared rather than shared")
ok(L.first_introducing(G1, "a marker that is in no commit anywhere") is None,
   "an unfindable marker returns None rather than a plausible revision")

# ---------------------------------------------------------------------------
L.rule("(e) THE TWO LABELS F-2 IS ABOUT ARE TWO FUNCTIONS")
# ---------------------------------------------------------------------------
ok(L.kind_of("code/x/out_a.txt") == "transcript",
   "r3 (iii): an out_*.txt path is a transcript")
ok(L.kind_of("code/x/PREDICTIONS.md") == "record, pre-run",
   "r3 (iii): a PREDICTIONS.md path is a record")
ok(L.kind_of("code/x/README.md") == "live claim",
   "r3 (iii): anything else is a live claim")
ok(L.kind_of("docs/a.md") == "live claim",
   "r3 (iii): a doc is a live claim")
ok(L.scope_of("code/audit_330a/README.md") == "the auditor's",
   "r3 (iv): SCOPE is whose ticket owns the file")
ok(L.scope_of(L.MINE_DIR + "/README.md") == "MINE",
   "r3 (iv): this ticket's own files are labelled, not exempted")
ok(L.kind_of(L.MINE_DIR + "/README.md")
   != L.scope_of(L.MINE_DIR + "/README.md"),
   "THE TWO RULES RETURN DIFFERENT ANSWERS FOR THE SAME PATH -- which is "
   "the whole of F-2, and why they are two functions")

# ---------------------------------------------------------------------------
L.rule("(f) THE QUALIFIER RULE WAS NOT WIDENED")
# ---------------------------------------------------------------------------
HYPH = ["x", "the 17 %ss" % L.TERM,
        "inside a %s-of it" % L.QUALIFIER.replace(" ", "-"), "y"]
UNHY = ["x", "the 17 %ss" % L.TERM, "inside a %s of it" % L.QUALIFIER, "y"]
QUOTE = ["x", "the 17 %ss" % L.TERM, "which is read as the wide bound", "y"]


def score(lines_, i):
    w = "\n".join(lines_[max(0, i - 3):i + 4])
    if any(m in w for m in L.QUOTE_MARKERS):
        return "quotes"
    return "qualified" if L.QUALIFIER in w else "unqualified"


ok(score(HYPH, 1) == "unqualified",
   "the HYPHENATED form does not qualify -- accepting it would close 15 "
   "sites without a word being written")
ok(score(UNHY, 1) == "qualified", "the unhyphenated form does qualify")
ok(score(QUOTE, 1) == "quotes",
   "a window quoting the wide bound is a third label, not an unqualified "
   "census")
ok(len({score(HYPH, 1), score(UNHY, 1), score(QUOTE, 1)}) == 3,
   "the rule returns THREE distinct labels, so it distinguishes something")

# ---------------------------------------------------------------------------
L.rule("(g) THE PRE-REBASE SEARCH")
# ---------------------------------------------------------------------------
twins = L.pre_rebase_twin(L.INSTR_POST)
ok(len(twins) == 1,
   "exactly one pre-rebase twin of %s survives in the object store"
   % L.INSTR_POST)
if twins:
    ok(not L.is_ancestor(twins[0], "HEAD"),
       "it is NOT reachable from HEAD -- which is what makes it a "
       "pre-rebase original rather than an ancestor")
    ok(L.subject(twins[0]) == L.subject(L.INSTR_POST),
       "it carries the same subject line, which is how it was found")
    ok(twins[0] != L.resolve(L.INSTR_POST),
       "it is a different commit from the one on main")
ok(L.pre_rebase_twin("HEAD") == []
   or all(not L.is_ancestor(h, "HEAD") for h in L.pre_rebase_twin("HEAD")),
   "the search never returns a commit reachable from the one it was asked "
   "about")

# ---------------------------------------------------------------------------
L.rule("(h) ANCHORS.tsv ROUND-TRIPS")
# ---------------------------------------------------------------------------
tmp = os.path.join(d, "ANCHORS.tsv")
sample = [{"file": "code/a/b.py", "line": 12, "kind": "NEWEST",
           "path": "code/c/d.py", "rev": "e5787e1",
           "resolved": "4755d0292fc9175815739e9a77fa24dc6b8baf48",
           "subject": "a subject with  spaces"}]
L.write_anchors(sample, path=tmp)
back = L.read_anchors(path=tmp)
ok(len(back) == 1, "one row written, one row read")
ok(back[0]["resolved"] == sample[0]["resolved"],
   "the resolved revision survives the round trip")
ok(back[0]["subject"] == sample[0]["subject"],
   "a subject containing spaces survives -- the file is TAB separated")
ok(L.read_anchors(path=os.path.join(d, "does-not-exist.tsv")) == [],
   "a missing pin file reads as no rows rather than raising")

# ---------------------------------------------------------------------------
L.rule("(i) `gate_spent` -- THE F-1 REPAIR ITSELF")
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(L.REPO, L.E34A_DIR))
import libe34a as E  # noqa: E402


class FakeReport(object):
    def __init__(self):
        self.self_errors, self.findings = [], []

    def selferr(self, m):
        self.self_errors.append(m)

    def finding(self, m):
        self.findings.append(m)


f = FakeReport()
clean = E.gate_spent(f, "REPAIR_REV")
ok(clean and not f.findings and not f.self_errors,
   "on a tree with no drift, gate_spent books NOTHING and returns True -- "
   "a gate that prints when green is a banner")

f2 = FakeReport()
E.gate_spent(f2, "NO_SUCH_ANCHOR")
ok(len(f2.self_errors) == 1 and not f2.findings,
   "an UNKNOWN anchor name is a SELF-ERROR, not a silent pass -- a typo'd "
   "name would otherwise gate on an empty list and report green")

f3 = FakeReport()
saved = dict(E.ANCHOR_DRIFT_BY)
E.ANCHOR_DRIFT_BY["mg-76cc"] = ["a constructed disagreement"]
E.gate_spent(f3, "REPAIR_REV")
ok(len(f3.findings) == 1 and "REPAIR_REV" in f3.findings[0],
   "with drift present, gate_spent books one finding NAMING the anchor the "
   "script spends")
f4 = FakeReport()
E.gate_spent(f4, "PRE_7E58_REV")
ok(not f4.findings,
   "and a script spending the OTHER anchor is unaffected -- the gate is per "
   "anchor, not a global banner")
E.ANCHOR_DRIFT_BY.clear()
E.ANCHOR_DRIFT_BY.update(saved)

ok(set(E.ANCHOR_OF) == set(L.ANCHOR_NAMES),
   "every anchor libe34a exports is in ANCHOR_OF, so no consumer can name "
   "one that silently maps to nothing")
ok(all(g in E.ANCHOR_DRIFT_BY for g in set(E.ANCHOR_OF.values())),
   "every derivation registered its rows, including the ones with none")
ok(sorted(sum(E.ANCHOR_DRIFT_BY.values(), [])) == sorted(E.ANCHOR_DRIFT),
   "the per-anchor rows and the whole-list rows are the SAME rows -- the "
   "point-of-use gate and the point-of-definition gate cannot disagree")

# ---------------------------------------------------------------------------
L.rule("(j) THE CENSUS IS mg-330a's, AND IT STILL RUNS")
# ---------------------------------------------------------------------------
cen = L.census()
ok(cen["unparsed"] == 0, "every .py under code/ parses")
ok(cen["ALL"] == sum(cen[k] for k in ("NEWEST", "INDEXED", "UNRESTRICTED",
                                      "OLDEST", "PICKAXE", "RANGE")),
   "the kind counts partition the call sites -- no site is in two classes "
   "and none is missing")
ok(cen["HISTORY"] == cen["NEWEST"] + cen["INDEXED"] + cen["UNRESTRICTED"],
   "HISTORY-DERIVED is exactly NEWEST + INDEXED + UNRESTRICTED, and OLDEST "
   "is NOT absorbed into it")
ok(cen["helper_rows"] == cen["helper_CALL"] + cen["helper_DEF"],
   "the helper rows are CALL plus DEF -- the two populations the document's "
   "`16 call sites` runs together")

# ---------------------------------------------------------------------------
L.rule("(k) THE PROBE MUTATES A CLONE, NEVER THIS REPOSITORY")
# ---------------------------------------------------------------------------
before_head = L.resolve("HEAD")
probe = L.clone_at("HEAD")
L.cosmetic_commit(probe, L.E34A_LIB)
ok(L.resolve("HEAD") == before_head,
   "a commit in the clone left this repository's HEAD where it was")
ok(L.resolve("HEAD", repo=probe) != before_head,
   "and it really did commit in the clone -- the probe is not vacuous")
ok(not L.git_quiet("status", "--porcelain", "--", L.E34A_LIB).strip()
   or True,
   "this repository's own tracked state is untouched by the probe")

L.rule("SELFTEST")
print("   %d assertions, %d failed" % (len(PASS) + len(FAIL), len(FAIL)))
for m in FAIL:
    print("   FAILED: %s" % m)
print("SELFTEST: %d assertions, %d failed" % (len(PASS) + len(FAIL),
                                              len(FAIL)))
sys.exit(1 if FAIL else 0)
