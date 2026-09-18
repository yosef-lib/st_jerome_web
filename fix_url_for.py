import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

code = code.replace("url_for('koleksi', lokasi='IMAVI')", "url_for('daftar_koleksi', lokasi='IMAVI')")

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
