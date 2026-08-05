"""SELFTEST -- break the repaired document on purpose, nine ways, and check the
instrument notices.  A gate that has never been shown to fail is not a gate.

EVERY MUTATION IS CHECKED TO BE A REAL MUTATION FIRST.  mg-fcb2's finding against
its own parent was that a corruption which is a no-op leaves a green row that means
nothing.  So each case below asserts `mutated != original` BEFORE asserting that the
detector's verdict moved, and the assertion is printed.

  M1  REMOVE THE BOUND from each site in turn (9 mutations).  Each must move
      exactly that site from BOUNDED to UNBOUNDED and leave the population size
      alone.  Population per mutation: the 9 sites.  Grain: one site's verdict.

  M2  REPLACE THE BOUND WITH A HEDGE ("roughly", "essentially", "broadly").  The
      site must remain UNBOUNDED.  This is the case that distinguishes a bound
      from a softening, and it is the one this whole arc turns on.

  M3  DELETE A SITE SENTENCE.  The population must fall by 1.  Without this, "0
      unbounded" is achievable by deletion.

  M4  BLOCK-QUOTE A SITE.  Liveness must drop it: population falls.

  M5  MARK A SITE'S UNIT STRUCK.  Same.

  M6  ADD A NEW UNBOUNDED SITE.  The population must rise by 1 and unbounded must
      become 1 -- the regression case the gate exists for.

EXIT 0 if every mutation is a real mutation and every verdict moves as stated.
PREDICTED 0.
"""

import os
import re
import sys

import lib_d075 as L

OUT = sys.stdout
TMP = os.path.join(L.HERE, ".selftest_doc.md")
BAD = 0


def with_text(text):
    with open(TMP, "w", encoding="utf-8") as f:
        f.write(text)
    return L.relaxed_sites(TMP)


def find_flex(base, sentence, n=60):
    """Locate a normalised sentence in the RAW file text.

    A sentence read at unit grain has its newlines collapsed to single spaces, so
    a literal `base.find(sentence[:60])` fails for any hard-wrapped paragraph --
    which is how it failed on site <04> the first time this selftest ran.  The
    prefix is turned into a whitespace-flexible pattern instead.
    """
    toks = [re.escape(t) for t in sentence[:n].split() if t]
    if not toks:
        return -1
    m = re.search(r"\s+".join(toks), base)
    return m.start() if m else -1


def ck(label, ok, extra=""):
    global BAD
    print("    %-62s %s%s" % (label, "ok" if ok else "BAD", extra), file=OUT)
    if not ok:
        BAD += 1


def main():
    global BAD
    base = open(L.DOC, encoding="utf-8").read()
    sites0 = L.relaxed_sites(L.DOC)
    n0 = len(sites0)
    L.rule(OUT, "SELFTEST mg-d075 -- nine deliberate breakages of the repaired\n"
                "         document, each checked to be a real breakage first.")
    print(file=OUT)
    print("  baseline: %d sites, %d bounded, %d unbounded"
          % (n0, sum(1 for t in sites0 if t[3]),
             sum(1 for t in sites0 if not t[3])), file=OUT)
    print(file=OUT)

    # ------------------------------------------------------------------ M1
    L.rule(OUT, "  M1  REMOVE THE BOUND, site by site.  9 mutations.")
    for i, (line, kind, s, b) in enumerate(sites0, 1):
        m = L.RANK6.search(s)
        if not m:
            ck("site <%02d> has a bound to remove" % i, False)
            continue
        frag = m.group(0)
        # remove the FIRST occurrence of the bound fragment inside this site only
        idx = find_flex(base, s)
        if idx < 0:
            ck("site <%02d> located verbatim in the file" % i, False)
            continue
        seg = base[idx:idx + len(s) + 200]
        newseg = seg.replace(frag, "", 1)
        mutated = base[:idx] + newseg + base[idx + len(s) + 200:]
        changed = mutated != base
        sites = with_text(mutated)
        nunb = sum(1 for t in sites if not t[3])
        ck("site <%02d> line %-4d mutation is a real change" % (i, line), changed)
        ck("site <%02d> line %-4d removing `%s` makes 1 site unbounded"
           % (i, line, frag), nunb == 1, "   (%d unbounded, %d sites)"
           % (nunb, len(sites)))
    print(file=OUT)

    # ------------------------------------------------------------------ M2
    L.rule(OUT, "  M2  REPLACE THE BOUND WITH A HEDGE.  A softening word must NOT\n"
                "      score as a bound.  This is the case the arc turns on.")
    line, kind, s, _ = sites0[2]
    m = L.RANK6.search(s)
    for hedge in ("roughly", "essentially", "broadly the same range"):
        mutated = base.replace(m.group(0), hedge, 1)
        changed = mutated != base
        sites = with_text(mutated)
        nunb = sum(1 for t in sites if not t[3])
        ck("hedge '%s' is a real change" % hedge, changed)
        ck("hedge '%s' does NOT score as a bound" % hedge, nunb >= 1,
           "   (%d unbounded)" % nunb)
    print(file=OUT)

    # ------------------------------------------------------------------ M3
    L.rule(OUT, "  M3  DELETE A SITE SENTENCE.  Population must fall by 1.")
    victim = sites0[8][2]
    idx = find_flex(base, victim, 80)
    ck("victim sentence located verbatim", idx >= 0)
    if idx >= 0:
        end = idx + len(victim)
        mutated = base[:idx] + base[end:]
        ck("deletion is a real change", mutated != base)
        sites = with_text(mutated)
        ck("deleting one site drops the population by 1", len(sites) == n0 - 1,
           "   (%d -> %d)" % (n0, len(sites)))
    print(file=OUT)

    # ------------------------------------------------------------------ M4
    L.rule(OUT, "  M4  BLOCK-QUOTE A SITE.  Liveness must drop it.")
    para = [t for t in sites0 if t[1] == "para"][0]
    lines = base.split("\n")
    hit = next((i for i, l in enumerate(lines) if para[2][:50] in l), None)
    if hit is None:
        # the sentence may span source lines; quote the whole paragraph block
        hit = para[0] - 1
    lines2 = list(lines)
    j = hit
    while j < len(lines2) and lines2[j].strip():
        lines2[j] = "> " + lines2[j]
        j += 1
    while hit > 0 and lines2[hit - 1].strip():
        hit -= 1
        lines2[hit] = "> " + lines2[hit]
    mutated = "\n".join(lines2)
    ck("block-quoting is a real change", mutated != base)
    sites = with_text(mutated)
    ck("block-quoting a paragraph site removes it from the population",
       len(sites) < n0, "   (%d -> %d)" % (n0, len(sites)))
    print(file=OUT)

    # ------------------------------------------------------------------ M5
    L.rule(OUT, "  M5  MARK A SITE'S UNIT STRUCK.  Same.")
    lines2 = base.split("\n")
    k = para[0] - 1
    lines2[k] = "**STRUCK (selftest)** " + lines2[k]
    mutated = "\n".join(lines2)
    ck("strike marker is a real change", mutated != base)
    sites = with_text(mutated)
    ck("a struck unit leaves the population", len(sites) < n0,
       "   (%d -> %d)" % (n0, len(sites)))
    print(file=OUT)

    # ------------------------------------------------------------------ M6
    L.rule(OUT, "  M6  ADD A NEW UNBOUNDED SITE.  The regression case.")
    inject = ("\n\nA new paragraph asserting that 28 of the 33 Young–Fibonacci "
              "intervals are distributive, with no scope at all.\n")
    mutated = base + inject
    ck("injection is a real change", mutated != base)
    sites = with_text(mutated)
    nunb = sum(1 for t in sites if not t[3])
    ck("a new unbounded site raises the population by 1", len(sites) == n0 + 1,
       "   (%d -> %d)" % (n0, len(sites)))
    ck("a new unbounded site is scored unbounded", nunb == 1,
       "   (%d unbounded)" % nunb)
    print(file=OUT)

    if os.path.exists(TMP):
        os.remove(TMP)
    L.rule(OUT)
    print("SUMMARY selftest_d075: baseline %d sites, %d bounded"
          % (n0, sum(1 for t in sites0 if t[3])), file=OUT)
    print("SUMMARY selftest_d075: failures %d" % BAD, file=OUT)
    L.rule(OUT)
    return 1 if BAD else 0


if __name__ == "__main__":
    sys.exit(main())
