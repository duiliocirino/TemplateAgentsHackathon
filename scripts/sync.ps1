# One-command sync for everyone: pull safely, show state, show the feed.
git pull --rebase --autostash
Write-Output "--- STATUS ---"
git status -sb
Write-Output "--- RECENT LOG HEADLINES ---"
Get-ChildItem docs/log -Filter *.md | Where-Object Name -ne 'README.md' |
  Sort-Object Name | Select-Object -Last 15 -ExpandProperty Name
Write-Output "--- RECENT COMMITS ---"
git log --oneline -10
