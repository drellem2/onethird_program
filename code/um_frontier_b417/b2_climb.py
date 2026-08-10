"""b2 -- THE SEARCH.  Push the frontier upward at n = 9..14 and report every restart.

WHAT IS BEING MAXIMISED, AND WHY IT IS NOT u_M.

  A poset refutes the DISJUNCTION iff (F) fails AND (M#) fails, i.e. iff
  J(P) := min(u_F, u_M) > 1.  Maximising bare u_M is a DIFFERENT search with a known
  and worthless answer: 4 primitive posets at n = 7 already have u_M > 1, and (F) holds
  at every one of them.  Arm B2.4 runs that search on purpose, so that the difference
  between the two is measured here rather than asserted.

WHAT EVERY NUMBER IN THIS FILE IS.  A SEARCH FIGURE OVER A POPULATION IT DID NOT
ENUMERATE.  `0.968818` at n = 8 is barred from being quoted as a maximum for exactly
this reason and the same bar applies to every digit below.  The restart counts are
printed so that "the search found x" can be read as what it is.

AND THE SCREEN OVER-STATES.  Stage 1 scores with mu_ub_float, an UPPER bound on
mu_pref, so every J printed by the climb is an UPPER bound on the true J.  Champions
are re-scored exhaustively (stage 2) and certified on integers (b4).  A champion that
does not survive that is a REFUSAL and is reported as one.

SEEDS.  Two arms, counted separately, because a lifted seed is not an independent
restart (E7):
  B2.2  RANDOM restarts, rng seeded 20260810 in this file, and the (L*)-gap witnesses
        are NOT in the seed list -- so "the climb reaches this region on its own" is a
        claim that can fail.
  B2.3  LIFTED seeds: every one-element extension of the best posets found at n-1,
        screened, best few climbed.
"""

import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from libb417 import (LSTAR_GAP, N8_ARGMAX, climb, height, lifts, neighbours,
                     random_poset, score_float, score_screen)

RND = random.Random(20260810)

NS = [9, 10, 11, 12, 13, 14]
RESTARTS = {9: 30, 10: 24, 11: 18, 12: 14, 13: 10, 14: 8}
STEPS = {9: 60, 10: 60, 11: 50, 12: 40, 13: 30, 14: 25}
LIFT_CAP = 40            # ideals screened per parent, reported when it bites
LIFT_CLIMB = 4           # how many screened lifts are actually climbed

TOPK = 6                 # champions handed to the exact stage per n

BEST = {}                # n -> list of (J_screen, dn) candidates
POOL = {}                # n -> list of dn for lifting


def report(tag, n, dn, s, steps, evals, dt):
    print("    %-14s n=%2d  J>=%.6f  (u_F %.6f  u_M %.6f  v_L %.6f  D %.6f  mu %.6f  h %d)"
          "  %d steps %d evals %.0fs"
          % (tag, n, s["J"], s["u_F"], s["u_M"], s["v_L"], s["D"] if s["D"] else -1,
             s["mu"], height(dn, n), steps, evals, dt))
    sys.stdout.flush()


print("=" * 78)
print("B2.1  THE OBJECTIVE, AND THE FLOOR IT STARTS FROM")
print("=" * 78)
print("""
  J(P) = min(u_F, u_M).  The disjunction holds at n iff  W(n) = max_P J(P) <= 1.

  PUBLISHED, EXHAUSTIVE, and NOT re-measured here (mg-c50b s2 out_s2_theory.txt:38-42):
      W(3..7) = 0.000000 / 0.486136 / 0.649886 / 0.818379 / 0.890780
  PUBLISHED, EXHAUSTIVE, n = 8 (mg-c50b s3): c_or(8) = 0.943649, both routes fail at
      0 of 2600369.  n = 8 IS NOT ENUMERATED HERE and is not this ticket's business.

  Everything below is n >= 9 and is SEARCH.
""")

print("  the (L*)-gap population, scored exhaustively (stage 2) -- the seed floor:")
for tag, dn, n in LSTAR_GAP:
    s = score_float(dn, n)
    print("    %-3s n=%2d  J=%.6f  u_F=%.6f  u_M=%.6f  v_L=%.6f  D=%.6f  mu=%.6f  gamma=%.6f  h=%d"
          % (tag, n, s["J"], s["u_F"], s["u_M"], s["v_L"], s["D"], s["mu"], s["gamma"],
             height(dn, n)))
    BEST.setdefault(n, []).append((s["J"], dn, "gap:" + tag))
    POOL.setdefault(n, []).append(dn)
sys.stdout.flush()

print()
print("=" * 78)
print("B2.2  RANDOM RESTARTS -- the (L*)-gap witnesses are NOT in this seed list")
print("=" * 78)
for n in NS:
    t0 = time.time()
    for r in range(RESTARTS[n]):
        t1 = time.time()
        start = random_poset(RND, n)
        dn, s, steps, evals = climb(start, n, max_steps=STEPS[n])
        if s is None:
            print("    random  %2d     n=%2d  REFUSED (non-primitive / gamma 0)" % (r, n))
            continue
        report("random %2d" % r, n, dn, s, steps, evals, time.time() - t1)
        BEST.setdefault(n, []).append((s["J"], dn, "random%d" % r))
    print("    -- n=%2d random arm done, %d restarts, %.0fs" % (n, RESTARTS[n], time.time() - t0))
    sys.stdout.flush()

print()
print("=" * 78)
print("B2.3  LIFTED SEEDS -- every one-element extension of the best posets at n-1")
print("=" * 78)
print("""  A lifted seed is NOT an independent restart: it is one trajectory continued.
  Counted and reported separately for that reason (E7).
""")
for n in NS:
    parents = []
    for dnp in POOL.get(n - 1, []):
        parents.append((dnp, n - 1))
    seen = set()
    for J, dnp, tag in sorted(BEST.get(n - 1, []), reverse=True)[:3]:
        if dnp not in seen:
            seen.add(dnp)
            parents.append((dnp, n - 1))
    if not parents:
        print("    n=%2d  no parents at n=%d -- nothing lifted" % (n, n - 1))
        continue
    cands = []
    for dnp, np_ in parents:
        L = lifts(dnp, np_)
        if len(L) > LIFT_CAP:
            stride = len(L) // LIFT_CAP + 1
            print("    n=%2d  parent %s has %d lifts, screening every %dth (CAP %d BIT)"
                  % (n, str(dnp), len(L), stride, LIFT_CAP))
            L = L[::stride]
        for dnl, nl in L:
            s = score_screen(dnl, nl)
            if s is not None:
                cands.append((s["J"], dnl))
    cands.sort(reverse=True)
    print("    n=%2d  %d lifts screened, top screen J = %s"
          % (n, len(cands), "%.6f" % cands[0][0] if cands else "n/a"))
    sys.stdout.flush()
    for i, (J0, dnl) in enumerate(cands[:LIFT_CLIMB]):
        t1 = time.time()
        dn, s, steps, evals = climb(dnl, n, max_steps=STEPS[n])
        if s is None:
            continue
        report("lift %d" % i, n, dn, s, steps, evals, time.time() - t1)
        BEST.setdefault(n, []).append((s["J"], dn, "lift%d" % i))
        POOL.setdefault(n, []).append(dn)
    # keep the pool small and deterministic
    POOL[n] = sorted(set(POOL.get(n, [])))[:6]
sys.stdout.flush()

print()
print("=" * 78)
print("B2.4  THE CONTROL THAT MAKES THE OBJECTIVE MEAN SOMETHING")
print("=" * 78)
print("""  The SAME climb, same seeds, same moves, maximising BARE u_M instead of
  min(u_F,u_M).  If bare u_M runs far above 1 while (F) HOLDS at its argmax, then
  'max u_M' is not the frontier and a ticket phrased in those terms is pointed at the
  wrong number.  E3, measured.
""")
for n in (9, 10, 12):
    t1 = time.time()
    start = random_poset(RND, n)
    dn, s, steps, evals = climb(start, n, max_steps=STEPS[n],
                                objective=lambda z: z["u_M"])
    if s is None:
        continue
    print("    bare-u_M n=%2d  u_M >= %.6f   u_F = %.6f   (F) FAILS: %s   "
          "=> refutes disjunction: %s   [%d steps, %.0fs]"
          % (n, s["u_M"], s["u_F"], s["u_F"] > 1.0, (s["u_F"] > 1.0 and s["u_M"] > 1.0),
             steps, time.time() - t1))
    sys.stdout.flush()

print()
print("=" * 78)
print("B2.5  CHAMPIONS -- re-scored EXHAUSTIVELY (stage 2), handed to b4 for integers")
print("=" * 78)
print("  screen J is an UPPER bound; float J is the truth up to float error; the gap")
print("  between them is how much the screen inflated, printed rather than assumed.")
print()
print("   n | screen J   | float J    | inflation  | u_F        | u_M        | dn")
champions = {}
for n in NS:
    rows = sorted(set((round(J, 12), dn) for J, dn, tag in BEST.get(n, [])), reverse=True)
    picked, seen = [], set()
    for J, dn in rows:
        if dn in seen:
            continue
        seen.add(dn)
        picked.append((J, dn))
        if len(picked) >= TOPK:
            break
    champions[n] = []
    for J, dn in picked:
        sf = score_float(dn, n)
        if sf is None:
            continue
        champions[n].append(dict(dn=list(dn), n=n, screen_J=J, float_J=sf["J"],
                                 u_F=sf["u_F"], u_M=sf["u_M"], v_L=sf["v_L"],
                                 D=sf["D"], mu=sf["mu"], gamma=sf["gamma"],
                                 height=height(dn, n)))
        print("  %2d | %10.6f | %10.6f | %+10.6f | %10.6f | %10.6f | %s"
              % (n, J, sf["J"], J - sf["J"], sf["u_F"], sf["u_M"], str(dn)))
    sys.stdout.flush()

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "champions.json"), "w") as fh:
    json.dump(champions, fh, indent=1, sort_keys=True)

print()
print("=" * 78)
print("B2.6  THE SEARCH FRONTIER, PER n -- SEARCH FIGURES, NOT MAXIMA")
print("=" * 78)
print("   n | best float J | crosses 1 | restarts (random) | argmax dn")
for n in NS:
    if not champions[n]:
        continue
    top = max(champions[n], key=lambda c: c["float_J"])
    print("  %2d | %12.6f | %9s | %17d | %s"
          % (n, top["float_J"], "YES" if top["float_J"] > 1 else "no",
             RESTARTS[n], str(tuple(top["dn"]))))
print()
print("  Every entry above is a SEARCH result over a population of primitive posets")
print("  that was NOT enumerated.  None of these is a maximum at its n.")
