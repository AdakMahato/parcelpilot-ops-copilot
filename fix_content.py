with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

insertion = """
                    {/* Message Content */}
                    {m.role === 'user' ? (
                      <div className="text-sm whitespace-pre-wrap leading-relaxed">{m.content}</div>
                    ) : (
                      <div className="text-slate-800 leading-relaxed text-sm">
                        <ReactMarkdown 
                           components={{
                             h3: ({...props}: any) => <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mt-6 mb-2" {...props} />,
                             h4: ({...props}: any) => <h4 className="text-sm font-semibold text-slate-800 mt-4 mb-1" {...props} />,
                             p: ({...props}: any) => <p className="mb-3 text-sm leading-relaxed text-slate-700" {...props} />,
                             ul: ({...props}: any) => <ul className="list-none space-y-1 mb-3 text-sm text-slate-700" {...props} />,
                             li: ({...props}: any) => <li className="relative pl-3 before:content-['•'] before:absolute before:left-0 before:text-slate-400" {...props} />,
                             strong: ({...props}: any) => <strong className="font-semibold text-slate-900" {...props} />,
                             hr: ({...props}: any) => <hr className="my-5 border-slate-100" {...props} />
                           }}
                        >
                          {m.content}
                        </ReactMarkdown>
                      </div>
                    )}
"""

# Insert before {/* Action Confirmation Card */}
content = content.replace("{/* Action Confirmation Card */}", insertion + "\n                    {/* Action Confirmation Card */}")

with open("frontend/src/app/page.tsx", "w") as f:
    f.write(content)
