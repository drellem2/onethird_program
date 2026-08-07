#!/usr/bin/env bash
# a7_history — the PREMISE'S SECOND HALF, checked: "never attacked by any arc".
#
# STATE.md (mg-a58f's row, audited mg-d112) says:
#     "`lambda_std -> 1` as stated here needs only (LIB-weak) E[inv_e] = o(n^2)
#      -- never attacked by any arc."
# mg-c3ca's ticket repeats it and mg-c3ca's Sec.0 turns it into
#     "'never attacked' is an opportunity, not an oversight."
#
# That is a claim about the corpus's HISTORY and it is checkable.  This script does
# not settle whether an attack would have been GOOD; it establishes what the record
# contains, and it prints the population it searched so the negative is not silence.
#
# EXIT 0 always: this is a census, not a gate.
set -u
cd "$(dirname "$0")"
REPO=$(cd ../.. && pwd)
CUT=81214a9        # mg-c3ca's own commit; "before this" is the window that matters

echo "=============================================================================="
echo "a7_history -- is (LIB-weak) really NEVER ATTACKED?  (audit target 1, half 2)"
echo "=============================================================================="
echo

echo "------------------------------------------------------------------------------"
echo "H1. THE POPULATION SEARCHED (printed first, so the negative is not silence)"
echo "------------------------------------------------------------------------------"
MGROOT="${MG_ROOT:-$HOME/.macguffin}"
echo "  mg store root        : $MGROOT"
if [ -d "$MGROOT" ]; then
  echo "  mg item files        : $(find "$MGROOT/work" -name 'mg-*.md*' 2>/dev/null | wc -l | tr -d ' ')"
else
  echo "  mg store NOT FOUND -- H2 cannot run and says so rather than reporting 0"
fi
echo "  merged docs (docs/)  : $(git -C "$REPO" ls-tree -r --name-only "$CUT" -- docs | wc -l | tr -d ' ')"
echo "  merged code dirs     : $(git -C "$REPO" ls-tree -r --name-only "$CUT" -- code | wc -l | tr -d ' ')"
echo "  commits before $CUT  : $(git -C "$REPO" rev-list --count "$CUT^" 2>/dev/null)"
echo

echo "------------------------------------------------------------------------------"
echo "H2. mg ITEMS MENTIONING (LIB-weak) OR ITS STATEMENT, ANYWHERE"
echo "------------------------------------------------------------------------------"
if [ -d "$MGROOT" ]; then
  echo "  files containing the literal string 'LIB-weak':"
  grep -rl 'LIB-weak' "$MGROOT/work" 2>/dev/null | sed "s|$MGROOT/work/||" | sort | head -40
  echo "  count: $(grep -rl 'LIB-weak' "$MGROOT/work" 2>/dev/null | wc -l | tr -d ' ')"
  echo
  echo "  of those, how many have (LIB-weak) as their TITLE subject (a deliverable"
  echo "  aimed at it) rather than a mention in passing:"
  grep -rl 'LIB-weak' "$MGROOT/work" 2>/dev/null | while read -r f; do
    t=$(grep -m1 -i '^title:\|^# ' "$f" 2>/dev/null | head -1)
    case "$t" in *LIB-weak*) echo "    TITLE HIT: $(basename "$f") :: $t";; esac
  done
  echo "  (a blank list here means: 0 items were FILED against (LIB-weak))"
  echo
  echo "  SPLIT BY DATE AGAINST mg-c3ca's OWN FILING (2026-08-05 23:49Z) -- the only"
  echo "  split that can test \"never attacked\", since everything after is a consequence:"
  for f in $(grep -rl 'LIB-weak' "$MGROOT/work" 2>/dev/null); do
    id=$(basename "$f" | sed 's/\.md.*//;s/\.result.*//')
    cr=$(mg show "$id" 2>/dev/null | sed -n 's/^Created: *//p' | head -1)
    ti=$(mg show "$id" 2>/dev/null | sed -n 's/^Title: *//p' | head -1 | cut -c1-72)
    [ -z "$cr" ] && continue
    if [[ "$cr" < "2026-08-05 23:49" ]]; then when="BEFORE"; else when="after "; fi
    echo "    $when  $id  $cr  $ti"
  done | sort -u
  echo
  echo "  Only the BEFORE rows can bear on the claim.  A BEFORE row is an ATTACK only"
  echo "  if (LIB-weak) is its deliverable, which the TITLE HIT list above tests."
fi
echo

echo "------------------------------------------------------------------------------"
echo "H3. MERGED DOCS AT $CUT^ (i.e. BEFORE mg-c3ca) MENTIONING IT"
echo "------------------------------------------------------------------------------"
for pat in 'LIB-weak' 'o(n^2)' 'o(n²)'; do
  echo "  pattern: $pat"
  git -C "$REPO" grep -l -F "$pat" "$CUT^" -- docs STATE.md 2>/dev/null \
    | sed 's|^[^:]*:||' | sort -u | sed 's/^/    /'
  n=$(git -C "$REPO" grep -l -F "$pat" "$CUT^" -- docs STATE.md 2>/dev/null | wc -l | tr -d ' ')
  echo "    -> $n file(s)"
done
echo

echo "------------------------------------------------------------------------------"
echo "H4. WHERE THE SENTENCE ITSELF COMES FROM, AND WHETHER ITS AUDIT TOUCHED IT"
echo "------------------------------------------------------------------------------"
echo "  the sentence, at $CUT^ :"
git -C "$REPO" grep -n -F 'never attacked by any arc' "$CUT^" -- STATE.md docs 2>/dev/null \
  | cut -c1-200 | sed 's/^/    /'
echo
echo "  it belongs to the mg-a58f row.  mg-d112 is its audit.  Does the audit document"
echo "  mention the claim at all?"
AUD=$(git -C "$REPO" ls-tree -r --name-only "$CUT^" -- docs | grep -i 'Bbias.*Audit' | head -1)
echo "    STATE.md names it: docs/OneThird-Bbias-Locality-Lemma-IndependentAudit.md"
echo "    present in this repo at $CUT^ : ${AUD:-NO -- NOT PRESENT}"
echo "    present in this repo at HEAD  : $(git -C "$REPO" ls-tree -r --name-only HEAD -- docs | grep -ci 'Bbias.*Audit') file(s)"
echo "    present in one_third_width_three: $(ls /Users/daniel/research/one_third_width_three/docs 2>/dev/null | grep -ci 'Bbias.*Audit') file(s)"
echo "    (so the audit that STATE.md credits for this row is NOT LOCATABLE, and"
echo "     therefore whether mg-d112 checked the \`never attacked\` half is UNVERIFIABLE"
echo "     from the record.  That is a measured absence, not an accusation.)"
if [ -n "${AUD:-}" ]; then
  for pat in 'never attacked' 'LIB-weak' 'o(n^2)' 'o(n²)'; do
    c=$(git -C "$REPO" show "$CUT^:$AUD" 2>/dev/null | grep -c -F "$pat")
    echo "    occurrences of '$pat' in the audit: $c"
  done
  echo "  NON-VACUITY: the same file's length is $(git -C "$REPO" show "$CUT^:$AUD" | wc -l | tr -d ' ') lines,"
  echo "  and it contains 'LIB' $(git -C "$REPO" show "$CUT^:$AUD" | grep -c 'LIB') times -- so a 0 above is a"
  echo "  measured absence in a file that is otherwise about exactly this material."
fi
echo

echo "------------------------------------------------------------------------------"
echo "H5. THE ATTEMPT INDEX -- what the corpus records as having been TRIED"
echo "------------------------------------------------------------------------------"
echo "  rows of STATE.md's attempt index at $CUT^ (verdict column only):"
git -C "$REPO" show "$CUT^:STATE.md" 2>/dev/null \
  | awk '/^\| verdict \| attempt/,/^$/' | sed -n 's/^| *\([^|]*\) *| *\([^|]*\) *|.*/    [\1] \2/p' \
  | cut -c1-140
echo
echo "  READ THIS AS THE POPULATION FOR THE NEGATIVE: if (LIB-weak) had been attacked,"
echo "  this index is where the attempt would be recorded, and the corpus's own rule is"
echo "  that the index exists 'so nothing is re-walked'."
echo
echo "=============================================================================="
echo "a7_history done."
echo "=============================================================================="
