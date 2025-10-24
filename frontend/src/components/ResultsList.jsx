import React from 'react';

export default function ResultsList({ message }) {
  if (!message) return <div style={{color:'#6b7280'}}>No message selected</div>;
  return (
    <div>
      <div style={{marginBottom:12}}><strong>Original</strong><div style={{marginTop:6}}>{message.text}</div></div>

      {(message.analyses || []).map(a => (
        <div key={a.id} style={{marginBottom:10}}>
          <div style={{fontSize:12, color:'#6b7280'}}>Type: {a.kind}</div>
          <pre>{typeof a.result === 'string' ? a.result : JSON.stringify(a.result, null, 2)}</pre>
        </div>
      ))}
    </div>
  );
}
