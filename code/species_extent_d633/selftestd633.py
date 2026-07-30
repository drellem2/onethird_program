"""SELF-TEST for mg-d633's kernel.

Roughly half of these assert that the detector does NOT fire.  A detector only
ever seen to fire is a detector that fires on everything, and the two findings
this instrument exists to close were both a checker being silent where its own
extent line said it was looking.

    python3 code/species_extent_d633/selftestd633.py
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

from kernd633 import (toks, paragraphs, fences, longest_run, strike_findings,
                      md_files, sandbox, NEGATES, RUN_MIN, RUN_FRAC, REPO)

n = 0
fail = 0


def ck(label, cond):
    global n, fail
    n += 1
    if not cond:
        fail += 1
        print("  *** FAILED: %s" % label)


# --- tokens ----------------------------------------------------------------
ck("toks splits words", toks("one two") == ["one", "two"])
ck("toks lowercases", toks("ONE") == ["one"])
ck("toks separates punctuation", toks("K(P)") == ["k", "(", "p", ")"])
ck("toks strips blockquote markers", toks("> a b") == ["a", "b"])
ck("toks strips nested blockquote markers", toks("> > a") == ["a"])
ck("toks on empty is empty", toks("") == [])
ck("toks keeps digits", toks("4 399") == ["4", "399"])

# --- paragraphs and fences --------------------------------------------------
P = "a\n\nb\n\nc"
ck("three paragraphs", len(paragraphs(P)) == 3)
ck("paragraph offsets bracket their text",
   P[paragraphs(P)[1][0]:paragraphs(P)[1][1]] == "b")
ck("a blank line with spaces still splits", len(paragraphs("a\n   \nb")) == 2)
ck("one paragraph when there is no blank line",
   len(paragraphs("a\nb\nc")) == 1)
F = "x\n```\nq\n```\ny"
ck("one fence found", len(fences(F)) == 1)
ck("no fence in plain text", fences("x\ny") == [])
ck("an odd number of fence markers yields no unterminated fence",
   len(fences("```\na\n```\nb\n```")) == 1)

# --- longest run ------------------------------------------------------------
b = ["a", "b", "c", "d"]
idx = {}
for i, t in enumerate(b):
    idx.setdefault(t, []).append(i)
ck("identical sequences run the whole length",
   longest_run(["a", "b", "c", "d"], b, idx)[0] == 4)
ck("a shared middle is found", longest_run(["z", "b", "c"], b, idx)[0] == 2)
ck("no overlap gives 0", longest_run(["x", "y"], b, idx)[0] == 0)
ck("an empty needle gives 0", longest_run([], b, idx)[0] == 0)
ck("the run is CONSECUTIVE, not a bag of words",
   longest_run(["a", "c"], b, idx)[0] == 1)

# --- the rule ---------------------------------------------------------------
CLAIM = ("the quotient of the descent algebra is a commutative split algebra "
         "of dimension p of n and carries no multiplicity whatsoever")


def doc(strike, rest):
    return "# t\n\nsomething.\n\n~~%s~~\n\n%s\n" % (strike, rest)


fired = [f for f in strike_findings(doc(CLAIM, CLAIM)) if f[4] is False]
ck("the claim restated verbatim FIRES", len(fired) == 1)
ck("...and reports the run as the whole strike",
   fired and fired[0][2] == len(toks(CLAIM)))

ck("a document with no strike is silent",
   strike_findings("# t\n\nnothing struck here.\n") == [])
ck("a strike restated NOWHERE is silent",
   not [f for f in strike_findings(doc(CLAIM, "an unrelated paragraph."))
        if f[4] is False])
short = " ".join(toks(CLAIM)[:6])
ck("a shared run below RUN_MIN (%d tokens) is silent" % RUN_MIN,
   not [f for f in strike_findings(doc(CLAIM, short)) if f[4] is False])
part = " ".join(toks(CLAIM)[:10])
ck("a shared run below RUN_FRAC (%.0f%%) is silent" % (100 * RUN_FRAC),
   not [f for f in strike_findings(doc(CLAIM, part)) if f[4] is False])
ck("...and that run is over RUN_MIN, so it is the FRACTION doing the work",
   len(toks(part)) > RUN_MIN)

ck("a restatement whose paragraph says it is STRUCK is exonerated",
   [f for f in strike_findings(doc(CLAIM, "This is struck: " + CLAIM))
    if f[4] is True])
ck("...and 'misquotation' exonerates too",
   [f for f in strike_findings(doc(CLAIM, "A misquotation: " + CLAIM))
    if f[4] is True])
ck("a NEARBY ticket id alone does NOT exonerate -- the whole point",
   [f for f in strike_findings(doc(CLAIM, "See mg-6f61.\n\n" + CLAIM))
    if f[4] is False])
ck("a ticket id in the SAME paragraph does not exonerate either",
   [f for f in strike_findings(doc(CLAIM, "mg-6f61 says " + CLAIM))
    if f[4] is False])
ck("a fenced block naming STRICKEN exonerates",
   [f for f in strike_findings(
       doc(CLAIM, "check_doc.py's STRICKEN table:\n\n```\n" + CLAIM
           + "\n```\n")) if f[4] is True])
ck("a fenced block naming NOTHING does not exonerate",
   [f for f in strike_findings(doc(CLAIM, "```\n" + CLAIM + "\n```\n"))
    if f[4] is False])

ck("NEGATES matches 'no longer holds'", NEGATES.search("it no longer holds"))
ck("NEGATES matches 'withdrawn'", NEGATES.search("WITHDRAWN"))
ck("NEGATES does not match a bare 'REPAIRED'",
   not NEGATES.search("this was REPAIRED"))
ck("NEGATES does not match a bare ticket id", not NEGATES.search("mg-a4ef"))
ck("NEGATES does not match ordinary prose",
   not NEGATES.search("the algebra of symmetric functions"))

# --- the real document ------------------------------------------------------
DOC = os.path.join(REPO, "docs",
                   "OneThird-Species-Hopf-Monoids-Where-This-Lives.md")
real = strike_findings(open(DOC, encoding="utf-8").read())
ck("the target document has at least ten strikes", len(real) >= 10)
ck("none of them stands un-struck", not [f for f in real if f[4] is False])
ck("at least one is exonerated rather than merely short",
   [f for f in real if f[4] is True])

# --- file discovery ---------------------------------------------------------
mds = md_files(os.path.join(REPO, "docs"))
ck("md_files finds the target document",
   os.path.relpath(DOC, REPO) in mds)
ck("md_files returns only .md", all(f.endswith(".md") for f in mds))
ck("md_files skips __pycache__",
   not [f for f in md_files(os.path.join(REPO, "code"))
        if "__pycache__" in f])

# --- the sandbox ------------------------------------------------------------
tmp = tempfile.mkdtemp(prefix="d633_self_")
try:
    root = sandbox(os.path.join(tmp, "repo"))
    ck("the sandbox carries docs/", os.path.isdir(os.path.join(root, "docs")))
    ck("the sandbox carries the four checked trees",
       all(os.path.isdir(os.path.join(root, "code", t))
           for t in ["species_7d75", "species_repair_6f61",
                     "species_remainder_f8fa", "species_repair_a4ef"]))
    ck("the sandbox carries run_all.sh, which the old filter dropped",
       os.path.isfile(os.path.join(root, "code", "species_7d75",
                                   "run_all.sh")))
    ck("the sandbox carries no __pycache__",
       not [d for _r, ds, _f in os.walk(root) for d in ds
            if d == "__pycache__"])
    with open(os.path.join(root, "docs", "probe.md"), "w") as fh:
        fh.write("x")
    ck("writing in the sandbox does not touch the repository",
       not os.path.exists(os.path.join(REPO, "docs", "probe.md")))
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# --- the tracer -------------------------------------------------------------
tmp = tempfile.mkdtemp(prefix="d633_trace_")
try:
    script = os.path.join(tmp, "reader.py")
    with open(script, "w") as fh:
        fh.write("open(__file__, encoding='utf-8').read()\n"
                 "open(__file__ + '.data', encoding='utf-8').read()\n")
    with open(script + ".data", "w") as fh:
        fh.write("data\n")
    rec = os.path.join(tmp, "rec.json")
    subprocess.run([sys.executable,
                    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "trace_open.py"), script],
                   env=dict(os.environ, D633_TRACE=rec),
                   capture_output=True, text=True)
    import json
    data = json.load(open(rec, encoding="utf-8"))
    ck("the tracer records a read of another file",
       script + ".data" in data["text"])
    ck("the tracer records a SELF-read as a target, not runpy's own open",
       script in data["text"])
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("selftestd633: %d assertion(s), %d failure(s)" % (n, fail))
sys.exit(1 if fail else 0)
