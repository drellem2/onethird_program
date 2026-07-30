"""R1b8 -- the n = 8 entry of R1d's corrected table, on its own because it
takes about three minutes.

mg-af28's ledger B2 gives 12/16 999 at n = 8 for the class "posets P with J(P)
an interval of Young's lattice".  12 is the number of STRAIGHT cell posets with
8 cells; the class B2 names is the SKEW ones.  This counts them.

mg-6ad0 reported 360 and stated the provenance (same function, run behind a
flag).  This is a third instrument, and 360 is either reproduced or it is not.
FALSIFIER: any count other than 360, or a straight count other than af28's 12.

The last line is machine-readable so `run_all.sh` can feed the number to
`r1_exactly.py` rather than have anything hard-code it.
"""

import sys
import time

from kern41aa import canon, partitions, skew_poset
from r1_exactly import skew_shapes, A000112

OUT = sys.stdout


def main():
    print("=" * 78, file=OUT)
    print("R1b8  The corrected n = 8 count.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    t = time.time()
    straight = {canon(skew_poset(l)[0]) for l in partitions(8)}
    sk = skew_shapes(8)
    dt = time.time() - t
    print("   n   straight D_lam   skew = interval posets   all posets    af28   corrected",
          file=OUT)
    print("   8   %14d   %22d   %10d  %6.4f    %8.4f"
          % (len(straight), len(sk), A000112[8], len(straight) / A000112[8],
             len(sk) / A000112[8]), file=OUT)
    print(file=OUT)
    print("  af28's straight count reproduced: %s (it said 12)."
          % ("YES" if len(straight) == 12 else "NO -- %d" % len(straight)), file=OUT)
    print("  mg-6ad0's skew count reproduced:  %s (it said 360)."
          % ("YES" if len(sk) == 360 else "NO -- %d" % len(sk)), file=OUT)
    print("  wall clock: %.0f s.  All 16 999 posets on 8 elements are NOT"
          % dt, file=OUT)
    print("  enumerated here -- the denominator is A000112, cited, exactly as", file=OUT)
    print("  af28 cited it; only the numerators are computed.", file=OUT)
    print(file=OUT)
    print("=" * 78, file=OUT)
    print("SUMMARY r1b_skew8: straight %d, skew %d, of %d"
          % (len(straight), len(sk), A000112[8]), file=OUT)
    print("=" * 78, file=OUT)
    print("SKEW8 %d" % len(sk), file=OUT)


if __name__ == "__main__":
    main()
