#!/usr/bin/env python3
"""mg-132a -- A FIGURE'S PROVENANCE IS WHERE IT WAS COMPUTED, NOT WHERE IT CAME
TO REST.

THE DEFECT.  `repair_7e39.py` repaired mg-7e39's F2 -- "a population figure that
was already wrong at the commit which published it" -- with a check keyed on
`publishing_commit(rel)`, which is `git log -1 -- rel`.  At `94ecf9d` that check
is RED on the two transcripts it was built to protect: both publish 473 and the
tree at their publishing commit holds 481.

AND THEY WERE RIGHT WHEN WRITTEN.  The pre-merge commits `8a07ae0` and `3d7b32f`
hold exactly 473.  THE MERGE REBASED THEM onto a tree that had grown.  `git
log -1` follows the file to its new resting place, so THE COMMIT THAT PUBLISHES
EACH FIGURE IS NO LONGER THE COMMIT IT WAS MEASURED AT.

F2 was "wrong when written".  This is the complementary failure, and the repair's
vocabulary has no word for it: `STALE` is one word doing four jobs.

THE DECISION, WHICH IS THE DELIVERABLE.  The ticket names two coherent answers:
(1) regenerate the transcripts at the commit that now publishes them, or (2)
stop keying on `git log -1` and record the commit the figure was MEASURED at.

  ⚠️ THIS FILE TAKES (2), AND THE REASON IS A FACT ABOUT THE TREE RATHER THAN A
  PREFERENCE: THE ANCHOR WAS ALREADY PUBLISHED.  `repair_ec07.py`'s
  `population_line()` has been writing "473 .py files swept, walked from the
  WORKING TREE at HEAD 8a07ae01fc45" all along, and `repair_7e39.py` prints
  `HEAD : 3d7b32fdd240` at the head of its own transcript.  Both transcripts
  NAME THE TREE THEY MEASURED.  The checker was reading the wrong field.

  (1) is not rejected -- it is demoted from RULE to REPAIR.  It is what you do
  when (2) cannot be satisfied, because an unanchored figure has no way back
  except a re-run.

THE PRICE OF (2), STATED RATHER THAN HIDDEN.  A reader can meet 473 beside a
tree of 481 and this check stays green.  That is only tolerable because the
figure names its own tree.  The instant the anchor stops resolving, 473 becomes
an unfalsifiable assertion in a file -- so A1b makes an unresolvable anchor RED,
every anchor is verified by RE-DERIVING the count at the named rev rather than
believing it (A2c is the control), and the declared anchor line carries a DIGEST
OF THE POPULATION so that a figure whose anchor commit has been pruned can still
be located (A2d).

SIX VERDICTS WHERE THERE WAS ONE WORD, `STALE`:

  AGREES              anchor verified, and the publishing tree holds it too.
  DISPLACED           anchor verified; the publishing tree holds something else.
                      RIGHT WHEN WRITTEN, MOVED BY A REBASE.  Green, and named.
                      It has lost CURRENCY, not TRUTH, and those are different.
  WRONG WHEN WRITTEN  the anchor resolves and its tree does NOT hold the
                      figure.  RED.  This is mg-7e39's F2 proper.
  UNANCHORED          the transcript names no commit that resolves.  RED --
                      a figure that names no tree cannot be checked against
                      one, which is a stronger defect than being out of date.
  UNRESOLVABLE        an anchor was declared and is gone.  RED unless the
                      digest recovers it.
  INCONSISTENT        the declared anchor's `count=` disagrees with the figure
                      the transcript publishes.  RED, and ⚠️ NO TREE LOOKUP
                      COULD SEE IT: whichever tree is named, one of the two
                      numbers matches.  This rung exists because the first
                      version of A2d built exactly that forgery by accident and
                      the run refuted it -- a defect of this instrument, kept
                      rather than smoothed away.

THE GAP THAT LET IT THROUGH, AND WHAT THIS FILE CAN AND CANNOT DO ABOUT IT.
Nothing re-runs the staleness check after a merge.  The publication step this
repair separates from prose is THE RUN; the step that broke it is THE MERGE, and
the merge is performed by the refinery, outside this tree.  ⚠️ SO THIS FILE DOES
NOT CLAIM TO CLOSE IT.  What it does is make the audit runnable AT ANY COMMIT
(`--at <rev>`), so a post-merge check is one command, and say plainly in its own
transcript that A COMMITTED `0 REFUTED` IS A MEASUREMENT AT THE RUN'S COMMIT AND
NOT A LIVE PROPERTY.  A deliverable that claimed otherwise would be making this
defect one level up.

Pure Python 3 + git.  No third-party packages.  Import-safe: everything runs
under `__main__`, because `repair_7e39.py` LOADS this module for its S4 rather
than keeping a second copy of the lattice (`8c55168`: two copies of `figures()`
disagreeing on 3).
"""

import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))

# How far back the digest recovery search is willing to walk.  ⚠️ NAMED AND
# PRINTED rather than silent: a bounded search that reports "not found" without
# saying how far it looked is a scope nobody chose.
RECOVERY_LIMIT = 800


def git(*args, repo=None):
    return subprocess.run(["git", "-C", repo or REPO, *args],
                          capture_output=True, text=True).stdout


def git_ok(*args, repo=None):
    return subprocess.run(["git", "-C", repo or REPO, *args],
                          capture_output=True, text=True).returncode == 0


# --------------------------------------------------------------------------
# THE POPULATION, AND ITS DIGEST
# --------------------------------------------------------------------------
# ⚠️ ONE DEFINITION OF THE FIGURE REGEX IN THE TREE.  `repair_7e39.py` imports
# this name rather than keeping its own copy.  The repository has already been
# bitten by two copies of `figures()` disagreeing on 3.
POP_FIGURE = re.compile(r"(\d[\d,  ]*)\s*`?\.py`?\s+files")

_POP_CACHE = {}


def py_files_at(rev):
    """Every `.py` under `code/` IN THE TREE AT `rev`, from `git ls-tree`.  The
    working directory is a different object from any commit, and confusing the
    two is how 429 came to be committed beside a tree of 448."""
    if rev not in _POP_CACHE:
        out = git("ls-tree", "-r", "--name-only", rev, "code/")
        _POP_CACHE[rev] = sorted(p for p in out.split("\n") if p.endswith(".py"))
    return _POP_CACHE[rev]


def population_digest(rev):
    """A digest of the POPULATION ITSELF -- the sorted path list, not the count.

    ⚠️ THIS IS WHAT MAKES A RECORDED COMMIT FALSIFIABLE AFTER IT IS PRUNED.  A
    recorded sha alone is an assertion that dies with the object; a digest can
    be searched for.  It digests the PATHS rather than the count because two
    different populations of the same size are two different facts."""
    return hashlib.sha256("\n".join(py_files_at(rev)).encode()).hexdigest()[:16]


def resolve(rev):
    """The full sha of `rev` if it names a commit OBJECT in this repository,
    else None.  Deliberately not `--is-ancestor`: an object rebased off the
    mainline still resolves, and whether it is REACHABLE is a separate question
    this file reports separately (A6) rather than folding into resolution."""
    out = subprocess.run(["git", "-C", REPO, "rev-parse", "--verify", "-q",
                          f"{rev}^{{commit}}"], capture_output=True, text=True)
    return out.stdout.strip() or None


# --------------------------------------------------------------------------
# THE ANCHOR
# --------------------------------------------------------------------------
# The line a publication step SHOULD write.  ⚠️ IT CARRIES NO POPULATION FIGURE
# IN `POP_FIGURE`'s GRAMMAR -- no `.py files` -- so declaring an anchor cannot
# change which number a reader (or this checker) reads as the figure.  A2c
# asserts that rather than trusting it.
DECLARED = re.compile(
    r"^\s*POPULATION ANCHOR: commit=([0-9a-f]{40}) count=(\d+) "
    r"digest=([0-9a-f]{16}) scope=(\S+)\s*$", re.M)

# The compatibility path for transcripts written before the declared line
# existed: any 12--40 hex token.  Both live transcripts carry one.
HEX = re.compile(r"\b[0-9a-f]{12,40}\b")


def anchor_line(rev):
    """The declared anchor a publication step emits for `rev`."""
    return (f"POPULATION ANCHOR: commit={resolve(rev)} "
            f"count={len(py_files_at(rev))} digest={population_digest(rev)} "
            f"scope=code/**/*.py")


def read_anchor(text, figure):
    """The commit this transcript says it MEASURED, as
    `(kind, commit, detail)`.

    DECLARED is strong: the run wrote the sha down, and nothing about the
    figure was used to pick it.

    ⚠️ INFERRED IS WEAKER AND IS LABELLED SO EVERYWHERE IT IS REPORTED.  For a
    legacy transcript the anchor is recovered by resolving the hex tokens in
    its text and keeping those whose tree yields the figure -- which SELECTS
    FOR AGREEMENT, and therefore CANNOT WITNESS `WRONG WHEN WRITTEN`.  That is
    a real hole in the compatibility path and it is stated rather than
    smoothed away: a transcript is only fully checkable once its publication
    step declares its anchor.  What inference CAN still witness is
    `UNANCHORED` -- naming no resolvable commit at all -- and that is the
    verdict the original F2 transcript earns (A5)."""
    m = DECLARED.search(text)
    if m:
        sha, count, digest, scope = m.groups()
        return "DECLARED", sha, {"count": int(count), "digest": digest,
                                 "scope": scope}
    resolved, matching = [], []
    for tok in dict.fromkeys(HEX.findall(text)):
        full = resolve(tok)
        if not full:
            continue
        resolved.append((tok, full))
        if figure is not None and len(py_files_at(full)) == figure:
            matching.append((tok, full))
    if matching:
        return "INFERRED", matching[0][1], {"resolved": resolved,
                                            "matching": matching}
    return "NONE", None, {"resolved": resolved, "matching": []}


def digest_matches(digest, as_of):
    """Every commit in the searched window whose `code/` population has
    `digest`, newest first, with the size of the window walked.

    ⚠️ `--all`, NOT JUST `as_of`.  A rebased measurement commit is by
    construction off the mainline; searching only the audited rev's ancestry
    would refuse to find exactly the commits this repair exists to find.  The
    price is that recovery depends on what refs still exist, which is why A1d
    measures that exposure instead of assuming it away.

    ⚠️ AND IT RETURNS A LIST, BECAUSE THE MAP IS MANY-TO-ONE.  A digest
    identifies a POPULATION, not a COMMIT: 8 commits reachable from `94ecf9d`
    share one `code/` population, because a commit that adds no `.py` file
    leaves it untouched.  That is SUFFICIENT to verify a COUNT -- every commit
    with this digest has the same file list, so it has the same count -- and
    INSUFFICIENT to identify provenance uniquely.  A recovered anchor answers
    "a tree holding exactly this population existed", which is the falsifiable
    half; it does not answer "and it was that commit"."""
    revs = [r for r in git("rev-list", f"-n{RECOVERY_LIMIT}", "--all",
                           as_of).split("\n") if r]
    return [r for r in revs if population_digest(r) == digest], len(revs)


def recover_by_digest(digest, as_of):
    """The newest commit whose `code/` population has `digest`.  This is the
    half of (2) that keeps a pruned anchor falsifiable.  Returns
    `(sha_or_None, walked, n_matching)`."""
    hits, walked = digest_matches(digest, as_of)
    return (hits[0] if hits else None), walked, len(hits)


# --------------------------------------------------------------------------
# THE VERDICT LATTICE -- ONE DEFINITION, FED BY TEXT
# --------------------------------------------------------------------------
def verdict_from_text(text, publishing, as_of, recover=True):
    """The verdict for a transcript's TEXT published at `publishing`, audited as
    of `as_of`.

    ⚠️ IT TAKES TEXT, NOT A PATH.  That is what lets the controls in A5 feed it
    a COPY of a real transcript with one token changed and show each verdict
    actually firing, instead of asserting that the lattice has five rungs."""
    v = {"publishing": publishing, "figure": None, "anchor": None,
         "anchor_kind": None, "anchor_count": None, "published_count":
         len(py_files_at(publishing)), "verdict": None, "note": "",
         "reachable": None}
    m = POP_FIGURE.search(text)
    if not m:
        v["verdict"] = "NO FIGURE"
        v["note"] = "publishes no `.py` population figure"
        return v
    v["figure"] = int(re.sub(r"\D", "", m.group(1)))

    kind, sha, detail = read_anchor(text, v["figure"])
    v["anchor_kind"] = kind

    if kind == "NONE":
        v["verdict"] = "UNANCHORED"
        v["note"] = (f"names no commit whose tree yields {v['figure']} "
                     f"({len(detail['resolved'])} hex token(s) in it resolve "
                     f"to commits at all)")
        # A figure that names SOME tree, none of which holds it, is a stronger
        # statement than one that names none: the first is refuted, the second
        # is uncheckable.  Both are RED and they are told apart in the note.
        if detail["resolved"]:
            v["verdict"] = "WRONG WHEN WRITTEN"
            v["note"] = ("names " + ", ".join(
                f"{t[:12]} (holds {len(py_files_at(f))})"
                for t, f in detail["resolved"][:4]) +
                f" -- and NONE of them holds {v['figure']}")
        return v

    if kind == "DECLARED":
        # ⚠️ THE DECLARED LINE IS CHECKED AGAINST THE TRANSCRIPT IT SITS IN,
        # BEFORE ANY TREE IS CONSULTED.  A publication step that computes the
        # anchor's `count=` and the prose figure by two different routes can
        # disagree with ITSELF, and no amount of `git ls-tree` would notice --
        # whichever tree it named, one of the two numbers would match.  That is
        # F2's shape inside a single file, and A2g is the control for it.
        if detail["count"] != v["figure"]:
            v["verdict"] = "INCONSISTENT"
            v["note"] = (f"its own declared anchor line says count="
                         f"{detail['count']} while the transcript publishes "
                         f"{v['figure']} -- the file disagrees with itself "
                         f"before any tree is consulted")
            return v
        full = resolve(sha)
        if full is None:
            if recover:
                got, walked, n = recover_by_digest(detail["digest"], as_of)
                if got:
                    v["anchor"], v["anchor_kind"] = got, "RECOVERED"
                    v["recovered_from"] = n
                    v["note"] = (f"declared anchor {sha[:12]} does not "
                                 f"resolve; RECOVERED BY DIGEST "
                                 f"{detail['digest']} at {got[:12]} -- one of "
                                 f"{n} commit(s) with that population, found "
                                 f"by walking {walked}")
                else:
                    v["verdict"] = "UNRESOLVABLE"
                    v["note"] = (f"declared anchor {sha[:12]} does not resolve "
                                 f"and none of the {walked} commit(s) searched "
                                 f"holds digest {detail['digest']}")
                    return v
            else:
                v["verdict"] = "UNRESOLVABLE"
                v["note"] = f"declared anchor {sha[:12]} does not resolve"
                return v
        else:
            v["anchor"] = full
    else:
        v["anchor"] = sha

    # ⚠️ THE ANCHOR IS VERIFIED, NEVER BELIEVED.  The count is RE-DERIVED from
    # `git ls-tree` at the named rev.  A recorded commit that is merely stated
    # is exactly the unfalsifiable assertion in a file that (2) is accused of
    # being, and this line is the whole answer to that accusation.
    v["anchor_count"] = len(py_files_at(v["anchor"]))
    v["reachable"] = git_ok("merge-base", "--is-ancestor", v["anchor"], as_of)

    if v["anchor_count"] != v["figure"]:
        v["verdict"] = "WRONG WHEN WRITTEN"
        v["note"] = (f"the tree at its own declared anchor {v['anchor'][:12]} "
                     f"holds {v['anchor_count']}, not {v['figure']}")
    elif v["published_count"] != v["figure"]:
        v["verdict"] = "DISPLACED"
        v["note"] = (f"right when written -- {v['figure']} at "
                     f"{v['anchor'][:12]} -- and rebased onto a tree of "
                     f"{v['published_count']} at {publishing[:12]}")
    else:
        v["verdict"] = "AGREES"
        v["note"] = (f"{v['figure']} at its anchor {v['anchor'][:12]} and at "
                     f"the commit that publishes it")
    return v


def publishing_commit(rel, as_of="HEAD"):
    """The commit at or before `as_of` that last wrote `rel`.  KEPT, and no
    longer load-bearing: under (2) it answers "where did this come to rest",
    which is a different question from "where was this measured" and is
    reported BESIDE the anchor rather than in place of it."""
    return git("log", "-1", "--format=%H", as_of, "--", rel).strip() or None


def verdict_for(rel, as_of="HEAD"):
    """The verdict for the transcript `rel` AS PUBLISHED -- read from git at its
    own publishing commit, never from the working tree.

    ⚠️ THE WORKING TREE IS DELIBERATELY IGNORED, for the reason
    `repair_7e39.py` gives and for one more: this instrument's own transcript
    is truncated on disk by the redirect that is about to write it, so a check
    that read from disk could not reach its own author."""
    pub = publishing_commit(rel, as_of)
    if pub is None:
        return {"rel": rel, "verdict": "UNPUBLISHED", "publishing": None,
                "note": "never committed at or before this rev, so nothing is "
                        "published yet -- this row becomes a measurement at "
                        "the commit that lands it",
                "figure": None, "anchor": None, "anchor_kind": None,
                "anchor_count": None, "published_count": None,
                "reachable": None}
    v = verdict_from_text(git("show", f"{pub}:{rel}"), pub, as_of)
    v["rel"] = rel
    return v


# Every place in this arc that PUBLISHES a `.py` population for the sweep.
COMPUTED = ["code/hodge_leverage_repair_6df0/out_repair_6df0.txt",
            "code/hodge_leverage_repair_3f3b/out_repair_3f3b.txt",
            "code/publication_anchor_132a/out_anchor_132a.txt"]

# The verdicts that make a run RED.  DISPLACED is deliberately absent: that is
# the decision this deliverable is.
RED = {"WRONG WHEN WRITTEN", "UNANCHORED", "UNRESOLVABLE", "INCONSISTENT"}


# --------------------------------------------------------------------------
# THE RUN
# --------------------------------------------------------------------------
RESULTS = []


def record(ok, desc):
    RESULTS.append((desc, ok))
    tag = {True: "CONFIRMED", False: "REFUTED  ", None: "MEASURED "}[ok]
    print(f"  [{tag}] {desc}")


def head(t):
    print(f"\n{t}\n{'-' * len(t)}")


def show(v):
    mark = "⚠️" if v["verdict"] in RED else "  "
    print(f"    {mark} {v['rel']}")
    print(f"        verdict   : {v['verdict']}"
          + (f"  (anchor {v['anchor_kind']})" if v["anchor_kind"] else ""))
    if v["figure"] is not None:
        print(f"        publishes : {v['figure']}")
        print(f"        anchor    : "
              + (f"{v['anchor'][:12]} holds {v['anchor_count']}"
                 f"   reachable from the audited rev: "
                 f"{'YES' if v['reachable'] else 'NO'}"
                 if v["anchor"] else "none that resolves"))
        if v["publishing"]:
            print(f"        published : {v['publishing'][:12]} holds "
                  f"{v['published_count']}")
    print(f"        {v['note']}")


def main(argv):
    as_of = "HEAD"
    if "--at" in argv:
        as_of = argv[argv.index("--at") + 1]
    as_of = resolve(as_of) or sys.exit(f"cannot resolve --at {as_of}")

    print("=" * 78)
    print("mg-132a -- a figure's provenance is WHERE IT WAS COMPUTED, not "
          "where it came to rest")
    print("=" * 78)
    print(f"    audited as of            : {as_of[:12]}")
    print(f"    {len(py_files_at(as_of))} .py files under `code/` in the tree "
          f"at that rev")
    print(f"    {anchor_line(as_of)}")
    print()
    print("""⚠️  THIS TRANSCRIPT IS A MEASUREMENT AT THE COMMIT ABOVE, NOT A LIVE PROPERTY OF
    THE REPOSITORY.  A committed `0 REFUTED` says the audit passed WHEN IT RAN.
    The step that broke the check this file repairs was not a run -- it was A
    MERGE, which rebased two transcripts onto a tree that had grown, and nothing
    re-runs after one.  Re-run with `--at <rev>` after any merge; that is what
    the flag is for.  A deliverable that printed `0 REFUTED` and let you read it
    as `0 now` would be committing this defect one level up.
""")

    a1(as_of)
    a2(as_of)
    a3(as_of)

    head("SUMMARY")
    ok = sum(1 for _d, v in RESULTS if v is True)
    meas = sum(1 for _d, v in RESULTS if v is None)
    bad = [d for d, v in RESULTS if v is False]
    print(f"    checks          : {len(RESULTS)}")
    print(f"    confirmed       : {ok}")
    print(f"    measured        : {meas}")
    print(f"    refuted         : {len(bad)}")
    for d in bad:
        print(f"      REFUTED: {d[:170]}")
    return 1 if bad else 0


# --------------------------------------------------------------------------
# A1 -- THE POPULATION, AT THE COMMIT IT WAS MEASURED AT
# --------------------------------------------------------------------------
def a1(as_of):
    head("A1 -- EVERY PUBLISHED FIGURE, AGAINST THE TREE IT WAS MEASURED AT")
    print("""`publishing_commit()` is `git log -1`, which follows a file to wherever a
rebase puts it.  So the two questions are asked separately here: WHERE WAS THIS
MEASURED (the anchor, re-derived) and WHERE DID IT COME TO REST (the publishing
commit).  They agreed until a merge, and the merge is why one word could not
carry both.
""")
    vs = [verdict_for(rel, as_of) for rel in COMPUTED]
    for v in vs:
        show(v)
    print()

    live = [v for v in vs if v["verdict"] != "UNPUBLISHED"]
    unpub = [v["rel"] for v in vs if v["verdict"] == "UNPUBLISHED"]
    wrong = [v for v in live if v["verdict"] == "WRONG WHEN WRITTEN"]
    record(not wrong,
           f"A1a of the {len(live)} published transcript(s) that carry a `.py` "
           f"population, {len(wrong)} are WRONG WHEN WRITTEN -- the tree at "
           f"the commit each one NAMES AS ITS OWN does not hold the figure it "
           f"publishes.  This is mg-7e39's F2 proper, and it is the only "
           f"question `git log -1` was ever able to answer by accident.  "
           f"{len(unpub)} are not published at this rev and are named rather "
           f"than counted as passes: {unpub}")

    unver = [v for v in live if v["verdict"] in ("UNANCHORED", "UNRESOLVABLE")]
    record(not unver,
           f"A1b {len(unver)} published figure(s) cannot be checked against "
           f"ANY tree -- naming no commit that resolves, or naming one that is "
           f"gone and not recoverable by digest.  ⚠️ THIS IS THE GATE THAT "
           f"KEEPS (2) HONEST.  Recording the measurement commit is only an "
           f"improvement on `git log -1` while that record is VERIFIABLE; an "
           f"anchor nobody can resolve is an unfalsifiable assertion in a "
           f"file, and is worse than a wrong number because a wrong number can "
           f"at least be refuted")

    disp = [v for v in live if v["verdict"] == "DISPLACED"]
    record(None,
           f"A1c {len(disp)} figure(s) are DISPLACED: right when written and "
           f"rebased onto a tree that had grown -- "
           + "; ".join(f"{v['rel'].split('/')[-1]} {v['figure']} at "
                       f"{v['anchor'][:7]} now published at "
                       f"{v['publishing'][:7]} which holds "
                       f"{v['published_count']}" for v in disp) +
           f".  ⚠️ NOT RED, AND THAT IS THE DECISION.  A displaced figure has "
           f"lost CURRENCY, not TRUTH; it remains a correct statement about a "
           f"named tree.  The remedy is answer (1) -- re-run at the commit "
           f"that now publishes it -- and this row is where a reader learns "
           f"that it is owed")

    unreach = [v for v in live if v["anchor"] and not v["reachable"]]
    record(None,
           f"A1d {len(unreach)} verified anchor(s) are NOT REACHABLE from the "
           f"audited rev -- "
           + "; ".join(f"{v['anchor'][:7]} for {v['rel'].split('/')[-1]}"
                       for v in unreach) +
           f".  ⚠️ THIS IS WHAT (2) COSTS, MEASURED RATHER THAN ARGUED.  A "
           f"rebase leaves the measurement commit off the mainline; it "
           f"survives on whatever side ref still points at it and dies at the "
           f"next `git gc`.  The digest in the declared anchor line is the "
           f"answer to that, and A2d is where it is demonstrated -- but the "
           f"two legacy transcripts predate the line and have no digest, so "
           f"for them this row is an unfixed exposure, named")

    legacy = [v for v in live if v["anchor_kind"] == "INFERRED"]
    record(None,
           f"A1e {len(legacy)} anchor(s) are INFERRED rather than DECLARED, by "
           f"resolving the hex tokens in the transcript's own text: "
           + "; ".join(f"{v['rel'].split('/')[-1]} -> {v['anchor'][:7]}"
                       for v in legacy) +
           f".  ⚠️ AN INFERRED ANCHOR IS WEAKER THAN A DECLARED ONE AND THE "
           f"WEAKNESS IS STRUCTURAL: inference keeps the tokens whose tree "
           f"YIELDS the figure, so it SELECTS FOR AGREEMENT and can never "
           f"witness `WRONG WHEN WRITTEN` on a legacy transcript.  It can "
           f"still witness `UNANCHORED`, which is what the original F2 "
           f"transcript earns at A2a.  A transcript is only fully checkable "
           f"once its own publication step declares its anchor")


# --------------------------------------------------------------------------
# A2 -- THE CONTROLS: EVERY VERDICT SHOWN FIRING ON REAL COMMITS
# --------------------------------------------------------------------------
ORIGINAL_F2 = ("77306a7", "code/hodge_leverage_repair_6df0/out_repair_6df0.txt")
PRE_REBASE, POST_REBASE = "c1a57fd", "3958b5a"


def a2(as_of):
    head("A2 -- THE CONTROLS: EACH VERDICT SHOWN FIRING, ON THIS REPOSITORY")
    print("""A lattice with five rungs is a claim about a lattice.  Each rung below is
demonstrated on real commits of this repository -- including one where the
defect is still present -- rather than asserted.
""")

    # A2a -- the original F2, caught by a different route than the old rule.
    rev, rel = ORIGINAL_F2
    full = resolve(rev)
    v = verdict_from_text(git("show", f"{full}:{rel}"), full, as_of)
    v["rel"] = f"{rel} @ {rev} (mg-7e39's F2, before any repair)"
    show(v)
    record(v["verdict"] == "UNANCHORED",
           f"A2a THE ORIGINAL DEFECT, ON THE COMMIT WHERE IT IS STILL PRESENT: "
           f"the transcript at {rev} publishes {v['figure']} against a tree of "
           f"{v['published_count']}, and this rule calls it "
           f"`{v['verdict']}` -- {v['note']}.  ⚠️ CAUGHT BY A DIFFERENT ROUTE "
           f"THAN THE OLD RULE, AND A STRICTER ONE: not `the number disagrees "
           f"with its tree` but `IT NAMES NO TREE`.  A figure that names none "
           f"cannot be right or wrong, only unchecked -- which is why 429 "
           f"survived a publication step at all")

    # A2b -- the same bytes, two commits, two verdicts.  The rebase, visible.
    pre, post = resolve(PRE_REBASE), resolve(POST_REBASE)
    rel6 = COMPUTED[0]
    t_pre = git("show", f"{pre}:{rel6}")
    t_post = git("show", f"{post}:{rel6}")
    v_pre = verdict_from_text(t_pre, pre, pre)
    v_post = verdict_from_text(t_post, post, as_of)
    for lbl, vv in ((f"{PRE_REBASE} (pre-rebase)", v_pre),
                    (f"{POST_REBASE} (post-rebase)", v_post)):
        vv["rel"] = f"{rel6} @ {lbl}"
        show(vv)
    record(t_pre == t_post and v_pre["verdict"] == "AGREES"
           and v_post["verdict"] == "DISPLACED",
           f"A2b THE SAME BYTES, TWO COMMITS, TWO VERDICTS: "
           f"`out_repair_6df0.txt` is byte-identical at {PRE_REBASE} and "
           f"{POST_REBASE} ({'identical' if t_pre == t_post else 'DIFFERENT'}) "
           f"and this rule reads it `{v_pre['verdict']}` at the first and "
           f"`{v_post['verdict']}` at the second.  ⚠️ NOTHING ABOUT THE FILE "
           f"CHANGED -- THE MERGE MOVED IT.  This is the failure the repair's "
           f"vocabulary had no word for, in one row, and it is why the "
           f"publication step cannot be the only thing that recomputes: no "
           f"run happened between these two commits")

    # A2c -- WRONG WHEN WRITTEN, on a COPY with one token changed.
    #
    # ⚠️ A COPY OF A REAL TRANSCRIPT, ONE TOKEN SUBSTITUTED, both commits real.
    # Constructing the case is the only way to show this rung firing on a
    # DECLARED anchor, because no declared anchor in the tree is wrong -- and a
    # rung nobody has seen fire is a rung nobody has tested.
    # ⚠️ THE FORGED ANCHOR IS INTERNALLY CONSISTENT: it states the count the
    # transcript publishes, so the cheap `INCONSISTENT` rung cannot catch it and
    # the only thing left that can is RE-DERIVING THE COUNT AT THE NAMED REV.
    # That is the whole of what makes (2) a check rather than a note, so the
    # control has to be built so nothing else could have caught it.
    bad_rev = resolve("77306a7")
    forged = (f"POPULATION ANCHOR: commit={bad_rev} count={v_post['figure']} "
              f"digest={population_digest(v_post['anchor'])} "
              f"scope=code/**/*.py\n" + t_post)
    v_bad = verdict_from_text(forged, post, as_of)
    v_bad["rel"] = (f"COPY of out_repair_6df0.txt + a SELF-CONSISTENT DECLARED "
                    f"anchor at 77306a7 (which holds "
                    f"{len(py_files_at(bad_rev))})")
    show(v_bad)
    record(v_bad["verdict"] == "WRONG WHEN WRITTEN"
           and v_bad["anchor_kind"] == "DECLARED",
           f"A2c `WRONG WHEN WRITTEN` FIRES ON A DECLARED ANCHOR: a copy of a "
           f"real transcript publishing {v_post['figure']}, with a declared "
           f"anchor that AGREES WITH THE TRANSCRIPT (count="
           f"{v_post['figure']}) and names 77306a7, whose tree actually holds "
           f"{len(py_files_at(bad_rev))}.  Verdict `{v_bad['verdict']}`.  The "
           f"declared line is believed about WHICH COMMIT and never about WHAT "
           f"IT HOLDS -- the count is RE-DERIVED from `git ls-tree`, which is "
           f"the whole of what makes (2) a check rather than a note.  ⚠️ "
           f"NOTHING CHEAPER COULD HAVE CAUGHT THIS ONE: the file agrees with "
           f"itself, so only the tree can refute it")

    # A2d -- the digest recovers an anchor whose commit is gone.
    #
    # ⚠️ THE ANCHOR PLANTED HERE IS INTERNALLY CONSISTENT -- its `count=` and
    # its digest are the audited rev's own, and the text publishes that same
    # figure.  The first version of this control planted 3958b5a's count beside
    # a text publishing 473 and the run REFUTED it, correctly: the forgery was
    # self-contradictory and A2g now exists because of it.  A control that only
    # ever passed would have hidden that.
    n_now = len(py_files_at(as_of))
    lost = ("POPULATION ANCHOR: commit=" + "0" * 39 + "1 "
            f"count={n_now} digest={population_digest(as_of)} "
            f"scope=code/**/*.py\n"
            f"    {n_now} .py files under `code/` at the audited rev\n")
    v_lost = verdict_from_text(lost, as_of, as_of)
    v_lost["rel"] = "SYNTHETIC transcript with a DECLARED anchor whose commit does not exist"
    show(v_lost)
    record(v_lost["anchor_kind"] == "RECOVERED"
           and v_lost["verdict"] not in RED
           and v_lost["anchor_count"] == n_now,
           f"A2d THE DIGEST BUYS BACK A PRUNED ANCHOR: an anchor sha that "
           f"names no object recovers to {(v_lost['anchor'] or '')[:12]}, "
           f"whose `code/` population re-derives to {v_lost['anchor_count']} "
           f"-- the figure the transcript publishes -- so the verdict is "
           f"`{v_lost['verdict']}` rather than RED.  ⚠️ THIS IS THE ANSWER TO "
           f"THE STRONGEST OBJECTION AGAINST (2), that a recorded commit "
           f"becomes an unfalsifiable assertion once it is pruned.  The "
           f"figure survives its own anchor")

    # A2e -- and it must FAIL when there is nothing to recover.
    gone = ("POPULATION ANCHOR: commit=" + "0" * 39 + f"1 count={n_now} "
            "digest=" + "f" * 16 + " scope=code/**/*.py\n"
            f"    {n_now} .py files under `code/` at the audited rev\n")
    v_gone = verdict_from_text(gone, as_of, as_of)
    v_gone["rel"] = "SYNTHETIC, anchor gone AND a digest no tree holds"
    show(v_gone)
    record(v_gone["verdict"] == "UNRESOLVABLE",
           f"A2e AND RECOVERY FAILS CLOSED: an anchor that does not resolve "
           f"and a digest no tree in the searched history holds reads "
           f"`{v_gone['verdict']}` and is RED.  A recovery that could only "
           f"succeed would be a blessing, not a check")

    # A2f -- the declared line must not be readable as the figure.
    record(POP_FIGURE.search(anchor_line(as_of)) is None,
           f"A2f the declared anchor line is NOT itself readable as a "
           f"population figure -- `POP_FIGURE` finds nothing in "
           f"`{anchor_line(as_of)[:58]}...`.  Adding provenance to a "
           f"transcript must not change which number a reader, or this "
           f"checker, takes as the figure.  Predicted, and asserted rather "
           f"than left to the phrasing")


    # A2g -- the file disagreeing with ITSELF, which no tree lookup can see.
    forged2 = (f"POPULATION ANCHOR: commit={post} "
               f"count={len(py_files_at(post))} "
               f"digest={population_digest(post)} scope=code/**/*.py\n"
               + t_post)
    v_inc = verdict_from_text(forged2, post, as_of)
    v_inc["rel"] = "COPY of out_repair_6df0.txt + a TRUE anchor for the WRONG figure"
    show(v_inc)
    record(v_inc["verdict"] == "INCONSISTENT",
           f"A2g A DECLARED ANCHOR THAT IS TRUE ABOUT ITS TREE AND WRONG ABOUT "
           f"ITS FILE: the anchor line above names {post[:7]} and states "
           f"count={len(py_files_at(post))}, both correct, inside a transcript "
           f"that publishes {v_post['figure']}.  Verdict "
           f"`{v_inc['verdict']}`.  ⚠️ NO AMOUNT OF `git ls-tree` COULD CATCH "
           f"THIS -- whichever tree is consulted, one of the two numbers "
           f"matches it.  A publication step that computes the anchor and the "
           f"prose figure by two routes can disagree with itself, which is "
           f"F2's shape inside a single file.  THIS ROW EXISTS BECAUSE THE "
           f"FIRST VERSION OF A2d BUILT EXACTLY THIS FORGERY BY ACCIDENT AND "
           f"THE RUN REFUTED IT")

    # A2h -- the many-to-one property, measured rather than glossed.
    hits, walked = digest_matches(population_digest(as_of), as_of)
    record(None,
           f"A2h A DIGEST WITNESSES A POPULATION, NOT A COMMIT: "
           f"{len(hits)} of the {walked} commit(s) searched share the audited "
           f"rev's `code/` population digest {population_digest(as_of)}, "
           f"because a commit that adds no `.py` file leaves the population "
           f"untouched.  That is ENOUGH to verify a COUNT -- every one of them "
           f"has the same file list -- and NOT ENOUGH to identify provenance "
           f"uniquely.  A recovered anchor answers 'a tree holding exactly "
           f"this population existed', which is the falsifiable half, and does "
           f"not answer 'and it was that commit'.  Stated here rather than "
           f"left for a reader to discover that `RECOVERED` is weaker than "
           f"`DECLARED`")

    # A2i -- how exposed the two legacy anchors actually are.
    n473, _ = digest_matches(population_digest("8a07ae0"), as_of)
    reach = [r for r in n473
             if git_ok("merge-base", "--is-ancestor", r, as_of)]
    record(None,
           f"A2i AND THE EXPOSURE IS TOTAL FOR THE TWO LEGACY FIGURES: "
           f"{len(n473)} commit(s) in the object store hold the population the "
           f"473 figures were measured against, and {len(reach)} of them are "
           f"reachable from the audited rev.  ⚠️ THE PRE-MERGE TREES SURVIVE "
           f"ONLY ON `origin/polecat-3f3b`.  Delete that branch, run `git gc`, "
           f"and 473 becomes permanently uncheckable -- no digest to search by "
           f"and no tree left to find.  This is not an argument against (2); "
           f"it is the measurement of what (2) inherited, and the only remedy "
           f"for these two files specifically is answer (1), a re-run")

# --------------------------------------------------------------------------
# A3 -- THIS DELIVERABLE, AND THE GAP IT CANNOT CLOSE
# --------------------------------------------------------------------------
MINE_REL = "code/publication_anchor_132a/anchor_132a.py"
OUT_REL = "code/publication_anchor_132a/out_anchor_132a.txt"


def a3(as_of):
    head("A3 -- THIS DELIVERABLE, CHECKED BY ITS OWN RULE")
    print("""This deliverable is of the same kind as the defect it repairs: it publishes
figures with provenance.  So it is put through its own lattice, read FROM GIT at
its own publishing commit -- and the run that writes this transcript is the run
that reads the last committed one.
""")
    mine = verdict_for(OUT_REL, as_of)
    show(mine)
    record(mine["verdict"] not in RED,
           f"A3a THIS INSTRUMENT'S OWN TRANSCRIPT reads `{mine['verdict']}` "
           f"under the rule it ships -- {mine['note']}.  ⚠️ A CHECK THAT "
           f"CANNOT BE APPLIED TO ITS AUTHOR IS A SCOPE NOBODY CHOSE, and this "
           f"is the row that would go red first if the argument in this file "
           f"were wrong")

    # ⚠️ THE ORDER OF THIS BRANCH'S COMMITS IS PART OF THE DESIGN, and it is
    # read out of git rather than asserted.
    pred = git("log", "--format=%H", as_of, "--",
               "code/publication_anchor_132a/PREDICTIONS.md").strip().split("\n")
    first_instr = git("log", "--format=%H", as_of, "--",
                      MINE_REL).strip().split("\n")
    ordered = bool(pred[-1] and first_instr[-1]) and git_ok(
        "merge-base", "--is-ancestor", pred[-1], first_instr[-1]) \
        and pred[-1] != first_instr[-1]
    record(ordered,
           f"A3b PREDICTIONS BEFORE INSTRUMENT, FROM `git log`: "
           f"`PREDICTIONS.md` first appears at {(pred[-1] or 'NOT YET '
           'COMMITTED')[:7]} and `anchor_132a.py` at "
           f"{(first_instr[-1] or 'NOT YET COMMITTED')[:7]}, and the first is "
           f"an ancestor of the second.  'Decided before measuring' is a claim "
           f"about the repository and is read out of git here rather than "
           f"asserted in prose.  ⚠️ THIS ROW IS RED ON A RUN FROM AN "
           f"UNCOMMITTED WORKING TREE, and that is correct rather than "
           f"inconvenient: before the instrument is committed there is no "
           f"ordering in git to read, and a row that went green on the absence "
           f"of evidence would be the defect this deliverable is about")

    # A3c -- the gap, stated as a limit rather than a fix.
    hooks = [p for p in ("../../.git/hooks/post-merge", "../../.git/hooks/post-rewrite")
             if os.path.exists(os.path.join(HERE, p))]
    record(None,
           f"A3c THE GAP THIS DELIVERABLE DOES NOT CLOSE, NAMED: nothing in "
           f"this tree re-runs the check after a merge -- {len(hooks)} "
           f"post-merge/post-rewrite hook(s) exist ({hooks}).  The rebase that "
           f"produced this defect is performed by the refinery, OUTSIDE the "
           f"repository, and no artifact committed inside it can run after "
           f"one.  ⚠️ WHAT IS DELIVERED INSTEAD IS `--at <rev>`, so the audit "
           f"is ONE COMMAND against any commit including a post-merge one, and "
           f"the banner above, which says that a committed `0 REFUTED` is a "
           f"measurement at the run's commit.  Claiming the gap closed would "
           f"be this deliverable committing the defect it repairs")

    # A3d -- and the flag is shown to work, not just offered.
    earlier = resolve(f"{as_of}~1")
    other = [verdict_for(rel, earlier) for rel in COMPUTED[:2]]
    record(all(v["verdict"] != "NO FIGURE" for v in other),
           f"A3d `--at` IS EXERCISED, NOT MERELY OFFERED: the same lattice run "
           f"as of {earlier[:7]} gives "
           + "; ".join(f"{v['rel'].split('/')[-1]} -> {v['verdict']}"
                       for v in other) +
           f".  A flag that is documented and never run is a plan; this row is "
           f"the audit answering at a commit that is not HEAD, which is what a "
           f"post-merge re-check will be")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
