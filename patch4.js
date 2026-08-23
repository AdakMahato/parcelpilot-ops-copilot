const fs = require('fs');
const path = './frontend/src/app/page.tsx';
let content = fs.readFileSync(path, 'utf8');

const pagesRender = `
        {['tickets', 'orders', 'accounts', 'activity', 'settings'].includes(activeTab) && (
          <div className="p-8 max-w-6xl mx-auto w-full overflow-y-auto">
            <h2 className="text-3xl font-bold mb-8 text-slate-800 tracking-tight capitalize">{activeTab}</h2>
            <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-200 flex flex-col items-center justify-center text-center">
               <div className="text-6xl mb-4 text-slate-200">🛠️</div>
               <h3 className="text-xl font-bold text-slate-700 mb-2">Feature Under Construction</h3>
               <p className="text-slate-500 max-w-md">The {activeTab} view is fully wired up to the frontend navigation state, but the backend data endpoints for this section are coming soon!</p>
               <button onClick={goHome} className="mt-6 px-6 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition">Return to Home</button>
            </div>
          </div>
        )}
`;

content = content.replace(
  /          <\/div>\n        \)}\n      <\/div>\n    <\/div>\n  \);\n\}/,
  `          </div>\n        )}\n${pagesRender}      </div>\n    </div>\n  );\n}`
);

fs.writeFileSync(path, content);
