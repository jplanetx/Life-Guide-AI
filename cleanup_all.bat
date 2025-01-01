@echo off
cd %~dp0
git stash
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch backend/.env" --prune-empty --tag-name-filter cat -- --all
git push origin --force --all
git stash pop
