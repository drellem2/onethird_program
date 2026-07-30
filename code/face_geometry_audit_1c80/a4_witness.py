"""mg-1c80 part 4 -- THE WITNESS, AND WHETHER THE CONDITION MOVED.

Two questions the brief puts in the same breath, because a repair can fail
either way round:

  1. mg-8a12 cited NEGATIVE CONTROL 3's facet-parity gauge as the witness that
     ROW I4 IS FALSIFIABLE.  mg-da45 says that gauge is `D.L.D` BY CONSTRUCTION,
     so it cannot be that witness.  Verified here by EXHIBITING the sign vector,
     not by asking the predicate -- "the predicate says True" is the weaker
     statement and is the one the old text leaned on.
     Then: does the repair install a REPLACEMENT witness?  A replacement that is
     also absorbable by construction is the same defect with a new name.

  2. Did the repair change the CONDITION?  It was forced and correct; only the
     printed reason was false, and a repair that weakens or removes row I4 has
     over-corrected.  Checked mechanically: `controls.py` is parsed at HEAD and
     at HEAD~1, every STRING LITERAL AND COMMENT is deleted, and what is left is
     diffed.  Prose is invisible to that diff; a moved condition is not.
"""

import ast
import difflib
import io
import subprocess
import sys
import tokenize

sys.path.insert(0, "../face_geometry")

from posets import all_posets                                        # noqa: E402
from kern1c80 import (absorbable_2col, eq, gate_priority, parity_gauge,
                      target, twisted)                               # noqa: E402

BAR = "=" * 78
CONTROLS = "../face_geometry/controls.py"
ps = [P for n in range(2, 6) for P in all_posets(n)]

print(BAR)
print("mg-1c80 part 4 -- the witness, and whether the condition moved")
print(BAR)
print()

# ---------------------------------------------------------------------------
print("1. NC3's PARITY GAUGE IS ABSORBABLE **BY CONSTRUCTION**")
print()
print("   Claim under audit: 'NC3's corruption is D.L.D by construction, so its")
print("   magnitudes ARE the target's'.  Tested by exhibiting s and checking")
print("   s_i . A_ij . s_j == B_ij entry by entry -- no predicate consulted.")
print()
exhibited = bites = mag_same = pred_true = 0
for P in ps:
    Lp, tg = parity_gauge(P), target(P)
    m = len(Lp)
    s = [1 if j % 2 == 0 else -1 for j in range(m)]
    if all(s[i] * Lp[i][j] * s[j] == tg[i][j] for i in range(m) for j in range(m)):
        exhibited += 1
    if not eq(Lp, twisted(P)):
        bites += 1
        if all(abs(Lp[i][j]) == abs(tg[i][j]) for i in range(m) for j in range(m)):
            mag_same += 1
        pred_true += absorbable_2col(Lp, tg)
print("   s = ((-1)^j) verifies E.L^rel(parity).E == S . (D-A) . S on %d/%d posets"
      % (exhibited, len(ps)))
print("   bites (L^rel changes) on %d posets; magnitudes identical to the target"
      % bites)
print("     on %d/%d of them; the predicate returns absorbable on %d/%d."
      % (mag_same, bites, pred_true, bites))
print("   So it reaches the parity system for a reason that is prior to the")
print("   measurement: a conjugation by a diagonal +-1 matrix cannot change an")
print("   absolute value.  It witnesses that the PREDICATE can say True.  It")
print("   cannot witness anything about a pair whose magnitudes differ.")
print()

# ---------------------------------------------------------------------------
print("2. DOES THE REPAIR KEEP A WITNESS FOR ROW I4?")
print()
src = open(CONTROLS).read()
art = open("../face_geometry/controls_output.txt").read()
for hay, tag in [(src, "controls.py"), (art, "controls_output.txt")]:
    hits = [ln for ln in hay.split("\n") if "witness" in ln.lower()]
    print("   %-20s : %d line(s) mention a witness" % (tag, len(hits)))
print()
for ln in art.split("\n"):
    low = ln.lower()
    if "witness" in low:
        # print the witness sentences of the artifact, wrapped
        for piece in ln.strip().split(". "):
            if "witness" in piece.lower():
                print("     > %s." % piece.strip().rstrip("."))
print()
print("   The claim 'row I4 is falsifiable' and the phrase 'this is the witness'")
print("   are searched for by name:")
for phrase in ["row I4 is falsifiable", "this is the witness",
               "IT IS NOT A WITNESS THAT ROW I4 IS FALSIFIABLE"]:
    print("     %-46s in controls.py: %-5s  in artifact: %s"
          % ("'%s'" % phrase, phrase in src, phrase in art))
print()
print("   Can row I4's SCORED CONDITION fail, clause by clause?  (The condition")
print("   is `app > 0 and rej == app and shape_ok == app and absorb == 0`.)")
app = rej = shape_ok = absorb = 0
for P in ps:
    Lt, Lm, tg = twisted(P), twisted(P, "facet_offbyone"), target(P)
    if eq(Lm, Lt):
        continue
    app += 1
    rej += not eq(Lm, tg)
    m = len(Lt)
    shape_ok += (len(Lm) == m and all(len(Lm[i]) == m for i in range(m)))
    absorb += absorbable_2col(Lm, tg)
base_ok = sum(1 for P in ps if eq(twisted(P), target(P)))
print("     app = %d, rej = %d, shape_ok = %d, absorb = %d" % (app, rej, shape_ok, absorb))
print("     claim (1) holds on the UNCORRUPTED build on %d/%d posets, and it is"
      % (base_ok, len(ps)))
print("       PROVEN for every finite poset (mg-276d).  Given that, L_mut != L_true")
print("       iff L_mut != target, so `rej == app` is an identity, not a test.")
print("     |facets| = |L(P)| under every incidence mode (le_to_facet_offbyone is")
print("       injective on words), so `shape_ok == app` is an identity too.")
print("     `absorb == 0` is forced -- parts 1, 2 and 3.")
print("     What is left that can fail: `app > 0`, i.e. the corruption biting at all.")
print()

# ---------------------------------------------------------------------------
print(BAR)
print("3. DID THE CONDITION MOVE?  code-only diff of controls.py, HEAD~1 -> HEAD")
print(BAR)
print()


def strip_prose(source):
    """One normalised line per LOGICAL line, with every comment and every string
    literal deleted outright.  Docstrings, printed text and format strings are
    invisible to a diff of this; a moved condition, a changed routing quantity
    or a new call is not."""
    out, cur, depth = [], [], 0
    for tok in tokenize.generate_tokens(io.StringIO(source).readline):
        t, s = tok.type, tok.string
        if t in (tokenize.COMMENT, tokenize.NL, tokenize.STRING):
            continue
        if t in (tokenize.INDENT, tokenize.DEDENT, tokenize.ENCODING,
                 tokenize.ENDMARKER):
            continue
        if t == tokenize.NEWLINE:
            if cur:
                out.append(" ".join(cur))
            cur = []
            continue
        if s in "([{":
            depth += 1
        elif s in ")]}":
            depth -= 1
        cur.append(s)
    if cur:
        out.append(" ".join(cur))
    return out


old = subprocess.check_output(
    ["git", "show", "HEAD~1:code/face_geometry/controls.py"],
    cwd="..").decode()
new = open(CONTROLS).read()
a, b = strip_prose(old), strip_prose(new)
diff = [ln for ln in difflib.unified_diff(a, b, "HEAD~1", "HEAD", lineterm="", n=1)]
print("   executable lines: %d before, %d after" % (len(a), len(b)))
print("   code-only diff (%d hunk lines):" % len([d for d in diff if d[:1] in "+-"]))
for ln in diff:
    print("     %s" % ln[:110])
print()
print("   The scored conditions themselves, extracted from the AST:")
tree = ast.parse(new)


def find_fn(t, name):
    for node in ast.walk(t):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    return None


fn_new = find_fn(tree, "negative_control_incidence")
fn_old = find_fn(ast.parse(old), "negative_control_incidence")
for label, fn in (("HEAD~1", fn_old), ("HEAD", fn_new)):
    conds = []
    for node in ast.walk(fn):
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id in ("cond", "forced")
                for t in node.targets):
            conds.append("%s = %s" % (node.targets[0].id, ast.unparse(node.value)))
        if isinstance(node, ast.AugAssign):
            pass
    print("     %-7s : %s" % (label, " | ".join(conds)))
print()
