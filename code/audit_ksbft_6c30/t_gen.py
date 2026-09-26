import time, sys
from eng import gen, A022493, Poset
for n in range(1, int(sys.argv[1]) + 1):
    t = time.time(); L = list(gen(n)); s = set(L)
    print(n, len(L), len(s), A022493[n], len(L) == A022493[n] == len(s), f"{time.time()-t:.1f}s", flush=True)
