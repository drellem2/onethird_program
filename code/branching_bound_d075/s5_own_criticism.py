"""S5 -- THE SENTENCES IN WHICH I FAULT SOMEONE ELSE'S SCOPE, CHECKED FOR MY OWN.

WHY THIS SCRIPT EXISTS, in the words of the brief that commissioned this repair:

  "The clause that faults Young-Fibonacci for naming no class itself states the
   YOUNG classification unbounded.  A sentence criticising another for unbounded
   naming, unbounded.  That is the author inside their own blind spot at the
   finest possible grain -- the defect was in the writer's hands as they wrote the
   criticism of it.  Whoever repairs this should expect to do the same thing
   somewhere in the repair, and should look for it deliberately."

So this is the deliberate look.  It is pointed at MY OWN deliverable and nothing
else.  PREDICTIONS.md P9 says in advance that it exits 1 on its first run.

  POPULATION.  Live sentences of every document this repair AUTHORS:
    code/branching_bound_d075/README.md
    docs/repair-mg-d075-the-figure-and-its-scope.md
    plus the sentences this repair added to the living document (computed, not
    listed -- the same NEW-sentence set s4 computes).
  Liveness and sentence grain are lib_d075's, i.e. the parent's.

  A CRITICISM SENTENCE is a live sentence of mine that (a) carries a FAULT marker
  -- it says something misses, drops, is unbounded, disagrees, is a defect -- and
  (b) names a TARGET that is not this work item: another ticket id, "the parent",
  "the predecessor", "the census", "the instrument".  Both conjuncts are required,
  because a sentence that merely contains the word "unbounded" is doing arithmetic,
  not criticism.

  IT CARRIES ITS OWN SCOPE if the SAME sentence states the population or the grain
  of what it asserts: a numeric scope, a count with its denominator, a named file
  or predicate, or the words population / grain / live sentences / sites.  A
  neighbouring sentence does not rescue it -- that is precisely the standard this
  repair applied to the document, and applying a weaker one to myself would be the
  defect a second time.

EXIT 1 if any criticism sentence of mine lacks its own scope.  PREDICTED: 1 on the
first run, 0 once repaired.  The first run's transcript is committed either way.
"""

import os
import re
import subprocess
import sys

import lib_d075 as L

OUT = sys.stdout
ITEM = "mg-d075"
RELPATH = "docs/OneThird-Branching-Graphs-Where-This-Lives.md"
MINE = [
    os.path.join(L.HERE, "README.md"),
    os.path.join(L.DOCS, "repair-mg-d075-the-figure-and-its-scope.md"),
]

FAULT = re.compile(
    r"\bmisses\b|\bmissed\b|cannot see|\bdrops\b|\bdropped\b|\bunbounded\b"
    r"|\bdisagree|\bdefect\b|\bfails\b|\bfailed\b|\bblind\b|under-collect"
    r"|over-collect|\bhollow\b|\btautolog|too narrow|too wide|\bwrong\b"
    r"|no instrument computes|\bnot the population\b|\bnever computes\b"
    r"|\bdoes not carry\b|\bno bound\b|\binvalid\b|\bartefact\b", re.I)
TARGET = re.compile(
    r"\bmg-(?!d075)[0-9a-f]{4}\b|the parent\b|the predecessor\b|the census\b"
    r"|the instrument\b|its own instrument|the published audit", re.I)
OWNSCOPE = re.compile(
    r"\bpopulation\b|\bgrain\b|live sentences?\b|\b\d+ of (?:the )?\d+\b"
    r"|\b\d+ sites?\b|\b\d+ sentences?\b|\b\d+ tokens?\b|\b\d+ occurrences?\b"
    r"|rank\s*\(?w?\)?\s*(?:≤|<=)\s*\d|to rank \d|`?n`?\s*(?:≤|<=)\s*\d"
    r"|code/[a-z0-9_]+|docs/[A-Za-z0-9_.\-]+|out_[a-z0-9_]+\.txt"
    r"|\b\d+ (?:files?|rows?|cells?|figures?|commits?|intervals?|phrasings?)\b"
    r"|STRICT|RELAXED|POP-\d|\b\d+ -> \d+\b|\b\d+/\d+\b", re.I)


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=L.ROOT, capture_output=True,
                          text=True).stdout


def added_sentences():
    """The sentences this repair added to the living document."""
    for row in git("log", "--format=%H\t%s", "--", RELPATH).strip().split("\n"):
        h, _, subj = row.partition("\t")
        if ITEM not in subj:
            break
    tmp = os.path.join(L.HERE, ".baseline_doc5.md")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(git("show", "%s:%s" % (h, RELPATH)))
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    old = {norm(s) for _, _, s, _ in L.live_sentences(tmp)}
    out = [(RELPATH, a, norm(s)) for a, _, s, _ in L.live_sentences(L.DOC)
           if norm(s) not in old]
    os.remove(tmp)
    return out


def main():
    L.rule(OUT, "S5  THE SENTENCES IN WHICH I FAULT SOMEONE ELSE'S SCOPE,\n"
                "    CHECKED FOR MY OWN.  Pointed at this repair and nothing else.")
    print(file=OUT)

    pop = []
    print("  THE POPULATION, NAMED", file=OUT)
    for path in MINE:
        if not os.path.exists(path):
            print("    %-58s ABSENT" % os.path.relpath(path, L.ROOT), file=OUT)
            continue
        ss = [(os.path.relpath(path, L.ROOT), a, re.sub(r"\s+", " ", s).strip())
              for a, _, s, _ in L.live_sentences(path)]
        pop += ss
        print("    %-58s %d live sentences"
              % (os.path.relpath(path, L.ROOT), len(ss)), file=OUT)
    add = added_sentences()
    pop += add
    print("    %-58s %d sentence(s) added by this repair"
          % (RELPATH, len(add)), file=OUT)
    print("    %-58s %d" % ("TOTAL population", len(pop)), file=OUT)
    print("    grain: one sentence", file=OUT)
    print(file=OUT)

    crit = [(f, l, s) for f, l, s in pop if FAULT.search(s) and TARGET.search(s)]
    L.rule(OUT, "  MY CRITICISM SENTENCES -- fault marker AND a target that is\n"
                "  not this work item.  Each checked for ITS OWN scope.")
    print("    criticism sentences : %d of %d in the population"
          % (len(crit), len(pop)), file=OUT)
    print(file=OUT)
    unbounded = []
    for i, (f, l, s) in enumerate(crit, 1):
        m = OWNSCOPE.search(s)
        ok = bool(m)
        print("    [%02d] %-42s line %-4d %s"
              % (i, os.path.basename(f)[:42], l,
                 "CARRIES ITS OWN SCOPE" if ok else "*** UNBOUNDED ***"), file=OUT)
        print("         fault : %s" % ",".join(
            sorted({x.lower() for x in FAULT.findall(s)}))[:90], file=OUT)
        print("         target: %s" % ",".join(
            sorted({x.lower() for x in TARGET.findall(s)}))[:90], file=OUT)
        if ok:
            print("         scope : %s" % m.group(0)[:80], file=OUT)
        else:
            unbounded.append((f, l, s))
        print("         %s" % s[:104], file=OUT)
        for j in range(104, len(s), 104):
            print("         %s" % s[j:j + 104], file=OUT)
        print(file=OUT)

    L.rule(OUT, "  VERDICT ON MYSELF")
    print("    criticism sentences carrying their own scope : %d of %d"
          % (len(crit) - len(unbounded), len(crit)), file=OUT)
    print("    criticism sentences UNBOUNDED                : %d of %d"
          % (len(unbounded), len(crit)), file=OUT)
    print(file=OUT)
    if unbounded:
        print("    THE DEFECT IS IN MY HANDS, at the grain the brief predicted:",
              file=OUT)
        for f, l, s in unbounded:
            print("      %s line %d" % (os.path.basename(f), l), file=OUT)
            print("        %s" % s[:100], file=OUT)
        print(file=OUT)
    else:
        print("    No criticism sentence of mine is unbounded at this grain.",
              file=OUT)
        print("    That is not proof of innocence -- it is one predicate over one",
              file=OUT)
        print("    population, and a defect outside the predicate is invisible to",
              file=OUT)
        print("    it.  mg-aaf4 is asked to pick a different one.", file=OUT)
        print(file=OUT)

    L.rule(OUT)
    print("SUMMARY s5_own_criticism: population %d live sentences of my own"
          % len(pop), file=OUT)
    print("SUMMARY s5_own_criticism: %d criticism sentence(s); %d unbounded"
          % (len(crit), len(unbounded)), file=OUT)
    L.rule(OUT)
    return 1 if unbounded else 0


if __name__ == "__main__":
    sys.exit(main())
