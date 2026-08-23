const fs = require('fs');
const path = './frontend/src/app/page.tsx';
let content = fs.readFileSync(path, 'utf8');

// 1. Add import for ReactMarkdown
if (!content.includes('react-markdown')) {
  content = content.replace(
    /import React, \{ useState, useEffect, useRef \} from 'react';/,
    `import React, { useState, useEffect, useRef } from 'react';\nimport ReactMarkdown from 'react-markdown';`
  );
}

// 2. Fix layout overflow issue
// Replace `className="flex-1 flex flex-col min-w-0"` with `className="flex-1 flex flex-col min-w-0 overflow-hidden"`
content = content.replace(
  /<div className="flex-1 flex flex-col min-w-0">/,
  `<div className="flex-1 flex flex-col min-w-0 overflow-hidden">`
);

// 3. Render markdown
content = content.replace(
  /<div className="whitespace-pre-wrap leading-relaxed text-\[15px\]">\s*\{m\.content\}\s*<\/div>/,
  `<div className="leading-relaxed text-[15px] space-y-4">
     <ReactMarkdown 
       components={{
         h3: ({node, ...props}) => <h3 className="text-lg font-bold mt-4 mb-2" {...props} />,
         h4: ({node, ...props}) => <h4 className="text-base font-bold mt-3 mb-1" {...props} />,
         p: ({node, ...props}) => <p className="mb-2" {...props} />,
         ul: ({node, ...props}) => <ul className="list-disc pl-5 space-y-1 mb-2" {...props} />,
         ol: ({node, ...props}) => <ol className="list-decimal pl-5 space-y-1 mb-2" {...props} />,
         strong: ({node, ...props}) => <strong className="font-bold text-slate-900" {...props} />,
         hr: ({node, ...props}) => <hr className="my-4 border-slate-200" {...props} />
       }}
     >
       {m.content}
     </ReactMarkdown>
   </div>`
);

fs.writeFileSync(path, content);
