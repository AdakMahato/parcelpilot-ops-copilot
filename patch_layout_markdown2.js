const fs = require('fs');
const path = './frontend/src/app/page.tsx';
let content = fs.readFileSync(path, 'utf8');

if (!content.includes("import ReactMarkdown from 'react-markdown';")) {
  content = content.replace(
    /import React, \{ useState, useEffect, useRef \} from 'react';/,
    "import React, { useState, useEffect, useRef } from 'react';\nimport ReactMarkdown from 'react-markdown';"
  );
}

content = content.replace(/h3: \(\{node, \.\.\.props\}\) =>/g, 'h3: ({...props}: any) =>');
content = content.replace(/h4: \(\{node, \.\.\.props\}\) =>/g, 'h4: ({...props}: any) =>');
content = content.replace(/p: \(\{node, \.\.\.props\}\) =>/g, 'p: ({...props}: any) =>');
content = content.replace(/ul: \(\{node, \.\.\.props\}\) =>/g, 'ul: ({...props}: any) =>');
content = content.replace(/ol: \(\{node, \.\.\.props\}\) =>/g, 'ol: ({...props}: any) =>');
content = content.replace(/strong: \(\{node, \.\.\.props\}\) =>/g, 'strong: ({...props}: any) =>');
content = content.replace(/hr: \(\{node, \.\.\.props\}\) =>/g, 'hr: ({...props}: any) =>');

fs.writeFileSync(path, content);
