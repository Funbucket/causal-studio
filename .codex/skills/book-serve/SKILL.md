---
name: book-serve
description: Start local Jupyter Book preview with minimal commands. Use when asked to run jupyter-book start, serve docs locally, restart the book server, or open localhost.
---

# Book Serve

Use direct commands first.

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
pids=$(lsof -ti tcp:${PORT} 2>/dev/null || true)
[ -z "$pids" ] || kill $pids
jupyter-book start --port ${PORT}
```
