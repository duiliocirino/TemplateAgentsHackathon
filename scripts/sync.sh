#!/usr/bin/env bash
# One-command sync for everyone: pull safely, show state, show the feed.
set -e
git pull --rebase --autostash
echo "--- STATUS ---"
git status -sb
echo "--- RECENT LOG HEADLINES ---"
find docs/log -maxdepth 1 -name '*.md' ! -name 'README.md' -printf '%f\n' 2>/dev/null | sort | tail -15
echo "--- RECENT COMMITS ---"
git log --oneline -10
