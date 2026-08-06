"""mg-ec63 / SELFTEST -- every rule of this instrument, on CONSTRUCTED input.

Nothing here reads the arc.  Every assertion is against a runner or a probe
written inside this file, so a change in the arc cannot turn this green or red
and a bug in this suite cannot hide behind the corpus.

THE THING BEING TESTED IS THE PARSER'S ARGUMENT ORDER.  The failure this suite
exists to avoid is reading `run out_d1.txt d1_trace.py` as "run the transcript,
write the probe" -- an off-by-one in a helper's positional parameters, which is
invisible in the output because both words look like plausible file names.  So
the two orders are tested SIDE BY SIDE, and a positive control carries both.

Exit code = number of failed assertions.
"""

import os
import shutil
import subprocess
import sys
import tempfile

import lib_ec63 as B

BAD = 0
N = 0


def ck(label, got, want):
    global BAD, N
    N += 1
    ok = got == want
    if not ok:
        BAD += 1
    print("  %-4s %-58s got %r" % ("ok" if ok else "FAIL", label, got))
    if not ok:
        print("       %-58s want %r" % ("", want))


def parse_text(text, name="t_fixture"):
    """Parse a CONSTRUCTED runner by writing it into a scratch tree."""
    d = os.path.join(B.REPO, "code", name)
    os.makedirs(d, exist_ok=True)
    try:
        with open(os.path.join(d, "run_all.sh"), "w") as f:
            f.write(text)
        for stem in ("p1", "p2", "p3", "d1_trace", "s1_census", "selftest_x"):
            open(os.path.join(d, stem + ".py"), "a").close()
            open(os.path.join(d, "out_%s.txt" % stem), "a").close()
        return B.parse_runner("code/" + name)
    finally:
        shutil.rmtree(d, ignore_errors=True)


print("mg-ec63 / SELFTEST")
print()

B.hdr("T1  THE SIX RUNNER IDIOMS, AND THE TWO ARGUMENT ORDERS")

steps, un = parse_text("""#!/bin/sh
python3 p1.py > out_p1.txt
""")
ck("direct redirect", steps, [("code/t_fixture/p1.py",
                               "code/t_fixture/out_p1.txt", "TRUNC")])

steps, un = parse_text("""#!/bin/sh
run() {
    _p=$1
    _o=$2
    python3 -B "$_p" > "$_o"
}
run p1.py out_p1.txt
""")
ck("helper, PROBE first", steps, [("code/t_fixture/p1.py",
                                   "code/t_fixture/out_p1.txt", "TRUNC")])

steps, un = parse_text("""#!/bin/sh
run() {
    out=$1
    shift
    python3 "$@" > "$out" 2>&1
}
run out_d1_trace.txt d1_trace.py 5
""")
ck("helper, OUT first (the order that flips the answer)", steps,
   [("code/t_fixture/d1_trace.py", "code/t_fixture/out_d1_trace.txt",
     "TRUNC")])

steps, un = parse_text("""#!/bin/sh
expect() {
    want="$1"; shift
    out="out_$(basename "$1" .py).txt"
    python3 "$1" > "$out"
}
expect 0 p2.py
""")
ck("helper, out name DERIVED from the probe stem", steps,
   [("code/t_fixture/p2.py", "code/t_fixture/out_p2.txt", "TRUNC")])

steps, un = parse_text("""#!/bin/sh
HERE=$(dirname "$0")
run() {
    name=$1
    python3 "$HERE/$name.py" > "$HERE/out_$name.txt" 2>&1
}
run s1_census 1
""")
ck("helper, no extension, opaque directory prefix", steps,
   [("code/t_fixture/s1_census.py", "code/t_fixture/out_s1_census.txt",
     "TRUNC")])

steps, un = parse_text("""#!/bin/sh
for s in p1 p2 \\
         p3 ; do
    python3 -W ignore "$s.py" > "out_$s.txt" 2>&1
done
""")
ck("a LOOP is N steps, not one", [s[0] for s in steps],
   ["code/t_fixture/p1.py", "code/t_fixture/p2.py", "code/t_fixture/p3.py"])

B.hdr("T2  THE OPERATORS TOLD APART")

steps, un = parse_text("""#!/bin/sh
run() {
    _p=$1
    _o=$2
    python3 "$_p" > "$_o.new" 2>&1
    mv -f "$_o.new" "$_o"
}
run p1.py out_p1.txt
""")
ck("`.new` + `mv` is STRUCT, and the target loses `.new`", steps,
   [("code/t_fixture/p1.py", "code/t_fixture/out_p1.txt", "STRUCT")])

steps, un = parse_text("""#!/bin/sh
python3 p1.py >> out_p1.txt
""")
ck("`>>` is APPEND, not TRUNC", [s[2] for s in steps], ["APPEND"])

steps, un = parse_text("""#!/bin/sh
python3 p1.py
""")
ck("no redirect is STREAM", steps, [("code/t_fixture/p1.py", None, "STREAM")])

B.hdr("T3  WHAT IT REFUSES TO GUESS AT, AND WHAT IT REFUSES TO INVENT")

steps, un = parse_text("""#!/bin/sh
( cd ../elsewhere && python3 p1.py ) > out_p1.txt
""")
ck("a `cd` into another tree is UNRESOLVED, not mis-attributed", steps, [])
ck("...and is reported", len(un), 1)

steps, un = parse_text("""#!/bin/sh
step() {
    echo "### $1"
    shift
    python3 "$@"
}
step "F2: can the V6 row go red?  five constructions" p1.py
""")
ck("a QUOTED argument with spaces is ONE argument", steps,
   [("code/t_fixture/p1.py", None, "STREAM")])
print("       ^ split on whitespace this reads a probe called `can` writing a")
print("         transcript called `the`, which is what it did before shlex.")

steps, un = parse_text("""#!/bin/sh
echo "run python3 p1.py > out_p1.txt to reproduce"
""")
ck("prose that TALKS about a step is not a step", steps, [])

steps, un = parse_text("""#!/bin/sh
# python3 p1.py > out_p1.txt
python3 p2.py > out_p2.txt
""")
ck("a commented-out step is not a step", [s[0] for s in steps],
   ["code/t_fixture/p2.py"])

B.hdr("T4  THE OPEN TRACE, ON A CONSTRUCTED PROBE")

d = tempfile.mkdtemp(prefix="ec63_", dir=os.path.join(B.REPO, "code"))
tname = "code/" + os.path.basename(d)
try:
    with open(os.path.join(d, "out_reader.txt"), "w") as f:
        f.write("SEVENTEEN\n")
    with open(os.path.join(d, "out_other.txt"), "w") as f:
        f.write("other\n")
    # a probe that reads its OWN transcript through a variable -- the literal
    # `out_reader.txt` never appears in its source, so a text rule misses it
    with open(os.path.join(d, "reader.py"), "w") as f:
        f.write("import os\n"
                "stem = 'read' + 'er'\n"
                "p = os.path.join(os.path.dirname(os.path.abspath(__file__)),\n"
                "                 'out_' + stem + '.txt')\n"
                "print('LEN', len(open(p).read().strip()))\n")
    with open(os.path.join(d, "blind.py"), "w") as f:
        f.write("# mentions out_reader.txt in a comment and opens nothing\n"
                "print('LEN 0')\n")
    with open(os.path.join(d, "nosy.py"), "w") as f:
        f.write("import os\n"
                "p = os.path.join(os.path.dirname(os.path.abspath(__file__)),\n"
                "                 'out_other.txt')\n"
                "print('OTHER', len(open(p).read()))\n")

    r = B.run_probe(tname, "reader.py", "out_reader.txt", empty_first=False,
                    timeout=30, trace=True)
    ck("trace sees a probe open its own transcript",
       B.opened_own(r, tname, "out_reader.txt"), True)
    ck("...and B reads the real bytes", r["text"].strip(), "LEN 9")

    r = B.run_probe(tname, "reader.py", "out_reader.txt", empty_first=True,
                    timeout=30, trace=True)
    ck("A reads NOTHING -- the shape reproduced", r["text"].strip(), "LEN 0")

    ck("the tree is restored: the transcript is back",
       open(os.path.join(d, "out_reader.txt")).read().strip(), "SEVENTEEN")

    r = B.run_probe(tname, "blind.py", "out_blind.txt", empty_first=False,
                    timeout=30, trace=True)
    ck("a probe that only MENTIONS a transcript does not open one",
       B.opened_own(r, tname, "out_blind.txt"), False)

    r = B.run_probe(tname, "nosy.py", "out_nosy.txt", empty_first=False,
                    timeout=30, trace=True)
    ck("reading ANOTHER transcript is not the EMPTIED class",
       B.opened_own(r, tname, "out_nosy.txt"), False)
    ck("...it is the STALE class, and is reported apart",
       B.opened_other_outs(r, tname, "out_nosy.txt"), ["out_other.txt"])
finally:
    # ONLY the fixture is removed.  An earlier version ran `git checkout --
    # code` here, which is a repo-wide restore fired from a selftest -- and
    # this suite's other probes are, by design, running other tickets' scripts.
    # A blanket restore from inside a test is a write nobody asked for.
    shutil.rmtree(d, ignore_errors=True)

B.hdr("T5  THE CLASSIFIER, ON CONSTRUCTED RECORDS")

# s3_sweep.py does its work at import time, so its classifier cannot be
# imported without running the sweep.  It is RE-STATED here -- and re-stating a
# rule is exactly how two copies drift apart, which is a defect this arc has
# already recorded twice.  So the last assertion of T5 reads s3's own source
# and checks the two still say the same thing.


def classify(row):
    if row["A_to"] and not row["B_to"]:
        return "A TIMED OUT"
    if row["A_to"] and row["B_to"]:
        return "BOTH TIMED OUT"
    if row.get("nondet"):
        return "NONDETERMINISTIC"
    b_broke = row["B_to"] or (row["B_exit"] is not None
                              and "Traceback" in row["B_text"])
    a_ok = (not row["A_to"]) and "Traceback" not in row["A_text"]
    if b_broke and a_ok:
        return "NEVER EXERCISED"
    if row["A_text"] == row["B_text"]:
        return "SAME"
    return "DIFFERENT"


base = {"A_text": "x", "B_text": "x", "A_to": False, "B_to": False,
        "A_exit": 0, "B_exit": 0}
ck("identical output is SAME", classify(dict(base)), "SAME")
ck("different output is DIFFERENT",
   classify(dict(base, B_text="y")), "DIFFERENT")
ck("B crashing where A did not is NEVER EXERCISED",
   classify(dict(base, B_text="Traceback (most recent call last):", B_exit=1)),
   "NEVER EXERCISED")
ck("B timing out where A did not is NEVER EXERCISED",
   classify(dict(base, B_text="y", B_to=True, B_exit=None)),
   "NEVER EXERCISED")
ck("a nondeterministic probe is NOT counted as DIFFERENT",
   classify(dict(base, B_text="y", nondet=True)), "NONDETERMINISTIC")
ck("A crashing too is not NEVER EXERCISED -- the probe is just broken",
   classify(dict(base, A_text="Traceback x", B_text="Traceback y", B_exit=1)),
   "DIFFERENT")
ck("A timing out is NOT a difference -- A never finished",
   classify(dict(base, A_to=True, A_exit=None, B_text="y")), "A TIMED OUT")
ck("...and if both time out, neither run answered anything",
   classify(dict(base, A_to=True, B_to=True, A_exit=None, B_exit=None,
                 B_text="y")), "BOTH TIMED OUT")

src = B.read("%s/s3_sweep.py" % B.MINE)
body = src.split("def classify(row):", 1)[1].split("\n\n\n")[0]
mine = ('    if row.get("nondet")' in body
        and '"NEVER EXERCISED"' in body and '"SAME"' in body
        and 'row["A_text"] == row["B_text"]' in body)
ck("the classifier tested here is the one s3 uses (checked by reading it)",
   mine, True)

B.hdr("T6  THE POPULATION RULE'S OWN EDGE")

ck("a step whose transcript does not exist yields a path, not a crash",
   bool(B.locate("code/nowhere", "out_nothing.txt")), True)
ck("locate finds a CROSS-TREE probe by its repo-relative path",
   B.locate("code/truncate_sweep_ec63", "code/truncate_sweep_ec63/"
            "lib_ec63.py"), "code/truncate_sweep_ec63/lib_ec63.py")

print()
print("selftest_ec63 TOTAL: %d assertions, %d BAD" % (N, BAD))
sys.exit(min(BAD, 120))
