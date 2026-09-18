import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

code = code.replace("data.get('lokasi', 'STPD')", "data.get('lokasi', 'IMAVI')")
code = code.replace("lokasi = request.args.get('lokasi', 'STPD')", "lokasi = request.args.get('lokasi', 'IMAVI')")

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
