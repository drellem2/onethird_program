#!/bin/sh
# THE ONLY THING THAT ASKS THIS REPOSITORY'S CONTROLS (mg-724a).
#
# This repository is a mathematics corpus, not a program: there is nothing here to compile.
# `build.sh` is the name because the refinery's DEFAULT gate discovery looks for exactly
# `./build.sh` and `./test.sh` at the root when a repository declares no gates of its own
# (internal/refinery/merge.go, defaultGates).  Naming this file that gives the gate TWO
# independent routes to the same command:
#
#   1. .pogo/refinery.toml names it explicitly, which is what runs today;
#   2. if that file is ever deleted, default discovery finds this one anyway.
#
# There is exactly one definition of what the gate IS — the line below — so the two routes
# cannot drift apart into two gate lists that disagree.  Both routes reaching the same file
# is the point: the hole this whole ticket exists to close is a control that nothing invokes,
# and a config file that can be deleted into silence is that hole with a shorter fuse.
#
# WHAT IT DOES ON RED: it exits non-zero, the refinery FAILS THE MERGE REQUEST, and the
# branch does not land.  See code/control_gate_724a/README.md for who hears about it.
exec sh code/control_gate_724a/run_all.sh
