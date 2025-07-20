
// frontend/app.js

// MediaPipe FaceMeshを使う想定のスクリプト（ダミー構成）
async function sendKeypoints() {
    const keypoints = {
        eye_left_open: 0.8,
        eye_right_open: 0.75,
        mouth_open: 0.4,
        brow_raise: 0.2
    };

    const ws = new WebSocket("ws://localhost:8000/ws");
    ws.onopen = () => ws.send(JSON.stringify(keypoints));
}
