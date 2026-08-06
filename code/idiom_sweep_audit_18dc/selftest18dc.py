"""mg-18dc / SELFTEST -- the instrument, run against runners built to have a
known answer.

Every assertion here is a runner or a probe this file WRITES, in a scratch
directory outside the repository, whose classification is known before the
instrument sees it.  A sweep that only ever runs on the arc cannot tell a
correct answer from a confident one.

Exit code = failed assertions.
"""

import os
import shutil
import subprocess
import sys
import tempfile

import lib18dc as B

FAILED = []
PASSED = 0


def ok(name, cond, detail=""):
    global PASSED
    if cond:
        PASSED += 1
        print("      pass  %s" % name)
    else:
        FAILED.append(name)
        print("      FAIL  %s   %s" % (name, detail))


print("mg-18dc / SELFTEST")
print("HEAD: %s" % B.head())

ROOT = tempfile.mkdtemp(prefix="mg18dc-selftest-")


def mktree(name, runner, probes, outs):
    """A fake tree, git-initialised so the sandbox helpers work on it."""
    d = os.path.join(ROOT, name, "code", name)
    os.makedirs(d)
    open(os.path.join(d, "run_all.sh"), "w").write(runner)
    for f, s in probes.items():
        open(os.path.join(d, f), "w").write(s)
    for f, s in outs.items():
        open(os.path.join(d, f), "w").write(s)
    r = os.path.join(ROOT, name)
    subprocess.run(["git", "init", "-q"], cwd=r, capture_output=True)
    subprocess.run(["git", "add", "-A"], cwd=r, capture_output=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t",
                    "commit", "-qm", "x"], cwd=r, capture_output=True)
    return r, "code/%s" % name


# ---------------------------------------------------------------------------
B.hdr("A.  THE STUB DISTINGUISHES `>` FROM `.new`+`mv`")

r1, t1 = mktree("plain", "python3 p1.py > out_p1.txt\n",
                {"p1.py": "print('hi')\n"}, {"out_p1.txt": "OLD BYTES\n"})
res, _ = B.stub_run(r1, t1, timeout=30)
st = B.emptied_steps(res)
ok("A1  a `>` runner starts its probe on an empty transcript", len(st) == 1,
   "got %r" % st)
ok("A2  and the empty file is the one that probe writes",
   bool(st) and st[0]["zero"] == ["out_p1.txt"], "got %r" % st)

r2, t2 = mktree("newmv", "python3 p1.py > out_p1.txt.new && mv out_p1.txt.new out_p1.txt\n",
                {"p1.py": "print('hi')\n"}, {"out_p1.txt": "OLD BYTES\n"})
res2, _ = B.stub_run(r2, t2, timeout=30)
ok("A3  a `.new`+`mv` runner starts its probe on the PREVIOUS bytes",
   B.emptied_steps(res2) == [], "got %r" % B.emptied_steps(res2))

r2b, t2b = mktree("twostep",
                  "python3 p1.py > out_p1.txt.new && mv out_p1.txt.new out_p1.txt\n"
                  "python3 p2.py > out_p2.txt.new && mv out_p2.txt.new out_p2.txt\n",
                  {"p1.py": "print('a')\n", "p2.py": "print('b')\n"},
                  {"out_p1.txt": "OLD1\n", "out_p2.txt": "OLD2\n"})
res2b, _ = B.stub_run(r2b, t2b, timeout=30)
ok("A4  and the SECOND step of a `.new`+`mv` runner is clean too -- the "
   "control that a silent stub would have destroyed",
   B.emptied_steps(res2b) == [], "got %r" % B.emptied_steps(res2b))

r3, t3 = mktree("append", "python3 p1.py >> out_p1.txt\n",
                {"p1.py": "print('hi')\n"}, {"out_p1.txt": "OLD BYTES\n"})
res3, _ = B.stub_run(r3, t3, timeout=30)
ok("A5  `>>` is not truncation", B.emptied_steps(res3) == [],
   "got %r" % B.emptied_steps(res3))

r4, t4 = mktree("helper",
                "run() { python3 \"$2\" > \"$1\" ; }\nrun out_p1.txt p1.py\n",
                {"p1.py": "print('hi')\n"}, {"out_p1.txt": "OLD BYTES\n"})
res4, _ = B.stub_run(r4, t4, timeout=30)
ok("A6  the OUT-FIRST helper idiom is measured without being parsed",
   len(B.emptied_steps(res4)) == 1, "got %r" % B.emptied_steps(res4))

r5, t5 = mktree("loop",
                "for s in a b c ; do python3 \"$s.py\" > \"out_$s.txt\" ; done\n",
                {"a.py": "print(1)\n", "b.py": "print(2)\n", "c.py": "print(3)\n"},
                {"out_a.txt": "A\n", "out_b.txt": "B\n", "out_c.txt": "C\n"})
res5, _ = B.stub_run(r5, t5, timeout=30)
ok("A7  a LOOP is N steps and not one", len(B.emptied_steps(res5)) == 3,
   "got %d" % len(B.emptied_steps(res5)))

# ---------------------------------------------------------------------------
B.hdr("B.  THE READ SHIM RECORDS THE SIZE THE OPENER SAW")

PROBE_READ = ("import io\n"
              "print(open('out_p1.txt').read())\n")
r6, t6 = mktree("bite", "python3 p1.py > out_p1.txt\npython3 p2.py > out_p2.txt\n",
                {"p1.py": "print('one')\n", "p2.py": PROBE_READ},
                {"out_p1.txt": "OLD BYTES\n", "out_p2.txt": "OLD2\n"})
rec = B.real_run(r6, t6, timeout=60)
hits = B.own_empty_reads(rec, r6, t6)
# SD1 of this instrument: this assertion shipped for one draft under the name
# "a probe reading a transcript THIS RUN emptied is caught" while asserting
# len(hits) == 0.  The name was the opposite of the measurement.  What the
# fixture actually builds is the STALE case -- p1 has already REWRITTEN
# out_p1.txt by the time p2 reads it, so the file has bytes and this must NOT
# fire.  Renamed to what it measures.
ok("B1  a transcript an EARLIER step of the same run rewrote is populated, "
   "not empty, when a later probe reads it (the STALE case, and NOT a bite)",
   rec is not None and len(hits) == 0,
   "expected 0; got %r" % [h["path"] for h in hits])

PROBE_READ_OWN = ("print(open('out_p2.txt').read())\n")
r7, t7 = mktree("biteown", "python3 p2.py > out_p2.txt\n",
                {"p2.py": PROBE_READ_OWN}, {"out_p2.txt": "OLD2\n"})
rec7 = B.real_run(r7, t7, timeout=60)
hits7 = B.own_empty_reads(rec7, r7, t7)
ok("B2  a probe reading its OWN emptied transcript IS caught, at size 0",
   len(hits7) == 1 and hits7[0]["size"] == 0, "got %r" % hits7)

PROBE_WRITE = ("open('out_p2.txt','w').write('x')\n")
r8, t8 = mktree("writenotread", "python3 p2.py > out_zz.txt\n",
                {"p2.py": PROBE_WRITE}, {"out_p2.txt": "OLD2\n", "out_zz.txt": "Z\n"})
rec8 = B.real_run(r8, t8, timeout=60)
ok("B3  a WRITE of an empty transcript is not counted as a READ",
   B.own_empty_reads(rec8, r8, t8) == [],
   "got %r" % B.own_empty_reads(rec8, r8, t8))

OTHER = os.path.join(ROOT, "other")
os.makedirs(OTHER, exist_ok=True)
open(os.path.join(OTHER, "out_foreign.txt"), "w").close()
PROBE_FOREIGN = "print(open(%r).read())\n" % os.path.join(OTHER, "out_foreign.txt")
r9, t9 = mktree("foreign", "python3 p2.py > out_p2.txt\n",
                {"p2.py": PROBE_FOREIGN}, {"out_p2.txt": "OLD2\n"})
rec9 = B.real_run(r9, t9, timeout=60)
ok("B4  an empty `out_` file OUTSIDE the tree is not attributed to it",
   B.own_empty_reads(rec9, r9, t9) == [],
   "got %r" % B.own_empty_reads(rec9, r9, t9))

CHILD = ("import subprocess, sys\n"
         "subprocess.run([sys.executable, 'p3.py'])\n")
r10, t10 = mktree("child", "python3 p2.py > out_p2.txt\n",
                  {"p2.py": CHILD, "p3.py": PROBE_READ_OWN},
                  {"out_p2.txt": "OLD2\n"})
rec10 = B.real_run(r10, t10, timeout=60)
h10 = B.own_empty_reads(rec10, r10, t10)
# SD2 of this instrument: the first draft of this assertion was
#   len(h10) == 1 and ... and pids != {...} or len(h10) == 1
# whose trailing `or len(h10) == 1` makes the pid half unable to fail.  An
# assertion that cannot fail on the property it names is a green row that
# measures nothing -- this ticket's own defect class, in my selftest.  The two
# properties are now separate assertions.
ok("B5  a CHILD's read of an emptied transcript is recorded at all",
   len(h10) == 1, "got %r" % h10)
parent_pids = {o["pid"] for o in (rec10["opens"] if rec10 else [])
               if "w" in o["mode"]}
ok("B5a  and it is attributed to the CHILD's pid, not the parent's",
   len(h10) == 1 and (not parent_pids or h10[0]["pid"] not in parent_pids),
   "child pid %r, writer pids %r"
   % ([h["pid"] for h in h10], sorted(parent_pids)))

# ---------------------------------------------------------------------------
B.hdr("C.  THE POPULATION RULE IS A PROPERTY OF A COMMIT")

a = B.runners_at("d33970b")
b = B.runners_at("9f1ecaa")
ok("C1  runners_at differs between two revisions", a != b)
ok("C2  and it does not read the working directory: the answer for a revision "
   "is stable across two calls", B.runners_at("d33970b") == a)
ok("C3  every returned path is `code/<one dir>`",
   all(x.count("/") == 1 and x.startswith("code/") for x in a))

# ---------------------------------------------------------------------------
B.hdr("D.  THE SANDBOX CANNOT REACH THE WORKTREE")

ok("D1  WORK is outside the repository", not B.WORK.startswith(B.REPO))
sb = B.sandbox("d33970b", tag="d33970b-selftest")
ok("D2  the sandbox is outside the repository", not sb.startswith(B.REPO))
p = os.path.join(sb, "code", "audit_2c77", "out_q1_reason.txt")
if os.path.exists(p):
    open(p, "w").write("DESTROYED BY THE SELFTEST\n")
    src = os.path.join(B.REPO, "code", "audit_2c77", "out_q1_reason.txt")
    ok("D3  destroying a transcript in the sandbox leaves the worktree's alone",
       open(src).read() != "DESTROYED BY THE SELFTEST\n")
    ok("D4  and the sandbox restore puts it back",
       B.sandbox_reset(sb) == [] and open(p).read() != "DESTROYED BY THE SELFTEST\n")

# ---------------------------------------------------------------------------
B.hdr("E.  THE SANDBOX LOOKS LIKE THE WORKTREE TO A PROBE THAT RESOLVES `main`")

r = subprocess.run(["git", "rev-parse", "--verify", "main"], cwd=sb,
                   capture_output=True, text=True)
ok("E1  the clone has a resolvable local `main` (SD14: `git clone` creates "
   "only the source's CURRENT branch, and in a polecat worktree that is not "
   "`main`; every arc probe doing `git diff main..HEAD` crashed without it)",
   r.returncode == 0, "rev-parse main -> %s" % r.returncode)
r2 = subprocess.run(["git", "rev-parse", "--verify", "main"], cwd=B.REPO,
                    capture_output=True, text=True)
ok("E2  and it is the SAME commit `main` names in the worktree",
   r.stdout.strip() == r2.stdout.strip() and r.returncode == 0,
   "clone %s vs worktree %s" % (r.stdout.strip()[:8], r2.stdout.strip()[:8]))

env = dict(os.environ)
env["V18_RUNNING"] = "a-caller-that-should-not-stop-a-measurement"
r3, t3 = mktree("guarded", "python3 p1.py > out_p1.txt\n",
                {"p1.py": "print('hi')\n"}, {"out_p1.txt": "OLD\n"})
saved = os.environ.get("V18_RUNNING")
os.environ["V18_RUNNING"] = "outer"
resg, _ = B.stub_run(r3, t3, timeout=30)
if saved is None:
    os.environ.pop("V18_RUNNING", None)
else:
    os.environ["V18_RUNNING"] = saved
ok("E3  an inherited V18_RUNNING does not silence a measured runner "
   "(SD13: it silenced THIS suite's own and the empty result was printed as a "
   "clean bill of health)",
   resg is not None and len(resg["rows"]) == 1,
   "got %r invocations" % (len(resg["rows"]) if resg else None))

shutil.rmtree(ROOT, ignore_errors=True)

print()
print("population: the assertions in this file")
B.plain("...ASSERTIONS run", PASSED + len(FAILED), "one assertion")
B.plain("...ASSERTIONS passed", PASSED, "one assertion")
B.plain("...ASSERTIONS FAILED", len(FAILED), "one assertion")
for f in FAILED:
    print("      FAILED: %s" % f)
print()
print("SELFTEST FAILURES: %d" % len(FAILED))
sys.exit(min(len(FAILED), 120))
