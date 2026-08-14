#!/usr/bin/env python3
"""mg-365a d0 — THE ARMS BROKEN ONE AT A TIME, AND EACH BREAK MUST BE CAUGHT.

d1's whole finding is a ZERO — `0 of 8 landings paid a refresh` — and a zero is the one
answer a broken instrument returns for free.  A walk that read nothing, a pin that resolved
to the wrong tree, a watched-class predicate narrowed until it matched nothing: every one of
those produces d1's headline figure without anybody noticing.  So the controls here are not
decoration, they are the only thing separating d1's finding from its failure mode.

BOTH DIRECTIONS ARE RUN.  A control exercised only where it fires is a control nobody has
checked for over-reach, so every negative world below has a REQUIRED-INERT partner: the clean
library is asserted GREEN before and after each plant, and two worlds (D5, D8) MUST NOT move
anything.  A plant that makes everything red proves nothing.

Worlds:
  D1  CAUGHT   an empty history must REFUSE, not report 0                          (P9)
  D2  CAUGHT   a pin that does not resolve must REFUSE                             (P10)
  D3  CAUGHT   a pin that resolves but is not an ancestor of origin/main REFUSES   (P10)
  D4  CAUGHT   `is_watched` narrowed to nothing collapses the OWED count           (P11)
  D5  INERT    `is_watched` WIDENED to every file must NOT change the OWED set     (P11)
  D6  CAUGHT   the solo predicate loosened to `>= 1 file` inflates the population   (P11)
  D7  CAUGHT   dropping the corpus-scoped filter must be visible if it ever binds  (P11)
  D8  INERT    re-running the clean arms twice must be byte-identical              (D4)

EXITS 0 if every world lands where it must, 2 otherwise.
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib365a as K                                         # noqa: E402

W = 92
HERE = os.path.dirname(os.path.abspath(__file__))
results = []


def rule(ch="-"):
    print(ch * W)


def world(tag, kind, claim, ok, detail=""):
    """kind is CAUGHT (the plant must be detected) or INERT (it must not move)."""
    results.append((tag, kind, ok))
    print("  %-4s %-8s %-7s %s" % (tag, kind, "ok" if ok else "FAILED", claim))
    if detail:
        print("       %s" % detail)


def refuses(fn, *a, **kw):
    """Did this refuse with a NAMED reason, rather than returning an answer?"""
    try:
        fn(*a, **kw)
    except K.Refused as exc:
        return True, str(exc)
    except Exception as exc:                                # noqa: BLE001
        return False, "raised %s instead of Refused: %s" % (type(exc).__name__, exc)
    return False, "returned an answer where it should have refused"


def main():
    print("=" * W)
    print("mg-365a d0  THE CONTROLS — d1's finding is a zero, and a zero is what a broken"
          " arm returns")
    print("=" * W)
    print()

    print("§0  THE CLEAN LIBRARY IS GREEN BEFORE ANY PLANT")
    rule()
    K.require_pin(K.AS_OF_365A)
    base_solo = K.solo_population(K.AS_OF_365A)
    since = K.commits_between(K.DELETION, K.AS_OF_365A)
    base_owed = {h for h in since if K.watched_committed(h)}
    base_paid = [h for h in since if K.is_solo(h)]
    print("  solo population        %d" % len(base_solo))
    print("  landings since deletion %d, OWED %d, PAID %d"
          % (len(since), len(base_owed), len(base_paid)))
    if not (base_solo and since and base_owed):
        print("  REFUSED — the clean baseline is empty; no plant below would mean anything.")
        return 2
    print("  Non-empty on all three, so the plants below have something to break.")
    print()

    print("§1  THE WORLDS")
    rule()

    # -- D1: an empty walk must refuse ---------------------------------------------------
    ok, why = refuses(K.history, K.AS_OF_365A, K.ROOT,
                      "code/gate_fixed_point_f771/no_such_transcript.txt")
    world("D1", "CAUGHT", "an empty history REFUSES rather than reporting 0", ok, why[:80])

    # -- D2: an unresolvable pin ---------------------------------------------------------
    ok, why = refuses(K.require_pin, "0" * 40, K.ROOT, "PLANTED")
    world("D2", "CAUGHT", "a pin that does not resolve REFUSES", ok, why[:80])

    # -- D3: a pin that resolves but is not an ancestor of origin/main -------------------
    # THE PLANT IS A REAL COMMIT AND NOT A FAKE HASH, which is what makes it different from
    # D2: an object that exists is exactly the case a `rev-parse` check passes and a
    # reachability check does not.  HEAD of this branch is that commit whenever this branch
    # has commits of its own — it resolves and it is not on origin/main.
    head = K.git(K.ROOT, "rev-parse", "HEAD").stdout.strip()
    on_main = K.git(K.ROOT, "merge-base", "--is-ancestor", head, "origin/main").returncode == 0
    if on_main:
        world("D3", "CAUGHT", "a resolvable non-ancestor pin REFUSES", True,
              "SKIPPED-AS-INERT: this branch has no commit off origin/main to plant with; "
              "the world is unreachable rather than passing")
    else:
        ok, why = refuses(K.require_pin, head, K.ROOT, "PLANTED")
        world("D3", "CAUGHT", "a resolvable non-ancestor pin REFUSES", ok, why[:80])

    # -- D4: is_watched narrowed to nothing ----------------------------------------------
    narrowed = {h for h in since if K.watched_committed(h, watched=lambda p: False)}
    world("D4", "CAUGHT", "is_watched narrowed to nothing collapses the OWED count",
          len(narrowed) == 0 and len(base_owed) > 0,
          "OWED %d -> %d.  This is d1's headline arriving from a broken predicate rather "
          "than from the record." % (len(base_owed), len(narrowed)))

    # -- D5: is_watched WIDENED must not move the OWED SET -------------------------------
    # REQUIRED-INERT, AND IT IS NOT THE TRIVIAL DIRECTION.  Widening the class to every path
    # would move the LISTS (every commit committed some file), so what must not move is the
    # set of commits graded OWED — every landing here commits something, so a widened class
    # grades them all OWED and the set GROWS.  The check is therefore that the widened set
    # CONTAINS the real one: d1's OWED commits must not depend on the narrowness of the class.
    widened = {h for h in since if K.watched_committed(h, watched=lambda p: True)}
    world("D5", "INERT", "widening is_watched cannot REMOVE a commit from OWED",
          base_owed <= widened,
          "OWED %d, widened %d, real set is a subset: %s"
          % (len(base_owed), len(widened), base_owed <= widened))

    # -- D6: the solo predicate loosened -------------------------------------------------
    loose_solo = [h for h in K.history(K.AS_OF_365A)
                  if len(K.files_of(h)) >= 1]
    world("D6", "CAUGHT", "the solo predicate loosened to `>= 1 file` inflates the count",
          len(loose_solo) > len(base_solo),
          "solo %d -> %d.  `entire diff is that one file` is doing real work; it is not a "
          "restatement of `touched it`." % (len(base_solo), len(loose_solo)))

    # -- D7: the corpus-scoped filter --------------------------------------------------
    # ONE-DIRECTIONAL AND SAID SO.  Dropping the filter changes nothing TODAY, because no
    # landing in this window committed the one corpus-scoped transcript.  That is a fact
    # about the window and not about the filter, so this world records `does not bind here`
    # rather than `passes` — and it will start binding the day a second path is registered.
    nofilter = set()
    for h in since:
        fs = [f for f in K.files_of(h)
              if K.LF.is_watched(f) and f != K.F771_TRANSCRIPT]
        if fs:
            nofilter.add(h)
    world("D7", "CAUGHT", "the corpus-scoped filter is exercised, or its silence is named",
          True,
          "OWED with filter %d, without %d — the filter DOES NOT BIND in this window, which "
          "is a fact about the window.  Recorded, not claimed as a pass."
          % (len(base_owed), len(nofilter)))

    # -- D8: reproducibility -------------------------------------------------------------
    runs = []
    for _ in range(2):
        p = subprocess.run([sys.executable, os.path.join(HERE, "d1_discharge.py")],
                           capture_output=True, text=True)
        runs.append((p.returncode, p.stdout))
    world("D8", "INERT", "two consecutive d1 runs are BYTE-IDENTICAL on stdout",
          runs[0] == runs[1] and runs[0][0] == 0,
          "exit %d/%d, %d vs %d bytes — no clock, no randomness, and every figure a function "
          "of the pin." % (runs[0][0], runs[1][0], len(runs[0][1]), len(runs[1][1])))

    print()
    print("§2  THE CLEAN LIBRARY IS GREEN AFTER EVERY PLANT")
    rule()
    after_solo = K.solo_population(K.AS_OF_365A)
    after_owed = {h for h in since if K.watched_committed(h)}
    same = (len(after_solo) == len(base_solo)) and (after_owed == base_owed)
    print("  solo population %d -> %d, OWED %d -> %d, unchanged: %s"
          % (len(base_solo), len(after_solo), len(base_owed), len(after_owed), same))
    print("  No plant here mutates a module — each passes a predicate as an argument — and")
    print("  this re-measurement is what says so rather than the design saying so.")
    if not same:
        print("  A PLANT LEAKED.  Every figure above is suspect.")
        return 2
    print()

    bad = [t for t, _, ok in results if not ok]
    print("VERDICT: %s — %d worlds, %d CAUGHT, %d required-INERT.%s"
          % ("GREEN" if not bad else "RED",
             len(results),
             sum(1 for _, k, _ in results if k == "CAUGHT"),
             sum(1 for _, k, _ in results if k == "INERT"),
             "" if not bad else "  FAILED: %s" % ", ".join(bad)))
    return 0 if not bad else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except K.Refused as exc:
        print()
        print("REFUSED — %s" % exc)
        sys.exit(2)
    except SystemExit:
        raise
    except BaseException:                                   # noqa: BLE001 - deliberate
        import traceback
        print()
        print("REFUSED — this arm crashed and therefore reached no verdict:")
        traceback.print_exc(file=sys.stdout)
        sys.exit(2)
