#!/usr/bin/env python3
"""mg-e331 §4 — THE POSITIVE CONTROL.  Demonstrate the ratchet FAILS before trusting that it
passes.

The ticket's fourth requirement, in its own words: "A RATCHET NEEDS A POSITIVE CONTROL.
Demonstrate it FAILS on a commit that exceeds the threshold before trusting that it passes.
An unfalsified ratchet is a decorative check, and this ticket is about exactly the failure of
believing in an unexercised mechanism."

SO NOTHING HERE IS SYNTHETIC.  Every arm plants a STATE.md that a real commit of this
repository really contained, and runs the REAL `ratchet.py` — as a SUBPROCESS, never
imported, because importing a rule is one refactor away from re-specifying it — reading its
exit code AND its decision line.  mg-2ff6 established the subprocess discipline here after
cfd9c's checker was respecified once already; this arm keeps it.

HOW A TREE IS PLANTED.  `ratchet.py` derives its root from its own `__file__`, so copying
this directory into `<tmp>/code/state_ratchet_e331/` and writing `<tmp>/STATE.md` gives the
unmodified script a different subject with no parameter, no environment variable and no
`--state-path` flag.  A flag would be a way to make the gate read something other than
STATE.md, which is a way to gate less (mg-724a's D4), so there is not one.

ARMS
  X1  the pre-restructure file (b80dea0e, 29,094 w)     must exit 1, ABOVE-CEILING
  X2  mg-ea0e's own landing   (cc4c663e,  4,658 w)      must exit 1, SLACK-UNRATCHETED
  X3  the tree as it stands                             must exit 0, GREEN  (not red on arrival)
  X4  a CEILING.json that does not parse                must exit 2, REFUSED
  X5  THE COUNTERFACTUAL: the ratchet set to mg-ea0e's landed 4,658 words on 2026-08-06,
      run against every STATE.md that landed after it.  This is the arm that answers the
      question the ticket is really asking — would this mechanism have stopped what happened?
  X6  THE LIVE MERGE GATE.  `./build.sh` — the command the refinery actually runs — against
      a working tree carrying the pre-restructure STATE.md, restored afterwards under a
      digest.  X1 shows a script exiting 1; X6 shows THE GATE going red, which is the only
      claim that means the branch does not land.

EXITS: 0 every arm scored as required · 1 an arm did not · 2 the exhibit broke.
"""

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib_e331 as L  # noqa: E402

PRE_RESTRUCTURE = "b80dea0ec"
EA0E_LANDING = "cc4c663e8"


def plant(state_text, ceiling_text=None):
    """A throwaway tree carrying `state_text` as STATE.md and this directory's real code."""
    tmp = tempfile.mkdtemp(prefix="e331-positive-")
    dst = os.path.join(tmp, "code", "state_ratchet_e331")
    os.makedirs(dst)
    for name in ("ratchet.py", "lib_e331.py", "negative_control_e331.py", "CEILING.json"):
        shutil.copy2(os.path.join(HERE, name), os.path.join(dst, name))
    if ceiling_text is not None:
        with open(os.path.join(dst, "CEILING.json"), "w", encoding="utf-8") as fh:
            fh.write(ceiling_text)
    with open(os.path.join(tmp, "STATE.md"), "w", encoding="utf-8") as fh:
        fh.write(state_text)
    return tmp, os.path.join(dst, "ratchet.py")


def run_ratchet(state_text, ceiling_text=None):
    tmp, script = plant(state_text, ceiling_text)
    try:
        p = subprocess.run([sys.executable, "-u", script], capture_output=True, text=True)
        line = ""
        for l in p.stdout.splitlines():
            if l.startswith("RATCHET VERDICT:"):
                line = l
                break
        return p.returncode, line, p.stdout
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def score(arm, what, rc, line, want_rc, want_token):
    ok = rc == want_rc and want_token in line
    detail = line[:66] if line else "NO DECISION LINE (exit %d)" % rc
    return (arm, what, "AS REQUIRED" if ok else "FAILED", "exit %d · %s" % (rc, detail), ok)


def main():
    print("=" * 92)
    print("mg-e331 §4 — POSITIVE CONTROL: the ratchet demonstrated FAILING, on real commits")
    print("=" * 92)
    print()
    arms = []

    # ---- X1 / X2 / X3 / X4 -----------------------------------------------------------------
    print("§4.1  THE RATCHET, RUN AS A SUBPROCESS AGAINST PLANTED REAL TREES")
    print("-" * 92)
    pre = L.show(PRE_RESTRUCTURE)
    land = L.show(EA0E_LANDING)
    here = L.read_state()
    print("  b80dea0e (pre-restructure) : %6d words" % L.measure(pre)["words"])
    print("  cc4c663e (mg-ea0e landing) : %6d words" % L.measure(land)["words"])
    print("  the tree as it stands      : %6d words" % L.measure(here)["words"])
    print()

    rc, line, _ = run_ratchet(pre)
    arms.append(score("X1", "pre-restructure STATE.md (29,094 w)", rc, line, 1,
                      "ABOVE-CEILING"))
    rc, line, _ = run_ratchet(land)
    arms.append(score("X2", "mg-ea0e's own landing (4,658 w)", rc, line, 1,
                      "SLACK-UNRATCHETED"))
    rc, line, _ = run_ratchet(here)
    arms.append(score("X3", "the tree as it stands — NOT red on arrival", rc, line, 0,
                      "GREEN"))
    rc, line, _ = run_ratchet(here, ceiling_text='{"words_ceiling": 1, oops\n')
    arms.append(score("X4", "a CEILING.json that does not parse", rc, line, 2, "REFUSED"))

    width = max(len(a[1]) for a in arms)
    for arm, what, status, detail, _ in arms:
        print("  %-4s %-*s  %-11s  %s" % (arm, width, what, status, detail))
    print()

    # ---- X5 --------------------------------------------------------------------------------
    print("§4.2  X5 — THE COUNTERFACTUAL.  Had this ratchet landed WITH mg-ea0e on 2026-08-06,")
    print("      set to the 4,658 words mg-ea0e achieved, which landings would it have")
    print("      BLOCKED?  The real ratchet, the real ceiling format, the real committed")
    print("      STATE.md of every landing since.")
    print("-" * 92)
    counterfactual_ceiling = _ceiling_at(L.EA0E_LANDED[2])
    raw = L.git("log", "--first-parent", "--format=%H|%ad|%s", "--date=iso-strict",
                "main", "--", "STATE.md")
    rows = []
    for l in raw.strip().split("\n"):
        sha, date, subj = l.split("|", 2)
        rows.append((sha, date[:19], subj))
    rows.reverse()
    idx = [i for i, r in enumerate(rows) if r[0].startswith(EA0E_LANDING[:8])]
    after = rows[idx[0] + 1:] if idx else []
    blocked, passed = 0, 0
    import re as _re
    for sha, date, subj in after:
        txt = L.show(sha)
        w = L.measure(txt)["words"]
        rc, line, _ = run_ratchet(txt, counterfactual_ceiling)
        tk = _re.findall(r"\(mg-([0-9a-f]{4})\)", subj)
        verdict = "BLOCKED" if rc == 1 else ("passed" if rc == 0 else "REFUSED")
        if rc == 1:
            blocked += 1
        elif rc == 0:
            passed += 1
        print("  %-9s %s  %6d w  %-8s %s"
              % (sha[:9], date[:10], w, verdict, "mg-" + tk[-1] if tk else "—"))
    print()
    print("  %d of %d landings since mg-ea0e would have been BLOCKED by a ratchet set to"
          % (blocked, len(after)))
    print("  mg-ea0e's own achieved size; %d would have passed." % passed)
    print()
    print("  READ THIS CAREFULLY, BECAUSE IT CUTS BOTH WAYS.  It is the evidence that the")
    print("  mechanism would have bitten, and it is ALSO the evidence for §3's decision not")
    print("  to set today's ceiling at 6,000: a threshold that stops %d consecutive landings"
          % blocked)
    print("  does not hold a line, it gets removed.  What the ratchet buys is that each of")
    print("  those %d landings would have had to RAISE the number and say why — and the" % blocked)
    print("  raises themselves would then be the record nobody currently has.")
    arms.append(("X5", "counterfactual sweep at mg-ea0e's 4,658", "AS REQUIRED",
                 "%d blocked, %d passed of %d" % (blocked, passed, len(after)),
                 blocked > 0))
    print()

    # ---- X0 / X6 ---------------------------------------------------------------------------
    print("§4.3  X0 AND X6 — ONE PLANTED TREE, TWO COMMANDS, ONE DIFFERENCE.")
    print("-" * 92)
    print("  THE PLANT IS DERIVED FROM REAL BYTES, NOT TYPED: this repository's own")
    print("  docs/state-history/attempt-mg-a3d4.md, appended to STATE.md under a heading.")
    print("  That file is a relocated attempt write-up — precisely the content whose 5")
    print("  successors were written INTO the attempt index instead (out_p1_growth.txt")
    print("  §1.4).  So the planted tree is not a hypothetical: it is what this repository")
    print("  looks like when one more attempt goes into STATE.md rather than beside it.")
    print()
    graft = L.show("HEAD", "docs/state-history/attempt-mg-a3d4.md")
    planted = here + "\n\n## Appendix Z — one more attempt, written here instead of beside\n\n" \
                   + graft
    print("  planted STATE.md : %d words (%+d against the ceiling of %d)"
          % (L.measure(planted)["words"],
             L.measure(planted)["words"] - L.load_ceiling()["words_ceiling"],
             L.load_ceiling()["words_ceiling"]))
    print()
    print("  X0  the PRE-EXISTING gate, code/control_gate_724a/run_all.sh — untouched by this")
    print("      ticket.  It must exit 0: the point of X0 is that the gate this repository")
    print("      already had CANNOT SEE this, which is why a new gated quantity is the remedy")
    print("      and a new schedule is not.")
    ok0, detail0 = _gate_arm(["sh", os.path.join(L.ROOT, "code", "control_gate_724a",
                                                 "run_all.sh")],
                             planted, want_red=False, label="X0")
    arms.append(("X0", "the PRE-EXISTING gate is BLIND to it",
                 "AS REQUIRED" if ok0 else "FAILED", detail0, ok0))
    print()
    print("  X6  `./build.sh` — the command .pogo/refinery.toml names and the refinery runs.")
    print("      Same tree, same bytes, one suite added.  It must exit non-zero AND the")
    print("      non-zero must be attributable to this ratchet by its own decision line.")
    ok6, detail6 = _gate_arm(["sh", os.path.join(L.ROOT, "build.sh")],
                             planted, want_red=True, label="X6")
    arms.append(("X6", "the WIRED merge gate goes RED and names the ratchet",
                 "AS REQUIRED" if ok6 else "FAILED", detail6, ok6))
    print()

    # ---- X7 --------------------------------------------------------------------------------
    print("§4.4  X7 — P7, MEASURED RATHER THAN REMEMBERED.")
    print("-" * 92)
    print("  PREDICTIONS.md P7 bet at 0.55 that the PRE-EXISTING gate exits 0 against a tree")
    print("  carrying the 186,710-byte pre-restructure STATE.md.  X0 above already showed it")
    print("  blind to a 24,678-word file, but P7 named THAT file, so P7 is scored against")
    print("  THAT file and not against a nearby one that happens to agree with me.")
    ok7, detail7 = _gate_arm(["sh", os.path.join(L.ROOT, "code", "control_gate_724a",
                                                 "run_all.sh")],
                             pre, want_red=None, label="X7")
    print()
    p7_hit = " exit 0;" in detail7
    print("  P7: %s — the pre-existing gate came back %s on that tree."
          % ("HIT" if p7_hit else "MISS", detail7.split(";")[0].strip()))
    if not p7_hit:
        print()
        print("  P7 LOSES, AND THE REASON IS WORTH MORE THAN THE BET.  That gate does not")
        print("  exit 0 on the pre-restructure file — it REFUSES, because the twin-pin suite")
        print("  cannot parse that file's ledger and reports `twin.verdict_grade matched its")
        print("  pattern 0 time(s)`.  So the existing gate goes red on that tree for a reason")
        print("  that is not size at all: it is red because a control broke, not because the")
        print("  file is 29,094 words.  Had I scored blindness on P7's own file I would have")
        print("  recorded a green I never saw and a mechanism I never demonstrated.  X0 is")
        print("  the honest form of the claim: a file that GREW while staying structurally")
        print("  intact — which is what the last 20 landings actually did — sails through.")
    arms.append(("X7", "P7's own file against the pre-existing gate", "SCORED",
                 detail7 + (" — P7 HIT" if p7_hit else " — P7 MISS"), True))
    print()

    # ---- verdict ----------------------------------------------------------------------------
    print("=" * 92)
    print("PREDICTIONS SCORED BY THIS PRODUCER")
    print("-" * 92)
    p5 = all(a[4] for a in arms if a[0] in ("X1", "X2"))
    print("  P5    %-6s red on REAL committed bytes in BOTH directions        X1 exit 1 "
          "ABOVE, X2 exit 1 SLACK" % ("HIT" if p5 else "MISS"))
    print("  P6    HIT    a probe came back unfalsifiable/SETUP FAILED on run one")
    print("               D4: N1/N2 went UNFALSIFIABLE the moment the subject exceeded the")
    print("               ceiling and the verdict became BROKEN instead of RED — the ratchet")
    print("               could not report its own finding.  D5: N4's typed literal equalled")
    print("               the observed count on mg-ea0e's landing and N13 called SETUP FAILED.")
    print("               Both found by THIS producer, on its first run, and neither would")
    print("               have been found by any number of green runs.")
    print("  P7    %-6s see §4.4" % ("HIT" if p7_hit else "MISS"))
    print()
    bad = [a for a in arms if not a[4]]
    for arm, what, status, detail, ok in arms:
        if not ok:
            print("  %-4s %-50s %s  %s" % (arm, what[:50], status, detail))
    if bad:
        print("POSITIVE CONTROL VERDICT: FAILED — %d of %d arms did not score as required."
              % (len(bad), len(arms)))
        print("=" * 92)
        return 1
    print("POSITIVE CONTROL VERDICT: %d of %d arms scored as required.  This ratchet has been"
          % (len(arms), len(arms)))
    print("SHOWN — not argued — to exit 1 on a commit that exceeds its ceiling, to exit 1 in")
    print("the OTHER direction on a commit far below it, to exit 2 rather than guess, to be")
    print("GREEN on the tree it ships with, and to take this repository's live merge gate RED")
    print("on a tree the gate was blind to twenty minutes ago.")
    print("=" * 92)
    return 0


def _ceiling_at(words):
    import json
    return json.dumps({
        "words_ceiling": words,
        "tighten_below": max(words - 500, 0),
        "set_by": "mg-e331 X5 counterfactual",
        "set_at_words": words,
        "why": "COUNTERFACTUAL ONLY — this is what CEILING.json would have said had it "
               "landed with mg-ea0e on 2026-08-06 at the size mg-ea0e achieved.  It is not "
               "the shipped ceiling and is never written to disk outside a throwaway tree.",
    })


DIRTIED = ("code/control_audit_9876", "code/control_gate_724a",
           "code/rendered_twin_pin_9bc2", "code/state_ratchet_e331")


def _gate_arm(cmd, planted_text, want_red, label):
    """Run a REAL gate command against the real tree with STATE.md replaced, then put it back.

    THE RESTORE IS THE RISKY PART AND IT IS WHY THESE ARE THE ONLY ARMS THAT TOUCH THE REAL
    TREE.  The original bytes are held in memory, the digest is taken BEFORE, the restore is
    in a `finally`, and the digest is re-checked AFTER — so a crash mid-arm leaves a
    DETECTABLE state rather than a silently edited STATE.md.  mg-724a's exhibit established
    this shape when it planted a narrowed applicability claim in ledger row 7 and restored it
    under a checked digest; this is that, with a different plant.

    IT ALSO LEAVES OTHER TICKETS' TRANSCRIPTS MODIFIED, because both suites redirect into
    their own directories.  That is mg-724a's own recorded D5 and this arm inherits rather
    than fixes it — a `git checkout` of another ticket's files is not mine to make silently.
    The dirtied paths are NAMED and reported, so a reader knows what to restore.
    """
    original = L.read_state()
    before = hashlib.sha256(original.encode("utf-8")).hexdigest()
    try:
        with open(L.STATE, "w", encoding="utf-8") as fh:
            fh.write(planted_text)
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=L.ROOT)
        rc, out = p.returncode, p.stdout + p.stderr
    finally:
        with open(L.STATE, "w", encoding="utf-8") as fh:
            fh.write(original)
    after = hashlib.sha256(L.read_state().encode("utf-8")).hexdigest()
    print("      STATE.md sha256 %s -> %s  %s"
          % (before[:16], after[:16],
             "RESTORED byte-identically" if after == before else "*** DIFFERS ***"))
    if after != before:
        return False, "STATE.md was NOT restored — this arm is not evidence, it is damage"
    hit = [l for l in out.splitlines()
           if l.startswith("RATCHET VERDICT:") or l.startswith("GATE VERDICT:")]
    print("      %s" % " ".join(cmd[1:]).replace(L.ROOT + "/", ""))
    print("      exit %d" % rc)
    for l in hit:
        print("        %s" % l[:84])
    if want_red is None:
        # X7 SCORES a prediction; it does not require a value, so it asserts nothing here.
        ok = True
        print("      exit %d — recorded, not required.  P7 is scored on this number in §4.4."
              % rc)
    elif want_red:
        ok = rc != 0 and any(l.startswith("RATCHET VERDICT: RED") for l in hit)
        print("      %s" % (
            "THE MERGE GATE GOES RED AND THE RATCHET IS NAMED AS THE CAUSE — a branch "
            "carrying that STATE.md does not land." if ok else
            "THE MERGE GATE DID NOT GO RED FOR THIS REASON (exit %d).  If this ratchet is "
            "not wired into build.sh, that is E5 in PREDICTIONS.md happening." % rc))
    else:
        ok = rc == 0
        print("      %s" % (
            "BLIND, as required: the gate this repository already had exits 0 on a "
            "STATE.md it should be alarmed by." if ok else
            "NOT BLIND — it exited %d.  X6's claim that the difference is THIS ratchet is "
            "then unsupported, and X0 is the arm that says so." % rc))
    dirty = L.git("status", "--porcelain", "--", *DIRTIED).strip().splitlines()
    if dirty:
        print("      %d transcript(s) left modified by this arm (expected; mg-724a D5): %s"
              % (len(dirty), ", ".join(d.split()[-1] for d in dirty[:3])
                 + ("..." if len(dirty) > 3 else "")))
    return ok, "%s exit %d; %d decision line(s)" % (label, rc, len(hit))


TRANSCRIPT = os.path.join(HERE, "out_x1_positive.txt")


def run_and_transcribe():
    """Run, then write `out_x1_positive.txt` — LAST, and by this script rather than by a
    shell redirect.

    mg-502f.  THIS SCRIPT WAS IN THE CLASS mg-479c NAMED AND DID NOT SWEEP FOR.  It runs
    `./build.sh` in arm X6, and since mg-f771 joined the gate that command grades every
    tracked `code/**/out_*.txt` against its committed copy — so under
    `python3 x1_positive_control.py > out_x1_positive.txt` the shell truncates this
    script's own transcript before the script starts, and X6's `./build.sh` is handed a
    half-written file and goes RED for a reason that is nothing to do with the ratchet.

    WHAT THAT COST, MEASURED RATHER THAN ASSUMED, AND IT IS NOT WHAT IT COST x0_exhibit.py.
    Two full runs on 2026-08-13, one under the redirect and one writing outside the watched
    class: BOTH exit 0, BOTH score 8 of 8 arms AS REQUIRED, and the transcripts differ in
    12 lines, all of them inside the "N transcript(s) left modified by this arm" listings.
    X6 REQUIRES red and attributes it by the ratchet's own decision line, so a gate red for
    two reasons and a gate red for one are the same observation to it.  This arm was
    FRAGILE, never INERT — the opposite of x0_exhibit.py, whose E0 arm required GREEN and
    therefore refused outright.

    THE SELF-REDNESS IS VISIBLE IN THE REDIRECTED RUN'S OWN TRANSCRIPT, MISLABELLED: X0
    lists `code/state_ratchet_e331/out_x1_positive.txt` among the transcripts "left
    modified by this arm (expected; mg-724a D5)".  The arm did not modify it.  The shell
    did, before the arm existed, and mg-724a's D5 is the wrong owner for that line.

    So the output is buffered and the file is written after the last gate run — mg-479c's
    shape, applied to the instance mg-479c did not sweep for.
    """
    import io
    sys.path.insert(0, os.path.join(L.ROOT, "code", "self_red_sweep_502f"))
    import guard_502f
    guard_502f.refuse_if_self_red("x1_positive_control.py")

    buf = io.StringIO()
    real = sys.stdout
    sys.stdout = buf
    try:
        rc = main()
    except L.Refusal as exc:
        print()
        print("POSITIVE CONTROL VERDICT: REFUSED — %s" % exc)
        rc = 2
    finally:
        sys.stdout = real
    text = buf.getvalue()
    real.write(text)
    with open(TRANSCRIPT, "w", encoding="utf-8") as fh:
        fh.write(text)
    return rc


if __name__ == "__main__":
    sys.exit(run_and_transcribe())
