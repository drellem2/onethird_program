"""mg-e7bc -- RUN mg-04a8'S REPAIRED LABEL CHECK AS A PROCESS, ON ONE ARTIFACT.

    python3 checkrun.py <artifact> [battery-exit-code] [registered-substring...]

    exit 0  the check says every scored row carries the label independently
            derived for it
    exit 1  THE CHECK GOES RED
    exit 2  the check could not be run at all

mg-e7bc asks for an EXIT CODE, and `check_labels` is a function returning a
tuple.  A tuple in a transcript is a description; an exit code is something a
shell, a CI job or the next generation of this lineage can act on without
reading the prose around it.  So the subject's function is imported unmodified
and this file is the only thing wrapped around it: read the artifact, derive the
inputs here, call it, translate its verdict into a status.

WHAT IS IMPORTED AND WHAT IS NOT.  `check_labels` is imported -- it IS the thing
under audit, and auditing a paraphrase of it would be worthless.  Everything fed
to it is derived by `kerne7bc`: the row population, the baseline CANNOT FAIL set
(read from the committed clean artifact's own summary block, since a corrupted
artifact's may be a lie) and the registration.  Importing `d2_deletion` runs its
module body only; `main()` is under a `__main__` guard and no battery runs.

THIS FILE'S ANSWER WOULD DIFFER UNDER: `check_labels` changing its signature or
its verdict, which is the point; and under the committed artifact's CANNOT FAIL
block moving, which is why that derivation is printed on every run rather than
assumed.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from kerne7bc import ART, INSTR, baseline_cannot, read, scored_rows  # noqa: E402

sys.path.insert(0, INSTR)

try:
    from d2_deletion import check_labels                             # noqa: E402
except Exception as exc:                                             # pragma: no cover
    sys.stderr.write("cannot import the repaired check: %r\n" % (exc,))
    sys.exit(2)


def main(argv):
    if not argv:
        sys.stderr.write(__doc__)
        return 2
    path = argv[0]
    code = int(argv[1]) if len(argv) > 1 else 0
    registered = list(argv[2:])
    text = read(path)
    cannot = baseline_cannot(read(ART))
    ok, msg, notes = check_labels(os.path.basename(path), text, code,
                                  registered, cannot)
    print("artifact      : %s (%d bytes, %d scored rows)"
          % (path, len(text), len(scored_rows(text))))
    print("battery exit  : %d (supplied)" % code)
    print("registered    : %s" % (registered or "none"))
    print("baseline CANNOT FAIL set, from the COMMITTED artifact: %d name(s)"
          % len(cannot))
    print("verdict       : %s" % ("GREEN -- the check says yes"
                                  if ok else "RED -- the check fires"))
    print("message       : %s" % msg)
    for n in notes:
        print("  note        : %s" % n)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
