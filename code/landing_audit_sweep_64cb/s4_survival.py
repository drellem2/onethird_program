#!/usr/bin/env python3
"""s4 — DID THE WRONG FIGURE REACH THE LANDED ARTIFACT, AND IS IT STILL THERE?

The ticket's question 2: a near-miss caught by rebase is a different finding from one that
landed and stayed. Two measurements, of deliberately different kinds:

  (A) THE SEED CASE, EXACTLY. mg-5cba's repairs name their SUPERSEDED values, so this arm
      searches for each superseded figure across every canonical document at HEAD and
      classifies each hit. THREE classes, not two, and the third is the one my first draft
      got wrong:
        LIVE      running prose, no repair named nearby. THE DEFECT.
        STRUCK    inside ~~...~~, or a repair named within +/-3 lines.
        IN-REPAIR the hit is inside the very document that publishes the repair (the audit
                  doc, or mg-8d63's landing doc). Quoting a wrong value in order to correct
                  it is the correction, not the defect.
      My first draft had no IN-REPAIR class and scored 6 of 6 LIVE, every one of them a
      quotation inside the repair. It is kept as defect D2 in the report.

  (B) THE SCREEN over the residue. My first draft intersected ALL numeric literals and
      flagged 12 of 13 on section numbers (`4.2`, `5.1`), years (`2026`) and ticket digits
      (`9461`). A screen that fires on everything is not a screen. It is restricted here to
      MEASURED QUANTITIES -- decimals with three or more fraction digits -- and the count
      before and after is printed, because the drop is the whole point.

NOTE ON MY OWN EXPOSURE (E4, filed in advance): the superseded values below are READ from
mg-5cba's and mg-8d63's records and NOT recomputed -- the ticket forbids re-opening them.
This arm can tell you WHERE a value sits, never whether mg-5cba was right about it.
"""
import json
import os
import re
import subprocess
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib64cb as L

L.banner("s4 — SURVIVAL AT HEAD", __doc__.strip())

FILES = [f for f in subprocess.run(
    ["git", "-C", L.REPO, "ls-tree", "-r", "--name-only", "HEAD"],
    capture_output=True, text=True).stdout.split("\n") if f and L.is_canonical(f)]
print(f"count canonical documents at HEAD {len(FILES)}\n")

# Documents whose JOB is to publish these repairs. A superseded value quoted here is the
# repair being made, not a figure still standing.
REPAIR_DOCS = ("mg-5cba-IndependentAudit", "landing-mg-8d63", "roadmap.md")

# Read from the mg-64cb ticket body and mg-5cba's verdict. NOT recomputed.
SEED = [
    ("R2  LSTAR(6)", r"0\.794253", "0.794235"),
    # The lookarounds are load-bearing and took two tries. `(?<![\d.])338(?![\d])` matched
    # inside the comma-grouped `1,338,193,159,771` (the comma is neither a digit nor a dot)
    # and inside the line reference `:338`, and scored three false LIVEs on a probe whose
    # whole job is to decide whether a superseded figure still stands. Kept as defect D3.
    ("R3  Theorem A (SO) count at n<=7", r"(?<![\d.,:])338(?![\d,])", "2500"),
    ("R4  (M#) survival, the published TRIPLE", r"0\.943\s*[/,]\s*0\.982\s*[/,]\s*0\.958", "4 of 4"),
    ("R5  counterexample count", r"\bfour counterexamples\b|\ball three\b(?=[^\n]{0,80}counterexample)",
     "five / all four"),
]
STRIKE = re.compile(r"~~|superseded|corrected|WRONG|STRUCK|repair|was\b|instead|R\d\b", re.I)

print("(A) THE REPAIRS — every superseded figure, searched at HEAD\n")
seed_rows = []
for label, pat, new in SEED:
    rx = re.compile(pat)
    hits = []
    for f in FILES:
        try:
            lines = open(os.path.join(L.REPO, f), encoding="utf-8", errors="replace").read().split("\n")
        except OSError:
            continue
        for n, line in enumerate(lines):
            if not rx.search(line):
                continue
            if any(d in f for d in REPAIR_DOCS):
                cls = "IN-REPAIR"
            else:
                ctx = "\n".join(lines[max(0, n - 3):n + 4])
                cls = "STRUCK" if STRIKE.search(ctx) else "LIVE"
            hits.append((f, n + 1, cls, line.strip()[:130]))
    counts = {c: sum(1 for h in hits if h[2] == c) for c in ("LIVE", "STRUCK", "IN-REPAIR")}
    state = "ABSENT" if not hits else ("LIVE" if counts["LIVE"] else
                                       ("STRUCK" if counts["STRUCK"] else "IN-REPAIR"))
    seed_rows.append((label, pat, new, state, counts))
    print(f"  count hits {label}: {len(hits)}  "
          f"LIVE={counts['LIVE']} STRUCK={counts['STRUCK']} IN-REPAIR={counts['IN-REPAIR']}"
          f"  -> {state}")
    for h in hits:
        if h[2] == "LIVE" or len(hits) <= 8:
            print(f"       [{h[2]:9s}] {h[0]}:{h[1]}  {h[3]}")
    print()

live = [r for r in seed_rows if r[3] == "LIVE"]
print(f"count seed probes reading LIVE at HEAD {len(live)} of {len(seed_rows)}")
print("  -> LIVE means a superseded figure is still standing in running prose. Any non-zero")
print("     count here turns the seed from a NEAR-MISS into one that landed and stayed.\n")

# ---------------------------------------------------------------- (B) the screen
print("(B) SCREEN over the residue — MEASURED QUANTITIES ONLY\n")
adj = json.load(open(os.path.join(L.SELF_DIR, "adjudicated.json")))
residue = adj["residue"]
idx = L.build()["idx"]
ANY = re.compile(r"(?<![\w.])\d+(?:\.\d+)?(?![\w])")
MEASURED = re.compile(r"(?<![\w.])\d+\.\d{3,}(?![\w])")
REPAIRWORD = re.compile(r"repair|correct|superseded|wrong|is really|should be|overstat|"
                        r"understat|defect|instead of", re.I)


def added(item_id, rx):
    nums = set()
    for h in idx.get(item_id, {}).get("canonical", []):
        d = subprocess.run(["git", "-C", L.REPO, "show", h, "--unified=0", "--",
                            "STATE.md", "docs", "README.md"], capture_output=True, text=True).stdout
        for line in d.split("\n"):
            if line.startswith("+") and not line.startswith("+++"):
                nums |= set(rx.findall(line))
    return nums


def audit_corr(aid, rx):
    nums = set()
    for h in idx.get(aid, {}).get("commits", []):
        d = subprocess.run(["git", "-C", L.REPO, "show", h, "--unified=0"],
                           capture_output=True, text=True).stdout
        for line in d.split("\n"):
            if line.startswith("+") and not line.startswith("+++") and REPAIRWORD.search(line):
                nums |= set(rx.findall(line))
    return nums


print(f"  {'landing':9s} {'audit':9s} {'sharedANY':>10s} {'sharedMEAS':>11s}  measured overlap")
flagged, any_hits = [], 0
for t in residue:
    lid, aid = t["landing"], t["audit"]
    sa = added(lid, ANY) & audit_corr(aid, ANY)
    sm = sorted(added(lid, MEASURED) & audit_corr(aid, MEASURED))
    any_hits += 1 if sa else 0
    print(f"  {lid:9s} {aid:9s} {len(sa):>10d} {len(sm):>11d}  {sm[:8]}")
    if sm:
        flagged.append((lid, aid, sm))
print()
print(f"count residue triples screened                  {len(residue)}")
print(f"count flagged on ALL literals (the bad screen)  {any_hits}")
print(f"count flagged on MEASURED quantities            {len(flagged)}")
print("  -> the drop is the measurement. A screen firing on 12 of 13 was reporting section")
print("     numbers and years; the restricted screen is what a human should read.\n")
print("A SHARED MEASURED LITERAL IS STILL NOT A DEFECT. It says only that a number the")
print("landing published also appears on a correction line of the concurrent audit.")

json.dump(dict(seed=[(a, b, c, d, e) for a, b, c, d, e in seed_rows],
               flagged=flagged), open(os.path.join(L.SELF_DIR, "survival.json"), "w"), indent=1)
