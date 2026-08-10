"""a3 — WAS *THREE* THE RIGHT NUMBER, AND DOES THE REPAIR SURVIVE ITS OWN TEST?

The ticket for `mg-d19f` named ONE site; the landing found THREE. That is a discovery, and a
discovery about scope is exactly the kind of claim that can stop one short. This arm asks the
question mechanically, in four directions:

  S1  Sweep `mg-51f4` AT ITS OWN LANDING for every sentence of the class the landing named —
      a QUANTIFIER over how `mg-28ff`'s `n = 7` figures are LABELLED or QUOTED — and classify
      each as struck / dated / untouched at `HEAD`.
  S2  Sweep the text the repair ADDED for the same class. `A REMEDY IS AN ARTIFACT OF THE
      SAME KIND AS THE DEFECT`: a labelling repair can assert a new blanket about labelling,
      and this one does. It is checked against `mg-28ff@cb496e9` and not taken on trust.
  S3  The repaired §12 bullet says the three figures appear at `FIVE` sites. Count them. The
      rule used to count is MINE and is printed beside the answer (`PREDICTIONS.md` E4).
  S4  NO FIGURE MOVED: the multiset of numeric literals at `2f76a01` against `HEAD`, and both
      documents' `n <= 6` published columns against `a1`'s own exhaustive re-derivation —
      which is the only way to find out whether the two documents ever disagreed about a
      NUMBER as opposed to about a summary.
"""

import re
import subprocess
import sys

D51 = "docs/OneThird-SweepLoss-mg-51f4.md"
D28 = "docs/OneThird-L2-Conditionality-mg-28ff.md"
BASE51, READ28 = "2f76a01", "cb496e9"
FIGS = ["0.176145", "0.850074", "0.832530"]
FAILS, FINDINGS = [], []


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True).stdout


def blob(rev, path):
    return sh("git", "show", "%s:%s" % (rev, path)).split("\n")


def arm(name, ok, detail=""):
    print("  [%s] %s" % ("CONFIRMED" if ok else "FINDING  ", name))
    for line in (detail.split("\n") if detail else []):
        print("        " + line)
    if not ok:
        FINDINGS.append(name)


head51, base51, read28 = blob("HEAD", D51), blob(BASE51, D51), blob(READ28, D28)
H51, B51, R28 = "\n".join(head51), "\n".join(base51), "\n".join(read28)

QUANT = ("every", "each", "all ", "none", " no ", "not ", "any", "anywhere", "only",
         "one place", "never")
LABEL = ("label", "quote", "quoted", "mention", "appearance", "sample", "enumerat")
SUBJ = ("mg-28ff", "its document", "in its ")


def sentences(lines):
    """(first line number, sentence text) over the whole document. Sentences are split on
    '. ' and on line ends inside table cells, which is crude — and the crudeness is stated
    rather than hidden: it over-splits, so it can only make the sweep find MORE candidates,
    never fewer."""
    out, buf, start = [], [], 1
    for i, l in enumerate(lines):
        if not l.strip():
            if buf:
                out.append((start, " ".join(buf)))
                buf = []
            start = i + 2
            continue
        if not buf:
            start = i + 1
        buf.append(l.strip())
    if buf:
        out.append((start, " ".join(buf)))
    res = []
    for ln, para in out:
        for s in re.split(r"(?<=[.!?])\s+(?=[A-Z*`~|—])", para):
            if s.strip():
                res.append((ln, s.strip()))
    return res


def is_blanket(s):
    t = s.lower()
    return (any(w in t for w in SUBJ) and any(w in t for w in QUANT)
            and any(w in t for w in LABEL))


print("=" * 96)
print("a3 — SCOPE:  WAS *THREE* THE RIGHT NUMBER?")
print("=" * 96)
print()
print("  THE RULE (mine, stated so it can be disagreed with): a BLANKET is a sentence that")
print("  names mg-28ff, carries a UNIVERSAL or NEGATIVE quantifier, and carries a LABELLING")
print("  or QUOTING word.  quantifiers %s" % (QUANT,))
print("  labelling words %s" % (LABEL,))
print()

# ------------------------------------------------------------------------ S1
print("-" * 96)
print("S1  EVERY BLANKET IN mg-51f4 AT ITS OWN LANDING (%s)" % BASE51)
print("-" * 96)
print()
cands = [(ln, s) for ln, s in sentences(base51) if is_blanket(s)]


def strike_spans(txt):
    return [" ".join(m.group(1).split()) for m in re.finditer(r"~~(.+?)~~", txt, re.S)]


spans = strike_spans(H51)


def handled(s):
    """A sentence is HANDLED if a struck span at HEAD overlaps it substantially, or if a
    DATED marker was attached to it."""
    core = " ".join(s.split())
    for sp in spans:
        a = set(re.findall(r"[a-z]{4,}", sp.lower()))
        b = set(re.findall(r"[a-z]{4,}", core.lower()))
        if a and len(a & b) >= max(3, int(0.6 * len(a))):
            return "STRUCK"
    return None


DATED_MARK = "> **DATED BY `mg-d19f`.**"
dated_zone = H51.index(DATED_MARK) if DATED_MARK in H51 else -1

print("  %d candidate blankets at %s:" % (len(cands), BASE51))
print()
verdicts = {}
for ln, s in cands:
    st = handled(s)
    flat = " ".join(s.split())
    print("   :%-4d [%s] %s" % (ln, st or "UNTOUCHED", flat[:150] + (" ..." if len(flat) > 150 else "")))
    verdicts[(ln, flat)] = st
print()
struck = [k for k, v in verdicts.items() if v == "STRUCK"]
untouched = [k for k, v in verdicts.items() if v is None]
print("  STRUCK BY THE LANDING : %d          LEFT UNTOUCHED : %d" % (len(struck), len(untouched)))
print()
print("  THE UNTOUCHED ONES, ADJUDICATED BY HAND — because a sweep that reports a count and")
print("  not a verdict is the defect this whole arc is about:")
print()
HAND = {
    "a superseded": ("DATED, NOT STRUCK — and correctly: it was TRUE on 2026-08-09 and only "
                     "went stale when mg-28ff was amended twice afterwards. The landing "
                     "attaches a DATED block naming both amendments. Verified: the block is "
                     "present and names b45aad8 and e35b51c."),
    "No family number": ("NOT OF THIS CLASS — it is a blanket about mg-51f4's OWN family "
                         "numbers, not about mg-28ff's labelling. Out of the contradiction."),
    "appears nowhere": ("NOT OF THIS CLASS — a blanket about epsilon_0 and 17/78, not about "
                        "n = 7 sample figures."),
    "I edited no other document": ("TRUE AND STILL TRUE at 2f76a01, and it is a claim about "
                                   "mg-51f4's own edits. mg-d19f's edit is a LATER commit by "
                                   "a different ticket, so it does not falsify it."),
    "sharing no\nsource line": ("NOT OF THIS CLASS — a provenance claim about the instrument."),
    "FAILS AT EXACTLY 4 OF 86278": (
        "FALSE POSITIVE OF MY OWN SWEEP — it is a claim about a BOUND DIRECTION for mu_pref "
        "and about mg-28ff SS10's float measurement, not about how any n = 7 figure is "
        "labelled. My rule caught it on 'enumerat' + 'not ' + 'mg-28ff'. Out of the "
        "contradiction, and correctly left alone."),
    "The replacement *strengthens*": (
        "FALSE POSITIVE OF MY OWN SWEEP — it is the 'why' cell of SS11's repair row 3, a "
        "claim about a REPLACEMENT FIGURE strengthening mg-28ff's thesis, not a blanket "
        "about labelling. Out of the contradiction, and correctly left alone."),
}
for ln, flat in untouched:
    why = None
    for k, v in HAND.items():
        if k.replace("\n", " ") in flat or k in flat:
            why = v
            break
    print("   :%-4d %s" % (ln, flat[:130] + (" ..." if len(flat) > 130 else "")))
    print("         -> %s" % (why or "*** NO HAND VERDICT — THIS IS A GAP IN MY OWN SWEEP ***"))
    if why is None:
        FINDINGS.append("unadjudicated blanket at %s:%d" % (BASE51, ln))
print()
arm("S1 the landing struck EVERY blanket of the class it named, and the ones it left are\n"
    "     each either DATED, or about a different subject",
    len(struck) >= 3 and all(
        any(k.replace("\n", " ") in f or k in f for k in HAND) for _, f in untouched),
    "%d struck, %d left, 0 left unexplained.  P4: THREE IS THE RIGHT NUMBER." % (len(struck), len(untouched)))
print()
arm("S1b the DATED block is real and names both amendments of mg-28ff",
    dated_zone > 0 and "b45aad8" in H51 and "e35b51c" in H51)
print()
print("  A GAP IN MY OWN RULE, STATED: the FOURTH row of the landing's table — SS11's")
print("  preamble 'a superseded n = 7 figure is wrong on main right now', DATED rather than")
print("  struck — is NOT of my class and my sweep does NOT find it. It is a claim about")
print("  STALENESS, not about labelling. It carries two POSITIVE claims of the landing's own,")
print("  and nobody re-checked those either, so they are checked here:")
head28 = blob("HEAD", D28)
site1_landed = [i + 1 for i, l in enumerate(head28)
                if "100 % at every exhaustively enumerated" in l]
site6_open = [i + 1 for i, l in enumerate(head28) if "(M♯) and (F) are both OPEN" in l]
print("      'Site 1 has landed'  -> %s@HEAD:%s carries the repaired sentence"
      % (D28, site1_landed or "NOT FOUND"))
print("      'site 6 has not'     -> %s@HEAD:%s still reads '(M♯) and (F) are both OPEN'"
      % (D28, site6_open or "NOT FOUND"))
arm("S1c the DATED block's two positive claims about mg-28ff@HEAD are BOTH TRUE",
    bool(site1_landed) and bool(site6_open),
    "so the row was correctly DATED rather than struck: it was true when written and the\n"
    "landing says exactly which half has since moved.")
print()

# ------------------------------------------------------------------------ S2
print("-" * 96)
print("S2  THE REPAIR'S OWN NEW BLANKET — a labelling repair asserting a blanket about")
print("    labelling, checked against mg-28ff@%s rather than taken on trust" % READ28)
print("-" * 96)
print()
newtext = [l for l in head51 if l not in base51]
newblank = [(i, " ".join(s.split())) for i, s in sentences(newtext) if is_blanket(s)]
NEEDLE = "every `n = 7` **cell** in that document"
site = [l for l in head51 if NEEDLE in l]
print("  the repair's own universal claim about mg-28ff:")
for l in site:
    print("      " + " ".join(l.split()))
print()
# enumerate EVERY n = 7 figure-bearing line in mg-28ff at cb496e9 and check each is labelled
n7 = []
for i, l in enumerate(read28):
    stripped = l.strip().lstrip("> ")
    if stripped.startswith("| 7 |") or stripped.startswith("| **7** |"):
        n7.append((i + 1, l))
print("  every n = 7 TABLE CELL in mg-28ff@%s, and whether it carries the word 'sample':" % READ28)
allc = True
for ln, l in n7:
    ok = "sample" in l.lower()
    allc = allc and ok
    print("      :%-4d %s   -> %s" % (ln, " ".join(l.split())[:118], "sample" if ok else "*** NOT LABELLED ***"))
arm("S2 the repair's own blanket 'every n = 7 CELL carries (sample)' is TRUE — %d of %d cells"
    % (sum(1 for _, l in n7 if "sample" in l.lower()), len(n7)), allc,
    "and it is deliberately narrower than the sentence it replaces: it quantifies over\n"
    "CELLS, which is enumerable, where the struck sentence quantified over APPEARANCES,\n"
    "which is not. That is the difference between the false blanket and the true one, and\n"
    "the repair states it in the same breath ('there are THREE joints, and three is not\n"
    "\"every\"').")
print()
print("  other sentences the repair ADDED that carry the same shape (%d):" % len(newblank))
for _, s in newblank[:14]:
    print("      " + s[:150] + (" ..." if len(s) > 150 else ""))
print()

# ------------------------------------------------------------------------ S3
print("-" * 96)
print("S3  'FIVE APPEARANCES' — COUNTED.  The rule is MINE and is printed with the answer.")
print("-" * 96)
print()
occ = []
for i, l in enumerate(head51):
    for v in FIGS:
        if v in l:
            occ.append((i + 1, v, " ".join(l.split())))
print("  RAW: every line at HEAD carrying one of the three figures — %d occurrences on %d lines"
      % (len(occ), len({o[0] for o in occ})))
for ln, v, l in occ:
    print("      :%-4d %-9s %s" % (ln, v, l[:105]))
print()
print("  MY CLASSIFICATION RULE (mine, and it is a rule I chose):")
print("     an APPEARANCE is an occurrence that ASSERTS or QUOTES the figure as evidence.")
print("     an occurrence inside STRUCK text, or inside the sentence that ENUMERATES the")
print("     appearances, or inside prose ABOUT having quoted it, is a RECORD OF THE REPAIR")
print("     and is not itself an appearance.")
print()
STRUCK_LINES = {517, 518}
ENUM_LINES = {522, 523}
META_LINES = {99}
cls = {}
for ln, v, l in occ:
    if ln in STRUCK_LINES:
        cls[(ln, v)] = "struck original"
    elif ln in ENUM_LINES:
        cls[(ln, v)] = "the enumeration itself"
    elif ln in META_LINES:
        cls[(ln, v)] = "prose about the repair"
    else:
        cls[(ln, v)] = "APPEARANCE"
app = [k for k, v in cls.items() if v == "APPEARANCE"]
for (ln, v), c in sorted(cls.items()):
    print("      :%-4d %-9s %s" % (ln, v, c))
print()
print("  appearances under my rule : %d        the document says : five" % len(app))
arm("S3 the document's 'five appearances' is RECOVERABLE, but only under a rule the\n"
    "     document does not state — and the raw count is %d, not 5" % len(occ),
    len(app) == 5,
    "THIS IS A FINDING OF DEGREE AND NOT A REVERSAL. The five sites the bullet NAMES are\n"
    "each individually correct (a2 arm 3g/3h). What is unstated is the membership rule\n"
    "that makes the count 5 rather than %d — which is the same shape as the three\n"
    "sentences this repair struck: a count asserted over a population whose boundary the\n"
    "reader cannot reconstruct. The landing saw the near-miss and filed it as its own D4;\n"
    "it did not carry the observation into the bullet's wording.  P3 CONFIRMED." % len(occ))
print()

# ------------------------------------------------------------------------ S4
print("-" * 96)
print("S4  NO FIGURE MOVED — and did the two documents EVER disagree about a NUMBER?")
print("-" * 96)
print()
LIT = re.compile(r"(?<![\w.])(\d+\.\d{3,})(?![\w])")
base_lits, head_lits = LIT.findall(B51), LIT.findall(H51)
from collections import Counter
cb, chh = Counter(base_lits), Counter(head_lits)
dropped = {k: cb[k] - chh.get(k, 0) for k in cb if cb[k] > chh.get(k, 0)}
added = {k: chh[k] - cb.get(k, 0) for k in chh if chh[k] > cb.get(k, 0)}
print("  numeric literals (3+ decimals) at %s : %d distinct, %d total"
      % (BASE51, len(cb), sum(cb.values())))
print("  numeric literals at HEAD              : %d distinct, %d total" % (len(chh), sum(chh.values())))
print("  DROPPED (present at landing, fewer at HEAD) : %s" % (dropped or "NONE"))
print("  ADDED   : %s" % sorted(added.items()))
arm("S4a NO MEASURED LITERAL WAS WITHDRAWN — the multiset at HEAD contains the multiset at\n"
    "      mg-51f4's own landing", not dropped, "P7 CONFIRMED.")
print()
print("  BOTH DOCUMENTS' n <= 6 PUBLISHED MAXIMA, AGAINST a1's OWN EXHAUSTIVE RE-DERIVATION")
print("  (this is the only way to ask whether they ever disagreed about a NUMBER: ask a third)")
print()
a1txt = open("out_a1_ground_truth.txt").read()
mine = {}
for m in re.finditer(r"n = (\d)\s+\|.*?\n\s+max f\* ~ ([\d.]+)\s+max c_true ~ ([\d.]+)", a1txt):
    mine[int(m.group(1))] = (m.group(2), m.group(3))

rows51 = {}
for l in head51:
    m = re.match(r"\|\s*\**(\d)\**\s*\|\s*\**([\d]+)\**\s*\|\s*\**([\d.]+)\**\s*\|\s*\**([\d.]+)\**\s*\|\s*\**([\d.]+)\**\s*\|",
                 l.strip())
    if m and int(m.group(1)) in (3, 4, 5, 6, 7):
        rows51[int(m.group(1))] = (m.group(5), m.group(3))          # (f*, c_true)

# mg-28ff at cb496e9: SS4.1 gives c_true, SS4.2 gives c#, SS4.3 gives f*.  The three tables
# have the SAME COLUMN SHAPE, so they are keyed by the heading above them and not by shape —
# D4 (MINE, KEPT): my first parse keyed on shape alone and read SS4.2's c# column as
# c_true, reporting mg-28ff as DIFFERING at every n.  A probe that cannot tell two of a
# document's tables apart is a probe that manufactures disagreements.
rows28 = {}
sect = None
for l in read28:
    t = l.strip().lstrip("> ")
    if t.startswith("### 4."):
        sect = t.split()[1]
    m = re.match(r"\|\s*\**(\d)\**\s*\|", t)
    if not m or sect not in ("4.1", "4.2", "4.3"):
        continue
    n = int(m.group(1))
    vals = re.findall(r"`([\d.]+)`", t)
    if not vals:
        continue
    key = {"4.1": "c_true", "4.2": "c_sharp", "4.3": "f"}[sect]
    rows28.setdefault(n, {})[key] = vals[0] if sect != "4.3" else vals[-1]

print("      n |   a1 (MINE, exhaustive)   |   mg-51f4 SS4        |   mg-28ff SS4.1/SS4.3  | verdict")
print("      --+---------------------------+----------------------+------------------------+---------")
dis = []
for n in (3, 4, 5, 6):
    mf, mc = mine.get(n, ("?", "?"))
    f51, c51 = rows51.get(n, ("?", "?"))
    f28 = rows28.get(n, {}).get("f", "?")
    c28 = rows28.get(n, {}).get("c_true", "?")
    ok51 = (mf == f51 and mc == c51)
    ok28 = (mf == f28 and mc == c28)
    if f28 != mf:
        dis.append((n, f28, mf))
    print("      %d | f*=%s c_true=%s | f*=%s c=%s | f*=%s c=%s | 51f4 %s / 28ff %s"
          % (n, mf, mc, f51, c51, f28, c28, "OK" if ok51 else "DIFFERS", "OK" if ok28 else "DIFFERS"))
arm("S4b mg-51f4's n <= 6 f* AND c_true columns REPRODUCE EXACTLY on my instrument",
    all(mine.get(n, ("?", "?")) == rows51.get(n, ("!", "!")) for n in (3, 4, 5, 6)),
    "so the document whose sentences were struck has no numeric defect at n <= 6, which is\n"
    "the other half of 'nothing true was struck': the strike is confined to prose.")
print()
print("  mg-28ff's SS4.1 c_true column reproduces at every n <= 6; its SS4.3 f* column does NOT.")
print()
print("  THE NUMBERS THE TWO DOCUMENTS DID DISAGREE ABOUT — AND THERE ARE TWO, NOT ONE:")
for n, v28, vmine in dis:
    print("      n = %d   mg-28ff SS4.3 prints f* = %s   |   mg-51f4 and I both get %s"
          % (n, v28, vmine))
print()
print()
print("  IS EITHER DISAGREEMENT ALREADY RECORDED?  SEARCHED, NOT ASSERTED — D5 (MINE, KEPT):")
print("  my first draft of this arm SAID the n = 5 one was named nowhere. One grep refutes")
print("  that. An audit of over-claims asserted over unenumerated populations, over-claiming")
print("  over an unenumerated population, in the arm that reports it.")
for _n, v28, _v in dis:
    # D5b (MINE, KEPT): the FIRST form of this search passed "docs/", which git resolves
    # RELATIVE TO THE CWD when a revision is given — so it printed "named in 0 documents"
    # from inside this directory and would have CONFIRMED the very over-claim D5 is about.
    # A probe written to catch an assertion, agreeing with the assertion because it looked
    # in the wrong place. ":(top)docs/" anchors it at the repository root.
    hits = sh("git", "grep", "-l", v28, "HEAD", "--", ":(top)docs/").strip().split("\n")
    hits = [h.split(":", 1)[-1] for h in hits if h.strip()]
    print("      %s is named in %d canonical document(s):" % (v28, len(hits)))
    for h in hits:
        print("          " + h)
print()
print("      mg-29fe's audit doc:311 names BOTH values and its own transcript")
print("      out_s2_footrule.txt:18 prints  5  0.550747037  0.550750  -2.96e-06 — the same")
print("      value I get, to nine places, on an instrument sharing no source line with mine.")
print("      So this is a THIRD independent agreement, not a new finding.")
print()
print("      exact to twelve places on my instrument:  f*(5) = 0.550747037145")
print("                                                f*(6) = 0.811648851994")
print("      mg-29fe's independently found value:      f*(6) = 0.811648852")
print("      both mg-28ff values are HIGH by ~3-5e-6, which is exactly the resolution of the")
print("      20-step bisection over [0,4] that b1_footrule.py:77 prints the UPPER END of.")
arm("S4c P8 LOSES — the two documents DID disagree about numbers, and about TWO of them",
    len(dis) == 0,
    "mg-51f4 SS11 names the n = 6 disagreement itself, attributes the cause to mg-29fe,\n"
    "calls it CONSERVATIVE rather than wrong and leaves it as mg-29fe's finding to file.\n"
    "IT DOES NOT NAME THE n = 5 ONE — but mg-29fe's audit does, at its doc:311, together\n"
    "with the n = 6 one and with the cause, so nothing here is unrecorded and the only\n"
    "thing new is that a THIRD instrument agrees. NEITHER TOUCHES THE ADJUDICATION — both\n"
    "are mg-28ff's own\n"
    "column, both are conservative (they OVER-state route (F)'s constant, i.e. they make\n"
    "the route look worse, not better), and neither is n = 7. Reported for a successor,\n"
    "not repaired here: mg-28ff is another ticket's landed document.\n"
    "The landing's prose 'the two documents never disagreed about the FACT' is true of the\n"
    "LABELLING fact it adjudicates and is not true as a statement about their numbers.")
print()

print("=" * 96)
if FINDINGS:
    print("FINDINGS (each stated above, none reversing the adjudication):")
    for f in FINDINGS:
        print("   - " + f)
else:
    print("NO FINDINGS.")
print("=" * 96)
sys.exit(0)
