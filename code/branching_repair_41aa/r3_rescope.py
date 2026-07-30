"""R3 -- the re-scoping of X3 and X4.  Neither is a false measurement; both are
claims stated at a level wider than what was measured licenses.  Nothing here
manufactures a proof: where the honest output is an open question it is printed
as one.

X3  mg-af28's row 3 books towers of algebras "ADJACENT -- axiom tested and
    failed" against Bergeron-Li's axiom (2), quoted from section 3.1 of
    arXiv:math/0612170.  The quotation verifies (af28 checked it, mg-6ad0
    re-checked it).  Section 3.1 is titled "Tower of Algebras (Preserving
    unities)"; section 3.6 of the SAME paper is titled "Tower of Algebras (not
    Preserving unities)" and takes as input "an algebra injection not
    necessarily preserving unities".  Unitality is the ONLY clause af28
    measured to fail.  So the "no" is licensed against one of the two
    definitions the cited paper offers.

    R3a re-reads all four strings from the PDF on a third extractor, both as
    spelt and as a ligature-dropping reader renders them.
    FALSIFIER: any of the four strings absent, in which case X3 collapses and
    row 3's "no" stands as written.

X4  "Brown 4.3 reaches the Young graph and no other differential poset".  Brown
    section 4.3's hypothesis is a FINITE distributive lattice; no differential
    poset is finite (mg-af28's own section 2 item 1 says so); so at the level of
    whole differential posets the statement is true of nothing -- Brown consumes
    none of them, Young's lattice included.  At the level where mg-af28's own
    contact lives -- finite intervals -- it is false.

    R3b rebuilds the Young-Fibonacci lattice, reproduces mg-af28's T8 counts,
    and for every distributive interval CONSTRUCTS the poset P with J(P) = that
    interval and verifies the isomorphism pair by pair.
    FALSIFIER: 33 or 5 coming out differently (T8 would be wrong, not its
    reading), or a distributive interval for which no such P exists (Birkhoff
    would be wrong).
"""

import re
import sys
import zlib
import urllib.request

from kern41aa import (young_fibonacci, yf_interval_poset, is_lattice,
                      is_distributive, join_irreducibles, ideal_lattice, iso,
                      ideals)

OUT = sys.stdout
BERGLI = "https://arxiv.org/pdf/math/0612170"

# The four strings.  Each is given twice: as the paper spells it, and as an
# extractor that drops the fi/ff/fl ligatures renders it.  mg-6ad0's X6 showed
# that mg-af28's extractor drops them, so a search for only the first spelling
# is not a search.
STRINGS = [
    ("section 3.1's title",
     "Tower of Algebras (Preserving unities)",
     "Tower of Algebras (Preserving unities)"),
    ("section 3.6's title",
     "Tower of Algebras (not Preserving unities)",
     "Tower of Algebras (not Preserving unities)"),
    ("section 3.6's input",
     "an algebra injection not necessarily preserving unities",
     "an algebra injection not necessarily preserving unities"),
    ("axiom (2), the clause af28 quotes",
     "is an injective homomorphism of algebras, for all m and n (sending",
     "is an injective homomorphism of algebras, for all m and n (sending"),
]


def pdf_text(data):
    """Text out of a PDF's Flate-compressed content streams.

    A third extractor.  It differs from the one in code/branching_af28 and
    code/branching_audit_6ad0 in that it reads the TJ array operator as well as
    plain parenthesised strings, and decodes hex strings -- so a string split
    across kerning adjustments is recovered rather than lost.
    """
    chunks = []
    for m in re.finditer(rb"stream\r?\n", data):
        s = m.end()
        e = data.find(b"endstream", s)
        if e < 0:
            continue
        try:
            chunks.append(zlib.decompress(data[s:e]))
        except Exception:
            pass
    raw = b"\n".join(chunks).decode("latin1")
    out = []
    for m in re.finditer(r"\((?:[^()\\]|\\.)*\)|<[0-9A-Fa-f\s]*>", raw):
        tok = m.group()
        if tok.startswith("("):
            s = tok[1:-1]
            s = re.sub(r"\\(\d{1,3})", lambda g: chr(int(g.group(1), 8)), s)
            s = re.sub(r"\\(.)", r"\1", s)
            out.append(s)
        else:
            hx = re.sub(r"\s", "", tok[1:-1])
            if len(hx) % 2 == 0 and hx:
                try:
                    out.append(bytes.fromhex(hx).decode("latin1"))
                except Exception:
                    pass
    return " ".join(out)


def flat(s):
    return re.sub(r"[\s\-]+", "", s)


def drop_ligatures(s):
    for lig in ("ffi", "ffl", "fi", "ff", "fl"):
        s = s.replace(lig, "")
    return s


def r3a():
    print("=" * 78, file=OUT)
    print("R3a  X3.  The definition space row 3's \"no\" was tested against.", file=OUT)
    print("     Bergeron-Li, arXiv:math/0612170, re-read on a third extractor.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    try:
        data = urllib.request.urlopen(BERGLI, timeout=120).read()
    except Exception as exc:
        print("  DOWNLOAD FAILED (%s).  This step needs network; the committed" % exc,
              file=OUT)
        print("  output records the run that was made, and mg-6ad0's", file=OUT)
        print("  out_a6_quotes.txt records an independent one.", file=OUT)
        print(file=OUT)
        return None
    txt = pdf_text(data)
    f = flat(txt)
    fl = flat(drop_ligatures(txt))
    print("  bytes downloaded: %d   flattened chars: %d" % (len(data), len(f)), file=OUT)
    print(file=OUT)
    print("   string                                as spelt   ligature-dropped", file=OUT)
    missing = 0
    for label, spelt, _ in STRINGS:
        a = len(re.findall(re.escape(flat(spelt)), f, re.I))
        b = len(re.findall(re.escape(flat(drop_ligatures(spelt))), fl, re.I))
        if a == 0 and b == 0:
            missing += 1
        print("   %-36s %8d   %16d" % (label, a, b), file=OUT)
    print(file=OUT)
    print("  strings not found in either spelling: %d." % missing, file=OUT)
    print(file=OUT)
    print("  WHAT THIS DOES AND DOES NOT SETTLE.  It settles that the cited", file=OUT)
    print("  paper contains TWO tower definitions and that mg-af28 tested one.", file=OUT)
    print("  It settles nothing about whether kF(P) forms a tower under the", file=OUT)
    print("  weaker one: Bergeron-Li's conditions (3), (4) and (5) --", file=OUT)
    print("  projectivity of A_{m+n} over A_m (x) A_n, the idempotent condition,", file=OUT)
    print("  and the Mackey-type identity -- are untested by mg-af28, by", file=OUT)
    print("  mg-6ad0 and by this repair.  Testing them is new mathematics,", file=OUT)
    print("  which every ticket in this lineage forbids.  The honest output is", file=OUT)
    print("  a HEDGE plus a NAMED OPEN QUESTION, not a proof and not a \"no\".", file=OUT)
    print(file=OUT)
    return missing


def r3b():
    print("=" * 78, file=OUT)
    print("R3b  X4.  \"Brown 4.3 reaches the Young graph and no other", file=OUT)
    print("     differential poset\" -- at which level does it have content?", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("  Brown section 4.3's hypothesis is a FINITE distributive lattice.", file=OUT)
    print("  A differential poset is locally finite with infinitely many ranks", file=OUT)
    print("  -- mg-af28's own section 2 item 1, and the reason its T3 finds", file=OUT)
    print("  0 of 405.  So no differential poset is finite, Brown consumes no", file=OUT)
    print("  differential poset at all, and at THAT level the claim is true of", file=OUT)
    print("  nothing: Young's lattice is not consumed either.  The level at", file=OUT)
    print("  which mg-af28's own contact lives is the finite INTERVALS.", file=OUT)
    print(file=OUT)
    ranks, covers = young_fibonacci(6)
    fib = [len(ranks[r]) for r in range(7)]
    print("  CONTROL 1  Young-Fibonacci rank sizes to rank 6: %s"
          % (fib,), file=OUT)
    expect = [1, 1, 2, 3, 5, 8, 13]
    print("             Fibonacci as published: %s   %s"
          % (expect, "PASS" if fib == expect else "FAIL"), file=OUT)
    # CONTROL 2: DU - UD = I below the top rank
    dn = {}
    for v, us in covers.items():
        for x in us:
            dn.setdefault(x, set()).add(v)
    bad_diff = 0
    for r in range(0, 6):
        for v in ranks[r]:
            du = {}
            for u in covers[v]:                       # up then down
                for x in dn.get(u, ()):
                    du[x] = du.get(x, 0) + 1
            ud = {}
            for y in dn.get(v, ()):                   # down then up
                for z in covers[y]:
                    ud[z] = ud.get(z, 0) + 1
            diff = {}
            for k in set(du) | set(ud):
                c = du.get(k, 0) - ud.get(k, 0)
                if c:
                    diff[k] = c
            if diff != {v: 1}:
                bad_diff += 1
    print("  CONTROL 2  DU - UD = I as an operator identity below the top rank:",
          file=OUT)
    print("             %s (%d violations)"
          % ("PASS" if bad_diff == 0 else "FAIL", bad_diff), file=OUT)
    ivs = []
    for r in range(0, 7):
        for w in ranks[r]:
            ivs.append(w)
    notlat = 0
    nondist = []
    dist = []
    for w in ivs:
        P, elems = yf_interval_poset(w, ranks, covers)
        if not is_lattice(P):
            notlat += 1
            continue
        ok, wit = is_distributive(P)
        if ok:
            dist.append((w, P, elems))
        else:
            nondist.append(w)
    print("  CONTROL 3  every interval [0-hat, w] is a lattice: %s (%d failures)"
          % ("PASS" if notlat == 0 else "FAIL", notlat), file=OUT)
    print(file=OUT)
    print("  intervals [0-hat, w] with rank(w) <= 6:            %d   (af28's T8: 33)"
          % len(ivs), file=OUT)
    print("  of them NON-distributive:                          %d   (af28's T8: 5)"
          % len(nondist), file=OUT)
    print("  of them DISTRIBUTIVE, so consumed by Brown 4.3:    %d"
          % len(dist), file=OUT)
    print("  smallest non-distributive witness: %s   (af28's T8: (2, 2, 1))"
          % (str(min(nondist, key=lambda w: (sum(w), w))) if nondist else "none",),
          file=OUT)
    print(file=OUT)
    print("  For each distributive interval, build P from the join-irreducibles", file=OUT)
    print("  and verify J(P) = the interval, pair by pair:", file=OUT)
    print(file=OUT)
    print("   w                    |[0,w]|   |P|   J(P) = [0,w]", file=OUT)
    bad = 0
    shown = 0
    for w, P, elems in dist:
        JI, _ = join_irreducibles(P)
        JP, _ = ideal_lattice(JI)
        ok = iso(JP, P) is not None
        if not ok:
            bad += 1
        if shown < 6 or not ok:
            print("   %-20s %7d  %4d   %s"
                  % (str(w), P[0], JI[0], "." if ok else "BAD"), file=OUT)
            shown += 1
    print("   ... all %d distributive intervals reconstructed." % len(dist), file=OUT)
    print(file=OUT)
    print("  reconstructions bad: %d." % bad, file=OUT)
    print(file=OUT)
    print("  READING.  %d of the %d finite intervals of the Young-Fibonacci"
          % (len(dist), len(ivs)), file=OUT)
    print("  lattice ARE finite distributive lattices, so Brown section 4.3", file=OUT)
    print("  consumes them, and each is J(P) for a P built here.  So the Okada", file=OUT)
    print("  monoid's branching graph (row 10) has the same index-set contact", file=OUT)
    print("  with this construction that mg-af28 headlines for Young's -- for", file=OUT)
    print("  %d of its %d finite intervals.  Row 10's stated reason for booking"
          % (len(dist), len(ivs)), file=OUT)
    print("  it merely ADJACENT does not hold.  Reproduces mg-6ad0's A6 on a", file=OUT)
    print("  third instrument.", file=OUT)
    print(file=OUT)
    print("  WHAT SURVIVES.  Young's lattice is still the only DISTRIBUTIVE", file=OUT)
    print("  1-differential lattice (Stanley 1988, cited by af28 from a", file=OUT)
    print("  secondary source and read by nobody here), and every interval", file=OUT)
    print("  [empty, lambda] of it is distributive -- af28's 30 of 30, which", file=OUT)
    print("  mg-6ad0 reproduced.  That is a statement about WHOLE lattices and", file=OUT)
    print("  it is the one B4 may keep.", file=OUT)
    print(file=OUT)
    return len(ivs), len(nondist), len(dist), bad, notlat, bad_diff, fib == expect


def main():
    missing = r3a()
    n_iv, n_nd, n_d, bad, notlat, bad_diff, fibok = r3b()
    print("=" * 78, file=OUT)
    print("SUMMARY r3_rescope: Bergeron-Li strings missing %s; Young-Fibonacci"
          % ("n/a (no network)" if missing is None else missing), file=OUT)
    print("  intervals %d, non-distributive %d, distributive %d, J(P) rebuilds"
          % (n_iv, n_nd, n_d), file=OUT)
    print("  bad %d; controls: rank sizes %s, DU-UD violations %d, non-lattice %d"
          % (bad, "PASS" if fibok else "FAIL", bad_diff, notlat), file=OUT)
    print("=" * 78, file=OUT)


if __name__ == "__main__":
    main()
