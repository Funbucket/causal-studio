---
name: git-pr
description: Prepare and create pull requests with a minimal direct flow. Use when asked to inspect branch status, check commits against base, push a branch, or run gh pr create.
---

# Git Pr

Use direct git/gh commands first.

## Quick Run

```bash
git status --short
git branch --show-current
git push -u origin "$(git branch --show-current)"
gh pr create --base main --fill
```

## Optional Variants

```bash
gh pr create --base main --title "docs: guide update" --body "Summary"
gh pr create --base main --fill --draft
```
