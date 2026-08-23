with open('frontend/src/app/page.tsx', 'r') as f:
    content = f.read()

# Fix dashboard scroll container
content = content.replace(
    'className="p-8 max-w-6xl mx-auto w-full overflow-y-auto"',
    'className="p-8 max-w-6xl mx-auto w-full overflow-y-auto h-full"'
)

# Fix tickets/orders/accounts scroll container
content = content.replace(
    'className="p-8 max-w-4xl mx-auto w-full overflow-y-auto"',
    'className="p-8 max-w-4xl mx-auto w-full overflow-y-auto h-full"'
)

with open('frontend/src/app/page.tsx', 'w') as f:
    f.write(content)
