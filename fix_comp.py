import codecs, re

with codecs.open('template_stiker.py', 'r', 'utf-8') as f:
    code = f.read()

pattern = r"components = \[\]\s*if options.*?if not components:"
new_comp = '''components = []
    if options.get('identitas'): components.append({'type': 'identitas', 'w': 7.5*cm, 'h': 4.0*cm})
    if options.get('punggung'): components.append({'type': 'punggung', 'w': 4.5*cm, 'h': 5.0*cm})
    if options.get('barcode'): components.append({'type': 'barcode', 'w': 4.0*cm, 'h': 3.0*cm})
    if options.get('kartu'): components.append({'type': 'kartu', 'w': 7.5*cm, 'h': 12.0*cm})
    if options.get('kantong'): components.append({'type': 'kantong', 'w': 10.5*cm, 'h': 9.0*cm})
    
    if not components:'''

code, count = re.subn(pattern, new_comp, code, flags=re.DOTALL)
print(f"Replaced {count} times")

with codecs.open('template_stiker.py', 'w', 'utf-8') as f:
    f.write(code)
