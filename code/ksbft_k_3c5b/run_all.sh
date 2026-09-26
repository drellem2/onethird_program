#!/bin/sh
# run_all.sh (mg-3c5b): Appendix A / 67/242 / theta-number checks for notes/lemma-W-polynomial-range-bound.tex
# and docs/KSBFT-K-writeup-novelty.md.  Deterministic, single process, < 2 s.  Also rebuilds the note's PDF
# if pdflatex is available.  Writes then moves, so a failure keeps the committed transcript.
set -e
cd "$(dirname "$0")"
python3 appA_check.py > out_appA_check.txt.tmp && mv out_appA_check.txt.tmp out_appA_check.txt
grep -q '^ALL OK$' out_appA_check.txt
grep -q 'NEG CONTROL .* FIRES' out_appA_check.txt
TEX=/Library/TeX/texbin/pdflatex
if [ -x "$TEX" ]; then
  ( cd ../../notes && for i in 1 2; do "$TEX" -interaction=nonstopmode -halt-on-error lemma-W-polynomial-range-bound.tex >/dev/null; done
    rm -f lemma-W-polynomial-range-bound.aux lemma-W-polynomial-range-bound.log lemma-W-polynomial-range-bound.out )
fi
echo "run_all (mg-3c5b): ALL OK, negative control fired"
