#!/usr/bin/env python3
"""a3 — mg-39bf reconstructs mg-9461's run timeline from artefacts only.

E3, filed in advance: I must not build the timeline on my own ticket's
"~40 minutes in", nor on the mayor's note's "~5 minutes into its run", nor on
the parent's 12's "~40 minutes after dispatch".  Those three disagree, so at
most one is right and none is evidence.  Every time printed below comes from a
file mtime, a mail `Date:` header, or a git AUTHOR date (committer dates are
rewritten by the refinery's rebase and are not evidence of when work happened).

The claim under audit (parent 12):

    "pm-onethird's mid-flight correction arrived ~40 minutes after dispatch,
     after I had read the sources and committed predictions.  Nothing had to
     be discarded."

Two separable assertions: the INTERVAL, and the ORDER.  They are checked apart,
because a worker's incentive attaches to the second and not the first.
"""

import datetime as dt
import os
import re
import subprocess
import sys

MAILDIR = os.path.expanduser("~/.macguffin/mail/q9461")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FAILURES = []


def fail(m):
    FAILURES.append(m)
    print("  *** FAIL: %s" % m)


def utc(ts):
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc)


def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True).stdout.strip()


def main():
    events = []

    print("A — MAILBOX CREATION (pogod registers it at spawn)")
    for sub in ("", "new", "cur"):
        p = os.path.join(MAILDIR, sub)
        if os.path.isdir(p):
            print("  %-40s %s" % (p.replace(os.path.expanduser("~"), "~"),
                                  utc(os.stat(p).st_ctime).isoformat()))
    box_ct = utc(os.stat(MAILDIR).st_ctime)
    events.append((box_ct, "q9461 mailbox created (proxy for SPAWN)"))

    print("\nB — THE CORRECTION MAIL")
    msgs = []
    for sub in ("new", "cur"):
        d = os.path.join(MAILDIR, sub)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            msgs.append(os.path.join(d, f))
    if not msgs:
        fail("no mail found in %s — cannot date the correction" % MAILDIR)
        return 1
    for m in msgs:
        raw = open(m).read()
        hdr = dict(re.findall(r"^(From|Subject|Date):\s*(.*)$", raw, re.M))
        sent = dt.datetime.fromisoformat(hdr["Date"].replace("Z", "+00:00"))
        st = os.stat(m)
        print("  file      %s" % os.path.basename(m))
        print("  From      %s" % hdr.get("From"))
        print("  Subject   %s" % hdr.get("Subject", "")[:78])
        print("  Date:     %s   <- when pm-onethird SENT it" % sent.isoformat())
        print("  in dir    %s   <- 'cur' means the worker read it"
              % os.path.basename(os.path.dirname(m)))
        print("  mtime     %s   <- DELIVERY write.  NOT the read: `mv`"
              % utc(st.st_mtime).isoformat())
        print("            preserves mtime across the new->cur move, so this"
              " timestamp")
        print("            survives the move unchanged and dates the SEND, not"
              " the read.")
        print("            (My first version of this script used it as the read"
              " time and")
        print("            was wrong by 10.5 minutes.  What records the move is"
              " the")
        print("            DIRECTORY ctime, below.)")
        events.append((sent, "correction SENT by pm-onethird"))
        if os.path.basename(os.path.dirname(m)) == "cur":
            cur_ct = utc(os.stat(os.path.join(MAILDIR, "cur")).st_ctime)
            print("  cur/ ctime %s   <- the new->cur move, i.e. READ"
                  % cur_ct.isoformat())
            events.append((cur_ct, "correction READ (new->cur move)"))
        # The mail's own first line dates the dispatch independently.
        mrel = re.search(r"dispatched ~(\d+) minutes ago", raw)
        if mrel:
            print("  the mail's OWN first line: 'dispatched ~%s minutes ago'"
                  % mrel.group(1))
            events.append((sent - dt.timedelta(minutes=int(mrel.group(1))),
                           "DISPATCH, per the correction mail's own wording"))

    print("\nC — GIT AUTHOR DATES (committer dates are rebase artefacts)")
    for ref, label in (("3cd39f1", "PREDICTIONS.md committed (pre-rebase)"),
                       ("ba19c06", "instrument committed (pre-rebase)"),
                       ("424e693", "deliverable committed (pre-rebase)"),
                       ("6e5d88b", "mg-d3c7 landed on main")):
        iso = git("log", "-1", "--format=%aI", ref)
        cmt = git("log", "-1", "--format=%cI", ref)
        if not iso:
            fail("cannot resolve %s" % ref)
            continue
        a = dt.datetime.fromisoformat(iso).astimezone(dt.timezone.utc)
        c = dt.datetime.fromisoformat(cmt).astimezone(dt.timezone.utc)
        print("  %-8s author %s   committer %s   %s"
              % (ref, a.isoformat(), c.isoformat(), label))
        events.append((a, label))

    print("\nD — RECONSTRUCTED TIMELINE (UTC, sorted)")
    events.sort()
    t0 = None
    for t, what in events:
        if "DISPATCH" in what:
            t0 = t
    for t, what in events:
        off = ""
        if t0 is not None:
            d = (t - t0).total_seconds() / 60.0
            off = "T%+07.1f min" % d
        print("  %s  %-12s  %s" % (t.isoformat(), off, what))

    print("\nE — THE THREE STATED INTERVALS, SCORED")
    sent = [t for t, w in events if "SENT" in w][0]
    read = [t for t, w in events if "READ" in w]
    pred = [t for t, w in events if "PREDICTIONS" in w][0]
    disp = t0
    d_sent = (sent - disp).total_seconds() / 60.0
    print("  dispatch -> correction SENT : %.1f min" % d_sent)
    if read:
        d_read = (read[0] - disp).total_seconds() / 60.0
        print("  dispatch -> correction READ : %.1f min" % d_read)
    print()
    for src, claim in (("parent 12 + its commit subject", 40),
                       ("mg-39bf ticket body ('~40 minutes in')", 40),
                       ("mayor dispatch note ('~5 minutes into its run')", 5),
                       ("the correction mail's own first line", 5)):
        near_sent = abs(claim - d_sent) <= 5
        near_read = read and abs(claim - (read[0] - disp).total_seconds() / 60.0) <= 5
        verdict = ("matches SENT" if near_sent else
                   "matches READ" if near_read else "MATCHES NEITHER")
        print("  %-48s says %2d min -> %s" % (src[:48], claim, verdict))

    print("\nF — THE ORDER, WHICH IS THE PART THAT ACTUALLY MATTERS")
    print("  The parent's substantive claim is that the correction arrived")
    print("  AFTER it had read the sources and committed predictions.")
    print("  predictions authored : %s" % pred.isoformat())
    print("  correction SENT      : %s" % sent.isoformat())
    if read:
        print("  correction READ      : %s" % read[0].isoformat())
    print()
    if sent < pred:
        print("  SENT is BEFORE the predictions commit, by %.1f min."
              % ((pred - sent).total_seconds() / 60.0))
        print("  So my own ticket's 'the correction landed after it [3cd39f1]'")
        print("  is FALSE on the SENT reading.")
    else:
        print("  SENT is after the predictions commit.")
    if read and read[0] > pred:
        print("  READ is AFTER the predictions commit, by %.1f min."
              % ((read[0] - pred).total_seconds() / 60.0))
        print("  So the parent's own claim — that it had committed predictions")
        print("  before the correction reached it — is TRUE on the READ")
        print("  reading, which is the only reading a worker can act on.")
    elif read:
        fail("correction was READ before predictions were committed — the "
             "parent's ordering claim is FALSE")

    print("\n" + "=" * 72)
    if FAILURES:
        print("RESULT: %d FAILURE(S)" % len(FAILURES))
        for f in FAILURES:
            print("  - %s" % f)
        return 1
    print("RESULT: timeline reconstructed from artefacts only.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
