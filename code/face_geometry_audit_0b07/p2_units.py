"""mg-0b07 p2 -- THE 8 OF 11, RE-MEASURED, AND THE SPECIMEN CHECKED FOR FIDELITY.

The subject keeps mg-9220's eleven WRITTEN declarations verbatim and measures
them against the patches they were written for, reporting 8 of 11 understating.
Three things have to be true for that to be evidence and not a quotation:

  1. the sentences really are mg-9220's, not a transcription of them;
  2. the patches really are mg-9220's, not today's narrowed ones;
  3. the triple beside each sentence -- what the sentence CLAIMS to remove -- is
     a reading of English, and the subject quotes mg-c4c8's reading rather than
     making one.  A quoted reading is a borrowed premise.

So mg-9220's own `d2_deletion.py` is read out of `b6bc2ef` and its `UNITS` table
reconstructed by executing that file's assignments, the sentences and patches
compared byte for byte with the subject's copies, and every sentence read AGAIN
here, by this auditor, before anything is measured.  The measurement itself uses
this audit's own census.

AND THE DIRECTION IS COMPUTED.  "Understates" is a claim about which way the
difference goes.  The subject's verdict column is `"exact" if got == reading
else "*** UNDERSTATES ***"` -- a binary that names a direction it never
measures.  Here each row is scored AGREES / UNDERSTATES / OVERSTATES / MIXED
from the componentwise comparison, and the subject's own expression is then run
on an overstating pair to see what it would say.
"""

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "face_geometry_instr_5f9a"))

from kern0b07 import (                                          # noqa: E402
    BAR, INSTR, REPO, apply_edits, census, claim, finding, head, report,
    source_at,
)

# The ONE import from the subject, and it is the table under audit.  Every
# number below is computed here; nothing is taken from `kern5f9a`.
import d2_deletion as SUBJ                                      # noqa: E402

MG9220 = "b6bc2ef"

# WHICH TREE EACH OF mg-9220's ELEVEN PATCHES WAS APPLIED TO, read out of its
# own `main()` rather than assumed: BEFORE-* against the pre-repair pin, AFTER-*
# against its own tree, R* against the two-return pin.
REF_OF = {"BEFORE-1": SUBJ.PRE_REPAIR_REF, "BEFORE-2": SUBJ.PRE_REPAIR_REF,
          "AFTER-1": MG9220, "AFTER-2": MG9220, "AFTER-3": MG9220,
          "AFTER-4": MG9220, "AFTER-5": MG9220, "AFTER-6": MG9220,
          "R1": SUBJ.TWO_RETURN_REF, "R2": SUBJ.TWO_RETURN_REF,
          "R3": SUBJ.TWO_RETURN_REF}

# THIS AUDITOR'S OWN READING of mg-9220's eleven sentences, written down before
# any of them was measured, and deliberately WITHOUT looking at the triple the
# subject carries beside them.  The question each row answers is: what would
# this sentence have to remove for it to be exact?  (returns, other statements,
# boolean clauses).
MY_READING = {
    # "one CLAUSE of a compound condition; the `return` it guards stays"
    "BEFORE-1": (0, 0, 1),
    # "one `return` statement -- the magnitude gate"
    "BEFORE-2": (1, 0, 0),
    "AFTER-1": (1, 0, 0),
    "AFTER-2": (1, 0, 0),
    # "NO statement: the ORDER of two gates, both returns kept"
    "AFTER-3": (0, 0, 0),
    # "one statement, and not a `return`: the `signs_read += 1` counter"
    "AFTER-4": (0, 1, 0),
    "AFTER-5": (1, 0, 0),
    "AFTER-6": (1, 0, 0),
    "R1": (1, 0, 0),
    "R2": (1, 0, 0),
    # "TWO `return` statements -- the PAIR"
    "R3": (2, 0, 0),
}


def units_of_mg9220():
    """mg-9220's `UNITS` table, reconstructed from its own committed source.

    The subject keeps a copy of these sentences and of four of these patches.
    A copy is a second statement of the same thing, so it is checked against
    the original rather than trusted -- which is the subject's own argument for
    deleting `returns_removed`, applied to the specimen it kept.
    """
    src = source_at(MG9220, "d2_deletion.py", "face_geometry_instr_5f9a")
    ns = {}
    for node in ast.parse(src).body:
        if not isinstance(node, ast.Assign):
            continue
        try:
            exec(compile(ast.Module([node], []), "<mg9220>", "exec"), ns)
        except Exception:                                       # noqa: BLE001
            continue
    if "UNITS" not in ns:
        raise SystemExit("could not reconstruct mg-9220's UNITS")
    return [(tag, [edit], sentence) for tag, edit, sentence in ns["UNITS"]]


def direction(reading, got):
    if got == reading:
        return "AGREES"
    ge = all(g >= r for g, r in zip(got, reading))
    le = all(g <= r for g, r in zip(got, reading))
    if ge:
        return "UNDERSTATES"
    if le:
        return "OVERSTATES"
    return "MIXED"


def main():
    print(BAR)
    print("mg-0b07 p2 -- the eleven written declarations, re-measured here")
    print(BAR)
    print("\nPREDICTIONS, registered before these runs (PREDICTIONS.md p2):")
    print("   p2.1  my reading agrees with mg-c4c8's quoted triples 11 of 11")
    print("   p2.2  8 UNDERSTATE, 3 AGREE, 0 OVERSTATE")
    print("   p2.3  sentences byte-identical to b6bc2ef's on 11 of 11")
    print("   p2.4  patches identical on 10 of 11; R3 differs in FORM, "
          "identical in EFFECT")
    print("   p2.5  the subject's verdict expression, fed an OVERSTATING pair, "
          "prints UNDERSTATES\n")

    orig = units_of_mg9220()
    head("1.  IS THE SPECIMEN THE SPECIMEN?  mg-9220's own file, at b6bc2ef")
    print("The subject's argument for deleting `returns_removed` is that two "
          "statements of\none number are two things that can disagree.  It then "
          "kept a COPY of mg-9220's\neleven sentences and of four of its "
          "patches.  Same argument, same treatment.\n")
    print("   %-9s %-12s %-12s %s"
          % ("tag", "sentence", "patch", "note"))
    sent_ok = patch_ok = 0
    notes = []
    subj_sent = {t: s for t, _r, s in SUBJ.UNITS_AS_SHIPPED}
    for tag, edits, sentence in orig:
        s_same = subj_sent.get(tag) == sentence
        sent_ok += s_same
        subj_edits = SUBJ.SHIPPED_PATCHES.get(
            tag, [e for n, _r, _f, es, _a in
                  [(m[0], m[1], m[2], m[3], m[4]) for m in SUBJ.MUTATIONS]
                  if n == tag for e in [es]][0])
        p_same = subj_edits == edits
        patch_ok += p_same
        note = ""
        if not p_same:
            note = ("%d edit(s) here vs %d there"
                    % (len(subj_edits), len(edits)))
            notes.append((tag, subj_edits, edits))
        print("   %-9s %-12s %-12s %s"
              % (tag, "identical" if s_same else "*** DIFFERS ***",
                 "identical" if p_same else "*** DIFFERS ***", note))
    claim("mg-9220's eleven sentences are kept VERBATIM: %d of %d byte-"
          "identical to the text at %s" % (sent_ok, len(orig), MG9220),
          sent_ok == len(orig),
          "a sentence retyped, reflowed or tidied in the copy.  The whole "
          "value of a specimen is that it is the thing itself; a paraphrase of "
          "a declaration being measured for exactness is worth nothing",
          "%d of %d identical" % (sent_ok, len(orig)))

    # R3's form: two edits here, one concatenated anchor there.  Same effect?
    r3_here = SUBJ.SHIPPED_PATCHES.get(
        "R3", [m[3] for m in SUBJ.MUTATIONS if m[0] == "R3"][0])
    r3_there = [e for t, es, _s in orig if t == "R3" for e in es]
    src_r3 = source_at(REF_OF["R3"])
    same_effect = (apply_edits(src_r3, r3_here)
                   == apply_edits(src_r3, r3_there))
    claim("ten of the eleven patches are identical as text; R3 is written as "
          "%d edit(s) here and %d there, and the two produce a BYTE-IDENTICAL "
          "mutated tree" % (len(r3_here), len(r3_there)),
          patch_ok == len(orig) - 1 and same_effect,
          "a patch the copy narrowed, widened or moved.  The subject's whole "
          "claim is about mg-9220's work, so a copy that measures today's "
          "patches would report this commit's improvement as mg-9220's defect. "
          " R3's two forms are checked by APPLYING both, not by comparing "
          "their text",
          "identical as text: %d of %d; R3 same effect: %s; differing: %s"
          % (patch_ok, len(orig), same_effect,
             ", ".join(t for t, _a, _b in notes) or "none"))

    head("2.  THE READING -- made here, then compared with the one quoted")
    print("The triple beside each sentence is what the sentence would have to "
          "remove for the\ndeclaration to be exact.  It is a reading of "
          "English, and the subject QUOTES\nmg-c4c8's rather than making one -- "
          "a borrowed premise carrying the conclusion.\nSo each sentence is "
          "read again here, and the two readings are compared.\n")
    print("   %-9s %-10s %-10s %s" % ("tag", "mine", "quoted", "agree"))
    agree = 0
    for tag, _e, sentence in orig:
        quoted = dict((t, r) for t, r, _s in SUBJ.UNITS_AS_SHIPPED)[tag]
        mine = MY_READING[tag]
        agree += (mine == quoted)
        print("   %-9s %-10s %-10s %s"
              % (tag, "%d/%d/%d" % mine, "%d/%d/%d" % quoted,
                 "yes" if mine == quoted else "*** NO ***"))
    claim("the reading made here and the reading the subject quotes agree on "
          "%d of %d.  The conclusion below does not rest on mg-c4c8's reading"
          % (agree, len(orig)),
          agree == len(orig),
          "a sentence whose plain reading is genuinely contested -- at which "
          "point the 8 of 11 is a statement about a reading and has to be "
          "reported as one.  Two independent readings agreeing is the most "
          "this question admits of; it is not a proof and is not offered as one",
          "%d of %d agree" % (agree, len(orig)))

    head("3.  THE MEASUREMENT -- this audit's census, mg-9220's patches")
    print("   %-9s %-10s %-10s %-12s %s"
          % ("tag", "written", "measured", "verdict", "nodes"))
    tally = {"AGREES": [], "UNDERSTATES": [], "OVERSTATES": [], "MIXED": []}
    for tag, edits, _s in orig:
        src = source_at(REF_OF[tag])
        d = census(src)
        m = census(apply_edits(src, edits))
        got = (d.returns - m.returns, d.statements - m.statements,
               d.clauses - m.clauses)
        verdict = direction(MY_READING[tag], got)
        tally[verdict].append(tag)
        print("   %-9s %-10s %-10s %-12s %d"
              % (tag, "%d/%d/%d" % MY_READING[tag], "%d/%d/%d" % got, verdict,
                 d.nodes - m.nodes))
    claim("RE-MEASURED FROM mg-9220's OWN PATCHES BY THIS AUDIT'S OWN CENSUS: "
          "%d UNDERSTATE, %d AGREE, %d OVERSTATE, %d MIXED.  Understating: %s. "
          " Agreeing: %s"
          % (len(tally["UNDERSTATES"]), len(tally["AGREES"]),
             len(tally["OVERSTATES"]), len(tally["MIXED"]),
             ", ".join(tally["UNDERSTATES"]), ", ".join(tally["AGREES"])),
          len(tally["UNDERSTATES"]) == 8 and len(tally["AGREES"]) == 3
          and not tally["OVERSTATES"] and not tally["MIXED"],
          "any of the eleven patches or sentences changing, or this audit's "
          "census disagreeing with the subject's.  The subject reports the "
          "same 8 of 11 from different code; two censuses agreeing on eleven "
          "patches is what makes the figure a measurement rather than a "
          "quotation",
          "per tag: %s"
          % "; ".join("%s %s" % (k, ", ".join(v) or "-")
                      for k, v in tally.items() if v))

    head("4.  THE VERDICT COLUMN NAMES A DIRECTION IT DOES NOT MEASURE")
    print("The subject's column is a binary on equality.  Fed a declaration "
          "that OVERSTATES\nits patch -- says it removes more than it does -- "
          "it prints the same word.  The\nsubject's own expression is lifted "
          "out of its source and RUN here on such a pair,\nrather than argued "
          "about.\n")
    d2src = open(os.path.join(INSTR, "d2_deletion.py")).read()
    ifexp = None
    for node in ast.walk(ast.parse(d2src)):
        if (isinstance(node, ast.IfExp)
                and isinstance(node.body, ast.Constant)
                and node.body.value == "exact"):
            ifexp = node
    if ifexp is None:
        raise SystemExit("could not locate the subject's verdict expression")
    expr = compile(ast.Expression(ifexp), "<subject>", "eval")
    over = eval(expr, {}, {"got": (0, 0, 0), "reading": (1, 0, 0)})
    under = eval(expr, {}, {"got": (1, 1, 0), "reading": (1, 0, 0)})
    exact = eval(expr, {}, {"got": (1, 0, 0), "reading": (1, 0, 0)})
    print("   reading 1/0/0, measured 0/0/0 (OVERSTATES) -> %r" % over)
    print("   reading 1/0/0, measured 1/1/0 (UNDERSTATES) -> %r" % under)
    print("   reading 1/0/0, measured 1/0/0 (AGREES)      -> %r" % exact)
    if over == under:
        finding("A2",
                "THE SUBJECT'S VERDICT COLUMN ASSERTS A DIRECTION IT NEVER "
                "MEASURES: its own expression, run here, prints %r for a "
                "declaration that OVERSTATES its patch as well as for one that "
                "understates it, and the claim beside the table says "
                "'UNDERSTATE THEIR OWN PATCHES ON 8 OF 11' from a set built by "
                "`r[1] != r[2]`." % over,
                "It happens to be right about all eight -- re-measured "
                "independently above, 8 UNDERSTATE and 0 OVERSTATE -- so the "
                "figure stands and this is a defect of the instrument and not "
                "of the finding.  It matters because the direction is the whole "
                "content of the word: a declaration that OVERSTATES its patch "
                "makes the evidence look COARSER than it is, which is harmless, "
                "and one that understates makes it look finer, which is what "
                "mg-c4c8 found.  A column that cannot tell them apart cannot "
                "report the next one.")
    claim("the subject's verdict expression is a binary on equality: it prints "
          "%r for exact and %r for BOTH directions of inexact -- located in its "
          "source by shape and evaluated here, not paraphrased"
          % (exact, over),
          exact == "exact" and over == under and over != exact,
          "the column being computed from the componentwise comparison, which "
          "is what would let it name the direction.  This claim goes red the "
          "moment the subject distinguishes the two -- which is the repair",
          "over=%r under=%r exact=%r" % (over, under, exact))
    return report()


if __name__ == "__main__":
    sys.exit(main())
