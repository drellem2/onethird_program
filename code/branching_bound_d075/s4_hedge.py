"""S4 -- BOUNDED, NOT MERELY HEDGED.  And the predecessor's own hedge figure,
counted instead of quoted.

THE STANDARD IS INHERITED, NOT INVENTED.  mg-19ec's test was: take every phrasing
the repair introduced, and scan THE SENTENCE THAT CONTAINS IT for hedge tokens -- a
hedge is a property of the claim's own sentence, not of a helpful neighbour.  Its
one weaker construction, "of the same KIND", was defended not by asserting it was
fine but by ENUMERATING what falls inside it.  That is the test applied here.

  H1  THE NEW PHRASINGS.  Population: live sentences of
      docs/OneThird-Branching-Graphs-Where-This-Lives.md that exist after this
      repair and did not exist before it, the pre-repair text read out of git at
      the derived anchor.  Grain: one sentence.  This is a superset of the sites
      -- a repair that added prose elsewhere would be caught too.

  H2  THE SCAN.  Each new sentence against the hedge-token list.  The list is
      mg-19ec's own 25 tokens, VERBATIM, plus 8 this repair adds, = 33 tokens.
      A sentence carrying a token is NOT automatically a failure: the inherited
      standard is that a weaker word is admissible when the sentence ENUMERATES
      or states the scope of what falls inside it.  So a hedged sentence must ALSO
      carry an enumeration or a numeric scope, or it fails.

  H3  IS THE BOUND AN ENUMERATION OR A SOFTENING?  For each of the 9 sites, the
      exact substring that carries the bound is printed, and classified as
      NUMERIC SCOPE / ENUMERATION / SOFTENING WORD.  A site whose bound is a
      softening word fails.  Printing the substring is the point: "bounded" as a
      boolean is exactly the kind of claim this arc keeps finding hollow.

  H4  THE PREDECESSOR'S OWN FIGURE, COUNTED.  mg-19ec's published audit states,
      twice, that the phrasings were scanned "against 26 hedge tokens".  Its
      instrument's HEDGES list is read here and its length counted.  Its own
      transcript's phrasing count is read too, and compared with the "13" that
      reached the recovered verdict.  Population: the literal figures in
      docs/OneThird-Warrant-Repair-mg-dffa-IndependentAudit.md and the values its
      own code and transcript carry.  Grain: one figure.  Reported whichever way
      it comes out; this script does not gate on it, because a finding against a
      predecessor is not a reason for MY repair to fail.

EXIT 0 if H1-H3 hold.  PREDICTED 0.
"""

import os
import re
import subprocess
import sys

import lib_d075 as L

OUT = sys.stdout
ITEM = "mg-d075"
RELPATH = "docs/OneThird-Branching-Graphs-Where-This-Lives.md"
AUDITDOC = os.path.join(L.DOCS, "OneThird-Warrant-Repair-mg-dffa-IndependentAudit.md")
PARENTSRC = os.path.join(L.ROOT, "code", "branching_audit_19ec", "e2_f2_clauses.py")
PARENTOUT = os.path.join(L.ROOT, "code", "branching_audit_19ec",
                         "out_e2_f2_clauses.txt")

# mg-19ec's list, copied verbatim from code/branching_audit_19ec/e2_f2_clauses.py.
INHERITED = [
    "may ", "might", "could be", "appears", "seems", "arguably", "roughly",
    "broadly", "essentially", "in some sense", "more or less", "largely",
    "generally", "tends to", "presumably", "plausibly", "believed",
    "on mg-af28's reading", "which nobody", "has not re-read", "to a degree",
    "something like", "in effect", "effectively", "for the most part",
]
# Added by this repair.  "kind" and "some" are here ON PURPOSE: they are the
# tokens a bounding repair is most tempted to lean on, and the inherited standard
# is that they survive only by enumeration.
ADDED = ["kind", "some ", "several", "various", "approximately", "about ",
         "nearly", "almost"]
HEDGES = INHERITED + ADDED

NUMERIC = re.compile(r"rank\s*\(?w?\)?\s*(?:≤|<=)\s*\d"
                     r"|to rank \d|of size ≤ \d|of size <= \d"
                     r"|`?n`?\s*(?:≤|<=)\s*\d|\|λ\|\s*(?:≤|<=)\s*\d")
ENUM = re.compile(r"\b\d+ of (?:the )?\d+\b|\b\d+ of \d+\b"
                  r"|\b\d+ (?:intervals|partitions|classes|posets|pairs)\b"
                  r"|— .*?,.*?,.*? —")


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=L.ROOT, capture_output=True,
                          text=True).stdout


def baseline_commit():
    for row in git("log", "--format=%H\t%s", "--", RELPATH).strip().split("\n"):
        if not row.strip():
            continue
        h, _, subj = row.partition("\t")
        if ITEM not in subj:
            return h
    return None


def main():
    bad = 0

    def ck(label, ok, extra=""):
        nonlocal bad
        print("    %-58s %s%s" % (label, "ok" if ok else "BAD", extra), file=OUT)
        if not ok:
            bad += 1

    L.rule(OUT, "S4  BOUNDED, NOT MERELY HEDGED -- and the predecessor's own\n"
                "    hedge figure counted rather than quoted.")
    print(file=OUT)

    h = baseline_commit()
    tmp = os.path.join(L.HERE, ".baseline_doc.md")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(git("show", "%s:%s" % (h, RELPATH)))

    def norm(s):
        return re.sub(r"\s+", " ", s).strip()

    old = {norm(s) for _, _, s, _ in L.live_sentences(tmp)}
    new = [(a, b, norm(s)) for a, b, s, _ in L.live_sentences(L.DOC)]
    fresh = [t for t in new if t[2] not in old]

    # ------------------------------------------------------------------ H1
    L.rule(OUT, "  H1  THE NEW PHRASINGS.  Population: live sentences of the\n"
                "      document present after this repair and absent before it.\n"
                "      Grain: one sentence.  Anchor: %s" % (h or "")[:12])
    # BOTH SIDES AS DISTINCT NORMALISED SENTENCES.  The first form of this print
    # compared len(set) before against len(list) after -- 297 vs 316 -- which is a
    # grain mismatch of exactly the kind this repair is about, in this repair's own
    # output.  Occurrence counts are printed too, and labelled.
    print("    live sentence OCCURRENCES  before : %d   after : %d"
          % (len(list(L.live_sentences(tmp))), len(new)), file=OUT)
    print("    DISTINCT live sentences    before : %d   after : %d"
          % (len(old), len({t[2] for t in new})), file=OUT)
    print("    NEW distinct sentences            : %d" % len(fresh), file=OUT)
    print(file=OUT)
    for i, (line, kind, s) in enumerate(fresh, 1):
        print("    [%02d] line %-4d %-5s %s" % (i, line, kind, s[:104]), file=OUT)
        for j in range(104, len(s), 104):
            print("                            %s" % s[j:j + 104], file=OUT)
        print(file=OUT)
    ck("the repair introduced at least one new sentence", len(fresh) >= 1,
       "   (%d)" % len(fresh))
    print(file=OUT)

    # ------------------------------------------------------------------ H2
    L.rule(OUT, "  H2  THE SCAN.  %d hedge tokens -- mg-19ec's %d verbatim plus %d\n"
                "      added by this repair -- against EACH new sentence's OWN text."
                % (len(HEDGES), len(INHERITED), len(ADDED)))
    print("    inherited : %s" % ", ".join(t.strip() for t in INHERITED[:13]),
          file=OUT)
    print("                %s" % ", ".join(t.strip() for t in INHERITED[13:]),
          file=OUT)
    print("    added     : %s" % ", ".join(t.strip() for t in ADDED), file=OUT)
    print(file=OUT)
    hedged, unrescued = 0, []
    for i, (line, kind, s) in enumerate(fresh, 1):
        low = s.lower()
        hits = [t.strip() for t in HEDGES if t in low]
        if not hits:
            print("    [%02d] line %-4d definite -- no hedge token" % (i, line),
                  file=OUT)
            continue
        hedged += 1
        rescue = bool(NUMERIC.search(s)) or bool(ENUM.search(s))
        print("    [%02d] line %-4d HEDGE %-22s %s" %
              (i, line, ",".join(hits),
               "ENUMERATED -> admissible" if rescue else "NOT ENUMERATED -> FAIL"),
              file=OUT)
        if rescue:
            m = NUMERIC.search(s) or ENUM.search(s)
            print("         what falls inside it, stated: %s" % m.group(0)[:80],
                  file=OUT)
        else:
            unrescued.append((line, hits, s))
    print(file=OUT)
    print("    new sentences carrying a hedge token : %d of %d"
          % (hedged, len(fresh)), file=OUT)
    print("    of those, NOT rescued by enumeration : %d" % len(unrescued),
          file=OUT)
    ck("no new phrasing hedges without enumerating what is inside it",
       not unrescued, "   (%d)" % len(unrescued))
    for line, hits, s in unrescued:
        print("      line %d: %s -- %s" % (line, ",".join(hits), s[:90]), file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------------ H3
    L.rule(OUT, "  H3  IS THE BOUND AN ENUMERATION OR A SOFTENING?  Population:\n"
                "      the 9 sites.  Grain: the exact substring carrying the bound.")
    sites = L.relaxed_sites(L.DOC)
    softening = []
    for i, (line, kind, s, b) in enumerate(sites, 1):
        m = L.RANK6.search(s)
        sub = m.group(0) if m else "<none>"
        cls = ("NUMERIC SCOPE" if m and re.search(r"\d", sub) else "SOFTENING WORD")
        also = "yes" if ENUM.search(s) else "no"
        print("    <%02d> line %-4d bound=%-14s class=%-14s enumeration in sentence: %s"
              % (i, line, "`%s`" % sub, cls, also), file=OUT)
        if cls != "NUMERIC SCOPE":
            softening.append(line)
    print(file=OUT)
    ck("every site's bound is a numeric scope, not a softening word",
       not softening, "   (%d softening)" % len(softening))
    ck("every site is bounded", all(t[3] for t in sites),
       "   (%d of %d)" % (sum(1 for t in sites if t[3]), len(sites)))
    print(file=OUT)

    # ------------------------------------------------------------------ H4
    L.rule(OUT, "  H4  THE PREDECESSOR'S OWN FIGURE, COUNTED.  Not gated on.\n"
                "      Population: the hedge-token and phrasing figures stated in\n"
                "      mg-19ec's published audit vs. the values its own code and\n"
                "      transcript carry.  Grain: one figure.")
    src = open(PARENTSRC, encoding="utf-8").read()
    blk = src[src.index("HEDGES = ["):src.index("]", src.index("HEDGES = [")) + 1]
    ns = {}
    exec(blk, ns)
    n_code = len(ns["HEDGES"])
    doc = open(AUDITDOC, encoding="utf-8").read()
    stated = re.findall(r"against (\d+) hedge tokens", doc)
    tr = open(PARENTOUT, encoding="utf-8").read()
    m = re.search(r"no new phrasing sits in a hedged sentence\s+ok \((\d+) of "
                  r"(\d+) hedged\)", tr)
    tr_pop = m.group(2) if m else "?"
    print("    figure stated in the published audit prose : %s"
          % (", ".join(stated) or "<none found>"), file=OUT)
    print("    tokens actually in the instrument's HEDGES : %d" % n_code, file=OUT)
    print("    times the transcript prints a token count  : %d"
          % len(re.findall(r"hedge token", tr)), file=OUT)
    print("    phrasing population in the transcript      : %s" % tr_pop, file=OUT)
    print("    phrasing population in the recovered verdict: 13"
          "  (mg-d075's brief, quoting mg-19ec's commit message)", file=OUT)
    print(file=OUT)
    agree_tok = all(int(x) == n_code for x in stated) if stated else None
    print("    FINDING, and it is of THIS ARC'S OWN CLASS.", file=OUT)
    print("      the token figure %s: prose says %s, code carries %d"
          % ("AGREES" if agree_tok else "DISAGREES",
             "/".join(stated) or "-", n_code), file=OUT)
    print("      the phrasing figure %s: transcript %s, verdict 13"
          % ("AGREES" if tr_pop == "13" else "DISAGREES", tr_pop), file=OUT)
    print(file=OUT)
    print("    Both are the same shape as the defect this repair lands: a figure", file=OUT)
    print("    stated in prose that no instrument computes.  Neither is scored", file=OUT)
    print("    against this repair and neither is repaired here -- mg-19ec's", file=OUT)
    print("    audit document is a dated record.  They are handed to mg-aaf4.", file=OUT)
    print(file=OUT)

    os.remove(tmp)
    L.rule(OUT)
    print("SUMMARY s4_hedge: %d new sentence(s); %d carry a hedge token; %d "
          "unrescued" % (len(fresh), hedged, len(unrescued)), file=OUT)
    print("SUMMARY s4_hedge: %d hedge tokens (%d inherited + %d added)"
          % (len(HEDGES), len(INHERITED), len(ADDED)), file=OUT)
    print("SUMMARY s4_hedge: %d of %d site bounds are numeric scopes"
          % (len(sites) - len(softening), len(sites)), file=OUT)
    print("SUMMARY s4_hedge: predecessor prose says %s hedge tokens, its code "
          "carries %d" % ("/".join(stated) or "-", n_code), file=OUT)
    print("SUMMARY s4_hedge: failures %d" % bad, file=OUT)
    L.rule(OUT)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
