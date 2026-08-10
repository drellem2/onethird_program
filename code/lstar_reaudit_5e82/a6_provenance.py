"""a6 -- THE PROVENANCE FINDING, and the mechanism that produced it.

Two separable claims from the work item, each checked against `main` rather than
against the worktree, so the result does not depend on what this branch has added.

  P1  The counterexample was ALREADY ON MAIN, in published figures nobody multiplied.
  P2  THE MECHANISM: mg-5cba's audit table has five rows and a u_M column; C1-C4
      carry values and the C5 row carries a DASH.  STATE.md then published
      '(M#) HOLDS at 4 of 4'.  A blank cell became a published bound.

  P3  A FOURTH SITE, examined and NOT claimed as an error: STATE.md's row says the
      gap between (L*) and (M#) is exactly mu_pref^2.  Which normalisation is that in?
"""
import subprocess
import sys
from common5e82 import banner

ok = True


def check(label, got, want):
    global ok
    good = got == want
    ok = ok and good
    print("  [%s] %-62s got=%r want=%r" % ("ok " if good else "FAIL", label, got, want))


def on_main(path):
    return subprocess.run(["git", "show", "main:" + path], capture_output=True,
                          text=True, check=True).stdout


MAIN_SHA = subprocess.run(["git", "rev-parse", "main"], capture_output=True,
                          text=True, check=True).stdout.strip()
banner("a6  PROVENANCE -- READ FROM main AT %s" % MAIN_SHA[:12])

DOC = "docs/OneThird-LStar-mg-5cba-IndependentAudit.md"
SCOPE = "code/audit_5cba/out_a5_scope.txt"
STATE = "STATE.md"

print()
print("P1  THE TWO HALVES, ON MAIN, NAMING THIS EXACT POSET")
print("-" * 78)
scope = on_main(SCOPE).splitlines()
hits = [(i + 1, ln) for i, ln in enumerate(scope)
        if "0.061699260" in ln and "0.065579592" in ln]
for lineno, ln in hits:
    print("  %s:%d" % (SCOPE, lineno))
    print("    %s" % ln.strip())
check("out_a5_scope.txt on main carries BOTH halves on one line", len(hits), 1)
ctx = scope[hits[0][0] - 2].strip() if hits else ""
print("  the line above it (which is what names the poset as the n=12 one):")
print("    %s" % ctx)
check("  ... and that context line says n = 12", "n=12" in ctx, True)
check("  ... gamma upper bound present", "0.061699262" in hits[0][1], True)
check("  ... mu_pref lower bound present", "mu_pref >= 0.065579592" in hits[0][1], True)
check("  ... Delta present", "Delta=195/196" in hits[0][1], True)
check("  ... LE present", "LE=10584" in hits[0][1], True)

doc = on_main(DOC).splitlines()
row = [(i + 1, ln) for i, ln in enumerate(doc) if ln.startswith("| **C5 `n=12`**")]
print()
print("  and the SAME two numbers, again, in the audit table itself:")
for lineno, ln in row:
    print("  %s:%d" % (DOC, lineno))
    print("    %s" % ln.strip())
check("the C5 table row exists on main", len(row), 1)
print("""
  SO THE WORK ITEM'S 'two published halves nobody multiplied' IS CONFIRMED IN
  SUBSTANCE and refined in form: they are not two halves in two places.  They are on
  ONE LINE of out_a5_scope.txt and again on ONE LINE of the audit table -- the same
  poset, the same Delta, both bounds, printed twice on main.  Multiplying them is
  four lines of arithmetic (a4.4 does it and gets +0.0027907976).  This counterexample
  has been on main since mg-5cba landed.""")

print()
print("P2  THE MECHANISM: THE DASH")
print("-" * 78)
tbl = [(i + 1, ln) for i, ln in enumerate(doc)
       if ln.startswith("| C1 ") or ln.startswith("| C2 ") or ln.startswith("| C3 ")
       or ln.startswith("| C4 ") or ln.startswith("| **C5")]
for lineno, ln in tbl:
    cells = [c.strip() for c in ln.strip().strip("|").split("|")]
    print("  :%-4d %-16s u_M = %s" % (lineno, cells[0], cells[-1]))
check("the audit table has five counterexample rows", len(tbl), 5)
last_cells = [c.strip() for c in tbl[-1][1].strip().strip("|").split("|")]
check("the C5 row's u_M cell is a dash", last_cells[-1], "—")
check("C1-C4 u_M cells all carry values", all(
    [c.strip() for c in ln.strip().strip("|").split("|")][-1] != "—" for _, ln in tbl[:4]),
    True)

state = on_main(STATE)
S1 = "`(M♯)` HOLDS at **4 of 4**"
S2 = "`u_M = 0.943486 / 0.947534 / 0.981830 / 0.958326`"
check("STATE.md on main contains '(M#) HOLDS at 4 of 4'", S1 in state, True)
check("STATE.md on main lists exactly four u_M figures", S2 in state, True)
nfig = state.count("0.943486") + state.count("0.947534") + state.count("0.981830") + state.count("0.958326")
print("""
  THE MECHANISM IS CONFIRMED, AND IT IS EXACTLY AS THE WORK ITEM DESCRIBES IT.
  mg-5cba certified FIVE counterexamples and computed u_M at FOUR of them.  The fifth
  cell is a dash -- an HONEST dash: the audit did not compute it and did not say it
  had.  STATE.md then wrote '(M#) HOLDS at 4 of 4' with four figures.  That sentence
  is TRUE OF THE FOUR IT NAMES.  What it does not carry is that there is a fifth
  certified counterexample at which (M#) was never evaluated -- and the reader of
  'at 4 of 4' beside 'FIVE counterexamples certified' has to notice the arithmetic
  themselves.  mg-b417 then inherited it: 'u_M = 0.981830 is the closest any (M#)
  witness has come to failing' is the closest of the four that were COMPUTED.

  A BLANK CELL BECAME A PUBLISHED BOUND, and no step in that chain stated a falsehood.""")

print()
print("P3  THE FOURTH SITE -- WHICH NORMALISATION IS THE mu_pref^2 CLAUSE IN?")
print("-" * 78)
CLAUSE = "the gap between `(L*)` and `(M♯)` is exactly `μ_pref²`"
check("STATE.md on main contains the mu_pref^2 clause", CLAUSE in state, True)
LSTAR_IN_ROW = "`M² > 2γ ⟹ μ_pref·Δ_P ≤ γ`"
check("the SAME row states (L*) as mu_pref*Delta <= gamma (UNDOUBLED)",
      LSTAR_IN_ROW in state, True)
print("""
  SETTLED, AND NOT TOUCHED.

    doubled form   (L*) conclusion :  2*Delta*mu             <= 2*gamma
                   (M#)            :  2*Delta*mu - mu^2      <= 2*gamma   gap = mu^2
    undoubled form (L*) conclusion :    Delta*mu             <=   gamma
                   (M#)            :    Delta*mu - mu^2/2    <=   gamma   gap = mu^2/2

  mg-5cba's §2 displays the pair in the DOUBLED form and the clause is EXACTLY RIGHT
  there.  STATE.md's row writes (L*) in the UNDOUBLED form -- `M² > 2γ ⟹ μ_pref·Δ_P
  ≤ γ` -- and then quotes the doubled form's gap.  So in the normalisation the row
  itself uses, the gap is mu_pref^2/2, and the clause has travelled from a display
  block into a sentence with a different normalisation without its factor of 2.

  IT CHANGES NO VERDICT HERE and this audit does NOT edit it.  a4 evaluates (M#) from
  its own definition, `2*Delta*mu_pref - mu_pref^2 <= 2*gamma`, and never uses the gap
  clause for anything.  Recording it because it is the mg-0d1b hazard in the form the
  alias-agreement check CANNOT see: a factor of 2 between two conventions is
  indistinguishable, to a value comparison, from two implementations disagreeing.""")

print()
print("P4  THE THREE CLAUSES THAT MOVE IF THIS CONFIRMS")
print("-" * 78)
for tag, frag in [
    ("(a) the row's headline", "AND THE DISJUNCTION SURVIVES IT"),
    ("(b) the 4-of-4 sentence", S1),
    ("(c) what is lost", "What is lost is exactly one thing: the uniform-in-`n` proof."),
]:
    check("%s is present on main" % tag, frag in state, True)
for tag, frag in [
    ("n=7 enumeration", "96428/86278"),
    ("n=8 enumeration", "2800472/2600369"),
    ("c_or(8)", "c_or(8) = 0.943649"),
]:
    check("%s is present on main (and is NOT moved by this)" % tag, frag in state, True)
print()
print("  This audit changes NO document.  It records that (a), (b) and (c) are the")
print("  clauses a confirming verdict reaches, and that the n <= 8 enumerations,")
print("  Theorem A, the onset correction and the depth table are not among them.")
print()
banner("a6 VERDICT: %s" % ("ALL ARMS SATISFACTORY" if ok else "*** AN ARM FAILED ***"))
sys.exit(0 if ok else 1)
