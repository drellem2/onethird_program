"""mg-cdd5 selftest -- the library's own behaviour, on synthetic inputs only.

No repo is read here.  s3 tests the instrument against the real corpus; this
tests the pieces against inputs whose right answer is known by construction,
so that a failure in s3 can be attributed.

Exit 1 on any FAIL.
"""
import sys

import lib_cdd5 as L

N = [0, 0]


def check(name, got, want):
    ok = got == want
    N[0 if ok else 1] += 1
    print("  [%s] %-58s got=%r" % ("PASS" if ok else "FAIL", name, got))
    if not ok:
        print("         want=%r" % (want,))


def main():
    L.banner("mg-cdd5 selftest -- library behaviour on synthetic inputs")

    # ---- _normalise -------------------------------------------------------
    print("_normalise -- the link target reduced to a mirror-relative path")
    check("plain ../ link",
          L._normalise("../one_third_width_three/docs/a.md"), ("docs/a.md", None))
    check("deeper ../../ link",
          L._normalise("../../one_third_width_three/step8.tex"),
          ("step8.tex", None))
    check("bare backticked path",
          L._normalise("one_third_width_three/docs/a.md"), ("docs/a.md", None))
    check("with a cited line number",
          L._normalise("../one_third_width_three/docs/a.md:65"), ("docs/a.md", 65))
    check("EN-DASH line range (the corpus's own spelling)",
          L._normalise("one_third_width_three/step8.tex:389–394"),
          ("step8.tex", 389))
    check("hyphen line range",
          L._normalise("one_third_width_three/step8.tex:57-73"),
          ("step8.tex", 57))
    check("em-dash line range",
          L._normalise("one_third_width_three/step8.tex:57—73"),
          ("step8.tex", 57))
    check("directory target keeps its trailing slash",
          L._normalise("one_third_width_three/docs/"), ("docs/", None))
    check("not the mirror at all",
          L._normalise("docs/local.md"), (None, None))
    check("trailing punctuation stripped",
          L._normalise("../one_third_width_three/docs/a.md,"), ("docs/a.md", None))
    print()

    # ---- extract_citations ------------------------------------------------
    print("extract_citations -- md, href and backtick channels")
    md = "supported by [`x`](../one_third_width_three/docs/a.md) at §5 and §5.0'."
    c = L.extract_citations(md, "S.md")
    check("markdown link found", len(c), 1)
    check("  path", c[0].path if c else None, "docs/a.md")
    check("  kind", c[0].kind if c else None, "md")
    check("  sections on the same line", c[0].sections if c else None,
          ["5", "5.0'"])
    check("  source line", c[0].srcline if c else None, 1)

    html = '<a href="../one_third_width_three/docs/b.md">see sec 2.3</a>'
    h = L.extract_citations(html, "twin.html")
    check("html href found", len(h), 1)
    check("  kind", h[0].kind if h else None, "href")
    check("  section from `sec 2.3`", h[0].sections if h else None, ["2.3"])

    tick = "the file `one_third_width_three/scripts/c.py` was run"
    t = L.extract_citations(tick, "d.md")
    check("backticked path found", len(t), 1)
    check("  path", t[0].path if t else None, "scripts/c.py")

    none = "no citation here, just ../one_third/other.md"
    check("non-mirror path not picked up", len(L.extract_citations(none, "e.md")), 0)

    multi = ("line one [`a`](../one_third_width_three/docs/a.md)\n"
             "line two [`b`](../one_third_width_three/docs/b.md)\n")
    m = L.extract_citations(multi, "f.md")
    check("two lines -> two citations", len(m), 2)
    check("  line numbers", [x.srcline for x in m], [1, 2])
    print()

    # ---- dedupe -----------------------------------------------------------
    print("dedupe -- unique on (citing file, citing line, cited path)")
    dup = L.extract_citations(
        "[`a`](../one_third_width_three/docs/a.md) and "
        "`one_third_width_three/docs/a.md` again", "g.md")
    check("same path twice on one line, two channels", len(dup), 2)
    check("  deduped to one row", len(L.dedupe(dup)), 1)
    print()

    # ---- classify ---------------------------------------------------------
    print("classify -- and in particular that MISSING is not a value")
    check("identical", L.classify("x", "x"), L.UNCHANGED)
    check("edited without markers", L.classify("x", "y"), L.CHANGED)
    check("edited WITH a strike marker",
          L.classify("a claim", "~~a claim~~ STRUCK"), L.STRUCK)
    check("absent at both", L.classify(L.MISSING, L.MISSING), L.ABSENT_BOTH)
    check("absent in mirror only", L.classify(L.MISSING, "x"), L.ABSENT_MIRROR)
    check("deleted by tip", L.classify("x", L.MISSING), L.ABSENT_TIP)
    check("empty string is NOT missing", L.classify("", ""), L.UNCHANGED)
    check("empty vs missing", L.classify("", L.MISSING), L.ABSENT_TIP)
    check("marker REMOVED is not a strike",
          L.classify("~~gone~~", "gone"), L.CHANGED)
    check("a directory target is its own class, not CHANGED",
          L.classify("tree A", "tree B", "docs/"), L.DIRECTORY)
    check("DIRECTORY is not a hazard class",
          L.DIRECTORY in L.HAZARD_CLASSES, False)
    check("every absence class IS a hazard class",
          all(k in L.HAZARD_CLASSES for k in
              (L.ABSENT_BOTH, L.ABSENT_MIRROR, L.ABSENT_TIP)), True)
    print()

    # ---- added_markers ----------------------------------------------------
    print("added_markers -- counts only markers the tip GAINED")
    check("two tildes added",
          L.added_markers("a", "~~a~~"), {"~~": 2})
    check("word marker added",
          L.added_markers("a", "a REFUTED"), {"REFUTED": 1})
    check("none added", L.added_markers("~~a~~", "~~a~~"), {})
    check("missing side yields nothing",
          L.added_markers(L.MISSING, "~~a~~"), {})
    print()

    # ---- section_present --------------------------------------------------
    print("section_present -- heading, §-mention and bold forms")
    check("markdown heading", L.section_present("### 5.0' Correction", "5.0'"), True)
    check("prime character variant",
          L.section_present("### 5.0′ Correction", "5.0'"), True)
    check("ascii label finds prime heading",
          L.section_present("### 5.0′ Correction", "5.0′"), True)
    check("section mention", L.section_present("see §5 above", "5"), True)
    check("absent", L.section_present("### 4 Something", "5.0'"), False)
    check("MISSING is not present", L.section_present(L.MISSING, "5"), False)
    check("5 does not match 5.0'",
          L.section_present("### 5.0' only", "5"), False)
    print()

    # ---- section_heading_set ---------------------------------------------
    print("section_heading_set -- for the renumbering question")
    doc = "# 1 A\n## 2.3 B\n### 5.0′ C\nnot a heading 9.9\n"
    check("headings collected", L.section_heading_set(doc), {"1", "2.3", "5.0'"})
    check("MISSING gives the empty set", L.section_heading_set(L.MISSING), set())
    print()

    print("  %d PASS, %d FAIL" % (N[0], N[1]))
    print("== selftest exit: %d ==" % (1 if N[1] else 0))
    return 1 if N[1] else 0


if __name__ == "__main__":
    sys.exit(main())
