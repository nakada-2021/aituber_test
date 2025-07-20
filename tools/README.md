
# tools/ フォルダ概要

AITuberプロジェクトの Live2D 自動生成＆モデル化用ツール群です。

## ツール一覧

### 1. live2d_auto_generator.py

- LLM（ChatGPT API）にプロンプトを送信し、髪・顔・体のパーツ画像生成コード（Pillow）を自動生成・実行します。
- 出力：`output/hair.png`, `output/face.png`, `output/body.png`

### 2. auto_psd_generator.py

- `output/` にあるパーツPNGを自動でPSDファイルにまとめます。
- Cubism Editorで読み込めるPSDを生成します。

### 3. cubism_template_injector.py

- `cubism_template/` にあるCubism Editor用テンプレートモデルに、生成したPSDを差し替えます。
- 物理演算・目パチ・リップシンクなどテンプレ設定を再利用可能です。

## フロー概要

```
[1] live2d_auto_generator.py → パーツPNG生成
[2] auto_psd_generator.py    → PSD自動生成
[3] cubism_template_injector.py → Cubismテンプレ差し替え
```

## 注意事項

- Cubism Editor作業は「テンプレートモデルからPSD差替＆微調整」で完了できます。
- メッシュ割りはCubism側の自動メッシュ生成で対応してください。
