import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

code = code.replace("url_for('dashboard', lokasi='IMAVI')", "url_for('index', lokasi='IMAVI')")

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
