import codecs

with codecs.open('template_stiker.py', 'r', 'utf-8') as f:
    code = f.read()

code = code.replace("c.setFillColorRGB(0, 0, 0)\n    # Text", "c.setFillColorRGB(0, 0, 0)\n    c.setStrokeColorRGB(0, 0, 0)\n    # Text")

with codecs.open('template_stiker.py', 'w', 'utf-8') as f:
    f.write(code)
