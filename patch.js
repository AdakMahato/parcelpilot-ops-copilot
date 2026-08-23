const fs = require('fs');
const path = './frontend/src/app/page.tsx';
let content = fs.readFileSync(path, 'utf8');

content = content.replace(
  /if \(!res\.ok\) \{\s*throw new Error\(\`Server returned \$\{res\.status\}\`\);\s*\}/,
  `if (!res.ok) {
        let errMsg = \`Server returned \$\{res.status\}\`;
        try {
          const errData = await res.json();
          errMsg = errData.detail || errData.message || errMsg;
        } catch(e) {}
        throw new Error(errMsg);
      }`
);

content = content.replace(
  /setMessages\(prev => \[\.\.\.prev, \{role: 'agent', content: 'Tool failure.*?\}\]\);/,
  `setMessages(prev => [...prev, {role: 'agent', content: 'Agent Error: ' + (e as Error).message}]);`
);

fs.writeFileSync(path, content);
