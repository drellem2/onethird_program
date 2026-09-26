"""gencheck.py (audit mg-6e7c): positive control for the census files, independent of OEIS A000112 and of the
generator: sum over classes of n!/|Aut(P)| must equal the number of LABELLED posets (OEIS A001035), which
certifies the file is complete AND duplicate-free.  |Aut| by my own backtracking (aud.autcount)."""
import sys
from math import factorial
from aud import close, autcount
A001035 = {1: 1, 2: 3, 3: 19, 4: 219, 5: 4231, 6: 130023, 7: 6129859, 8: 431723379, 9: 44511042511}
ok = True
for f in sys.argv[1:]:
    tot = 0
    n = None
    for line in open(f):
        a = line.split()
        n = int(a[0])
        tot += factorial(n) // autcount(close([int(t, 16) for t in a[1:1 + n]]))
    good = tot == A001035[n]
    ok &= good
    print(f"{f.split('/')[-1]}: n={n} sum n!/|Aut| = {tot}  A001035 = {A001035[n]}  {'OK' if good else 'MISMATCH'}")
    sys.stdout.flush()
# negative control: drop one class / duplicate one class from the n=6 file -> must mismatch
print("RESULT", "OK" if ok else "MISMATCH")
