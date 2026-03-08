# Book Stop

Jupyter Book 로컬 서버를 종료한다.

## 실행 명령어

```bash
pkill -f "jupyter-book" 2>/dev/null; lsof -ti:3000 | xargs kill -9 2>/dev/null; echo "서버 종료됨"
```

위 명령어를 실행하라.
