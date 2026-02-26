# Book Serve

Jupyter Book 로컬 서버를 시작하고 브라우저를 연다.

## 실행 명령어

```bash
# 기존 서버 종료
pkill -f "jupyter-book" 2>/dev/null

# 서버 시작 (백그라운드)
cd book && source ../.venv/bin/activate && jupyter-book start &

# 브라우저 열기
sleep 3 && open http://localhost:3000
```

위 명령어들을 순서대로 실행하라.
