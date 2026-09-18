import codecs, re

with codecs.open('template_stiker.py', 'r', 'utf-8') as f:
    code = f.read()

code = code.replace("from reportlab.lib.pagesizes import A4", "from reportlab.lib.pagesizes import A4\nF4 = (21.5 * cm, 33.0 * cm)")
code = code.replace("c = canvas.Canvas(output_file, pagesize=A4)", "c = canvas.Canvas(output_file, pagesize=F4)")
code = code.replace("width, height = A4", "width, height = F4")

with codecs.open('template_stiker.py', 'w', 'utf-8') as f:
    f.write(code)
