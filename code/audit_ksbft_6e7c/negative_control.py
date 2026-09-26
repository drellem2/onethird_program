"""negative_control.py (audit mg-6e7c): planted falsehoods that this audit's instruments must CATCH.
Each line prints CAUGHT or MISSED; exit 1 on any MISSED."""
import sys
from fractions import Fraction as F
from aud import parse, ups, incp, probs, ladders, brute, prob_aug, autcount
from math import factorial
from pinch import pinch_levels_event, pinch_levels_struct
missed = 0
def rep(tag, caught):
    global missed
    print(("CAUGHT " if caught else "MISSED ") + tag)
    missed += not caught
P9 = parse("9 0 0 2 2 3 b 2b 2f 7f")
e, B = probs(P9)
P = lambda a, b: F(B[a][b], e)
# 1. a planted wrong witness value (doc's 118/197 perturbed) is detected by the 3-engine agreement
rep("planted P9 P[2<5]=119/197 differs from all engines", P(2, 5) != F(119, 197) and prob_aug(P9, 2, 5, e) != F(119, 197))
# 2. Swap Ladder steps WITHOUT H1 increase: in 2+1 (3 0 0 2), x=2 (above 1), b=0; W = Up[0]-Up[2] = {0} is full,
#    steps (P[2<0], P[0<2]) = (1/3, 2/3) increase, so dropping down(x) <= down(b) breaks Thm 1.4(a)
d = parse("3 0 0 2"); e3, B3 = probs(d)
rep("H1-violating full ladder (2;0) in 2+1 has increasing steps 1/3 -> 2/3", F(B3[2][0], e3) < F(B3[0][2], e3))
# 3. Doubling without up(x) <= up(b): some ladder has t_1 != t_0 (W8)
W8 = parse("8 0 0 0 4 4 6 16 2f"); e8, B8 = probs(W8); P8 = lambda a, b: F(B8[a][b], e8)
u8 = ups(W8)
found = any(W8[x] == W8[b] and len(ch) >= 2 and (u8[x] & ~u8[b]) and r[1] - r[0] != r[0]
            for x, b, ch, full, r in ladders(W8, u8, P8))
rep("Doubling identity fails when up(x) <= up(b) is dropped (W8)", found)
# 4. Pinch: the sloppy structural condition (no 'M above w') disagrees with the event somewhere
Y = parse("6 0 0 2 2 3 f")
rep("sloppy ordinal-sum condition disagrees with the event on 6 0 0 2 2 3 f",
    pinch_levels_event(Y, 0) != pinch_levels_struct(Y, 0, sloppy=True))
# 5. generator certificate: a dropped class breaks sum n!/|Aut| = A001035
L = [parse("3 0 0 0"), parse("3 0 1 3"), parse("3 0 1 1"), parse("3 0 0 3")]  # 4 of the 5 posets on 3 points
rep("incomplete n=3 list fails A001035 (19)", sum(factorial(3) // autcount(d) for d in L) != 19)
print("RESULT", "ALL CAUGHT" if not missed else f"{missed} MISSED")
sys.exit(1 if missed else 0)
