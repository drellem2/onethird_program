#!/usr/bin/env python3
"""a1 — THE INDEX RE-MEASURED WITH c9876's OWN DETECTOR, AND THE DRIFT SAID OUT LOUD.

The ticket names three figures: 202 membership candidates in 66 directories, 18 live `| tee`
sites in 4, 24 directories shipping code with no evidence of a falsification attempt.  It
also says, in as many words, not to re-derive them with a third regex and report a fourth
number.  So this arm does two things and nothing else:

  §1  CHECKS THAT THE DETECTOR IS c9876's, BY DIGEST.  `liba397.load_c9876()` executes
      `code/control_audit_9876/a4_sweep.py` and uses the patterns it compiled.  A claim that
      we "used c9876's detector" is worth exactly as much as the check behind it, so the file
      is hashed and the hash is printed.  If somebody edits that file, this number moves and
      the claim has to be re-earned.

  §2  RE-MEASURES AND PRINTS THE DRIFT.  The population is `every directory under code/`, and
      this repository gains directories daily — mg-724a's gate observed 207 candidates on the
      REBASED tree where its author's worktree observed 206, on the same afternoon.  A figure
      quoted from a ticket is a DATED READING.  Any disagreement here is expected and is
      reported as arithmetic (what arrived, in which directories), never as a finding against
      c9876.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import liba397 as L  # noqa: E402


def main():
    print("=" * 92)
    print("mg-a397 a1 — THE INDEX, RE-MEASURED WITH mg-9876's DETECTOR")
    print("=" * 92)
    print()

    a4_path = os.path.join(L.C9876, "a4_sweep.py")
    print("§1  THE DETECTOR IS c9876's, AND THE CLAIM IS CHECKED RATHER THAN MADE")
    print("-" * 92)
    print(f"    detector : {L.rel(a4_path)}")
    print(f"    sha256   : {L.sha256(a4_path)}")
    a4 = L.load_c9876()
    print(f"    membership pattern : {a4.SMELL_MEMBERSHIP.pattern}")
    print(f"    for-binding veto   : {a4._FOR_BINDING.pattern}")
    print(f"    tee pattern        : {a4.SMELL_TEE.pattern}")
    print()
    print("    The two constructions c9876's own repair distinguishes are named in its")
    print("    docstring: `X in out` is membership, `for line in out.splitlines()` is")
    print("    ITERATION, and counting the second is how its first sweep reported 597.")
    print("    Both are exercised here against the loaded patterns, so a regression in the")
    print("    detector is visible in THIS transcript and not only in c9876's:")
    for probe, want in [('if "8 9" in out:', True),
                        ('for line in out.splitlines():', False),
                        ('for name, text in contents.items():', False),
                        ('red += check("no crash", "Traceback" not in out)', True)]:
        hit = bool(a4.SMELL_MEMBERSHIP.search(probe)) and not bool(a4._FOR_BINDING.search(probe))
        mark = "ok " if hit == want else "BROKEN"
        print(f"      {mark}  membership={hit!s:5} expected={want!s:5}  {probe}")
    print()

    print("§2  TODAY'S POPULATION, AND THE DRIFT AGAINST THE TICKET'S FIGURES")
    print("-" * 92)
    all_dirs = list(a4.dirs())
    mem = L.sites(a4)
    tee = L.tee_sites(a4)
    bare = L.bare_dirs(a4)
    mem_dirs = sorted({s["dir"] for s in mem})
    tee_dirs = sorted({s["dir"] for s in tee})

    rows = [("membership candidate sites", len(mem), L.TICKET_FIGURES["membership_sites"]),
            ("… in directories", len(mem_dirs), L.TICKET_FIGURES["membership_dirs"]),
            ("live `| tee` sites", len(tee), L.TICKET_FIGURES["tee_sites"]),
            ("… in directories", len(tee_dirs), L.TICKET_FIGURES["tee_dirs"]),
            ("dirs with code, no falsification evidence", len(bare),
             L.TICKET_FIGURES["bare_dirs"])]
    print(f"    population: {len(all_dirs)} directories under code/ "
          f"(the ticket was filed over 178)")
    print()
    print(f"    {'quantity':44} {'today':>7} {'ticket':>7} {'drift':>7}")
    for label, now, then in rows:
        print(f"    {label:44} {now:>7} {then:>7} {now - then:>+7}")
    print()
    print("    WHAT ARRIVED SINCE THE TICKET WAS FILED (directories, not sites):")
    print(f"      tee directories today : {', '.join(tee_dirs)}")
    print("      the ticket names four : eps_spec_sweep_372e, l2_conditionality_28ff,")
    print("                              lstar_789d, state_restructure_ea0e")
    extra = [d for d in tee_dirs if d not in
             ("eps_spec_sweep_372e", "l2_conditionality_28ff", "lstar_789d",
              "state_restructure_ea0e")]
    print(f"      not in the ticket     : {', '.join(extra) if extra else '(none)'}")
    print()
    print("    A DRIFT HERE IS NOT A FINDING AGAINST c9876.  It is the same fact mg-724a's")
    print("    gate split RECORDED from GATED fields over: a count whose population is the")
    print("    whole corpus is a dated reading and is expected to go stale.  What would be a")
    print("    finding is the detector changing, and §1 is where that would show.")
    print()

    print("§3  WHAT a2/a3/a4 WILL ADJUDICATE")
    print("-" * 92)
    print(f"    a2  the {len(tee)} tee sites in {len(tee_dirs)} directories — run two ways")
    print(f"    a3  the {len(bare)} directories with no falsification evidence")
    print(f"    a4  the {len(mem)} membership candidates in {len(mem_dirs)} directories")
    print()
    print("    ORDER IS THE TICKET'S: smallest population and highest prior first.")
    print()
    print("a1 RESULT: index re-measured, detector identity checked by digest.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
