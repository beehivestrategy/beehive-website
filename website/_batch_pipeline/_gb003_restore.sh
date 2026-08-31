#!/bin/zsh
# restore one slug (all langs) from backup
ROOT="/Users/kennethkwok/Beehive Strategy/0 - New Beehive/website"
BK="$ROOT/_batch_pipeline/_backup_gb003"
s="$1"
for d in "" "zh-cn/" "zh-tw/"; do
  src="$BK/${d}blog/articles/$s.html"
  dst="$ROOT/${d}blog/articles/$s.html"
  [ -f "$src" ] && cp "$src" "$dst" && echo "restored $dst"
done
