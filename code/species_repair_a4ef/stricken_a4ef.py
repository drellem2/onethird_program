"""THE ONE LIST.

mg-73df's MAJOR finding, in its own words: *"A checker has two scopes -- what
it reads and what it looks for -- and fixing one reads as fixing both."*

  * `code/species_repair_6f61/check_doc.py` has the FULL list over ONE file.
  * `code/species_remainder_f8fa/w3_scope.py` has a TWO-ITEM list over a
    DIRECTORY.

Between them every file was covered and every statement was covered, and NO
STATEMENT WAS COVERED IN EVERY FILE -- which is how X3, the correction the
whole repair centres on, stayed in force in a committed output inside a run
ending `T6 TOTAL BAD: 0`.

This module is the union of both tables, in one place, with each row carrying
BOTH forms: the exact document sentence (matched against the document, where
it must survive only inside its `~~strike~~`) and the source-code patterns
(matched against every code tree, where it must not be asserted at all).
`s1_extent.py` runs this one list over every target and prints the extent.

ROW Y2 IS NEW AND IS mg-a4ef's OWN.  mg-73df found §0's headline box asserting
the plain isomorphism where five other places in the document, and AM Thm 10.13
as §0 itself quotes it, say ANTI-isomorphic.  It is added here rather than
fixed silently, because a correction that is not on the list is a correction
that recurs -- which is the entire finding above.
"""

# id, label, document sentence (exact, or None), source patterns, and the
# words that say THIS statement no longer holds.  The last field is the
# per-statement half of the exoneration rule and it is not optional: without
# it the file that REFUTES a claim reads as asserting it.  mg-a4ef's first
# version omitted it and reported 14 false positives; see OUTCOMES.md.
CORRECTIONS = [
    ("X1", "§8 C3, the extremal claim",
     "Smallest witness with `AC(P) ≠ Π[n]`: `P = {a<c, b<d}`, "
     "where `ad|bc` has a 2-cycle.",
     [r"[Ss]mallest\s+witness[^.]{0,40}\{?\s*a\s*<\s*c\s*,\s*b\s*<\s*d"],
     r"3-?ELEMENT\s+CHAIN|3-?chain|smallest\s+is\s+the|NOT\s+the\s+smallest"
     r"|IS\s+a\s+witness|only\s+'smallest'"),

    ("X3", "§0, the five-axiom count",
     "it passes every Hopf-monoid axiom with 0 failures on 4 399 basis "
     "elements (T5)",
     [r"every\s+Hopf[- ]?monoid\s+axiom\s+with\s+0\s+failures",
      r"passes\s+every\s+Hopf[- ]?monoid\s+axiom"],
     r"CLOSURE|closure\s+only|two\s+columns|cannot\s+fail|pinned"),

    ("X6a", "§1, the Aguiar–Ardila quotation",
     "Define a braid cone to be a cone in `(ℝ^I)/ℝ^I` cut out by "
     "inequalities of the form `y(i) ≤ y(j)` for `i, j ∈ I`",
     [r"cut\s+out\s+by\s+inequalities\s+of\s+the\s+form\s+`?\s*y\(i\)"
      r"\s*<=\s*y\(j\)"],
     r"y\(i\)\s*>=\s*y\(j\)|direction|reversed|as\s+printed"),

    ("X6b", "§9 row 6, the inequality direction",
     "`y(i) ≤ y(j)`",
     [r"y\(i\)\s*<=\s*y\(j\)"],
     r"y\(i\)\s*>=\s*y\(j\)|direction|reversed|as\s+printed|BEFORE|AFTER"),

    ("X7", "§4, the AM §17.5 quotation",
     "Recall from Section 17.4 that `K̄(Π)` is the algebra of "
     "symmetric functions in noncommuting variables and `K(Π)` is the "
     "familiar Hopf algebra of symmetric functions",
     [r"Recall\s+from\s+Section\s+17\.4\s+that\s+K-?bar\(Pi\)\s+is\s+the\s+"
      r"algebra\s+of\s+symmetric\s+functions"],
     r"Pi-?\*|misquot|printed\s+it\s+wrong|both\s+slots"),

    ("X4", "§2.2, the control count",
     "Three of the four columns are the control, and they fire.",
     [r"three\s+are\s+controls",
      r"the\s+three\s+controls",
      r"three\s+of\s+the\s+four\s+(?:columns\s+)?are\s+the\s+control"],
     r"two\s+statements|one\s+control|computed\s+twice"),

    ("X5", "§5, control (ii)'s accounting",
     "**fires hard**: 1 442 closure, 252 associativity, 11 020 "
     "compatibility failures",
     [r"fires\s+hard",
      r"measures\s+how\s+differently"],
     r"type\s+mismatch|near[- ]miss|disjoint\s+ground"),

    ("X2a", "§6 item 6, 'measured, not proved'",
     "The `Aut(P)`-invariant identity of §2.3 is measured, not proved, and "
     "is stated for `n ≤ 5`.",
     [r"is\s+measured,\s+not\s+proved"],
     # NOT a bare "PROVED": the scan is case-insensitive, so "PROVED" matches
     # inside "not proved" and the sentence exonerates ITSELF.  Caught by
     # selftesta4ef.py section 6, which is why that section exists.
     r"corollary|PROVED,\s+in\s+three|three\s+lines"
     r"|no\s+.?n.?\s+dependence"),

    ("X2b", "§10 item 2, the withdrawn errand",
     "Read Saliola and Commins before quoting §2.3 as anything but a "
     "measurement.",
     [r"Read\s+Saliola\s+and\s+Commins\s+before\s+quoting"],
     r"CLOSED|errand|cancelled|DO\s+NOT\s+FILE"),

    ("X2c", "S12, the withdrawn non-location",
     "The `Aut(P)` form of the radical theorem was **not located** stated "
     "in that generality, and this is the weakest claim here",
     [r"not\s+located[^.]{0,40}in\s+that\s+generality"],
     # likewise NOT a bare "located", which matches inside "not located".
     r"corollary|WITHDRAWN|no\s+gap\s+to\s+locate|is\s+\*?\*?located"),

    ("Y2", "§0, the descent algebra read as an ISOMORPHISM (mg-a4ef)",
     None,
     [r"left\s+side\s+is\s+(?:\*\*)?Solomon's\s+descent\s+algebra"],
     r"anti-?isomorph|opposite\s+algebra|\^\{?op\}?"),
]

# Every row of CORRECTIONS whose document sentence is not None must survive in
# the document ONLY inside a `~~strike~~`.  Y2 has no struck sentence: the
# repair is a word, so the positive form below is what the document must say.
REQUIRED_IN_DOC = [
    ("Y2  §0 states the ANTI-isomorphism the body measures",
     "anti-isomorphic to Solomon's descent algebra"),
    ("Y3  the self-assessment survives in exactly ONE version",
     "THE SAME LIMITATION APPLIES TO §14 ITSELF"),
    ("Y1  the document states which extents the checkers cover",
     "WHICH EXTENTS EACH CHECKER COVERS"),
]

# Statements that must NOT appear in the document at all, struck or not,
# because the passage carrying them was resolved rather than corrected.
GONE_FROM_DOC = [
    # Y2's positive form above is NOT enough on its own: "anti-isomorphic to
    # Solomon's descent algebra" was already in §9 row 8, quoting Saliola, so
    # the positive check passed while §0 still said the opposite.  A positive
    # check that a correction is present is not a check that the error is
    # gone -- which is check_doc.py's own "the negative half is the
    # load-bearing half", re-learned here.
    ("Y2  §0's headline box no longer asserts the plain isomorphism",
     "the left side is **Solomon's descent algebra**"),
    ("Y3  the duplicate copy's miscount of the banner",
     "the five items in the banner at the top"),
    ("Y3  the stale 'if there is one' left standing above §14.3",
     "an eighth defect, if there is one"),
    ("Y4  mg-f8fa's filing described as shelved",
     "a second, shelved filing"),
]

# The trees this one list is run over.  Naming them here is the point: an
# extent that is declared can be checked, and a checker whose extent is not
# declared reads as covering everything.
TREES = [
    "species_7d75",
    "species_repair_6f61",
    "species_remainder_f8fa",
    "species_repair_a4ef",
]

# Files skipped by the scan, NAMED ONE BY ONE rather than pattern-matched: an
# exclusion that is a short list is auditable, an exclusion that is a heuristic
# is a hole.  `s1_extent.py` prints this list in its extent declaration so it
# cannot grow without a reader seeing it.
#
# Note what is NOT here: `out_t6_fock_and_record.txt`.  A committed output that
# quotes a forbidden sentence is exactly the defect this ticket closes, so
# "it is only an output" is not a reason to skip a file.  The three below are
# skipped because their SUBJECT is the list itself -- the list module, the two
# prediction records, and two committed runs of another instrument's controls.
EXCLUDE = {
    "stricken_a4ef.py",              # this list, which is every string
    "PREDICTIONS.md",                # written before the run, never edited
    "OUTCOMES.md",                   # scores it, and quotes what was found
    "out_c4_scope_73df_after.txt",   # mg-73df's detector re-run: its controls
    "out_c5_doc_73df_after.txt",     # quote the strings they search for
}
