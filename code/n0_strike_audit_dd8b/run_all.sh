#!/bin/sh
# mg-dd8b — run every instrument of this audit. s4 exits 1 BY DESIGN (Finding 1b).
set -x
python3 "$(dirname "$0")/s1_census.py"    > "$(dirname "$0")/out_s1_census.txt"    2>&1
python3 "$(dirname "$0")/s2_format.py"    > "$(dirname "$0")/out_s2_format.txt"    2>&1
python3 "$(dirname "$0")/s3_overclaim.py" > "$(dirname "$0")/out_s3_overclaim.txt" 2>&1
python3 "$(dirname "$0")/s4_sites.py"     > "$(dirname "$0")/out_s4_sites.txt"     2>&1
