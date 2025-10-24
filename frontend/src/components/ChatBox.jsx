import React, { useState } from 'react';

export default function ChatBox({ onSend }) {
  const [text, setText] = useState('');
  const sending = text.trim().length === 0;

  const handleSend = async () => {
    if (!text.trim()) return;
    await onSend(text.trim());
    setText('');
  };

  return (
    <div>
      <textarea rows={6} value={text} onChange={(e)=>setText(e.target.value)} placeholder="Write a message for the experts..." />
      <div style={{display:'flex', justifyContent:'flex-end', marginTop:8}}>
        <button disabled={sending} onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}
