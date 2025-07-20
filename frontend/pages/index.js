
import { useState } from 'react';

export default function Home() {
  const [text, setText] = useState("");
  const [response, setResponse] = useState("");

  async function sendText() {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    setResponse(data.response);
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>AITuber Frontend (Next.js)</h1>
      <textarea value={text} onChange={e => setText(e.target.value)} rows="4" cols="50"/>
      <br/>
      <button onClick={sendText}>送信</button>
      <h3>Response:</h3>
      <p>{response}</p>
    </div>
  );
}
