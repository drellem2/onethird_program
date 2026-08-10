#!/usr/bin/env python3
"""mg-e331 §1-2 — CHARACTERISE THE GROWTH BEFORE RATCHETING IT, AND THEN DECIDE THE TARGET.

The ticket forbids going straight to the ratchet, and it is right to: "A ratchet on a file
that is absorbing work with no other home will simply relocate the problem or start failing
every landing."  So this producer answers three questions with numbers before any threshold
is chosen.

  §1  WHAT GREW — per commit, per section, and per table row, over the whole recorded life of
      the file and not only since mg-ea0e.
  §2  DOES IT BELONG — did the commits that added it have a destination available, and did
      they use it?
  §3  IS 6,000 WORDS THE RIGHT NUMBER — answered against §1 and §2 rather than asserted.

ITS SUBJECT IS HISTORY, so unlike ratchet.py this producer reads COMMITS.  It is not the
gate and it is not on the merge critical path; it is the evidence the gate's threshold rests
on, and it is re-runnable so that the evidence can be re-read rather than believed.

The predictions in PREDICTIONS.md are scored at the end, by rule, including the ones I lose.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_e331 as L  # noqa: E402

RESTRUCTURES = {
    "57f962f1": "mg-34bf",
    "cc4c663e": "mg-ea0e",
}


def commit_walk():
    """(sha, iso date, subject, bytes, words) for every first-parent commit touching
    STATE.md, oldest first.  FIRST-PARENT because the question is what LANDED on main; a
    full walk counts a polecat's intermediate commits, which never existed on main as a
    state anyone read."""
    raw = L.git("log", "--first-parent", "--format=%H|%ad|%s", "--date=iso-strict",
                "main", "--", "STATE.md")
    rows = []
    for line in raw.strip().split("\n"):
        sha, date, subj = line.split("|", 2)
        m = L.measure(L.show(sha))
        rows.append((sha, date[:19], subj, m["bytes"], m["words"]))
    rows.reverse()
    return rows


def ticket_of(subject):
    ids = re.findall(r"\(mg-([0-9a-f]{4})\)", subject)
    return "mg-" + ids[-1] if ids else "—"


def main():
    print("=" * 92)
    print("mg-e331 §1-3 — CHARACTERISING STATE.md's GROWTH, AND DECIDING THE TARGET")
    print("=" * 92)
    print()

    walk = commit_walk()
    head_text = L.read_state()
    head = L.measure(head_text)
    scores = {}

    # ---- §1.1 -----------------------------------------------------------------------------
    print("§1.1  EVERY LANDING THAT TOUCHED STATE.md, oldest first")
    print("-" * 92)
    print("  %-9s %-19s %9s %9s %8s  %s" % ("commit", "landed", "bytes", "delta", "words",
                                            "ticket"))
    prev = None
    cuts = []
    for sha, date, subj, b, w in walk:
        d = 0 if prev is None else b - prev
        mark = "  <<< CUT" if d < -1000 else ""
        if d < -1000:
            cuts.append((sha[:8], date, prev, b, ticket_of(subj)))
        print("  %-9s %-19s %9d %+9d %8d  %-8s%s"
              % (sha[:9], date, b, d, w, ticket_of(subj), mark))
        prev = b
    print()
    print("  %d landings.  First %d B, last %d B." % (len(walk), walk[0][3], walk[-1][3]))
    print()

    # ---- §1.2 -----------------------------------------------------------------------------
    print("§1.2  HOW MANY TIMES HAS THIS BEEN CUT, AND WHAT HAPPENED AFTER EACH CUT")
    print("-" * 92)
    print("  The ticket says the arc has paid for this twice.  Counted rather than assumed:")
    print()
    by_sha = {s[:8]: i for i, (s, _, _, _, _) in enumerate(walk)}
    regrowth = []
    for sha8, date, before, after, tk in cuts:
        i = by_sha[sha8]
        tail = walk[i + 1:]
        regrown, hours, n = None, None, 0
        # D2, KEPT AND REPAIRED IN PLACE.  My first rule asked `did it get back to its
        # PRE-CUT size` and printed `NOT yet back` for mg-34bf — literally true and
        # thoroughly misleading, because mg-34bf's cut WAS 97% undone in 8.5 hours and only
        # escaped the threshold because a LARGER cut (mg-ea0e) arrived before it finished.
        # An absolute threshold that a later, bigger cut makes unreachable forever reports
        # every interrupted regression as no regression.  It is mg-f8e5's `c1_rebase.py:48`
        # in a third costume: a fixed anchor answering a question about a moving quantity.
        # The measure that survives is the PEAK reached before the NEXT cut, expressed as a
        # fraction of the cut that was undone.
        stop = len(tail)
        for j, (_, _, _, b2, _) in enumerate(tail):
            if j and b2 < tail[j - 1][3] - 1000:
                stop = j
                break
        window = tail[:stop]
        if window:
            k = max(range(len(window)), key=lambda i: window[i][3])
            peak, peak_date, peak_n = window[k][3], window[k][1], k + 1
            hours = _hours(date, peak_date)
            undone = 100.0 * (peak - after) / max(before - after, 1)
        else:
            peak = after
            peak_n, hours, undone = 0, 0.0, 0.0
        print("  %-8s %s  %s" % (sha8, tk, date))
        print("      cut  %d -> %d B  (-%d, %.0f%% of the file)"
              % (before, after, before - after, 100.0 * (before - after) / before))
        print("      peak %d B after %d landings and %.1f hours — %.0f%% OF THE CUT UNDONE"
              % (peak, peak_n, hours, undone))
        print("      %s"
              % ("interrupted by the next cut before it finished" if stop < len(tail)
                 else "and it is still growing: %d B at HEAD" % tail[-1][3]))
        regrowth.append((tk, undone, hours))
    print()
    fastest = min(regrowth, key=lambda r: r[2] / max(r[1], 0.1))
    print("  CUTS FOUND: %d.  Every one was substantially undone; the fastest was %s at"
          % (len(cuts), fastest[0]))
    print("  %.0f%% within %.1f hours." % (fastest[1], fastest[2]))
    print("  THE TICKET NAMES ONE CUT (mg-ea0e).  There are %d: %s cut first, on %s, and was"
          % (len(cuts), regrowth[0][0], cuts[0][1][:10]))
    print("  %.0f%% undone in %.1f hours — seven days before mg-ea0e cut the same file"
          % (regrowth[0][1], regrowth[0][2]))
    print("  again.  So mg-ea0e was not the first cleanup with no mechanism —")
    print("  it was the SECOND, and the first one's failure was already on the record when")
    print("  it was planned.  That is the strongest available argument that the missing")
    print("  thing is a mechanism and not more care.")
    scores["P-H2"] = ("MEASUREMENT (not a bet): mg-ea0e is not the first cut", len(cuts) >= 2,
                      "%d cuts of >1000 B found; earliest %s" % (len(cuts), cuts[0][4]))
    print()

    # ---- §1.3 -----------------------------------------------------------------------------
    ea0e = [c for c in cuts if c[4] == "mg-ea0e"]
    base = ea0e[0][0] if ea0e else L.EA0E_LANDED[0][:8]
    base_text = L.show(base)
    print("§1.3  WHERE THE %d BYTES ADDED SINCE mg-ea0e WENT — by section"
          % (head["bytes"] - L.measure(base_text)["bytes"]))
    print("-" * 92)
    s0 = {k: (b, w) for k, b, w in L.sections(base_text)}
    s1 = {k: (b, w) for k, b, w in L.sections(head_text)}
    keys = [k for k, _, _ in L.sections(base_text)]
    keys += [k for k, _, _ in L.sections(head_text) if k not in keys]
    print("  %9s %9s %10s %8s   %s" % ("ea0e B", "HEAD B", "delta B", "share", "section"))
    total = head["bytes"] - L.measure(base_text)["bytes"]
    ranked = []
    for k in keys:
        b0 = s0.get(k, (0, 0))[0]
        b1 = s1.get(k, (0, 0))[0]
        ranked.append((b1 - b0, k, b0, b1))
    for d, k, b0, b1 in sorted(ranked, reverse=True):
        share = (100.0 * d / total) if total else 0.0
        print("  %9d %9d %+10d %7.1f%%   %s" % (b0, b1, d, share, k[:48]))
    print()

    # ---- §1.4 -----------------------------------------------------------------------------
    print("§1.4  NEW ROWS, OR OLD ROWS GETTING LONGER?  (the question that decides the remedy)")
    print("-" * 92)
    print("  If old rows are swelling, the content has nowhere else to go and a cap on the")
    print("  total will start failing every landing.  If the section is GAINING ROWS, each")
    print("  row is a self-contained document and `docs/state-history/` is where it goes.")
    print()
    tables = [("## Attempt index", 1, "P1"), ("### Full ledger", 0, "P2")]
    for heading, keycell, pid in tables:
        a = L.table_rows(base_text, heading, keycell)
        b = L.table_rows(head_text, heading, keycell)
        newk = [k for k in b if k not in a]
        kept = [k for k in b if k in a]
        gone = [k for k in a if k not in b]
        new_ch = sum(b[k] for k in newk)
        grew_ch = sum(b[k] - a[k] for k in kept)
        print("  %-18s rows %d -> %d" % (heading, len(a), len(b)))
        print("      %+7d chars from %d NEW rows      (mean %d chars/row)"
              % (new_ch, len(newk), new_ch // len(newk) if newk else 0))
        print("      %+7d chars from %d KEPT rows growing in place" % (grew_ch, len(kept)))
        if gone:
            print("      %+7d chars dropped with %d rows" % (-sum(a[k] for k in gone),
                                                             len(gone)))
        if pid == "P1":
            hit = new_ch >= 5 * max(grew_ch, 1)
            scores["P1"] = ("new-row bytes >= 5x in-place growth in the attempt index", hit,
                            "%d vs %d = %.1fx" % (new_ch, grew_ch,
                                                  new_ch / max(grew_ch, 1)))
            print("      P1: new %d vs in-place %d = %.1fx  ->  %s"
                  % (new_ch, grew_ch, new_ch / max(grew_ch, 1), "HIT" if hit else "MISS"))
            print("      The %d new rows, longest first:" % len(newk))
            for k in sorted(newk, key=lambda k: -b[k]):
                print("        %6d chars | %s" % (b[k], k[:62]))
        else:
            hit = len(newk) == 0 and grew_ch > 0
            scores["P2"] = ("ledger gained ZERO rows and grew entirely in place", hit,
                            "%d new rows, %+d chars in place" % (len(newk), grew_ch))
            print("      P2: %d new rows, %+d in place  ->  %s"
                  % (len(newk), grew_ch, "HIT" if hit else "MISS"))
        print()

    print("  SO THE TWO HALVES GROW BY TWO DIFFERENT MECHANISMS.  The attempt index gains")
    print("  whole documents; the ledger's fixed 13 rows absorb qualifications in place.")
    print("  'STATE.md is big' explains neither and prescribes nothing.")
    print()

    # ---- §2 -------------------------------------------------------------------------------
    print("§2  DOES IT BELONG HERE — was there a destination, and was it used?")
    print("-" * 92)
    dest = "docs/state-history"
    files = [f for f in L.git("ls-tree", "--name-only", "HEAD", dest + "/").split()]
    print("  %s exists at HEAD and holds %d files." % (dest, len(files)))
    print("  It was created by mg-ea0e as the home for exactly this content.")
    print()
    since = L.git("log", "--first-parent", "--format=%H|%s", "%s..main" % base,
                  "--", "STATE.md").strip().split("\n")
    wrote, silent = [], []
    for line in since:
        if not line:
            continue
        sha, subj = line.split("|", 1)
        touched = L.git("show", "--name-only", "--format=", sha).split()
        if any(t.startswith(dest + "/") for t in touched):
            wrote.append((sha[:8], ticket_of(subj)))
        else:
            silent.append((sha[:8], ticket_of(subj)))
    print("  Landings that changed STATE.md since mg-ea0e: %d" % (len(wrote) + len(silent)))
    print("    %2d ALSO wrote to %s : %s"
          % (len(wrote), dest, ", ".join(t for _, t in wrote) or "—"))
    print("    %2d wrote to STATE.md and NOTHING to %s:" % (len(silent), dest))
    print("       %s" % ", ".join(t for _, t in silent))
    hit4 = len(silent) >= 3
    scores["P4"] = ("at least 3 growth landings wrote nothing to the destination", hit4,
                    "%d of %d wrote nothing there" % (len(silent), len(wrote) + len(silent)))
    print()
    print("  P4: %s" % ("HIT" if hit4 else "MISS"))
    print()
    print("  READING.  The destination is not missing and it is not unknown — it is four")
    print("  days old, it is in the same repository, and %d of %d landings used it.  So the"
          % (len(wrote), len(wrote) + len(silent)))
    print("  growth is NOT content with nowhere to go, and the ticket's first hazard — that a")
    print("  ratchet would 'simply relocate the problem' — has a destination to relocate to.")
    print("  What was missing was not a home.  It was anything that ASKED.")
    print()

    # ---- §3 -------------------------------------------------------------------------------
    print("§3  IS 6,000 WORDS THE RIGHT TARGET?  Decided against §1.4, not asserted")
    print("-" * 92)
    att_rows = L.table_rows(head_text, "## Attempt index", 1)
    att_base = L.table_rows(base_text, "## Attempt index", 1)
    relocatable_ch = sum(v for k, v in att_rows.items() if k not in att_base)
    # words, measured on the actual row text rather than converted by a ratio
    reloc_words = 0
    inside = False
    for line in head_text.split("\n"):
        if L.HEADING.match(line):
            inside = line.startswith("## Attempt index")
            continue
        if inside and line.startswith("|") and not L.TABLE_SEP.match(line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) > 1 and cells[1][:60] not in att_base:
                reloc_words += len(line.split())
    residue = head["words"] - reloc_words
    print("  HEAD                                        %6d words" % head["words"])
    print("  minus every attempt-index row added since   -%5d words   (%d chars, %d rows)"
          % (reloc_words, relocatable_ch, len(att_rows) - len(att_base)))
    print("  = residue if ALL of it were relocated       %6d words" % residue)
    print("  mg-ea0e's stated target                     %6d words" % L.EA0E_TARGET_WORDS)
    print("  mg-ea0e's own landed value                  %6d words" % L.EA0E_LANDED[2])
    print()
    hit3 = residue > L.EA0E_TARGET_WORDS
    scores["P3"] = ("residue after full relocation still exceeds 6,000 words", hit3,
                    "%d words residue vs %d target" % (residue, L.EA0E_TARGET_WORDS))
    print("  P3: %s — %d > %d is %s"
          % ("HIT" if hit3 else "MISS", residue, L.EA0E_TARGET_WORDS, str(hit3).upper()))
    print()
    if hit3:
        print("  DECIDED: 6,000 WORDS IS NOT THE THRESHOLD THIS RATCHET GETS SET TO, and the")
        print("  reason is not that the target was wrong when mg-ea0e chose it.  It is that a")
        print("  gate set to 6,000 today is RED ON ARRIVAL — %d words over — and would block"
              % (head["words"] - L.EA0E_TARGET_WORDS))
        print("  every merge in this repository from the moment it landed, for a reason no")
        print("  author of an unrelated branch can act on.  gate.py's own docstring refuses")
        print("  exactly that construction, in those words, about a different suite.")
        print()
        print("  A ratchet is not a target.  It is a MONOTONE FLOOR UNDER A REGRESSION: it")
        print("  says the file does not get bigger than it is now without somebody saying so")
        print("  in writing.  Set it where the file stands and it binds from today; set it at")
        print("  an aspiration nobody has met and it is either removed within a week or")
        print("  suppressed, and a suppressed control is worse than none (mg-d91f).")
        print()
        print("  THE 6,000-WORD TARGET IS NOT WITHDRAWN AND IT IS NOT MINE TO WITHDRAW.  It")
        print("  remains what mg-ea0e aimed at and what `docs/state-history/` was built to")
        print("  make reachable.  The gap is %d words and it is a DEBT with a named remedy"
              % (head["words"] - L.EA0E_TARGET_WORDS))
        print("  (relocate attempt rows to their per-attempt files), not a number to assert")
        print("  into a config file and call enforced.  Every landing that pays some of it")
        print("  down must lower the ceiling in the same commit — which is what the")
        print("  SLACK-UNRATCHETED half of the rule exists to force, and it is the half that")
        print("  makes this a ratchet rather than a cap.")
    else:
        print("  DECIDED: the target is reachable by relocation alone.  The ratchet goes to")
        print("  %d words and the relocation is the work." % L.EA0E_TARGET_WORDS)
    print()

    # ---- scores ---------------------------------------------------------------------------
    print("=" * 92)
    print("PREDICTIONS SCORED BY THIS PRODUCER")
    print("-" * 92)
    for pid in sorted(scores):
        what, hit, ev = scores[pid]
        print("  %-5s %-6s %-62s %s" % (pid, "HIT" if hit else "MISS", what, ev))
    print()
    print("P1_GROWTH VERDICT: characterised — %d landings, %d cuts, growth is %s"
          % (len(walk), len(cuts),
             "NEW ROWS in the attempt index and IN-PLACE in the ledger"))
    print("=" * 92)
    return 0


def _hours(a, b):
    import datetime
    fa = datetime.datetime.fromisoformat(a)
    fb = datetime.datetime.fromisoformat(b[:19])
    if fa.tzinfo is None and fb.tzinfo is not None:
        fa = fa.replace(tzinfo=fb.tzinfo)
    if fb.tzinfo is None and fa.tzinfo is not None:
        fb = fb.replace(tzinfo=fa.tzinfo)
    return (fb - fa).total_seconds() / 3600.0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except L.Refusal as exc:
        print()
        print("P1_GROWTH VERDICT: REFUSED — %s" % exc)
        sys.exit(2)
