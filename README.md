
# AITuber Test

## 構成

- frontend/ : ブラウザUI＋MediaPipeキーポイント送信（仮）
- backend/ : Node.js WebSocketサーバーとFastAPI LLM接続
- unity_webgl/ : Unity WebGLビルド配置用
- tools/ : Live2D自動生成スクリプト

## 使い方

### Frontend

ブラウザで `index.html` を開き、`Send Keypoints` をクリックするとWebSocketでサーバーに送信します。

### Backend

Node.jsとFastAPIでサーバーを起動します。

### Live2D自動生成

```bash
python tools/live2d_auto_generator.py --prompt "赤髪 ショート ボーイッシュ 女の子"
```

