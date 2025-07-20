
function sendInput() {
    const text = document.getElementById("textInput").value;
    sendKeypoints(text, 0.1); // 仮の音量
}

function startAudio() {
    alert("音声入力はWebAudio APIで実装（未実装）");
    // 実際は keypoints_generator.js の getAudioKeypoints を呼ぶ
}

function startCamera() {
    alert("カメラ起動はMediaPipe連携（未実装）");
    // 実際は keypoints_generator.js の getCameraKeypoints を呼ぶ
}
