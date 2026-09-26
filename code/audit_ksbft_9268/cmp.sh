#!/bin/sh
# cmp.sh A_ARGS -- B_ARGS : per-depth (nodes cert lp cut frontier) rows of aud vs tree
AUD=$1; TREE=$2; shift 2
a=$(mktemp); b=$(mktemp)
$AUD $1 | awk '/^depth/{print $2,$4,$6,$8,$10,$12}' > $a
$TREE $2 | awk '/^depth/{print $2,$4,$6,$8,$10,$12}' > $b
if [ -s $a ] && cmp -s $a $b; then echo "IDENTICAL ($(awk '{s+=$2}END{print s}' $a) nodes)"; else echo DIFFER; paste $a $b; fi
rm -f $a $b
