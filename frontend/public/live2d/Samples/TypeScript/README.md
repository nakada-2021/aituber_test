[English](README.md) / [日本語](README.ja.md)

---

# Cubism Web Samples for TypeScript

This is a sample implementation of an application implemented with TypeScript.


## Development environment

| Package | Version |
| --- | --- |
| TypeScript | 5.8.3 |
| Vite | 6.3.5 |

For other packages, check the `package.json` for each project.
For other development environments and operation environments, see [README.md](/README.md) in the top directory.


## Task list

### `npm: start`

Starts a local server for development and creates a project monitor build.
Any changes you make to the project will automatically rebuild and cause the browser to reload.
You can debug in Visual Studio Code from [Debug Project].

To terminate in Visual Studio Code, type `>Tasks: Terminate Task` and select the task from the command palette.

### `npm: build`

Outputs a TypeScript build deliverable to the `dist` directory.
The output is a JavaScript file that has been bundled into one using Vite.
When you execute this command, it will also copy the necessary files for operation.

You can change the settings by editing `tsconfig.json` and `vite.config.mts`.

### `npm: build:prod`

Creates above build after optimizing it.
It is used to output deliverables for production environments as it reduces the build size.

### `npm: test`

Performs a TypeScript type check test.

You can change the settings by editing `tsconfig.json`.

### `npm: lint`

Performs static analysis of TypeScript files in the `src` directory.

You can change the settings by editing `.eslintrc.yml`.

### `npm: lint:fix`

Performs static analysis and automatic modification of TypeScript files in the `src` directory.

You can change the settings by editing `.eslintrc.yml`.

### `npm: serve`

Starts a simple local server.
You can check the index.html by accessing `/Samples/TypeScript/Demo` in the server from your browser.
The project needs to be built in advance.

Deliverables can be verified in an environment close to the production environment.

### `npm: clean`

Deletes the build deliverable directory (`dist`).

---

# Live2D Cubism Web SDK TypeScript サンプル: bundle.js ビルド手順

このディレクトリは、Live2D Cubism Web SDK 公式 TypeScript サンプル（Demo）をベースに、
Next.js等のWebアプリで利用できるUMD形式の `bundle.js` をビルドするためのものです。

## 前提
- Node.js 20.x（Viteのビルド要件）
- Docker（推奨。ホスト環境のNode.jsバージョン差異を吸収できます）
- Live2D Cubism Web SDK 5.x の `Framework`/`Resources` ディレクトリが正しく配置されていること

## ディレクトリ構成（抜粋）

```
Samples/TypeScript/
  Demo/
    src/
      main.ts
      lappdelegate.ts
      lappdefine.ts
      ...
    vite.config.ts
    tsconfig.json
    ...
  Framework/
    src/
      ...
  Resources/
    ...
```

## ビルド手順（Docker推奨）

1. **Dockerでビルド**

```sh
cd frontend/public/live2d/Samples/TypeScript/Demo

docker run --rm \
  -v $(pwd)/../:/workspace \
  -w /workspace/Demo \
  node:20 \
  npx vite build --config vite.config.ts --mode development
```

- `dist/bundle.umd.js` が生成されます。

2. **生成物の配置**

Next.jsや静的Webサーバで利用する場合は、
`dist/bundle.umd.js` を `frontend/public/unity_webgl/bundle.js` など公開ディレクトリにコピーしてください。

```sh
cp dist/bundle.umd.js ../../../../unity_webgl/bundle.js
```

3. **Next.jsや静的HTMLでの利用例**

`<script src="./bundle.js"></script>` で読み込むと、
`window.Live2DCubismFramework` グローバル変数でSDK APIにアクセスできます。

```html
<script src="./bundle.js"></script>
<script>
  const LAppDelegate = window.Live2DCubismFramework.LAppDelegate;
  // ...
</script>
```

## 注意点
- `src/lappdefine.ts` などでモデルディレクトリやパスを変更した場合は、再ビルドが必要です。
- ホストの `node_modules` を使わず、必ずDocker内で `npm install` してください（アーキテクチャ差異によるビルドエラー防止）。
- ViteやTypeScriptの設定は `vite.config.ts`/`tsconfig.json` を参照してください。

---

ご不明点があればこのREADMEに追記してください。
