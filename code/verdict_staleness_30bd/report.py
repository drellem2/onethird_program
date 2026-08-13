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
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import lib30bd as L                                                # noqa: E402

RECORD = os.path.join(HERE, "sweep_30bd.jsonl")
W = 90


def rule(ch="-"):
    return ch * W


def load():
    if not os.path.exists(RECORD):
        return None, []
    header, suites = None, []
    with open(RECORD, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("kind") == "header":
                header = rec
            else:
                suites.append(rec)
    return header, suites


def main():
    header, suites = load()
    if header is None:
        sys.stderr.write("mg-30bd: no sweep record at %s.  Run sweep.py first; this report "
                         "is a pure function of that file and refuses to invent one.\n"
                         % RECORD)
        return 2

    out = []
    e = out.append

    # ------------------------------------------------------------------ the population
    all_tx = set()
    owned_by_candidate = set()
    rewritten = {}                       # path -> set of dirs that rewrote it
    buckets = {}                         # path -> (bucket, detail, hunk, dropped)
    for s in suites:
        if "error" in s:
            continue
        owned_by_candidate.update(s.get("owned", []))
        for row in s.get("rows", []):
            if not row.get("rewritten"):
                continue
            rewritten.setdefault(row["path"], set()).add(s["dir"])
            prev = buckets.get(row["path"])
            cand = (row["bucket"], row.get("detail", ""), row.get("hunk"),
                    row.get("dropped", 0), s["dir"], "runner")
            # A transcript two suites both rewrite is counted ONCE, under the strongest
            # bucket seen, and both producers are named in the listing.
            if prev is None or _rank(cand[0]) > _rank(prev[0]):
                buckets[row["path"]] = cand

    pass2_rows = {}
    for s in suites:
        for row in s.get("pass2", []) or []:
            pass2_rows[row["path"]] = (row, s["dir"])

    p = subprocess.run(["git", "-C", ROOT, "ls-files", "code"],
                       capture_output=True, text=True)
    all_tx = {r for r in p.stdout.splitlines() if L.lib_f771.is_transcript(r)}

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
    e("  head            : %s" % header["head"])
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
    errored = [s for s in suites if "error" in s]
    timed_out = [s for s in ran if s.get("timeout")]
    not_rewritten = sorted(owned_by_candidate - set(rewritten))
    outside = sorted(all_tx - owned_by_candidate)
    foreign = sorted(pth for pth, ds in rewritten.items()
                     if all(os.path.dirname(pth) != d for d in ds))
    e("")
    e("  %5d  tracked out_*.txt under code/ at this HEAD" % len(all_tx))
    e("  %5d  of them sit in a directory that has a run_all.sh  (the candidates)"
      % len(owned_by_candidate))
    e("  %5d  candidate suite(s) run" % len(ran))
    e("")
    e("  %5d  transcript(s) a runner ACTUALLY REWROTE — the measured population"
      % len(rewritten))
    e("  %5d  transcript(s) in a candidate directory that NO RUNNER TOUCHED" % len(not_rewritten))
    e("  %5d  transcript(s) in a directory with no run_all.sh at all" % len(outside))
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
             L.VERDICT_NUMBER, L.VERDICT_TOKEN, "GONE"]
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
        e("      %-22s %s" % (b, detail))
        e("      regenerated by  %s/run_all.sh" % dname)
        for mark, text in (hunk or []):
            e("      %s %s" % (mark, text[:78]))
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
            e("      %-22s %s" % (row["bucket"], row.get("detail", "")))
            e("      produced by     %s   (in %s, rc=%s)" % (row.get("cmd"), dname, row.get("rc")))
            for mark, text in (row.get("hunk") or []):
                e("      %s %s" % (mark, text[:78]))
            if row.get("dropped"):
                e("      … and %d more verdict line(s) moved" % row["dropped"])
            e("")

    # ------------------------------------------------------------------ blind spots
    e(rule("="))
    e("§6  WHAT THIS METHOD CANNOT SEE — stated per the mayor's instruction to p6e4f")
    e(rule("="))
    e("")
    e("  1  A TRANSCRIPT NO SUITE REGENERATES CANNOT BE CHECKED THIS WAY.  %d tracked" % len(outside))
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
    e("  3  SUITES THAT DID NOT FINISH.  %d timed out at %d s and %d raised."
      % (len(timed_out), header["timeout"], len(errored)))
    for s in timed_out:
        e("       T/O  %s" % s["dir"])
    for s in errored:
        e("       ERR  %s  %s" % (s["dir"], s["error"]))
    e("")
    e("  4  THE TOKEN SET IS A CHOICE, AND §2 STATES BOTH ITS BIASES.  A verdict written in")
    e("     a word nobody put on the list is not counted, and this instrument cannot tell you")
    e("     how many those are — that is what makes §2 the instrument rather than a detail.")
    e("")
    e("  5  AND THE ONE THAT MATTERS MOST: AN ENUMERATION ONLY SEES WHAT IT ENUMERATES.")
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
    e("      54  presumed stale        mg-20ee's original, superseded")
    e("      32  already-stale         the census ground truth — AUTHORITATIVE FOR ADDRESSES")
    e("      %2d  verdict-stale        this measurement, over a DIFFERENT population"
      % (len(vs) + len([p for p in pass2_rows if pass2_rows[p][0].get("bucket") in L.VERDICT_STALE])))
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


def _rank(bucket):
    return {L.IDENTICAL: 0, L.BENIGN_F771: 1, L.BENIGN_ADDR: 2, L.NON_VERDICT: 3,
            "GONE": 4, L.VERDICT_NUMBER: 5, L.VERDICT_TOKEN: 6}.get(bucket, 0)


if __name__ == "__main__":
    sys.exit(main())
