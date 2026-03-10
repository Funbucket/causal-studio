---
name: book-serve
description: Start local Jupyter Book preview with minimal commands. Use when asked to run jupyter-book start, serve docs locally, restart the book server, or open localhost.
---

# Book Serve

Use direct commands first.

Notes:
- Prefer a restart-safe command that does not rely on shell word-splitting for PID handling.
- If `jupyter-book start` fails with a sandbox port-binding error such as `listen EPERM`, rerun the same command with escalated permissions.

## Quick Run

```bash
if [ -d book ]; then
  cd book
elif [ -d ../book ]; then
  cd ../book
else
  echo "book directory not found" >&2
  exit 1
fi

source ../.venv/bin/activate
PORT=3000
lsof -ti tcp:${PORT} 2>/dev/null | xargs -r kill
jupyter-book start --port ${PORT}
```

## Why This Form

- `lsof -ti ... | xargs -r kill` handles multiple PIDs safely and avoids zsh newline/word-splitting issues.
- The command remains minimal while still supporting restart behavior on an already-used port.
