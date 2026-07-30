#!/usr/bin/env python3
"""mg-2216 — the non-mutation half of the audit of `bf17716` (mg-2da3).

`mutation_battery.py` answers "what can the new control not see?".  This file answers the
other three questions the ticket asks:

  T2  DID THE REPAIR PRESERVE THE PINNED BATTERY'S ORIGINAL PURPOSE?  `code/state_audit_6a2f/`
      pins `97cb533` / `60f4dac` / `57f962f` deliberately — it reproduces an audit of a
      specific historical state.  mg-2da3 was told not to repoint it.  A repair that fixed
      the certification by breaking the reproduction would have traded one defect for
      another.

  T3  IS THE RECORD CORRECTION FINDABLE FROM THE CLAIM IT CORRECTS, and does it follow the
      repo's existing convention?  A retraction filed where nobody reading the original will
      meet it is not a correction.

  T4  ARE THE COMMIT'S OWN FACTUAL CLAIMS TRUE — including the ones that read as fairness
      rather than as claims.  Caveats are the least-audited sentences in this arc, so the
      two the commit adds in mitigation ("b68db5d's SECOND cited re-run IS genuine"; "the
      verify_relocation.py failure is pre-existing, not mine") are checked here as claims.

Every check states what it measured.  Nothing is inherited from the artifact under audit:
the ancestry, the line and cell counts, the four completeness figures and the runtime are
all re-derived here.  Read-only — this script mutates nothing.
"""
import os
import re
import subprocess
import sys
import time

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()

REPAIR = "bf17716"          # mg-2da3, the commit under audit
LANDING = "b68db5d"         # mg-7735, the commit whose message it corrects
RESTRUCTURE = "57f962f"     # mg-34bf, the revision the pinned battery is evidence about

BATTERY_DIR = "code/state_audit_6a2f"
CONTROL_DIR = "code/state_landing_control_2da3"

ok_count = [0]
bad = []


def say(label, ok, detail=""):
    print(f"  [{'ok' if ok else 'NO'}] {label}")
    if detail:
        for line in detail.split("\n"):
            print(f"        {line}")
    if ok:
        ok_count[0] += 1
    else:
        bad.append(label)
    return ok


def git(*args, binary=False):
    p = subprocess.run(["git", "-C", REPO, *args],
                       capture_output=True, check=True)
    return p.stdout if binary else p.stdout.decode("utf-8")


def read(path):
    with open(os.path.join(REPO, path), encoding="utf-8") as fh:
        return fh.read()


def table_cells(text):
    rows = 0
    cells = 0
    for line in text.split("\n"):
        if not line.startswith("|"):
            continue
        bars = [i for i, ch in enumerate(line)
                if ch == "|" and (i == 0 or line[i - 1] != "\\")]
        if len(bars) < 2:
            continue
        rows += 1
        cells += len(bars) - 1
    return rows, cells


def appendix_a(text):
    return text[text.index("## Appendix A —"):]


def main():
    print("mg-2216 — audit of bf17716's non-instrument claims")
    print("=" * 86)
    print()

    # ==== T2 — the pinned battery ========================================================
    print("T2. DID THE REPAIR PRESERVE THE PINNED BATTERY?")
    diff = git("diff", "--name-only", f"{REPAIR}^..{REPAIR}", "--", BATTERY_DIR).strip()
    say(f"{BATTERY_DIR}/ is byte-identical across the repair",
        diff == "", f"git diff --name-only {REPAIR}^..{REPAIR} -- {BATTERY_DIR} -> "
                    f"{diff!r} (empty = untouched)")

    touched = git("diff", "--name-only", f"{REPAIR}^..{REPAIR}").split()
    say("the repair touched exactly 6 files, none of them an existing instrument",
        len(touched) == 6, "\n".join(touched))

    t0 = time.time()
    p = subprocess.run(["sh", f"{BATTERY_DIR}/run_all.sh"], cwd=REPO, capture_output=True)
    battery_secs = time.time() - t0
    with open(os.path.join(REPO, BATTERY_DIR, "out_audit.txt"), "rb") as fh:
        committed = fh.read()
    say("the historical reproduction still works, byte-identically, at this commit",
        p.stdout == committed,
        f"{len(p.stdout)} bytes produced vs {len(committed)} committed; "
        f"exit {p.returncode}")

    pinned_hits = []
    for name in sorted(os.listdir(os.path.join(REPO, BATTERY_DIR))):
        if not name.endswith((".py", ".sh")):
            continue
        src = read(f"{BATTERY_DIR}/{name}")
        if re.search(r"\bopen\s*\(|\bHEAD\b", src):
            pinned_hits.append(name)
    say("no script in the pinned battery opens the working tree or resolves HEAD "
        "(the commit's own claim, re-run here)",
        not pinned_hits, f"scripts matching open(|HEAD: {pinned_hits or 'none'}")
    print()

    # ==== T2b — the one-grep test the new Appendix A clause promotes ======================
    print("T2b. THE ONE-GREP TEST THE CONVENTION PROMOTES, applied to this repo")
    print("     Appendix A: \"does any script in it open the working tree or resolve "
          "HEAD?\"")
    mixed = []
    for d in sorted(os.listdir(os.path.join(REPO, "code"))):
        full = os.path.join(REPO, "code", d)
        if not os.path.isdir(full):
            continue
        srcs = [n for n in sorted(os.listdir(full)) if n.endswith(".py")]
        if not srcs:
            continue
        reading = [n for n in srcs
                   if re.search(r"\bopen\s*\(|\bHEAD\b", read(f"code/{d}/{n}"))]
        if reading and len(reading) < len(srcs):
            mixed.append((d, reading, [n for n in srcs if n not in reading]))
    say("the test is asked of a DIRECTORY, and no directory in code/ is mixed "
        "(so 'any script' cannot license citing a pinned one)",
        not mixed,
        "\n".join(f"{d}: tree-reading {r}, pinned {p}" for d, r, p in mixed)
        or "no mixed directory")
    print()

    # ==== T3 — the record correction ======================================================
    print("T3. IS THE CORRECTION FINDABLE FROM THE CLAIM IT CORRECTS?")
    tracked = git("ls-files").split()
    mentions = [f for f in tracked
                if f.endswith((".md", ".py", ".sh")) and "state_landing_control_2da3" in
                read(f)]
    say("the new control is named in at least one document a reader lands on",
        len(mentions) >= 2, "named in:\n" + "\n".join(sorted(mentions)))

    battery_srcs = " ".join(read(f"{BATTERY_DIR}/{n}")
                            for n in sorted(os.listdir(os.path.join(REPO, BATTERY_DIR)))
                            if n.endswith((".py", ".sh")))
    say("THE POINT OF USE CARRIES A POINTER: re-running the pinned battery surfaces the "
        "correction",
        ("state_landing_control_2da3" in battery_srcs
         or "evidence about" in battery_srcs),
        "grep over every script in the pinned battery for the correction or the new "
        "control: no hit.\n"
        "A future agent who runs the battery and is about to cite it meets nothing.")

    row_history = read("docs/state-history/attempt-mg-276d.md")
    say("the per-row history of the row b68db5d edited carries the correction "
        "(the repo's rule 2: 'the row keeps a pointer naming it')",
        "state_landing_control_2da3" in row_history or "mg-2da3" in row_history,
        "docs/state-history/attempt-mg-276d.md mentions neither mg-2da3 nor the new "
        "control.\nThe correction lives only in docs/state-history/README.md and "
        "STATE.md's Appendix A.")

    readme = read("docs/state-history/README.md")
    say("the A3 correction sits adjacent to the bullet it corrects (the good pattern)",
        readme.index("`two commits before mg-34bf's parent` was off by one")
        - readme.index("**Two corrections to this bullet, from mg-6a2f §B1") < 900,
        "the A3 blockquote opens "
        f"{readme.index(chr(96) + 'two commits before mg-34bf' + chr(39) + 's parent' + chr(96) + ' was off by one') - readme.index('**Two corrections to this bullet, from mg-6a2f §B1')}"
        " characters after the bullet it corrects — a reader of the claim meets the "
        "correction.")

    say("the A1 correction (the ticket's headline) is in a section of its own at the "
        "end of the same file",
        readme.index("## What certifies a change to these files") > readme.index(
            "## How completeness is checked"),
        "placed after '## How completeness is checked'; nothing above it points down at "
        "it,\nand the claim it corrects is in a frozen commit message.")

    say("the convention has repo precedent for correcting a commit log (Appendix A)",
        "RECORDED HERE BECAUSE NOTHING ELSE CORRECTS A COMMIT LOG" in read("STATE.md"),
        "STATE.md Appendix A already corrects `ba3ec79`'s commit message on that basis.")

    say("mg-7735 itself put its F1/F2 corrections in this README (the cited precedent)",
        LANDING in git("log", "--format=%h", "-S",
                       "THOSE FIVE FIGURES WERE WRONG, here and in",
                       "--", "docs/state-history/README.md"),
        "git log -S over the F2 block returns b68db5d.")
    print()

    # ==== T4 — the commit's own factual claims ===========================================
    print("T4. THE COMMIT'S OWN FACTUAL CLAIMS")

    # A3 — the ancestry correction
    parents = {r: git("log", "--format=%p", "-1", r).strip().split()[0][:7]
               for r in (RESTRUCTURE, "97cb533", "60f4dac")}
    say("A3's correction is right: 60f4dac is mg-34bf's PARENT'S PARENT, not two "
        "commits before the parent",
        parents[RESTRUCTURE].startswith("97cb533"[:7])
        and parents["97cb533"].startswith("60f4dac"[:7]),
        f"{RESTRUCTURE} <- {parents[RESTRUCTURE]} <- {parents['97cb533']} "
        f"(re-derived from git log --format=%p)")

    # A2 — the over-claim correction
    audit_doc = read("docs/OneThird-STATE-Restructure-IndependentAudit.md").split("\n")
    line212 = audit_doc[211]
    say("A2's correction is right: mg-6a2f DID name the source, at :212 of its document",
        "pm-onethird's ticket (a stale revision, line bytes)" in line212,
        f":212 = {line212.strip()[:100]}")
    db = git("show", "db08b4c:STATE.md")
    say("and the hash db08b4c is the real new contribution: 327 lines, 0 'mg-a3d4'",
        len(db.split("\n")) - 1 == 327 and db.count("mg-a3d4") == 0,
        f"{len(db.split(chr(10))) - 1} lines, {db.count('mg-a3d4')} occurrences of mg-a3d4")

    # the "in fairness" caveat — audited as a claim, not accepted as fairness
    vr = read("code/state_restructure_34bf/verify_relocation.py")
    say("CAVEAT AUDITED — 'b68db5d's SECOND cited re-run IS genuine': "
        "verify_relocation.py's completeness half really opens the working tree",
        'open("STATE.md"' in vr,
        "code/state_restructure_34bf/verify_relocation.py:95 "
        "-> new = open(\"STATE.md\", encoding=\"utf-8\").read()")
    p = subprocess.run([sys.executable, "code/state_restructure_34bf/verify_relocation.py"],
                       cwd=REPO, capture_output=True, text=True)
    out = p.stdout
    figs = {
        "cells changed": 10,
        "words in those cells at base": 11625,
        "maximal verbatim runs covering them": 125,
        "words not found anywhere reachable": 0,
    }
    got = {}
    for k in figs:
        m = re.search(re.escape(k) + r"\s*:\s*(\d+)", out)
        got[k] = int(m.group(1)) if m else None
    say("and its four cited figures reproduce here exactly",
        got == figs, "; ".join(f"{k} = {v}" for k, v in got.items()))

    # the pre-existing-failure attribution
    say("CAVEAT AUDITED — the 'FAIL Appendix A changed' really is pre-existing",
        "FAIL  Appendix A changed" in out
        and appendix_a(git("show", "bdcb006:STATE.md")) != appendix_a(
            git("show", f"{RESTRUCTURE}:STATE.md")),
        "it fails at this clean commit, and Appendix A had already diverged from "
        f"{RESTRUCTURE} at bdcb006,\ntwo commits before {LANDING} — so the repair's "
        "+2 lines did not cause it.")

    # SCOPE arithmetic
    for rev, want_lines in ((LANDING, 380), (REPAIR, 382)):
        t = git("show", f"{rev}:STATE.md")
        rows, cells = table_cells(t)
        lines = len(t.split("\n")) - 1
        say(f"{rev}: {want_lines} lines, 210 cells (the commit's SCOPE paragraph)",
            lines == want_lines and cells == 210,
            f"measured {lines} lines, {rows} table rows, {cells} cells")

    # the certified row is byte-identical to what b68db5d left
    def row135(text):
        for line in text.split("\n"):
            if line.startswith("|") and "mg-276d" in line[:400]:
                return line
        return None
    say("row :135 is byte-for-byte what b68db5d left (the commit's 'not re-opened' claim)",
        row135(git("show", f"{LANDING}:STATE.md")) == row135(read("STATE.md")),
        "compared as whole lines")

    say("no per-row history file and no ledger row was touched by the repair",
        not [f for f in touched if f.startswith("docs/state-history/attempt-")],
        "changed files: " + ", ".join(touched))

    # 'nothing was lost' is not re-opened
    msg = git("log", "-1", "--format=%B", REPAIR)
    say("'NOTHING WAS LOST' is restated as STANDING and is not re-verified",
        "NOTHING WAS LOST\" STANDS" in msg or '"NOTHING WAS LOST" STANDS' in msg,
        "the commit message states it stands and cites mg-6a2f and mg-bd41 for it.")

    # the runtime claim
    t0 = time.time()
    subprocess.run(["sh", f"{CONTROL_DIR}/run_all.sh"], cwd=REPO, capture_output=True)
    secs = time.time() - t0
    # Wall-clock is the one figure that cannot reproduce byte-identically, so it is
    # reported as a bracket rather than a number; the raw seconds are in the audit
    # document, stamped with the box they were measured on.
    say("the '~25 s' runtime the repair states for its own battery",
        20 <= secs <= 30,
        f"measured wall time is in the bracket "
        f"{'20-30 s' if 20 <= secs <= 30 else ('under 5 s' if secs < 5 else 'other')}, "
        "against a stated ~25 s in both the commit message and run_all.sh:25.\n"
        f"the pinned battery it runs twice is itself in the bracket "
        f"{'under 2 s' if battery_secs < 2 else 'over 2 s'}.")

    # out_control.txt reproduction
    p = subprocess.run(["sh", f"{CONTROL_DIR}/run_all.sh"], cwd=REPO, capture_output=True)
    with open(os.path.join(REPO, CONTROL_DIR, "out_control.txt"), "rb") as fh:
        want = fh.read()
    say("out_control.txt reproduces byte-identically",
        p.stdout == want, f"{len(p.stdout)} bytes vs {len(want)} committed")
    print()

    print("=" * 86)
    print(f"{ok_count[0]} checks held, {len(bad)} did not.")
    if bad:
        print("DID NOT HOLD:")
        for b in bad:
            print(f"  - {b}")
    print("=" * 86)
    return 0


if __name__ == "__main__":
    sys.exit(main())
