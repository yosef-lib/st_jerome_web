import codecs

with codecs.open('template_stiker.py', 'r', 'utf-8') as f:
    code = f.read()

old_imports = '''from reportlab.lib.pagesizes import A4
F4 = (21.5 * cm, 33.0 * cm)
from reportlab.lib.units import cm'''

new_imports = '''from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
F4 = (21.5 * cm, 33.0 * cm)'''

code = code.replace(old_imports, new_imports)

with codecs.open('template_stiker.py', 'w', 'utf-8') as f:
    f.write(code)
