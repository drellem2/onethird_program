#!/usr/bin/env python3
"""mg-9bc2 — seed the twin's pin at the revision it was ACTUALLY last reconciled against.

THE ONE DECISION THIS FILE MAKES, AND WHY IT IS NOT `HEAD`.  The obvious way to install a
pin is to compute it from `STATE.md` as it stands today.  That would be WRONG, and wrong in
the exact direction this ticket is about: it would record that the twin had been reconciled
today, when nothing about the twin's content changed.  The control would come up clean on a
document known to be stale, and the pin would be a second false provenance claim installed
to replace the first one.

The honest seed is the last commit at which the twin's CONTENT was edited, because that is
the last moment anybody put the two documents side by side:

    276aead  2026-08-07  "ROW 3b's 0/132 IS A SAMPLING ARTIFACT — … in BOTH files (mg-55f2)"

`git log --follow docs/state-of-the-wall.html` has five entries and this is the newest.  Its
diffstat touches `STATE.md` and `docs/state-of-the-wall.html` together, which is what makes
it a reconciliation rather than a one-sided edit.

So the pin is seeded at `276aead` and THE CONTROL IS EXPECTED TO FIRE ON ITS FIRST RUN.
That is the point.  A detector installed green tells you nothing about whether it works.
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib9bc2 as L  # noqa: E402
from twin_pin import ROOT, STATE, TWIN  # noqa: E402

# The last commit whose diffstat contains BOTH STATE.md and the twin.
PIN_COMMIT = "276aead"

NOTE = ("HAND-MAINTAINED, NOT GENERATED — there is no generator; "
        "seeded at the last commit that edited BOTH files")


def main():
    show = subprocess.run(["git", "-C", ROOT, "show", f"{PIN_COMMIT}:STATE.md"],
                          capture_output=True, text=True)
    if show.returncode != 0:
        sys.exit(f"cannot read STATE.md at {PIN_COMMIT}: {show.stderr.strip()}")
    state_at_pin = show.stdout

    touched = subprocess.run(
        ["git", "-C", ROOT, "show", "--name-only", "--format=", PIN_COMMIT],
        capture_output=True, text=True).stdout.split()
    for required in ("STATE.md", "docs/state-of-the-wall.html"):
        if required not in touched:
            sys.exit(f"REFUSED: {PIN_COMMIT} does not touch {required}, so it is not a "
                     f"reconciliation and must not be used as the seed.")

    full = subprocess.run(["git", "-C", ROOT, "rev-parse", PIN_COMMIT],
                          capture_output=True, text=True).stdout.strip()[:12]
    date = subprocess.run(["git", "-C", ROOT, "log", "-1", "--format=%cs", PIN_COMMIT],
                          capture_output=True, text=True).stdout.strip()

    import hashlib
    state_sha = hashlib.sha256(state_at_pin.encode("utf-8")).hexdigest()

    digests = L.row_digests(state_at_pin)
    block = L.render_pin(full, date, state_sha, digests, NOTE)

    twin_text = open(TWIN, encoding="utf-8").read()
    if L.parse_pin(twin_text) is not None:
        sys.exit("REFUSED: the twin already carries a pin.  Use twin_pin.py --reconcile.")
    with open(TWIN, "w", encoding="utf-8") as fh:
        fh.write(block + "\n" + twin_text)

    print(f"seeded pin at {full} ({date}) with {len(digests)} ledger rows")
    print(f"STATE.md@{PIN_COMMIT} sha256 {state_sha}")
    print("the control is EXPECTED to report drift now — that is the seed doing its job")
    return 0


if __name__ == "__main__":
    sys.exit(main())
