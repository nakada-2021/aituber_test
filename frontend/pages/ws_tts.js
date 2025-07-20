
import { useState, useEffect } from 'react';

export default function WsTts() {
  const [text, setText] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [ws, setWs] = useState(null);

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws/tts");
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setAudioUrl(data.audio_url);
    };
    setWs(socket);

    return () => {
      socket.close();
    };
  }, []);

  const sendText = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(text);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>WebSocket TTS Demo</h1>
      <textarea value={text} onChange={e => setText(e.target.value)} rows="4" cols="50"/>
      <br/>
      <button onClick={sendText}>送信して発声</button>
      <h3>音声:</h3>
      {audioUrl && <audio controls src={audioUrl} autoPlay />}
    </div>
  );
}
