"""THE LIST, AND WHERE THIS AUDIT GOT IT.

mg-a4ef built ONE list as the union of `check_doc.py`'s ten `STRICKEN` rows and
`w3_scope.py`'s two `FORBIDDEN` rows, plus Y2 -- eleven rows.

This file does not take that list.  It takes the DOCUMENT'S OWN `~~strike~~`
spans, which is the only enumeration in this arc that cannot fall behind the
document, because it IS the document.  A worker who strikes a sentence writes
the `~~`; a worker who strikes a sentence and forgets the checker's table does
not write the table row.  `d2_extent.py` compares the two enumerations, and the
comparison is the audit.

The source-side patterns below are hand-written per statement, because a
struck sentence in Markdown and the same statement printed by a Python file are
not the same string -- `K̄(Π)` against `K-bar(Pi)`, `≤` against `<=`.  Written
over the token stream of `kern7dd3.py`, where every non-alphanumeric character
is its own token, so `K-bar(Pi)` is `k - bar ( pi )`.

X8 IS HERE AND IS ON NO OTHER LIST IN THIS ARC EXCEPT mg-73df's `c4_scope.py`.
"""

# id, label, source patterns (token stream), own-negation regex (raw text)
STATEMENTS = [
    ("X1", "§8 C3, the extremal claim",
     [r"smallest witness", r"a < c , b < d"],
     r"3-?ELEMENT\s+CHAIN|3-?chain|smallest\s+is\s+the|NOT\s+the\s+smallest"
     r"|IS\s+a\s+witness|only\s+'smallest'"),

    ("X3", "§0, the five-axiom count",
     [r"every hopf (?:- )?monoid axiom with 0 failures",
      r"passes every hopf (?:- )?monoid axiom",
      r"against every hopf monoid axiom"],
     r"CLOSURE|closure\s+only|two\s+columns|cannot\s+fail|pinned"),

    ("X4", "§2.2, the control count",
     [r"three are controls", r"the three controls",
      r"three of the four (?:columns )?are the control"],
     r"two\s+statements|one\s+control|computed\s+twice"),

    ("X5", "§5, control (ii)'s accounting",
     [r"fires hard", r"measures how differently"],
     r"type\s+mismatch|near[- ]miss|disjoint\s+ground"),

    ("X6a", "§1, the Aguiar-Ardila quotation",
     [r"cut out by inequalities of the form (?:` )?y \( i \) (?:< =|≤) "
      r"y \( j \)"],
     r"y\(i\)\s*>=\s*y\(j\)|direction|reversed|as\s+printed"),

    ("X6b", "§9 row 6, the inequality direction",
     [r"y \( i \) (?:< =|≤) y \( j \)"],
     r"y\(i\)\s*>=\s*y\(j\)|direction|reversed|as\s+printed|BEFORE|AFTER"),

    ("X7", "§4, the AM §17.5 quotation",
     [r"k - bar \( pi \) is the algebra of symmetric functions",
      r"k \( pi \) is the familiar hopf algebra"],
     r"Pi-?\*|misquot|printed\s+it\s+wrong|both\s+slots"),

    ("X2a", "§6 item 6, 'measured, not proved'",
     [r"is measured , not proved"],
     r"corollary|PROVED,\s+in\s+three|three\s+lines|no\s+.?n.?\s+dependence"),

    ("X2b", "§10 item 2, the withdrawn errand",
     [r"read saliola and commins before quoting"],
     r"CLOSED|errand|cancelled|DO\s+NOT\s+FILE"),

    ("X2c", "S12, the withdrawn non-location",
     [r"not located\b.{0,90}in that generality"],
     r"corollary|WITHDRAWN|no\s+gap\s+to\s+locate|is\s+\*?\*?located"),

    # ------------------------------------------------------------------
    # THE ROW mg-a4ef's UNION DOES NOT HAVE.  mg-a61f's X8: the document
    # struck "as three independent agreements about the term" and replaced
    # it with "two sources using the term ... and a third that flags it".
    # It is a `~~strike~~` in the document like the other ten, it is on
    # mg-73df's c4_scope.py list, and it is on NEITHER check_doc.py's
    # STRICKEN NOR w3_scope.py's FORBIDDEN -- so the union of those two
    # does not contain it.
    # ------------------------------------------------------------------
    ("X8", "§1, 'three independent agreements' about 'braid cone'",
     [r"three independent agreements", r"as three independent"],
     r"collision|two\s+sources|flags\s+the\s+term|not\s+a\s+third"),

    ("Y2", "§0, the descent algebra read as an ISOMORPHISM",
     [r"left side is (?:\* \* )?solomon ' s descent algebra"],
     r"anti-?isomorph|opposite\s+algebra|\^\{?op\}?"),
]

# The four trees mg-a4ef declares as its extent, plus the two it declares it
# is silent about.  This audit runs over BOTH sets and reports them apart.
DECLARED_TREES = [
    "species_7d75",
    "species_repair_6f61",
    "species_remainder_f8fa",
    "species_repair_a4ef",
]
SILENT_TREES = [
    "species_audit_a61f",
    "species_audit_73df",
]

DOC = "OneThird-Species-Hopf-Monoids-Where-This-Lives.md"

# mg-a4ef's declared per-file exclusion, verbatim from stricken_a4ef.py.
# Quoted here rather than imported: an audit that imports the list it is
# checking cannot find the list wrong.
A4EF_EXCLUDE = {
    "stricken_a4ef.py",
    "PREDICTIONS.md",
    "OUTCOMES.md",
    "out_c4_scope_73df_after.txt",
    "out_c5_doc_73df_after.txt",
}

# and its file-extension filter, also verbatim
A4EF_EXTENSIONS = (".py", ".txt", ".md")
