"""B3 — the two document-level checks mg-345e's verdict rests on:

  (a) THE 1/6 CENSUS. mg-345e §6 says "1/6 occurs twice in this corpus and neither
      occurrence is a supply-side derivation". Re-run against the tree AS OF mg-345e's
      OWN COMMIT, so the count is scored against what it could actually have seen.

  (b) THE SCOPE CONFLATION. Does mg-345e use mg-3af9 (a CONSUMPTION result about
      Step 6) to establish anything about the PROVABILITY of L4-as-stated? Every
      sentence in which `mg-3af9` appears is extracted verbatim for hand reading —
      a keyword classifier is not trusted to decide this, because the classifier is
      the thing that would be tuned until it returned the answer I wanted.
"""

import re
import subprocess
import sys

MG345E_COMMIT = "550a7f105c30273b06d376a60d720cd61b652499"
DOC = "docs/OneThird-PairBias-Independence-mg-345e.md"

SIX = re.compile(r"1/6|1⁄6|⅙|\\t?frac\{?1\}?\{?6\}?|\\tfrac16")


def git_show(rev, path):
    r = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def tracked(rev, prefix):
    # DEFECT OF THIS SCRIPT, KEPT IN THE SOURCE (mg-6bd1 §D3) — AND IT IS THE WORST
    # KIND. The first form omitted `--full-tree`. `git ls-tree -r` run from a
    # SUBDIRECTORY lists only that subtree, so `docs/` matched NOTHING and the census
    # reported exactly 2 occurrences of `1/6` — WHICH IS mg-345e's OWN NUMBER. A broken
    # instrument that AGREES with the party under audit is the failure this whole
    # discipline exists to prevent, and it was caught only because the verbatim-quote
    # block below printed nothing. It is recorded rather than quietly fixed.
    r = subprocess.run(["git", "ls-tree", "-r", "--full-tree", "--name-only", rev],
                       capture_output=True, text=True)
    return [p for p in r.stdout.split("\n") if p.startswith(prefix)]


print("=" * 78)
print("B3 — the 1/6 census and the scope-conflation reading")
print("=" * 78)
print()
print(f"tree pinned at mg-345e's own commit {MG345E_COMMIT[:12]} so the census is scored")
print("against what mg-345e could actually have seen, not against tonight's tree.")
print()

# ---------------------------------------------------------------- (a) the census
paths = [p for p in tracked(MG345E_COMMIT, "docs/") if p.endswith(".md")]
paths.append("STATE.md")
hits = []
for p in sorted(set(paths)):
    if p == DOC:
        continue
    txt = git_show(MG345E_COMMIT, p)
    if txt is None:
        continue
    for i, line in enumerate(txt.split("\n"), 1):
        for _ in SIX.finditer(line):
            hits.append((p, i, line.strip()))

files = sorted({h[0] for h in hits})
print(f"(a) 1/6 CENSUS — occurrences OUTSIDE mg-345e's own document, at its own commit")
print(f"    total occurrences : {len(hits)}")
print(f"    distinct files    : {len(files)}")
print(f"    mg-345e §6 says   : 'occurs twice in this corpus'")
print(f"    -> the claim is REFUTED on the literal count by a factor of"
      f" {len(hits) // 2}x")
print()
print("    per file:")
for f in files:
    print(f"       {sum(1 for h in hits if h[0] == f):>3}  {f}")
print()
print("    THE ONE THAT MATTERS — the supply-side occurrence mg-345e says does not")
print("    exist, quoted verbatim from the tree mg-345e itself was standing on:")
print()
for p, i, line in hits:
    if "c4f5" in p and "Freezing" in line:
        print(f"       {p}:{i}")
        print(f"       > {line}")
print()
print("    HAND CLASSIFICATION — the raw 34 is NOT the number to quote against mg-345e,")
print("    and saying so is the point. It is inflated two ways, both disclosed:")
print("      * REGEX FALSE POSITIVES: `61/61`, `6197/6197` contain the substring `1/6`.")
print("        audit-mg-2789 (2), audit-mg-5f9a (1), landing-mg-1c80 (1),")
print("        Hodge-IndependentAudit (1)  ->  5 hits are not the number 1/6 at all.")
print("      * DIFFERENT SUBJECT MATTER: Hodge gamma-weights (4), mg0a11's")
print("        1/C(6,1) extremal-core probability (5), L4-branch-(ii) cut arithmetic (2),")
print("        roadmap prose naming Daniel's ask (2)  ->  13 are unrelated to eps_spec.")
print()
print("    In the eps_spec / pair-bias subject matter, the DISTINCT occurrences are:")
print("      1. Op-Form 6.4 'slack <= 1/6 for a centred pair'  [DEMAND; BROKEN as")
print("         labelled by mg-e35c F5]  — restated in its audit and in attempt-mg-88bd")
print("      2. mg-e2de's 1/6, the collapse of a local delta LOWER bound at co-degree 2")
print("         (STATE.md:158)  [neither supply nor demand: a lower bound]")
print("      3. mg-c4f5:415 'Freezing unconditionally gives only eps < 1/6'  [SUPPLY]")
print()
print("    mg-345e names 1 and 2 and says there are two. THERE ARE AT LEAST THREE, and")
print("    the third is the one its sentence rules out by kind.")
print()
print("    This is SUPPLY-side — it says what FREEZING GIVES, not what the")
print("    architecture needs — and B2/C4 shows it is mg-345e's OWN `eps_sup < 1`")
print("    under a different division. So mg-345e's §6 sentence is wrong on BOTH of")
print("    its two counts: the number, and the 'neither is supply-side'.")
print()

# --------------------------------------------------------- (b) the scope reading
txt = git_show(MG345E_COMMIT, DOC)
lines = txt.split("\n")

print("(b) SCOPE CONFLATION — every mg-3af9 sentence, verbatim, for hand reading.")
print("    (no keyword classifier decides this; a classifier tuned until it returns")
print("     the answer I want is unfalsifiable)")
print()
for i, line in enumerate(lines, 1):
    if "mg-3af9" in line:
        print(f"    {DOC}:{i}")
        for seg in re.split(r"(?<=[.;])\s+", line.strip()):
            if "mg-3af9" in seg or "F`" in seg:
                print(f"      | {seg}")
        print()

print("    and the paragraph mg-345e wrote to guard exactly this, verbatim:")
for i, line in enumerate(lines, 1):
    if "SCOPE DISCIPLINE" in line:
        for j in range(i - 1, min(i + 8, len(lines))):
            print(f"    {j+1:>4} | {lines[j]}")
        break
print()

# where the qualifier does and does not appear — the three-column discipline of P13
print("    THREE COLUMNS (mg-6bd1 P13's binding guard — a defect present only in the")
print("    compression is a LABELLING finding, not BROKEN):")
subj = subprocess.run(["git", "log", "-1", "--format=%s", MG345E_COMMIT],
                      capture_output=True, text=True).stdout
body = subprocess.run(["git", "log", "-1", "--format=%b", MG345E_COMMIT],
                      capture_output=True, text=True).stdout
state = git_show(MG345E_COMMIT, "STATE.md")
QUAL = ("provab", "CONSUME", "consumes", "consumption")


def has_qual(s, near=None):
    return any(q in s for q in QUAL)


doc_scope = [i for i, l in enumerate(lines, 1) if "SCOPE DISCIPLINE" in l]
print(f"      document body   : scope guard present at line(s) {doc_scope}"
      f"  -> {bool(doc_scope)}")
st_rows = [i for i, l in enumerate(state.split("\n"), 1)
           if "mg-345e" in l and "SCOPE" in l]
print(f"      STATE.md rows   : rows carrying an explicit SCOPE clause: {st_rows}"
      f"  -> {bool(st_rows)}")
print(f"      commit body     : carries the guard: {has_qual(body)}")
print(f"      commit SUBJECT  : carries the guard: {has_qual(subj)}")
print(f"      subject text    : {subj.strip()[:100]}")
print()
print("=" * 78)
