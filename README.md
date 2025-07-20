
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

## 起動方法

### Docker一括起動

```bash
docker-compose up --build
```

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

