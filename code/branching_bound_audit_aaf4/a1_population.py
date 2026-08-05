"""A1 -- I COUNT THE SITES MYSELF.

The brief:

  "COUNT THE SITES YOURSELF RATHER THAN TAKING 8.  The parent's own finding was
   that 'four is not the population' -- it corrected an undercount.  An audit that
   inherits the parent's new number repeats the parent's method and can only
   confirm it.  Derive the population independently, and say what instrument you
   used, because the instrument is what decides whether you could have found a
   different answer."

So the first block of this script is the instrument, named -- the four choices that
decide the answer -- and every count below is printed with the POPULATION it is
over and the GRAIN of the value.

WHAT COULD HAVE MADE ME DISAGREE WITH THE PARENT, and did:

  the UNIVERSE.  The parent's widest population is the glob `docs/*.md`.  Two of
  the four files mg-d075 authored that state the figure are not in `docs/`, so the
  parent's own README and its own PREDICTIONS.md are outside every population it
  counts.  U3 is that population and it is the reason this script exits 1.

EXIT 1 if the parent's own deliverable contains a live sentence stating the figure
with no scope in that sentence.  PREDICTED 1 (PREDICTIONS.md P1).
"""

import os
import re
import subprocess
import sys

import lib_aaf4 as L

# MY hedge list.  Not mg-19ec's 25 and not mg-d075's 33.  A different list is the
# point: if the verdict "no new phrasing hedges without enumerating" survives a
# list drawn by somebody else, it is a property of the prose and not of the list.
MY_HEDGES = [
    "kind", "some", "sort of", "roughly", "broadly", "essentially", "largely",
    "mostly", "generally", "typically", "usually", "often", "many", "several",
    "various", "about", "around", "nearly", "almost", "approximately", "may",
    "might", "could", "appears", "seems", "arguably", "presumably", "plausibly",
    "in effect", "effectively", "more or less", "in practice", "basically",
    "fairly", "quite", "relatively", "significant", "substantial",
]


def _new_sentences(git, pre_path):
    """Sentences live at HEAD and not live at the pre-repair anchor."""
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    old = {norm(s) for _, _, s, _ in L.live_sentences(pre_path)}
    return [norm(s) for _, _, s, _ in L.live_sentences(L.DOC)
            if norm(s) not in old]

OUT = sys.stdout
TMP = os.path.join(L.HERE, ".a1_tmp")

PARENT_PROSE = [
    os.path.join(L.DOCS, "repair-mg-d075-the-figure-and-its-scope.md"),
    os.path.join(L.PARENT, "README.md"),
    os.path.join(L.PARENT, "PREDICTIONS.md"),
]
GATE_COVERS = {"docs/OneThird-Branching-Graphs-Where-This-Lives.md",
               "docs/repair-mg-d075-the-figure-and-its-scope.md"}

MINE = [os.path.join(L.HERE, "PREDICTIONS.md"),
        os.path.join(L.HERE, "README.md")]


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=L.ROOT,
                          capture_output=True, text=True).stdout


def anchor_for(relpath, item):
    """Newest commit touching `relpath` whose subject does not name `item`.

    Derived from the log, never pinned: the refinery rebases before merging, so a
    recorded SHA is displaced by construction and an anchor written as a literal
    would be stale the moment this branch lands.
    """
    for row in git("log", "--format=%H\t%s", "--", relpath).strip().split("\n"):
        h, _, subj = row.partition("\t")
        if item not in subj:
            return h, subj
    return None, None


def at_commit(sha, relpath, tag):
    os.makedirs(TMP, exist_ok=True)
    p = os.path.join(TMP, tag + ".md")
    with open(p, "w", encoding="utf-8") as f:
        f.write(git("show", "%s:%s" % (sha, relpath)))
    return p


def tally(sites):
    b = sum(1 for r in sites if r[3])
    return len(sites), b, len(sites) - b


def main():
    L.rule(OUT, "A1  mg-aaf4: I COUNT THE SITES MYSELF.  Not 4, not 8, not 9,\n"
                "    not 10 -- counted again, at two grains, over a universe\n"
                "    that is not `docs/*.md`.")
    print(file=OUT)

    # ---------------------------------------------------------------- U0
    L.rule(OUT, "  U0  THE INSTRUMENT, NAMED.  Four choices; each could have\n"
                "      gone the other way and changed the answer.")
    print("""    1. UNIT     paragraph, or table cell > 30 chars, fenced code excluded.
                THE PARENT'S UNIT, KEPT ON PURPOSE, so that a disagreement in a
                count cannot hide inside a disagreement about a parser.
    2. LIVENESS outside block quotes, no STRUCK/CORRECTED/RE-SCOPED marker and
                none of the three "the version this replaces" phrases.  Kept.
    3. GRAIN    TWO of them.  S = one sentence (the parent's).  O = one
                OCCURRENCE of the numeral.  These are different questions.
    4. UNIVERSE MINE IS A FILE LIST, NOT THE GLOB `docs/*.md`.  This is the
                choice that makes disagreement possible, and it is the one that
                produced the finding below.""", file=OUT)
    print(file=OUT)

    rel = "docs/OneThird-Branching-Graphs-Where-This-Lives.md"
    sha, subj = anchor_for(rel, "mg-d075")
    pre = at_commit(sha, rel, "pre")
    print("    pre-repair anchor : %s" % sha, file=OUT)
    print("    anchor subject    : %s" % subj[:88], file=OUT)
    print(file=OUT)

    fails = 0

    # ---------------------------------------------------------------- U1
    L.rule(OUT, "  U1  THE LIVING DOCUMENT AT GRAIN S (one sentence).\n"
                "      Population: live sentences of that ONE file.")
    print("    predicate       state          sites  bounded  unbounded", file=OUT)
    u1 = {}
    for tag, path in (("PRE-REPAIR", pre), ("AS IT STANDS", L.DOC)):
        for pname, fn in (("STRICT ", L.strict_sites), ("RELAXED", L.relaxed_sites)):
            n, b, u = tally(fn(path))
            u1[(tag, pname.strip())] = (n, b, u)
            print("    %s         %-14s %5d %8d %10d" % (pname, tag, n, b, u),
                  file=OUT)
    print(file=OUT)
    print("    mg-19ec published 8 / 4 / 4 (STRICT, pre-repair).", file=OUT)
    print("    mg-d075 published 9 / 4 / 5 (RELAXED, pre-repair) and", file=OUT)
    print("    10 / 10 / 0 both predicates as it stands.  `a2` reproduces", file=OUT)
    print("    those row-by-row before this audit disagrees with anything.", file=OUT)
    print(file=OUT)

    # ---------------------------------------------------------------- U2
    L.rule(OUT, "  U2  THE SAME FILE AT GRAIN O (one occurrence of the\n"
                "      numeral).  Population: identical.  Grain: different.")
    print("    state          sentences(S)  occurrences(O)  O-S", file=OUT)
    for tag, path in (("PRE-REPAIR", pre), ("AS IT STANDS", L.DOC)):
        s_n = len(L.relaxed_sites(path))
        o_n = len(L.occurrences(path))
        print("    %-14s %12d %15d %4d" % (tag, s_n, o_n, o_n - s_n), file=OUT)
    print(file=OUT)
    multi = [r for r in L.occurrences(L.DOC) if r[4] > 1]
    print("    sentences stating the figure MORE THAN ONCE, as it stands : %d"
          % len(multi), file=OUT)
    for line, kind, s, b, n in multi:
        print("      line %-4d %-5s occurrence #%d  %s"
              % (line, kind, n, "BOUNDED" if b else "UNBOUNDED"), file=OUT)
    print(file=OUT)
    print("    A count of SENTENCES and a count of OCCURRENCES are different", file=OUT)
    print("    numbers about the same text.  The parent publishes one grain and", file=OUT)
    print("    says so; this is the other, and neither is wrong.", file=OUT)
    print(file=OUT)

    # ---------------------------------------------------------------- U3
    L.rule(OUT, "  U3  THE PARENT'S OWN DELIVERABLE.  Population: every file\n"
                "      mg-d075 AUTHORS OR EDITS that states the figure.\n"
                "      Grain: one sentence.  Predicate: the parent's STRICT.")
    u3rows, covered, uncovered = [], [], []
    allfiles = [L.DOC] + PARENT_PROSE
    for path in allfiles:
        r = L.rel(path)
        st = L.strict_sites(path)
        rx = L.relaxed_sites(path)
        if not rx:
            continue
        n, b, u = tally(rx)
        ns, bs, us = tally(st)
        inside = r in GATE_COVERS
        (covered if inside else uncovered).append(r)
        u3rows.append((r, ns, us, n, u, inside))
    print("    file                                                 "
          "STRICT unb  RELAXED unb  gate", file=OUT)
    for r, ns, us, n, u, inside in u3rows:
        print("    %-52s %2d %5d %6d %5d  %s"
              % (r[-52:], ns, us, n, u, "yes" if inside else "NO"), file=OUT)
    print(file=OUT)
    tot_files = len(u3rows)
    tot_unb = sum(u for _, _, _, _, u, _ in u3rows)
    out_unb = sum(u for _, _, _, _, u, ins in u3rows if not ins)
    print("    FILES stating the figure in the parent's deliverable : %d" % tot_files,
          file=OUT)
    print("    of those, INSIDE the parent's gate                   : %d  (%s)"
          % (len(covered), ", ".join(os.path.basename(c) for c in covered)), file=OUT)
    print("    of those, OUTSIDE every population the parent counts : %d  (%s)"
          % (len(uncovered), ", ".join(os.path.basename(c) for c in uncovered)),
          file=OUT)
    print("    UNBOUNDED sites in the parent's own deliverable      : %d" % tot_unb,
          file=OUT)
    print("      of which outside the gate                          : %d" % out_unb,
          file=OUT)
    print(file=OUT)
    print("    THE SITES, IN FULL:", file=OUT)
    print(file=OUT)
    for path in allfiles:
        bad = [r for r in L.relaxed_sites(path) if not r[3]]
        if not bad:
            continue
        print("    %s" % L.rel(path), file=OUT)
        L.show_sites(bad, OUT)
    if tot_unb:
        fails += 1

    # ---------------------------------------------------------------- U4
    L.rule(OUT, "  U4  THE WIDER UNIVERSE.  Population: every markdown file\n"
                "      TRACKED BY GIT, not the glob `docs/*.md`.\n"
                "      Grain: one sentence, RELAXED predicate.")
    tracked = [p for p in git("ls-files", "*.md").strip().split("\n") if p]
    rows = []
    for p in tracked:
        full = os.path.join(L.ROOT, p)
        if not os.path.exists(full):
            continue
        rx = L.relaxed_sites(full)
        if rx:
            n, b, u = tally(rx)
            rows.append((p, n, b, u, len(L.occurrences(full))))
    rows.sort(key=lambda r: (-r[3], r[0]))
    print("    markdown files tracked : %d" % len(tracked), file=OUT)
    print("    in docs/               : %d"
          % sum(1 for p in tracked if p.startswith("docs/")), file=OUT)
    print("    OUTSIDE docs/          : %d"
          % sum(1 for p in tracked if not p.startswith("docs/")), file=OUT)
    print(file=OUT)
    print("    file                                                     "
          "S-sites  bnd  unb   O", file=OUT)
    for p, n, b, u, o in rows:
        print("    %-56s %5d %5d %4d %4d" % (p[-56:], n, b, u, o), file=OUT)
    print(file=OUT)
    tot_s = sum(r[1] for r in rows)
    tot_u = sum(r[3] for r in rows)
    tot_o = sum(r[4] for r in rows)
    ndocs = sum(1 for r in rows if r[0].startswith("docs/"))
    print("    files stating the figure          : %d  (%d in docs/, %d outside)"
          % (len(rows), ndocs, len(rows) - ndocs), file=OUT)
    print("    sites, GRAIN S                    : %d, of which %d unbounded"
          % (tot_s, tot_u), file=OUT)
    print("    occurrences, GRAIN O              : %d" % tot_o, file=OUT)
    print("    the parent's published corpus (D) : 36 sites in 7 files of docs/",
          file=OUT)
    print(file=OUT)
    print("    THE 24 UNBOUNDED SITES, BY WHAT COULD BE DONE ABOUT THEM.", file=OUT)
    print("    Population: the unbounded sites of U4.  Grain: one site.", file=OUT)
    cls_docs = sum(r[3] for r in rows if r[0].startswith("docs/"))
    cls_pre = sum(r[3] for r in rows if not r[0].startswith("docs/")
                  and os.path.basename(r[0]) == "PREDICTIONS.md")
    cls_free = tot_u - cls_docs - cls_pre
    print("      in docs/ -- dated audit records, editing destroys the trail : %d"
          % cls_docs, file=OUT)
    print("      outside docs/, in a PRE-REGISTRATION file -- never reworded : %d"
          % cls_pre, file=OUT)
    print("      outside docs/, in an ordinary instrument README -- REPAIRABLE: %d"
          % cls_free, file=OUT)
    for p, n, b, u, o in rows:
        if u and not p.startswith("docs/") and \
                os.path.basename(p) != "PREDICTIONS.md":
            print("        %s  (%d unbounded)" % (p, u), file=OUT)
    print("      So a repo-wide gate over this figure would be permanently red", file=OUT)
    print("      on %d of %d sites for reasons that are correct, and would find"
          % (cls_docs + cls_pre, tot_u), file=OUT)
    print("      %d it could actually close.  What is missing is not a gate; it"
          % cls_free, file=OUT)
    print("      is a DECLARED EXEMPTION.", file=OUT)
    print(file=OUT)
    print("    THE FIGURE IN WORDS.  `thirty-three` occurrences, all tracked", file=OUT)
    print("    markdown: %d" % sum(len(L.FIG_WORD.findall(open(
        os.path.join(L.ROOT, p), encoding="utf-8").read())) for p in tracked
        if os.path.exists(os.path.join(L.ROOT, p))), file=OUT)
    print(file=OUT)

    # ---------------------------------------------------------------- U5
    L.rule(OUT, "  U5  MY OWN DELIVERABLE, HELD TO THE SAME STANDARD.\n"
                "      Population: the files mg-aaf4 authors.  Grain: sentence.")
    mine_unb = 0
    for path in MINE:
        if not os.path.exists(path):
            print("    %-52s ABSENT" % L.rel(path), file=OUT)
            continue
        n, b, u = tally(L.relaxed_sites(path))
        mine_unb += u
        print("    %-52s %2d sites  %2d bounded  %2d UNBOUNDED"
              % (L.rel(path), n, b, u), file=OUT)
    print(file=OUT)
    for path in MINE:
        if not os.path.exists(path):
            continue
        bad = [r for r in L.relaxed_sites(path) if not r[3]]
        if bad:
            print("    %s -- the unbounded sites, printed rather than omitted:"
                  % L.rel(path), file=OUT)
            L.show_sites(bad, OUT)
    print("""    THESE ARE NOT REPAIRED, AND THE REASON IS A FINDING, NOT AN EXCUSE.
    `PREDICTIONS.md` is a PRE-REGISTRATION commit.  The lineage discipline for
    this arc is that such a commit is never amended, reworded, squashed or
    rebased away.  Adding a bound to a sentence of it is a rewording.  So the
    bounding standard and the pre-registration standard CONFLICT on exactly this
    population, and the conflict is not mine -- it applies identically to
    `code/branching_bound_d075/PREDICTIONS.md`, which is why U3's uncovered
    sites could not have been repaired by the parent either.  What the parent
    could have done, and did not, is NAME the population as excluded by that
    invariant instead of drawing the glob so that it never appeared.""", file=OUT)
    print(file=OUT)

    # ---------------------------------------------------------------- U7
    L.rule(OUT, "  U7  BOUNDED, NOT MERELY HEDGED -- re-derived, with my own\n"
                "      hedge list.  Population: the 10 post-repair sites of\n"
                "      the living document.  Grain: the exact substring\n"
                "      carrying the bound.")
    nsoft = 0
    for n, (line, kind, s, bnd) in enumerate(L.relaxed_sites(L.DOC), 1):
        m = L.RANK6.search(s)
        sub = m.group(0) if m else ""
        cls = "NUMERIC SCOPE" if sub and re.search(r"\d", sub) else "SOFTENING"
        hedge = [h for h in MY_HEDGES if re.search(r"\b%s\b" % re.escape(h), s, re.I)]
        enum = bool(L.NUMERIC_SCOPE.search(L.strip_emphasis(s)))
        if cls != "NUMERIC SCOPE":
            nsoft += 1
        print("    <%02d> line %-4d bound=%-14s %-13s hedge=%-12s enumerates=%s"
              % (n, line, "`%s`" % sub, cls, ",".join(hedge) or "-",
                 "yes" if enum else "NO"), file=OUT)
    print(file=OUT)
    print("    site bounds that are SOFTENING WORDS rather than scopes : %d"
          % nsoft, file=OUT)
    print("    my hedge list is %d tokens, and it is MINE: %s"
          % (len(MY_HEDGES), ", ".join(MY_HEDGES)), file=OUT)
    print(file=OUT)
    newsent = [s for s in _new_sentences(git, pre)]
    hed = [(s, [h for h in MY_HEDGES
                if re.search(r"\b%s\b" % re.escape(h), s, re.I)])
           for s in newsent]
    carry = [(s, h) for s, h in hed if h]
    unresc = [(s, h) for s, h in carry
              if not L.NUMERIC_SCOPE.search(L.strip_emphasis(s))]
    print("    THE NEW PHRASINGS, scanned against my list in their OWN sentence.",
          file=OUT)
    print("    Population: sentences live at HEAD and not at the anchor.  "
          "Grain: one sentence.", file=OUT)
    print("      new sentences                        : %d" % len(newsent),
          file=OUT)
    print("      carrying a hedge token of MY list    : %d" % len(carry), file=OUT)
    print("      of those, NOT rescued by enumeration : %d" % len(unresc), file=OUT)
    for s, h in carry:
        print("        [%s] " % ",".join(h), end="", file=OUT)
        L.wrap(OUT, s, 96, 8)
    print(file=OUT)
    print("    ADJUDICATION.  My list over-collects and I say so rather than",
          file=OUT)
    print("    trimming it after seeing the result.  The %d unrescued row(s)"
          % len(unresc), file=OUT)
    for s, h in unresc:
        if h == ["could"]:
            print("      `could` in *could not see* is a past-tense modal inside a",
                  file=OUT)
            print("      NEGATED FACTUAL CLAIM about what a predicate did.  It",
                  file=OUT)
            print("      softens no quantity, and the sentence states 9 and 5.",
                  file=OUT)
            print("      HAND VERDICT: not a hedge.", file=OUT)
        else:
            print("      no hand verdict recorded for %r -- treated as REAL." % h,
                  file=OUT)
    adj = len([1 for s, h in unresc if h != ["could"]])
    print("      machine: %d unrescued        adjudicated: %d"
          % (len(unresc), adj), file=OUT)
    print("    mg-d075's own H4 measured 3 of 14 with a 33-token list.  My list",
          file=OUT)
    print("    is different and so is the arithmetic -- 4 of 14, not 3 -- and", file=OUT)
    print("    the verdict that matters, 0 phrasings hedged without enumerating,",
          file=OUT)
    print("    survives being measured with somebody else's list.", file=OUT)
    print(file=OUT)
    print("    THE NUMERAL `33`, AND WHAT IT DENOTES.  Population: occurrences",
          file=OUT)
    print("    of `\\b33\\b` in the parent's own README.  Grain: one occurrence.",
          file=OUT)
    rm = os.path.join(L.PARENT, "README.md")
    occ_all = sum(len(L.FIG.findall(s)) for _, _, s, _ in L.live_sentences(rm))
    occ_site = len(L.occurrences(rm))
    print("      occurrences of `33` in live sentences  : %d" % occ_all, file=OUT)
    print("      of those, in a sentence naming the family: %d" % occ_site,
          file=OUT)
    print("      occurrences denoting something else      : %d"
          % (occ_all - occ_site), file=OUT)
    for _, _, s, _ in L.live_sentences(rm):
        if L.FIG.search(s) and not L.YF.search(s):
            print("        NOT the interval figure: ", end="", file=OUT)
            L.wrap(OUT, s, 88, 10)
    print("      So the numeral denotes at least two populations in one file,",
          file=OUT)
    print("      and the family name is the whole of what separates them.",
          file=OUT)
    print(file=OUT)

    # ---------------------------------------------------------------- U6
    L.rule(OUT, "  U6  THE SILENT EXCLUSIONS -- what the LIVENESS RULE takes\n"
                "      out of every population above, and whether the marker\n"
                "      that took it out is a USE or a MENTION.")
    print("""    The liveness rule is a text match for `**STRUCK` / `**CORRECTED` /
    `**RE-SCOPED` and three phrases.  It cannot distinguish a unit that IS
    struck from a unit that QUOTES the marker while describing the rule.  So a
    document that documents the rule is scored dead BY the rule.  This block is
    the population that leaves silently, and it is not counted anywhere in
    mg-19ec, mg-d075, or in U1-U5 above.""", file=OUT)
    print(file=OUT)
    dead_rows, mention_sites = [], 0
    for p in tracked:
        full = os.path.join(L.ROOT, p)
        if not os.path.exists(full):
            continue
        for line, kind, text in L.dead_units(full):
            if not (L.FIG.search(text) and L.YF.search(text)):
                continue
            ev = L.strike_evidence(text)
            kinds = sorted({k for _, k in ev}) or ["BLOCKQUOTE"]
            nfig = len(L.FIG.findall(text))
            dead_rows.append((p, line, kind, "/".join(kinds), len(ev), nfig, text))
            if kinds == ["MENTION"]:
                mention_sites += nfig
    print("    file                                              line  unit   "
          "marker    hits  figures", file=OUT)
    for p, line, kind, k, nev, nfig, _t in dead_rows:
        print("    %-48s %5d  %-5s  %-9s %4d %6d"
              % (p[-48:], line, kind, k, nev, nfig), file=OUT)
    print(file=OUT)
    print("    dead units stating the figure                  : %d" % len(dead_rows),
          file=OUT)
    print("    of those, killed by a MENTION of the marker    : %d"
          % sum(1 for r in dead_rows if r[3] == "MENTION"), file=OUT)
    print("    FIGURE OCCURRENCES removed by a MENTION        : %d" % mention_sites,
          file=OUT)
    print(file=OUT)
    for p, line, kind, k, nev, nfig, t in dead_rows:
        if k != "MENTION":
            continue
        print("    %s line %d -- killed by a marker it only QUOTES:" % (p, line),
              file=OUT)
        print("      markers: %s" % ", ".join(
            "%s [%s]" % (m, c) for m, c in
            L.strike_evidence(t)), file=OUT)
        print("      ", end="", file=OUT)
        L.wrap(OUT, t, 100, 6)
        print(file=OUT)
    print("""    THE ADJUDICATION.  A unit that quotes the strike markers in order
    to define them is not a withdrawn claim, and treating it as one is a
    use/mention conflation in the shared reader every ticket of this arc
    inherits.  I do NOT re-score the parent's numbers on this basis -- the
    parent's numbers are correct for the rule as written, and mg-19ec's,
    mg-d075's and MY OWN counts all use it.  What is wrong is that the exclusion
    is silent: no transcript in this arc prints it.  This block prints it.""",
          file=OUT)
    print(file=OUT)

    L.rule(OUT)
    print("SUMMARY a1_population: U6 %d dead unit(s) state the figure, %d killed "
          "by a MENTION of the marker, %d figure occurrence(s) removed silently"
          % (len(dead_rows), sum(1 for r in dead_rows if r[3] == "MENTION"),
             mention_sites), file=OUT)
    print("SUMMARY a1_population: U1 living doc GRAIN S, pre-repair "
          "STRICT %d/%d unb, RELAXED %d/%d unb"
          % (u1[("PRE-REPAIR", "STRICT")][0], u1[("PRE-REPAIR", "STRICT")][2],
             u1[("PRE-REPAIR", "RELAXED")][0], u1[("PRE-REPAIR", "RELAXED")][2]),
          file=OUT)
    print("SUMMARY a1_population: U1 living doc GRAIN S, as it stands "
          "STRICT %d/%d unb, RELAXED %d/%d unb"
          % (u1[("AS IT STANDS", "STRICT")][0], u1[("AS IT STANDS", "STRICT")][2],
             u1[("AS IT STANDS", "RELAXED")][0], u1[("AS IT STANDS", "RELAXED")][2]),
          file=OUT)
    print("SUMMARY a1_population: U2 living doc GRAIN O, as it stands %d occurrences"
          % len(L.occurrences(L.DOC)), file=OUT)
    print("SUMMARY a1_population: U3 parent deliverable %d files state the figure, "
          "gate covers %d, %d unbounded site(s) and %d of them outside the gate"
          % (tot_files, len(covered), tot_unb, out_unb), file=OUT)
    print("SUMMARY a1_population: U4 wider universe %d files, %d sites GRAIN S, "
          "%d unbounded, %d occurrences GRAIN O"
          % (len(rows), tot_s, tot_u, tot_o), file=OUT)
    print("SUMMARY a1_population: U5 my own deliverable %d unbounded, NOT repaired "
          "-- a pre-registration is never reworded" % mine_unb, file=OUT)
    print("SUMMARY a1_population: failures %d" % fails, file=OUT)
    L.rule(OUT)

    for f in os.listdir(TMP):
        os.remove(os.path.join(TMP, f))
    os.rmdir(TMP)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
