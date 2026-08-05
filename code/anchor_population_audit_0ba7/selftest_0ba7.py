#!/usr/bin/env python3
"""selftest_0ba7.py -- assertions on CONSTRUCTED inputs, not on the repo.

Every check here is over an input written in this file.  A self-test that
asserts about the repository asserts about the subject, and a subject that
changes turns the instrument red for a reason that is not the instrument's.

The two that matter most:

  * `kind_of` and mg-330a's `classify_call` are run over the SAME
    constructed call.  The difference a1 reports over 59 repository sites is
    demonstrated here on one line of Python, so that `mine sees 15 more` is
    a property of the two rules rather than a property of this tree.
  * `gate_spent` is asked about a name it does not know, and the SELF-ERROR
    path is confirmed to be a self-error rather than a pass.

Predicted exit: 0.
"""
import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_0ba7 as L                                          # noqa: E402
sys.path.insert(0, os.path.join(L.REPO, "code", "audit_330a"))
import warnings                                               # noqa: E402
warnings.filterwarnings("ignore", category=SyntaxWarning)
from lib330a import classify_call                             # noqa: E402

OK = [0]
BAD = []


def ok(cond, msg):
    OK[0] += 1
    print("   %-5s %s" % ("ok" if cond else "FAIL", msg))
    if not cond:
        BAD.append(msg)


L.banner("mg-0ba7 selftest", "ASSERTIONS ON CONSTRUCTED INPUTS")

# ---------------------------------------------------------------------------
L.rule("(1) THE TAXONOMY, ONE CONSTRUCTED CALL PER CLASS")
# ---------------------------------------------------------------------------
CASES = [
    (["log", "-1", "--format=%H", "--", "a.py"], "NEWEST"),
    (["log", "-1", "--format=%H"], "NEWEST-norestrict"),
    (["log", "--format=%H", "--", "a.py"], "INDEXED"),
    (["log", "--format=%H"], "UNRESTRICTED"),
    (["log", "--reverse", "--format=%H", "--", "a.py"], "OLDEST"),
    (["log", "-S", "marker", "--format=%H", "--", "a.py"], "PICKAXE"),
    (["log", "-G", "re", "--format=%H", "--", "a.py"], "PICKAXE"),
    (["log", "--format=%H", "a..b", "--", "a.py"], "RANGE"),
]
for strs, want in CASES:
    ok(L.kind_of(strs) == want,
       "kind_of(%s) == %s (got %s)" % (strs, want, L.kind_of(strs)))

ok(L.kind_of(["show", "--format=%H"]) is None,
   "a call with no `log` argument produces no revision row")
ok(L.kind_of(["log", "--oneline"]) is None,
   "a `log` with no hash format produces no revision row")
ok(L.kind_of(["mylog", "-1", "--format=%H", "--", "a.py"]) == "NEWEST",
   "a helper named `mylog` is matched by the endswith rule, as mg-330a's is")

# ---------------------------------------------------------------------------
L.rule("(2) THE ONE LETTER, DEMONSTRATED ON A CONSTRUCTED CALL")
# ---------------------------------------------------------------------------
CAP = ["log", "-1", "--format=%H", "--", "a.py"]
LOW = ["log", "-1", "--format=%h", "--", "a.py"]
ok(classify_call(CAP) == "NEWEST",
   "mg-330a's classifier sees the CAPITAL form and calls it NEWEST")
ok(classify_call(LOW) is None,
   "mg-330a's classifier does NOT see the LOWERCASE form at all (got "
   + repr(classify_call(LOW)) + ")")
ok(L.kind_of(CAP) == "NEWEST", "mine sees the capital form as NEWEST")
ok(L.kind_of(LOW) == "NEWEST", "mine sees the lowercase form as NEWEST too")
ok(L.FORMATS_330A == ("--format=%H", "--pretty=%H", "--format=format:%H"),
   "the copy of mg-330a's format tuple in lib_0ba7 still matches its source")
import lib330a                                                # noqa: E402
ok(tuple(lib330a._HASH_FORMATS) == L.FORMATS_330A,
   "and it matches character for character AT RUN TIME, so a1's `why` "
   "cannot go stale silently")
ok(set(L.FORMATS_330A) < set(L.HASH_FORMATS),
   "mg-330a's format set is a PROPER SUBSET of mine; the widening is one-way")

# ---------------------------------------------------------------------------
L.rule("(3) STRING EXTRACTION -- NESTED CALLS ARE NOT ATTRIBUTED OUTWARD")
# ---------------------------------------------------------------------------
src = 'outer(inner("--reverse"), "log", "--format=%H", "--", "a.py")'
call = ast.parse(src).body[0].value
ok("--reverse" not in L.direct_strings(call),
   "a string inside a NESTED call is not a direct argument of the outer one")
ok(L.kind_of(L.direct_strings(call)) == "NEWEST-norestrict"
   or L.kind_of(L.direct_strings(call)) == "INDEXED",
   "so the nested `--reverse` does not turn the outer call into OLDEST "
   "(got %s)" % L.kind_of(L.direct_strings(call)))
src2 = 'f(["log", "--format=%H", "--", "a.py"])'
ok(L.kind_of(L.direct_strings(ast.parse(src2).body[0].value)) == "INDEXED",
   "a LIST argument is flattened -- subprocess-style argv is seen")
src3 = 'f(("log", "--format=%H", "--reverse", "--", "a.py"))'
ok(L.kind_of(L.direct_strings(ast.parse(src3).body[0].value)) == "OLDEST",
   "a TUPLE argument is flattened too")

# ---------------------------------------------------------------------------
L.rule("(4) THE TAINT TEST -- THE DEFECT THIS INSTRUMENT HAD")
# ---------------------------------------------------------------------------
def _fd(src):
    return ast.parse(src).body[0]


ASSIGN = '''
def f(p):
    h = git("log", "-1", "--format=%H", "--", p)
    return h
'''
FORLOOP = '''
def f(p):
    for h in git("log", "--format=%H", "--", p).split():
        return h
    return None
'''
PRINTS = '''
def f(p):
    print(git("log", "-1", "--format=%H", "--", p))
    return 0
'''
NONE = '''
def f(p):
    return p
'''
ok(L._tainted_return(_fd(ASSIGN)) == (True, True),
   "a function that ASSIGNS the anchor and returns it is a wrapper")
ok(L._tainted_return(_fd(FORLOOP)) == (True, True),
   "a function that receives it through a FOR TARGET is a wrapper too -- "
   "this is the assertion the first form of _tainted_return failed")
ok(L._tainted_return(_fd(PRINTS)) == (True, False),
   "a function that PRINTS it and returns 0 is not a wrapper: its callers "
   "obtain no anchor")
ok(L._tainted_return(_fd(NONE)) == (False, False),
   "a function with no history call at all is not a seed")

WALRUS = '''
def f(p):
    if (h := git("log", "-1", "--format=%H", "--", p)):
        return h
    return None
'''
ok(L._tainted_return(_fd(WALRUS)) == (True, True),
   "a walrus binding is propagated as well")

# ---------------------------------------------------------------------------
L.rule("(5) IMPORT RESOLUTION -- THE NAME COLLISION IS THE POINT")
# ---------------------------------------------------------------------------
FILES = {
    "d/libA.py": "def last_touching(p):\n    pass\n",
    "d/libB.py": "def last_touching(p):\n    pass\n",
    "d/user1.py": "from libA import last_touching\nlast_touching('x')\n",
    "d/user2.py": "import libB as B\nB.last_touching('x')\n",
}
trees = {r: ast.parse(s) for r, s in FILES.items()}
b1, a1, s1 = L.bindings_of("d/user1.py", trees["d/user1.py"], trees)
ok(b1.get("last_touching") == ("d/libA.py", "last_touching"),
   "`from libA import last_touching` binds to libA, not to libB")
b2, a2, s2 = L.bindings_of("d/user2.py", trees["d/user2.py"], trees)
ok(a2.get("B") == "d/libB.py",
   "`import libB as B` binds the alias to libB")
ok(b1.get("last_touching") != ("d/libB.py", "last_touching"),
   "a BARE NAME match would have conflated the two; the binding does not")
ok(not s1 and not s2, "neither constructed file uses `import *`")

STAR = {"d/libA.py": FILES["d/libA.py"],
        "d/u.py": "from libA import *\nlast_touching('x')\n"}
st = {r: ast.parse(s) for r, s in STAR.items()}
_b, _a, star = L.bindings_of("d/u.py", st["d/u.py"], st)
ok(star, "`import *` is REPORTED, so a file whose bindings cannot be "
         "enumerated is named rather than silently resolved")

AMB = {"x/lib.py": "", "y/lib.py": "", "z/u.py": "from lib import f\n"}
at = {r: ast.parse(s) for r, s in AMB.items()}
ok(L._module_file("z/u.py", "lib", at) is None,
   "a module basename that is ambiguous across directories resolves to "
   "None rather than to whichever came first")

# ---------------------------------------------------------------------------
L.rule("(6) THE TWO LABELS")
# ---------------------------------------------------------------------------
ok(L.kind_by_path("code/x/out_t1.txt") == "RECORD",
   "a transcript is a RECORD by KIND")
ok(L.kind_by_path("code/x/PREDICTIONS.md") == "RECORD",
   "a prediction file is a RECORD by KIND")
ok(L.kind_by_path("code/x/t1.py") == "LIVE CLAIM",
   "a script is a LIVE CLAIM by KIND")
ok(L.scope_by_dir("code/anchor_population_audit_0ba7/a1_population.py")
   == "MINE", "SCOPE is MINE inside my own directory")
ok(L.scope_by_dir("code/repair_b2af/t1_population.py")
   == "ANOTHER TICKET'S", "SCOPE is another ticket's outside it")
ok(L.kind_by_path("code/repair_b2af/t1_population.py") == "LIVE CLAIM"
   and L.scope_by_dir("code/repair_b2af/t1_population.py")
   == "ANOTHER TICKET'S",
   "one path, two labels, two different answers -- which is F-2")

# ---------------------------------------------------------------------------
L.rule("(7) `gate_spent`: AN UNKNOWN NAME IS A SELF-ERROR")
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(L.REPO, "code", "branching_audit_e34a"))
import libe34a as E                                           # noqa: E402


class P(object):
    def __init__(self):
        self.s, self.f = [], []

    def selferr(self, m):
        self.s.append(m)

    def finding(self, m):
        self.f.append(m)


p = P()
ok(E.gate_spent(p, "NOT_AN_ANCHOR") is False and p.s and not p.f,
   "an unknown name is a SELF-ERROR and returns False, not a silent pass")
p = P()
ok(E.gate_spent(p, "REPAIR_REV") is True and not p.s and not p.f,
   "a known, undrifted anchor gates silently and returns True")
p = P()
E.gate_spent(p, "LAST_TOUCHING_G1")
ok(bool(p.s),
   "`LAST_TOUCHING_G1` -- an anchor libe34a DERIVES -- is a self-error too, "
   "which is a3 (ii)'s finding reproduced on a call written here")

# ---------------------------------------------------------------------------
L.rule("(8) PATCH-ID: THE IDENTITY THAT SURVIVES A REBASE")
# ---------------------------------------------------------------------------
print("""   Ancestry gives a FALSE NEGATIVE after a rebase.  These two
   assertions are the reason every content claim in this deliverable is
   made with `git patch-id --stable` and not with `merge-base --is-ancestor`.
""")
head = L.resolve("HEAD")
pid = L.patch_id(head)
ok(len(pid) == 40, "patch_id(HEAD) returns a 40-character id (got %d chars)"
   % len(pid))
ok(L.same_content(head, head), "a commit has the same content as itself")
ok(not L.same_content(head, L.resolve("HEAD~1")),
   "and not the same content as its parent")

d = L.clone_at("HEAD~1")
try:
    L.run_py  # keep the import honest
    import subprocess
    subprocess.run(["git", "-C", d, "checkout", "--quiet", "-b", "t"],
                   capture_output=True, text=True)
    subprocess.run(["git", "-C", d, "cherry-pick", "--quiet", head],
                   capture_output=True, text=True)
    picked = L.resolve("HEAD", repo=d)
    ok(picked != head, "a cherry-pick produces a DIFFERENT sha")
    ok(L.patch_id(picked, repo=d) == L.patch_id(head, repo=d),
       "and the SAME patch-id -- which is how a rebased commit is "
       "recognised on main")
finally:
    L.rm_tree(d)

# ---------------------------------------------------------------------------
L.rule("(9) THE REPORT REFUSES A BARE TOTAL")
# ---------------------------------------------------------------------------
r = L.Report("s", "f")
r.total("labelled", 1, "a population", "a grain")
ok(not r.selferrs, "a labelled total books no self-error")
r.total("bare", 1, "", "")
ok(len(r.selferrs) == 1,
   "a total with no population and no grain books a SELF-ERROR")

# ---------------------------------------------------------------------------
L.rule("(10) THE SCORER -- THE SECOND DEFECT THIS INSTRUMENT HAD")
# ---------------------------------------------------------------------------
r2 = L.Report("s", "f")
ok(L.score(r2, "T", 5, 5) is True, "an equality row scores HIT")
ok(L.score(r2, "T", "1..9", 5) is False,
   "a RANGE row with no `hit=` scores MISS -- this is the defect, kept "
   "visible: `==` cannot express `1..9`")
ok(L.score(r2, "T", "1..9", 5, hit=True) is True,
   "and the caller stating the comparison scores it correctly")

# ---------------------------------------------------------------------------
L.rule("SUMMARY")
# ---------------------------------------------------------------------------
print("   assertions run    : %d" % OK[0])
print("   assertions failed : %d" % len(BAD))
for m in BAD:
    print("     FAILED: %s" % m)
print("   population        : the constructed inputs written in this file")
print("   grain             : one ASSERTION")
raise SystemExit(1 if BAD else 0)
