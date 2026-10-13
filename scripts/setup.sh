#!/usr/bin/env bash
# Run once per clone. Makes the git behavior the protocol assumes the default.
set -e
git config pull.rebase true          # no more "Merge branch 'main' of ..." noise
git config rerere.enabled true       # remember conflict resolutions, replay repeats
git config rerere.autoupdate true
echo "OK: pull.rebase, rerere set for this clone."
