#!/usr/bin/env python3
"""mg-937c — THE OWNERS ARM.  Does every verdict-stale transcript have an owner, and HAS
THE LIST GROWN?

mg-30bd measured 150 and repaired none of them, which was its ticket's instruction, and it
declared two things it did not have the standing to do: give every entry an owner per
instance (README §8 item 1) and set a baseline so that something could say the list had
grown (item 2).  They are ONE piece of work and this arm is why — a baseline that is not a
list of things somebody read is a number that launders whatever was true on the day it was
taken, so `OWNERS.json` is both, and you cannot declare the baseline without naming a cause
for every row of it.

Exit codes:  0  every stale entry has a row, and no row's class has strengthened
             1  A FINDING IN THIS DIRECTORY'S OWN FILES — the list has grown, or a hand
                field in OWNERS.json is contradicted by the record
             2  no sweep record, or no OWNERS.json

WHY EXIT 1 IS RIGHT HERE AND WRONG FOR `report.py`, which is the same distinction
run_all.sh already draws between report.py and the prose arm.  `report.py` reports a
population of findings ABOUT THE CORPUS, none of which this directory may repair, and a
runner that exited 1 on a non-empty list would ask the next branch to repair 150
transcripts to get green — mg-e35b's red-on-improvement.  THIS arm grades `OWNERS.json`,
which is this directory's own file, and every finding it can raise is repairable in the
same commit: add the row, or fix the field.  A gate on somebody else's work is
red-on-improvement; a gate on your own is just a gate.

AND THE POLARITY OF THE OTHER DIRECTION IS THE HALF THAT MATTERS.  A row whose transcript
has been REPAIRED — so it is no longer stale — is GREEN and prints the deletion to make.
Going red because somebody fixed one of the 150 would be the exact shape this arm exists
under, one level in.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import lib30bd as L                                                # noqa: E402
import report as R                                                 # noqa: E402

OWNERS = os.path.join(HERE, "OWNERS.json")
W = 90


def rule(ch="-"):
    return ch * W


def gated_suites(build_sh):
    """The suites `./build.sh` actually runs, read out of build.sh rather than listed here.

    A hand list would be a second definition of the gate, and build.sh's own header exists
    to stop there being one ("There is exactly one definition of what the gate IS").  So
    this reads the file: any `code/<dir>/<something>.sh` token that is not inside a comment.
    """
    out = set()
    for line in build_sh.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        for tok in stripped.replace("\\", " ").split():
            if tok.startswith("code/") and tok.endswith(".sh"):
                out.add(os.path.dirname(tok))
    return out


def f771_scope():
    """What mg-f771's committed g0 transcript declares its subject to be, READ rather than
    quoted from memory.

    §1 makes a claim about another directory's control, and a hand-typed quotation of one is
    a figure backed by nothing — mg-2959's whole finding, in the directory that found it.  So
    the line is read.

    IT USED TO READ THE `VERDICT:` LINE AND THERE IS NO LONGER ONE (mg-c15e).  That is not a
    regression in either directory: g0's transcript was mg-f771's single self-exemption
    precisely BECAUSE it carried the verdict — the file was committed by the same act that
    repaired what it reported, so 16 of its 31 committed versions were red and 7 commits of
    main exist for nothing but flipping it back.  The exemption is gone and the verdict went
    with it, to the exit status and to stderr.  What this arm was actually using it for is the
    SCOPE and not the outcome — the sentence below is about which files g0 compares — so the
    scope line is what is read now, and it is a better citation than the one it replaces: it
    is invariant under a gate run, where the verdict never was.
    """
    p = os.path.join(ROOT, "code", "gate_fixed_point_f771", "out_g0_fixed_point.txt")
    if not os.path.exists(p):
        return "nothing — its transcript is not in this tree"
    for line in open(p, encoding="utf-8"):
        if line.strip().startswith("every tracked file under code/"):
            return "`%s`" % line.strip().rstrip(".")
    return "no watched-class line"


def load_owners():
    if not os.path.exists(OWNERS):
        return None
    with open(OWNERS, encoding="utf-8") as fh:
        return json.load(fh)


def quoted_lines(buckets, pass2):
    """Every quoted line the record holds, as (path, masked text).

    ONE definition, called by `grade()` and by §6a/§6b alike.  mg-1344's rule: two copies of
    `which lines the record quotes` drift into an arm graded against a population its own
    report no longer reports, and this list is now the input to a hand file.
    """
    lines = []
    for pth, tup in sorted(buckets.items()):
        for _m, t in (tup[2] or []):
            lines.append((pth, t))
    for pth, (row2, _d) in sorted(pass2.items()):
        for _m, t in (row2.get("hunk") or []):
            lines.append((pth, t))
    return lines


def grade(header, suites, doc):
    """Every finding this arm can raise, as data.  Returned rather than printed so the
    planted worlds in §6 can run the SAME function over a mutated world and read its
    answer, instead of scraping the text of a report."""
    # THE DECLARATION CENSUS IS PASSED THROUGH, NOT RE-DERIVED (mg-5491).  Same reason the
    # two functions below are imported rather than paraphrased: a baseline graded against a
    # population the report no longer reports has gone quietly complete against a different
    # question.
    owned, rew, buckets, observed, pass2 = R.population(suites, header.get("declared"))
    ran = {s["dir"] for s in suites if "error" not in s}
    stale = R.stale_set(buckets, pass2)
    rows = doc["rows"]

    f = {"grown": [], "strengthened": [], "retired": [], "weakened": [],
         "bad_read": [], "bad_disagree": [], "bad_vocab": [],
         "walk_unread": [], "walk_stale": [], "walk_notwalk": []}

    for pth in sorted(stale):
        cls = "token" if stale[pth] == L.VERDICT_TOKEN else "number"
        row = rows.get(pth)
        if row is None:
            f["grown"].append((pth, cls))
            continue
        if row["class"] != cls:
            # number -> token is the STRONG direction and is growth: the same transcript
            # now carries a moved verdict WORD where it carried only a moved number.
            (f["strengthened"] if cls == "token" else f["weakened"]).append(
                (pth, row["class"], cls))

    # A ROW LEAVES THE STALE LIST FOR THREE DIFFERENT REASONS AND ONLY TWO OF THEM ARE GOOD
    # NEWS.  mg-937c printed one line for all three — `DELETE this row from OWNERS.json` —
    # and mg-5491 found the third by using it: re-measuring four suites turned
    # `code/species_bound_repair_5040/out_r2_wiring.txt` from stale into RETIRED, and the
    # reason was NOT that anybody repaired it.  The only two suites that had ever graded it
    # stale stopped rewriting it, and the runner-blind pass that reached it was KILLED AT THE
    # LIMIT.  So the record now contains no grade for it at all, and deleting its row would
    # have shrunk the baseline by an UNMEASURED transcript while the arm stayed green.
    # That is the shape this whole directory exists to catch, inside the remedy for it.
    # `observed` DELIBERATELY KEEPS THE CLASSIFIER'S REAL ANSWER for a declared transcript —
    # that is what §3b's false-declaration check reads — so `DECLARED` has to be asked of the
    # CENSUS and not of the observations.  Asking the observations would classify every
    # declared row as UNMEASURED, which is the opposite of true.
    decl = R.honoured(header.get("declared"))
    for pth in sorted(rows):
        if pth in stale:
            continue
        seen = [b for _d, b in observed.get(pth, [])]
        p2b = (pass2[pth][0].get("bucket") if pth in pass2 else None)
        if pth in decl:
            why = "DECLARED"
        elif any(b in L.BENIGN for b in seen) or p2b in L.BENIGN:
            why = "REPRODUCES"
        else:
            why = "UNMEASURED"
        f["retired"].append((pth, rows[pth]["class"], why))

    # ---- the hand fields that ARE falsifiable ------------------------------------------
    for pth, row in sorted(rows.items()):
        if row["cause"] not in doc["causes"] or row["disposition"] not in doc["dispositions"]:
            f["bad_vocab"].append((pth, row["cause"], row["disposition"]))
        if pth not in stale:
            continue
        runner = pth in buckets and buckets[pth][0] in L.VERDICT_STALE
        dropped = (buckets[pth][3] if runner else pass2[pth][0].get("dropped", 0)) or 0
        want = "sample" if dropped else "full"
        if row.get("read") != want:
            f["bad_read"].append((pth, row.get("read"), want, dropped))
        # `RECORD-DISAGREES` is a claim ABOUT THE RECORD, so the record decides it.  A
        # cause that cannot be checked is a cause that rots; this is the one that can be,
        # and it is checked in BOTH directions so the field cannot be quietly dropped
        # either.
        note = R.disagreement(pth, observed, ran)
        own_benign = bool(note and not note.startswith("%d other" % 0)) and (
            note.startswith("THE OWNING RUNNER") or note.startswith("NEITHER"))
        if own_benign != (row["cause"] == "RECORD-DISAGREES"):
            f["bad_disagree"].append((pth, row["cause"], own_benign))

    # ---- mg-cda7: the PER-LINE hand list, graded in BOTH directions --------------------
    # `walk_lines` is the third column §6b needs, and it is a hand file, so it rots exactly
    # the way OWNERS.json's rows would without this arm.  Two checks, and the second is the
    # one that matters: an in-family line with no entry is UNREAD — a new HISTORY-WALK row
    # arriving quietly is how the list would go complete against a corpus that moved — and an
    # entry naming a line the record no longer holds is STALE.  Neither is a judgement.
    # THE THIRD IS THE GATE THE OUT COLUMN COULD NOT PROVIDE: the SHIPPED rule taking a line
    # somebody read as NOT-WALK is a NOTE printed on a line that is not a history walk.
    walk_paths = {p for p, r in rows.items() if r["cause"] == "HISTORY-WALK"}
    wl = doc.get("walk_lines") or {}
    seen_keys = set()
    for pth, t in quoted_lines(buckets, pass2):
        if pth not in walk_paths:
            continue
        k = L.line_key(t)
        seen_keys.add(k)
        entry = wl.get(k)
        if entry is None:
            f["walk_unread"].append((pth, k, t.strip()[:66]))
        elif entry["verdict"] == "NOT-WALK" and L.is_walk_line(t):
            f["walk_notwalk"].append((pth, k, t.strip()[:66]))
    for k in sorted(wl):
        if k not in seen_keys:
            f["walk_stale"].append((k, wl[k]["excerpt"][:66]))
    return f, stale, buckets, pass2, observed, ran


def main():
    header, suites = R.load()
    if header is None:
        sys.stderr.write("mg-937c: no sweep record.  This arm grades OWNERS.json against "
                         "the record and refuses to grade it against nothing.\n")
        return 2
    doc = load_owners()
    if doc is None:
        sys.stderr.write("mg-937c: no OWNERS.json at %s.\n" % OWNERS)
        return 2

    out = []
    e = out.append
    f, stale, buckets, pass2, observed, ran = grade(header, suites, doc)
    rows = doc["rows"]

    e(rule("="))
    e("mg-937c — THE OWNERS OF THE VERDICT-STALE LIST, AND WHETHER IT HAS GROWN")
    e(rule("="))
    e("")
    e("  the baseline    : OWNERS.json, declared by %s over the corpus at `main` %s"
      % (doc["declared_by"], doc["corpus_at"]))
    e("  what it grades  : sweep_30bd.jsonl, through report.py's OWN `population()` and")
    e("                    `stale_set()` — imported, not paraphrased, so the baseline")
    e("                    cannot go complete against a classification the report no")
    e("                    longer performs.")
    e("  what it is not  : a re-measurement.  Nothing here runs a suite; the sweep is")
    e("                    hours and is deliberately outside every runner (run_all.sh).")
    e("")

    # ------------------------------------------------------------------ §1
    e(rule("="))
    # COMPUTED, NOT TYPED.  This heading said `150` and the file said 151 the first time
    # anybody added a row (mg-5491) — a hand-typed figure in the transcript-producing arm of
    # the directory that counts hand-typed figures going stale.  mg-2959's own subject, in
    # mg-937c's own §1 heading.
    e("§1  THE STANDING: WHAT %d ROWS OF READING CAME TO" % len(doc["rows"]))
    e(rule("="))
    e("")
    by_cause, by_disp, by_read = {}, {}, {}
    for r in rows.values():
        by_cause[r["cause"]] = by_cause.get(r["cause"], 0) + 1
        by_disp[r["disposition"]] = by_disp.get(r["disposition"], 0) + 1
        by_read[r["read"]] = by_read.get(r["read"], 0) + 1
    e("  %d row(s), over %d owning directories.  THE CAUSE IS THE HAND FIELD AND IT IS THE"
      % (len(rows), len({r["owner"] for r in rows.values()})))
    e("  WHOLE POINT OF THE FILE — a baseline nobody has read is a number that launders")
    e("  whatever was true on the day it was taken, which is why mg-30bd refused to set one.")
    e("")
    # THE BASELINE'S OWN SIZE, PRINTED BESIDE THE LIVE ONE (mg-5491).  It was prose until
    # this line existed: `150` was quoted in this directory's README nine times and in its
    # run_all.sh twice, and the moment the list actually moved not one transcript printed it
    # — mg-2959's exact class, in the file mg-2959's arm grades.  Reading the two together
    # is also the only way anybody can see that the list has BOTH shrunk and grown.
    e("  DECLARED OVER %d ROW(S) AT %s, AND IT CARRIES %d NOW.  §4 says which rows left and"
      % (doc.get("declared_rows", len(rows)), doc["corpus_at"], len(rows)))
    e("  why; §3 says which arrived.  A baseline whose size is prose cannot show either.")
    e("")
    for k in sorted(by_cause, key=lambda k: (-by_cause[k], k)):
        e("  %5d  %-24s %s" % (by_cause[k], k, doc["causes"][k][:52]))
    e("")
    for k in sorted(by_disp, key=lambda k: (-by_disp[k], k)):
        e("  %5d  %-24s %s" % (by_disp[k], k, doc["dispositions"][k][:52]))
    e("")
    e("  %5d  read in FULL — the record quotes every verdict line that moved"
      % by_read.get("full", 0))
    e("  %5d  read as a SAMPLE — the record caps its quotation at 6 lines and this entry"
      % by_read.get("sample", 0))
    e("         has more, so the cause above was assigned from part of the move.  SAID")
    e("         RATHER THAN SMOOTHED: `read` is checked against the record below, so this")
    e("         is the one figure here that cannot be overstated.")
    e("")
    e("  " + rule("-")[:86])
    e("  AND THE STRUCTURAL FACT UNDERNEATH ALL %d, MEASURED RATHER THAN FELT:"
      % len(stale))
    e("  " + rule("-")[:86])
    with open(os.path.join(ROOT, "build.sh"), encoding="utf-8") as fh:
        gated = gated_suites(fh.read())
    # MEASURED, NOT COUNTED BY HAND: how many of the rows this baseline calls HISTORY-WALK
    # report.py's own `<sha> <subject>` detector does NOT annotate.  A hand number here
    # would be a figure in a transcript backed by nothing, in the directory that counts
    # exactly that (mg-2959).
    walk_rows = sum(1 for r in rows.values() if r["cause"] == "HISTORY-WALK")
    unflagged_walks = 0
    narrow_unflagged = 0
    walk_residue = []
    for pth, row in sorted(rows.items()):
        if row["cause"] != "HISTORY-WALK":
            continue
        runner = pth in buckets and buckets[pth][0] in L.VERDICT_STALE
        hunk = (buckets[pth][2] if runner else pass2[pth][0].get("hunk")) or []
        if not any(L.walk_line_start(t) for _m, t in hunk):
            narrow_unflagged += 1
        if not R.walk_note(hunk):
            unflagged_walks += 1
            walk_residue.append((pth, hunk))
    in_gate = sorted(p for p in stale if os.path.dirname(p) in gated)
    e("")
    e("  ./build.sh runs %d suite(s).  The record ran %d.  Of the %d verdict-stale"
      % (len(gated), len(ran), len(stale)))
    e("  transcripts, %d sit in a directory the merge gate runs." % len(in_gate))
    for p in in_gate:
        e("       %s" % p)
    e("")
    e("  THAT NUMBER IS THE ANSWER TO `WHO OWNS THESE`, AND IT IS NOT A PERSON.  Every one")
    e("  of the %d is in a directory nothing on the merge path ever runs, so no branch has"
      % len(stale))
    e("  ever been told about any of them.  mg-f771's fixed-point control IS the whole-run")
    e("  before/after diff §6.6 asks for, and its committed transcript declares its subject")
    e("  as")
    e("      %s" % f771_scope())
    e("  — READ OFF THAT FILE rather than quoted from memory.  It is the SCOPE line and not")
    e("  the VERDICT because mg-c15e took the verdict out of that transcript: g0's own file")
    e("  was mg-f771's single self-exemption for exactly as long as it carried one.")
    e("  THAT IS NOT IN TENSION WITH THESE %d, AND THE RECONCILIATION IS THE COVERAGE READ"
      % len(stale))
    e("  ABOVE RATHER THAN A CAVEAT ABOUT EITHER NUMBER.  g0 can only compare a transcript")
    e("  THE GATE'S OWN RUN REWROTE, and the gate's run reaches %d of the %d candidate"
      % (len(gated), len(ran)))
    e("  suites.  A green whole-run diff over a ninth of the corpus and %d stale transcripts"
      % len(stale))
    e("  in the other eight ninths are THE SAME MEASUREMENT, not two that need reconciling.")
    e("")

    # ------------------------------------------------------------------ §2
    e(rule("="))
    e("§2  WHERE THE RECORD DISAGREES WITH ITSELF, COUNTED")
    e(rule("="))
    e("")
    multi = sum(1 for v in observed.values() if len(v) > 1)
    dis_all, dis_owner = [], []
    for pth in sorted(stale):
        note = R.disagreement(pth, observed, ran)
        if not note:
            continue
        dis_all.append(pth)
        if note.startswith("THE OWNING RUNNER") or note.startswith("NEITHER"):
            dis_owner.append((pth, note.split(" —")[0].split(" and ")[0]))
    e("  A transcript a sibling suite also runs is observed TWICE, and report.py keeps the")
    e("  STRONGEST bucket.  That is the right headline and it is silent about the")
    e("  disagreement, so the disagreement is counted here and annotated there.")
    e("")
    e("  %5d  rewritten transcript(s) observed by more than one suite" % multi)
    e("  %5d  verdict-stale entr(ies) with a disagreeing observation in the same record"
      % len(dis_all))
    e("  %5d  of those where the BENIGN observation is not a foreign suite's" % len(dis_owner))
    e("")
    for pth, why in dis_owner:
        e("      %s" % pth)
        e("          %s" % why)
    e("")
    runner_stale = sum(1 for p, v in buckets.items() if v[0] in L.VERDICT_STALE)
    e("  THE COUNTERFACTUAL, PRINTED SO IT IS A MEASUREMENT AND NOT AN ARGUMENT.  Dropping")
    e("  those %d would move §3's runner-reachable headline %d -> %d, and the total in"
      % (len(dis_owner), runner_stale, runner_stale - len(dis_owner)))
    # THE TRAILING PERIOD MATTERS AND THAT IS NOT A JOKE: mg-7522's number rule reads
    # `147.` as one token and the figure does not close the loop, so the README sentence
    # quoting it stays UNBACKED and the prose arm fires.  Measured on this branch — the
    # first version of this line ended here and 147 was the one figure still red.
    e("  report.py's own §7 table %d -> %d entries.  They are"
      % (len(stale), len(stale) - len(dis_owner)))
    e("  NOT dropped: which observation is authoritative is a decision about the corpus and")
    e("  belongs to the instance's owner.  That a decision is OWED is a fact about the")
    e("  record, and it now has a number.")
    e("")

    # ------------------------------------------------------------------ §3
    e(rule("="))
    e("§3  HAS THE LIST GROWN?")
    e(rule("="))
    e("")
    if not f["grown"] and not f["strengthened"]:
        e("  NO.  Every verdict-stale transcript in the record has a row in OWNERS.json, and")
        e("  no row's class has strengthened from `number` to `token`.")
    for pth, cls in f["grown"]:
        e("  *** THE LIST HAS GROWN: %s" % pth)
        e("      VERDICT-STALE/%s in the record, and no row in OWNERS.json." % cls)
        e("      Read its entry in out_verdict_staleness.txt, then add a row with a cause.")
    for pth, was, now in f["strengthened"]:
        e("  *** A ROW HAS STRENGTHENED: %s" % pth)
        e("      OWNERS.json says `%s`, the record says `%s`.  A number moving under an" % (was, now))
        e("      unmoved token is the weak claim; a verdict WORD moving is the strong one,")
        e("      so this is growth inside a row that already existed.")
    e("")
    e("  WHAT THIS CAN AND CANNOT SEE, and the second half is the important one.  The")
    e("  record is FROZEN: it changes when somebody runs `sweep.py --only <dir> --pass2`")
    e("  and appends, which is exactly what README §8 item 3 asks the next worker to do to")
    e("  the %d timed-out suites.  Re-measuring one of those will turn UNGRADED rows into"
      % len([s for s in suites if s.get("timeout")]))
    e("  clean or into stale, and the stale ones are NEW ENTRIES — that is the growth this")
    e("  arm exists to catch, and until this baseline existed nothing could have.")
    e("  IT CANNOT SEE A TRANSCRIPT THE RECORD DOES NOT COVER.  A branch adding a suite")
    e("  with a stale transcript is invisible here until somebody sweeps it, and no cheap")
    e("  check can be otherwise: the measurement is hours.  §5 item 1.")
    e("")

    # ------------------------------------------------------------------ §3
    e(rule("="))
    e("§4  WHAT HAS BEEN REPAIRED SINCE THE BASELINE — REPORTED, NEVER GRADED")
    e(rule("="))
    e("")
    if not f["retired"] and not f["weakened"]:
        e("  Nothing.  No row's transcript has left the verdict-stale list.")
    else:
        e("  A ROW LEAVES FOR THREE REASONS AND ONLY TWO OF THEM ARE GOOD NEWS (mg-5491).")
        e("  REPRODUCES and DECLARED are decided and the row may go.  UNMEASURED IS NEITHER:")
        e("  the record no longer contains a GRADE for that transcript — every observation of")
        e("  it was killed or refused, or the suites that used to rewrite it stopped — so")
        e("  deleting the row would shrink the baseline by a transcript NOBODY MEASURED.")
        e("  Unmeasured is not clean, which is §6.3's rule one level in.")
        e("")
    unmeasured = [r for r in f["retired"] if r[2] == "UNMEASURED"]
    for pth, cls, why in f["retired"]:
        e("  RETIRED/%-10s %s  (was %s)" % (why, pth, cls))
        if why == "REPRODUCES":
            e("           The record regenerated it and graded it BENIGN.  A repair.  DELETE")
            e("           this row from OWNERS.json; the baseline tightens and this stays green.")
        elif why == "DECLARED":
            e("           Its own text now declares it is not a fixed point, and §3b of")
            e("           out_verdict_staleness.txt carries it with the bucket it would have")
            e("           had.  DELETE this row; the entry has moved, not vanished.")
        else:
            e("           *** DO NOT DELETE THIS ROW.  No grade for it survives in the record:")
            e("           it is UNMEASURED, not repaired.  Re-measure the suite that owns it")
            e("           (`sweep.py --only <dir> --pass2`), then read the answer.")
    if unmeasured:
        e("")
        e("  %d of the %d retirements above are UNMEASURED and the row STAYS.  Reported and"
          % (len(unmeasured), len(f["retired"])))
        e("  NOT graded: nothing here is this directory's defect, and a red would be asking a")
        e("  branch to re-run somebody else's suite to get green.")
    for pth, was, now in f["weakened"]:
        e("  WEAKENED %s  %s -> %s" % (pth, was, now))
        e("           Amend the row's class.  Not growth and not graded.")
    e("")

    # ------------------------------------------------------------------ §4
    e(rule("="))
    e("§5  THE HAND FIELDS THAT THE RECORD CAN CONTRADICT")
    e(rule("="))
    e("")
    e("  Three of OWNERS.json's fields are claims about the record, so the record decides")
    e("  them.  `cause` and `disposition` are judgements and NOTHING HERE CHECKS THEM —")
    e("  said plainly, because an arm that implied otherwise would be the laundering the")
    e("  file exists to avoid.")
    e("")
    bad = f["bad_read"] + f["bad_disagree"] + f["bad_vocab"]
    if not bad:
        e("  %5d  `read` agrees with whether the record quotes the whole move" % len(rows))
        e("  %5d  `cause: RECORD-DISAGREES` agrees with the record's own disagreement, in"
          % len(rows))
        e("         BOTH directions — no row claims it falsely and no row omits it")
        e("  %5d  cause and disposition are from the declared vocabularies" % len(rows))
    for pth, got, want, dropped in f["bad_read"]:
        e("  *** `read` IS WRONG: %s" % pth)
        e("      says %r, the record drops %d verdict line(s) from its quotation, so %r."
          % (got, dropped, want))
    for pth, cause, should in f["bad_disagree"]:
        e("  *** `RECORD-DISAGREES` IS %s: %s"
          % ("MISSING" if should else "CLAIMED FALSELY", pth))
        e("      cause is %r; the record %s carry a disagreement whose benign side is not"
          % (cause, "does" if should else "does not"))
        e("      the owning runner's.")
    for pth, cause, disp in f["bad_vocab"]:
        e("  *** OFF-VOCABULARY: %s  cause=%r disposition=%r" % (pth, cause, disp))
    e("")

    # ------------------------------------------------------------------ §5
    e(rule("="))
    e("§6  WHAT THIS ARM CANNOT SEE — the enumeration's own blind spots, stated")
    e(rule("="))
    e("")
    e("  1  IT GRADES THE RECORD, NOT THE TREE.  `the list has not grown` here means `no")
    e("     new entry in sweep_30bd.jsonl`.  The corpus has moved since %s and this arm"
      % doc["corpus_at"])
    e("     cannot say by how much, because saying so means re-running the sweep.  A")
    e("     coverage figure read off `git ls-files` was considered and REFUSED: it would")
    e("     put a live-tree number in a committed transcript, which is the defect 649b186")
    e("     removed from report.py two commits before this one, in this directory.")
    e("")
    e("  2  THE %d UNGRADED ROWS AND THE %d TIMED-OUT SUITES ARE OUTSIDE THIS BASELINE"
      % (sum(1 for v in buckets.values() if v[0] == R.UNUSABLE),
         len([s for s in suites if s.get("timeout")])))
    e("     ENTIRELY, and OWNERS.json says nothing about them.  They are not clean and not")
    e("     stale; they are unmeasured.  Re-measuring them is how this list grows.")
    e("")
    unparsed = sum(1 for su in suites for row in (su.get("pass2") or [])
                   if row.get("status") == "unparsed")
    e("  3  %d PRODUCERS THE RUNNER-BLIND PASS CANNOT PARSE ARE NOT IN THE POPULATION, so"
      % unparsed)
    e("     they cannot be in the baseline.  Nothing in this estate regenerates or compares")
    e("     them and no baseline can make that untrue.")
    e("")
    e("  4  THE HISTORY-WALK DETECTOR IS STILL NARROWER THAN THE FAMILY IT NAMES, BUT BY")
    e("     ONE SHAPE RATHER THAN THREE, AND THE RESIDUE IS NOW A CLASS WITH A REASON")
    e("     (mg-aff1).  %d of the %d rows this baseline calls HISTORY-WALK carry no NOTE in"
      % (unflagged_walks, walk_rows))
    e("     §4 of out_verdict_staleness.txt; under the rule mg-937c measured, %d did."
      % narrow_unflagged)
    e("     THE BEFORE IS PRINTED BESIDE THE AFTER — see §6a, which re-measures both rules")
    e("     and the two refuted widenings over every quoted line in the record.")
    e("     WHAT IS LEFT IS ONE SHAPE: a BARE COMMIT SUBJECT, no sha and no label.  It is")
    e("     not repaired because it CANNOT be from the line alone, which §6a measures.")
    e("")
    e("  5  AND THE ONE THAT OUTRANKS THEM.  A successor working only these %d is working"
      % len(stale))
    e("     the list mg-30bd's instrument could see.  §6.6 of out_verdict_staleness.txt is")
    e("     unchanged and still owed: mg-6cb9 was found by a whole-run before/after diff,")
    e("     by accident, and not by any enumeration including this one.  What §1 above adds")
    e("     is WHERE to point that diff — the %d suites ./build.sh does not run."
      % (len(ran) - len(gated)))
    e("")

    # ---- §6a ---------------------------------------------------------------------------
    # THE FOUR RULES ON THE WHOLE RECORD (mg-aff1).  §6.4 above is a claim about a detector,
    # and every version of it that has ever been written is run here over every quoted line
    # the record holds — the one that shipped before, the one that ships now, and the two
    # that look right until they are run.  A widening argued for in prose is a widening
    # nobody measured, which is this directory's own subject applied to its own repair.
    e(rule("="))
    e("§6a  THE HISTORY-WALK DETECTOR, ALL FOUR RULES, OVER EVERY QUOTED LINE — mg-aff1")
    e(rule("="))
    e("")
    mark = len(out)
    lines = quoted_lines(buckets, pass2)
    hw_paths = {p for p, r in rows.items() if r["cause"] == "HISTORY-WALK"}
    rules = [("line-start  (mg-937c, replaced)", L.walk_line_start),
             ("SHIPPED     (mg-aff1)", L.is_walk_line),
             ("anywhere    (REFUTED)", L.walk_anywhere),
             ("bare subject(REFUTED)", L.walk_bare_subject)]
    e("  %d quoted line(s) in the record, over %d path(s).  A line in a row this baseline"
      % (len(lines), len({p for p, _t in lines})))
    e("  calls HISTORY-WALK is counted IN-FAMILY and any other line OUT.  That is a PROXY")
    e("  and it is named as one: the cause was assigned by reading, so it is the best")
    e("  ground truth here and it is not a proof.  An OUT hit is the expensive kind —")
    e("  a NOTE saying `this moves when main moves` on somebody else's finding.")
    e("")
    e("  %-32s %8s %8s %8s" % ("rule", "hits", "in-fam", "OUT"))
    e("  " + rule("-")[:60])
    for label, fn in rules:
        hit = [(p, t) for p, t in lines if fn(t)]
        infam = sum(1 for p, _t in hit if p in hw_paths)
        e("  %-32s %8d %8d %8d" % (label, len(hit), infam, len(hit) - infam))
    e("")
    e("  SO THE OBVIOUS WIDENING IS REFUTED ON THE RECORD AND NOT ON TASTE.  Dropping the")
    e("  %d-character label window annotates every FINDING sentence that quotes a sha, and"
      % L.WALK_LABEL_WINDOW)
    e("  the OUT column is how much.")
    e("")
    added = [(p, t) for p, t in lines if L.is_walk_line(t) and not L.walk_line_start(t)]
    e("  WHAT THE WIDENING BOUGHT AND WHAT IT COST, WHICH IS THE ROW THIS SECTION IS FOR:")
    e("  %d line(s) gained, %d of them IN-FAMILY, and the OUT column DID NOT MOVE."
      % (len(added), sum(1 for p, _t in added if p in hw_paths)))
    e("  THE TWO OUT HITS ARE PRINTED, BECAUSE A NUMBER IS NOT A DEFENCE — and both were")
    e("  already hit by the rule mg-937c measured, so neither is this repair's doing:")
    e("")
    for pth, t in [(p, t) for p, t in lines if L.is_walk_line(t) and p not in hw_paths]:
        e("    %s" % pth)
        e("        cause on file: %s" % rows.get(pth, {}).get("cause", "not in the baseline"))
        e("        %s" % t[:74])
    e("")
    e("  THEY ARE WALK LINES BY SHAPE AND THE PROXY IS WHAT DISAGREES, NOT THE DETECTOR: a")
    e("  transcript may carry one walk line and still be filed under the cause that")
    e("  dominates it.  Said here rather than smoothed into the OUT column, because the")
    e("  same two would be the whole warrant for calling this rule clean.")
    e("")
    e("  THE WINDOW IS A PLATEAU, RE-DERIVED ON THE RECORD RATHER THAN ON 9 STRINGS:")
    plateau = {}
    for k in range(1, 41):
        alt = __import__("re").compile(
            r"^(?:HEAD:\s*)?[A-Za-z ]{0,%d}<sha>[:,]?\s+\S" % k)
        n = sum(1 for _p, t in lines if alt.match(t) or L.HEAD_SUBJECT.match(t))
        plateau.setdefault(n, []).append(k)
    for n in sorted(plateau):
        ks = plateau[n]
        e("      width %2d-%2d -> %d hit(s)" % (ks[0], ks[-1], n))
    e("  The shipped width is %d.  It is inside the widest plateau and not at its edge,"
      % L.WALK_LABEL_WINDOW)
    e("  which is what stops it being a number fitted to this corpus.")
    e("")
    e("  AND WHAT IS LEFT, LISTED RATHER THAN COUNTED — the %d HISTORY-WALK row(s) with no"
      % len(walk_residue))
    e("  NOTE, with the lines that made somebody call them a walk:")
    e("")
    for pth, hunk in walk_residue:
        e("    %s" % pth)
        for _m, t in hunk[:3]:
            e("        %s" % t[:76])
    e("")
    e("  EVERY ONE IS A BARE COMMIT SUBJECT, and the row above says why that stays open:")
    e("  the `bare subject` rule takes them and takes %d line(s) that are not walks at all."
      % sum(1 for p, t in lines if L.walk_bare_subject(t) and p not in hw_paths))
    e("  A CLOSED VOCABULARY OF COMMIT TYPES WOULD SEPARATE THEM AND ROT: this estate's log")
    e("  carries `refresh`, `measure`, `declare`, `amend`, `land`, `discharge`, `owners`,")
    e("  `scope` and `census+repair`, and nothing closes that set.  THE ONE RULE THAT WOULD")
    e("  WORK IS REFUSED ON THIS DIRECTORY'S OWN GROUNDS: matching the line against `git")
    e("  log` answers differently on different days, so the transcript carrying the answer")
    e("  stops being a function of repo state — mg-e720's family, which is the very cause")
    e("  this NOTE names.  A history-walk detector that walked history would be a member of")
    e("  the population it counts.")
    e("")
    # THE REMEDY PUT TO ITS OWN DEFECT, AND IT DOES NOT COME BACK CLEAN.  DECLARATION has a
    # WINDOW, which is what stops a transcript quoting the marker from exempting itself.
    # This detector has no such defence and cannot have one: it reads a hunk, so its input is
    # already a quotation, and a quoted walk line is letter-for-letter a walk line.  This
    # section is now the densest concentration of quoted walk lines in the corpus, so the
    # count is taken over the lines it has just printed rather than asserted to be zero.
    self_hits = sum(1 for ln in out[mark:] if L.is_walk_line(ln))
    e("  AND THE RULE APPLIED TO THIS SECTION'S OWN TEXT, WHICH IS NOT ZERO: %d of the %d"
      % (self_hits, len(out) - mark))
    e("  line(s) printed above are walk lines under the rule they are printed to justify.")
    e("  mg-5491's DECLARATION has a WINDOW for exactly this and THIS DETECTOR CANNOT: its")
    e("  input is a hunk, so what it reads is ALREADY a quotation, and a quoted walk line is")
    e("  letter-for-letter a walk line.  What keeps the number small is an ACCIDENT and it")
    e("  is named as one — the 8-space evidence indent pushes some of them past the label")
    e("  window — so nobody should read it as a defence.  IT COSTS NOTHING TODAY: report.py")
    e("  annotates §4 and §5, this transcript is in neither, and README §8 item 4 already")
    e("  records that this directory is outside the population it counts.  It is here so")
    e("  that the sweep which finally includes this directory finds the reason written down")
    e("  rather than discovering it.")
    e("")

    # ---- §6b ---------------------------------------------------------------------------
    # THE OUT COLUMN'S OWN POWER (mg-cda7).  §6a is a measurement of the DETECTOR; this is a
    # measurement of the CONTROL §6a defends it with.  mg-aff1's carry-forward asked for it
    # in as many words: a control that has never fired is a claim.
    e(rule("="))
    e("§6b  IS THE OUT COLUMN SENSITIVE ENOUGH? — THE CONTROL, MEASURED — mg-cda7")
    e(rule("="))
    e("")
    wl = doc.get("walk_lines") or {}
    infam = [(p, t) for p, t in lines if p in hw_paths]
    nwalk = sum(1 for v in wl.values() if v["verdict"] == "WALK")
    e("  §6a's defence of the shipped rule is `the OUT column did not move`, and it is only")
    e("  a defence if that is HARD TO PRODUCE.  Nobody had measured whether it is.  The")
    e("  in/out split is a PROXY OVER PATHS — a line is in-family because the ROW it sits in")
    e("  was read and filed HISTORY-WALK, not because anybody looked at the LINE — so a")
    e("  widening confined to those rows moves the OUT column by ZERO however wrong it is.")
    e("")
    e("  SO THERE IS A THIRD COLUMN, AND IT IS A READING: OWNERS.json's `walk_lines` carries")
    e("  a hand verdict for each of the %d quoted line(s) inside a HISTORY-WALK row — %d read"
      % (len(infam), nwalk))
    e("  as WALK, %d as NOT-WALK.  mg-937c's remedy for the 150, one level in, at the LINE"
      % (len(wl) - nwalk))
    e("  instead of the ROW.  NOTHING CHECKS THAT A READING IS RIGHT, which is word for word")
    e("  what OWNERS.json already declares about `cause`; what stops it being tuned to")
    e("  flatter the shipped rule is that every rule below is graded against the SAME list.")
    e("")
    walk_bad = f["walk_unread"] + f["walk_stale"] + f["walk_notwalk"]
    if not walk_bad:
        e("  %5d  every in-family quoted line has an entry — a HISTORY-WALK row arriving"
          % len(infam))
        e("         with unread lines is a FINDING, not a silent gap")
        e("  %5d  every entry still names a line the record holds — BOTH directions, for the"
          % len(wl))
        e("         reason `cause: RECORD-DISAGREES` is checked in both")
        e("  %5d  the SHIPPED rule takes no line read NOT-WALK" % len(wl))
    for pth, k, t in f["walk_unread"]:
        e("  *** UNREAD in-family line: %s  key=%s" % (pth, k))
        e("      %s" % t)
        e("      Read it and add an entry to `walk_lines`, or this section is complete")
        e("      against a corpus that moved.")
    for k, ex in f["walk_stale"]:
        e("  *** STALE `walk_lines` entry, the record no longer holds it: key=%s" % k)
        e("      %s" % ex)
    for pth, k, t in f["walk_notwalk"]:
        e("  *** THE SHIPPED RULE TAKES A LINE READ NOT-WALK: %s  key=%s" % (pth, k))
        e("      %s" % t)
    e("")
    base = [(p, t) for p, t in lines if L.is_walk_line(t)]
    b_in = sum(1 for p, _t in base if p in hw_paths)
    b_out = len(base) - b_in
    e("  EVERY RULE THAT HAS BEEN WRITTEN OR PLANTED, ON THE SAME %d LINE(S).  `gain` is"
      % len(lines))
    e("  against the SHIPPED rule and is never negative: a candidate is the shipped rule OR")
    e("  itself, so these are supersets and not swaps.  `dOUT` is the control under test.")
    e("")
    e("  %-4s %-34s %5s %5s %5s %5s %6s" %
      ("id", "rule", "hits", "gain", "g-in", "dOUT", "!WALK"))
    e("  " + rule("-")[:68])
    e("  %-4s %-34s %5d %5s %5s %5s %6s" %
      ("--", "SHIPPED (mg-aff1) — the baseline", len(base), "--", "--", "--", "--"))
    caught = missed = gainful = 0
    witness = []
    for cid, label, _bad, pat in L.CANDIDATE_WIDENINGS:
        fn = L.candidate(pat)
        hit = [(p, t) for p, t in lines if fn(t)]
        gain = [(p, t) for p, t in hit if not L.is_walk_line(t)]
        g_in = sum(1 for p, _t in gain if p in hw_paths)
        d_out = (len(hit) - sum(1 for p, _t in hit if p in hw_paths)) - b_out
        nw = sum(1 for p, t in gain
                 if p in hw_paths and (wl.get(L.line_key(t)) or {}).get("verdict") == "NOT-WALK")
        if gain:
            gainful += 1
            if d_out:
                caught += 1
            else:
                missed += 1
                witness.append((cid, label, len(gain), g_in, nw))
        e("  %-4s %-34s %5d %5d %5d %5d %6d"
          % (cid, label, len(hit), len(gain), g_in, d_out, nw))
    e("")
    e("  %d OF THE %d GAIN NOTHING AT ALL, which is worth its own line rather than being"
      % (len(L.CANDIDATE_WIDENINGS) - gainful, len(L.CANDIDATE_WIDENINGS)))
    e("  read past: several of the widenings a successor would plausibly reach for are")
    e("  NO-OPS on this corpus — the shipped rule already takes everything they would.  So")
    e("  `hits did not move` is the common answer and a rule that DOES gain is the unusual")
    e("  one, which is the context the numbers below are read in.")
    e("")
    e("  THE COLUMN HAS POWER AND IT IS A NUMBER NOW: of the %d rule(s) that gain any line"
      % gainful)
    e("  at all, %d MOVE THE OUT COLUMN.  mg-aff1's refutation of `anywhere` was not luck —"
      % caught)
    e("  the OUT population is %d line(s) over %d path(s), so a rule that reaches past the"
      % (len(lines) - len(infam), len({p for p, _t in lines if p not in hw_paths})))
    e("  walk shape almost cannot avoid it.  THAT IS THE HALF THAT DEFENDS mg-aff1.")
    e("")
    if witness:
        e("  AND %d DO NOT, WHICH IS THE HALF THAT BOUNDS IT.  Each of these gains lines,"
          % missed)
        e("  gains them ALL IN-FAMILY, and leaves the OUT column exactly where it was —")
        e("  mg-aff1's own signature, letter for letter — on a rule that is not a walk")
        e("  detector at all.  THE THIRD COLUMN IS WHAT DISAGREES WITH THEM:")
        e("")
        for cid, label, g, gi, nw in witness:
            e("    %-4s %-36s gained %d, %d in-family, OUT +0, %d read NOT-WALK"
              % (cid, label, g, gi, nw))
        e("")
    e("  SO `OUT UNMOVED` IS NECESSARY AND NOT SUFFICIENT.  That is the correction this")
    e("  section makes to §6a, and it is made ON THE RECORD rather than on taste: the")
    e("  witnesses above are rules that pass the control and are wrong.")
    e("")
    # THE CEILING.  How much room is there in the blind spot?  Computed, not bounded by
    # taste: a line is REACHABLE if its exact text occurs nowhere outside a HISTORY-WALK row,
    # because then the rule `match this literal` gains it with the OUT column provably still.
    # An exact-literal rule is the crudest member of the class and therefore the safest
    # witness — anything a regex can do to a line, a literal can do to that line.
    import collections as _c
    out_texts = _c.Counter(t.strip() for p, t in lines if p not in hw_paths)
    miss = [(p, t) for p, t in infam if not L.is_walk_line(t)]
    reach = [(p, t) for p, t in miss if out_texts[t.strip()] == 0]
    reach_nw = [(p, t) for p, t in reach
                if (wl.get(L.line_key(t)) or {}).get("verdict") == "NOT-WALK"]
    e("  THE CEILING ON THE BLIND SPOT, COMPUTED RATHER THAN ESTIMATED:")
    e("    %3d  in-family line(s) the shipped rule does not take" % len(miss))
    e("    %3d  of those are REACHABLE with the OUT column provably still — their exact"
      % len(reach))
    e("         text occurs nowhere outside a HISTORY-WALK row, so `match this literal`")
    e("         gains them and moves nothing.  A literal is the crudest rule there is,")
    e("         which makes it the safest witness: it needs no argument to be possible.")
    e("    %3d  of those %d are hand-read NOT-WALK — the room a bad widening has, and the"
      % (len(reach_nw), len(reach)))
    e("         reason the third column is a file and not a sentence.")
    e("")
    added_in = sum(1 for p, _t in added if p in hw_paths)
    added_nw = sum(1 for p, t in added
                   if (wl.get(L.line_key(t)) or {}).get("verdict") == "NOT-WALK")
    e("  AND THE SHIPPED RULE'S OWN ROW, GRADED BY THE COLUMN mg-aff1 DID NOT HAVE:")
    e("  %d gained, %d in-family, OUT unmoved, AND %d OF %d READ NOT-WALK.  The two numbers"
      % (len(added), added_in, added_nw, len(added)))
    e("  mg-aff1 published still stand; this is the third, and it is the one the witnesses")
    e("  above would have failed.  A widening that takes a NOT-WALK line is a FINDING here")
    e("  and exits 1 — this is OWNERS.json, this directory's own file, and the repair is in")
    e("  the same commit: narrow the rule, or read the line again and say why.")
    e("")
    e("  WHAT THIS SECTION STILL CANNOT DO, SAID HERE RATHER THAN DISCOVERED LATER.  The")
    e("  third column only sees lines inside HISTORY-WALK rows, because that is the only")
    e("  population anybody has read line by line; a widening's damage OUTSIDE them is what")
    e("  the OUT column is for, and neither column subsumes the other.  A rule bad in BOTH")
    e("  places is caught twice and a rule bad in neither is not bad here — which is the")
    e("  most this can claim without somebody reading the other %d line(s)."
      % (len(lines) - len(infam)))
    e("")
    e("  AND THIS SECTION'S OWN CLAIM IS THE CLAIM IT WAS WRITTEN TO REFUSE, so the third")
    e("  column's power is PLANTED rather than argued: §7's P12c flips one reading to")
    e("  NOT-WALK under the live rule and the finding fires, P12a and P12b delete and")
    e("  invent an entry, and P13 checks the arm is SILENT on the %d line(s) read NOT-WALK"
      % (len(wl) - nwalk))
    e("  that the rule correctly does not take — the polarity a remedy gets wrong, since a")
    e("  column that fired on those would report every transcript line in the corpus.")
    e("")

    findings = (len(f["grown"]) + len(f["strengthened"]) + len(bad)
                + len(walk_bad))
    e(rule("="))
    if findings:
        e("OWNERS VERDICT: %d FINDING(S) IN THIS DIRECTORY'S OWN FILES — see §3, §5 and §6b."
          % findings)
    else:
        e("OWNERS VERDICT: GREEN — %d verdict-stale transcript(s), %d with a row, 0 without."
          % (len(stale), len(rows) - len(f["retired"])))
    e(rule("="))
    e("")

    # ------------------------------------------------------------------ §6
    e(rule("="))
    e("§7  THE PLANTED WORLDS — this arm shown FAILING, in the ways it claims to fail")
    e(rule("="))
    e("")
    e("  Every world below mutates a COPY of the record or of OWNERS.json and re-runs the")
    e("  SAME `grade()` the verdict above came from.  A control that scores its own")
    e("  expectations against a stub is mg-1344's finding; these run the real function.")
    e("")
    worlds, bad_worlds = plant(header, suites, doc)
    for name, want, got, ok in worlds:
        e("  %-4s %-56s %s" % (name, want, "ok" if ok else "*** FAILED ***  got %r" % (got,)))
    e("")
    if bad_worlds:
        e("  %d WORLD(S) DID NOT COME OUT AS PLANTED, so the verdict above is not evidence"
          % bad_worlds)
        e("  of anything and this arm exits 1 on itself.")
    else:
        e("  %d worlds, all as planted." % len(worlds))
    e("")
    print("\n".join(out))
    return 1 if (findings or bad_worlds) else 0


def plant(header, suites, doc):
    """The controls.  Each returns (name, what must happen, what did, ok)."""
    import copy
    W_ = []

    def run(d, s=suites):
        return grade(header, s, d)[0]

    # P1  A NEW STALE ENTRY WITH NO ROW IS GROWTH.  The row is deleted from a COPY of
    #     OWNERS.json rather than a path invented, so the world is one the record can
    #     actually produce.
    victim = sorted(doc["rows"])[0]
    d = copy.deepcopy(doc)
    d["rows"].pop(victim)
    f = run(d)
    W_.append(("P1", "a stale transcript with no row -> GROWN",
               len(f["grown"]), [p for p, _c in f["grown"]] == [victim]))

    # P2  A ROW WHOSE TRANSCRIPT IS NO LONGER STALE IS RETIRED AND **GREEN**.  This is the
    #     polarity that matters: red here would be mg-e35b's red-on-improvement, and it is
    #     planted rather than promised.
    # THE EXPECTATION IS A DELTA AND NOT AN ABSOLUTE, AND THAT IS mg-5491's REPAIR TO THIS
    # CONTROL.  It read `len(f["retired"]) == 1`, which held only while the live record had
    # ZERO retirements — so the first branch to actually repair one of the 150 would have
    # made this control fail, i.e. a control that goes red when its own subject improves.
    # mg-e35b's shape, inside the world planted to demonstrate the opposite polarity.
    base = run(doc)
    f = run(_p2_world(doc, copy, victim))
    W_.append(("P2", "a repaired transcript -> RETIRED, and not GROWN",
               (len(f["retired"]) - len(base["retired"]), len(f["grown"])),
               len(f["retired"]) - len(base["retired"]) == 1
               and len(f["grown"]) == len(base["grown"])))

    # P3  number -> token IS GROWTH; token -> number IS NOT.
    tok = next(p for p, r in doc["rows"].items() if r["class"] == "token")
    num = next(p for p, r in doc["rows"].items() if r["class"] == "number")
    d = copy.deepcopy(doc)
    d["rows"][tok]["class"] = "number"
    f = run(d)
    W_.append(("P3a", "a token entry recorded as number -> STRENGTHENED",
               len(f["strengthened"]), [p for p, _a, _b in f["strengthened"]] == [tok]))
    d = copy.deepcopy(doc)
    d["rows"][num]["class"] = "token"
    f = run(d)
    W_.append(("P3b", "a number entry recorded as token -> WEAKENED, not graded",
               (len(f["weakened"]), len(f["strengthened"])),
               len(f["weakened"]) == 1 and not f["strengthened"]))

    # P4  `read: full` ON AN ENTRY THE RECORD ONLY SAMPLES IS CAUGHT.  This is the field
    #     that makes "somebody read it" falsifiable rather than a claim.
    owned, rew, buckets, observed, pass2 = R.population(suites, header.get("declared"))
    sampled = next(p for p, r in doc["rows"].items() if r["read"] == "sample")
    d = copy.deepcopy(doc)
    d["rows"][sampled]["read"] = "full"
    f = run(d)
    W_.append(("P4", "`read: full` where the record drops lines -> caught",
               len(f["bad_read"]), [x[0] for x in f["bad_read"]] == [sampled]))

    # P5  `RECORD-DISAGREES` IS CHECKED IN BOTH DIRECTIONS.  Claiming it falsely and
    #     dropping it where the record has one both fire — a one-sided check would let the
    #     harder half be deleted in silence, which is mg-9876's membership smell.
    #
    #     P5a PLANTS THE DISAGREEMENT INTO A COPY OF THE RECORD RATHER THAN LOOKING FOR ONE,
    #     AND mg-5491 REWROTE IT FOR A REASON WORTH KEEPING.  It used to pick a live row
    #     whose cause was already RECORD-DISAGREES — so the day somebody re-measured those
    #     three suites and the disagreement was RESOLVED, this control had no subject and
    #     failed.  It failed exactly that way on this branch.  A control that stops working
    #     when its subject is repaired tests the corpus, not the instrument; this one now
    #     builds the shape itself, out of a stale row and a synthetic OWNING observation
    #     saying IDENTICAL, which is precisely the world mg-937c found three of.
    dis, dis_suites = _plant_disagreement(suites, doc, copy)
    d = copy.deepcopy(doc)
    d["rows"][dis]["cause"] = "RECORD-DISAGREES"
    f0 = run(d, dis_suites)
    d["rows"][dis]["cause"] = "CORPUS-COUNT"
    f = run(d, dis_suites)
    W_.append(("P5a", "a RECORD-DISAGREES row relabelled -> caught",
               (len(f0["bad_disagree"]), [x[0] for x in f["bad_disagree"]]),
               not f0["bad_disagree"] and [x[0] for x in f["bad_disagree"]] == [dis]))
    d = copy.deepcopy(doc)
    plain = next(p for p, r in doc["rows"].items() if r["cause"] == "SUBJECT-MOVED")
    d["rows"][plain]["cause"] = "RECORD-DISAGREES"
    f = run(d)
    W_.append(("P5b", "RECORD-DISAGREES claimed where the record has none -> caught",
               len(f["bad_disagree"]), [x[0] for x in f["bad_disagree"]] == [plain]))

    # P6  AN OFF-VOCABULARY CAUSE IS CAUGHT.  A free-text cause field would let the
    #     vocabulary drift into 150 singletons, which is a list and not a classification.
    d = copy.deepcopy(doc)
    d["rows"][plain]["cause"] = "BECAUSE"
    f = run(d)
    W_.append(("P6", "a cause outside the declared vocabulary -> caught",
               len(f["bad_vocab"]), [x[0] for x in f["bad_vocab"]] == [plain]))

    # P7  THE UNMUTATED WORLD IS SILENT.  A control suite whose every world fires proves
    #     only that the arm always fires.
    f = run(doc)
    W_.append(("P7", "the unmutated baseline -> no finding of any kind",
               sum(len(v) for k, v in f.items() if k not in ("retired", "weakened")),
               not any(f[k] for k in ("grown", "strengthened", "bad_read",
                                      "bad_disagree", "bad_vocab"))))

    # P8  AND THE REMEDY PUT TO THE DEFECT IT REMEDIES.  This arm's own transcript is a
    #     committed out_*.txt in a directory the next sweep WILL cover, so it will join the
    #     population it grades.  That is stated in README §8 item 4 and is not a hole; the
    #     hole would be this arm being unable to grade its OWN row.  Planted: a row for
    #     this arm's transcript is an ordinary row and is graded like any other.
    d = copy.deepcopy(doc)
    d["rows"]["code/verdict_staleness_30bd/out_owners_937c.txt"] = dict(
        d["rows"][plain], cause="CONTROL-FLIPPED", disposition="TICKET", read="full")
    f = run(d)
    W_.append(("P8", "a row naming THIS arm's own transcript -> graded, not exempt",
               len(f["retired"]),
               "code/verdict_staleness_30bd/out_owners_937c.txt"
               in [r[0] for r in f["retired"]]))

    # P9  mg-5491's DECLARATION, PUT TO THIS ARM AND NOT ONLY TO THE REPORT.  A transcript
    #     that declares itself not a fixed point leaves the stale list, so its row RETIRES —
    #     and the arm must stay GREEN, because a baseline going red when somebody repairs one
    #     of the 150 is mg-e35b's red-on-improvement wearing the remedy's clothes.  The world
    #     is built by mutating the HEADER, which is where the census actually travels, rather
    #     than by calling the exemption directly.
    victim2 = sorted(p for p in doc["rows"]
                     if p != "code/verdict_staleness_30bd/out_owners_937c.txt")[0]
    h = dict(header, declared={victim2: "planted by P9 — it reads a stream, not a tree"})
    f = grade(h, suites, doc)[0]
    W_.append(("P9", "a DECLARED transcript -> RETIRED/DECLARED, and no NEW finding",
               [(r[0], r[2]) for r in f["retired"] if r[0] == victim2],
               (victim2, "DECLARED") in [(r[0], r[2]) for r in f["retired"]]
               and all(len(f[k]) == len(base[k]) for k in ("grown", "strengthened",
                                                           "bad_read", "bad_disagree",
                                                           "bad_vocab"))))

    # P10 AND THE HALF THAT STOPS IT BEING AN ESCAPE HATCH.  A marker with NOTHING AFTER IT
    #     is not a declaration: it is honoured by nobody, the row stays stale, and the report
    #     lists it as MALFORMED.  An exemption that costs a reason is a claim; one that costs
    #     a keyword is a keyword.
    h = dict(header, declared={victim2: ""})
    f = grade(h, suites, doc)[0]
    W_.append(("P10", "a marker with NO REASON -> not honoured, the row stays",
               len(f["retired"]), victim2 not in [r[0] for r in f["retired"]]))

    # P11 THE THREE REASONS A ROW LEAVES ARE TOLD APART, AND THE ONE THAT MATTERS IS THE
    #     THIRD.  P2's planted row names a path THE RECORD HAS NO GRADE FOR, which is the
    #     exact shape that cost mg-937c a silent baseline shrink: leaving the stale list
    #     because nobody measured it is NOT leaving because somebody repaired it, and only
    #     the second may be deleted.  Planted on the same world P2 uses, so the two read the
    #     same mutation and disagree about nothing except the question asked.
    got = [r[2] for r in run(_p2_world(doc, copy, victim))["retired"]
           if r[0] == "code/nowhere_0000/out_repaired.txt"]
    W_.append(("P11", "a row the record has NO GRADE for -> RETIRED/UNMEASURED, not REPRODUCES",
               got, got == ["UNMEASURED"]))

    # P12 mg-cda7 — THE THIRD COLUMN'S OWN THREE FAILURES, PLANTED.  `walk_lines` is a hand
    #     file and it rots the way OWNERS.json's rows would without P1: an entry deleted, an
    #     entry that outlives its line, and the one the whole section exists for — the
    #     SHIPPED rule taking a line somebody read as NOT-WALK.  The third is planted by
    #     FLIPPING A VERDICT rather than by inventing a rule, because grade() sees rules only
    #     through `is_walk_line`; flipping the reading under the live rule builds exactly the
    #     world a bad widening would produce and needs no second detector to do it.
    wl_keys = sorted(doc.get("walk_lines") or {})
    victim3 = next(k for k in wl_keys
                   if doc["walk_lines"][k]["verdict"] == "WALK"
                   and L.is_walk_line(doc["walk_lines"][k]["excerpt"]))
    d = copy.deepcopy(doc)
    d["walk_lines"].pop(victim3)
    f = run(d)
    W_.append(("P12a", "an in-family line with no entry -> UNREAD, a finding",
               [k for _p, k, _t in f["walk_unread"]],
               [k for _p, k, _t in f["walk_unread"]] == [victim3]))
    d = copy.deepcopy(doc)
    d["walk_lines"]["deadbeef0000"] = {"excerpt": "a line the record does not hold",
                                       "verdict": "WALK", "why": "planted by P12b"}
    f = run(d)
    W_.append(("P12b", "an entry whose line has left the record -> STALE, a finding",
               [k for k, _e in f["walk_stale"]],
               [k for k, _e in f["walk_stale"]] == ["deadbeef0000"]))
    d = copy.deepcopy(doc)
    d["walk_lines"][victim3]["verdict"] = "NOT-WALK"
    f = run(d)
    W_.append(("P12c", "the SHIPPED rule taking a NOT-WALK line -> a finding",
               [k for _p, k, _t in f["walk_notwalk"]],
               [k for _p, k, _t in f["walk_notwalk"]] == [victim3]))

    # P13 mg-cda7 — AND THE OTHER POLARITY, WHICH IS THE ONE A REMEDY GETS WRONG.  A line
    #     read NOT-WALK that the shipped rule DOES NOT take is the normal, correct state of
    #     16 of these entries, and a third column that fired on it would report every
    #     transcript line in the corpus as a defect.  Planted on the live file so the check
    #     is that the arm is SILENT where it should be, not merely loud where it should be.
    quiet = next(k for k in wl_keys if doc["walk_lines"][k]["verdict"] == "NOT-WALK")
    f = run(doc)
    W_.append(("P13", "a NOT-WALK line the rule does not take -> NOT a finding",
               (quiet in [k for _p, k, _t in f["walk_notwalk"]], len(f["walk_notwalk"])),
               not f["walk_notwalk"]))

    return W_, sum(1 for _n, _w, _g, ok in W_ if not ok)


def _plant_disagreement(suites, doc, copy):
    """(path, mutated suites) — a stale row whose OWNING runner reproduces it byte-identically.

    Built rather than found.  Take a stale transcript its own directory observed; flip that
    observation to IDENTICAL in a COPY of the record, and add a synthetic FOREIGN suite
    carrying the stale grade the owner just gave up — same hunk, same `dropped`, so the
    `read` field stays consistent and P5a cannot pass by accidentally firing `bad_read`.
    The result is the exact shape `report.py`'s `disagreement()` calls THE OWNING RUNNER
    REPRODUCES THIS BYTE-IDENTICALLY, and it exists whether or not the corpus has one.
    """
    s2 = copy.deepcopy(suites)
    for suite in s2:
        if "error" in suite or suite.get("timeout") or suite.get("rc") == 2:
            continue
        for row in suite.get("rows", []):
            pth = row["path"]
            if (row.get("bucket") not in L.VERDICT_STALE or not row.get("rewritten")
                    or os.path.dirname(pth) != suite["dir"] or pth not in doc["rows"]):
                continue
            foreign = {"kind": "suite", "dir": "code/planted_foreign_5491", "rc": 0,
                       "timeout": False, "secs": 0.0, "owned": [], "rewritten": [pth],
                       "rows": [dict(row)]}
            row["bucket"] = L.IDENTICAL
            row["detail"] = ""
            row.pop("hunk", None)
            row.pop("dropped", None)
            s2.append(foreign)
            return pth, s2
    raise AssertionError("no stale transcript observed by its own runner to plant on")


def _p2_world(doc, copy, victim):
    """P2's mutation, built once and used by P2 and P11 so they cannot drift apart."""
    d = copy.deepcopy(doc)
    d["rows"]["code/nowhere_0000/out_repaired.txt"] = dict(
        d["rows"][victim], cause="CORPUS-COUNT", disposition="PIN-AS-DATED", read="full")
    return d


if __name__ == "__main__":
    sys.exit(main())
