# Codex Local Adapter

This directory adapts existing `.claude` assets for Codex.

## Skill Entry

`.codex/skills/*` is the primary REPO skill scope.

Current linked Claude skills:
- `.codex/skills/manim-video-pipeline`
- `.codex/skills/pip-install`
- `.codex/skills/skill-creator`

Current repo-native skills:
- `.codex/skills/book-serve`
- `.codex/skills/git-commit`
- `.codex/skills/git-pr`

Use explicit skill invocation (`$book-serve`, `$git-commit`, `$git-pr`) or natural-language requests that match each skill description.
