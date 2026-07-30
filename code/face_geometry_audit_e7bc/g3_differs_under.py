"""mg-e7bc G3 -- THE "WOULD DIFFER UNDER" STATEMENTS, AUDITED AS CLAIMS.

mg-d0e2 attached a requirement to its repair: every check must state IN THE CODE
what change would alter its answer.  mg-04a8 implemented it as a required
argument to `claim()`, so the transcript now carries a `WOULD DIFFER UNDER` line
under every scored claim.

AN UNMEASURED "DIFFERS UNDER X" IS THE SAME DEFECT ONE LEVEL UP: a claim about a
check, asserted rather than tested.  So this file takes the statements and MAKES
THE CHANGE.  Five are tested, chosen because each is load-bearing on the
repair's own account of itself; the population they are drawn from is counted
below rather than left as "the statements".

AND OF EACH, THE SECOND QUESTION THE TICKET ASKS: is X actually the failure the
check guards against, or merely some change it happens to notice?  A statement
naming a change that would break the check but is not the failure it exists for
is a true sentence doing no work.  That judgement is printed per statement.

PREDICTIONS REGISTERED BEFORE THE RUNS.  One missed and is kept.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kerne7bc import (ART, BAR, BRUTEFORCE_TO_SELF, DEL_PARITY,       # noqa: E402
                      DEL_SHAPE, FC, FINDINGS, HERE, INSTR, ROOT, SCORE,
                      SHAPE_1, claim, finding, head, read, retag_rows,
                      run_battery, scored_rows)

sys.path.insert(0, INSTR)
import d2_deletion as SUBJ                                            # noqa: E402

D2 = read(os.path.join(INSTR, "d2_deletion.py"))
TRANSCRIPTS = ["out_d1_trace.txt", "out_d2_deletion.txt",
               "out_d3_reintroduction.txt", "out_d4_auditor_rerun.txt"]

# (tag, the statement being tested, the change made, predicted verdict)
# "CONFIRMED" = making the change does alter the answer.
# "REFUTED"   = the answer does not move under the change the statement names.
PREDICTIONS = [
    ("S1", "run_case: 'deleting a gate that no row's answer depends on'",
     "delete a gate no row's answer depends on, under a BYTE-IDENTICAL "
     "prediction", "REFUTED"),
    ("S2", "positive control: 'the repaired check reverting to a comparison "
     "against the baseline's own labels'",
     "revert check_labels to the baseline-label comparison", "CONFIRMED"),
    ("S3", "positive control: '...or to a substring row scan'",
     "revert scored_rows to the shipped substring scan", "REFUTED"),
    ("S4", "the shipped check: 'nothing available to a corruption of the "
     "artifact'",
     "delete one scored row line; and un-indent one scored row", "REFUTED"),
    ("S5", "AFTER-5/6 and d4: 'its expected value being taken from the "
     "predicate rather than from absorbable_bruteforce'",
     "replace absorbable_bruteforce(A, B) with the predicate's own answer, "
     "then delete the shape and parity gates", "REFUTED"),
]


def substring_rows(text):
    """The shipped row scan: any line CONTAINING a marker is a row."""
    out = []
    for ln in text.split("\n"):
        for m in ("[CANNOT FAIL]", "[PASS]", "[FAIL]"):
            if m in ln:
                out.append((m, ln.split(m, 1)[1].strip()))
                break
    return out


def baseline_label_check(base_text, mut_text):
    """The SHIPPED semantics with the parsing bug fixed: compare the mutant's
    labels against the BASELINE's, row for row.  This is the reversion S2
    names -- stability, correctly parsed."""
    a = [m for m, _ in scored_rows(base_text)]
    b = [m for m, _ in scored_rows(mut_text)]
    return len(a) == len(b) and a == b


def shipped_holds(base_text, mut_text):
    def rows(t):
        return [l for l in t.split("\n")
                if "[PASS]" in l or "[CANNOT FAIL]" in l or "[FAIL]" in l]
    a, b = rows(base_text), rows(mut_text)
    return len(a) == len(b) and all(x.split(" ")[1] == y.split(" ")[1]
                                    for x, y in zip(a, b))


def main():
    print(BAR)
    print("mg-e7bc G3 -- the WOULD DIFFER UNDER statements, tested by making "
          "the change")
    print(BAR)

    head("THE POPULATION -- how many claims carry a statement, and how many "
         "do not")
    print("   %-24s %8s %10s   %s"
          % ("script", "claims", "statements", "claim() signature"))
    counts, total, claims_total, uncovered = [], 0, 0, []
    for t in TRANSCRIPTS:
        txt = read(os.path.join(INSTR, t))
        src = read(os.path.join(INSTR, t.replace("out_", "").replace(".txt",
                                                                    ".py")))
        n = txt.count("WOULD DIFFER UNDER:")
        m = re.search(r"^(\d+) claim\(s\) scored", txt, re.M)
        c = int(m.group(1)) if m else 0
        has = "differs_under" in re.search(r"^def claim\(.*", src,
                                           re.M).group(0)
        counts.append((t, c, n, has))
        total += n
        claims_total += c
        if not has:
            uncovered.append((t, c))
        print("   %-24s %8d %10d   %s"
              % (t, c, n, "requires differs_under" if has
                 else "NO differs_under parameter"))
    print("   %-24s %8d %10d" % ("TOTAL", claims_total, total))
    claim(total == 34 and claims_total == 56,
          "the repair's instrument scores %d claims across four scripts and "
          "%d of them carry a WOULD DIFFER UNDER statement" % (claims_total,
                                                               total),
          "a claim being added to d1 or d3, which would widen the gap, or "
          "either of them gaining the parameter, which would close it",
          "counts read from the committed transcripts' own bottom lines, not "
          "from run_all.sh's summary")
    claim("def claim(text, ok, differs_under, detail=\"\")" in D2,
          "and in d2_deletion.py it is a REQUIRED argument with no default, so "
          "a claim cannot be written there without one",
          "a default appearing in the signature, which is how a required field "
          "quietly becomes optional")
    finding(bool(uncovered),
            "THE REQUIREMENT IS IMPLEMENTED IN 2 OF THE 4 SCRIPTS, covering %d "
            "of the instrument's %d claims.  %s carry none at all -- their "
            "`claim()` is still `def claim(text, ok, detail=\"\")`.  This is "
            "not an oversight of scope: d1_trace.py WAS edited by this same "
            "commit (15 lines, the pre-repair pin), and the one differs-under "
            "sentence it gained was written into a CODE COMMENT -- 'ITS ANSWER "
            "WOULD DIFFER UNDER: any edit to `absorb_trace` that changes a "
            "decision on the 516 pairs below' -- where the transcript a reader "
            "checks does not carry it.  mg-d0e2's requirement was that each "
            "check state it IN THE CODE; the repair's own framing is that the "
            "transcript should carry it ('so the transcript carries it'), and "
            "for %d claims it does not"
            % (total, claims_total,
               " and ".join("%s (%d claims)" % (t, c) for t, c in uncovered),
               claims_total - total))

    print("\nPREDICTIONS, registered before the runs:")
    for tag, stmt, change, pred in PREDICTIONS:
        print("   %-3s %-72s %s" % (tag, stmt[:72], pred))
    observed = {}

    clean = read(ART)
    broken = read(os.path.join(INSTR, "positive_control_all_fail.txt"))
    cannot = SUBJ.summary_block(clean)[1]

    # ------------------------------------------------------------------- S1
    head("S1 -- the statement `run_case` prints under EVERY one of its 8 cases")
    print("The string is a literal in `run_case`, so all eight byte-comparison")
    print("claims carry the same sentence.  For the six cases predicting")
    print("CHANGES it is right.  BEFORE-1 predicts BYTE-IDENTICAL, and for it")
    print("the sentence names the state of affairs under which the claim")
    print("HOLDS.  Tested by making the change on THIS tree: E1* from G2 is a")
    print("gate whose deletion no row's answer depends on.\n")
    lit = ("deleting a gate that no row's answer depends on -- which is what "
           "AFTER-5 and AFTER-6 used to be, and what BEFORE-1 still is")
    uses = read(os.path.join(INSTR, "out_d2_deletion.txt")).count(lit)
    base, base_code = run_battery({}, "s1base")
    out, code = run_battery({FC: SHAPE_1}, "s1")
    changed = out != base
    # The claim's own arithmetic, under a BYTE-IDENTICAL prediction:
    answer_before = (False == False) and (code == 0)          # noqa: E712
    answer_after = (changed == False) and (code == 0)         # noqa: E712
    observed["S1"] = "CONFIRMED" if answer_before != answer_after else "REFUTED"
    print("   the literal appears %d time(s) in out_d2_deletion.txt" % uses)
    print("   change made: delete `if m != len(B): return Trace(False, "
          "\"shape\", 0)`")
    print("   result: artifact %s, exit %d; a claim predicting BYTE-IDENTICAL "
          "still %s" % ("CHANGED" if changed else "BYTE-IDENTICAL", code,
                        "HOLDS" if answer_after else "goes BROKEN"))
    claim(uses == 8,
          "the sentence is one literal shared by all %d of `run_case`'s "
          "byte-comparison claims -- it is not derived from the case" % uses,
          "`run_case` computing the statement from `want_change`, which is the "
          "one input that decides whether the named change would break the "
          "claim or make it")
    finding(answer_after,
            "AN UNMEASURED 'DIFFERS UNDER' THAT IS INVERTED FOR ONE OF ITS 8 "
            "USES.  `run_case` prints the same sentence under every case, and "
            "for BEFORE-1 -- the one case whose registered prediction is "
            "BYTE-IDENTICAL -- 'deleting a gate that no row's answer depends "
            "on' is precisely what makes the claim HOLD, not what would make "
            "it differ.  Measured on this tree by making the change: deleting "
            "the first `shape` return is a gate no row's answer depends on, "
            "the artifact stays byte-identical at %d bytes, exit %d, and a "
            "claim predicting BYTE-IDENTICAL still HOLDS.  The sentence is "
            "correct for the other 7 uses; the requirement is 'state what "
            "would alter THIS answer', and a constant cannot" % (len(out), code))
    print("   IS X THE FAILURE THE CHECK GUARDS AGAINST?  For AFTER-1..6 and "
          "BEFORE-2, yes:\n   a gate going dead is exactly what the deletion "
          "test exists to catch.  For BEFORE-1 it is\n   the experiment "
          "itself.")

    # ------------------------------------------------------------------- S2
    head("S2 -- 'the repaired check reverting to a comparison against the "
         "baseline's own labels'")
    print("Predicted CONFIRMED.  It is not, and the miss is the finding.  Three")
    print("inputs are needed to say what the reversion does and does not do.\n")
    red_now = not SUBJ.check_labels("pc", broken, 0, [], cannot)[0]
    reverted_on_broken = baseline_label_check(clean, broken)
    shipped_on_broken = shipped_holds(clean, broken)
    # THE WRONG-BUT-STABLE INPUT, which is the case mg-04a8's prose is about: a
    # row that was PREDICTED to break and did not.  Every label equals the
    # baseline's, so a stability comparison says yes whatever the registration.
    stable_registered = ["I4 the facet enumeration"]
    red_repaired_stable = not SUBJ.check_labels(
        "stable", clean, 0, stable_registered, cannot)[0]
    green_reverted_stable = baseline_label_check(clean, clean)
    observed["S2"] = ("CONFIRMED" if (red_now and reverted_on_broken)
                      else "REFUTED")
    print("   input 1 -- the all-[FAIL] artifact, which is the claim this")
    print("             statement is attached to:")
    print("       as repaired by mg-04a8:                 %s"
          % ("RED" if red_now else "green"))
    print("       reverted to the baseline comparison:    %s"
          % ("RED -- the answer does NOT differ" if not reverted_on_broken
             else "green"))
    print("       reverted to the SHIPPED check entire:   %s"
          % ("green -- and THIS is what flips it" if shipped_on_broken
             else "RED"))
    print("   input 2 -- the wrong-but-stable case: a row registered as failing")
    print("             that did not fail, labels identical to the baseline's:")
    print("       as repaired by mg-04a8:                 %s"
          % ("RED" if red_repaired_stable else "green"))
    print("       reverted to the baseline comparison:    %s"
          % ("green -- the answer DOES differ here" if green_reverted_stable
             else "RED"))
    claim(red_now and not reverted_on_broken and shipped_on_broken
          and red_repaired_stable and green_reverted_stable,
          "MEASURED, AGAINST THE PREDICTION: the reversion the statement names "
          "does NOT change the answer on the artifact the claim is about -- a "
          "correctly-parsed baseline comparison also goes RED on the all-"
          "[FAIL] flip, because every label moved.  What restores green there "
          "is the shipped `a.split(' ')[1]` token, which this statement does "
          "not name.  On the wrong-but-stable input the reversion DOES change "
          "the answer, from RED to green",
          "the baseline acquiring a [FAIL] row, which would make the all-"
          "[FAIL] flip a stable relabelling instead of a moving one",
          "this claim scores the four measurements above, not the prediction")
    finding(not reverted_on_broken,
            "THE DIFFERS-UNDER ON THE POSITIVE-CONTROL CLAIM NAMES A REVERSION "
            "THAT DOES NOT MOVE IT.  'The repaired check reverting to a "
            "comparison against the baseline's own labels' is attached to the "
            "claim 'THE REPAIRED CHECK ON THE SAME ARTIFACT GOES RED'.  Made: "
            "a baseline-label comparison ALSO goes red on that artifact -- all "
            "43 labels moved, so stability is exactly what it does not have.  "
            "The reversion that restores green is the shipped token bug, which "
            "the sentence does not mention.  The statement is right about "
            "WHICH SEMANTICS is the defect and mg-04a8's prose is right that "
            "'stability is what a wrong label has too' -- measured here on the "
            "wrong-but-stable input, where the reversion does flip the answer "
            "from RED to green.  But it is attached to the one claim whose "
            "input it cannot move, so the transcript reads as though the "
            "positive control tests the stability semantics, and it does not: "
            "mg-04a8's own c2 control does")

    # ------------------------------------------------------------------- S3
    head("S3 -- '...or to a substring row scan'")
    real = SUBJ.scored_rows
    try:
        SUBJ.scored_rows = substring_rows
        red_substr = not SUBJ.check_labels("pc", broken, 0, [], cannot)[0]
        green_clean = SUBJ.check_labels("clean", clean, 0, [], cannot)[0]
    finally:
        SUBJ.scored_rows = real
    observed["S3"] = "REFUTED" if red_substr else "CONFIRMED"
    print("   with `scored_rows` replaced by the shipped substring scan:")
    print("     on the broken artifact:   %s (%d 'rows' seen)"
          % ("RED" if red_substr else "GREEN",
             len(substring_rows(broken))))
    print("     on the clean artifact:    %s"
          % ("green" if green_clean else "RED"))
    finding(red_substr,
            "A 'DIFFERS UNDER' THAT DOES NOT.  The positive-control claim says "
            "its answer would differ if the repaired check reverted 'to a "
            "substring row scan'.  Made: with `scored_rows` replaced by the "
            "shipped substring selection, the check STILL GOES RED on the "
            "broken artifact -- the %d lines it then treats as rows include "
            "the %d prose bullets, and the label mismatch on the real rows is "
            "untouched.  The row scan is what fixed the published COUNT "
            "(mg-d0e2's F3, 43 vs 41); it is not what makes the check "
            "non-vacuous.  The two repairs are named in one sentence as though "
            "either alone would restore the defect, and only the first would"
            % (len(substring_rows(broken)),
               len(substring_rows(broken)) - len(scored_rows(broken))))
    print("   IS X THE FAILURE THE CHECK GUARDS AGAINST?  No -- it is a change "
          "the check\n   happens to survive.  The failure is the stability "
          "comparison, which is S2.")

    # ------------------------------------------------------------------- S4
    head("S4 -- the shipped check: 'nothing available to a corruption of the "
         "artifact'")
    rows = scored_rows(clean)
    lines = clean.split("\n")
    idx = [i for i, ln in enumerate(lines)
           if ln.strip().startswith("[PASS]")][0]
    dropped = "\n".join(lines[:idx] + lines[idx + 1:])
    unindented = "\n".join(lines[:idx] + [lines[idx].strip()]
                           + lines[idx + 1:])
    flipped = retag_rows(clean, "[FAIL]")
    trials = [("every row flipped to [FAIL]", flipped),
              ("one scored row LINE deleted", dropped),
              ("one scored row UN-INDENTED", unindented)]
    movers = []
    for what, text in trials:
        h = shipped_holds(clean, text)
        print("   %-32s shipped check %s" % (what, "HOLDS" if h else "GOES RED"))
        if not h:
            movers.append(what)
    observed["S4"] = "REFUTED" if movers else "CONFIRMED"
    finding(bool(movers),
            "'NOTHING AVAILABLE' IS TOO WIDE BY %d CORRUPTIONS.  mg-04a8 "
            "scores the shipped check's vacuity TRUE -- correctly -- and "
            "states its answer would differ under 'nothing available to a "
            "corruption of the artifact ... its answer is fixed by the "
            "INDENTATION and cannot depend on any label'.  The second half is "
            "exactly right and is the finding.  The first half is refuted by "
            "%s: the shipped check also compares ROW COUNTS, so a corruption "
            "that removes a marker-bearing line moves its answer without "
            "touching a label.  Scope, stated the way the sentence should "
            "have been: nothing available to a corruption that PRESERVES the "
            "set of marker-bearing lines and their indentation"
            % (len(movers), " and ".join(movers)))
    print("   IS X THE FAILURE THE CHECK GUARDS AGAINST?  The statement's job "
          "here is the\n   opposite -- to admit the check guards against "
          "nothing.  It overshoots by one class.")

    # ------------------------------------------------------------------- S5
    head("S5 -- 'its expected value being taken from the predicate rather than "
         "from absorbable_bruteforce'")
    print("This is the crux of the whole repair, and both `d2_deletion.py` and")
    print("`d4_auditor_rerun.py` say the change would put the two branches back")
    print("out of reach.  Made: `truth = absorbable_bruteforce(A, B)` becomes")
    print("`truth = tr.absorbable`.\n")
    alone, alone_code = run_battery({FC: [], "controls.py": BRUTEFORCE_TO_SELF},
                                    "s5alone")
    with_shape, shape_code = run_battery(
        {FC: DEL_SHAPE, "controls.py": BRUTEFORCE_TO_SELF}, "s5shape")
    with_parity, parity_code = run_battery(
        {FC: DEL_PARITY, "controls.py": BRUTEFORCE_TO_SELF}, "s5parity")
    still_bites = (with_shape != alone and shape_code == 1
                   and with_parity != alone and parity_code == 1)
    observed["S5"] = "REFUTED" if still_bites else "CONFIRMED"
    print("   the substitution ALONE:                artifact %s, exit %d"
          % ("CHANGED" if alone != base else "BYTE-IDENTICAL", alone_code))
    print("   substitution + delete `shape`:         artifact %s, exit %d"
          % ("CHANGED" if with_shape != alone else "BYTE-IDENTICAL", shape_code))
    print("   substitution + delete `parity`:        artifact %s, exit %d"
          % ("CHANGED" if with_parity != alone else "BYTE-IDENTICAL",
             parity_code))
    claim(alone == base and alone_code == 0,
          "the substitution alone leaves the artifact BYTE-IDENTICAL and exits "
          "0 -- on an unmutated predicate the two expected values agree, which "
          "is why nothing in the battery notices the difference until a gate "
          "goes",
          "the predicate disagreeing with the definition on one of the five "
          "constructed pairs, which is the state the row exists to detect")
    finding(still_bites,
            "THE NAMED CHANGE DOES NOT RESTORE THE DEFECT, and the statement "
            "says it would.  With the expected value taken from the predicate "
            "itself, deleting the `shape` gate still CHANGES the artifact "
            "(exit %d) and deleting the `parity` branch still does (exit %d).  "
            "Cause, measured: each row scores THREE things, not one -- "
            "agreement with brute force, agreement with the answer REGISTERED "
            "beside each pair before the run, and that the rejected pairs "
            "return at the named gate.  Killing the brute-force channel leaves "
            "the registered channel, and the registered answers are literals "
            "in `UNREACHED_GATE_PAIRS` that no mutation of the predicate can "
            "move.  The repair is therefore MORE robust than its own statement "
            "claims -- but the statement is still an untested assertion about "
            "a check, which is the defect one level up that this ticket names, "
            "and it appears in the transcript of `d4_auditor_rerun.py` as the "
            "sole differs-under of its headline 9-of-9 claim"
            % (shape_code, parity_code))
    print("   IS X THE FAILURE THE CHECK GUARDS AGAINST?  Yes in kind -- an "
          "expected value\n   copied from the subject is the defect mg-d0e2 "
          "named -- but not in fact: here it\n   is not sufficient to cause "
          "the failure the sentence attributes to it.")

    head("SCORE ON THE FIVE STATEMENTS")
    print("   %-3s %-10s %-10s %s" % ("tag", "predicted", "observed", "verdict"))
    n_ok = 0
    for tag, _s, _c, pred in PREDICTIONS:
        got = observed[tag]
        n_ok += got == pred
        print("   %-3s %-10s %-10s %s"
              % (tag, pred, got, "MATCH" if got == pred else "*** MISS ***"))
    print("\n   %d of %d predictions matched.  Of the five statements, %d were "
          "CONFIRMED\n   by making the change and %d were REFUTED."
          % (n_ok, len(PREDICTIONS),
             sum(1 for v in observed.values() if v == "CONFIRMED"),
             sum(1 for v in observed.values() if v == "REFUTED")))
    print("   THE MISS IS KEPT: S2 was predicted CONFIRMED on the reasoning "
          "that a stability\n   comparison passes an all-[FAIL] flip.  It does "
          "not -- the flip moves every label.\n   The prediction confused the "
          "shipped check's PARSING BUG with its SEMANTICS, which\n   is the "
          "same conflation mg-04a8's own commit message warns against, made "
          "here by\n   this audit and caught by running it.")
    print("   Population: %d WOULD DIFFER UNDER statements across the four "
          "transcripts;\n   five tested, chosen for being load-bearing on the "
          "repair's account of itself." % total)

    print("\n" + BAR)
    print("%d claim(s) scored; %d BROKEN.  %d FINDING(s)."
          % (len(SCORE), SCORE.count(False), len(FINDINGS)))
    for f in FINDINGS:
        print("  FINDING: %s" % f)
    print(BAR)
    return 1 if not all(SCORE) else 0


if __name__ == "__main__":
    sys.exit(main())
