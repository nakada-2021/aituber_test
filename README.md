
# AITuber Test 完全統合版（2025年7月版）

## 概要

AITuber Testは、以下の機能を全て統合したマルチモーダルAIキャラクターシステムです。

### 主要機能

- Live2D自動生成（パーツ→PSD→Cubism連携）
- 多言語＆キャラ人格切替チャット
- リアルタイム表情制御（カメラ＋音声＋文字）
- ローカルLLM（Llama.cpp）＋RAG（社内QA）
- WebGL（Pixi.js）によるLive2D表示デモ
- TTS（音声出力）＋Cloud Storage配信
- WebSocket音声配信（リアルタイムTTS）

## ディレクトリ構成

```
aituber_test/
├─ backend/
│   ├─ Dockerfile
│   ├─ requirements.txt
│   ├─ app/
│   │   ├─ main.py
│   │   ├─ persona_chat.py
│   │   ├─ multilang_tts_api.py
│   │   ├─ cloud_ws_tts_api.py
│   │   └─ rag_qa.py
│   └─ rag/
│       └─ router_chain.py
├─ company_data/company_info.txt
├─ cubism_template/placeholder.txt
├─ tools/
│   ├─ auto_psd_generator.py
│   ├─ cubism_template_injector.py
│   └─ README.md
├─ frontend/
│   ├─ Dockerfile
│   ├─ package.json / next.config.js
│   ├─ app.js / index.html / style.css
│   └─ pages/
│       ├─ index.js
│       └─ ws_tts.js
├─ unity_webgl/
│   ├─ index.html / websocket.js / model.json
├─ docker-compose.yml
└─ LICENSE / README.md
```

## 起動手順（Docker環境）

1. `.env` ファイルを用意（`LOCAL_LLM=on`で設定）

2. モデルファイルを `./models` に配置  
   例：`mistral-7b-instruct-v0.2.Q2_K.gguf`

3. Docker起動

```bash
docker compose up -d
```

※ `models` が無い場合は OpenAI APIに自動フォールバックします。

---

## Web画面一覧と操作フロー

### ① メインチャット画面

#### URL:
```
http://localhost:3000/
```

#### 画面内容：

- テキスト入力欄（チャット入力）
- 送信ボタン

#### 操作：

1. メッセージを入力して「送信」すると、  
   **ローカルLLM または OpenAI にチャットリクエスト**を送ります。

2. 返答はテキストで表示されます。

3. **表情パラメータも自動生成され、Live2Dアバターと連動可能です。**

---

### ② WebGL Live2D連動版（表情・TTSリアルタイム反映）

#### URL:
```
http://localhost:3000/ws_tts
```

#### 画面内容：

- チャット入力欄
- Live2D WebGL表示エリア（自動で動きます）

#### 操作：

1. テキスト入力 → 送信すると、  
   **リアルタイムにLive2Dアバターが口パク・目パチしながら返答します。**

2. 返答は **多言語TTSで音声出力**され、同時にアニメーションも動きます。

3. 表情制御は WebSocket で `backend` に送信され、`text2keypoints` 経由で制御します。

---

### ③ Unity用 Live2D連携デモ

#### URL:
```
http://localhost:3000/unity_webgl/index.html
```

#### 内容：

- UnityビルドされたLive2Dモデルが表示されます。
- WebSocket経由でリアルタイム表情制御（`/ws/tts`と連動）

#### 操作：

- **`ws_tts`から送信した表情制御が、Unity側にも反映されます。**

> **注意：**  
> `frontend/public/unity_webgl/` に `index.html` を配置する必要があります。

---

### ③ APIエンドポイント（バックエンド）

| API | URL |
|---|---|
| チャットAPI | `http://localhost:8000/api/chat` |
| キャラ人格切替 | `http://localhost:8000/api/persona_chat` |
| 多言語TTS | `http://localhost:8000/api/multilang_tts_chat` |
| WebSocket TTS | `ws://localhost:8000/ws/tts` |
| 表情制御（text2keypoints） | `http://localhost:8000/api/text2keypoints` |

---

## LLM切り替え

| 状況 | 動作 |
|---|---|
| `LOCAL_LLM=on` & モデル起動成功 | ローカルLLM（Llama.cpp）使用 |
| `LOCAL_LLM=on` & モデル起動失敗 | OpenAI APIに自動切替 |
| `LOCAL_LLM=off` | 常にOpenAI API使用 |

---

## 便利コマンド

### モデル無しでもOpenAIで動作させる場合：

```
echo "LOCAL_LLM=off" >> .env
docker compose up -d
```

### コンテナ内モデル確認

```
docker exec -it aituber_test-llama_cpp-1 ls /models
```

---

## トラブルシューティング

- **5000番ポート競合 → `5001`に変更済み**
- Macでファイル共有エラーが出た場合は、`docker cp`で直接モデルをコンテナにコピー可能



## 必要モデル

- ./models/your_model.gguf（Llama.cppモデル）
- unity_webgl/ に Live2Dモデル（.moc3、.model3.json）

## エンドポイント一覧

| 機能 | URL |
|---|---|
| LLMチャット（OpenAI） | /api/chat |
| キャラ人格切替 | /api/persona_chat |
| 多言語TTS（ローカルmp3） | /api/multilang_tts_chat |
| CloudStorage＋音声URL返却 | /api/cloud_tts_chat |
| WebSocket TTS音声 | /ws/tts |
| RAG（社内情報検索） | backend/app/rag_qa.py（内部呼び出し） |
| WebSocket表情制御 | unity_webgl/websocket.js |

## フロントエンドUI

| URL | 内容 |
|---|---|
| /（Next.js） | テキストチャット |
| /ws_tts（Next.js） | WebSocketリアルタイムTTS |
| /unity_webgl/index.html | WebGL Live2Dデモ |

## 多言語・人格パラメータ

| persona | キャラ |
|---|---|
| default | 丁寧なAI |
| tsundere | ツンデレ |
| kansai | 関西弁 |
| english_teacher | 英語教師 |

| lang | 言語 |
|---|---|
| ja | 日本語 |
| en | 英語 |
| zh | 中国語 |

## RAG（社内QA）の動作

- backend/app/rag_qa.py から Llama.cpp API (/completion) 呼び出し
- company_data/company_info.txt をFAISSベクトル化検索

## Live2Dモデル生成フロー

1. live2d_auto_generator.py（パーツ自動生成）
2. auto_psd_generator.py（PSD変換）
3. cubism_template_injector.py（テンプレ差し替え）
4. Cubism Editorで読み込み＋微調整

## 音声出力

- gTTS + mp3保存（ローカルorCloud Storage）
- WebSocketで音声URLリアルタイム配信対応

## 拡張対応（今後対応可能）

- GPU対応（CUDA版 Llama.cpp）
- Unity完全連携（Live2D SDK for Unity）
- CI/CD（GitHub Actions用 ci.yml）

## フロントエンドの依存更新・バージョンアップ後のビルド手順

依存パッケージ（例: pixi-live2d-display）をアップデートした場合や、エラーが解消しない場合は、Next.jsのキャッシュクリアと再ビルドが必要です。

```sh
docker compose exec frontend rm -rf .next
docker compose exec frontend npm run build
docker compose restart frontend
```

これで古いバンドルやキャッシュが消え、最新の依存・コードで再ビルドされます。

