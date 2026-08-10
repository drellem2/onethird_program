#!/usr/bin/env python3
"""s3 — ADJUDICATION. Which collisions are the ticket's defect and which are my join being loose.

P1 bet my own headline is an over-count. Betting that and then hand-waving each case down
is the cheapest way to be right, so every disqualification here is made by a rule that
runs, and the rule is stated before the verdict:

  D1  LANDING-OF-THE-AUDIT.  The landing NAMES THE AUDIT in its own title or body head.
      A landing that knows the audit exists is not "reading figures the audit is in the
      middle of repairing" -- it is CARRYING the audit, which is remedy (b) already
      working. This is a category P1 did not name and it is the largest one.

  D2  AUDIT-OF-THE-LANDING.  The audit's declared subject IS the landing. Then the audit
      is downstream of the landing, not of its parent, and the triple is backwards.

  D3  SUBJECT MISMATCH.  The audit's title says "INDEPENDENT AUDIT of mg-XXXX" and that
      explicit subject is NOT the parent in the triple. The join reached this audit through
      a prose mention, not through what it audits. P1's reason (b).

  D4  SELF-AUTHORED.  The landing's canonical commits touch only documents named after
      the LANDING itself -- it authored its own document rather than carrying a parent's
      figures outward. P1's reason (a).

What survives all four is the RESIDUE: a landing that did not know about the audit, whose
audit really is of its parent, and which really did edit a document it did not author.
"""
import json
import os
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib64cb as L

B = L.build()
one, idx = B["one"], B["idx"]
L.banner("s3 — ADJUDICATION", __doc__.strip())

EXPLICIT = re.compile(r"INDEPENDENT AUDIT of\s+(mg-[0-9a-f]{4})", re.I)


def explicit_subject(aid):
    a = one.get(aid)
    if not a:
        return None
    m = EXPLICIT.search(a["title"])
    return m.group(1) if m else None


def d1_landing_names_audit(lid, aid):
    v = one[lid]
    return aid in v["title"] or aid in v["body"][:1500]


def d2_audit_of_the_landing(lid, aid):
    return lid in L.parents(one[aid]) if aid in one else False


def d3_subject_mismatch(pid, aid):
    es = explicit_subject(aid)
    return es is not None and es != pid


def d4_self_authored(lid):
    """Every canonical file the landing touched is a doc named after the landing itself."""
    files = set()
    import subprocess
    for h in idx.get(lid, {}).get("canonical", []):
        out = subprocess.run(["git", "-C", L.REPO, "log", "-1", "--format=", "--name-only", h],
                             capture_output=True, text=True).stdout.split()
        files |= {f for f in out if L.is_canonical(f)}
    if not files:
        return True, files
    stem = lid.split("-")[1]
    return all(stem in f for f in files), files


rows = [t for t in B["triples"] if "CONCURRENT" in (t["wall"], t["write"])]
print(f"count triples CONCURRENT under either reading {len(rows)}\n")

survivors, killed = [], []
for t in sorted(rows, key=lambda x: x["landing"]):
    lid, pid, aid = t["landing"], t["parent"], t["audit"]
    d1 = d1_landing_names_audit(lid, aid)
    d2 = d2_audit_of_the_landing(lid, aid)
    d3 = d3_subject_mismatch(pid, aid)
    d4, files = d4_self_authored(lid)
    fired = [n for n, f in (("D1", d1), ("D2", d2), ("D3", d3), ("D4", d4)) if f]
    verdict = "DISQUALIFIED" if fired else "RESIDUE"
    print(f"  {lid} par={pid} aud={aid}  wall={t['wall']:12s} write={t['write']:12s} "
          f"STATE={'y' if t['state'] else 'n'}")
    print(f"     explicit audit subject: {explicit_subject(aid)}")
    print(f"     D1 landing-names-audit {d1}   D2 audit-of-landing {d2}   "
          f"D3 subject-mismatch {d3}   D4 self-authored {d4}")
    print(f"     -> {verdict}" + (f"  (fired: {','.join(fired)})" if fired else ""))
    print()
    (killed if fired else survivors).append(dict(t, fired=fired))

print("=" * 78)
print(f"count DISQUALIFIED {len(killed)}")
print(f"count RESIDUE      {len(survivors)}")
print()
import collections
c = collections.Counter(f for k in killed for f in k["fired"])
print("WHICH RULE DID THE KILLING (a triple can fire more than one):")
for k, v in c.most_common():
    print(f"  count {k} {v}")
print()
print("THE RESIDUE — every one of these is the ticket's shape:")
print(f"  {'landing':9s} {'parent':9s} {'audit':9s} {'tier':9s} {'wall':12s} {'write':12s}")
for s in survivors:
    print(f"  {s['landing']:9s} {s['parent']:9s} {s['audit']:9s} "
          f"{'STATE.md' if s['state'] else 'docs-only':9s} {s['wall']:12s} {s['write']:12s}")
print(f"  count rows in them {len(survivors)}")
print(f"  count of them touching STATE.md {sum(1 for s in survivors if s['state'])}")

json.dump(dict(residue=survivors, killed=killed),
          open(os.path.join(L.SELF_DIR, "adjudicated.json"), "w"), indent=1, default=str)
