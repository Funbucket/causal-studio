# Book Serve

Jupyter Book 로컬 서버를 시작하고 브라우저를 연다.

## 실행 명령어

```bash
# 기존 서버 및 포트 3000 점유 프로세스 종료
pkill -f "jupyter-book" 2>/dev/null; lsof -ti:3000 | xargs kill -9 2>/dev/null; sleep 1

# 서버 시작 (백그라운드, 상대 경로 사용)
if [ -d book ]; then
  cd book
elif [ -f myst.yml ]; then
  :
else
  echo "book directory or myst.yml not found" >&2
  exit 1
fi

if [ -f ../.venv/bin/activate ]; then
  source ../.venv/bin/activate
elif [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
else
  echo ".venv not found" >&2
  exit 1
fi

jupyter-book start --port 3000 &

# 브라우저 열기
sleep 8 && open http://localhost:3000
```

위 명령어들을 순서대로 실행하라.
