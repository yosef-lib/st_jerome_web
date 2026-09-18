import codecs

with codecs.open('template_stiker.py', 'r', 'utf-8') as f:
    code = f.read()

code = code.replace("'type': 'kartu', 'w': 7.5*cm, 'h': 12.0*cm", "'type': 'kartu', 'w': 8.0*cm, 'h': 13.1*cm")

with codecs.open('template_stiker.py', 'w', 'utf-8') as f:
    f.write(code)
