#!/bin/sh
# tree_sample.sh (mg-9268): re-run a random sample of the AUTHOR's D=7 slices
# with the committed tree.c and diff them byte-for-byte against the committed
# transcripts ../ksbft_finite_state/out_d7/part_I.txt.
set -e
cd "$(dirname "$0")"
J=${POGO_WORKER_CORES:-3}
T=$(mktemp -d)
cc -O2 -Wall -o "$T/tree" ../ksbft_finite_state/tree.c
SLICES=$(python3 -c "import random; r=random.Random(9268); print(' '.join(map(str, sorted(r.sample(range(120), 9)))))")
echo "slices (random.Random(9268).sample(range(120), 9)): $SLICES"
echo $SLICES | tr ' ' '\n' | xargs -P "$J" -I{} sh -c "$T/tree 7 58 1 3 split:{}/120@9 > $T/part_{}.txt 2>/dev/null"
for i in $SLICES; do
  if cmp -s "$T/part_$i.txt" "../ksbft_finite_state/out_d7/part_$i.txt"; then echo "part_$i IDENTICAL"; else echo "part_$i DIFFERS"; fi
done
rm -rf "$T"
