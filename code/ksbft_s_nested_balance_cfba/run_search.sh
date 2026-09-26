#!/bin/sh
# run_search.sh (mg-cfba): the adversarial counterexample searches quoted in doc sec. 2.3 (instrument only).
# 3 processes (POGO_WORKER_CORES budget), ~25 min wall.  Outputs out_search_*.txt / out_search2_*.txt.
cd "$(dirname "$0")"
T13="13 0 1 0 3 5 17 3f b bf 1ff 7f 7ff 47f"
Q0="$(python3 -c 'from fam import *; P9=parse("9 0 0 2 2 3 b 2b 2f 7f"); lo=grow(P9,0,1); print(fmt(glue(lo,dual(lo),1)))')"
(for s in 1 2 3 4; do python3 search.py 10 $s 400; done > out_search_n10.txt) &
(for s in 1 2 3 4; do python3 search.py 11 $s 400; done > out_search_n11.txt) &
(for s in 1 2 3 4; do python3 search.py 12 $s 400; done > out_search_n12.txt) &
wait
(for s in 1 2; do python3 search.py 13 $s 500; done > out_search_n13.txt) &
(for s in 1 2; do python3 search.py 14 $s 500; done > out_search_n14.txt) &
(for s in 1 2; do python3 search.py 0 $s 300 "$Q0"; done > out_search_q0.txt) &
wait
(python3 search2.py 11 400 10 16 > out_search2_a.txt) &
(python3 search2.py 12 400 12 18 "$T13" > out_search2_b.txt) &
(python3 search2.py 13 300 14 20 "$Q0" "11 0 0 2 2 3 b 2b 2f af bf 1ff" > out_search2_c.txt) &
wait
(NBKEY=dN python3 search2.py 21 500 12 20 "$T13" > out_search2_d.txt) &
(NBKEY=dN python3 search2.py 22 500 14 22 > out_search2_e.txt) &
(NBKEY=cp python3 search2.py 41 400 10 16 > out_search2_i.txt) &
wait
(NBKEY=cp python3 search2.py 44 500 10 16 > out_search2_i2.txt) &
(NBKEY=cp python3 search2.py 42 500 9 16 "9 0 0 2 2 3 b 2b 2f 7f" > out_search2_j.txt) &
(NBKEY=cp python3 search2.py 43 400 11 18 "11 0 0 2 2 3 b 2b 2f af bf 1ff" > out_search2_k.txt) &
wait
(NBKEY=dP python3 search2.py 51 300 6 12 > out_search2_p1.txt) &
(NBKEY=dP python3 search2.py 52 300 8 14 > out_search2_p2.txt) &
wait
