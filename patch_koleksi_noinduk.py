import codecs

with codecs.open('templates/koleksi.html', 'r', 'utf-8') as f:
    code = f.read()

# Fix: use e.no_induk instead of e.id for delete, and also for the eksemplar API call
code = code.replace(
    "const res = await fetch('/api/eksemplar/' + id, { method: 'DELETE' });",
    "const res = await fetch('/api/eksemplar/' + encodeURIComponent(id), { method: 'DELETE' });"
)

# Fix the function to pass no_induk instead of id
code = code.replace(
    "async deleteEksemplar(id) {",
    "async deleteEksemplar(no_induk) {"
)
code = code.replace(
    "if (!confirm(\"Hapus barcode ini?\")) return;\n            try {\n                const res = await fetch('/api/eksemplar/' + encodeURIComponent(id), { method: 'DELETE' });",
    "if (!confirm(\"Hapus barcode \" + no_induk + \"?\")) return;\n            try {\n                const res = await fetch('/api/eksemplar/' + encodeURIComponent(no_induk), { method: 'DELETE' });"
)

# Fix the double toggle refresh to be cleaner
code = code.replace(
    "this.toggleEksemplar(this.expandedId); \n                    this.toggleEksemplar(this.expandedId); // double toggle to refresh",
    "await this.toggleEksemplar(this.expandedId);"
)

# Fix the button to pass e.no_induk
code = code.replace(
    '<button @click="deleteEksemplar(e.id)"',
    '<button @click="deleteEksemplar(e.no_induk)"'
)

with codecs.open('templates/koleksi.html', 'w', 'utf-8') as f:
    f.write(code)
print("Fixed koleksi.html to use no_induk")
