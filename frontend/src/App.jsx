import React, { useEffect, useState } from 'react';
import ChatBox from './components/ChatBox';
import ResultsList from './components/ResultsList';
import { postMessage, analyzeMessage, getMessage, listMessages } from './api';

export default function App() {
  const [messages, setMessages] = useState([]);
  const [selected, setSelected] = useState(null);

  useEffect(() => { refresh(); }, []);

  async function refresh() {
    const list = await listMessages();
    setMessages(list);
  }

  async function handleSend(text) {
    const created = await postMessage(text);
    await analyzeMessage(created.id, ['summarization','sentiment','keywords']);
    const msgWithAnalyses = await getMessage(created.id);
    setSelected(msgWithAnalyses);
    refresh();
  }

  return (
    <div className="container">
      <h1 style={{fontSize:22}}>Expert MCP — Summarize · Sentiment · Keywords</h1>
      <div style={{marginTop:12}} className="card">
        <ChatBox onSend={handleSend} />
      </div>

      <div style={{display:'flex', gap:20, marginTop:20}}>
        <div style={{flex:'0 0 260px'}}>
          <h3>Recent messages</h3>
          <div className="card" style={{marginTop:8}}>
            {messages.map(m => (
              <div key={m.id} style={{padding:8, borderBottom:'1px solid #f3f4f6'}}>
                <button style={{all:'unset', cursor:'pointer'}} onClick={async ()=> setSelected(await getMessage(m.id))}>
                  {m.text.slice(0,80)}{m.text.length>80?'…':''}
                </button>
              </div>
            ))}
          </div>
        </div>

        <div style={{flex:1}}>
          <h3>Selected message</h3>
          <div className="card" style={{marginTop:8}}>
            <ResultsList message={selected} />
          </div>
        </div>
      </div>
    </div>
  );
}
