import codecs

with codecs.open('database.py', 'r', 'utf-8') as f:
    code = f.read()

code = code.replace("lokasi TEXT DEFAULT 'STPD'", "lokasi TEXT DEFAULT 'IMAVI'")

with codecs.open('database.py', 'w', 'utf-8') as f:
    f.write(code)
