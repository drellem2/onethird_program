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

AS-OF PINNING, mg-c824.  This section prints LINE NUMBERS INTO DOCUMENTS IT DOES
NOT OWN -- mg-76b2's deliverable, mg-76b2's instrument, Op-Form, and mg-3ce3's
probe in ANOTHER REPOSITORY.  Those addresses are not a property of anything this
audit established; they are offsets into files other tickets amend.  Between this
transcript's commit and 2026-08-13 the deliverable was amended twice (ade980b,
bb6a0ff) and the instrument once (48cbbd8), so a re-run moved 32 lines of the
transcript and CHANGED NO VERDICT -- the same statements, found at new addresses.

That made the transcript NON-REPRODUCIBLE BY CONSTRUCTION, which is worse than it
sounds: this lineage repairs labels under a numbers-neutrality method whose step 1
is "reproduce the committed output byte-identically before touching anything", and
that method COULD NOT BE APPLIED TO THIS INSTRUMENT AT ALL.  mg-be0b's repair
stopped here for exactly that reason.

THE FIX IS TO PIN THE BYTES, NOT TO REFORMAT THE NUMBERS.  A line number into
someone else's file is a volatile address by nature and no printing convention
makes one stable; what CAN be made stable is THE THING ADDRESSED.  So the corpus
is read AT A DECLARED COMMIT via `git show` rather than from the working tree, and
the transcript stamps that commit at the top.  The property this buys:

  * a re-run against the pinned corpus is BYTE-IDENTICAL for as long as AS_OF is
    reachable -- so the numbers-neutrality method applies to this file again;
  * a re-run against a changed corpus (A4_CENSUS_AT=HEAD, or =WORKTREE) differs
    ONLY in the addresses and in the as-of block, both of which the transcript
    marks as address-valued;
  * mg-3ce3's probe is in another repository and CANNOT be pinned from here, so
    its content digest is recorded instead and D1b's addresses are valid at it.

WHAT THIS DOES NOT CHANGE is what the instrument concludes.  Every count, every
census, every classification, every P-score below is exactly what it was.
"""

import hashlib
import os
import re
import subprocess
from libA94 import banner

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DOC_REL = "docs/OneThird-C3-PrefixCapture-mg-76b2.md"
OPFORM_REL = "docs/OneThird-lambda-std-Operative-Form.md"
INSTR_REL = "code/c3_prefix_capture_76b2"
PROBE = ("/Users/daniel/research/one_third_width_three/scripts/"
         "onethird_mg3ce3_L4_near_ordinal_stability_probe.py")

# The commit mg-94c3 audited.  README s0 already names it ("as merged at
# 7b7d093"), and the transcript's own commit c80a4f1 reads THE SAME BYTES for
# every in-repo corpus path -- measured, not assumed: the deliverable blob
# (1b8184c5), the Op-Form blob (c406c73f) and the instrument tree (f69cdef3) are
# identical at 7b7d093 and at c80a4f1.
AS_OF = "7b7d093d2795dc7d3a5c544d50f905be43efcf79"

# mg-3ce3's probe lives in /Users/daniel/research/one_third_width_three, which
# this repository cannot pin.  Its digest at the as-of stamp is recorded so that
# a stale D1b address is distinguishable from a live one.
PROBE_SHA256_AS_OF = \
    "f446211a2cb454df71a360220ff5d21736356f2f706990205803d71f80cdd6cf"

# Override, for re-measuring against a different corpus: any commit-ish, or the
# literal WORKTREE.  Unset is the pinned default and is the only value that
# reproduces the committed transcript.
AT = os.environ.get("A4_CENSUS_AT", "").strip() or AS_OF
# Short form for the per-section address markers: abbreviate a sha, never a name.
AT_SHORT = AT[:7] if re.fullmatch(r"[0-9a-f]{40}", AT) else AT

rc = 0


def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def read_at(rel):
    """REPO/rel as of commit AT.  Every `rel:NNN` this script prints is an offset
    into THESE bytes, so pinning the bytes is what pins the addresses."""
    if AT == "WORKTREE":
        return read(os.path.join(REPO, rel))
    got = subprocess.run(["git", "-C", REPO, "show", f"{AT}:{rel}"],
                         capture_output=True)
    if got.returncode != 0:
        raise SystemExit(f"a4_census: cannot read {rel} at {AT}: "
                         f"{got.stderr.decode('utf-8', 'replace').strip()}\n"
                         f"  (A4_CENSUS_AT={AT!r}; unset it for the pinned run)")
    return got.stdout.decode("utf-8")


def listdir_at(rel):
    if AT == "WORKTREE":
        return sorted(os.listdir(os.path.join(REPO, rel)))
    got = subprocess.run(
        ["git", "-C", REPO, "ls-tree", "--name-only", f"{AT}:{rel}"],
        capture_output=True)
    if got.returncode != 0:
        raise SystemExit(f"a4_census: cannot list {rel} at {AT}: "
                         f"{got.stderr.decode('utf-8', 'replace').strip()}")
    return sorted(got.stdout.decode("utf-8").split())


def mg76b2_files():
    out = [(DOC_REL, read_at(DOC_REL))]
    for fn in listdir_at(INSTR_REL):
        if fn.endswith((".py", ".md", ".sh", ".txt")):
            out.append((f"{INSTR_REL}/{fn}", read_at(f"{INSTR_REL}/{fn}")))
    return out


probe_sha = (hashlib.sha256(read(PROBE).encode("utf-8")).hexdigest()
             if os.path.exists(PROBE) else None)

banner("AS-OF STAMP -- WHICH LINES BELOW ARE ADDRESSES AND WHICH ARE FINDINGS")
print(f"""  in-repo corpus read at : {AT}
      {'AS_OF, the pinned default'
       if AT == AS_OF else
       'OVERRIDE via A4_CENSUS_AT -- NOT the as-of stamp ' + AS_OF[:7]}
  mg-3ce3 probe, sha256  : {probe_sha or 'ABSENT'}
      {'matches the as-of stamp'
       if probe_sha == PROBE_SHA256_AS_OF else
       'MOVED SINCE THE AS-OF STAMP -- D1b ADDRESSES ARE STALE'}

  EVERY `file:NNN` AND EVERY `char NNN` BELOW IS AN ADDRESS, NOT A FINDING.  Each
  is an offset into a file this audit DOES NOT OWN, and it moves whenever another
  ticket amends that file.  They are valid at the commit named above and nowhere
  else.  THE QUOTED LINE UNDER EACH ADDRESS IS THE PRIMARY ADDRESS -- it survives
  the file moving; the number after the colon does not, and is printed second for
  that reason.  The address and its quoted line are ONE OBJECT: if the corpus
  moves, expect BOTH to change together.

  CORPUS-VALUED TOO, and marked where it is printed: the census-universe size on
  the next line, which measures the corpus rather than mg-76b2.

  EVERYTHING ELSE IS STABLE: every count of hits, every classification, every
  verdict and every P-score.  Run with no environment set and this transcript reproduces
  BYTE-IDENTICALLY, because the bytes read are pinned rather than live.  To ask
  the same questions of the CURRENT corpus instead:

      A4_CENSUS_AT=HEAD python3 a4_census.py     (or =WORKTREE, or any commit)

  which RE-MEASURES AND RE-ADDRESSES.  Compare the two runs' VERDICTS; the numbers
  after the colons are expected to differ, and their differing is not a defect in
  either run.
""")

FILES = mg76b2_files()
print(f"  census universe: {len(FILES)} files, "
      f"{sum(t.count(chr(10)) for _, t in FILES)} lines "
      f"(mg-76b2's deliverable AND its whole instrument, transcripts included)")
print(f"  [a SIZE OF THE CORPUS at {AT_SHORT}, so it is corpus-valued like the "
      f"addresses and not a finding]\n")

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
print(f"  {len(hits)} lines mention L4, a modulus, or an F(.) application")
print(f"  [the count is the finding; the `:NNN` are ADDRESSES at {AT_SHORT}]:\n")
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

    C_3 = 1                <- L2's FIRST DISJUNCT, Cheeger's hard half,
                              |A\\sigma(A)|=|A^c\\sigma(A^c)|, and
                              'monotone ==> threshold sets are prefixes'.  No F.
    eps_dem = eps_leak^2/2 <- C_3 = 1 and eps_leak.                        No F.
    2x10^-2                <- eps_leak = 1/5.                              No F.
    n >= 99                <- eps_dem and the mg-200d conjecture.          No F.
    c > 1 - eps_leak       <- eps_leak and Lemma 2.1.                      No F.
    c > 0.80 / c > 0.98    <- eps_leak = 0.20 / 0.02.                      No F.
    (II) vs (III) = 10     <- 2/eps_leak.                                  No F.

  (SCOPE ADDED AT THE CLAIM, mg-c824, on mg-be0b's finding, which is on mg-3329's,
  which is on mg-fa70's.  Row 1 read "<- L2", and L2 is a DISJUNCTION -- "a
  dominant standard eigenvector is monotone in the distinguished order, OR AT
  LEAST YIELDS A LOW-CONDUCTANCE PREFIX", carried on STATE.md's ledger ROW 9,
  which carries it on mg-76b2's document, which carries it on a .tex that is NOT
  IN THIS REPOSITORY and was not re-read here.  So an unqualified "L2" reads as
  EITHER disjunct, while C_3 = 1 is established on the FIRST.  The clause this row
  ALREADY carried, 'monotone ==> threshold sets are prefixes', IS that first
  disjunct -- so nothing computed changes and NO NUMBER MOVES; only the label
  over-reached.  The second disjunct is UNQUANTIFIED -- weaker than and different
  from refuted -- and is not struck here.  This is the site mg-be0b's sweep STOPPED
  AT, because step 1 of the numbers-neutrality method failed here; the as-of
  pinning stamped above is what makes it pass, and it passes: 23 of 23 addresses
  and every numeric token of the previous transcript are unchanged across this
  edit.

  THE CITATION IS BY ROW, NOT BY LINE, AND THAT IS THIS TICKET'S OWN LESSON TURNED
  ON ITSELF.  This note first read "STATE.md:116" -- a line number into a document
  a4_census does not own, i.e. the exact defect being repaired, reintroduced inside
  the repair.  It was ALREADY WRONG when written: the text is at STATE.md:126
  today.  A ledger ROW NUMBER is an identity and survives the file moving; a line
  number is an address and does not.)

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
    print(f"  {len(plines)} lines.  The predicate that calibrates eps_leak")
    print(f"  [ANOTHER REPOSITORY -- unpinnable from here; the `:NNN` are")
    print(f"   addresses valid at sha256 {PROBE_SHA256_AS_OF[:16]}...]:\n")
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
print(f"  {len(occ)} occurrences")
print(f"  [the count and each [labelled]/[BARE] verdict are the finding;")
print(f"   the `:NNN` are ADDRESSES at {AT_SHORT}]:\n")
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
op = read_at(OPFORM_REL)
ban_start = op.find("SUPERSEDED INPUT")
ban = op[ban_start:ban_start + 3000] if ban_start >= 0 else ""
lists = re.findall(r"§§?[\d.]+(?:[–-]§?[\d.]+)?", ban)
print(f"  supersession banner, anchored on the string it is found by:")
print(f"      \"{ban.splitlines()[0][:70] if ban else 'NOT FOUND'}\"")
print(f"  [ADDRESS at {AT_SHORT}, and the coarsest one here -- a raw byte offset]")
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
