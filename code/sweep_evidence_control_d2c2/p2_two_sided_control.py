#!/usr/bin/env python3
"""p2 — THE TWO-SIDED CONTROL §4 DOES NOT HAVE, BUILT AND RUN.

a4_sweep.py §4 is titled "THE SWEEP'S OWN TWO-SIDED CONTROL" and it means it: seven checks,
each naming a construction whose answer is known in advance.  Three of them exercise the
`tee` detector, three the `membership` detector, one the `pipe-status` detector.

NONE OF THEM EXERCISES THE §3 EVIDENCE PROBE.

That probe is the one producing `audit.sweep_dirs_without_evidence` — the field
control_gate_724a/BASELINE.json describes as "the number that should go DOWN as the estate
is widened past these two directories, and watching it is the point of recording it."  The
one number in the sweep that is declared to be watched is produced by the one detector in
the sweep that was never required to answer a question whose answer was known.

This file builds that control.  Five directories are constructed in a sandbox, each with a
KNOWN correct answer, and the probe — imported, not copied — is run on each.  A control that
only ever fires is not a control, so two worlds must come back BARE and three must come back
EVIDENCE if the probe is right.

The probe gets two of five right.

SCORED INVERTED, AND SAID SO LOUDLY.  Exit 0 here means "the probe behaved as this transcript
records", INCLUDING the three answers that are wrong.  If a4_sweep.py is ever repaired, this
file goes RED — and that red means the defect is FIXED, not that anything broke.  Which is
precisely why this suite is not wired into ./build.sh: a gate that turns red on the day a
defect is repaired is a gate that punishes the repair.  Read the decision line, not the exit
code; the decision line says which direction the change went.
"""

import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_d2c2 as L  # noqa: E402


# --------------------------------------------------------------------------- the worlds
#
# Each world is (name, why-its-answer-is-known, correct-answer-is-bare, {filename: content}).
# "bare" means: this directory ships code and NO evidence that any of it can fail.

W_BARE_HONEST = (
    "W0  a directory that genuinely has no falsification evidence",
    "It computes a number and prints it.  Nothing in it is ever required to fail, no arm\n"
    "     is scored inverted, and no transcript records anything going red.  The correct\n"
    "     answer is BARE and a probe that cannot say BARE is not a detector.",
    True,
    {
        "compute.py": (
            '"""Sum the first n squares and print the total."""\n'
            "def total(n):\n"
            "    return sum(i * i for i in range(n))\n\n"
            'print("total(10) =", total(10))\n'
        ),
        "out_compute.txt": "total(10) = 285\n",
        "README.md": "Computes a sum.  There is no control here and none is claimed.\n",
    },
)

W_EVIDENCE_HOUSE_STYLE = (
    "W1  real evidence, written in the vocabulary the probe was built around",
    "It ships a file named `negative_control.py` and a transcript carrying a token from\n"
    "     RED_TOKENS.  This is the shape the probe was written for; the correct answer is\n"
    "     EVIDENCE and getting it right is what makes W2 and W3 below meaningful.",
    False,
    {
        "instrument.py": "def check(x):\n    return x > 0\n",
        "negative_control.py": (
            "import instrument\n"
            "assert not instrument.check(-1), 'the instrument passed a known-bad input'\n"
            'print("mutation CAUGHT")\n'
        ),
        "out_negative_control.txt": "mutation CAUGHT\n",
    },
)

W_FALSE_NEGATIVE = (
    "W2  real evidence, written in the vocabulary THIS ESTATE ACTUALLY USES NOW",
    "An arm declared [MUST FAIL], scored inverted, with a committed transcript recording\n"
    "     it firing on 9420 of 13416 inputs.  This is code/compression_novelty_623a's own\n"
    "     shape, reduced.  The correct answer is EVIDENCE.",
    False,
    {
        "a1_arms.py": (
            '"""A3/A4 assert the identity.  A5 is a CONTROL and MUST GO RED."""\n'
            "# scored INVERTED: a failure here is the control working.\n"
            "def a5_control(f):\n"
            "    return not identity_holds(f)   # [MUST FAIL] on a real statistic\n"
        ),
        "out_a1_arms.txt": (
            "  A5  CONTROL on a NON-linear statistic                [MUST FAIL]\n"
            "    A5    13416 checked,   9420 failed   FIRES   [control: failure is the pass]\n"
        ),
    },
)

W_FALSE_POSITIVE_NAME = (
    "W3  NO evidence at all, but one file is named for a control",
    "`controls.py` prints a greeting.  There is no arm, nothing is required to fail, and\n"
    "     no transcript records anything.  The correct answer is BARE.  The probe credits\n"
    "     the directory on the SUBSTRING in the filename, having never read the file.",
    True,
    {
        "controls.py": '"""Controls for the pipeline (TODO)."""\nprint("hello")\n',
        "out_controls.txt": "hello\n",
    },
)

W_FALSE_POSITIVE_TOKEN = (
    "W4  NO evidence at all, but a README uses one of the red words in prose",
    "The prose says no mutation was CAUGHT BECAUSE NONE WAS ATTEMPTED — a sentence that\n"
    "     states the absence of evidence and is scored as its presence.  The correct answer\n"
    "     is BARE.  The probe reads the token, not the sentence.",
    True,
    {
        "compute.py": "print(6 * 7)\n",
        "README.md": (
            "Status: no mutation was CAUGHT during this work, because none was attempted.\n"
            "Wiring up a negative control is left for a successor ticket.\n"
        ),
    },
)

WORLDS = [W_BARE_HONEST, W_EVIDENCE_HOUSE_STYLE, W_FALSE_NEGATIVE,
          W_FALSE_POSITIVE_NAME, W_FALSE_POSITIVE_TOKEN]


def build(sandbox, files):
    path = os.path.join(sandbox, "world")
    os.makedirs(path)
    for name, content in files.items():
        with open(os.path.join(path, name), "w", encoding="utf-8") as fh:
            fh.write(content)
    return path


def main():
    print("=" * 92)
    print("mg-d2c2 §2 — THE CONTROL a4_sweep.py §4 DOES NOT HAVE")
    print("=" * 92)
    print()
    print("  a4_sweep.py §4 runs 7 checks with known answers:")
    print("      3 on the `tee` detector, 3 on `membership`, 1 on `pipe-status`.")
    print("      0 on the §3 evidence probe.")
    print()
    print("  The §3 evidence probe is the one that produces")
    print("  `audit.sweep_dirs_without_evidence`, which BASELINE.json calls \"the number")
    print("  that should go DOWN ... and watching it is the point of recording it\".")
    print("  The one number declared to be watched comes from the one detector never")
    print("  shown to answer a question whose answer was known.")
    print()

    sandbox = tempfile.mkdtemp(prefix="d2c2-worlds-")
    results = []
    try:
        for title, why, correct_bare, files in WORLDS:
            path = build(os.path.join(sandbox, title.split()[0]), files)
            got_bare, why_probe = L.probe(path)
            right = (got_bare == correct_bare)
            results.append((title, why, correct_bare, got_bare, right, why_probe))
            shutil.rmtree(os.path.dirname(path))
    finally:
        shutil.rmtree(sandbox, ignore_errors=True)

    def word(b):
        return "BARE" if b else "EVIDENCE"

    for title, why, correct, got, right, wp in results:
        print("-" * 92)
        print(f"  {title}")
        print(f"     {why}")
        print()
        print(f"     ships          : {', '.join(sorted(wp['sources'] + wp['transcripts']))}")
        print(f"     correct answer : {word(correct)}")
        print(f"     probe answers  : {word(got)}")
        if wp["filename_probe_hits"]:
            print(f"       filename probe fired on : {wp['filename_probe_hits']}")
        if wp["token_probe_hits"]:
            print(f"       token probe fired on    : "
                  f"{[f'{f}: {t}' for f, t in wp['token_probe_hits']]}")
        if not wp["filename_probe_hits"] and not wp["token_probe_hits"]:
            print("       neither probe fired")
        kind = ""
        if not right:
            kind = " — FALSE NEGATIVE" if correct is False else " — FALSE POSITIVE"
        print(f"     [{'PASS' if right else 'FAIL'}]{kind}")
        print()

    n_right = sum(1 for r in results if r[4])
    n_wrong = len(results) - n_right
    false_neg = [r[0].split()[0] for r in results if not r[4] and r[2] is False]
    false_pos = [r[0].split()[0] for r in results if not r[4] and r[2] is True]
    answered_both_ways = len({r[3] for r in results}) == 2

    print("-" * 92)
    print("  WHAT THIS CONTROL ESTABLISHES")
    print("-" * 92)
    print(f"    the probe answered both ways at all           : {answered_both_ways}")
    print(f"    correct answers                               : {n_right} of {len(results)}")
    print(f"    wrong answers                                 : {n_wrong} of {len(results)}")
    print(f"      false NEGATIVE (real evidence, called bare) : "
          f"{', '.join(false_neg) or '(none)'}")
    print(f"      false POSITIVE (no evidence, credited)      : "
          f"{', '.join(false_pos) or '(none)'}")
    print()
    print("    Answering both ways is what §4 demands of the other three detectors, and")
    print("    this one does answer both ways.  It is still wrong three times out of five,")
    print("    because BOTH of its halves test VOCABULARY: one matches substrings in")
    print("    filenames, the other matches six words in prose.  Neither has read an arm,")
    print("    run one, or asked whether anything in the directory is required to fail.")
    print()

    # ------------------------------------------------------------------ the expectation
    EXPECTED = {"correct": 2, "wrong": 3, "false_neg": ["W2"], "false_pos": ["W3", "W4"]}
    matches = (n_right == EXPECTED["correct"] and n_wrong == EXPECTED["wrong"]
               and false_neg == EXPECTED["false_neg"] and false_pos == EXPECTED["false_pos"])

    print("=" * 92)
    if matches:
        print(f"P2 CONTROL — AS RECORDED: the evidence probe answers both ways and is wrong "
              f"{n_wrong} of {len(results)} times "
              f"(false negative {', '.join(false_neg)}; false positive {', '.join(false_pos)}).")
        print("=" * 92)
        return 0
    print(f"P2 CONTROL — CHANGED: the probe now scores {n_right} of {len(results)}, not "
          f"{EXPECTED['correct']} of {len(results)}.")
    print("  This file is SCORED INVERTED.  A change here is most likely a4_sweep.py's §3")
    print("  probe being REPAIRED, in which case this transcript is stale and the repair is")
    print("  the good news.  Re-read the five worlds above before treating it as a break.")
    print("=" * 92)
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except L.Refused as exc:
        print()
        print("=" * 92)
        print(f"P2 CONTROL — REFUSED: {exc}")
        print("=" * 92)
        sys.exit(2)
