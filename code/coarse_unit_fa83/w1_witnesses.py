#!/usr/bin/env python3
"""mg-fa83 — RULES THAT PASS THE CONTROL AND ARE WRONG, BUILT AND RUN RATHER THAN ARGUED.

mg-cda7 measured one control's blind spot by constructing widenings that pass it: `OUT
unmoved` is necessary and was never sufficient, because the in/out split is a proxy over PATHS
guarding a decision about LINES.  Its carry-forward is the general claim — A CONTROL DEFINED
OVER A COARSER UNIT THAN THE THING IT IS GUARDING IS NECESSARY AND CANNOT BE SUFFICIENT — and
the method, which is to build the witnesses instead of arguing.  This arm does that on the
population where a false pass costs a merge: the arms `./build.sh` runs.

EVERY VERDICT HERE IS AN EXECUTION OF THE REAL ARM against a tree it resolves for itself.
Nothing is imported, re-spelled or read out of a committed transcript.

THE THREE THINGS THAT MAKE A WITNESS A MEASUREMENT RATHER THAN AN ASSERTION, and each is a
section below rather than a promise:

  §1  BASE FIDELITY.  The unmutated sandbox must reproduce every arm's real decision.  A
      sandbox that does not is measuring itself.
  §2  THE PAIRED MUST-FIRE.  Every recipe ships a mutation of the same document that the arm
      MUST catch.  Without it, `unmoved` cannot be told from `not running`.
  §3  THE DAMAGE IS A NUMBER, computed from the tree and never from the arm's output.

AND THE IN-SUBJECT SPLIT IS mg-cda7'S OWN IN/OUT COLUMN ONE LEVEL UP.  An arm is blind to a
mutation of a document it was never about, and that is not a defect — it is the base rate.
Each recipe names its TARGET (the arm whose own docstring makes that document its subject) and
the others are reported as CROSS, where a fire is the estate catching what the target could
not.  A recipe is a WITNESS OF THE TARGET when the target is unmoved; it is a WITNESS OF THE
GATE only when nothing else fires either.

EXITS 0 always.  THIS ARM GRADES NOTHING AND MUST NOT.  Every finding here is a property of
somebody else's control, and an arm that went red on them would make this branch red for a
defect it is reporting rather than introducing — mg-e35b's red-on-improvement wearing the
measurement's clothes.  What it exits non-zero for is its own failure to reach a decision.
"""

import os
import re
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_fa83 as L                                              # noqa: E402

W = 92


def rule(ch="-"):
    print(ch * W)


# =======================================================================================
# the recipes
# =======================================================================================
#
# Each is (id, target_arm, document, note, mutate, damage) where `mutate` returns the new text
# of `document` and `damage` returns [(label, value)] measured from (original, mutant).

FILLER = "lorem"


# --- STATE.md -------------------------------------------------------------------------

def m_inflate(text):
    return L.inflate_preserving_words(text)


def d_inflate(orig, mut):
    a, b = L.token_stats(orig), L.token_stats(mut)
    return [("words", "%d -> %d" % (a["words"], b["words"])),
            ("bytes", "%d -> %d  (x%.0f)" % (a["bytes"], b["bytes"],
                                             b["bytes"] / float(a["bytes"]))),
            ("longest token, chars", "%d -> %d" % (a["max_token_chars"], b["max_token_chars"])),
            ("original words surviving", "%.1f%%" % (100 * L.surviving_word_share(orig, mut)))]


LEDGER_HEAD = "### Full ledger"


def state_ledger_block(text):
    """Line numbers of the ledger TABLE — header, separator and rows.  This is the only part
    of STATE.md any gated arm digests at a finer unit than the whole file."""
    lines = text.split("\n")
    keep, inside = [], False
    for i, line in enumerate(lines):
        if line.startswith("### "):
            inside = line.startswith(LEDGER_HEAD)
        if inside and line.startswith("|"):
            keep.append(i)
    return keep


# THE PRESERVED SET FOR R2b, WRITTEN OUT AS PREDICATES AND NOT AS LINE NUMBERS.  It is HAND
# BUILT FROM R2a's OWN FINDINGS — R2a keeps the ledger alone, and the arms that fire on it name
# exactly these lines.  Line numbers would rot on the next edit to STATE.md; a predicate says
# what the estate is actually holding, which is the number §4 reports.
PRESERVE_PREDICATES = (
    ("the ledger table (header, separator, 12 rows)", None),
    ("any line naming docs/FACTS.md", "docs/FACTS.md"),
    ("any line naming docs/CONCEPTS.md", "docs/CONCEPTS.md"),
)


def state_preserved(text, with_pointers=True):
    keep = set(state_ledger_block(text))
    if with_pointers:
        for i, line in enumerate(text.split("\n")):
            for _label, needle in PRESERVE_PREDICATES:
                if needle and needle in line:
                    keep.add(i)
    return sorted(keep)


def m_prose_ledger_only(text):
    return L.replace_words_outside(text, state_ledger_block(text), FILLER)


def m_prose_preserved(text):
    return L.replace_words_outside(text, state_preserved(text), FILLER)


def _d_prose(keeper):
    def damage(orig, mut):
        a, b = L.token_stats(orig), L.token_stats(mut)
        return [("words", "%d -> %d" % (a["words"], b["words"])),
                ("lines held byte-identical", "%d of %d" % (len(keeper(orig)), a["lines"])),
                ("original words surviving",
                 "%.1f%%" % (100 * L.surviving_word_share(orig, mut)))]
    return damage


d_prose_ledger = _d_prose(lambda t: state_ledger_block(t))
d_prose_preserved = _d_prose(lambda t: state_preserved(t))


def m_state_plus_word(text):
    return text + "\nextraword\n"


def d_one_word(orig, mut):
    return [("words", "%d -> %d" % (len(orig.split()), len(mut.split())))]


# --- docs/FACTS.md --------------------------------------------------------------------

SCOPE_RE = re.compile(r"\*\*SCOPE\.\*\*.*?(?=\n\n)", re.S)
KIND_RE = re.compile(r"\*\*KIND\.\*\*\s*`U`")
ENTRY_RE = re.compile(r"^## (F\d+) · ", re.M)


def m_scope_emptied(text):
    return SCOPE_RE.sub("**SCOPE.** n/a", text, count=1)


def d_scope(orig, mut):
    a = SCOPE_RE.search(orig)
    b = SCOPE_RE.search(mut)
    return [("F1 SCOPE, characters", "%d -> %d" % (len(a.group(0)), len(b.group(0)))),
            ("occurrences of `exhaustive` in the file", "%d -> %d"
             % (orig.count("exhaustive"), mut.count("exhaustive"))),
            ("the field is still present", "yes — which is what the arm checks")]


def m_scope_renamed(text):
    return SCOPE_RE.sub(lambda m: m.group(0).replace("**SCOPE.**", "**POPULATION.**", 1),
                        text, count=1)


def d_scope_renamed(orig, mut):
    return [("entries carrying **SCOPE.**", "%d -> %d"
             % (orig.count("**SCOPE.**"), mut.count("**SCOPE.**")))]


FABRICATED = """## F99 · A fabricated entry with every declared field present

**STATEMENT.** Every finite poset satisfies a relation nobody has checked.

**KIND.** `FP` — corroborated.

**SCOPE.** Everything.

**FROM.** mg-fa83, this file's own witness.

**NOT.** No near-miss is claimed.

"""


def _entry_span(text, eid):
    marks = [(m.group(1), m.start()) for m in ENTRY_RE.finditer(text)]
    for i, (name, start) in enumerate(marks):
        if name == eid:
            end = marks[i + 1][1] if i + 1 < len(marks) else len(text)
            return start, end
    raise L.Refusal("docs/FACTS.md has no entry %s" % eid)


def _last_entry(text):
    return [m.group(1) for m in ENTRY_RE.finditer(text)][-1]


def m_count_preserving(text):
    eid = _last_entry(text)
    start, end = _entry_span(text, eid)
    return text[:start] + FABRICATED + text[end:]


def d_count_preserving(orig, mut):
    a = [m.group(1) for m in ENTRY_RE.finditer(orig)]
    b = [m.group(1) for m in ENTRY_RE.finditer(mut)]
    return [("entries", "%d -> %d" % (len(a), len(b))),
            ("removed", ", ".join(sorted(set(a) - set(b))) or "(none)"),
            ("added", ", ".join(sorted(set(b) - set(a))) or "(none)")]


def m_count_moving(text):
    start, end = _entry_span(text, _last_entry(text))
    return text[:start] + text[end:]


def d_count_moving(orig, mut):
    return [("entries", "%d -> %d" % (len(ENTRY_RE.findall(orig)),
                                      len(ENTRY_RE.findall(mut))))]


def m_kind_regraded(text):
    return KIND_RE.sub("**KIND.** `OPEN`", text, count=1)


def d_kind(orig, mut):
    return [("F1's KIND mark", "`U` (proved) -> `OPEN`"),
            ("still a mark the arm recognises", "yes — that is exactly §2's check"),
            ("entries whose mark this changes", "1")]


def m_kind_invented(text):
    return KIND_RE.sub("**KIND.** `ULTRA`", text, count=1)


def d_kind_invented(orig, mut):
    return [("F1's KIND mark", "`U` -> `ULTRA`, which is in no vocabulary")]


# --- docs/CONCEPTS.md -----------------------------------------------------------------

# The §2 row this touches is `alpha(P)` — the quantity Daniel asked about and the reason the
# document exists at all.  Its pointer cell is the last cell of the row.
ALPHA_ROW = re.compile(r"^\| `alpha\(P\)` \|.*\|$", re.M)


def _swap_last_cell(line, new):
    cells = line.strip().strip("|").split("|")
    cells[-1] = " %s " % new
    return "|" + "|".join(cells) + "|"


def m_pointer_dead(text):
    return ALPHA_ROW.sub(lambda m: _swap_last_cell(m.group(0), "`mg-0000`"), text, count=1)


def d_pointer_dead(orig, mut):
    ids = re.findall(r"mg-0000", L.read("STATE.md") + orig)
    return [("the row's pointer", "F6-F7 + two work items -> `mg-0000`"),
            ("occurrences of mg-0000 in STATE.md and this file", str(len(ids))),
            ("it matches the arm's POINTER_RE", "yes — [0-9a-f]{4} is what the rule asks for")]


def m_pointer_gone(text):
    return ALPHA_ROW.sub(lambda m: _swap_last_cell(m.group(0), ""), text, count=1)


def d_pointer_gone(orig, mut):
    return [("the row's pointer cell", "populated -> empty")]


def m_concepts_over(text):
    return text + "\n" + " ".join([FILLER] * 400) + "\n"


RECIPES = (
    # (id, kind, target, document, headline, mutate, damage)
    ("R1", "witness", "e331", L.STATE_REL,
     "STATE.md at the same token COUNT with every token 2 000 characters",
     m_inflate, d_inflate),
    ("R1'", "must-fire", "e331", L.STATE_REL,
     "STATE.md plus one word",
     m_state_plus_word, d_one_word),

    ("R2a", "probe", "9bc2", L.STATE_REL,
     "every non-LEDGER line's words replaced, ledger table byte-identical",
     m_prose_ledger_only, d_prose_ledger),
    ("R2b", "witness", "9bc2", L.STATE_REL,
     "the same, plus the hand-built preserved set §4 prints",
     m_prose_preserved, d_prose_preserved),

    ("R3", "witness", "03cf", L.FACTS_REL,
     "F1's SCOPE body replaced by `n/a` — the field is present and says nothing",
     m_scope_emptied, d_scope),
    ("R3'", "must-fire", "03cf", L.FACTS_REL,
     "F1's SCOPE field RENAMED",
     m_scope_renamed, d_scope_renamed),

    ("R4", "witness", "03cf", L.FACTS_REL,
     "one entry deleted and one fabricated entry added — the count is unmoved",
     m_count_preserving, d_count_preserving),
    ("R4'", "must-fire", "03cf", L.FACTS_REL,
     "one entry deleted and nothing added",
     m_count_moving, d_count_moving),

    ("R5", "witness", "602d", L.CONCEPTS_REL,
     "the `alpha(P)` row points at `mg-0000`, an id no work item has had",
     m_pointer_dead, d_pointer_dead),
    ("R5'", "must-fire", "602d", L.CONCEPTS_REL,
     "the `alpha(P)` row's pointer cell emptied",
     m_pointer_gone, d_pointer_gone),

    ("R6", "witness", "602d", L.CONCEPTS_REL,
     "CONCEPTS.md at the same token COUNT with every token 2 000 characters",
     m_inflate, d_inflate),
    ("R6'", "must-fire", "602d", L.CONCEPTS_REL,
     "CONCEPTS.md plus 400 words",
     m_concepts_over, d_one_word),

    ("R7", "witness", "03cf", L.FACTS_REL,
     "F1 re-graded `U` (proved) -> `OPEN` — a recognised mark, and the wrong one",
     m_kind_regraded, d_kind),
    ("R7'", "must-fire", "03cf", L.FACTS_REL,
     "F1 graded with an invented mark",
     m_kind_invented, d_kind_invented),
)


# =======================================================================================

def run_recipe(workdir, recipe, base, originals):
    """One world: apply the recipe, build the tree, run every arm against it.

    ONE DEFINITION, called by `w1` for its census and by `w0` D5 for its plant, because two
    spellings of `what a world is` drift into a control that grades a world the report no
    longer builds (mg-1344's rule, applied to this directory's own loop).
    """
    (rid, _kind, _target, rel, _headline, mutate, damage) = recipe
    orig = originals[rel]
    mutant = mutate(orig)
    if mutant == orig:
        raise L.Refusal("%s did not change %s — a world that plants nothing grades nothing "
                        "(mg-e331 N13's rule)" % (rid, rel))
    tree = L.build_tree(os.path.join(workdir, rid.replace("'", "p")), {rel: mutant})
    moved, refused, crashed, decisions = [], [], [], {}
    for arm_id, _r, _s, _re in L.ARMS:
        decisions[arm_id], _line = L.decision(arm_id, tree)
        if base is not None and decisions[arm_id] != base[arm_id]:
            moved.append(arm_id)
        if decisions[arm_id][1] == "REFUSED":
            refused.append(arm_id)
        elif decisions[arm_id][1] == "CRASH":
            crashed.append(arm_id)
    return mutant, decisions, moved, refused, crashed, damage(orig, mutant)


def main():
    print("=" * W)
    print("mg-fa83  RULES THAT PASS THE CONTROL AND ARE WRONG")
    print("=" * W)
    print()
    print("The general form of mg-cda7's finding, tested by construction on the arms that")
    print("block a merge.  Every line below is a real arm, executed.")
    print()

    workdir = tempfile.mkdtemp(prefix="fa83-")
    try:
        return run(workdir)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def run(workdir):
    originals = {rel: L.read(rel) for rel in (L.STATE_REL, L.FACTS_REL, L.CONCEPTS_REL)}
    before = L.doc_digests()

    # -----------------------------------------------------------------------------------
    print("§0  THE POPULATION — the arms ./build.sh runs, and which of them are here")
    rule()
    print("  A control that nothing invokes has never told anybody anything (mg-937c measured")
    print("  that: 0 of 150 stale transcripts sit in a directory the gate runs).  So the")
    print("  population is the gate's own suites, and the four below are the ones whose")
    print("  SUBJECT IS A DOCUMENT — the rest read posets, and a mutated markdown file is not")
    print("  a fact about them.  That restriction is this arm's own coarse unit and §5 says so.")
    print()
    for arm_id, rel, subject, _re in L.ARMS:
        print("  %-6s %-52s subject: %s" % (arm_id, rel, subject))
    print()
    print("  NOT EXERCISED, AND NAMED RATHER THAN OMITTED:")
    print("    code/control_gate_724a/gate.py — its decision is a comparison against")
    print("    BASELINE.json's gated fields, and reaching it needs the twin suite's git-valued")
    print("    sections.  This sandbox carries no .git BY CONSTRUCTION, so gate.py REFUSES")
    print("    here (measured: exit 2, `field twin.worklist matched its pattern 0 time(s)`).")
    print("    Its two count-valued fields are read in §6 and are NOT claimed as witnesses.")
    print()

    # -----------------------------------------------------------------------------------
    print("§1  BASE FIDELITY — the sandbox reproduces every arm's real decision")
    rule()
    base_tree = L.build_tree(os.path.join(workdir, "base"), {L.STATE_REL: originals[L.STATE_REL]})
    base, real = {}, {}
    fidelity_ok = True
    for arm_id, _rel, _s, _re in L.ARMS:
        real[arm_id], real_line = L.decision(arm_id, L.ROOT)
        base[arm_id], _ = L.decision(arm_id, base_tree)
        same = real[arm_id] == base[arm_id]
        fidelity_ok &= same
        print("  %-6s real tree exit %d / %-9s sandbox exit %d / %-9s %s"
              % (arm_id, real[arm_id][0], real[arm_id][1], base[arm_id][0], base[arm_id][1],
                 "AGREES" if same else "*** DISAGREES ***"))
        print("         %s" % real_line[:82])
    print()
    if not fidelity_ok:
        print("  REFUSED: the sandbox does not reproduce the real decision, so nothing below")
        print("  is evidence about anything.  This is a hole in THIS arm, not a finding.")
        print()
        print("VERDICT: REFUSED — base fidelity failed.")
        return 2
    print("  4 of 4 agree.  Every `unmoved` below is measured against these.")
    print()

    # -----------------------------------------------------------------------------------
    print("§2  THE WORLDS — each recipe run past ALL FOUR arms")
    rule()
    print("  TARGET is the arm whose own subject is the mutated document.  CROSS is the other")
    print("  three: a fire there is the ESTATE catching what the target could not, and it is")
    print("  why `witness of the target` and `witness of the gate` are two different findings.")
    print()

    results = []
    for recipe in RECIPES:
        (rid, kind, target, rel, headline, _m, _d) = recipe
        orig = originals[rel]
        mutant, decisions, moved, refused, crashed, dmg = run_recipe(workdir, recipe, base,
                                                                    originals)
        results.append((rid, kind, target, rel, headline, decisions, moved, dmg,
                        refused, crashed))

        # A CRASH IS NOT A CATCH.  It moves the decision and blocks the merge, and nothing in
        # it detected anything — so it is subtracted here rather than counted, which is the
        # difference between measuring coverage and measuring fragility.
        detectors = [a for a in moved if a not in crashed]
        t_caught = target in detectors
        cross = [a for a in detectors if a != target]
        if kind == "must-fire":
            grade = ("FIRED" if t_caught else
                     "*** CRASHED, NOT A CATCH ***" if target in crashed else
                     "*** DID NOT FIRE ***")
        elif kind == "probe":
            grade = ("CAUGHT by %s" % ",".join(detectors)) if detectors else "unmoved everywhere"
        else:
            grade = ("CAUGHT by the target" if t_caught else
                     ("WITNESS of %s, CAUGHT by %s" % (target, ",".join(cross))) if cross else
                     "WITNESS — nothing in this population caught it")
        note = []
        if refused:
            note.append("%s REFUSED — a designed default-deny, and it blocks" % ",".join(refused))
        if crashed:
            note.append("%s CRASHED — blocks, detects nothing, not counted as a catch"
                        % ",".join(crashed))

        print("  %-4s %-9s target %-5s  %s" % (rid, kind, target, headline))
        for label, value in dmg:
            print("         %-34s %s" % (label + ":", value))
        print("         %-34s %s" % ("arms:", "  ".join(
            "%s %-7s%s" % (a, decisions[a][1] if a in refused + crashed else
                           ("MOVED" if a in moved else "still"),
                           "*" if a == target else " ") for a, _r, _s, _re in L.ARMS)))
        print("         %-34s %s" % ("READS:", grade))
        for n in note:
            print("         %-34s %s" % ("", n))
        print()

    # -----------------------------------------------------------------------------------
    print("§3  THE VERDICT, AND THE BASE RATE IT IS READ AGAINST")
    rule()
    def detectors(r):
        return [a for a in r[6] if a not in r[9]]

    witnesses = [r for r in results if r[1] == "witness"]
    passing = [r for r in witnesses if r[2] not in detectors(r)]
    gatewide = [r for r in passing if not detectors(r)]
    caught = [r for r in witnesses if r[2] in detectors(r)]
    fires = [r for r in results if r[1] == "must-fire"]
    fired = [r for r in fires if r[2] in detectors(r)]

    for rid, kind, target, rel, headline, _d, moved, _dm, ref, crash in results:
        if kind != "witness":
            continue
        det = [a for a in moved if a not in crash]
        if target in det:
            verdict = "CAUGHT by its target (%s)" % target
        elif det:
            verdict = "passes %s, caught by %s" % (target, ",".join(det))
        else:
            verdict = "PASSES EVERY ARM"
        print("    %-4s %-5s %-44s %s" % (rid, target, headline[:44], verdict))
    print()
    print("  %d candidate witnesses were built, over %d documents and %d independently written"
          % (len(witnesses), 3, len(L.ARMS)))
    print("  arms.  %d PASS their target arm: its own decision is unmoved and the tree is wrong"
          % len(passing))
    print("  by the numbers §2 prints.  %d was CAUGHT BY ITS TARGET, and that number is why the"
          % len(caught))
    print("  others are worth reading — a search that found a witness everywhere would be")
    print("  measuring its own permissiveness, which is mg-cda7's `6 of the 13 gain nothing at")
    print("  all` doing the same job for the same reason.")
    print()
    print("  %d pass EVERY arm in this population.  For those, no control the merge gate runs"
          % len(gatewide))
    print("  over these documents distinguishes the mutated tree from the real one.")
    print()
    print("  %d of %d must-fire pairs FIRED on their target.  A pair that did not fire would"
          % (len(fired), len(fires)))
    print("  mean the sandbox is not exercising that arm and its witness is worth nothing.")
    if len(fired) != len(fires):
        print()
        print("  ⚠ NOT EVERY PAIR FIRED.  The witnesses whose pair is silent are NOT claims.")
    print()

    # -----------------------------------------------------------------------------------
    print("§3b  THE ONE THAT WAS CAUGHT IS THE REMEDY, AND IT COSTS NOTHING TO COPY")
    rule()
    print("  R1 and R6 ARE THE SAME RECIPE on two documents — same token count, every token")
    print("  2 000 characters — and they come back opposite ways.  `ratchet.py` is GREEN;")
    print("  `c0_concept_discipline.py` REFUSES at exit 2 and blocks the merge.")
    print()
    print("  The difference is one design decision, and it is already written down in the arm")
    print("  that has it.  c0 locates its sections by ANCHOR PHRASES and says:")
    print()
    print("      \"If a heading is reworded the anchor is not found and this arm REFUSES")
    print("       (exit 2) rather than passing -- a rename must be LOUD.  It cannot be")
    print("       silent-green, because a gate that quietly stops checking is worse than no")
    print("       gate: it is a gate people believe in.\"")
    print()
    print("  THAT IS A DEFAULT-DENY ON THE DOCUMENT'S SHAPE, and it is what turns a")
    print("  count-valued control into one that cannot be passed by a document that is no")
    print("  longer the document.  The ratchet has no such check: `measure()` computes")
    print("  `bytes`, `lines`, `max_line_chars` and `lines_over_2000` and `verdict()` reads")
    print("  ONLY `words`, so the four finer numbers are on the transcript and gate nothing.")
    print()
    print("  So the remedy this branch would propose is not new machinery: it is c0's rule at")
    print("  e331's site.  IT IS NOT MADE HERE — that is a rewrite of another directory's arm,")
    print("  its transcript and its PREDICTIONS, and a demonstration binding by the back door")
    print("  is not a demonstration (mg-585e).  It is exhibited, priced at one predicate, and")
    print("  handed to that arm's owner.")
    print()

    # -----------------------------------------------------------------------------------
    print("§4  WHAT THE MERGE GATE ACTUALLY HOLDS IN STATE.md, AS A NUMBER")
    rule()
    st = originals[L.STATE_REL]
    stats = L.token_stats(st)
    kept = state_preserved(st)
    ledger = state_ledger_block(st)
    print("  R2b is the recipe that says this, and the preserved set is the answer: it is the")
    print("  set of lines that had to be held byte-identical for every arm to stay green.")
    print()
    print("  STATE.md                       %d lines, %d words" % (stats["lines"], stats["words"]))
    print("  the ledger table               %d lines" % len(ledger))
    for label, needle in PRESERVE_PREDICATES:
        if needle:
            n = sum(1 for l in st.split("\n") if needle in l)
            print("  %-30s %d lines" % (label[:30], n))
    print("  PRESERVED SET, total           %d lines of %d  (%.1f%%)"
          % (len(kept), stats["lines"], 100.0 * len(kept) / stats["lines"]))
    held_words = sum(len(l.split()) for i, l in enumerate(st.split("\n")) if i in set(kept))
    print("  words inside it                %d of %d  (%.1f%%)"
          % (held_words, stats["words"], 100.0 * held_words / stats["words"]))
    print()
    print("  So %d of STATE.md's %d words are outside every fine-unit check the merge gate"
          % (stats["words"] - held_words, stats["words"]))
    print("  performs, and R2b is a tree in which all of them are the word `%s`." % FILLER)
    print("  The ratchet sees the COUNT and the twin sees the LEDGER ROWS; the complement is")
    print("  guarded by neither, and that complement is the majority of the document.")
    print()

    # -----------------------------------------------------------------------------------
    print("§5  WHAT THIS ARM CANNOT SEE — its own coarser unit")
    rule()
    print("  1  THE POPULATION IS FOUR ARMS, chosen because their subject is a document.  A")
    print("     gated arm that reads one of these files incidentally is invisible here.  That")
    print("     is the same proxy-over-a-coarser-unit this arm is about, in this arm.")
    print("  2  NO .git, so every git-valued decision is out of reach: twin_pin section 7")
    print("     grades itself REPORTED, NOT GRADED here, and gate.py refuses outright.  A")
    print("     witness that a git-valued section would catch would still read as a witness.")
    print("  3  `WRONG` IS THIS BRANCH'S READING.  §3's damage columns are numbers, but that")
    print("     an emptied SCOPE or an `mg-0000` pointer is a DEFECT is a judgement — the same")
    print("     one OWNERS.json makes about `cause`, and it declares that nothing checks it.")
    print("  4  A recipe that no arm catches may still be caught by a person reading the diff.")
    print("     Every witness here is loud in `git diff`.  What it is not is BLOCKED, and the")
    print("     difference is mg-be37's: a detector with no addressee and one that never fired")
    print("     are indistinguishable, and so are a reviewer who reads and one who does not.")
    print("  5  THIS TRANSCRIPT'S OWN HEADLINE IS A COUNT, which is §6's defect in §3.  `%d of"
          % len(passing))
    print("     %d pass` is unmoved by a recipe DELETED and a weaker one ADDED, exactly as"
          % len(witnesses))
    print("     `twin.mutations_total` is.  What stops it here is that the table above prints")
    print("     the SET — every recipe by id, headline and verdict — so the count is a summary")
    print("     of something a reader can re-read rather than the record itself.  That is the")
    print("     only remedy this directory found for a count, and it is not a check.")
    print("  6  A MUST-FIRE PAIR PROVES THE ARM RUNS, NOT THAT IT IS SENSITIVE TO THE WITNESS'S")
    print("     KIND OF CHANGE.  Each pair moves a check of the same arm; none of them is")
    print("     evidence that the arm could in principle have seen its partner.  It closes")
    print("     `the sandbox is not exercising this arm` and nothing wider.")
    print()

    # -----------------------------------------------------------------------------------
    print("§6  THE ONE THE ESTATE ALREADY NAMED, READ AND NOT WITNESSED")
    rule()
    print("  code/control_gate_724a/BASELINE.json gates two INTEGERS over the twin's negative")
    print("  control — `twin.mutations_caught` and `twin.mutations_total` — and the second")
    print("  exists because of this exact shape.  Its own `why`, quoted:")
    print()
    print("      \"Gated because a mutation quietly deleted is coverage quietly removed, and")
    print("       it would otherwise be invisible: 16 of 16 caught reads exactly like 17 of 17.\"")
    print()
    print("  THE REMEDY IS THE SAME KIND OF ARTIFACT AS THE DEFECT: a count was guarded by")
    print("  adding a second count, so a mutation DELETED and a different one ADDED moves")
    print("  neither field.  That is mg-cda7's `gains lines, OUT unmoved` letter for letter,")
    print("  on the file that gates the gate.")
    print()
    print("  IT IS READ AND NOT WITNESSED, AND THE DIFFERENCE IS THE WHOLE POINT OF THIS")
    print("  DIRECTORY, so it is labelled rather than dressed up as a result: exercising it")
    print("  needs gate.py, gate.py needs the twin suite's git-valued sections, and this")
    print("  sandbox has no git.  It is the sharpest instance in the estate and it is the one")
    print("  this arm could not build.  Filed forward rather than claimed.")
    print()

    print("§7  THE REAL WORKING TREE, BEFORE AND AFTER")
    rule()
    print("  Every arm above ran against a tree of symlinks into the corpus, so an arm that")
    print("  WROTE would write the real file.  The claim that none did is checked here rather")
    print("  than intended (`w0` D9 checks the same thing over its own worlds).")
    print()
    after = L.doc_digests()
    for rel in L.GUARDED_DOCS:
        print("  %-34s %s -> %s   %s" % (rel, before[rel], after[rel],
                                         "UNMOVED" if before[rel] == after[rel] else "*** MOVED ***"))
    print()
    if before != after:
        print("VERDICT: REFUSED — this arm moved the corpus it was measuring.")
        return 2

    rule("=")
    if not gatewide:
        print("VERDICT: %d of %d candidate witnesses PASS their target arm; %d were CAUGHT by it."
              % (len(passing), len(witnesses), len(caught)))
        print("None passed every arm in this population — the estate caught what each target")
        print("could not, which is a stronger result for the estate than for the claim.")
    else:
        print("VERDICT: %d of %d candidate witnesses PASS their target arm; %d caught by its"
              % (len(passing), len(witnesses), len(caught)))
        print("own target, and %d pass EVERY document arm the merge gate runs.  `The control did"
              % len(gatewide))
        print("not move` is necessary and is not sufficient, on this estate, by construction.")
    rule("=")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except L.Refusal as exc:
        print()
        print("REFUSED: %s" % exc)
        print("VERDICT: REFUSED — this arm did not reach its own decision.")
        sys.exit(2)
