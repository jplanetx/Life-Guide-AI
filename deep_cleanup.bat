@echo off
cd %~dp0
git stash
git filter-branch --force --tree-filter "find . -type f -exec sed -i 's/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/REMOVED_NOTION_KEY/g' {} +" HEAD --all
git push origin --force --all
git stash pop