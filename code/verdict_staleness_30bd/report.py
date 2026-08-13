#!/usr/bin/env python3
"""mg-30bd — THE REPORT.  A pure function of the frozen sweep record.

`sweep.py` executes the corpus and takes hours; this reads what it wrote and prints the
count.  The split is deliberate and it is mg-c824's discipline: the MEASUREMENT is a dated
run that cannot be a fixed point, and the INSTRUMENT that reads it must be one, or this
directory joins the population it is measuring on its first re-run.

Exit codes:  0  the sweep record was read and the report printed
             2  there is no sweep record, or it is not this HEAD's

A non-empty verdict-stale list is NOT an error exit.  This instrument REPORTS a population;
it does not gate on it.  Every entry needs an owner per instance — mg-30bd is tagged
`declares-remainder` for exactly that reason — and a runner that exited 1 on a finding would
be asking the next branch to repair 1051 transcripts to get green.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import lib30bd as L                                                # noqa: E402

RECORD = os.path.join(HERE, "sweep_30bd.jsonl")
W = 90

# NOT A BUCKET OF THE CLASSIFIER — a bucket of the HARNESS.  See `_unusable_why`.
UNUSABLE = "UNUSABLE/ungraded"

# The commit whose corpus this sweep measured.  See the header block for why this and not
# `header["head"]` is the identifier of the measurement.
CORPUS_AT = "f2117f1"


def _unusable_why(timed_out, rc):
    """Why a row cannot be graded, or None.

    TWO WAYS A RUN PRODUCES A TRANSCRIPT NOBODY MAY READ AS EVIDENCE:

      killed at the limit — the process was cut off, so the file may be half written, and
        comparing that against the committed copy is THE HARNESS ACCUSING THE CORPUS OF ITS
        OWN TRUNCATION.  mg-479c's defect exactly: a redirect handed mg-f771 a half-written
        file and f771 correctly graded DISAGREES about a redness the harness had caused.

      REFUSED — exit 2.  That is not this instrument's invention: `build.sh` prints the
        convention in its own footer, `0 green · 1 a control fired · 2 refused/broken`, and
        a refusal means the instrument declined to reach a verdict.  A transcript from a run
        that declined is not a measurement of anything.  Exit 1 is NOT in this class: in this
        corpus exit 1 means a control FIRED, which is a completed run with a finding.
    """
    if timed_out:
        return "killed at the limit"
    if rc == 2:
        return "the producing run REFUSED (exit 2)"
    return None


def rule(ch="-"):
    return ch * W


def load():
    if not os.path.exists(RECORD):
        return None, []
    header, bydir, heads = None, {}, set()
    with open(RECORD, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("kind") == "header":
                # THE FIRST HEADER WINS, and this is not a coin toss.  `--fresh` truncates,
                # so the first header in the file is the SWEEP's; every later one belongs to
                # a `--only` re-measurement of one directory and carries `dirs: 1`.  Taking
                # the last one printed "187 suites run, of 1 in the population" — an
                # instrument reporting its own denominator from a correction to itself.
                if header is None:
                    header = rec
                else:
                    heads.add(rec.get("head"))
            else:
                # LAST RECORD PER DIRECTORY WINS.  A re-measurement of one suite is appended
                # to this file rather than edited into it, so the record keeps the run that
                # was superseded and the report reads the newer one.  `sweep.py --only <dir>
                # >> sweep_30bd.jsonl` is the supported way to redo one line of a sweep.
                bydir[rec["dir"]] = rec
    if header is not None:
        heads.discard(header.get("head"))
        header = dict(header, foreign_heads=sorted(heads))
    return header, [bydir[k] for k in sorted(bydir)]


def population(suites):
    """The classification, from the record.  ONE FUNCTION, CALLED AND NOT PARAPHRASED.

    mg-937c's owners arm has to answer `which transcripts are VERDICT-STALE in this record`
    to grade OWNERS.json against it, and that is the same question §3 answers.  Written
    twice, the two answers drift apart into a baseline that is complete against a
    classification the report no longer performs — which is mg-1344's reason for having
    `pin_target()` and section 8 call one `reachable_state_commit()` rather than two.  So
    this was lifted OUT of `main` unchanged and `main` calls it; the control that it is
    unchanged is that `out_verdict_staleness.txt` reproduces byte-identically across the
    lift, and that is checked rather than asserted (README §10).

    Returns (owned_by_candidate, rewritten, buckets, observed, pass2_rows).

    `observed` is the one addition: EVERY graded observation, not only the winning one.
    `buckets` keeps a single row per transcript under the strongest bucket seen, which is
    the right headline and is lossy in one direction that matters — see `disagreement`.
    """
    owned_by_candidate = set()
    rewritten = {}                       # path -> set of dirs that rewrote it
    buckets = {}                         # path -> (bucket, detail, hunk, dropped, dir, src)
    observed = {}                        # path -> [(dir, bucket)] — every observation
    for s in suites:
        if "error" in s:
            continue
        owned_by_candidate.update(s.get("owned", []))
        for row in s.get("rows", []):
            if not row.get("rewritten"):
                continue
            rewritten.setdefault(row["path"], set()).add(s["dir"])
            prev = buckets.get(row["path"])
            # A RUN THAT WAS KILLED AT THE LIMIT LEAVES A TRANSCRIPT THAT MAY BE HALF
            # WRITTEN, AND COMPARING THAT AGAINST THE COMMITTED COPY IS THE HARNESS
            # ACCUSING THE CORPUS OF ITS OWN TRUNCATION.  That is mg-479c's exact defect —
            # a redirect handing mg-f771 a half-written file and f771 correctly grading
            # DISAGREES about a redness the harness caused.  So these rows are NOT graded:
            # they are moved to UNUSABLE, counted, and kept out of every headline.
            why = _unusable_why(s.get("timeout"), s.get("rc"))
            bucket = UNUSABLE if why else row["bucket"]
            observed.setdefault(row["path"], []).append((s["dir"], bucket))
            cand = (bucket, row.get("detail", "") if not why else
                    "%s — would have been %s" % (why, row["bucket"]),
                    row.get("hunk"), row.get("dropped", 0), s["dir"], "runner")
            # A transcript two suites both rewrite is counted ONCE, under the strongest
            # bucket seen, and both producers are named in the listing.
            if prev is None or _rank(cand[0]) > _rank(prev[0]):
                buckets[row["path"]] = cand

    pass2_rows = {}
    for s in suites:
        for row in s.get("pass2", []) or []:
            why = _unusable_why(row.get("timeout"), row.get("rc"))
            if why and row.get("bucket"):
                row = dict(row, detail="%s — would have been %s" % (why, row["bucket"]),
                           bucket=UNUSABLE)
            pass2_rows[row["path"]] = (row, s["dir"])
    return owned_by_candidate, rewritten, buckets, observed, pass2_rows


def stale_set(buckets, pass2_rows):
    """{path: bucket} for every VERDICT-STALE transcript this record reaches, both passes.

    THE ONE DEFINITION OF `THE LIST`.  OWNERS.json is graded against exactly this, so a
    successor who widens or narrows the classifier moves the baseline's population in the
    same edit and the owners arm reports it as growth or as retirement rather than going
    quietly complete against a different question.
    """
    out = {b: v[0] for b, v in buckets.items() if v[0] in L.VERDICT_STALE}
    for pth, (row, _d) in pass2_rows.items():
        if row.get("bucket") in L.VERDICT_STALE:
            out[pth] = row["bucket"]
    return out


def disagreement(path, observed, ran_dirs=()):
    """Two graded observations of ONE transcript at ONE head that DO NOT AGREE, or None.

    Many rewritten transcripts were regenerated by MORE THAN ONE suite, because a suite may
    run a sibling's runner.  `buckets` keeps the STRONGEST bucket seen, which is the right
    headline — a transcript that moved under any producer did move — and it is silent about
    the disagreement.  For some §4 entries there is one, and for a few of those the
    observation that says IDENTICAL is THE TRANSCRIPT'S OWN OWNING RUNNER.  HOW MANY OF
    EACH IS COUNTED IN out_owners_937c.txt §2 AND IS NOT WRITTEN HERE: a count in a
    docstring is a figure nothing regenerates, which is the class this directory exists to
    measure.

    THIS IS REPORTED AND NOT RECLASSIFIED, and the line is deliberate.  Reclassifying would
    move the headline counts, and those are quoted in the README, in §7, in mg-2959's
    commit message and in mg-937c's own title.  Which observation is authoritative is a
    decision ABOUT THE CORPUS and belongs to the owner of the instance; that a decision is
    owed at all is a fact about THE RECORD, and this is the report of the record.  mg-30bd's
    own rule, one level in.
    """
    rows = observed.get(path) or []
    if len(rows) < 2:
        return None
    benign = sorted({d for d, b in rows if b == L.IDENTICAL})
    if not benign:
        return None
    own = os.path.dirname(path)
    stale_dirs = sorted({d for d, b in rows if b in L.VERDICT_STALE})
    if own in benign:
        return ("THE OWNING RUNNER REPRODUCES THIS BYTE-IDENTICALLY and the move above is "
                "%s's regeneration.  Not a verdict move on this record's own evidence — "
                "re-measure before reading one into it (mg-937c)" % ", ".join(stale_dirs))
    if own in stale_dirs:
        return ("%d other suite(s) reproduced this byte-identically (%s); the move above is "
                "the owning runner's, so the finding stands on it.  A measurement "
                "condition, §6.4" % (len(benign), ", ".join(benign)))
    # NEITHER OBSERVATION IS THE OWNER'S, and that is the weakest row §4 can carry: two
    # foreign suites regenerated this transcript at one head and disagreed, and the runner
    # that owns it never ran here at all.  Saying "the finding stands on the owner" would
    # be false of exactly this shape, which is why it is a third branch and not a default.
    return ("NEITHER OBSERVATION IS THE OWNING RUNNER'S — %s says IDENTICAL, %s says the "
            "move, and %s %s.  The listing above is one foreign suite's answer (mg-937c)"
            % (", ".join(benign), ", ".join(stale_dirs), own,
               "contributes no observation of it to this record" if own in ran_dirs
               else "is not a candidate suite at all — it has no run_all.sh"))


def main():
    header, suites = load()
    if header is None:
        sys.stderr.write("mg-30bd: no sweep record at %s.  Run sweep.py first; this report "
                         "is a pure function of that file and refuses to invent one.\n"
                         % RECORD)
        return 2

    out = []
    e = out.append

    owned_by_candidate, rewritten, buckets, observed, pass2_rows = population(suites)

    # THE POPULATION SIZE COMES FROM THE FROZEN RECORD AND NOT FROM `git ls-files`, AND THIS
    # LINE IS THIS INSTRUMENT CATCHING ITS OWN DISEASE.  It WAS a live `git ls-files code`,
    # which meant this transcript's own §1 moved every time anybody added a file to the
    # corpus — a committed report drifting away from the tree it describes, which is exactly
    # what mg-f771 exists to stop and exactly what this directory exists to count.  Caught by
    # rebasing onto a main three commits newer and watching `1051` move.  Everything below is
    # now arithmetic on the header, so the report is a fixed point given the record.
    n_tx = header["transcripts"]

    e(rule("="))
    e("mg-30bd — VERDICT-STALENESS: how many committed transcripts still say something this")
    e("          tree no longer says?")
    e(rule("="))
    e("")
    e("  the question    : mg-20ee's census measures STALE ADDRESSES — `path:NNN` into files")
    e("                    the instrument does not own — and says, correctly of ITS OWN")
    e("                    population, that the verdicts are not affected.  A transcript can")
    e("                    drift in its VERDICTS with no address moving at all, and such a")
    e("                    transcript is invisible to an address classifier BY CONSTRUCTION.")
    e("                    This measures that second class.  IT REPAIRS NOTHING.")
    e("  sweep head      : %s" % header["head"])
    e("  the corpus is   : `main` at %s.  THAT is the sha to quote and the one above is not:" % CORPUS_AT)
    e("                    the sweep head is a BRANCH commit, the refinery rewrites it on")
    e("                    merge, and a record naming a commit that will not exist is")
    e("                    mg-daba's orphan pin in a different file.  The branch adds only")
    e("                    this directory's own sources, which carry no tracked transcripts")
    e("                    and are outside the population by the same test as everything else.")
    e("  method          : re-run each candidate suite in an isolated clone at HEAD, diff")
    e("                    every tracked out_*.txt against its committed copy, classify.")
    e("  per-suite limit : %d s" % header["timeout"])
    e("  produced by     : python3 -B sweep.py  (hours; executes instrument code)")
    e("                    then python3 -B report.py, which is what run_all.sh runs")
    e("")

    e(rule("="))
    e("§1  THE POPULATION, AND THE PART OF IT NO RUNNER REACHES")
    e(rule("="))
    ran = [s for s in suites if "error" not in s]
    ran_dirs = {s["dir"] for s in ran}
    errored = [s for s in suites if "error" in s]
    timed_out = [s for s in ran if s.get("timeout")]
    not_rewritten = sorted(owned_by_candidate - set(rewritten))
    n_outside = n_tx - len(owned_by_candidate)
    foreign = sorted(pth for pth, ds in rewritten.items()
                     if all(os.path.dirname(pth) != d for d in ds))
    e("")
    e("  %5d  tracked out_*.txt under code/ at the swept commit" % n_tx)
    e("  %5d  of them sit in a directory that has a run_all.sh  (the candidates)"
      % len(owned_by_candidate))
    e("  %5d  candidate suite(s) run, of %d in the population" % (len(ran), header["dirs"]))
    if header.get("foreign_heads"):
        e("")
        e("  ⚠️  A RE-MEASUREMENT IN THIS RECORD WAS TAKEN AT A DIFFERENT COMMIT: %s."
          % ", ".join(header["foreign_heads"]))
        e("     Rows from it describe a tree this report does not otherwise describe.")
    if len(ran) < header["dirs"]:
        e("")
        e("  ⚠️  THIS RECORD IS INCOMPLETE — %d of %d suites have no row in it at all, so every"
          % (header["dirs"] - len(ran), header["dirs"]))
        e("     count below is a LOWER BOUND and none of them is a measurement of the corpus.")
    e("")
    e("  %5d  transcript(s) a runner ACTUALLY REWROTE — the measured population"
      % len(rewritten))
    e("  %5d  transcript(s) in a candidate directory that NO RUNNER TOUCHED" % len(not_rewritten))
    e("  %5d  transcript(s) in a directory with no run_all.sh at all" % n_outside)
    e("  %5d  transcript(s) rewritten by a suite that does not own them" % len(foreign))
    e("")
    e("  A TRANSCRIPT ITS OWN RUNNER DOES NOT REWRITE IS NOT EVIDENCE OF ANYTHING.  It is")
    e("  outside this measurement in exactly the way mg-c824's out_a4_census.txt was outside")
    e("  mg-f771's control, and for the same reason: nothing regenerated it, so nothing")
    e("  compared it.  §5 lists them and §6 is what that costs.")
    e("")

    # ------------------------------------------------------------------ the token set
    e(rule("="))
    e("§2  THE TOKEN SET — THIS CHOICE IS THE INSTRUMENT, SO IT IS QUOTED IN FULL")
    e(rule("="))
    e("")
    e("  A line is a VERDICT LINE iff, after normalisation, it contains at least one of")
    e("  these as a WHOLE WORD.  Case-sensitive: this corpus writes graded outcomes in")
    e("  capitals and prose in sentence case, and the case rule is most of the selectivity.")
    e("")
    toks = sorted(header.get("tokens") or L.TOKENS)
    for i in range(0, len(toks), 6):
        e("      " + "  ".join("%-14s" % t for t in toks[i:i + 6]).rstrip())
    e("")
    e("  %d tokens.  A transcript is VERDICT-STALE iff the SORTED MULTISET of its verdict" % len(toks))
    e("  lines differs between the committed copy and the regeneration — after mg-f771's")
    e("  N1/N2/N3 and after this instrument's A1 (a `file.ext:NNN` address) and A2 (a sha, an")
    e("  ISO date, a clock time).  Sorted, so a verdict that only MOVED DOWN THE PAGE is not")
    e("  a verdict that moved.")
    e("")
    e("  WHAT THE CHOICE COSTS, BOTH WAYS:")
    e("    over  — a corpus-size count sharing a line with a token reads as a verdict move.")
    e("            That is why the bucket is split: TOKEN is the strong claim, NUMBER is not.")
    e("    under — a verdict stated in a word not on this list, or in lower case, is invisible.")
    e("")

    # ------------------------------------------------------------------ the counts
    e(rule("="))
    e("§3  THE CLASSIFICATION")
    e(rule("="))
    e("")
    order = [L.IDENTICAL, L.BENIGN_F771, L.BENIGN_ADDR, L.NON_VERDICT,
             L.VERDICT_NUMBER, L.VERDICT_TOKEN, "GONE", UNUSABLE]
    counts = {k: 0 for k in order}
    for pth, (b, _d, _h, _dr, _dir, _src) in buckets.items():
        counts[b] = counts.get(b, 0) + 1
    labels = {
        L.IDENTICAL: "byte-identical to the committed copy",
        L.BENIGN_F771: "BENIGN — mg-f771's N1 checkout path / N2 decimal seconds",
        L.BENIGN_ADDR: "BENIGN — A1 line address / A2 sha, date, clock",
        L.NON_VERDICT: "differs, but in no verdict line (corpus sizes live here)",
        L.VERDICT_NUMBER: "VERDICT-STALE — a number under an unmoved token moved",
        L.VERDICT_TOKEN: "VERDICT-STALE — a verdict TOKEN appeared, vanished or changed",
        "GONE": "the run REMOVED a tracked transcript",
        UNUSABLE: "the producing run was KILLED or REFUSED — not graded, see §6.3",
    }
    for k in order:
        if k in counts:
            e("  %5d  %-22s %s" % (counts[k], k, labels[k]))
    vs = sorted(p for p, v in buckets.items() if v[0] in L.VERDICT_STALE)
    e("")
    e("  " + rule("-")[:86])
    e("  VERDICT-STALE, reachable by a runner: %d  (%d token, %d number)"
      % (len(vs), counts.get(L.VERDICT_TOKEN, 0), counts.get(L.VERDICT_NUMBER, 0)))
    e("  " + rule("-")[:86])
    e("")
    e("  %d further transcript(s) came from a run this sweep KILLED AT THE LIMIT, or from one"
      % counts.get(UNUSABLE, 0))
    e("  that REFUSED (exit 2, build.sh's own convention).  They are NOT in the number above")
    e("  and NOT in any number in this report: a half-written or declined transcript compared")
    e("  against its committed copy is the harness accusing the corpus of its own truncation,")
    e("  which is mg-479c's defect exactly.  They are UNMEASURED, not clean.  Exit 1 is NOT in")
    e("  this class — in this corpus that means a control FIRED, which is a completed run.")
    e("")

    # ------------------------------------------------------------------ the list
    e(rule("="))
    e("§4  THE VERDICT-STALE TRANSCRIPTS, WITH THE LINES THAT MOVED")
    e(rule("="))
    e("")
    e("  `-` is the committed copy, `+` is this tree.  Quoted after normalisation, so this")
    e("  transcript cannot itself smuggle a worktree path into the corpus.")
    e("")
    if not vs:
        e("  none.")
    for pth in vs:
        b, detail, hunk, dropped, dname, _src = buckets[pth]
        e("  %s" % pth)
        e("      %-22s %s" % (b, short_detail(detail)))
        e("      regenerated by  %s/run_all.sh" % dname)
        note = walk_note(hunk or [])
        if note:
            e("      NOTE  %s" % note)
        note = disagreement(pth, observed, ran_dirs)
        if note:
            e("      NOTE  %s" % note)
        for mark, text in show(hunk or []):
            e("      %s %s" % (mark, text))
        if dropped:
            e("      … and %d more verdict line(s) moved" % dropped)
        e("")

    # ------------------------------------------------------------------ pass 2
    e(rule("="))
    e("§5  THE RUNNER-BLIND PASS — TRANSCRIPTS THEIR OWN RUNNER DID NOT REWRITE")
    e(rule("="))
    e("")
    if not header.get("pass2"):
        e("  NOT RUN in this sweep.  The %d transcript(s) in §1's second line are unmeasured."
          % len(not_rewritten))
    else:
        e("  A runner can decline to produce a transcript — most often because an earlier step")
        e("  in it failed and it exited.  mg-6cb9 is exactly that and it is the instance this")
        e("  whole ticket came from, so a sweep that stopped at runners would have MISSED THE")
        e("  ONE KNOWN MEMBER OF THE POPULATION IT WAS COMMISSIONED TO COUNT.  This pass takes")
        e("  the producing command out of the runner's own text and runs it alone.  A producer")
        e("  the parser cannot see is reported `unparsed` and is NOT guessed at.")
        e("")
        st = {}
        for pth, (row, _d) in sorted(pass2_rows.items()):
            st[row["status"]] = st.get(row["status"], 0) + 1
        for k in sorted(st):
            e("  %5d  %s" % (st[k], k))
        p2vs = sorted(pth for pth, (row, _d) in pass2_rows.items()
                      if row.get("bucket") in L.VERDICT_STALE)
        p2b = {}
        for pth, (row, _d) in pass2_rows.items():
            if row.get("bucket"):
                p2b[row["bucket"]] = p2b.get(row["bucket"], 0) + 1
        e("")
        for k in order:
            if k in p2b:
                e("  %5d  %-22s %s" % (p2b[k], k, labels[k]))
        e("")
        e("  " + rule("-")[:86])
        e("  VERDICT-STALE, reachable only by bypassing the runner: %d" % len(p2vs))
        e("  " + rule("-")[:86])
        e("")
        for pth in p2vs:
            row, dname = pass2_rows[pth]
            e("  %s" % pth)
            e("      %-22s %s" % (row["bucket"], short_detail(row.get("detail", ""))))
            e("      produced by     %s   (in %s, rc=%s)" % (row.get("cmd"), dname, row.get("rc")))
            note = walk_note(row.get("hunk") or [])
            if note:
                e("      NOTE  %s" % note)
            for mark, text in show(row.get("hunk") or []):
                e("      %s %s" % (mark, text))
            if row.get("dropped"):
                e("      … and %d more verdict line(s) moved" % row["dropped"])
            e("")

    # ------------------------------------------------------------------ blind spots
    e(rule("="))
    e("§6  WHAT THIS METHOD CANNOT SEE — stated per the mayor's instruction to p6e4f")
    e(rule("="))
    e("")
    e("  1  A TRANSCRIPT NO SUITE REGENERATES CANNOT BE CHECKED THIS WAY.  %d tracked" % n_outside)
    e("     transcripts sit in a directory with no run_all.sh; nothing here regenerates them,")
    e("     so nothing here compares them, and they are outside every number above.  This is")
    e("     mg-f771's own declared hole (its §1: \"a transcript no suite rewrites is never")
    e("     modified and therefore never appears below\") one level out.")
    e("")
    e("  2  A RUNNER THAT DECLINES.  %d transcript(s) in candidate directories were not"
      % len(not_rewritten))
    e("     rewritten by their runner at all.  §5 reaches the ones whose producer is written")
    e("     in the runner as a plain redirect; the rest stay unmeasured.")
    e("")
    unfinished = len(timed_out) + len(errored)
    e("  3  SUITES THAT DID NOT FINISH, AS A COVERAGE BOUND AND NOT ONLY A LIST.")
    e("     %d of %d suite(s) — %.1f%% — produced no usable answer: %d timed out at %d s and"
      % (unfinished, len(ran), 100.0 * unfinished / max(1, len(ran)), len(timed_out),
         header["timeout"]))
    e("     %d raised.  A timed-out suite may have rewritten SOME of its transcripts before"
      % len(errored))
    e("     the limit, so its rows are kept and are NOT evidence that the rest agree — size")
    e("     every total above against this fraction.")
    for s in timed_out:
        e("       T/O  %s" % s["dir"])
    for s in errored:
        e("       ERR  %s  %s" % (s["dir"], s["error"]))
    e("")
    e("  4  THE ANSWER DEPENDS ON THE LOAD IT WAS TAKEN UNDER, which is a measurement")
    e("     condition and not a caveat.  Suites here mutate a worktree and restore it, and")
    e("     several check the restore by comparing `git status` (and .pyc mtimes) across a")
    e("     probe — so a loaded host makes them REFUSE where a quiet one does not.  MEASURED,")
    e("     ON THE INSTANCE THIS TICKET IS ABOUT: code/species_extent_audit_6cb9's")
    e("     a1_bothways.py exited 2 under host load 40-50 during the full sweep, and exits 0")
    e("     reproducing p6e4f exactly when re-run alone.  Anyone re-taking this sweep should")
    e("     expect the UNGRADED count to move with the machine, and should re-measure a")
    e("     refusal on one worker before reading anything into it.")
    e("")
    e("  5  THE TOKEN SET IS A CHOICE, AND §2 STATES BOTH ITS BIASES.  A verdict written in")
    e("     a word nobody put on the list is not counted, and this instrument cannot tell you")
    e("     how many those are — that is what makes §2 the instrument rather than a detail.")
    e("")
    e("  6  AND THE ONE THAT MATTERS MOST: AN ENUMERATION ONLY SEES WHAT IT ENUMERATES.")
    e("     Everything above is a per-suite loop, so a transcript no loop entry reaches is")
    e("     invisible however the classifier is tuned.  THE THING THAT CATCHES WHAT AN")
    e("     ENUMERATION MISSES IS A WHOLE-RUN BEFORE/AFTER DIFF — run the corpus, diff the")
    e("     tree, and read what moved without having decided in advance what could.  mg-6cb9")
    e("     was found that way (by accident, by p6e4f, while pinning something else) and not")
    e("     by any enumeration, including this one.")
    e("")

    e(rule("="))
    e("§7  WHAT THIS DOES TO THE REPORTED NUMBERS")
    e(rule("="))
    e("")
    total_vs = len(vs) + len([q for q in pass2_rows
                              if pass2_rows[q][0].get("bucket") in L.VERDICT_STALE])
    e("    %4d  presumed stale     mg-20ee's original, superseded" % 54)
    e("    %4d  already-stale      the census ground truth — AUTHORITATIVE FOR ADDRESSES" % 32)
    e("    %4d  verdict-stale      this measurement, over a DIFFERENT population" % total_vs)
    e("")
    e("  %d DOES NOT SUPERSEDE 32 AND IT DOES NOT CONTAIN IT.  That is the misreading this" % total_vs)
    e("  section exists to stop: the two are counts of DIFFERENT POPULATIONS under different")
    e("  questions, and neither is a correction of the other.  32 remains the authoritative")
    e("  already-stale ADDRESS count and this report does not touch it.")
    e("")
    e("  THE TWO NUMBERS ARE NOT NESTED AND MUST NOT BE ADDED WITHOUT SAYING SO.  mg-20ee's")
    e("  44 candidates are the transcripts that carry a foreign `path:NNN`; this population is")
    e("  the transcripts whose GRADED STATEMENTS moved.  A transcript can be in either, both,")
    e("  or neither — code/species_extent_audit_6cb9 is in the second and NOT in the first,")
    e("  which is why nobody had counted it.")
    e("")
    e("  Anything quoting 32 as \"the staleness in the corpus\" is quoting one of two classes.")
    e("")
    print("\n".join(out))
    return 0


WALK = None


def _walk_re():
    global WALK
    if WALK is None:
        import re
        # A `<sha> <subject>` line: what a `git log` walk prints once the sha has been
        # masked by A2.  Named, not repaired: a transcript that QUOTES COMMIT SUBJECTS moves
        # whenever history moves, which is mg-e720's family ("unbounded history walks scored
        # as verdicts"), and adjudicating each instance is the successor's job, not this
        # instrument's.  Counted so a reader can see the cause without re-deriving it.
        WALK = re.compile(r"^\s*(?:HEAD:\s*)?<sha>\s+\S")
    return WALK


def show(rows):
    """Render a hunk so a `-`/`+` pair NEVER prints as two identical lines.

    The first version truncated at column 78 and printed pairs whose visible halves were
    letter-for-letter equal — a report that shows a difference by showing no difference.
    Here the window slides to the first differing character.
    """
    out = []
    for i, (mark, text) in enumerate(rows):
        other = None
        if mark == "-" and i + 1 < len(rows) and rows[i + 1][0] == "+":
            other = rows[i + 1][1]
        elif mark == "+" and i and rows[i - 1][0] == "-":
            other = rows[i - 1][1]
        cut = 0
        if other is not None:
            n = min(len(text), len(other))
            j = next((k for k in range(n) if text[k] != other[k]), n)
            if j > 70:
                cut = j - 24
        body = ("…" + text[cut:cut + 77]) if cut else text[:78]
        out.append((mark, body))
    return out


def short_detail(detail, limit=108):
    """A token delta over 28 words is unreadable as one line, so it is cut WITH ITS COUNT.
    A silent truncation reads as `that was all of it` (mg-502f)."""
    if len(detail) <= limit:
        return detail
    parts = detail.split(", ")
    kept, n = [], 0
    for part in parts:
        if n + len(part) + 2 > limit:
            break
        kept.append(part)
        n += len(part) + 2
    return ", ".join(kept) + ", … and %d more token(s)" % (len(parts) - len(kept))


def walk_note(rows):
    n = sum(1 for _m, t in rows if _walk_re().match(t))
    if not n:
        return None
    return ("%d of %d quoted line(s) are `<sha> <subject>` — a history walk, so this moves "
            "when main moves (mg-e720's family)" % (n, len(rows)))


def _rank(bucket):
    return {L.IDENTICAL: 0, L.BENIGN_F771: 1, L.BENIGN_ADDR: 2, L.NON_VERDICT: 3,
            "GONE": 4, L.VERDICT_NUMBER: 5, L.VERDICT_TOKEN: 6}.get(bucket, 0)


if __name__ == "__main__":
    sys.exit(main())
