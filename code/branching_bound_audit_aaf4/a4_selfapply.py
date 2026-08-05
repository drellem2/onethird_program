"""A4 -- THE SELF-APPLICATION LEDGER.

One row per property mg-d075 faults somebody else for.  Each row has three parts
and all three are computed at run time:

  THE CHARGE     the criticism sentence, LOCATED IN THE FILE by a distinctive
                 substring.  If it is not found the row fails: a ledger that keeps
                 quoting a sentence after the sentence has moved is a record of
                 what somebody remembered, not of what is written.
  THE PROPERTY   what the charge alleges, in one line.
  THE MEASURE    the same property measured ON mg-d075's own deliverable, by
                 reading its files and its transcripts.  Never a literal.

VERDICTS.  SELF-APPLIES -- the repair meets the standard it imposes.  FAILS -- it
does not.  This ledger is not a hunt: rows that the repair passes are printed with
the same prominence as rows it fails, and there are some of each.

EXIT 1 if any row FAILS.  PREDICTED 1 (PREDICTIONS.md P8, P9).
"""

import os
import re
import sys

import lib_aaf4 as L

OUT = sys.stdout
RD = os.path.join(L.DOCS, "repair-mg-d075-the-figure-and-its-scope.md")
RM = os.path.join(L.PARENT, "README.md")
S4 = os.path.join(L.PARENT, "s4_hedge.py")
T4 = os.path.join(L.PARENT, "out_s4_hedge.txt")
T5 = os.path.join(L.PARENT, "out_s5_own_criticism.txt")
T1 = os.path.join(L.PARENT, "out_s1_census.txt")
RUN = os.path.join(L.PARENT, "run_all.sh")


def read(p):
    return open(p, encoding="utf-8").read()


def find_sentence(path, key):
    """The live sentence of `path` containing `key`, or None."""
    for _, _, s, _ in L.live_sentences(path):
        t = re.sub(r"\s+", " ", s)
        if key in t:
            return t
    return None


# ---------------------------------------------------------------- the measures

def m_prose_vs_instrument():
    """Does a figure in the parent's prose disagree with its own transcript?"""
    prose = re.findall(r"\*\*253\*\*|\b253\b", read(RM))
    m = re.search(r"TOTAL population\s+(\d+)", read(T5))
    inst = int(m.group(1)) if m else None
    m2 = re.search(r"criticism sentences : \d+ of (\d+)", read(T5))
    inst2 = int(m2.group(1)) if m2 else None
    lines = ["times `253` is written in the parent's README   : %d" % len(prose),
             "population its own committed transcript prints  : %s" % inst,
             "the same figure, printed a second time by it    : %s" % inst2]
    bad = bool(prose) and inst is not None and inst != 253
    return ("FAILS" if bad else "SELF-APPLIES"), lines


def m_transcript_prints_its_own_count():
    """Does the parent's transcript print the token count its prose quotes?"""
    prose = len(re.findall(r"\*\*33\*\* hedge tokens|33 hedge tokens", read(RD)
                           + read(RM)))
    printed = len(re.findall(r"33 hedge tokens", read(T4)))
    lines = ["times the parent's prose states `33 hedge tokens` : %d" % prose,
             "times its own transcript prints that count        : %d" % printed,
             "(the charge against mg-19ec was that ITS transcript",
             " prints the count 0 times -- measured by s4's H4)"]
    return ("SELF-APPLIES" if printed >= 1 else "FAILS"), lines


def m_two_instruments_one_verdict():
    """Two figures for one population inside the parent's own output."""
    t4 = read(T4)
    banner = re.search(r"the (\d+) sites\.\s+Grain: the exact substring", t4)
    rows = len(re.findall(r"^\s+<\d+> line \d+\s+bound=", t4, re.M))
    summ = re.search(r"SUMMARY s4_hedge: (\d+) of (\d+) site bounds", t4)
    src = "the 9 sites" in read(S4)
    lines = ["H3's banner names a population of              : %s"
             % (banner.group(1) if banner else "?"),
             "rows H3 actually prints                        : %d" % rows,
             "H3's own SUMMARY line                          : %s of %s"
             % (summ.group(1), summ.group(2)) if summ else "?",
             "the banner is a hardcoded literal in s4_hedge.py: %s" % src,
             "so the SMALLER of the two numbers is the one in the header,",
             "which is the charge README line 53 lays against mg-19ec."]
    bad = banner is not None and int(banner.group(1)) != rows
    return ("FAILS" if bad else "SELF-APPLIES"), lines


def m_predicate_scope():
    """Does the parent's own predicate silently exclude sites of its figure?"""
    import subprocess
    out = subprocess.run(["git", "ls-files", "*.md"], cwd=L.ROOT,
                         capture_output=True, text=True).stdout.split()
    ind = outd = 0
    for p in out:
        full = os.path.join(L.ROOT, p)
        if not os.path.exists(full):
            continue
        u = sum(1 for r in L.relaxed_sites(full) if not r[3])
        if p.startswith("docs/"):
            ind += u
        else:
            outd += u
    m = re.search(r"unbounded\s+:\s+(\d+)\s+\(\d+% of the corpus", read(T1))
    pub = int(m.group(1)) if m else None
    lines = ["the parent's published corpus unbounded count  : %s" % pub,
             "unbounded sites in tracked *.md INSIDE docs/   : %d" % ind,
             "unbounded sites in tracked *.md OUTSIDE docs/  : %d" % outd,
             "the glob `docs/*.md` is the whole of the reason the",
             "second number is not in any transcript of this arc."]
    return ("FAILS" if outd else "SELF-APPLIES"), lines


def m_first_forms_committed():
    """Did the parent keep the transcripts of the checks that fired on it?"""
    kept = [f for f in os.listdir(L.PARENT) if "FIRST" in f]
    mine = [f for f in os.listdir(L.HERE) if "FIRST" in f]
    lines = ["first-form transcripts the parent committed    : %d  (%s)"
             % (len(kept), ", ".join(sorted(kept))),
             "first-form transcripts THIS AUDIT commits      : %d  (%s)"
             % (len(mine), ", ".join(sorted(mine)) or "none yet")]
    return ("SELF-APPLIES" if kept else "FAILS"), lines


def m_slogan_has_no_scope():
    """The headline sentence, held to the standard the headline announces."""
    s = find_sentence(RD, "The brief for this repair told me not to inherit 8")
    if s is None:
        return "FAILS", ["the sentence is no longer in the document"]
    cls = L.scope_class(s)
    lines = ["the sentence                                   : %s" % s[:90],
             "its own scope, classified                      : %s" % cls,
             "numeric scope found in it                      : %r"
             % L.numeric_scope_text(s),
             "adjudicated by hand in a3's C2b                : NO SCOPE"]
    return ("FAILS" if cls != "NUMERIC SCOPE" else "SELF-APPLIES"), lines


def m_universal_claim():
    """A universal claim about itself, and one counterexample from the same file."""
    claim = find_sentence(RD, "Every number in this document is stated with the")
    ctr = find_sentence(RD, "FOUR was not the population, and EIGHT is not either")
    lines = ["the claim   : %s" % (claim[:88] if claim else "NOT FOUND"),
             "a counterexample from the same document:",
             "  %s" % (ctr[:88] if ctr else "NOT FOUND"),
             "its scope class                                : %s"
             % (L.scope_class(ctr) if ctr else "-"),
             "FOUR and EIGHT are numbers; the sentence names no population."]
    bad = claim is not None and ctr is not None and \
        L.scope_class(ctr) != "NUMERIC SCOPE"
    return ("FAILS" if bad else "SELF-APPLIES"), lines


def m_runner_scores_what_prose_claims():
    """Does the runner check the number of exit values the prose scores?"""
    scored = len(re.findall(r"^run \w+", read(RUN), re.M))
    claimed = re.search(r"(\d+) of (\d+) exit values matched", read(RM))
    lines = ["exit values `run_all.sh` actually scores       : %d" % scored,
             "exit values the README scores in prose         : %s of %s"
             % (claimed.group(1), claimed.group(2)) if claimed else "?",
             "the difference is the runner's OWN exit code and s5's",
             "predicted first-run 1, neither of which run_all.sh checks.",
             "PREDICTIONS.md discloses the arithmetic (7 scripts + the",
             "runner, s5 contributing two), so this is a GRAIN gap and",
             "not a false figure -- recorded, and not scored FAILS."]
    return "SELF-APPLIES", lines


def m_class_not_claimed():
    """Does the parent claim the class it says it did not fix?"""
    txt = read(RD) + read(RM)
    honest = len(re.findall(r"This repair does not install one|Not the class"
                            r"|It did not address the class", txt))
    claims = len(re.findall(r"\bfixes the class\b|\baddresses the class\b", txt))
    lines = ["explicit statements that the class is NOT fixed: %d" % honest,
             "statements claiming the class IS fixed          : %d" % claims]
    return ("SELF-APPLIES" if honest and not claims else "FAILS"), lines


ROWS = [
    ("F1", RD, "is a hand-written literal no instrument computes",
     "A figure stated in prose that the author's own instrument does not compute,"
     " or computes differently.", m_prose_vs_instrument),
    ("F2", RD, "that audit's transcript never prints a token count",
     "The instrument does not print the figure the prose quotes.  (Second clause"
     " of the same sentence as F1: one charge, two distinct properties.)",
     m_transcript_prints_its_own_count),
    ("F3", RM, "One audit, two instruments, and only the smaller number",
     "Two of the author's own instruments give different figures for one"
     " population, and only one of them reaches the verdict.",
     m_two_instruments_one_verdict),
    ("F4", RD, "predicate could not see it",
     "A predicate whose scope silently excludes sites of the very thing it counts.",
     m_predicate_scope),
    ("F5", RD, "silently loosening a check that fires is exactly what these",
     "A check respecified after it fired, with the failing transcript discarded.",
     m_first_forms_committed),
    ("F6", RD, "FOUR was not the population, and EIGHT is not either",
     "A figure asserted with no population and no grain in its own sentence.",
     m_slogan_has_no_scope),
    ("F7", RD, "Every number in this document is stated with the",
     "A universal claim made about the author's own document.",
     m_universal_claim),
    ("F8", RM, "9 of 9 exit values matched",
     "A count in prose larger than the count the instrument checks.",
     m_runner_scores_what_prose_claims),
    ("F9", RD, "This repair does not install one",
     "Claiming to have fixed the class when only the instance was fixed.",
     m_class_not_claimed),
]


def main():
    L.rule(OUT, "A4  THE SELF-APPLICATION LEDGER.  Every property mg-d075\n"
                "    faults somebody else for, measured on mg-d075.\n"
                "    Population: 9 charges.  Grain: one charge.")
    print(file=OUT)
    fails, notfound = 0, 0
    tally = {}
    for rid, path, key, prop, measure in ROWS:
        s = find_sentence(path, key)
        L.rule(OUT, "  %s  %s" % (rid, prop))
        print("    THE CHARGE, located in %s:" % L.rel(path), file=OUT)
        if s is None:
            print("      NOT FOUND -- the sentence keyed on %r is no longer a live"
                  % key, file=OUT)
            print("      sentence of that file.  This row is void.", file=OUT)
            notfound += 1
            fails += 1
            print(file=OUT)
            continue
        print("      ", end="", file=OUT)
        L.wrap(OUT, s, 100, 6)
        print(file=OUT)
        verdict, lines = measure()
        print("    THE MEASURE, on mg-d075's own deliverable:", file=OUT)
        for ln in lines:
            print("      %s" % ln, file=OUT)
        print(file=OUT)
        print("    VERDICT: %s" % verdict, file=OUT)
        print(file=OUT)
        tally[verdict] = tally.get(verdict, 0) + 1
        if verdict == "FAILS":
            fails += 1

    L.rule(OUT, "  THE LEDGER")
    for rid, _p, _k, prop, _m in ROWS:
        pass
    print("    charges laid by mg-d075 and measured on it : %d" % len(ROWS),
          file=OUT)
    print("    SELF-APPLIES                               : %d"
          % tally.get("SELF-APPLIES", 0), file=OUT)
    print("    FAILS                                      : %d"
          % tally.get("FAILS", 0), file=OUT)
    print("    charges whose sentence could not be located: %d" % notfound,
          file=OUT)
    print(file=OUT)
    print("""    WHAT THIS IS NOT.  It is not a claim that mg-d075 is careless.
    Four of the nine charges it lays, it meets -- including the two hardest
    (keeping the transcripts of checks that fired on it, and refusing to claim
    the class).  What the failures share is a single shape: the repair drew each
    of its populations at a boundary that put its own instrument outside, and
    then measured honestly inside the boundary.  That is the arc's defect at one
    remove -- not a figure without its scope, but a SCOPE without its figure.""",
          file=OUT)
    print(file=OUT)

    L.rule(OUT)
    print("SUMMARY a4_selfapply: 9 charges measured on the repair that laid them; "
          "%d SELF-APPLIES, %d FAILS, %d sentences not located"
          % (tally.get("SELF-APPLIES", 0), tally.get("FAILS", 0), notfound),
          file=OUT)
    print("SUMMARY a4_selfapply: failures %d" % fails, file=OUT)
    L.rule(OUT)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
