import codecs

with codecs.open('template_stiker.py', 'r', 'utf-8') as f:
    code = f.read()

old_trunc = "    if len(judul) > 50:\n        judul = judul[:47] + '...'"
code = code.replace(old_trunc, '')

old_draw = '''    # Text
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 0.3*cm, y + card_h - 0.7*cm, f"JUDUL     : {judul}")
    
    c.setFont("Helvetica-Bold", 8)
    # Gunakan hanya nomor ID buku seperti yang diminta user (no_induk)
    c.drawString(x + 0.3*cm, y + card_h - 1.2*cm, f"NO BUKU : {no_induk}")'''

new_draw = '''    # Text
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 0.3*cm, y + card_h - 0.6*cm, "JUDUL     :")
    
    import textwrap
    wrapped = textwrap.wrap(judul, width=32)
    
    if len(wrapped) >= 1:
        c.drawString(x + 1.8*cm, y + card_h - 0.6*cm, wrapped[0])
    if len(wrapped) >= 2:
        line2 = wrapped[1]
        if len(wrapped) > 2:
            line2 = line2[:29] + '...'
        c.drawString(x + 1.8*cm, y + card_h - 0.95*cm, line2)
        
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 0.3*cm, y + card_h - 1.4*cm, f"NO BUKU : {no_induk}")'''

code = code.replace(old_draw, new_draw)

with codecs.open('template_stiker.py', 'w', 'utf-8') as f:
    f.write(code)
print("Title wrapping fixed")
