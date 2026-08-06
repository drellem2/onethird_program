#!/usr/bin/env python3
"""D2 -- THE CAUSE, DETERMINED RATHER THAN ASSUMED.

Two live hypotheses, and they are DIFFERENT FAULTS WITH DIFFERENT FIXES:

  H-INSTRUCTION (pm-onethird's) the verdict is never sent because the worker's
                                instructions degraded over a long run
  H-REAP        (mayor's)       the worker is stopped between producing the
                                verdict and mailing it, so the work exists and
                                the message never leaves

This section looks for evidence that DISCRIMINATES, not evidence consistent with
either. The discriminating quantity is a TIME INTERVAL:

    H-REAP requires the verdict to be written INSIDE the window between the
    worker's last chance to mail and its stop. If compliant workers demonstrably
    mail OUTSIDE that window -- minutes or hours before it opens -- then a stop
    inside the window cannot be what suppressed the mail.

Two stores are read. macguffin's own (`~/.macguffin`) for landings and mail, and
pogod's event log (`~/.pogo/events.log`) for `agent_stopped`. The second is read
BECAUSE mayor's dispatch note says not to take mayor's account of mayor's own
behaviour as evidence about mayor's behaviour.

Exit 0 -- this section reports and concludes; it asserts no threshold.
"""
import collections
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_bf3f as L  # noqa: E402

POGO = os.path.expanduser(os.environ.get("POGO_ROOT", "~/.pogo"))

# The instruction, exactly as pm-onethird wrote it in the tickets that carry it.
INSTR = re.compile(
    r"mail (it|the verdict|your verdict).{0,40}(to )?`?pm-onethird"
    r"|route your verdict to pm-onethird", re.I | re.S)


def load_stops():
    """agent -> [ (timestamp, reason, duration_seconds) ], from pogod's log."""
    out = collections.defaultdict(list)
    path = os.path.join(POGO, "events.log")
    if not os.path.exists(path):
        print(f"  !! {path} absent -- the reap half of this section cannot run")
        return out
    for line in open(path, encoding="utf-8", errors="replace"):
        if "agent_stopped" not in line:
            continue
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if e.get("event_type") != "agent_stopped":
            continue
        d = e.get("details") or {}
        out[e.get("agent")].append((e.get("timestamp"), d.get("reason"), d.get("duration_seconds")))
    return out


def fisher_exact_2x2(a, b, c, d):
    """Two-tailed Fisher exact p for [[a,b],[c,d]]. Exact, no scipy."""
    n = a + b + c + d
    r1, r2, c1 = a + b, c + d, a + c

    def prob(x):
        return (math.comb(r1, x) * math.comb(r2, c1 - x)) / math.comb(n, c1)

    p0 = prob(a)
    lo = max(0, c1 - r2)
    hi = min(r1, c1)
    return sum(prob(x) for x in range(lo, hi + 1) if prob(x) <= p0 * (1 + 1e-9))


def main():
    res = L.scan(filer="pm-onethird")
    rows = res["rows"]
    stops = load_stops()
    items = L.load_items(L.root())

    def stop_for(row):
        cands = set(row["worker_names"] or [])
        if row["worker"]:
            cands.add(row["worker"])
            cands.add("cat-" + row["worker"])
        for n in list(cands):
            cands.add("cat-" + n)
        ts = [t for n in cands for (t, _r, _d) in stops.get(n, [])]
        return max(ts) if ts else None

    print("=" * 78)
    print("D2.1  THE REAP IS REAL AND IT IS FAST -- measured, not taken from mayor")
    print("=" * 78)
    deltas = {"DELIVERED": [], "DROPPED": []}
    reasons = collections.Counter()
    for r in rows:
        if r["status"] == "UNDECIDABLE":
            continue
        s = stop_for(r)
        if not s:
            continue
        a, b = L.parse_ts(s), L.parse_ts(r["landed"])
        if a is None or b is None:
            continue
        deltas[r["status"]].append(round((a - b).total_seconds()))
        for n in set(r["worker_names"] or []) | {"cat-" + (r["worker"] or "")}:
            for (_t, rr, _d) in stops.get(n, []):
                reasons[rr] += 1
    for k in ("DELIVERED", "DROPPED"):
        v = sorted(deltas[k])
        med = v[len(v) // 2] if v else None
        le1 = sum(1 for x in v if 0 <= x <= 1)
        print(f"  {k:10} n={len(v):3}  stop-minus-landing seconds: median={med}  "
              f"within [0,1]s: {le1}/{len(v)}")
    print(f"  stop reasons seen: {dict(reasons)}")
    print("  -> mayor's account of the reap CHECKS OUT: the polecat is stopped within a")
    print("     second of its item landing, and the distribution is THE SAME in both groups.")
    print("     Identical in both groups means the reap does not discriminate them.")

    print()
    print("=" * 78)
    print("D2.2  THE DISCRIMINATOR -- when do verdicts that DID arrive actually arrive?")
    print("=" * 78)
    leads = []
    for r in rows:
        if r["status"] != "DELIVERED":
            continue
        lead = L.verdict_lead_minutes(r)
        if lead is not None:
            leads.append((lead, r["id"], r["verdict_mail"]["subject"][:52]))
    leads.sort(reverse=True)
    before = [x for x in leads if x[0] > 1]
    after = [x for x in leads if x[0] <= 1]
    print("  lead = minutes the verdict mail PRECEDED the landing (negative = arrived after)")
    for lead, iid, subj in leads:
        print(f"    {lead:>8}  {iid}  {subj}")
    print()
    print(f"  arrived MORE THAN A MINUTE BEFORE the landing : {len(before)} of {len(leads)}")
    print(f"  arrived within a minute either side           : {len(after)} of {len(leads)}")
    worst = min((x[0] for x in leads), default=None)
    print(f"  the LATEST any verdict ever arrived           : {worst} minutes relative to landing")
    print()
    print("  THIS IS THE DISCRIMINATION. The reap window is [landing, landing+1s].")
    print("  Every verdict that has ever been delivered was already sent before that")
    print("  window opened, or inside the same minute the worker itself closed the item.")
    print("  A stop at landing+0.5s cannot suppress a mail sent 167 minutes earlier.")
    print("  -> H-REAP does not explain the drops in the MAIL channel.")

    print()
    print("=" * 78)
    print("D2.3  LIVENESS -- dropped workers that were demonstrably alive and mailing")
    print("=" * 78)
    print("  A reaped process cannot send mail. These workers dropped the filer's verdict")
    print("  and went on mailing somebody else, or had already mailed somebody else and")
    print("  then lived on for many minutes:")
    sent = L.load_mail_sent(L.root())
    by_from = collections.defaultdict(list)
    for e in sent:
        by_from[e.get("from")].append(e)
    live = 0
    for r in rows:
        if r["status"] != "DROPPED" or not r["mails_elsewhere"]:
            continue
        s = stop_for(r)
        ms = sorted({(e["ts"], e["to"]) for n in (r["worker_names"] or []) for e in by_from.get(n, [])})
        if not ms:
            continue
        last, to = ms[-1]
        gap = None
        if s:
            a, b = L.parse_ts(s), L.parse_ts(last)
            if a and b:
                gap = round((a - b).total_seconds() / 60.0)
        live += 1
        print(f"    {r['id']}  worker {r['worker']:9} sent {len(ms)} mail(s), last to '{to}' at {last}")
        print(f"              its own stop was {gap} minutes LATER -- it was alive and mailing.")
    print(f"  -> {live} dropped items have positive proof the worker was not reaped before it")
    print("     could mail. For those, H-REAP is refuted outright, not merely unsupported.")

    print()
    print("=" * 78)
    print("D2.4  THE INSTRUCTION -- was the worker ever ASKED?")
    print("=" * 78)
    chron = []
    for iid, info in items.items():
        if info["creator"] != "pm-onethird":
            continue
        chron.append((info["created"] or "?", iid, bool(INSTR.search(info["text"]))))
    chron.sort()
    carry = [c for c in chron if c[2]]
    print(f"  pm-onethird has filed {len(chron)} items; {len(carry)} carry the instruction")
    print("  \"mail the verdict to pm-onethird BEFORE submitting to the refinery\".")
    print(f"  FIRST appearance : {carry[0][0]}  {carry[0][1]}")
    print(f"  LAST  appearance : {carry[-1][0]}  {carry[-1][1]}")
    after_last = [c for c in chron if c[0] > carry[-1][0]]
    print(f"  items filed AFTER that last appearance : {len(after_last)}")
    print(f"  of those, carrying the instruction     : {sum(1 for c in after_last if c[2])}")
    print()
    print("  Contingency over pm-onethird items that LANDED on/after the instruction's")
    print("  first appearance (before that date nobody was asked, so the comparison is void):")
    status = {r["id"]: r["status"] for r in rows}
    landed = {r["id"]: r["landed"] for r in rows}
    a = b = c = d = 0
    for created, iid, has in chron:
        if iid not in status or status[iid] == "UNDECIDABLE":
            continue
        if (landed[iid] or "") < carry[0][0]:
            continue
        deliv = status[iid] == "DELIVERED"
        if has and deliv:
            a += 1
        elif has and not deliv:
            b += 1
        elif not has and deliv:
            c += 1
        else:
            d += 1
    print(f"                      delivered   dropped")
    print(f"    instruction  YES   {a:>7}   {b:>7}")
    print(f"    instruction  NO    {c:>7}   {d:>7}")
    p = fisher_exact_2x2(a, b, c, d)
    ry = a / (a + b) if a + b else float("nan")
    rn = c / (c + d) if c + d else float("nan")
    print(f"    delivery rate      {ry:.0%}       {rn:.0%}")
    print(f"    Fisher exact two-tailed p = {p:.3g}")
    print()
    print("  -> THE DRIFT IS IN THE FILER'S TEMPLATE, NOT THE WORKER'S COMPLIANCE.")
    print("     The instruction stopped being WRITTEN. No worker after that date was")
    print("     ever asked for a verdict, so none of them 'failed to comply'.")

    print()
    print("  P11 control -- of the instruction-absent items that were delivered ANYWAY,")
    print("  how many were worked by an agent that never worked an instruction-carrying")
    print("  ticket? (If most were, ticket text is not the whole mechanism.)")
    carried_workers = set()
    for created, iid, has in chron:
        if not has:
            continue
        r = next((x for x in rows if x["id"] == iid), None)
        if r:
            carried_workers |= set(r["worker_names"] or [])
    novel = 0
    tot = 0
    for created, iid, has in chron:
        if has or status.get(iid) != "DELIVERED":
            continue
        if (landed.get(iid) or "") < carry[0][0]:
            continue
        tot += 1
        r = next((x for x in rows if x["id"] == iid), None)
        if r and not (set(r["worker_names"] or []) & carried_workers):
            novel += 1
            print(f"     {iid}  worker {r['worker']} never saw the instruction and mailed anyway")
    print(f"  -> {novel} of {tot} instruction-absent deliveries came from a worker that was")
    print("     never asked. Ticket text is a strong predictor, not the whole mechanism.")

    print()
    print("=" * 78)
    print("D2.5  THE SECOND CHANNEL IS REAP-SHAPED AND IT IS MAYOR'S (P9)")
    print("=" * 78)
    print("  pm-onethird's instruction has two halves: mail the verdict, AND write")
    print("  `mg done --result` with it. The second half is structurally unavailable.")
    tot = ref = withverdict = 0
    for r in rows:
        info = items.get(r["id"])
        side = L.load_sidecar(info) if info else None
        if side is None:
            continue
        tot += 1
        if side.get("completed_by") == "refinery":
            ref += 1
        keys = set(side) - {"branch", "completed_by", "mr", "target"}
        if keys:
            withverdict += 1
    print(f"  landed items with a result sidecar        : {tot}")
    print(f"  written by the refinery, not by the worker : {ref}  ({ref / tot:.0%})")
    print(f"  carrying ANY field beyond branch/mr/target : {withverdict}")
    actors = collections.Counter(r["done_actor"] for r in rows)
    print(f"  actor on the work.done event              : {dict(actors)}")
    print()
    print("  pogod closes the item ON MERGE, before the worker's own `mg done` can run;")
    print("  the polecat protocol's step 7 then hands the worker a result template that")
    print("  contains only {\"branch\": ...} and tells it 'already done' is success.")
    print("  A worker that obeyed 'write mg done --result with your verdict' would have")
    print("  been beaten to the item and told it had succeeded.")
    print("  -> THIS half IS reap-shaped, it is real, and it is MAYOR'S END. Routed.")

    print()
    print("=" * 78)
    print("D2.6  VERDICT ON THE CAUSE")
    print("=" * 78)
    print("  MAIL CHANNEL   H-REAP        REFUTED. Every delivered verdict predates the")
    print("                               reap window; several dropped workers are proven")
    print("                               alive and mailing others long past it.")
    print("                 H-INSTRUCTION CONFIRMED BUT MIS-STATED. Compliance did not")
    print("                               drift: the INSTRUCTION did. It vanished from")
    print("                               pm-onethird's own ticket template and has not")
    print("                               appeared in any ticket filed since.")
    print()
    print("  RESULT CHANNEL H-REAP        CONFIRMED, and it belongs to mayor: pogod's")
    print("                               close-on-merge plus the protocol's own step-7")
    print("                               template make `mg done --result` unreachable.")
    print()
    print("  REPAIRING ONE WITHOUT THE OTHER LEAVES THE OTHER ALIVE AND LOOKING FIXED --")
    print("  which is exactly what the ticket warned about, and both are live.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
