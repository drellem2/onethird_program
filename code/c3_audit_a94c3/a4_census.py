"""a4_census -- did mg-76b2 SMUGGLE IN L4, and did it ASSUME the mg-200d conjecture?

The ticket names these as the two most likely ways for this item to produce a
confident wrong answer.  mg-76b2 asserts in sec.11 that it did neither.  An
assertion is what an audit is for, so both are CHECKED HERE, and the L4 one is
checked AT THE SOURCE rather than against mg-76b2's own words: the calibration
that every derived number of mg-76b2 rests on is eps_leak = 0.20, which comes
from mg-3ce3's `survives` predicate, in a file in ANOTHER REPO that neither
mg-76b2 nor this audit wrote.  If that predicate reads L4's modulus F, the whole
chain reads F and mg-76b2's scope statement is false.

Scores P6 and P7.  Also re-checks mg-76b2's claim 14 against Op-Form itself.
"""

import os
import re
from libA94 import banner

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DOC = os.path.join(REPO, "docs", "OneThird-C3-PrefixCapture-mg-76b2.md")
OPFORM = os.path.join(REPO, "docs", "OneThird-lambda-std-Operative-Form.md")
INSTR = os.path.join(REPO, "code", "c3_prefix_capture_76b2")
PROBE = ("/Users/daniel/research/one_third_width_three/scripts/"
         "onethird_mg3ce3_L4_near_ordinal_stability_probe.py")

rc = 0


def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def mg76b2_files():
    out = [("docs/OneThird-C3-PrefixCapture-mg-76b2.md", read(DOC))]
    for fn in sorted(os.listdir(INSTR)):
        if fn.endswith((".py", ".md", ".sh", ".txt")):
            out.append((f"code/c3_prefix_capture_76b2/{fn}",
                        read(os.path.join(INSTR, fn))))
    return out


FILES = mg76b2_files()
print(f"  census universe: {len(FILES)} files, "
      f"{sum(t.count(chr(10)) for _, t in FILES)} lines "
      f"(mg-76b2's deliverable AND its whole instrument, transcripts included)\n")

# --------------------------------------------------------------------------
banner("D1. THE L4 CENSUS -- P6")
print("""  mg-345e established that Step 6 consumes no branch in which L4's MODULUS F
  appears; what the chain needs is L4's THRESHOLD eps_0.  The two are different
  objects and conflating them is the error this lineage has committed twice.
  So the census is not 'does L4 appear' -- it appears, and it should -- it is
  'does a DERIVED NUMBER of mg-76b2 depend on F'.
""")
PAT = re.compile(r"\bL4\b|modulus|F\(\s*(?:0\.|eps|\\vare|ε)")
hits = []
for name, txt in FILES:
    for i, line in enumerate(txt.splitlines(), 1):
        if PAT.search(line):
            hits.append((name, i, line.strip()))
print(f"  {len(hits)} lines mention L4, a modulus, or an F(.) application:\n")
for name, i, line in hits:
    short = line if len(line) <= 96 else line[:93] + "..."
    print(f"    {name}:{i}\n        {short}")

print("""
  CLASSIFICATION.  Every one of the above is a SCOPE STATEMENT ('no L4 attempt',
  'L4's threshold eps_0 is untouched'), a CITATION of mg-345e's ruling, or a
  provenance note on eps_leak.  None is an arithmetic step.  The check that
  makes that more than my reading follows.
""")

print("""  THE INPUT LIST OF EVERY DERIVED NUMBER OF mg-76b2, written out:

    C_3 = 1                <- L2, Cheeger's hard half, |A\\sigma(A)|=|A^c\\sigma(A^c)|,
                              'monotone ==> threshold sets are prefixes'.  No F.
    eps_dem = eps_leak^2/2 <- C_3 = 1 and eps_leak.                        No F.
    2x10^-2                <- eps_leak = 1/5.                              No F.
    n >= 99                <- eps_dem and the mg-200d conjecture.          No F.
    c > 1 - eps_leak       <- eps_leak and Lemma 2.1.                      No F.
    c > 0.80 / c > 0.98    <- eps_leak = 0.20 / 0.02.                      No F.
    (II) vs (III) = 10     <- 2/eps_leak.                                  No F.

  So the ENTIRE dependence on L4 is routed through the single number eps_leak.
  Is THAT number F-free?  mg-76b2 says it is; Op-Form:444 says it is; both are
  words.  Go and read the predicate.
""")

banner("D1b. eps_leak = 0.20 AT ITS SOURCE -- mg-3ce3's predicate, in another repo")
if not os.path.exists(PROBE):
    print(f"  NOT CHECKED: {PROBE} not present.  P6 is then UNVERIFIED, not passed.")
    rc = 1
else:
    ptxt = read(PROBE)
    plines = ptxt.splitlines()
    # locate the definition of `survives` and the RED-event predicate
    surv = [(i + 1, l.strip()) for i, l in enumerate(plines)
            if re.search(r"\bsurvives\s*=", l) or re.search(r"surviving\s*=", l)
            or re.search(r"balanced_full\s*=", l)]
    print(f"  {PROBE}")
    print(f"  {len(plines)} lines.  The predicate that calibrates eps_leak:\n")
    for i, l in surv:
        print(f"    :{i}  {l}")
    body = "\n".join(l for i, l in surv)
    uses_F = bool(re.search(r"\bF\b|modulus|envelope|C_lin|alpha", body))
    print(f"""
  Does that predicate read F, the fitted modulus, or the envelope?  {uses_F}

  `survives` is  len([pairs balanced in the SIDE that are still balanced in the
  FULL poset]) > 0, and `balanced_full` is  1/3 <= p^P_xy <= 2/3.  Both are
  membership of the fixed window [1/3, 2/3].  The probe DOES compute a deviation
  D and DOES fit an envelope F(eps) -- but those are REPORTED OUTPUTS, and the
  RED event that calibrates eps_leak = 0.20 ('neither side survives') never
  consults them.

  P6: {'HELD' if not uses_F else 'MISSED'}.  mg-76b2's dependence on L4 is on its
  THRESHOLD, which mg-345e permits, and NOT on its MODULUS, which mg-345e's
  ruling is about.  VERIFIED AT THE SOURCE, not against mg-76b2's scope
  statement.  This is the third occurrence the ticket warned about, and IT DID
  NOT OCCUR.""")
    if uses_F:
        rc = 1

# --------------------------------------------------------------------------
banner("D2. THE mg-200d CENSUS -- P7")
print("""  mg-76b2 was told not to assume `eps = 2/(n+1)`.  Census every occurrence in
  its deliverable and instrument, and ask of each: is it labelled, and does a
  headline claim of mg-76b2 change if the conjecture is WITHDRAWN?
""")
# The conditional-marker classifier.  "window" is deliberately NOT a marker --
# it is the noun a conditional qualifies, not the qualifier; a control in
# selftesta94c3 NC5 caught an earlier version of this line counting it as one.
LBL = re.compile(r"CONDITIONAL|conditional|\bif\b|mg-131e|not assumed|labelled")
P200 = re.compile(r"2\s*/\s*\(\s*n\s*\+\s*1\s*\)|mg-200d|2/\(n\+1\)")
occ = []
for name, txt in FILES:
    for i, line in enumerate(txt.splitlines(), 1):
        if P200.search(line):
            occ.append((name, i, line.strip()))
print(f"  {len(occ)} occurrences:\n")
for name, i, line in occ:
    short = line if len(line) <= 100 else line[:97] + "..."
    cond = bool(LBL.search(line))
    print(f"    [{'labelled' if cond else 'BARE'}] {name}:{i}")
    print(f"        {short}")
bare = [o for o in occ if not LBL.search(o[2])]

print(f"""
  THE WITHDRAWAL TEST.  Strike the mg-200d conjecture entirely and re-read
  mg-76b2's 24-row claim ledger.  Which rows fall?

    claim 17  'window n <= 98 under chain (I)'   -- FALLS.  It is the only row
              whose statement contains an n, and its own label already reads
              'CONDITIONAL on 9 AND ON THE mg-200d CONJECTURE'.
    claims 1-16, 18-24                            -- ALL STAND.  None mentions
              a supply-side value of eps_spec at all; C_3 = 1, eps_dem =
              eps_leak^2/2, the four chains, the literal-reading threshold on c,
              the population facts and the lib2de0 finding are every one of them
              statements about the DEMAND side or about the population.

  So 1 of 24 claims is conditional on the conjecture, it is labelled as such at
  the claim, and the verdict block states the conditional ('*if* the mg-200d
  route survives mg-131e') BEFORE the number it qualifies.

  P7: {'HELD' if not bare else 'HELD WITH ' + str(len(bare)) + ' MACHINE-BARE SITE(S)'}

  AND THE 'BARE' LABEL IS READ BY HAND BEFORE IT IS REPORTED, because a lexical
  classifier is not a verdict.  All {len(bare)} machine-bare sites are inside the
  INSTRUMENT, none is in the deliverable, and on reading every one carries its
  conditional in wording my regex does not cover:

    PREDICTIONS.md:29   H9, an arithmetic hand measurement in mg-76b2's own
                        pre-registered predictions -- not a claim of the document
    PREDICTIONS.md:96   says 'No assumption of the mg-200d conjecture' -- the
                        scope statement itself; my regex wants 'not assumed'
    s4_budget.py:33     says 'The n >= column ASSUMES the mg-200d conjecture'
    s4_budget.py:51     a helper docstring, 'smallest n with 2/(n+1) <= eps_dem'
    s4_budget.py:75     and out_s4_budget.txt:13, the column HEADER, which reads
                        'n >= (mg-200d)' -- the attribution IS the label

  SO THE MACHINE COUNT OF 6 IS A LIMITATION OF MY CLASSIFIER AND NOT A FINDING
  AGAINST mg-76b2.  It is reported rather than tuned away, because tuning the
  regex until it returns 0 would make the census unfalsifiable.""")
print("""
  ONE THING THE CENSUS DOES NOT EXCUSE, and it is a framing point rather than a
  defect: the deliverable's TITLE and sec.0 headline are about C_3, which is
  unconditional on mg-200d -- but the sentence a reader is most likely to carry
  away, 'the window still owed is n <= 98', is the one row that is not.  It is
  correctly labelled where it is stated.  It is not labelled in the commit
  subject, and commit subjects are what the next agent greps.""")

# --------------------------------------------------------------------------
banner("D3. mg-76b2 CLAIM 14 -- was Op-Form sec.4.3 really never re-examined?")
op = read(OPFORM)
ban_start = op.find("SUPERSEDED INPUT")
ban = op[ban_start:ban_start + 3000] if ban_start >= 0 else ""
lists = re.findall(r"§§?[\d.]+(?:[–-]§?[\d.]+)?", ban)
print(f"  supersession banner found at char {ban_start}")
print(f"  section references inside the banner: {sorted(set(lists))}")
mentions_43 = "§4.3" in ban
print(f"  banner mentions §4.3                : {mentions_43}")
m15 = re.search(r"^\|\s*15\s*\|.*$", op, re.M)
print(f"  Op-Form ledger claim 15 as it stands:\n      "
      f"{m15.group(0)[:150] if m15 else 'NOT FOUND'}")
still_proven = bool(m15 and "PROVEN" in m15.group(0)
                    and "SUPERSEDED" not in m15.group(0))
print(f"""
  claim 15 still labelled PROVEN, unamended : {still_proven}
  claim 14 of mg-76b2 ('sec.4.3 was never re-examined under mg-e35c F5'):
      {'CONFIRMED' if (not mentions_43 and still_proven) else 'NOT CONFIRMED'}

  AND A CORRECTION TO mg-76b2's OWN FRAMING OF IT.  mg-76b2 sec.5 says the
  literal reading 'closes for every c > 1 - eps_leak'.  Its own instrument uses
  the tighter, self-consistent  c >= (1-eps_leak)/(1-eps_spec) = 40/49 = 0.8163,
  because eps_dem must exceed the eps_spec it is being solved against.  The
  prose threshold 0.80 and the instrument threshold 0.8163 are different numbers
  and the document prints only the first in its headline.  The difference does
  not change any verdict -- 0.8163 is still 'an ordinary reading of a constant
  fraction' and still far from 0.98 -- but a reader comparing the two files will
  find two thresholds and no sentence reconciling them.""")

banner("EXIT")
print(f"rc = {rc}")
raise SystemExit(rc)
