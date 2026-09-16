import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    content = f.read()

content = content.replace('p.Kode Eksemplar', 'p.no_induk')
content = content.replace('p.Judul', 'p.judul')

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(content)
print("SQL queries fixed")
