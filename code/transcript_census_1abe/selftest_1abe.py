"""selftest_1abe -- the controls on THIS census's own instruments.

Every check here is about `lib_1abe`, not about the arc.  A FINDING in this
file means the census's own machinery is wrong and every number it prints is
suspect; a FINDING in t1-t6 means the arc has something to answer for.  The
exit codes are kept separate for that reason.

The four instruments that need controlling, and why each could be wrong in a
way that would change the answer:

  parse_producers   if it silently failed on a runner form, transcripts would
                    land in CANNOT-BE-RUN and the blast radius would look
                    smaller than it is.  Four forms live in this repo and all
                    four are exercised on synthetic input.
  conclusion_verdict  if it could not tell a changed DECISION from a changed
                    FIGURE INSIDE a decision, the ticket's step 2 would be
                    unanswerable.  Both directions are constructed.
  code_digest       the convention in t5 stands or falls on the digest being
                    INSENSITIVE to committing a transcript and SENSITIVE to a
                    code change.  Both are tested against real commits.
  patch-id/ancestry  the census's central methodological claim.  Tested on a
                    real pair where the two instruments are known to disagree.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_1abe as L                                          # noqa: E402

STRAIGHT = """#!/bin/sh
python3 -u check_bridge.py > out_bridge.txt
python3 verify.py > out_verify.txt || { echo FAILED; exit 1; }
"""

LOOP = """#!/bin/sh
for s in c1_rebase c2_anchors selftest_c067; do
    python3 "$s.py" "$@" > "out_$s.txt" 2>&1 || status=$?
done
"""

FUNC_DOTSTAR = """#!/bin/sh
run() {
    python3 -u "$1" > "out_${1%.*}.txt" 2>&1
}
run selftest_330a.py
run s1_anchors.py
"""

FUNC_NAMED = """#!/bin/sh
run() {
    name="$1"
    python3 -W ignore "$name" > "out_${name%.py}.txt" 2>&1
}
run q1_reason.py
"""

TRANSCRIPT_A = """
header 540 files
[OK       ] C1 the population is 528 files
[FINDING  ] C2 three anchors disagree
TOTAL BAD: 1
"""

TRANSCRIPT_FIGURE_MOVED = """
header 673 files
[OK       ] C1 the population is 540 files
[FINDING  ] C2 three anchors disagree
TOTAL BAD: 1
"""

TRANSCRIPT_DECISION_FLIPPED = """
header 540 files
[FINDING  ] C1 the population is 528 files
[FINDING  ] C2 three anchors disagree
TOTAL BAD: 2
"""

TRANSCRIPT_PROSE_ONLY = """
header 540 files
[OK       ] C1 the population is 528 files
[FINDING  ] C2 three anchors disagree
TOTAL BAD: 1
and one more line of prose
"""


def main():
    led = L.Ledger("selftest_1abe -- the controls on this census's own "
                   "instruments", reads_outside_tree=True)
    rev = L.main_rev()

    # ------------------------------------------------------ parse_producers
    led.head("S1 -- parse_producers ON ALL FOUR RUNNER FORMS IN THIS REPO")
    cases = [
        ("straight-line redirection", STRAIGHT,
         {"out_bridge.txt": "check_bridge.py",
          "out_verify.txt": "verify.py"}),
        ("`for s in ...` loop", LOOP,
         {"out_c1_rebase.txt": "c1_rebase.py",
          "out_c2_anchors.txt": "c2_anchors.py",
          "out_selftest_c067.txt": "selftest_c067.py"}),
        ("run() helper with ${1%.*}", FUNC_DOTSTAR,
         {"out_selftest_330a.txt": "selftest_330a.py",
          "out_s1_anchors.txt": "s1_anchors.py"}),
        ("run() helper via name=\"$1\" and ${name%.py}", FUNC_NAMED,
         {"out_q1_reason.txt": "q1_reason.py"}),
    ]
    for label, text, expect in cases:
        got = L.parse_producers(text)
        ok = True
        for out, script in expect.items():
            spec = got.get(out)
            if spec is None or script not in spec["cmd"]:
                ok = False
        led.record(ok, "S1 %s: %d of %d expected transcripts resolved to "
                       "their script"
                   % (label,
                      sum(1 for o, s in expect.items()
                          if got.get(o) and s in got[o]["cmd"]),
                      len(expect)))
    led.record("$" not in "".join(L.parse_producers(FUNC_DOTSTAR)),
               "S1' no unexpanded `$` survives into a transcript NAME; an "
               "unexpanded template would silently match no file and read as "
               "CANNOT-BE-RUN")

    # --------------------------------------------------- conclusion_verdict
    led.head("S2 -- conclusion_verdict TELLS A CHANGED DECISION FROM A "
             "CHANGED FIGURE")
    led.record(L.conclusion_verdict(TRANSCRIPT_A, TRANSCRIPT_A) == "HELD",
               "S2 identical transcripts read HELD")
    led.record(L.conclusion_verdict(TRANSCRIPT_A, TRANSCRIPT_PROSE_ONLY)
               == "HELD",
               "S2' a changed line that is NOT a decision reads HELD: prose "
               "moving is not a conclusion changing")
    led.record(L.conclusion_verdict(TRANSCRIPT_A, TRANSCRIPT_FIGURE_MOVED)
               == "HELD-DRIFTED",
               "S2'' a count moving INSIDE an `[OK]` reads HELD-DRIFTED -- the "
               "verdict stands and a stated number does not.  THIS IS THE ROW "
               "THE FIRST VERSION OF THIS CENSUS GOT WRONG: it compared whole "
               "lines and called this a flip, which would have reported five "
               "of mg-c067's six transcripts as false records")
    led.record(L.conclusion_verdict(TRANSCRIPT_A, TRANSCRIPT_DECISION_FLIPPED)
               == "FLIPS",
               "S2''' `[OK]` becoming `[FINDING]` reads FLIPS")
    led.record(L.conclusion_verdict("no verdicts here", "none here either")
               == "NO-VERDICT",
               "S2'''' a transcript with no decision rows reads NO-VERDICT "
               "rather than HELD; `I cannot tell` must not be spelled the same "
               "way as `it is fine`")

    # ------------------------------------------------------- code_digest
    led.head("S3 -- THE CONVENTION'S DIGEST: BLIND TO PUBLISHING, ALIVE TO "
             "CODE")
    d = "code/audit_c067"
    hist = L.git("log", "--format=%H", rev, "--", d).split()
    pub_pairs, code_pairs = [], []
    for c in hist[:40]:
        par = L.git("rev-parse", "%s^" % c).strip()
        if not par or L.blob_at(par, d + "/run_all.sh") is None:
            continue
        touched = [t for t in L.git("show", "--name-only", "--format=", c)
                   .split("\n") if t.startswith(d + "/")]
        code = [t for t in touched if t.endswith(L.CODE_SUFFIXES)]
        outs = [t for t in touched
                if os.path.basename(t).startswith("out_")]
        if outs and not code:
            pub_pairs.append((par, c))
        if code:
            code_pairs.append((par, c))
    if pub_pairs:
        par, c = pub_pairs[0]
        led.record(L.code_digest(d, par) == L.code_digest(d, c),
                   "S3 a commit that changes ONLY transcripts in %s (%s) "
                   "leaves the code-digest unchanged.  Without this the "
                   "declaration would be stale the instant it was committed, "
                   "which is mg-bf79's `a publisher is not a pin`"
                   % (d, c[:7]))
    else:
        led.record(None, "S3 no transcript-only commit found in the last 40 "
                         "touching %s; this control did not run" % d)
    if code_pairs:
        par, c = code_pairs[0]
        led.record(L.code_digest(d, par) != L.code_digest(d, c),
                   "S3' and a commit that DOES change code in %s (%s) moves "
                   "the digest.  Both answers, so the digest is a check rather "
                   "than a constant" % (d, c[:7]))
    else:
        led.self_error("S3' no code-touching commit found; the digest was "
                       "never shown able to change")

    # ---------------------------------------------------- patch-id/ancestry
    led.head("S4 -- THE CENSUS'S CENTRAL METHODOLOGICAL CLAIM, ON A REAL PAIR")
    a, b = L.resolve("72e36cb"), L.resolve("9c54a99")
    head = L.resolve(rev)
    if not a or not b:
        led.record(None, "S4 mg-f3ff's pair is not in this object store; the "
                         "control did not run")
    else:
        led.record(not L.is_ancestor(a, head),
                   "S4 ancestry says 72e36cb is NOT on %s" % rev)
        led.record(L.patch_id(a) == L.patch_id(b),
                   "S4' patch-id says its content IS on %s, identically, as "
                   "9c54a99.  The two instruments disagree on the same commit "
                   "and this census is built on the second" % rev)

    # -------------------------------------------------- population boundary
    led.head("S5 -- THE POPULATION REGEX DOES NOT WANDER")
    pop = L.transcripts(rev)
    bad = [p for p in pop if p.count("/") != 2 or
           not os.path.basename(p).startswith("out_")]
    led.record(not bad,
               "S5 all %d members of the CLASS 2 population are exactly "
               "`code/<one-dir>/out_*.txt`; %d are not" % (len(pop), len(bad)))
    for p in bad[:20]:
        print("      OUTSIDE THE SHAPE %s" % p)

    return led.done()


if __name__ == "__main__":
    sys.exit(main())
