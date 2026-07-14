# Rollback — tourist-SEO + CSS upgrade of 2026-07-14

Everything from the 2026-07-14 upgrade sits AFTER the git tag `pre-upgrade-2026-07-14`.
The site only changes when `main` is pushed to GitHub — so nothing is live until you push.

## Roll back BEFORE pushing (changes only on this PC)

```
git reset --hard pre-upgrade-2026-07-14
```

That's it. The working tree and history return exactly to the pre-upgrade state.

## Roll back AFTER pushing (changes already live)

Safest (keeps history, creates an "undo" commit):

```
git revert --no-edit pre-upgrade-2026-07-14..HEAD
git push
```

GitHub Pages redeploys automatically within ~1 minute of the push.

## Roll back just ONE part

Each part of the upgrade is its own commit (see `git log --oneline`).
Revert only the commit you dislike:

```
git revert --no-edit <commit-hash>
git push
```

## Verify what state you're in

```
git log --oneline pre-upgrade-2026-07-14..HEAD   # lists everything the upgrade added
git status                                        # should say "working tree clean"
```
