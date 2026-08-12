"""mg-ac0c `a0` — the controls, run FIRST so that a green `a1`/`a2` means something.

Seven controls.  Three are wrong-direction worlds: they build a world in which the answer
should be the OPPOSITE of the one this instrument reports, and FAIL if the instrument still
reports the same thing.  An instrument that says *does not close* no matter what it is fed is
not evidence that the chain does not close.
"""

from fractions import Fraction as F
import libac0c as L

FAIL = 0


def check(label, got, want, note=""):
    global FAIL
    ok = (got == want)
    if not ok:
        FAIL += 1
    print(f"  [{'OK ' if ok else 'RED'}] {label}: got {got}  want {want}   {note}")


print("=" * 78)
print("a0 §A — CONTROL 1: the instrument REFUSES a float on a decision path")
print("=" * 78)
try:
    L.chain_I_III(0.2)
    print("  [RED] a float was accepted")
    FAIL += 1
except TypeError as e:
    print(f"  [OK ] refused, with the reason printed: {e}")

print()
print("=" * 78)
print("a0 §B — CONTROL 2: a Const CANNOT be built without status / scope / source / pin")
print("=" * 78)
for label, kwargs in [
    ("no scope", dict(key="X", step="s", what="w", status=L.PROVED, value=F(1),
                      scope="", source="src")),
    ("no source", dict(key="X", step="s", what="w", status=L.PROVED, value=F(1),
                       scope="sc", source="")),
    ("non-PROVED with no pin-or-hole", dict(key="X", step="s", what="w", status=L.EMPIRICAL,
                                            value=F(1), scope="sc", source="src")),
    ("unknown status", dict(key="X", step="s", what="w", status="PROBABLY", value=F(1),
                            scope="sc", source="src")),
]:
    try:
        L.Const(**kwargs)
        print(f"  [RED] {label}: accepted")
        FAIL += 1
    except (ValueError, TypeError) as e:
        print(f"  [OK ] {label}: refused — {e}")

print()
print("=" * 78)
print("a0 §C — CONTROL 3: PLUG-BACK. The chains, re-solved here, must reproduce the corpus's")
print("        own published ε_dem values.  A mis-transcription of a chain fails HERE.")
print("=" * 78)
# mg-9461 §5.1 / §5.4, and mg-7564 §0.4's ladder.
check("chain (I)≡(III), ε_leak=1/5, C₃=1  [mg-9461 §5.1: 1/50]",
      L.chain_I_III(F(1, 5)), F(1, 50))
check("chain (III) at C₃=2                [mg-9461 §5.3: 1/100]",
      L.chain_I_III(F(1, 5), F(2)), F(1, 100))
check("chain (I)/(III) at ε_leak=1/7      [mg-9461 §5.3: 1/98]",
      L.chain_I_III(F(1, 7)), F(1, 98))
check("chain (I)/(III) at ε_leak=17/78    [mg-9461 §5.3: 289/12168]",
      L.chain_I_III(F(17, 78)), F(289, 12168))
check("chain (II) at C₃^gap=3/2           [mg-9461 §5.4: 2/15]",
      L.chain_II(F(1, 5), F(3, 2)), F(2, 15))
check("chain (IV) at c=40/49              [mg-9461 §5.4: 1/50]",
      L.chain_IV(F(1, 5), F(40, 49)), F(1, 50))
check("chain (IV) at c=9/10               [mg-9461 §5.4: 1/9]",
      L.chain_IV(F(1, 5), F(9, 10)), F(1, 9))
check("chain (IV) at c=1                  [mg-9461 §5.4: 1/5]",
      L.chain_IV(F(1, 5), F(1)), F(1, 5))
check("cap at ε_leak=1/5                  [mg-7564 §4: 2/5]",
      L.cap(F(1, 5)), F(2, 5))
check("cap at ε_leak=1/7                  [mg-7564 §4.1: 2/7]",
      L.cap(F(1, 7)), F(2, 7))

print()
print("  the chain question is worth exactly 2/ε_leak, at EVERY C₃ (mg-9461 §5.3, C₃ cancels):")
for C3 in [F(1), F(3, 2), F(7, 3), F(10)]:
    ratio = L.chain_II(F(1, 5), C3) / L.chain_I_III(F(1, 5), C3)
    check(f"    ratio (II)/(III) at C₃={C3}", ratio, F(10))

print()
print("=" * 78)
print("a0 §D — CONTROL 4: NEGATIVE. A DELIBERATELY WRONG chain must NOT reproduce the ladder.")
print("=" * 78)


def chain_wrong(eps_leak, C3=F(1)):
    """The Cheeger square DROPPED — ε_leak/(2C₃) instead of ε_leak²/(2C₃)."""
    return eps_leak / (2 * C3)


got = chain_wrong(F(1, 5))
if got == F(1, 50):
    print("  [RED] the mutated chain still reproduces 1/50 — §C proves nothing")
    FAIL += 1
else:
    print(f"  [OK ] mutated chain gives {got} ≠ 1/50, so §C's agreement is not automatic")

print()
print("=" * 78)
print("a0 §E — CONTROL 5: WRONG-DIRECTION WORLD for the cap. The cap test must REFUSE a")
print("        hypothetical ε_dem = 3·ε_leak rather than accepting everything.")
print("=" * 78)
for mult, expect_ok in [(F(1), True), (F(2), True), (F(3), False), (F(5, 2), False)]:
    hypothetical = mult * F(1, 5)
    admitted = hypothetical <= L.cap(F(1, 5))
    check(f"  hypothetical ε_dem = {mult}·ε_leak admitted by the cap", admitted, expect_ok)

print()
print("=" * 78)
print("a0 §F — CONTROL 6: WRONG-DIRECTION WORLD for the closure test. Fed a supply that DOES")
print("        meet the demand, `closes()` must say YES — otherwise `a2`'s NOs are vacuous.")
print("=" * 78)
check("  supply 1/100 against demand 1/50 (should close)",
      L.closes(F(1, 100), F(1, 50)), True)
check("  supply 1/50 against demand 1/50 (should close, boundary)",
      L.closes(F(1, 50), F(1, 50)), True)
check("  supply 1/25 against demand 1/50 (should NOT close)",
      L.closes(F(1, 25), F(1, 50)), False)
check("  supply n/(n+1) at n=6 against demand 1/50 (should NOT close)",
      L.closes(L.eps_sup(6), F(1, 50)), False)

print()
print("=" * 78)
print("a0 §G — CONTROL 7: mg-d3c7's family, REPRODUCED from its closed form against the four")
print("        values mg-9461 §4.3 tabulates.  ⚠️ THIS IS ARITHMETIC, NOT A POSET CHECK.")
print("=" * 78)
for n, k, want in [(9, 4, F(5, 36)), (21, 10, F(11, 210)),
                   (101, 50, F(51, 5050)), (401, 200, F(201, 80200))]:
    check(f"  n={n} (k={k}) Δ₁", L.d3c7_leak(k), want)
print(f"  monotone decreasing to 0: {[str(L.d3c7_leak(k)) for k in (3, 4, 10, 50, 200)]}")
mono = all(L.d3c7_leak(k) > L.d3c7_leak(k + 1) for k in range(3, 200))
check("  strictly decreasing on k = 3..200", mono, True)

print()
print("=" * 78)
print(f"a0 VERDICT: {'GREEN — all controls pass' if FAIL == 0 else f'RED — {FAIL} control(s) fired'}")
print("=" * 78)
raise SystemExit(1 if FAIL else 0)
