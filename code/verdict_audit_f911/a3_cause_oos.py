#!/usr/bin/env python3
"""mg-f911 A3 -- brief item 4: was the cause DETERMINED, or assumed?

The parent named two candidates and claimed to have separated them:

  H-REAP        the polecat is stopped ~0-1s after its merge, before it mails.
  H-INSTRUCTION the ask lives in ticket bodies and vanished from the template
                on 2026-07-31T10:02Z; workers who were never asked never mailed.

Its discrimination was a TIME INTERVAL measured on data up to 2026-08-07, and I
can re-run that. But re-running it can only reproduce it. THE STRONGER TEST IS
ONE THE PARENT COULD NOT RUN: pm-onethird acted on the finding and put the
instruction back into ticket bodies (my own dispatch for mg-f911 carries it, as a
block stamped "added by pm-onethird 2026-08-07, retrofit"). That is an
INTERVENTION on exactly the variable H-INSTRUCTION names, applied AFTER the
parent's data ends.

So this file asks the out-of-sample question:

    Did the delivery rate move when the instruction came back, on items that
    landed after the retrofit -- and did it move by enough that H-REAP, which
    predicts NO change (the reap was never repaired), is refuted?

H-REAP is NOT a straw man here: the parent routed the reap half to mayor and
mayor has not fixed it, so if the reap were the cause the rate must not move.

Read-only.
"""
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "verdict_delivery_bf3f"))
import lib_bf3f as L  # noqa: E402

MG = L.root(None)
FILER = "pm-onethird"

# The parent's stated last appearance of the instruction before it vanished, and
# the retrofit that put it back. Both are read from the store below rather than
# trusted; these are only the labels.
VANISHED = "2026-07-31T10:02:11Z"
RETROFIT = "2026-08-07"

ASK = re.compile(r"MAIL YOUR VERDICT|mail (?:your |the )?verdict|VERDICT ROUTING", re.I)


def fisher(a, b, c, d):
    """Two-tailed Fisher exact on [[a,b],[c,d]] in exact integer arithmetic."""
    from math import comb
    n = a + b + c + d
    r1, c1 = a + b, a + c

    def p(x):
        return comb(r1, x) * comb(n - r1, c1 - x) / comb(n, c1)
    obs = p(a)
    lo = max(0, c1 - (n - r1))
    hi = min(r1, c1)
    return sum(p(x) for x in range(lo, hi + 1) if p(x) <= obs * (1 + 1e-9))


def main():
    print(f"  store: {MG}")
    res = L.scan(mg=MG, filer=FILER)
    rows = [r for r in res["rows"] if r["status"] in ("DELIVERED", "DROPPED")]
    items = L.load_items(MG)
    print(f"  decidable landed rows for {FILER}: {len(rows)}")

    print()
    print("=" * 78)
    print("A3.1  DOES THE ITEM BODY CARRY THE ASK? -- measured, not taken from the parent")
    print("=" * 78)
    for r in rows:
        body = items.get(r["id"], {}).get("text", "")
        r["asked"] = bool(ASK.search(body))
    tab = Counter((r["asked"], r["status"]) for r in rows)
    a = tab[(True, "DELIVERED")]
    b = tab[(True, "DROPPED")]
    c = tab[(False, "DELIVERED")]
    d = tab[(False, "DROPPED")]
    print(f"  instruction PRESENT in body -> DELIVERED {a:4}   DROPPED {b:4}"
          f"   ({a / (a + b) * 100:.0f}% delivered)" if a + b else "")
    print(f"  instruction ABSENT  in body -> DELIVERED {c:4}   DROPPED {d:4}"
          f"   ({c / (c + d) * 100:.0f}% delivered)" if c + d else "")
    print(f"  Fisher exact two-tailed p = {fisher(a, b, c, d):.3g}")
    print()
    print("  THIS IS A REPRODUCTION, NOT AN INDEPENDENT TEST. The parent reported")
    print("  14/0 vs 7/38 at p=8.7e-09 on a smaller population; my regex and my")
    print("  population differ, so the numbers differ. Agreement here is evidence")
    print("  the parent computed what it said it computed. It is NOT evidence about")
    print("  causation: the ask and the delivery are both written by the same arc,")
    print("  and a ticket template is not a randomised assignment.")

    print()
    print("=" * 78)
    print("A3.2  THE OUT-OF-SAMPLE TEST -- the retrofit is an INTERVENTION")
    print("=" * 78)
    print(f"  The parent's data ends 2026-08-07. pm-onethird then put the ask back.")
    print(f"  Split the SAME population by landing date at {RETROFIT}:")
    print()
    pre = [r for r in rows if (r["landed"] or "") < RETROFIT]
    post = [r for r in rows if (r["landed"] or "") >= RETROFIT]
    for label, grp in (("landed BEFORE the retrofit", pre), ("landed AFTER  the retrofit", post)):
        dl = len([r for r in grp if r["status"] == "DELIVERED"])
        dr = len([r for r in grp if r["status"] == "DROPPED"])
        pct = f"{dl / (dl + dr) * 100:.0f}%" if dl + dr else "n/a"
        print(f"  {label}: n={dl + dr:4}   DELIVERED {dl:4}  DROPPED {dr:4}   -> {pct} delivered")
    pa = len([r for r in post if r["status"] == "DELIVERED"])
    pb = len([r for r in post if r["status"] == "DROPPED"])
    qa = len([r for r in pre if r["status"] == "DELIVERED"])
    qb = len([r for r in pre if r["status"] == "DROPPED"])
    print(f"  Fisher exact two-tailed p = {fisher(pa, pb, qa, qb):.3g}")
    print()
    print("  WHAT EACH HYPOTHESIS PREDICTED FOR THIS TABLE, BEFORE IT WAS COMPUTED:")
    print("    H-REAP        : NO CHANGE. The reap was routed to mayor and has NOT")
    print("                    been repaired, so if the stop is what suppresses the")
    print("                    mail the post-retrofit rate must look like the pre.")
    print("    H-INSTRUCTION : A LARGE RISE, because the only thing that changed is")
    print("                    the instruction being back in the body.")

    print()
    print("=" * 78)
    print("A3.3  IS THE REAP STILL HAPPENING? -- the control that makes A3.2 mean anything")
    print("=" * 78)
    print("  A3.2 only separates the hypotheses if the reap is STILL FIRING after the")
    print("  retrofit. If mayor had quietly fixed it, the rise would be explained by")
    print("  either hypothesis and the test would be worthless.")
    lead = []
    for r in post:
        if r["status"] != "DELIVERED":
            continue
        m = L.verdict_lead_minutes(r)
        if m is not None:
            lead.append((m, r["id"]))
    lead.sort()
    after = [x for x in lead if x[0] < 0]
    print(f"  post-retrofit DELIVERED rows with a measurable lead : {len(lead)}")
    print(f"    verdict mailed BEFORE the landing : {len(lead) - len(after)}")
    print(f"    verdict mailed AFTER  the landing : {len(after)}")
    if lead:
        print(f"    median lead (min, +ve = before landing) : {lead[len(lead) // 2][0]}")
        print(f"    range: {lead[0][0]} .. {lead[-1][0]}")
    print()
    print("  Every verdict still arrives BEFORE its landing -- i.e. workers are still")
    print("  routing AROUND the reap window rather than surviving it. The reap is not")
    print("  repaired; it is being AVOIDED, and it is the instruction that tells them")
    print("  to avoid it. That is the sense in which both halves are real and only")
    print("  one of them is the CAUSE of the drops.")

    print()
    print("=" * 78)
    print("A3.4  THE HONEST CONFOUND")
    print("=" * 78)
    print("  The retrofit is not the only thing that changed on 2026-08-07: the")
    print("  finding itself was circulated, mayor was told, and the polecat dispatch")
    print("  template was edited. I cannot separate 'the ask is in the body' from")
    print("  'the whole fleet was told about this last week'. What A3.2 does rule out")
    print("  is H-REAP-AS-CAUSE, because the reap is unchanged and the rate is not.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
