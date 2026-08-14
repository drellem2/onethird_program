#!/bin/sh
# mg-372e — the whole sweep, ~3 s, no dependencies beyond python3 and git.
#
# NO `| tee`, SINCE mg-528e, AND THAT IS NOT TIDINESS.  A pipeline's exit status
# is the LAST command's -- tee's -- so every non-zero exit these scripts raise
# used to be swallowed by the runner.  That did not matter while stdout was the
# only thing they said; it matters now, because the pinned reading is on stdout
# and the LIVE re-check of the working tree is on stderr AND IN THE EXIT CODE.
# `mg-188d` recorded the same defect in this file and left it (it was not its to
# repair); it is repaired here because this change is what made it load-bearing.
#
# The redirect goes to a temp file and is MOVED into place, so a script that
# fails leaves the committed transcript untouched instead of truncating it under
# `set -e`.  Since the corpus is pinned, a successful run is byte-identical and
# `git status` stays clean -- which retires this directory's other warning, that
# the one command a reader would reach for to check the transcripts destroyed
# them.
set -e
here=$(cd "$(dirname "$0")" && pwd)

take() {   # take <script> <transcript>
    python3 "$here/$1" > "$here/.$2.tmp"
    mv "$here/.$2.tmp" "$here/$2"
    cat "$here/$2"
}

take s1_census.py   out_s1_census.txt
take s2_classify.py out_s2_classify.txt
take s3_control.py  out_s3_control.txt
