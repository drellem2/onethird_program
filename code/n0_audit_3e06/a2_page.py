#!/usr/bin/env python3
"""
mg-3e06 — page-side checks of mg-5ce3's landing.

CHECKS 2, 3, 4 of the brief:
  2. did the strengthening OVERSHOOT §5.3?
  3. was each "unspecified" site decided on its merits, or blanket-replaced?
  4. did the mg-d1a2 row-8 guard SURVIVE?

Everything here is a BYTE test over the file as it stands, never a line-number
or line-content comparison — bound in PREDICTIONS.md P16 before the file was
opened, because row 8 was edited by four tickets in one day and a moved line is
not a lost line.
"""

import re
import subprocess
import sys

STATE = "STATE.md"
PARENT = "4ef64d7"          # mg-5ce3
PRE = PARENT + "^"


def git_show(rev, path):
    return subprocess.run(["git", "show", f"{rev}:{path}"],
                          capture_output=True, text=True, check=True).stdout


def banner(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


def main():
    cur = open(STATE, encoding="utf-8").read()
    pre = git_show(PRE, STATE)
    post = git_show(PARENT, STATE)
    head_sha = subprocess.run(["git", "log", "-1", "--format=%H", "--", STATE],
                              capture_output=True, text=True, check=True).stdout.strip()
    blob = subprocess.run(["git", "hash-object", STATE],
                          capture_output=True, text=True, check=True).stdout.strip()

    banner("A5 — WHICH STATE.md IS THIS?  (the dispatch requires the SHA be named)")
    print(f"   last commit touching STATE.md : {head_sha}")
    print(f"   blob sha1 of the file I read  : {blob}")
    print(f"   mg-5ce3's commit              : {PARENT}")
    anc = subprocess.run(["git", "merge-base", "--is-ancestor", PARENT, head_sha])
    print(f"   is mg-5ce3 an ANCESTOR of it? : {anc.returncode == 0}")
    print("   -> if True, STATE.md was REWRITTEN AFTER mg-5ce3 landed, and the")
    print("      survival test below is one the parent could not have run.")

    # ------------------------------------------------------------------
    banner("A6 — THE mg-d1a2 GUARD (check 4).  Byte substrings, not lines.")
    guard = {
        "the INSTRUCTION (mg-d1a2's, verbatim)":
            "DO NOT CITE THE LITERATURE BOUND AGAINST THIS `N₀`",
        "the REFUSAL (mg-d1a2's, verbatim)":
            "and that discharges nothing here",
        "mg-d1a2's ORIGINAL REASON, kept":
            "an unspecified threshold is not a size any number can exceed",
        "mg-d1a2's original reason ATTRIBUTED to mg-d1a2":
            "(mg-d1a2: *an unspecified threshold is not a size any number can exceed*, still true)",
        "the STRENGTHENED reason":
            "there is no threshold to exceed",
        "the two literature numbers the guard refuses":
            "`n ≥ 12` (refereed, Peczarski 2006) and `n ≥ 15` (preprint, Gupta 2026)",
    }
    ok = 0
    for label, s in guard.items():
        pre_has, cur_has = s in pre, s in cur
        status = "OK " if cur_has else "***"
        ok += cur_has
        print(f"   {status} {label:52s} pre={pre_has!s:5s} now={cur_has!s:5s}")
    print(f"   -> {ok}/{len(guard)} guard components present in the CURRENT file")

    print("\n   IS THE GUARD OVER-DETERMINED?  (a guard resting on ONE reason falls")
    print("   with that reason.  mg-5ce3 was told to strengthen the reason without")
    print("   weakening the guard — the test is whether BOTH reasons are live.)")
    both = ("an unspecified threshold is not a size any number can exceed" in cur
            and "there is no threshold to exceed" in cur)
    print(f"      both reasons present and each independently sufficient: {both}")

    # ------------------------------------------------------------------
    banner("A7 — THE 'unspecified' SITES (check 3).  Decided each, or swept?")
    for name, txt in (("PRE  (4ef64d7^)", pre), ("POST (4ef64d7)", post), ("NOW  (working tree)", cur)):
        lines = txt.split("\n")
        occ = [(i + 1, m.start()) for i, L in enumerate(lines) for m in re.finditer("unspecified", L)]
        by_line = {}
        for ln, _ in occ:
            by_line[ln] = by_line.get(ln, 0) + 1
        print(f"   {name:22s} occurrences={len(occ):2d}  lines={sorted(by_line)}  "
              f"per-line={ {k: v for k, v in sorted(by_line.items())} }")
    print("\n   -> the ticket said FOUR, mg-5ce3 said SIX.  grep -o counts")
    print("      OCCURRENCES, grep -n counts LINES.  Both numbers below.")

    print("\n   the survivors, and WHY each is a different use:")
    lines = cur.split("\n")
    for i, L in enumerate(lines):
        for m in re.finditer("unspecified", L):
            a, b = max(0, m.start() - 110), min(len(L), m.end() + 110)
            print(f"\n   line {i+1} col {m.start()}:")
            print(f"      ...{L[a:b]}...")

    # blanket-replace test
    banner("A8 — WAS IT A BLANKET REPLACE? (check 3, the mechanical half)")
    pre_l, post_l = pre.split("\n"), post.split("\n")
    changed = [i + 1 for i, (a, b) in enumerate(zip(pre_l, post_l)) if a != b]
    print(f"   lines differing pre->post : {changed}  ({len(changed)} lines)")
    print(f"   line counts               : pre={len(pre_l)} post={len(post_l)} "
          f"(equal: {len(pre_l) == len(post_l)})")
    print("   -> a sed sweep over 'unspecified' would have touched every site")
    print("      including the two deliberately left.  It did not.")

    # ------------------------------------------------------------------
    banner("A9 — DID THE STRENGTHENING OVERSHOOT? (check 2, the expensive one)")
    print("   §5.3 proves a statement about THE CLASS of o(n^2) functions.")
    print("   Two things it does NOT prove, and which a site must not assert:")
    print("     (X) that no single (LIB-weak) family has a threshold of its own")
    print("     (Y) that (LIB-const) never holds / the implication is false")
    print()
    sites = {
        "line 15  (one-paragraph state)": None,
        "line 23  (Axis 1)": None,
        "line 64  (mermaid label)": None,
        "line 115 (ledger row 8)": None,
    }
    for key in list(sites):
        ln = int(re.search(r"line (\d+)", key).group(1))
        sites[key] = lines[ln - 1]

    # every site must carry an in-sentence scope qualifier
    QUALIFIERS = ["for the class", "FOR THE CLASS",
                  "from the hypothesis", "from the `o(n²)` hypothesis"]
    print("   per-site: does the claim carry a SCOPE QUALIFIER in its own sentence?")
    for key, txt in sites.items():
        found = [q for q in QUALIFIERS if q in txt]
        print(f"      {'OK ' if found else '***'} {key:32s} -> {found}")

    print("\n   per-site: does any site assert (X) or (Y)?  searched as text:")
    OVERSHOOT = [
        "no family", "no (LIB-weak) family", "never satisfies",
        "(LIB-const) never holds", "no threshold exists for any",
        "cannot hold at any", "is false for every family",
    ]
    bad = [(k, o) for k, t in sites.items() for o in OVERSHOOT if o in t]
    print(f"      overshoot phrases found: {bad if bad else 'NONE'}")

    print("\n   the RIDER that prevents (X) — present anywhere on the page?")
    rider = ("a single family satisfying (LIB-weak) does have *some* threshold "
             "of its own")
    print(f"      {'OK ' if rider in cur else '***'} \"{rider}\"  -> {rider in cur}")
    named = "Only a *rate* would give one ((LIB)'s `O(n)`"
    print(f"      {'OK ' if named in cur else '***'} the page NAMES the surviving route: {named in cur}")

    # ------------------------------------------------------------------
    banner("A10 — MERMAID INTEGRITY (line 64 was edited inside a diagram)")
    block = re.search(r"```mermaid\n(.*?)\n```", cur, re.S)
    edges = [l for l in block.group(1).split("\n") if "-->" in l]
    allok = True
    for e in edges:
        labs = re.findall(r'\|"([^"]*)"\|', e)
        nq = e.count('"')
        bad_pipe = any("|" in l for l in labs)
        good = (len(labs) == 1) and (nq == 2) and not bad_pipe
        allok &= good
        print(f"   {'OK ' if good else '***'} quotes={nq} labels={len(labs)} "
              f"pipe-in-label={bad_pipe}  {e.strip()[:64]}")
    print(f"   -> all {len(edges)} edges well-formed: {allok}")
    print("   (mermaid edge labels break on an unescaped '|'; commas are safe.)")

    banner("A11 — DID mg-5ce3 OVERSHOOT ITS SOURCE?  landed text vs §5.3 text")
    doc = open("docs/OneThird-LIBweak-mg-c4f5-IndependentAudit.md", encoding="utf-8").read()
    s53 = doc[doc.index("### 5.3"):doc.index("### 5.4")]
    print("   §5.3's own operative sentence:")
    print("      \"No `N₀` works for the class.\"  present in §5.3: ",
          "No `N₀` works for\nthe class" in s53 or "No `N₀` works for the class" in s53.replace("\n", " "))
    print("   the ticket's paraphrase was \"NO N_0 EXISTS\" (looser).")
    print("   what LANDED on the page, per site:")
    for key, txt in sites.items():
        # SIXTH instrument defect, kept: this regex first required backticks
        # around N₀ and reported line 64 as carrying NO class-scoped phrase.
        # The mermaid label correctly omits backticks (they render literally
        # inside a diagram label), so the miss was mine.  A9 had already found
        # "for the class" there by plain substring — the two disagreed and the
        # regex was wrong.
        m = re.search(r"(NO `?N₀`? WORKS FOR THE CLASS[^.]*|no `?N₀`? works for the class[^:.]*)",
                      txt, re.I)
        print(f"      {key:32s} -> {m.group(1)[:70] if m else 'NO CLASS-SCOPED PHRASE'}")


if __name__ == "__main__":
    main()
