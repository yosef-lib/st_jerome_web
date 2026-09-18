import codecs, re

with codecs.open('template_stiker.py', 'r', 'utf-8') as f:
    code = f.read()

# 1. Fix dimensions in generate_stiker_pdf
old_comp = r"'type': 'kartu',\s*'w': 7\.5 \* cm,\s*'h': 12\.0 \* cm"
new_comp = "'type': 'kartu',\n                'w': 8.0 * cm,\n                'h': 13.1 * cm"
code, c1 = re.subn(old_comp, new_comp, code)

# 2. Fix draw_kartu_buku definition and layout
old_draw_def = r"def draw_kartu_buku.*?c\.drawString\(x \+ 1\.8\*cm, y \+ card_h - 1\.4\*cm, no_induk\)"
new_draw_def = '''def draw_kartu_buku(c, x, y, buku):
    card_w = 8.0 * cm
    card_h = 13.1 * cm
    
    judul = buku.get('judul', '')
    no_induk = str(buku.get('no_induk', ''))
    
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1)
    
    # Draw Outer Border
    c.rect(x, y, card_w, card_h)
    
    c.setFillColorRGB(0, 0, 0)
    # Text
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 0.3*cm, y + card_h - 0.7*cm, "JUDUL   : ")
    
    import textwrap
    wrapped = textwrap.wrap(judul, width=33)
    
    c.setFont("Courier-Bold", 8)
    if len(wrapped) >= 1:
        c.drawString(x + 1.8*cm, y + card_h - 0.7*cm, wrapped[0])
    if len(wrapped) >= 2:
        line2 = wrapped[1]
        if len(wrapped) > 2:
            line2 = line2[:29] + '...'
        c.drawString(x + 1.8*cm, y + card_h - 1.05*cm, line2)
        
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 0.3*cm, y + card_h - 1.5*cm, "NO BUKU : ")
    c.setFont("Courier-Bold", 8)
    c.drawString(x + 1.8*cm, y + card_h - 1.5*cm, no_induk)'''
code, c2 = re.subn(old_draw_def, new_draw_def, code, flags=re.DOTALL)

# 3. Fix Table logic in draw_kartu_buku
old_table = r"# Table.*?x \+ 0\.3\*cm \+ col1_w \+ col2_w, cur_y\)"
new_table = '''# Table
    table_y = y + card_h - 2.0*cm
    table_w = card_w - 0.6*cm
    col1_w = table_w * 0.35
    col2_w = table_w * 0.40
    col3_w = table_w * 0.25
    
    row_h = 0.8*cm
    
    # Table Header
    c.rect(x + 0.3*cm, table_y - row_h, table_w, row_h)
    c.line(x + 0.3*cm + col1_w, table_y, x + 0.3*cm + col1_w, table_y - row_h)
    c.line(x + 0.3*cm + col1_w + col2_w, table_y, x + 0.3*cm + col1_w + col2_w, table_y - row_h)
    
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x + 0.3*cm + col1_w/2, table_y - 0.5*cm, "No Anggota")
    c.drawCentredString(x + 0.3*cm + col1_w + col2_w/2, table_y - 0.5*cm, "Tanggal Kembali")
    c.drawCentredString(x + 0.3*cm + col1_w + col2_w + col3_w/2, table_y - 0.5*cm, "Ket")
    
    # Fill 13 rows to match physical card (which is 13.1cm tall with ~0.8cm rows)
    for i in range(12):
        cur_y = table_y - row_h - (i+1)*row_h
        c.rect(x + 0.3*cm, cur_y, table_w, row_h)
        c.line(x + 0.3*cm + col1_w, cur_y + row_h, x + 0.3*cm + col1_w, cur_y)
        c.line(x + 0.3*cm + col1_w + col2_w, cur_y + row_h, x + 0.3*cm + col1_w + col2_w, cur_y)'''
code, c3 = re.subn(old_table, new_table, code, flags=re.DOTALL)

with codecs.open('template_stiker.py', 'w', 'utf-8') as f:
    f.write(code)
print(f"Replaced {c1}, {c2}, {c3} times")
