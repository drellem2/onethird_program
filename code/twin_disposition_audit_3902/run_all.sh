#!/bin/sh
# mg-3902 — does the rendered twin's pin resolve against git, and does that check fail?
#
# THE RUNNER IS WHERE THIS LINEAGE KEEPS GETTING CAUGHT, so the shape below is not stylistic.
# `code/rendered_twin_pin_9bc2/run_all.sh` printed `CLEAN` over a drifted control (its `$?`
# was tee's), and later printed `CLEAN` over a control that NEVER RAN (exit 127 matched none
# of its branches and fell through to the green).  Both are recorded in that directory's
# COVERAGE.md.  So this runner:
#
#   * redirects and `cat`s rather than piping, because POSIX sh has no PIPESTATUS and `$?`
#     after a pipe is the LAST command's, not the instrument's;
#   * requires the control to have PRINTED A VERDICT LINE before any branch is taken, because
#     python exits non-zero both when the control decides and when it dies in a traceback;
#   * refuses an exit code outside the set the control documents, instead of treating an
#     unknown code as the good case.
#
# Exit: 0 clean · 2 the pin lies, the control never reached a verdict, or a mutation was missed.
set -u

HERE=$(dirname "$0")
STATUS=0

echo "############################################################ mg-3902 pin resolution"
python3 "$HERE/a2_pin_resolves.py" > "$HERE/out_pin_resolves.txt" 2>&1
CONTROL=$?
cat "$HERE/out_pin_resolves.txt"

echo
echo "############################################################ mg-3902 negative control"
python3 "$HERE/a3_negative_control.py" > "$HERE/out_negative_control.txt" 2>&1
NEGATIVE=$?
cat "$HERE/out_negative_control.txt"

echo
echo "############################################################ mg-3902 vs the shipped control"
python3 "$HERE/a1_prerepair.py" > "$HERE/out_a1_prerepair.txt" 2>&1
COMPARE=$?
cat "$HERE/out_a1_prerepair.txt"

echo
echo "================================================================================"
echo "control exit  : $CONTROL   (0 clean · 2 the pin states something false about git)"
echo "compare exit  : $COMPARE   (0 = the shipped control's blindness still reproduces)"
echo "negative exit : $NEGATIVE   (0 = every mutation caught)"

# THE VERDICT LINE MUST EXIST.  A control that died before deciding and a control that decided
# NO both leave a non-zero exit; only the printed verdict separates them.
if ! grep -q '^VERDICT:' "$HERE/out_pin_resolves.txt"; then
    echo "BROKEN — the control never printed a VERDICT line, so its exit code is not a"
    echo "         decision.  Read out_pin_resolves.txt; do not read this as a result."
    exit 2
fi
echo "control verdict: $(grep -m1 '^VERDICT:' "$HERE/out_pin_resolves.txt")"

case "$CONTROL" in
    0) ;;
    2) STATUS=2 ;;
    *) echo "BROKEN — the control exited $CONTROL, which is not one of its documented codes."
       exit 2 ;;
esac

case "$NEGATIVE" in
    0) ;;
    1|2) echo "BROKEN — the negative control found a HOLE or refused: this control has not"
         echo "         been shown to fail, so its green above is not evidence."
         STATUS=2 ;;
    *) echo "BROKEN — the negative control exited $NEGATIVE, outside its documented codes."
       exit 2 ;;
esac

# a1 REFUSES (exit 2) when twin_pin.py has moved away from origin/main, because its OLD column
# would then be comparing the new check against a copy of itself.  That refusal is a real
# finding about this suite's own meaning and must not be swallowed; a HOLE (exit 1) is one too.
case "$COMPARE" in
    0) ;;
    1|2) echo "BROKEN — the comparison against the shipped control refused or found a hole."
         echo "         Read out_a1_prerepair.txt: this suite's justification is what moved."
         STATUS=2 ;;
    *) echo "BROKEN — a1_prerepair.py exited $COMPARE, outside its documented codes."
       exit 2 ;;
esac

if [ "$STATUS" -eq 0 ]; then
    echo "CLEAN — the twin's pin resolves, names the revision it digests, and this control"
    echo "        was demonstrated to fail on five ways it could stop being true."
else
    echo "RED — see above."
fi
exit "$STATUS"
