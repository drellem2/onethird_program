"""Adversarial battery against mg-1319's A4 scoring repair.

Goal: emit the string "ALL CONTROLS PASS" as the bottom line while a row that
cannot fail is present.  Every attack below is a way a future control author
could plausibly write a row.
"""
import sys, io, contextlib
sys.path.insert(0, "../face_geometry")
import controls as C

def reset():
    C.FAIL.clear()
    C.CANNOT_FAIL.clear()

def bottom():
    lines, code = C.summarise(C.FAIL, C.CANNOT_FAIL)
    return "\n".join(lines), code

def banner_in(s):
    return "ALL CONTROLS PASS" in s

results = []
def report(name, lied, detail):
    results.append((name, lied, detail))

# ---- A1: the honest path -- a genuine cannot-fail row -------------------
reset()
with contextlib.redirect_stdout(io.StringIO()):
    C.check("tautology", True, cannot_fail=True)
b, code = bottom()
report("A1 baseline: cannot_fail=True row present",
       banner_in(b), "bottom=%r exit=%d" % (b.splitlines()[0], code))

# ---- A2: author forgets the flag (the obvious hole) ---------------------
reset()
with contextlib.redirect_stdout(io.StringIO()):
    # exactly the all-+1 tautology, but registered as an ordinary row
    C.check("all-+1 signs leave both Laplacians unchanged", True)  # no cannot_fail
b, code = bottom()
report("A2 tautological row registered WITHOUT cannot_fail=True",
       banner_in(b), "bottom=%r exit=%d" % (b.splitlines()[0], code))

# ---- A3: truthy-but-not-True flag --------------------------------------
reset()
with contextlib.redirect_stdout(io.StringIO()):
    C.check("taut", True, cannot_fail=1)
b, _ = bottom()
report("A3 cannot_fail=1 (truthy int)", banner_in(b), "bottom=%r" % b.splitlines()[0])

reset()
with contextlib.redirect_stdout(io.StringIO()):
    C.check("taut", True, cannot_fail="no")   # a string an author might pass
b, _ = bottom()
report("A3b cannot_fail='no' (truthy string, author means NO)",
       banner_in(b), "bottom=%r" % b.splitlines()[0])

# ---- A4: positional-argument slip --------------------------------------
reset()
try:
    with contextlib.redirect_stdout(io.StringIO()):
        C.check("taut", True, True)     # 3rd positional is `detail`, not cannot_fail
    b, _ = bottom()
    report("A4 cannot_fail passed positionally (lands in `detail`)",
           banner_in(b), "bottom=%r" % b.splitlines()[0])
except Exception as e:
    report("A4 positional slip", False, "raised %r" % e)

# ---- A5: cannot-fail row whose fact is FALSE ---------------------------
reset()
with contextlib.redirect_stdout(io.StringIO()):
    C.check("false tautology", False, cannot_fail=True)
b, code = bottom()
report("A5 cannot-fail row reporting a FALSE fact",
       banner_in(b), "bottom=%r exit=%d (want FAIL/1)" % (b.splitlines()[0], code))

# ---- A6: does score() have a path to PASS with cannot_fail true? --------
combos = [(ok, cf) for ok in (True, False) for cf in (True, False)]
bad = [(ok, cf, C.score(ok, cf)) for ok, cf in combos
       if cf and C.score(ok, cf) == "PASS"]
report("A6 score() ever returns PASS with cannot_fail set", bool(bad), repr(bad))

# ---- A7: summarise() reachability sweep --------------------------------
lie = []
for fails in ([], ["f"]):
    for cf in ([], ["x"], ["x", "y"]):
        lines, code = C.summarise(fails, cf)
        if "ALL CONTROLS PASS" in "\n".join(lines) and cf:
            lie.append((fails, cf, lines, code))
report("A7 summarise() emits banner with a non-empty cannot-fail tally",
       bool(lie), repr(lie))

# ---- A8: empty-string row name (falsy) ---------------------------------
reset()
with contextlib.redirect_stdout(io.StringIO()):
    C.check("", True, cannot_fail=True)
b, _ = bottom()
report("A8 cannot-fail row with empty name", banner_in(b),
       "CANNOT_FAIL=%r bottom=%r" % (C.CANNOT_FAIL, b.splitlines()[0]))

# ---- A9: the real question -- is the flag DERIVED or DECLARED? ---------
import inspect
src = inspect.getsource(C)
declared = src.count("cannot_fail=True")
report("A9 cannot_fail is a hand-set literal, never derived from the run",
       False, "occurrences of literal `cannot_fail=True` in controls.py: %d" % declared)

print("=" * 78)
print("ADVERSARIAL BATTERY AGAINST THE A4 SCORING REPAIR")
print("=" * 78)
lied_any = False
for name, lied, detail in results:
    tag = "*** LIED ***" if lied else "  held  "
    lied_any |= lied
    print("%s %s\n            %s" % (tag, name, detail))
print("=" * 78)
print("BANNER EMITTED WITH A NON-FAILABLE ROW PRESENT:", "YES" if lied_any else "NO")
