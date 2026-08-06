"""P3 -- WHICH PUBLISHED FIGURES INHERIT THE UNDERCOUNT.

"The 12 is one symptom; anything computed over the same glob carries it.  Enumerate
the consumers."  So this script does not argue that other figures are probably
affected.  It finds them, three ways, and prints each with its published value, the
value re-derived over the full population, and the delta.

  C1  THE CALL SITES.  Every place in tracked `.py` where the universe is built by
      listing `docs/` rather than by asking git.  Found by scanning source, with a
      CONTROL: the scan also reports the recursive and git-derived idioms, so a
      report of "only non-recursive idioms exist" is a finding and not a blind scan.

  C2  THE TRANSCRIPT FIGURES.  Every `SUMMARY` line of mg-d075's committed
      transcripts whose population is the corpus.  Published value vs re-derived.

  C3  THE PROSE FIGURES.  Population: live sentences of tracked `.md` that name the
      corpus universe (`corpus`, `docs/*.md`, `docs/`) AND carry a number.  Grain:
      one sentence.  A sentence INHERITS if the number it carries is one the glob
      produces.  The matched number is printed on every row so the classification
      can be argued with rather than trusted.

  C4  THE SECOND-ORDER CONSUMERS.  Files that quote an inheriting figure without
      computing it.  An undercount that has been quoted onward is harder to correct
      than one that has not, and the count of quoters is the size of that problem.

THE CLASSIFIER IS A CHOICE AND IT IS CONTROLLED.  C3 prints, beside the inheriting
sentences, the sentences of the SAME files that name the corpus and carry a number
that the glob does NOT produce.  A classifier that fired on everything would have an
empty control column.

EXIT 1 if any published figure inherits the undercount.  PREDICTED 1.
"""

import os
import re
import sys

import lib1d6c as U

OUT = sys.stdout

# The idioms, and what each one actually enumerates.
IDIOMS = [
    ("os.listdir(<docs>)", re.compile(r"os\.listdir\(\s*[A-Za-z_.]*DOCS?\b"),
     "working tree, ONE LEVEL, docs/ only"),
    ("glob('docs/*.md')", re.compile(r"glob[a-z.]*\(\s*['\"][^'\"]*docs/\*\.md"),
     "working tree, ONE LEVEL, docs/ only"),
    ("shell ls docs/*.md", re.compile(r"ls\s+-?\w*\s*docs/\*\.md"),
     "working tree, ONE LEVEL, docs/ only"),
    ("os.walk(<docs>)", re.compile(r"os\.walk\("), "working tree, RECURSIVE"),
    ("glob('**/*.md')", re.compile(r"\*\*/\*\.md"), "working tree, RECURSIVE"),
    ("git ls-files", re.compile(r"ls-files"), "the index, RECURSIVE"),
    ("git ls-tree -r", re.compile(r"ls-tree[^\n]*-r"), "a commit, RECURSIVE"),
]

MINE = "code/corpus_universe_1d6c/"

# A sentence that names the WIDER universe in its own words is CITING the glob's
# figure, not publishing it as the population.  This is a machine rule and it is
# coarse; every row it decides is printed, and the hand adjudication below overrides
# it per row WITH A REASON, both numbers published.
WIDE_MARK = re.compile(r"\btracked\b|ls-files|every markdown|outside (?:the )?"
                       r"[`']?docs/|wider universe", re.I)

# (path fragment, substring identifying the sentence, verdict, reason).
# Written by hand after reading the machine's rows.  A hand adjudication that is not
# published per row is a number nobody can chase.
ADJUDICATED = [
    ("branching_bound_audit_aaf4/PREDICTIONS.md", "carry a `33` line",
     "NOT A CONSUMER",
     "its 24 counts FILES CONTAINING A 33 LINE, a different quantity that "
     "collides with the glob's bounded-site count of 24"),
    ("branching_bound_audit_aaf4/README.md", "cannot see **12** unbounded",
     "DIAGNOSES", "mg-aaf4 states the glob's figure in order to fault it"),
    ("branching_bound_audit_aaf4/README.md", "globbed over `docs/*.md`",
     "DIAGNOSES", "the same, and it carries the wider 24 in the same sentence"),
    ("branching_bound_audit_aaf4/PREDICTIONS.md", "figure-stating file count",
     "DIAGNOSES", "quotes the parent's sentence as the object of a prediction"),
    ("branching_bound_audit_aaf4/README.md", "FOUR FILES, TWO GATED",
     "DIAGNOSES", "quotes the parent's sentence as the object of a finding"),
]


def live_prose_sentences(paths):
    out = []
    for p in paths:
        fp = os.path.join(U.ROOT, p)
        if not os.path.isfile(fp):
            continue
        try:
            for line, kind, s, _ in U.L.live_sentences(fp):
                out.append((p, line, re.sub(r"\s+", " ", s).strip()))
        except (IOError, OSError, UnicodeDecodeError):
            continue
    return out


def main():
    U.rule(OUT, "P3  WHICH PUBLISHED FIGURES INHERIT THE UNDERCOUNT.\n"
                "    Enumerated three ways: call sites, transcripts, prose.")
    print(file=OUT)

    # ---- the glob-derived values, computed here and not typed in -----------
    glob_sites = U.sites_of(U.ROOT, U.u_g_impl())
    gn, gnb, gnu = U.totals(glob_sites)
    gfiles = len({t[0] for t in glob_sites})
    full_sites = U.sites_of(U.ROOT, U.u_m_track())
    fn, fnb, fnu = U.totals(full_sites)
    ffiles = len({t[0] for t in full_sites})
    nglob = len(U.u_g_impl())

    U.rule(OUT, "  3.0  THE VALUES THE GLOB PRODUCES, computed here so that the\n"
                "       classifier below matches against derived numbers and not\n"
                "       against a hand-typed list.")
    derived = {gn: "corpus sites", gnu: "corpus unbounded", gfiles: "corpus files",
               nglob: "files in the glob", gnb: "corpus bounded"}
    for v, what in sorted(derived.items()):
        print("    %-6d %s" % (v, what), file=OUT)
    print(file=OUT)
    print("    the same five over the FULL population (tracked .md):", file=OUT)
    print("      %-6d sites   %-6d unbounded   %-6d files stating   %-6d files"
          % (fn, fnu, ffiles, len(U.u_m_track())), file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------------ C1
    U.rule(OUT, "  C1  THE CALL SITES.  Population: tracked .py.  Grain: one\n"
                "      occurrence of a universe-building idiom.")
    py = [p for p in U.lines(U.git("ls-files")) if p.endswith(".py")]
    hits = {k: [] for k, _, _ in IDIOMS}
    for p in py:
        try:
            with open(os.path.join(U.ROOT, p), encoding="utf-8",
                      errors="replace") as f:
                src = f.read().split("\n")
        except (IOError, OSError):
            continue
        for i, ln in enumerate(src, 1):
            for name, rx, _ in IDIOMS:
                if rx.search(ln):
                    hits[name].append((p, i, ln.strip()))
    print("    %-24s %6s   %s" % ("idiom", "hits", "what it enumerates"), file=OUT)
    for name, _, what in IDIOMS:
        print("    %-24s %6d   %s" % (name, len(hits[name]), what), file=OUT)
    print(file=OUT)
    narrow = [t for name, _, what in IDIOMS if "ONE LEVEL" in what
              for t in hits[name]]
    narrow = [t for t in narrow if not t[0].startswith(MINE)]
    print("    THE NARROW IDIOMS, EVERY OCCURRENCE, mine excluded (%d):"
          % len(narrow), file=OUT)
    for p, i, ln in narrow:
        print("      %s:%d" % (p, i), file=OUT)
        print("          %s" % ln[:96], file=OUT)
    print(file=OUT)
    print("    CONTROL: the same scan finds %d recursive/git-derived occurrence(s)"
          % sum(len(hits[n]) for n, _, w in IDIOMS if "ONE LEVEL" not in w),
          file=OUT)
    print("    in the same corpus, so the scan is not simply blind to breadth.",
          file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------------ C2
    U.rule(OUT, "  C2  THE TRANSCRIPT FIGURES.  Population: SUMMARY lines of\n"
                "      mg-d075's committed transcripts naming the corpus.\n"
                "      Grain: one published figure.")
    d075_out = sorted(f for f in os.listdir(U.D075) if f.startswith("out_")
                      and f.endswith(".txt"))
    tfigs = []
    for f in d075_out:
        with open(os.path.join(U.D075, f), encoding="utf-8",
                  errors="replace") as fh:
            for i, ln in enumerate(fh.read().split("\n"), 1):
                if ln.startswith("SUMMARY") and re.search(
                        r"corpus|docs/\*\.md", ln):
                    tfigs.append((f, i, ln.strip()))
    for f, i, ln in tfigs:
        print("    %s:%d" % (f, i), file=OUT)
        print("        %s" % ln[:100], file=OUT)
    print("    figures found : %d" % len(tfigs), file=OUT)
    print(file=OUT)
    print("    EACH OF THESE IS CORRECT OVER THE POPULATION ITS INSTRUMENT COULD",
          file=OUT)
    print("    SEE.  Re-derived over the full population the same three values are",
          file=OUT)
    print("      sites      %6d -> %6d" % (gn, fn), file=OUT)
    print("      unbounded  %6d -> %6d" % (gnu, fnu), file=OUT)
    print("      files      %6d -> %6d" % (gfiles, ffiles), file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------------ C3
    U.rule(OUT, "  C3  THE PROSE FIGURES.  Population: live sentences of tracked\n"
                "      .md naming the corpus universe and carrying a number.\n"
                "      Grain: one sentence.")
    cand_files = [p for p in U.u_m_track()
                  if re.search(r"branching|repair-mg-d075|1d6c", p)]
    sents = live_prose_sentences(cand_files)
    named = [(p, l, s) for p, l, s in sents
             if re.search(r"\bcorpus\b|docs/\*\.md", s) and re.search(r"\d", s)]
    inherit, other = [], []
    for p, l, s in named:
        nums = {int(x) for x in re.findall(r"\b\d{1,4}\b", s)}
        hit = sorted(nums & set(derived))
        (inherit if hit else other).append((p, l, s, hit))
    print("    sentences naming the corpus and carrying a number : %d"
          % len(named), file=OUT)
    print("    of them INHERITING a glob-derived value           : %d"
          % len(inherit), file=OUT)
    print("    of them carrying only other numbers (the CONTROL) : %d"
          % len(other), file=OUT)
    print(file=OUT)
    for i, (p, l, s, hit) in enumerate(inherit, 1):
        print("    [%02d] %s:%d   inherits %s"
              % (i, p, l, ", ".join(str(x) for x in hit)), file=OUT)
        for j in range(0, len(s), 96):
            print("         %s" % s[j:j + 96], file=OUT)
        print(file=OUT)
    print("    THE CONTROL COLUMN, in full -- sentences the classifier did NOT",
          file=OUT)
    print("    mark, from the same files:", file=OUT)
    for p, l, s, _ in other[:12]:
        print("      %s:%d  %s" % (p, l, s[:78]), file=OUT)
    if len(other) > 12:
        print("      ... and %d more" % (len(other) - 12), file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------ C3b
    U.rule(OUT, "  C3b  WHICH OF THOSE INHERIT THE UNDERCOUNT, AND WHICH MERELY\n"
                "       CITE IT.  Machine rule first, then hand adjudication with\n"
                "       a reason on every overridden row.  BOTH NUMBERS PUBLISHED.")
    rows = []
    for p, l, s, hit in inherit:
        if p.startswith(MINE):
            verdict, why = "MINE", "this ticket's own prose, quoting with attribution"
        elif WIDE_MARK.search(s):
            verdict, why = "CITES", "names the wider universe in the same sentence"
        else:
            verdict, why = "INHERITS", "states a glob-derived value as the population"
        for frag, sub, v, reason in ADJUDICATED:
            if frag in p and sub in s:
                verdict, why = v, "ADJUDICATED: " + reason
                break
        rows.append((p, l, s, hit, verdict, why))
    for i, (p, l, s, hit, verdict, why) in enumerate(rows, 1):
        print("    [%02d] %-14s %s:%d  (%s)"
              % (i, verdict, p[-46:], l, ", ".join(str(x) for x in hit)), file=OUT)
        print("         %s" % why[:96], file=OUT)
    print(file=OUT)
    kinds = {}
    for r in rows:
        kinds[r[4]] = kinds.get(r[4], 0) + 1
    print("    machine: %d sentence(s) carry a glob-derived value" % len(rows),
          file=OUT)
    for k in sorted(kinds):
        print("      %-16s %d" % (k, kinds[k]), file=OUT)
    inh = kinds.get("INHERITS", 0)
    print("    ADJUDICATED CONSUMERS OF THE UNDERCOUNT: %d" % inh, file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------ C5
    U.rule(OUT, "  C3c THE CONSUMER NOBODY HAS NAMED: THE UNIVERSE'S OWN SIZE.\n"
                "       PREDICTIONS.md P8b said at least one consumer would not be\n"
                "       36, 12, 29, 17 or 7.  This is it.")
    doc = os.path.join(U.DOCS, "repair-mg-d075-the-figure-and-its-scope.md")
    pub = []
    if os.path.exists(doc):
        with open(doc, encoding="utf-8") as f:
            for i, ln in enumerate(f.read().split("\n"), 1):
                m = re.search(r"(\d+)\s*`?docs/\*\.md", ln)
                if m:
                    pub.append((i, int(m.group(1)), ln.strip()))
    for i, v, ln in pub:
        print("    docs/repair-mg-d075-...:%d  publishes %d" % (i, v), file=OUT)
        print("        %s" % ln[:96], file=OUT)
    now_glob = len(U.u_g_impl())
    now_docs = len(U.u_d_track())
    now_all = len(U.u_m_track())
    print(file=OUT)
    print("    THE SAME QUANTITY, RE-DERIVED AT THIS COMMIT:", file=OUT)
    print("      the glob docs/*.md            : %d" % now_glob, file=OUT)
    print("      tracked .md under docs/       : %d" % now_docs, file=OUT)
    print("      tracked .md, the repository   : %d" % now_all, file=OUT)
    print(file=OUT)
    print("    A PUBLISHED FIGURE WHOSE POPULATION IS THE GLOB ITSELF.  It is not", file=OUT)
    print("    a site count, so no audit of the site counts has ever looked at it,", file=OUT)
    print("    and it inherits the same boundary: it is the size of the universe", file=OUT)
    print("    the glob can see and it is presented as the size of the corpus.", file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------------ C4
    U.rule(OUT, "  C4  THE SECOND-ORDER CONSUMERS.  Population: tracked .md that\n"
                "      QUOTE an inheriting figure without computing it.\n"
                "      Grain: one file.")
    quoters = sorted({p for p, _, _, _ in inherit})
    computed = {"code/branching_bound_d075/README.md",
                "docs/repair-mg-d075-the-figure-and-its-scope.md"}
    second = [p for p in quoters if p not in computed]
    print("    files carrying an inheriting figure : %d" % len(quoters), file=OUT)
    for p in quoters:
        print("      %-64s %s" % (p, "COMPUTED IT" if p in computed
                                  else "quotes it"), file=OUT)
    print(file=OUT)
    print("    THE UNDERCOUNT HAS TRAVELLED %d FILE(S) BEYOND THE INSTRUMENT THAT"
          % len(second), file=OUT)
    print("    PRODUCED IT.  Each is a dated record and none is edited here.",
          file=OUT)
    print(file=OUT)

    U.rule(OUT, "  VERDICT")
    print("    consumers of the glob, by kind:", file=OUT)
    print("      narrow call sites outside my own instrument : %d" % len(narrow),
          file=OUT)
    print("      transcript figures over the corpus          : %d" % len(tfigs),
          file=OUT)
    print("      prose sentences carrying a glob value       : %d" % len(inherit),
          file=OUT)
    print("      of them INHERITING after adjudication       : %d" % inh, file=OUT)
    print("      files carrying one                          : %d" % len(quoters),
          file=OUT)
    print("      published figures whose value IS the glob   : %d" % len(pub),
          file=OUT)
    print(file=OUT)

    U.rule(OUT)
    print("SUMMARY p3_consumers: narrow idiom occurrences %d in tracked .py "
          "(mine excluded)" % len(narrow), file=OUT)
    print("SUMMARY p3_consumers: recursive/git idiom occurrences %d -- the scan's "
          "control" % sum(len(hits[n]) for n, _, w in IDIOMS
                          if "ONE LEVEL" not in w), file=OUT)
    print("SUMMARY p3_consumers: transcript SUMMARY figures over the corpus %d"
          % len(tfigs), file=OUT)
    print("SUMMARY p3_consumers: prose sentences naming the corpus %d, carrying a "
          "glob value %d, control %d" % (len(named), len(inherit), len(other)),
          file=OUT)
    print("SUMMARY p3_consumers: machine %d rows -> %s after adjudication"
          % (len(rows), ", ".join("%s %d" % (k, kinds[k]) for k in sorted(kinds))),
          file=OUT)
    print("SUMMARY p3_consumers: ADJUDICATED consumers of the undercount %d" % inh,
          file=OUT)
    print("SUMMARY p3_consumers: C3c the universe's own size published as %s, "
          "re-derived glob %d / docs tracked %d / repo %d"
          % (", ".join(str(v) for _, v, _ in pub), now_glob, now_docs, now_all),
          file=OUT)
    print("SUMMARY p3_consumers: files carrying an inheriting figure %d, of which "
          "%d quote rather than compute" % (len(quoters), len(second)), file=OUT)
    print("SUMMARY p3_consumers: glob %d sites/%d unbounded vs population %d/%d"
          % (gn, gnu, fn, fnu), file=OUT)
    U.rule(OUT)
    return 1 if inherit or tfigs else 0


if __name__ == "__main__":
    sys.exit(main())
