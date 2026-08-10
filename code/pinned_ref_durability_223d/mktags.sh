#!/bin/sh
# mg-223d -- THE REPAIR.  Create (and optionally push) the keep-alive tags
# declared in PINS.tsv.
#
# THIS IS NOT PART OF `run_all.sh` AND IT NEVER WILL BE.  A suite whose subject
# is `an instrument quietly depending on the ref namespace` may not quietly
# mutate the ref namespace.  With no arguments this script PRINTS the commands
# and creates nothing.  `--yes` creates the local tags.  `--push` additionally
# pushes them to `origin`, which is the only thing that makes them durable off
# this one machine.
#
# WHY A TAG AND NOT THE OTHER TWO OPTIONS -- the choice the ticket asked to be
# stated rather than assumed:
#
#   COMMITTING THE TREE HASHES DOES NOT WORK.  It is the option that looks
#   cheapest and it does not do the job at all: a tree sha written into a text
#   file is not a ref, and `git gc` collects an unreachable TREE exactly as it
#   collects an unreachable commit.  Recording `7ef1dac00ca5` tells a future
#   reader WHICH object they needed.  It does not keep it.  `x1_gc.py` runs
#   this to the ground in a throwaway clone rather than asserting it.
#
#   VENDORING THE RECONSTRUCTED INPUT WORKS AND COSTS TOO MUCH.  Copying the
#   517 files' bytes into the tree does make the figure reproducible with no
#   git objects at all -- and it destroys the property that made the
#   reconstruction worth keeping.  cfd9c's finding is that the census is `a
#   function of two 40-character strings and of nothing else on this machine`;
#   vendoring makes it a function of a directory, which is the thing every
#   other figure in this arc already is and every one of which has drifted.
#   It also fixes exactly ONE of 26.
#
#   A TAG IS THE ONLY OPTION THAT SCALES AND THE ONLY ONE THAT PRESERVES THE
#   SUBJECT.  Six of the pinning directories pin the PRE-REBASE commit because
#   the pre-rebase commit IS their subject; for them there is nothing to vendor
#   and nothing to substitute.  A tag makes the object reachable and changes
#   no figure, no file, and no instrument.
#
# WHAT IT COSTS, stated:
#   - 26 refs in `refs/tags/pin/*`, about 50 bytes each.  They will show up in
#     `git tag`, in GitHub's release UI, and in anything that walks tags.
#   - THEY ARE NOT DURABLE UNTIL PUSHED.  A tag made here lives in this
#     machine's object store.  The refinery merges BRANCHES; it does not carry
#     tags.  `--push` is the half that survives this machine.
#   - A tag reads like an endorsement to someone who does not know what it is.
#     The prefix is `pin/` and PINS.tsv says in its header what it means; that
#     is mitigation and not a fix.
#   - Tagging makes the commits permanent, so a genuine mistake now costs a
#     `git tag -d` plus a `git push origin --delete`, both one line, both here.
#
# TO UNDO EVERYTHING THIS SCRIPT DOES:
#     git tag -l 'pin/*' | xargs -r git tag -d
#     git tag -l 'pin/*' | sed 's|^|:refs/tags/|' | xargs -r git push origin
set -u
cd "$(dirname "$0")"

DO=no
PUSH=no
for a in "$@"; do
    case "$a" in
        --yes)  DO=yes ;;
        --push) DO=yes; PUSH=yes ;;
        *) echo "usage: $0 [--yes] [--push]"; exit 2 ;;
    esac
done

MADE=0
SKIP=0
MISS=0
while IFS="$(printf '\t')" read -r short full tag dirs note; do
    case "$short" in ""|\#*) continue ;; esac
    if ! git -C ../.. cat-file -e "$full^{commit}" 2>/dev/null; then
        echo "*** UNRESOLVABLE: $short ($full) -- declared in PINS.tsv and GONE"
        MISS=$((MISS + 1))
        continue
    fi
    if git -C ../.. rev-parse --verify --quiet "refs/tags/$tag" >/dev/null; then
        SKIP=$((SKIP + 1))
        continue
    fi
    if [ "$DO" = yes ]; then
        git -C ../.. tag -a "$tag" "$full" \
            -m "keep-alive anchor for a ref pinned by tracked code (mg-223d).

$short is pinned by: $dirs
It is not an ancestor of main; it is a PRE-REBASE polecat commit that the
refinery replayed onto main under a different sha.  This tag exists so that
deleting the merged branch and running gc does not collect it.  It is an
anchor, not an endorsement.  See code/pinned_ref_durability_223d/PINS.tsv." \
            && MADE=$((MADE + 1))
    else
        echo "git tag -a $tag $full   # pinned by $dirs"
    fi
done < PINS.tsv

if [ "$DO" != yes ]; then
    echo
    echo "DRY RUN -- nothing was created.  Re-run with --yes (local) or --push."
    exit 0
fi

echo
echo "created $MADE, already present $SKIP, unresolvable $MISS"

if [ "$PUSH" = yes ]; then
    echo
    echo "pushing refs/tags/pin/* to origin -- this is the half that survives"
    echo "this machine, and it is the half P6 predicted would be needed."
    git -C ../.. tag -l 'pin/*' | sed 's|^|refs/tags/|' \
        | xargs -r git -C ../.. push origin
fi
