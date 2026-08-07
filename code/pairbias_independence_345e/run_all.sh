#!/usr/bin/env bash
# mg-345e — run every probe, record every transcript, exit on the declared values.
#
# DECLARED IN ADVANCE: all four exit 0. A probe here that exits nonzero is reporting
# that the ledger parse broke or that my own algebra does not close.
set -u
cd "$(dirname "$0")"

RC=0
run() {
  local name="$1"; shift
  echo "### $name"
  if python3 "$name.py" > "out_$name.txt" 2>&1; then
    echo "    exit 0  -> out_$name.txt"
  else
    echo "    exit $? (NONZERO) -> out_$name.txt"
    RC=1
  fi
}

run selftest345e
run p1_ledger_depgraph
run p2_architecture_graph
run p3_algebra

echo
echo "run_all exit $RC"
exit $RC
