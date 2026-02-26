# Codex Routing Rules For This Repo

## 1) Skill-First Operation

Use REPO skills in `.codex/skills` instead of project command files.

Project skills for previous command workflows:
- `book-serve`: local Jupyter Book server
- `git-commit`: change analysis and commit workflow
- `git-pr`: pull request workflow

## 2) Claude Skill Bridge

When request intent matches below topics, use `.claude/skills/*` as the operational source:
- `manim-video-pipeline`: scene design/script/render/audio mux/full concat
- `pip-install`: install package in `.venv` and sync `requirements.txt`
- `skill-creator`: create/update project skill package

How to execute:
1. Read the target `SKILL.md`.
2. Resolve relative paths from the skill directory first.
3. Prefer bundled scripts in `scripts/` over re-implementing logic.
4. Load only required files in `references/`.

Priority:
- In this repository, REPO scope skills (`.codex/skills/*`) take precedence over USER/ADMIN/SYSTEM skills when names overlap.
