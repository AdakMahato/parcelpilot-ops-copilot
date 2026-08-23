const fs = require('fs');
const path = './frontend/src/app/page.tsx';
let content = fs.readFileSync(path, 'utf8');

// Update goBack, goHome, and setActiveTab to clear selectedItem
content = content.replace(
  /const setActiveTab = \(tab: string\) => \{/,
  `const setActiveTab = (tab: string) => {
    setSelectedItem(null);`
);

content = content.replace(
  /const goBack = \(\) => \{/,
  `const goBack = () => {
    setSelectedItem(null);`
);

content = content.replace(
  /const goHome = \(\) => \{/,
  `const goHome = () => {
    setSelectedItem(null);`
);

// Add clear chat button inside the chat UI (when messages > 0)
// The Chat UI starts at `{activeTab === 'chat' && (`
// Let's add a clear button next to the input, or maybe a "New Chat" button in the Top Bar, or just above the messages.
// I'll add a "Clear Chat" button near the "Ask about..." input area, or in the chat header.
content = content.replace(
  /\{messages\.length === 0 && \(/,
  `{messages.length > 0 && (
                <div className="flex justify-center mb-4">
                  <button onClick={() => setMessages([])} className="px-4 py-1 bg-slate-200 text-slate-600 rounded-full text-xs font-bold uppercase tracking-wider hover:bg-slate-300 transition-colors">Clear Chat</button>
                </div>
              )}
              {messages.length === 0 && (`
);

fs.writeFileSync(path, content);
