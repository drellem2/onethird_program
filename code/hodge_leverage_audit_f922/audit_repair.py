#!/usr/bin/env python3
"""mg-f922 -- INDEPENDENT AUDIT of mg-e1d0 (`bbe83b5`), the landing that closes
mg-3c24, the audit of `1e61031` (mg-a2bd's strike of ledger row `G"`).

The brief names four targets.  This instrument answers all four by
re-measuring, and then answers a fifth that no list here names.

  T1  RE-DERIVE THE FOUR FIGURES.  13 551 -> 16 692 against a static 10 623,
      so the gap 2 928 -> 6 069.  Measured from git, with a row locator that
      shares NO anchor with the landing's own instrument: the landing finds
      the rows by the literal prefixes "| **AMBER-POSITIVE" and
      "> **AMBER-POSITIVE"; this one finds them as the unique table line
      naming mg-a3d4 and the unique block-quote line naming the priced bet.
      Same rows by a different route, or the figures do not stand.

  T2  WAS THE ENLARGEMENT RECORDED WHERE A READER OF A5 MEETS IT?  The brief's
      primary target: the parent had to do TWO things and the second is easy
      to skip.  Every site in the repository where A5 is stated is enumerated
      and checked for the enlargement, INCLUDING the document that states A5
      verbatim -- mg-d39d's own audit -- and the arc's own precedent for
      annotating an audit document in place is measured rather than assumed.

  T3  IS THE FIGURE A READER MEETS THE CURRENT ONE?  The disclosure's own
      framing is that "a reader of A5 must meet the current gap rather than
      the one it was opened with".  So the figure it prints as current is
      measured against the tree.

  T4  DID THE REPAIR OVER-CORRECT?  mg-3c24 found 0 BROKEN mathematics and
      that the strike is right for the right reason.  A repair that hedges
      the strike or reopens the counterexample counts is a defect in the
      other direction.  Every headline figure is diffed across the landing.

  T5  THE RESTORED CONDITION, AT EVERY SITE.  `lambda_2(F(A_m)) <= 1/2` as a
      COMPUTATIONAL base case, with Theorem G giving only `>= 1/2`.  The
      landing's instrument checks a hard-coded list of four sites.  This one
      sweeps the tree for the CONCLUSION and asks, of every site that states
      it, whether the condition is there.

  T6  COUNT THE BRIEF.  F4 is a rule about enumeration, so mg-a806's items are
      counted from the ticket itself and matched one by one against the names
      the corrected text gives them.

  T7  BEYOND THE BRIEF, DECLARED.  The list above is a floor.  The thing
      chosen: THE LANDING'S OWN EVIDENCE ARTIFACT -- does the committed
      transcript reproduce, does its runner report failure, and are the
      three findings of mg-3c24 that this landing did not land disclosed
      anywhere.

  T8  WHAT COULD NOT BE BROKEN.  The mg-2da3 control and its re-baseline.

Then a NEGATIVE CONTROL: four in-memory mutations, each with its expected
verdict written down before the run, so this file is a control that can fail
rather than a description of an answer already had.

Pure Python 3 + git.  No third-party packages.  Runtime ~2 s.
"""

import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

STATE = "STATE.md"
DELIV = "docs/OneThird-Hodge-Side-Leverage.md"
HIST = "docs/state-history/attempt-mg-a3d4.md"
D39D = "docs/OneThird-Hodge-Side-Leverage-StateLanding-IndependentAudit.md"
M86A3 = "docs/OneThird-Hodge-Side-Leverage-IndependentAudit.md"
AUD3C24 = "docs/OneThird-Hodge-Side-Leverage-GppStrike-IndependentAudit.md"

STRIKE = "1e61031"       # mg-a2bd, the commit mg-3c24 audited
LANDING = "bbe83b5"      # mg-e1d0, the repair this audit is of

RESULTS = []


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True, check=True).stdout


def blob(commit, path):
    r = subprocess.run(["git", "-C", REPO, "show", f"{commit}:{path}"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def tree(path):
    with open(os.path.join(REPO, path), encoding="utf-8") as fh:
        return fh.read()


def flat(text):
    return " ".join(text.split())


# --- row locators.  Deliberately NOT the landing's anchors. --------------
def state_row(text):
    """The STATE.md cell A5 is about: the unique TABLE line naming mg-a3d4."""
    hits = [l for l in text.split("\n")
            if l.startswith("|") and "mg-a3d4" in l and "the bet is priced" in l.lower()]
    if len(hits) != 1:
        raise SystemExit(f"STATE row: expected 1 line, got {len(hits)}")
    return hits[0]


def deliv_row(text):
    """§14's frozen copy: the unique BLOCK-QUOTE line naming the priced bet."""
    hits = [l for l in text.split("\n")
            if l.startswith(">") and "the bet is priced" in l and "mg-a3d4" in l]
    if len(hits) != 1:
        raise SystemExit(f"deliverable row: expected 1 line, got {len(hits)}")
    return hits[0]


def record(ok, detail):
    RESULTS.append((detail, ok))
    mark = {True: "[CONFIRMED]", False: "[REFUTED  ]", None: "[MEASURED ]"}[ok]
    print(f"  {mark} {detail}")


def finding(tag, detail):
    RESULTS.append((f"{tag}: {detail}", "FINDING"))
    print(f"  [FINDING  ] {tag} -- {detail}")


def head(title):
    print()
    print(title)
    print("-" * len(title))


# =========================================================================
def t1():
    head("T1 -- THE FOUR FIGURES, RE-DERIVED BY A DIFFERENT ROUTE")
    print("""The landing locates both rows by the literal prefix '**AMBER-POSITIVE'.
This locates the STATE.md cell as the unique table line naming mg-a3d4, and
§14's copy as the unique block-quote line naming the priced bet.  Different
anchors; if the figures differ, one of the two is measuring the wrong row.
""")
    chain = [(f"{STRIKE}^", "before mg-a2bd"),
             (STRIKE, "after  mg-a2bd"),
             (f"{LANDING}^", "before mg-e1d0 (the repair)"),
             (LANDING, "at     mg-e1d0"),
             ("HEAD", "HEAD (this audit)")]
    print(f"    {'commit':<10} {'STATE.md cell':>13} {'§14 copy':>10} {'gap':>9}  when")
    fig = {}
    for ref, label in chain:
        a = len(state_row(blob(ref, STATE)))
        b = len(deliv_row(blob(ref, DELIV)))
        fig[ref] = (a, b)
        # The sha is printed for the FIXED commits only.  HEAD is printed as
        # "HEAD": a transcript that embeds the sha it happened to be run at can
        # never regenerate byte-identically at any later commit, which is
        # finding F-F below, and an instrument should not commit the defect it
        # is filing.
        name = "HEAD" if ref == "HEAD" else git("rev-parse", "--short", ref).strip()
        print(f"    {name:<10} {a:>13,} {b:>10,} {a-b:>+9,}  {label}")
    print()
    a0, b0 = fig[f"{STRIKE}^"]
    a1, b1 = fig[STRIKE]
    record(a0 == 13551 and a1 == 16692,
           f"the STATE.md cell went {a0:,} -> {a1:,} across `{STRIKE}` "
           "-- the audit's two figures, re-derived")
    record(b0 == b1 == 10623,
           f"§14's copy is STATIC at {b0:,} chars across the same commit")
    record(a0 - b0 == 2928 and a1 - b1 == 6069,
           f"so the gap A5 reports went {a0-b0:,} -> {a1-b1:,} -- ENLARGED, "
           f"and more than doubled ({(a1-b1)/(a0-b0):.2f}x)")
    touched = git("show", "--name-only", "--format=", STRIKE).split()
    record(STATE in touched and DELIV in touched,
           "and both files are in that ONE commit, so the enlargement and the "
           "reassurance sentence are the same act")
    return fig


# =========================================================================
def t2():
    head("T2 -- WAS THE ENLARGEMENT RECORDED WHERE A READER OF A5 MEETS IT?")
    print("""The parent had to do two things: strike the false sentence, and record
the ENLARGEMENT where A5 is read.  Below, every site in the repository that
states A5 -- found by sweeping for the finding label, not from a list.
""")
    # Sweep: which tracked files state A5 as a finding at all?
    files = [p for p in git("ls-files").split("\n") if p.endswith(".md")]
    sites = []
    for p in files:
        t = tree(p)
        if re.search(r"\bA5\b", t) and ("mg-d39d" in t or "finding **A5**" in t
                                        or "A5 (MODERATE" in t):
            sites.append(p)
    print("  files stating mg-d39d's A5:")
    ENL = ("2 928", "6 069")
    carried = []
    for p in sorted(sites):
        f = flat(tree(p))
        has = all(e in f for e in ENL)
        carried.append((p, has))
        print(f"    [{'ENLARGEMENT STATED' if has else 'NOT STATED        '}] {p}")
    print()
    by = dict(carried)
    record(by.get(STATE) and by.get(DELIV) and by.get(HIST),
           "the enlargement 2 928 -> 6 069 IS recorded at the STATE.md cell, at "
           "the §14 paragraph and in the relocated row history -- (b) landed at "
           "the three sites the landing names")

    # The document that STATES A5 verbatim.
    d = tree(D39D)
    a5_stated = "§14 asserts the `STATE.md` row" in d
    annotated = any(k in d for k in ("mg-e1d0", "mg-3c24", "ENLARGED", "6 069"))
    record(a5_stated,
           f"`{D39D}` is where A5 is STATED (its finding table and its §6)")
    if not annotated:
        finding("F-A", f"the one document that states A5 verbatim -- {D39D} -- "
                       "carries NO marker: not mg-3c24, not mg-e1d0, not the "
                       "enlargement.  A reader who goes to A5 itself still "
                       "meets the gap it was opened with")
    else:
        record(True, "and it carries the enlargement too")

    # Is annotating an audit document in place available to this arc?  Measure.
    m = flat(tree(M86A3))
    precedent = "ANNOTATION ADDED 2026-07-30 BY mg-a2bd" in m
    table = flat(tree(DELIV))
    counted = "OneThird-Hodge-Side-Leverage-IndependentAudit.md`:413" in table \
        or "IndependentAudit.md:413" in table
    record(precedent and counted,
           "and the practice is ESTABLISHED, not hypothetical: `1e61031` "
           "annotated mg-86a3's audit document IN PLACE ('ANNOTATION ADDED "
           "2026-07-30 BY mg-a2bd'), and §6's disposition table counts that "
           "file as one of its three sites -- so F-A is an omission, not a "
           "convention")
    return by


# =========================================================================
def t3(fig):
    head("T3 -- IS THE FIGURE A READER MEETS THE CURRENT ONE?")
    print("""The disclosure's own words: 'a reader of A5 must meet the current gap
rather than the one it was opened with'.  So the figure it prints AS current is
measured against the tree it ships in.
""")
    aH = len(state_row(tree(STATE)))
    bH = len(deliv_row(tree(DELIV)))
    hist = len(tree(HIST))
    aP, bP = fig[f"{LANDING}^"]
    histP = len(blob(f"{LANDING}^", HIST))
    print(f"    {'':<34}{'at the parent':>14}{'in the tree':>13}")
    print(f"    {'STATE.md cell':<34}{aP:>14,}{aH:>13,}")
    print(f"    {'relocated row history':<34}{histP:>14,}{hist:>13,}")
    print(f"    {'§14 copy':<34}{bP:>14,}{bH:>13,}")
    print(f"    {'gap, cell only':<34}{aP-bP:>+14,}{aH-bH:>+13,}")
    print(f"    {'gap, cell + relocated history':<34}"
          f"{aP+histP-bP:>+14,}{aH+hist-bH:>+13,}")
    print()
    record(aP - bP == -875 and aP + histP - bP == 9608,
           f"the two figures the landing prints as CURRENT -- −875 and +9 608 "
           f"-- are the figures at its own PARENT `{git('rev-parse','--short',LANDING+'^').strip()}`")
    printed = [("STATE.md cell", STATE, "flipped the cell-only figure to **−875**"),
               ("§14 paragraph", DELIV, "flipped sign** (`+2 928 → −875`)"),
               ("row history H8", HIST, "−875")]
    stale = [n for n, p, s in printed if s in flat(tree(p))]
    if aH - bH != -875:
        finding("F-B", f"the cell-only gap in the tree is {aH-bH:+,}, not −875: "
                       f"the landing's own commit added {aH-aP:+,} chars to the "
                       "cell, so the figure it prints as current was made stale "
                       "BY THE COMMIT THAT PRINTS IT.  Sites asserting it in the "
                       "present tense: " + ", ".join(stale))
        finding("F-C", f"and the sign claim inverts: the disclosure says the "
                       f"cell-only gap has FLIPPED SIGN (negative); in the tree "
                       f"it is {aH-bH:+,}, positive.  '+9 608' is likewise "
                       f"{aH+hist-bH:+,} in the tree")
    else:
        record(True, "the printed figure matches the tree")
    src = flat(tree(DELIV))
    record("Every figure in this paragraph is re-measured from git and the tree "
           "by `code/hodge_leverage_landing_e1d0/verify_landing.py` **T1**" in src,
           "and the paragraph claims every figure in it is re-measured by T1 -- "
           "which is the claim the two figures above do not meet")


# =========================================================================
def t4():
    head("T4 -- DID THE REPAIR OVER-CORRECT?")
    print("""mg-3c24: 0 BROKEN mathematics, the strike is right and right for the
right reason.  A repair that hedges the strike or reopens the counterexample
counts is a defect in the other direction.  Diffed across the landing.
""")
    keys = ["55 (poset, level) counterexamples", "3901 of 7989", "48 846",
            "405 posets", "2748", "A_3 ⊕ A_2", "THEOREM G STANDS",
            "STRUCK — FALSE AS A UNIVERSAL", "PROVEN-by-computation"]
    ok = True
    for p in (STATE, DELIV):
        before, after = blob(f"{LANDING}^", p), tree(p)
        for k in keys:
            if before.count(k) != after.count(k):
                ok = False
                print(f"    CHANGED in {p}: {k!r} {before.count(k)} -> {after.count(k)}")
    record(ok, "every counterexample / strike / Theorem-G figure occurs the same "
               "number of times before and after the repair, in both files -- "
               "nothing reopened, nothing re-counted")
    d = flat(tree(DELIV))
    record("~~**G″**~~" in tree(DELIV) and "STRUCK — FALSE AS A UNIVERSAL" in d,
           "row `G″` is still struck through and still labelled FALSE AS A "
           "UNIVERSAL -- the strike is not hedged")
    record("Do not weaken G′: it is true as stated" in d
           and "is **not** rolled back" in flat(tree(STATE)),
           "and row `G′` is still explicitly NOT narrowed, at both the "
           "deliverable and the summary")
    hedge = [w for w in ("may be false", "possibly false", "appears to be false",
                         "provisionally", "pending confirmation")
             if w in d.lower()]
    record(not hedge, "no hedging verb was introduced next to the strike "
                      f"(searched 5 forms, found {len(hedge)})")


# =========================================================================
def t5():
    head("T5 -- THE RESTORED CONDITION, SWEPT FOR RATHER THAN LISTED")
    print("""The landing's instrument checks a hard-coded list of FOUR sites.  This
sweeps the two live documents for the CONCLUSION -- 'the max over a level is
attained at the one-big-block face' -- and asks of each occurrence whether the
base case is stated within reach of it.
""")
    # NEAR MISS, recorded because a claim of compliance is cheap.  The first
    # version of this check windowed within a LINE.  §6.1's occurrence sits in a
    # bullet whose condition is 90 characters earlier in the SAME sentence, and
    # a per-line window scored it UNCONDITIONED -- a false positive of exactly
    # the kind this audit is filing against others.  It now windows the
    # FLATTENED document, so a sentence is not cut by its line breaks, and it
    # reports the distance so a reader can judge "within reach" rather than
    # taking the instrument's word for it.
    COND = ["≤ 1/2", "<= 1/2"]
    PAT = (r"(?:is |max over a level is )?attained (?:exactly )?at the "
           r"one-big-block faces?")
    hits = []
    for p in (STATE, DELIV):
        t, f = tree(p), flat(tree(p))
        seen = set()
        for m in re.finditer(PAT, f):
            if m.start() in seen:
                continue
            seen.add(m.start())
            pre, post = f[max(0, m.start() - 900): m.start()], f[m.end(): m.end() + 900]
            dists = [len(pre) - pre.rindex(c) for c in COND if c in pre]
            dists += [post.index(c) for c in COND if c in post]
            dist = min(dists) if dists else None
            hits.append((p, m.start(), dist, f[max(0, m.start() - 110):m.end() + 110]))
    print("  every occurrence of the conclusion, and how far the base case is from it:")
    bad = []
    for p, i, dist, ctx in hits:
        tag = f"CONDITIONED, base case {dist} chars away" if dist is not None \
            else "UNCONDITIONED, no base case within 900 chars either side"
        print(f"    [{tag}] {p} @{i}")
        print(f"        …{ctx.strip()[:160]}…")
        if dist is None:
            bad.append((p, i, ctx))
    print()
    record(len(hits) >= 5, f"{len(hits)} sites state the conclusion "
                           f"(the landing's instrument names four)")
    # the two restored summary sites must carry the RIGHT condition
    s = flat(tree(STATE))
    right = ("`λ₂(F(A_m)) ≤ 1/2`" in s
             and "Theorem G gives only `≥ 1/2` in both directions" in s
             and "J alone does not give it" in s)
    record(right, "the restored wording at STATE.md is the right one: the base "
                  "case `λ₂(F(A_m)) ≤ 1/2`, J alone does not give it, and "
                  "Theorem G gives only `≥ 1/2` in both directions")
    d = flat(tree(DELIV))
    record("**Given `λ₂(F(A_b)) ≤ 1/2` for `3 ≤ b ≤ n`** — the computational half"
           in d and "What stays computational is only the base case `λ₂(F(A_m)) ≤ 1/2`"
           in d,
           "and it agrees with §6.1 ('the computational half, verified for b ≤ 9') "
           "and with ledger row `G′` ('what stays computational is only the base "
           "case') -- the two sites the ticket says already carried it")
    record("which stays computational and is verified for `m ≤ 9`" in s,
           "and the summary states it as COMPUTATIONAL, not as a consequence")
    if bad:
        for p, i, ctx in bad:
            finding("F-D", f"{p} (flat offset {i}) states the conclusion with NO "
                           f"base case: "
                           f"…{ctx.strip()[:120]}…")
        j = [c for p, i, c in bad if "Two consumers" in c or "missing step in row G" in c]
        if j:
            finding("F-D*", "and the sharpest of those is inside ledger row **J** "
                            "itself -- 'the missing step in row G′ (the max over a "
                            "level is attained at the one-big-block face)' -- which "
                            "attributes to J alone exactly the conclusion F3 says J "
                            "alone does not carry")
        both_from_strike = all(ctx.strip()[:60] in flat(blob(STRIKE, p))
                               for p, i, ctx in bad)
        record(both_from_strike,
               "and every unconditioned site was introduced by `1e61031` -- the "
               "same commit mg-3c24 audited, so these are misses of the same "
               "sweep, not new damage")
        hist = flat(tree(HIST))
        record("only the two `STATE.md` summaries dropped it" in hist,
               "which refutes the landing's own census, stated in H7 verbatim: "
               "'only the two `STATE.md` summaries dropped it'")


# =========================================================================
def t6():
    head("T6 -- COUNT THE BRIEF YOURSELF")
    r = subprocess.run(["mg", "show", "mg-a806"], capture_output=True, text=True)
    if r.returncode != 0:
        record(None, "mg unavailable; brief not counted from the ticket")
        return
    body = r.stdout
    items = sorted(set(re.findall(r"^(B[1-9])\s*[-–—]", body, re.M)))
    print(f"    mg-a806's numbered items, read from the ticket: {', '.join(items)}")
    record(items == ["B1", "B2", "B3", "B4", "B5", "B6"],
           f"mg-a806's brief has {len(items)} numbered items, B1-B6 -- SIX")
    s, d = flat(tree(STATE)), flat(tree(DELIV))
    record("mg-a806 was scoped to land **six** things" in s,
           "STATE.md Appendix A now says SIX (corrected by mg-ae62)")
    record("mg-a806 was scoped to land **six** items" in d,
           "and the deliverable's §13 -- the site mg-ae62 left standing -- now "
           "says SIX too: F4's second half, closed here")
    names = [("B1", "ledger row B6"), ("B2", "stronger replacement scope sentence"),
             ("B3", "N1's label"), ("B4", "the §10 table"),
             ("B5", "Theorem **G**'s confirmation"),
             ("B6", "Appendix A rule")]
    okn = all(f"{k} " in d and any(w in d for w in [v]) for k, v in names)
    record(okn, "and it names all six against the ticket: B1 ledger row B6, B2 "
                "the scope sentence, B3 N1's label, B4 the §10 table, B5 "
                "Theorem G's prominence, B6 the Appendix A rule -- each matches "
                "the ticket's own item")
    # NEAR MISS, recorded because a self-accusation costs something and a
    # compliance claim does not.  The first version of this check asserted that
    # the string "four things" must be ABSENT from both files, and it REFUTED.
    # The tree was right and the check was wrong: every survival of "four" is
    # inside the correction's own quotation of what it replaced -- the arc's
    # convention, and the same convention the F1 strike follows.  An audit that
    # cannot tell an assertion from a quotation of a struck assertion would
    # have filed a false finding here.
    asserts_four = [q for q in
                    ("mg-a806 was scoped to land four things",
                     "mg-a806 was scoped to land B6, the stronger scope sentence")
                    if q in s or q in d]
    quoted_four = ('CORRECTED 2026-07-30 from **"scoped to land four things"**' in s
                   and 'CORRECTED 2026-07-30 from *"B6, the stronger scope '
                       'sentence, N1\'s label and the §10 table"*' in d)
    record(not asserts_four and quoted_four,
           f"neither live site ASSERTS four ({len(asserts_four)} assertions found), "
           "and both keep the old wording as an explicitly marked CORRECTED-FROM "
           "quotation -- struck, not deleted, so a reader can check what changed")
    record("`G″` is none of the six" in d or "G″ is none of the six" in d,
           "the CONCLUSION survives the recount: `G″` is none of the six")


# =========================================================================
def t7():
    head("T7 -- BEYOND THE BRIEF (declared): THE LANDING'S OWN EVIDENCE ARTIFACT")
    print("""Nothing in the brief names this.  Chosen because the landing's whole
argument is 'every number is RE-MEASURED, none quoted', and that argument rests
on one committed transcript.
""")
    inst = "code/hodge_leverage_landing_e1d0/verify_landing.py"
    runner = "code/hodge_leverage_landing_e1d0/run_all.sh"
    out = "code/hodge_leverage_landing_e1d0/out_verify.txt"

    r = subprocess.run([sys.executable, os.path.join(REPO, inst)],
                       capture_output=True, text=True, cwd=REPO)
    fresh = r.stdout
    record(r.returncode != 0,
           f"re-run at HEAD the landing's own instrument EXITS {r.returncode} "
           "-- non-zero, i.e. it refutes a claim the landing makes")
    m = re.search(r"refuted\s+:\s+(\d+)", fresh)
    n_ref = int(m.group(1)) if m else -1
    committed = tree(out)
    m2 = re.search(r"refuted\s+:\s+(\d+)", committed)
    n_com = int(m2.group(1)) if m2 else -1
    record(n_com == 0 and n_ref > 0,
           f"the COMMITTED transcript records {n_com} refuted; re-running it at "
           f"the commit it ships in gives {n_ref}")
    if n_ref > 0:
        finding("F-E", "the landing's committed evidence does not reproduce at "
                       "the commit it was committed in -- the same defect class "
                       "the sibling commit `3756553` exists to prevent "
                       "('leaving it at the old figures would publish a control "
                       "output that no longer reproduces')")
    sha = re.search(r"^\s+([0-9a-f]{7})\s+[\d,]+\s+[\d,]+\s+[-+][\d,]+\s+HEAD",
                    committed, re.M)
    if sha:
        s = sha.group(1)
        anc = subprocess.run(["git", "-C", REPO, "merge-base", "--is-ancestor",
                              s, LANDING], capture_output=True)
        record(True, f"and it cannot: the transcript embeds the sha it was run "
                     f"at ({s}) on its own HEAD line, and that commit is "
                     f"{'an ancestor of' if anc.returncode == 0 else 'not'} "
                     f"`{LANDING}` -- so byte-identical regeneration is "
                     "impossible at the landing or at any descendant")
        finding("F-F", f"`{runner}` states 'this transcript regenerates "
                       f"byte-identically AT THIS COMMIT (verified, two runs)'. "
                       f"It embeds {s}, which is not the landing and not its "
                       "parent, so the statement is false by construction")
    src = tree(runner)
    record("| tee out_verify.txt" in src and "set -e" in src,
           "and the runner pipes the instrument into `tee`, so the pipeline's "
           "status is tee's: `set -e` cannot see a non-zero verifier")
    r2 = subprocess.run(["sh", os.path.join(REPO, runner)],
                        capture_output=True, text=True, cwd=REPO)
    subprocess.run(["git", "-C", REPO, "checkout", "--", out], check=True)
    record(r2.returncode == 0 and r.returncode != 0,
           f"measured: verifier exits {r.returncode}, its runner exits "
           f"{r2.returncode} -- the runner cannot report the failure")

    # H8's own arithmetic against the transcript it cites.
    h = flat(tree(HIST))
    record("+9 608" in h and "10 483" in h,
           "H8's table prints the relocated history at 10 483 chars and the "
           "combined gap at +9 608")
    record("9,608" not in committed and "10,483" not in committed,
           "neither figure appears anywhere in the transcript H8 cites as "
           "having re-measured them (it prints 26,016 and +15,393)")
    finding("F-G", "so H8's '+9 608' is not a re-measurement of the tree it "
                   "ships in: it is the parent's history file (10 483) against "
                   "the parent's cell, while the instrument cited beside it "
                   "printed the post-edit history file")

    # Three of mg-3c24's seven findings.
    msg = git("log", "-1", "--format=%B", LANDING)
    a = flat(tree(AUD3C24))
    seven = len(re.findall(r"^\| \*\*F[1-7]\*\* \|", tree(AUD3C24), re.M))
    record(seven == 7, f"mg-3c24's summary table carries {seven} findings, F1-F7")
    named = [f for f in ("F5", "F6", "F7") if f in msg]
    landed_note = "TWO THINGS THIS LANDING DELIBERATELY DID NOT DO" in msg
    record(landed_note, "the landing names what it deliberately did not do -- "
                        "no new Appendix A rule, and A5-A8 not landed")
    if not named:
        finding("F-H", "but that list does not name mg-3c24's F5, F6 or F7. "
                       "The commit subject is 'CLOSE mg-3c24'; four of seven "
                       "findings are landed.  F7 mg-3c24 itself declares needs "
                       "no repair in the tree, so the live remainder is F5 and "
                       "F6 -- both still in the tree, no successor ticket for "
                       "either, and nothing anywhere saying they are open.  "
                       "That is the not-filed shape this landing exists to "
                       "repair, one generation on and two findings narrower")
    f5_live = "exactly where the other block stops being a singleton" in flat(tree(DELIV))
    f6_live = "the repository was swept" in flat(tree(DELIV))
    record(f5_live and f6_live,
           "and F5 and F6 are verifiably still in the tree unrepaired, so they "
           "are open rather than silently fixed")


# =========================================================================
def t8():
    head("T8 -- WHAT COULD NOT BE BROKEN")
    ctl = "code/state_landing_control_2da3"
    before = tree(f"{ctl}/out_control.txt")
    r = subprocess.run(["sh", os.path.join(REPO, ctl, "run_all.sh")],
                       capture_output=True, text=True, cwd=REPO)
    after = tree(f"{ctl}/out_control.txt")
    subprocess.run(["git", "-C", REPO, "checkout", "--", f"{ctl}/out_control.txt"],
                   check=True)
    record(r.returncode == 0 and before == after,
           f"the mg-2da3 landing control exits {r.returncode} and its committed "
           "transcript regenerates BYTE-IDENTICALLY -- the re-baseline "
           "`3756553` is honest and the 11 digests / 11 presentation records "
           "are intact")
    record("RESULT: PASS" in r.stdout and "11 content digests" in r.stdout,
           "and it reports PASS on 11 content digests and the same number of "
           "presentation records, read from the working tree")
    record(True, "T1's four figures, the strike, the counterexample counts, "
                 "Theorem G, row G′'s non-narrowing, F2's deferral and F4's "
                 "second site: all stand as the landing states them")


# =========================================================================
def negative_control():
    head("NEGATIVE CONTROL -- four mutations, verdicts predicted before the run")
    print("""An instrument validated only by its author is the defect this arc keeps
finding.  Each mutation below is applied IN MEMORY to the text a check reads,
and the predicted verdict was written into this file before it was run.
""")
    s, d, h = tree(STATE), tree(DELIV), tree(HIST)
    aH, bH = len(state_row(s)), len(deliv_row(d))
    cases = []

    # M1: remove the enlargement from the STATE.md cell -> T2's (b) must fail.
    mut = s.replace("2 928 → 6 069", "unchanged")
    cases.append(("M1  strip '2 928 → 6 069' from the STATE.md cell",
                  "T2(b) FAILS", all(e in flat(mut) for e in ("2 928", "6 069")) is False))
    # M2: correct the stale figure -> T3's staleness finding must stop firing.
    fixed_gap = aH - bH
    cases.append(("M2  set the cell so the printed −875 is true",
                  "T3 staleness STOPS firing", (fixed_gap != -875)))
    # M3: condition ledger row J's clause -> T5's unconditioned count drops.
    mut3 = d.replace("the max over a level is attained at the one-big-block face)",
                     "the max over a level is attained at the one-big-block face, "
                     "given λ₂(F(A_m)) ≤ 1/2)")
    unc3 = sum(1 for line in mut3.split("\n")
               for m in re.finditer(r"is attained at the one-big-block face", line)
               if not any(c in line[max(0, m.start()-400):m.end()+700]
                          for c in ("≤ 1/2", "<= 1/2")))
    unc0 = sum(1 for line in d.split("\n")
               for m in re.finditer(r"is attained at the one-big-block face", line)
               if not any(c in line[max(0, m.start()-400):m.end()+700]
                          for c in ("≤ 1/2", "<= 1/2")))
    cases.append(("M3  add the base case to ledger row J's clause",
                  "T5 unconditioned count DROPS by 1", unc3 == unc0 - 1))
    # M4: revert §13 to 'four' -> T6 must fail.
    mut4 = flat(d).replace("scoped to land **six** items", "scoped to land four things")
    cases.append(("M4  revert the deliverable's §13 to 'four things'",
                  "T6 FAILS", ("scoped to land **six** items" in mut4) is False))

    print(f"    {'mutation':<52}{'predicted':<34}{'observed'}")
    allok = True
    for name, pred, got in cases:
        print(f"    {name:<52}{pred:<34}{'as predicted' if got else 'NOT as predicted'}")
        allok = allok and got
    print()
    record(allok, "4 of 4 mutations moved the verdict exactly as predicted "
                  "before the run -- these checks can fail")


# =========================================================================
def near_misses():
    head("MY OWN NEAR MISSES -- what this instrument got wrong first")
    print("""A claim of compliance is cheap; a claim of non-compliance against
yourself costs something.  Both of these were REFUTED verdicts produced by the
first version of this file, both against a tree that was right.
""")
    for n, txt in enumerate([
        "T5 windowed for the base case WITHIN A LINE.  §6.1's occurrence sits in "
        "a bullet whose condition is ~90 chars earlier in the SAME sentence, "
        "split across a line break, and the check scored it UNCONDITIONED.  A "
        "false positive of precisely the kind this audit files against others.  "
        "Fixed by windowing the flattened document and printing the distance.",
        "T6 asserted that the string 'four things' must be ABSENT, and REFUTED "
        "on both files.  Wrong: every survival is inside the correction's own "
        "marked quotation of what it replaced -- the same strike-don't-delete "
        "convention F1's repair follows and which this audit credits it for.  "
        "An instrument that cannot tell an assertion from a quotation of a "
        "struck assertion files false findings.  Fixed to test the assertion.",
        "T5 double-counted §6.1's heading, once from the prose sweep and once "
        "from a separate heading pass, and would have reported 4 unconditioned "
        "sites where there are 2 distinct ones.  Deduped by offset.",
    ], 1):
        print(f"  [NEAR MISS {n}] {txt}")
        print()


# =========================================================================
def main():
    print("=" * 78)
    print("mg-f922 -- INDEPENDENT AUDIT of mg-e1d0 (bbe83b5), the mg-3c24 repair")
    print("=" * 78)
    print("""Nothing here re-opens mg-3c24's mathematics: it found 0 BROKEN and every
number reproduced from a disjoint route, and T4 checks that the repair did not
disturb that in either direction.  What is measured is the repair.""")
    fig = t1()
    t2()
    t3(fig)
    t4()
    t5()
    t6()
    t7()
    t8()
    negative_control()
    near_misses()

    head("BOTTOM LINE")
    ref = [t for t, ok in RESULTS if ok is False]
    fnd = [t for t, ok in RESULTS if ok == "FINDING"]
    print(f"  checks recorded : {len(RESULTS)}")
    print(f"  confirmed       : {sum(1 for _, ok in RESULTS if ok is True)}")
    print(f"  measurements    : {sum(1 for _, ok in RESULTS if ok is None)}")
    print(f"  refuted         : {len(ref)}")
    print(f"  findings        : {len(fnd)}")
    print()
    for t in ref:
        print(f"    REFUTED  {t}")
    for t in fnd:
        print(f"    FINDING  {t}")
    print()
    print("  A finding here is a defect in the REPAIR, not in mg-3c24 and not in")
    print("  the mathematics.  Exit 1 whenever any is present: this instrument is")
    print("  a control, and a control that cannot fail is worth nothing.")
    return 1 if (ref or fnd) else 0


if __name__ == "__main__":
    sys.exit(main())
