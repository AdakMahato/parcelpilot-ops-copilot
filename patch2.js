const fs = require('fs');
const path = './frontend/src/app/page.tsx';
let content = fs.readFileSync(path, 'utf8');

// Update UI to optionally show Gemini • Online
content = content.replace(
  /\{backendHealth\?\.status === 'ok' \? \(/,
  `{backendHealth?.status === 'ok' ? (
              <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded font-bold">API Online {backendHealth?.llm_provider === 'gemini' ? '• Gemini Online' : ''}</span>
            ) : {backendHealth?.status === 'degraded' ? (`
);

// We need to handle the recoverable LLM error. In sendMessage, check data.type === 'llm_unavailable'
content = content.replace(
  /const data = await res\.json\(\);/,
  `const data = await res.json();
      if (data.type === 'llm_unavailable' && data.recoverable) {
        setMessages(prev => [...prev, {role: 'agent', content: data.response || 'Gemini API is temporarily unavailable (quota or rate limit reached).'}]);
        setIsLoading(false);
        return;
      }`
);

fs.writeFileSync(path, content);
