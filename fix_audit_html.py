import codecs

with codecs.open('templates/audit_rak.html', 'r', 'utf-8') as f:
    html = f.read()

# I will replace max-w-md with max-w-5xl
html = html.replace('<div class="max-w-md mx-auto p-4 md:p-6 2xl:p-10">', '<div class="max-w-5xl mx-auto p-4 md:p-6 2xl:p-10">')

with codecs.open('templates/audit_rak.html', 'w', 'utf-8') as f:
    f.write(html)

print("audit rak layout fixed")
