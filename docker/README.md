
# Docker構成（ローカルLLM付き）

## 起動方法

```bash
docker-compose up --build
```

## 構成内容

- FastAPIエンドポイント : `http://localhost:8000/chat`
- LLM自動ルーティング（LangChain Router）
- ローカルLLM： `models/local_model.gguf` に配置

