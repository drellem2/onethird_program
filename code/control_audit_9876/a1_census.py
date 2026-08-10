#!/usr/bin/env python3
"""mg-9876 — step 1 of the ticket: enumerate every control, assertion and selftest arm, and
STATE THE SIZE, so the audit's own coverage is legible rather than implied.

TWO HALVES, AND ONLY ONE OF THEM IS TRUSTWORTHY.  The registry in `lib9876.ARMS` is typed by
hand, because a regex cannot tell an arm from a `print`.  A hand list's failure mode is
silent incompleteness — it says 38 and nobody can tell whether the real number is 41.  So the
list's COMPLETENESS is not asserted here, it is checked: this script rediscovers every
arm-shaped site in the five source files mechanically and requires

    every discovered site to be claimed by at least one registered arm, and
    every registered arm's declared sites to resolve in the file it names.

An unclaimed site FAILS this census (exit 2).  That is the whole point: when somebody adds a
seventh section to `twin_pin.py` and does not register it, the census refuses instead of
quietly reporting a stale 38.  `a3_auditor_selftest.py` demonstrates that refusal rather than
claiming it.

WHAT THIS CENSUS DOES NOT DO.  It does not say whether an arm can fail — that is
`a2_discriminate.py`, and it is a different question with a different method.  A site that
exists is not a check that works; that confusion is the reason this ticket exists.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib9876 as L  # noqa: E402


def main(target_dir=None):
    """`target_dir` defaults to the audited directory; a3 passes a doctored COPY.

    The census must be runnable against a tree it did not expect, or its refusal could never
    be demonstrated — which would make the completeness claim exactly the kind of assertion
    this ticket exists to reject.
    """
    target_dir = target_dir or L.TARGET
    out = []

    def emit(line=""):
        out.append(line)

    emit("=" * 92)
    emit(f"mg-9876 — ARM CENSUS of {os.path.relpath(target_dir, L.ROOT)}")
    emit("=" * 92)
    emit()
    emit("An ARM is one place that can say NO.  Sections are not arms: twin_pin.py section 5")
    emit("is TWO arms, because `Generated <date>` and an unattributed canonicity claim are two")
    emit("things that could stop happening independently.  run_all.sh is FOUR arms, because")
    emit("its four branches classify four different worlds.")
    emit()

    # ------------------------------------------------------------------ the list
    by_source = {}
    for arm in L.ARMS:
        by_source.setdefault(arm.source, []).append(arm)

    emit("THE LIST")
    emit("-" * 92)
    width = max(len(a.name) for a in L.ARMS)
    for source in L.SOURCES:
        arms = by_source.get(source, [])
        emit(f"  {source}   ({len(arms)} arm(s))")
        for arm in arms:
            emit(f"    {arm.id:<4} §{arm.section:<9} {arm.name.ljust(width)}  grade {arm.grade}")
            emit(f"         subject: {arm.subject}")
        emit()

    emit(f"SIZE: {len(L.ARMS)} arms across {len(L.SOURCES)} source files.")
    emit(f"      by grade — {sum(1 for a in L.ARMS if a.grade == 2)} structural (2), "
         f"{sum(1 for a in L.ARMS if a.grade == 1)} drift/report (1), "
         f"{sum(1 for a in L.ARMS if a.grade == 0)} advisory (0)")
    emit()

    # ------------------------------------------------- the completeness check (machine)
    emit("=" * 92)
    emit("COMPLETENESS — every arm-shaped SITE in the sources must be claimed by an arm")
    emit("=" * 92)
    emit("Discovery is deliberately over-broad.  An unclaimed site is a FINDING and fails this")
    emit("census; it is how a check added without registration stops being invisible.")
    emit()

    sites = L.discover_sites(target_dir)
    emit(f"  discovered sites: {len(sites)}")
    for source in L.SOURCES:
        n = sum(1 for s in sites if s[0] == source)
        emit(f"    {source:<22} {n}")
    emit()

    # resolve every arm's declared sites to discovered ones
    texts = {name: L.read(os.path.join(target_dir, name)).split("\n")
             for name in L.SOURCES}
    claimed = set()
    unresolved = []
    for arm in L.ARMS:
        for needle in arm.sites:
            hits = [(arm.source, i + 1) for i, line in enumerate(texts[arm.source])
                    if needle in line]
            if not hits:
                unresolved.append((arm.id, needle))
                continue
            for h in hits:
                claimed.add(h)

    discovered = {(s[0], s[1]) for s in sites}
    unclaimed = sorted(discovered - claimed)
    phantom = sorted(claimed - discovered)

    if unresolved:
        emit(f"  FAIL  {len(unresolved)} registered site(s) do not resolve in the named file:")
        for arm_id, needle in unresolved:
            emit(f"        {arm_id}: {needle!r}")
    else:
        emit(f"  PASS  all {sum(len(a.sites) for a in L.ARMS)} registered site strings resolve.")
    emit()

    if unclaimed:
        emit(f"  FAIL  {len(unclaimed)} discovered site(s) claimed by NO registered arm:")
        for source, lineno in unclaimed:
            emit(f"        {source}:{lineno}  {texts[source][lineno - 1].strip()[:70]}")
        emit("        Register them or explain them.  An unregistered check is a check nobody")
        emit("        audits, which is one layer of exactly this ticket's defect.")
    else:
        emit(f"  PASS  all {len(discovered)} discovered sites are claimed by a registered arm.")
    emit()

    if phantom:
        emit(f"  note  {len(phantom)} registered site(s) resolve to lines the discovery patterns")
        emit("        do not match — these are arms whose site string is a body line rather than")
        emit("        the arm's head.  Listed so the difference is not mistaken for coverage:")
        for source, lineno in phantom:
            emit(f"        {source}:{lineno}  {texts[source][lineno - 1].strip()[:70]}")
        emit()

    ok = not unresolved and not unclaimed
    emit("=" * 92)
    if ok:
        emit(f"CENSUS COMPLETE — {len(L.ARMS)} arms, {len(discovered)} sites, none unclaimed.")
    else:
        emit("CENSUS INCOMPLETE — the hand registry does not cover the sources.  Exit 2.")
    emit("=" * 92)

    print("\n".join(out))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
