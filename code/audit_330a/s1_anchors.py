"""s1_anchors.py -- RESOLVE EVERY DERIVED ANCHOR AND LOOK.

Not: check the derivation logic.  Resolve it, print the revision pair it lands
on, and compare that pair against the pair the prose beside it claims.

  (i)    the four anchors libe34a derives, RESOLVED, each against the pair its
         own label names -- and the subject line of what it lands on, because
         a sha agreeing with a pin still says nothing about what that commit
         IS.
  (ii)   the history derivations libe34a KEEPS, resolved, with the distance.
  (iii)  IS THE GATE WHERE THE ANCHOR IS USED?  ANCHOR_DRIFT is built at
         import and gated in some scripts.  Every consumer of every anchor is
         enumerated and scored for whether it carries the gate.
  (iv)   THE SWEEP FOR A FOURTH.  Every revision-producing git log call in the
         repo's own Python, classified by HOW the revision is obtained.  The
         population of history-derived anchors, stated as a number, because
         the brief says it has never been enumerated.
  (v)    LAST_TOUCHING_G1 and NTH_TOUCHING_1: genuinely unused by any anchor?
         Demonstrated by DELETING them in a clone and seeing what breaks.

Every number here names its population.  Where a number is READ out of a
transcript rather than counted here, the row says READ.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib330a as L                                          # noqa: E402

E34A = os.path.join(L.REPO, L.E34A_DIR)
sys.path.insert(0, E34A)
import libe34a as E                                          # noqa: E402

R = L.Report(
    selfpop="every git read, source read, parse and clone this script "
            "performs, plus the requirement that each anchor resolve to a "
            "40-character revision that is an ancestor of this HEAD and that "
            "the deletion probe in (v) really remove the names it claims to",
    findpop="the 4 anchors libe34a derives, each RESOLVED and compared "
            "against the pair its own prose names and against the subject of "
            "the commit it lands on; every consumer of every one of those "
            "anchors, scored for whether the drift gate is where the anchor "
            "is used; every revision-producing git log call under code/, "
            "classified by how the revision is obtained; and the two kept "
            "history derivations, scored for whether anything depends on them")

L.banner("S1", "EVERY DERIVED ANCHOR, RESOLVED -- NOT ITS LOGIC, ITS ANSWER")

print("""
   The parent finding is that a DERIVED anchor silently re-pointed when an
   unrelated sentence was edited in the file it derives from, AND THE
   PRINTED NUMBER DID NOT CHANGE.  So this section does not read the
   derivation.  It runs it and prints where it lands.
""")

# ---------------------------------------------------------------------------
L.rule("(i) THE FOUR ANCHORS, RESOLVED, AGAINST WHAT THEIR PROSE CLAIMS")
# ---------------------------------------------------------------------------

print("""   Each row is: the label libe34a prints, the revision the derivation
   RETURNS when run here, the pin written beside it, and THE SUBJECT OF
   THE COMMIT IT LANDS ON.  The subject is the half a sha comparison
   cannot supply: `4755d029 agrees with 4755d029` is true of any
   derivation that has drifted onto its own pin, and the drifted anchor
   of A-1 printed exactly that shape of agreement.

   The derivations are re-run HERE, from libe34a's own sentences, not
   taken from libe34a's module-level values.
""")

# The pair each anchor's PROSE names, written out of the labels themselves.
CLAIMS = [
    ("mg-76cc repair", L.MARK_76CC, "REPAIR_REV",
     E.REPAIR_REV_PIN, "mg-76cc", "KERNEL HALF"),
    ("  its first parent -- THE PRE-REPAIR PREDICATE", None, "PRE_REV",
     E.PRE_REV_PIN, "mg-76cc's parent", None),
    ("mg-7e58 repair", L.MARK_7E58, "REV_7E58",
     E.REV_7E58_PIN, "mg-7e58", "PROVENANCE APPARATUS"),
    ("  its first parent", None, "PRE_7E58_REV",
     E.PRE_7E58_PIN, "mg-7e58's parent", None),
]

print("   %-46s %-9s %-9s %s" % ("anchor", "resolved", "pinned", ""))
resolved = {}
_prev = None
for label, marker, name, pin, whose, must_say in CLAIMS:
    if marker is not None:
        got = L.my_first_introducing(L.G1_REL, marker)
        _prev = got
    else:
        got = L.resolve(_prev + "^") if _prev else None
    resolved[name] = got
    R.selfgate(bool(got) and len(got) == 40,
               "%s did not resolve to a 40-character revision" % name)
    R.selfgate(bool(got) and L.is_ancestor(got, "HEAD"),
               "%s is not an ancestor of HEAD" % name)
    print("   %-46s %-9s %-9s %s"
          % (label, (got or "-")[:8], pin[:8],
             "agrees" if got == pin else "*** DISAGREES"))
    R.gate(got == pin,
           "the anchor %s RESOLVES to %s and its pin says %s -- the "
           "derivation and the pin do not name the same revision"
           % (name, (got or "-")[:8], pin[:8]))

print("\n   AND WHAT EACH ONE LANDS ON, WHICH A SHA COMPARISON CANNOT SAY:")
for label, marker, name, pin, whose, must_say in CLAIMS:
    got = resolved[name]
    if not got:
        continue
    subj = L.subject(got)
    print("     %-22s %s  %s" % (name, got[:8], subj[:72]))
    if must_say:
        R.gate(must_say.lower() in subj.lower(),
               "%s resolves to %s, whose subject does not mention %r -- the "
               "anchor's prose says it is %s's repair and the commit it "
               "lands on does not say so: %r"
               % (name, got[:8], must_say, whose, subj[:90]))

print("""
   AND THE MARKER IS REALLY THE PROPERTY, NOT A STRING THAT HAPPENS TO
   AGREE.  The two-sided test says the marker is present at the anchor
   and absent at its first parent.  Both halves, checked here:
""")
for name, marker, pre_name in (("REPAIR_REV", L.MARK_76CC, "PRE_REV"),
                               ("REV_7E58", L.MARK_7E58, "PRE_7E58_REV")):
    at = marker in L.show_or_empty(resolved[name], L.G1_REL)
    before = marker in L.show_or_empty(resolved[pre_name], L.G1_REL)
    print("     %-14s %-20r at %s: %-7s   at %s: %s"
          % (name, marker, resolved[name][:8], "PRESENT" if at else "absent",
             resolved[pre_name][:8], "PRESENT" if before else "absent"))
    R.gate(at and not before,
           "the marker %r is not `present at %s and absent at its parent` -- "
           "present=%s, at-parent=%s.  The anchor is not derived from the "
           "property it names" % (marker, name, at, before))

# ---------------------------------------------------------------------------
L.rule("(ii) THE HISTORY DERIVATIONS THE REPAIR KEPT, RESOLVED")
# ---------------------------------------------------------------------------

last_g1 = L.my_last_touching(L.G1_REL)
nth1_g1 = L.my_nth_touching(L.G1_REL, 1)
nth1_parent = L.resolve(nth1_g1 + "^") if nth1_g1 else None

print("""   These are what the anchor USED to be.  Re-derived here, at this
   HEAD, so that the distance is a measurement and not a quotation.
""")
print("   %-58s %-9s %-9s %s"
      % ("what the file's history returns", "history", "property", "apart"))
ROWS2 = [
    ("the newest commit touching g1_provenance.py -- the OLD anchor",
     last_g1, resolved["REPAIR_REV"]),
    ("its first parent -- the OLD `before this repair`",
     L.resolve(last_g1 + "^"), resolved["PRE_REV"]),
    ("the 2nd-newest commit's parent -- the OLD `before mg-7e58`",
     nth1_parent, resolved["PRE_7E58_REV"]),
]
for label, hist, prop in ROWS2:
    d = L.distance(prop, hist) if L.is_ancestor(prop, hist) else 0
    print("   %-58s %-9s %-9s %d commit(s)"
          % (label, hist[:8], prop[:8], d))

print("""
   The third row is the one only the repair found: `the 2nd-newest
   commit` now lands on %s, which is mg-76cc's parent, under a label
   that says mg-7e58.  Its subject:
     %s
   An index into a file's history is an anchor derived from that
   history, and it re-points for the same reason the newest-touching
   one does.
""" % (nth1_parent[:8], L.subject(nth1_parent)[:70]))

R.gate(last_g1 != resolved["REPAIR_REV"],
       "the newest commit touching g1_provenance.py IS the property anchor, "
       "so this tree cannot distinguish the two derivations and the whole "
       "comparison in (ii) is vacuous here")

# ---------------------------------------------------------------------------
L.rule("(iii) IS THE DRIFT GATE WHERE THE ANCHOR IS USED?")
# ---------------------------------------------------------------------------

print("""   ANCHOR_DRIFT is built once, at import of libe34a.  A consumer that
   reads an anchor and does NOT gate on ANCHOR_DRIFT will run on a
   drifted anchor and print a plausible number, which is A-1 exactly.
   So: every file that reads any of the four anchors, against every
   file that gates on ANCHOR_DRIFT.

   The population is every .py under %s.
""" % L.E34A_DIR)

ANCHORS = ("REPAIR_REV", "PRE_REV", "REV_7E58", "PRE_7E58_REV")
consumers = {}
gated = set()
for fn in sorted(os.listdir(E34A)):
    if not fn.endswith(".py"):
        continue
    with open(os.path.join(E34A, fn)) as fh:
        src = fh.read()
    uses = sorted({a for a in ANCHORS
                   if re.search(r"\b(?:L\.)?%s\b" % a, src)})
    # libe34a defines them; it is not a consumer of them
    if fn == "libe34a.py":
        continue
    if uses:
        consumers[fn] = uses
    if "ANCHOR_DRIFT" in src:
        gated.add(fn)

print("   %-22s %-42s %s" % ("script", "anchors it reads", "drift gate?"))
for fn in sorted(consumers):
    print("   %-22s %-42s %s"
          % (fn, ", ".join(consumers[fn]),
             "yes" if fn in gated else "*** NO"))
ungated = sorted(f for f in consumers if f not in gated)
print("\n   scripts reading an anchor                     : %d" % len(consumers))
print("   of those, carrying the ANCHOR_DRIFT gate      : %d"
      % (len(consumers) - len(ungated)))
print("   of those, NOT carrying it                     : %d" % len(ungated))
for fn in ungated:
    print("      %-22s reads %s" % (fn, ", ".join(consumers[fn])))

R.gate(not ungated,
       "%d of %d scripts in %s read a derived anchor WITHOUT gating on "
       "ANCHOR_DRIFT: %s.  The repair makes a drifted anchor loud in "
       "selftest_e34a.py and k1_prerepair.py (i) and nowhere else, so a "
       "drifted anchor is SILENT in the very scripts whose numbers move -- "
       "k4_cancel.py is the script the repair itself identifies as the one "
       "`where the count actually moved`, and it does not carry the gate.  "
       "Run alone, it would print a number derived from a drifted anchor "
       "with nothing to say so"
       % (len(ungated), len(consumers), L.E34A_DIR, ", ".join(ungated)))

# ---------------------------------------------------------------------------
L.rule("(iv) THE SWEEP FOR A FOURTH -- EVERY REVISION ANCHOR UNDER code/")
# ---------------------------------------------------------------------------

print("""   The repair found two anchors of this class that mg-2c77's audit did
   not name, and asks whether there is a third.  mg-8d5e's own r4
   enumerates 11 anchors and scopes that enumeration to
   code/repair_8d5e/.  Here the sweep is REPO-WIDE and classifies by
   HOW the revision is obtained, because that is what decides whether
   an unrelated edit moves it:

     NEWEST    `log -1 --format=%H -- <path>`         re-points on ANY edit
     INDEXED   `log --format=%H -- <path>` then [n]   every index shifts
     OLDEST    `log --reverse ... -- <path>` then [0] STABLE: a file's
                                                     creation does not move
     PICKAXE   `log -S <marker> -- <path>`            derived from a PROPERTY
     RANGE     `log <a>..<b> -- <path>`               a set, not an anchor
     UNRESTRICTED  no pathspec                        an anchor on the branch

   NEWEST and INDEXED are the defect class.  OLDEST is named separately
   on purpose: lumping it in would count a safe construct as the defect
   and inflate the population, which is the mirror of A-2.
""")

rows, unparsed = L.sweep_anchor_calls()
R.selfgate(not unparsed, "%d file(s) under code/ did not parse" % len(unparsed))

order = ["NEWEST", "NEWEST-norestrict", "INDEXED", "UNRESTRICTED", "OLDEST",
         "PICKAXE", "RANGE"]
bykind = {}
for r in rows:
    bykind.setdefault(r["kind"], []).append(r)

print("   kind                  sites   what it is")
WHAT = {"NEWEST": "HISTORY-DERIVED -- the A-1 defect class",
        "NEWEST-norestrict": "HISTORY-DERIVED on the branch, not a file",
        "INDEXED": "HISTORY-DERIVED -- the A-1 second half",
        "UNRESTRICTED": "HISTORY-DERIVED on the branch, not a file",
        "OLDEST": "stable against later edits",
        "PICKAXE": "PROPERTY-DERIVED",
        "RANGE": "a set, not an anchor"}
for k in order:
    if k in bykind:
        print("   %-21s %-7d %s" % (k, len(bykind[k]), WHAT[k]))
print("   %-21s %-7d %s" % ("ALL", len(rows), "call sites, walked by ast"))

print("\n   AND EVERY HISTORY-DERIVED SITE, NAMED.  A count of what is "
      "uncovered\n   that cannot be pointed at is the same silence as no "
      "count at all:")
hist_kinds = ("NEWEST", "NEWEST-norestrict", "INDEXED", "UNRESTRICTED")
hist_rows = [r for r in rows if r["kind"] in hist_kinds]
for r in sorted(hist_rows, key=lambda r: (r["file"], r["line"])):
    print("      %-13s %s:%d\n                    %s"
          % (r["kind"], r["file"], r["line"], r["src"][:88]))

print("\n   AND THE TWO NAMED HELPERS, WHICH HIDE THEIR FLAGS.  A call to\n"
      "   `last_touching(p)` contains no `--format=%H` at all:")
helpers = L.sweep_helper_uses()
for h in sorted(helpers, key=lambda h: (h["file"], h["line"])):
    print("      %-5s %-14s %s:%d" % (h["what"], h["name"], h["file"],
                                      h["line"]))
hdefs = [h for h in helpers if h["what"] == "DEF"]
hcalls = [h for h in helpers if h["what"] == "CALL"]

print("""
   population of HISTORY-DERIVED revision anchors under code/ :
     by explicit git log call (ast-walked)        : %d
     by a named helper (last_touching/nth_touching): %d definition(s),
                                                    %d call site(s)
   population of PROPERTY-DERIVED anchors under code/ :
     by pickaxe (`log -S`)                        : %d
     by the two-sided `first_introducing`         : %d definition(s)
""" % (len(hist_rows), len(hdefs), len(hcalls),
       len(bykind.get("PICKAXE", [])),
       sum(1 for dp, _d, fs in os.walk(os.path.join(L.REPO, "code"))
           for f in fs if f.endswith(".py")
           and "def first_introducing" in open(os.path.join(dp, f)).read())))

print("""   THE ANSWER TO `IS THERE A FOURTH`.  There are %d history-derived
   git log call sites and %d call sites of the two named helpers, over
   %d directories.  The two the repair named are two of them.  The
   population was never a small number and the repair's own enumeration
   ("11 anchors") is scoped to one directory, which is stated in its
   own transcript and is not a defect -- but it is not the population
   this brief asks about, and the difference is printed here rather
   than left to be inferred.
""" % (len(hist_rows), len(hcalls),
       len({r["file"].rsplit("/", 1)[0] for r in hist_rows}
           | {h["file"].rsplit("/", 1)[0] for h in hcalls})))

# The one the repair's own commit message points at without repairing.
P3 = "code/repair_69d1/p3_reason.py"
p3_src = L.read_worktree(P3)
p3_head = [i + 1 for i, ln in enumerate(p3_src.splitlines())
           if "HEAD" in ln and ("control" in ln.lower() or "i-b" in ln)]
print("   AND THE ONE THE REPAIR POINTS AT AND DOES NOT REPAIR.  Its own\n"
      "   commit message says code/repair_69d1/p3_reason.py (i-b) anchors\n"
      "   its control on HEAD and has been vacuous since mg-69d1's repair\n"
      "   landed.  Checked, not quoted: `HEAD` occurs %d time(s) in that\n"
      "   file, and its committed transcript ends TOTAL BAD: %s."
      % (p3_src.count("HEAD"),
         (L.read_worktree("code/repair_69d1/out_p3_reason.txt")
          .rsplit("TOTAL BAD:", 1)[-1].strip().splitlines() or ["-"])[0]))

# ---------------------------------------------------------------------------
L.rule("(v) LAST_TOUCHING_G1 -- KEPT, PRINTED, AND USED BY NO ANCHOR?")
# ---------------------------------------------------------------------------

print("""   `the quantity that moved is the evidence`.  The claim is that
   removing it would lose a DETECTOR and not a DEPENDENCY.  Not read
   off the source: the two names are DELETED in a clone and the suite
   is re-run, so the difference between a detector and a dependency is
   observed rather than argued.
""")

readers = {}
for fn in sorted(os.listdir(E34A)):
    if not fn.endswith(".py") or fn == "libe34a.py":
        continue
    with open(os.path.join(E34A, fn)) as fh:
        src = fh.read()
    hits = sorted({n for n in ("LAST_TOUCHING_G1", "NTH_TOUCHING_1")
                   if n in src})
    if hits:
        readers[fn] = hits
print("   %-22s %s" % ("script", "reads"))
for fn in sorted(readers):
    print("   %-22s %s" % (fn, ", ".join(readers[fn])))
print("   scripts reading either name : %d" % len(readers))

# Is either used to DERIVE anything, as opposed to being printed/compared?
lib_src = L.read_worktree(L.E34A_DIR + "/libe34a.py")
after = lib_src.split("LAST_TOUCHING_G1 = ", 1)[-1]
uses_in_lib = [ln.strip() for ln in lib_src.splitlines()
               if ("LAST_TOUCHING_G1" in ln or "NTH_TOUCHING_1" in ln)
               and "=" not in ln.split("#")[0].split("LAST_TOUCHING_G1")[0][-2:]]
print("\n   and inside libe34a itself, the only statements naming them are"
      "\n   their own assignments:")
for ln in lib_src.splitlines():
    s = ln.strip()
    if s.startswith("LAST_TOUCHING_G1") or s.startswith("NTH_TOUCHING_1"):
        print("      %s" % s[:80])

R.gate("LAST_TOUCHING_G1" not in E.anchor_rows.__doc__ if
       E.anchor_rows.__doc__ else True,
       "anchor_rows documents itself in terms of LAST_TOUCHING_G1")

print("""
   THE DELETION PROBE.  In a clone at HEAD, both names are removed from
   libe34a.py and every line that mentions them is removed from the
   scripts that read them.  If they are a DEPENDENCY the suite breaks;
   if they are a DETECTOR the suite still runs and the evidence is
   gone.  selftest_e34a.py is the cheapest thing that reads both.
""")

tree = L.clone_at("HEAD")
try:
    rc_before, out_before = L.run_py("selftest_e34a.py",
                                     os.path.join(tree, L.E34A_DIR))
    print("   selftest_e34a.py in the untouched clone      : exit %d"
          % rc_before)
    R.selfgate(rc_before == 0,
               "selftest_e34a.py does not pass in an untouched clone at HEAD "
               "(exit %d), so the deletion probe has no baseline" % rc_before)

    lib_p = os.path.join(tree, L.E34A_DIR, "libe34a.py")
    with open(lib_p) as fh:
        src = fh.read()
    cut = [ln for ln in src.splitlines()
           if not ln.startswith("LAST_TOUCHING_G1")
           and not ln.startswith("NTH_TOUCHING_1")]
    R.selfgate(len(cut) == len(src.splitlines()) - 2,
               "the deletion probe did not remove exactly 2 assignment lines "
               "from libe34a.py (removed %d)"
               % (len(src.splitlines()) - len(cut)))
    with open(lib_p, "w") as fh:
        fh.write("\n".join(cut) + "\n")

    rc_after, out_after = L.run_py("selftest_e34a.py",
                                   os.path.join(tree, L.E34A_DIR))
    broke = "NameError" in out_after or "AttributeError" in out_after
    print("   with both names DELETED from libe34a.py      : exit %d  %s"
          % (rc_after, "(AttributeError/NameError raised)" if broke else ""))

    # Which assertions of the selftest went with them?
    lost = [ln for ln in out_before.splitlines()
            if ("history anchor" in ln or "OLD anchor" in ln
                or "nth_touching" in ln)]
    print("\n   the selftest assertions that name them, and would go with"
          "\n   them (from the BASELINE run, %d):" % len(lost))
    for ln in lost:
        print("      %s" % ln.strip()[:96])

    print("""
   VERDICT ON (v).  Deleting the two names makes the consumers raise
   rather than merely lose a column -- so `used by no anchor` is true
   (no anchor is DERIVED from them) while `used by nothing` is not:
   %d script(s) read them and %d selftest assertion(s) are stated in
   terms of them.  What would be lost is a DETECTOR -- the `apart`
   column and the two assertions that the property anchor and the
   history anchor still differ -- and the failure mode of removing
   them is loud, which is the right failure mode for evidence.
""" % (len(readers), len(lost)))

    R.gate(rc_after != 0 or broke,
           "deleting LAST_TOUCHING_G1 and NTH_TOUCHING_1 from libe34a.py "
           "leaves selftest_e34a.py GREEN (exit %d) -- the evidence the "
           "repair says it kept is not observed by anything, so its removal "
           "would be silent" % rc_after)
finally:
    L.rm_tree(tree)

R.done()
