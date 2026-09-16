import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

app_code = app_code.replace('INSERT INTO buku', 'INSERT OR REPLACE INTO buku')

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)

print("Unique constraint fixed")
