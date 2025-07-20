
// frontend/keypoints_generator.js

// カメラ・音声・文字入力からkeypointsを生成し、Live2D表情制御用に送信する

let ws = new WebSocket("ws://localhost:8000/ws");

// カメラ（MediaPipe想定、ここはダミー）
function getCameraKeypoints() {
    return {
        eyeLeftOpen: 0.8,
        eyeRightOpen: 0.8,
        mouthOpen: 0.1,
        headYaw: 0.0
    };
}

// 音声（音量→口パク）
function getAudioKeypoints(volume) {
    return {
        mouthOpen: Math.min(1.0, volume * 2.0)
    };
}

// 文字入力→感情推定（LLM呼び出し）
async function getTextEmotionKeypoints(text) {
    const response = await fetch("http://localhost:8000/text2keypoints", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text })
    });
    return await response.json();
}

// 統合して送信
async function sendKeypoints(text, volume) {
    const cam = getCameraKeypoints();
    const audio = getAudioKeypoints(volume);
    const emotion = await getTextEmotionKeypoints(text);

    const keypoints = {
        eyeLeftOpen: cam.eyeLeftOpen,
        eyeRightOpen: cam.eyeRightOpen,
        mouthOpen: Math.max(cam.mouthOpen, audio.mouthOpen, emotion.mouthOpen || 0),
        headYaw: cam.headYaw,
        smile: emotion.smile || 0,
        sad: emotion.sad || 0,
        surprise: emotion.surprise || 0
    };

    ws.send(JSON.stringify(keypoints));
}
