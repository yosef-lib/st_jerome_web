import codecs

with codecs.open('templates/koleksi.html', 'r', 'utf-8') as f:
    code = f.read()

code = code.replace(
    '@click="deleteBiblio(b.id)"',
    '@click.stop="deleteBiblio(b.id)"'
)
code = code.replace(
    '@click="deleteEksemplar(e.no_induk)"',
    '@click.stop="deleteEksemplar(e.no_induk)"'
)

with codecs.open('templates/koleksi.html', 'w', 'utf-8') as f:
    f.write(code)
print("Added .stop modifier")
