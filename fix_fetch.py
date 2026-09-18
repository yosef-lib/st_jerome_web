import codecs

with codecs.open('templates/koleksi.html', 'r', 'utf-8') as f:
    code = f.read()

code = code.replace("const res = await fetch(/api/koleksi/list?search=\&page=\);", "const res = await fetch('/api/koleksi/list?search=' + encodeURIComponent(this.searchQuery) + '&page=' + page);")

with codecs.open('templates/koleksi.html', 'w', 'utf-8') as f:
    f.write(code)
print("fixed.")
