import codecs, re

with codecs.open('template_stiker.py', 'r', 'utf-8') as f:
    code = f.read()

old_draw = '''    # Text
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 0.3*cm, y + card_h - 0.7*cm, "JUDUL :")
    c.setFont("Helvetica", 8)
    c.drawString(x + 1.5*cm, y + card_h - 0.7*cm, judul)
    
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 0.3*cm, y + card_h - 1.2*cm, "NO BUKU :")
    c.setFont("Helvetica", 8)
    c.drawString(x + 1.7*cm, y + card_h - 1.2*cm, no_buku)
    
    # Table
    table_y = y + card_h - 1.8*cm
    col1_w = card_w * 0.3
    col2_w = card_w * 0.45
    col3_w = card_w * 0.25
    
    row_h = 0.55*cm
    
    # Table Header
    c.rect(x + 0.3*cm, table_y - row_h, card_w - 0.6*cm, row_h)
    c.line(x + 0.3*cm + col1_w, table_y, x + 0.3*cm + col1_w, table_y - row_h)
    c.line(x + 0.3*cm + col1_w + col2_w, table_y, x + 0.3*cm + col1_w + col2_w, table_y - row_h)
    
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x + 0.3*cm + col1_w/2, table_y - 0.4*cm, "No Anggota")
    c.drawCentredString(x + 0.3*cm + col1_w + col2_w/2, table_y - 0.4*cm, "Tanggal Kembali")
    c.drawCentredString(x + 0.3*cm + col1_w + col2_w + col3_w/2, table_y - 0.4*cm, "Ket")
    
    # 13 blank rows
    for i in range(13):
        cur_y = table_y - row_h - (i+1)*row_h
        c.rect(x + 0.3*cm, cur_y, card_w - 0.6*cm, row_h)
        c.line(x + 0.3*cm + col1_w, cur_y + row_h, x + 0.3*cm + col1_w, cur_y)
        c.line(x + 0.3*cm + col1_w + col2_w, cur_y + row_h, x + 0.3*cm + col1_w + col2_w, cur_y)'''

new_draw = '''    # Text
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 0.3*cm, y + card_h - 0.7*cm, f"JUDUL     : {judul}")
    
    c.setFont("Helvetica-Bold", 8)
    # Gunakan hanya nomor ID buku seperti yang diminta user (no_induk)
    c.drawString(x + 0.3*cm, y + card_h - 1.2*cm, f"NO BUKU : {no_induk}")
    
    # Table
    table_y = y + card_h - 1.8*cm
    table_w = card_w - 0.6*cm
    col1_w = table_w * 0.3
    col2_w = table_w * 0.45
    col3_w = table_w * 0.25
    
    row_h = 0.55*cm
    
    # Table Header
    c.rect(x + 0.3*cm, table_y - row_h, table_w, row_h)
    c.line(x + 0.3*cm + col1_w, table_y, x + 0.3*cm + col1_w, table_y - row_h)
    c.line(x + 0.3*cm + col1_w + col2_w, table_y, x + 0.3*cm + col1_w + col2_w, table_y - row_h)
    
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x + 0.3*cm + col1_w/2, table_y - 0.4*cm, "No Anggota")
    c.drawCentredString(x + 0.3*cm + col1_w + col2_w/2, table_y - 0.4*cm, "Tanggal Kembali")
    c.drawCentredString(x + 0.3*cm + col1_w + col2_w + col3_w/2, table_y - 0.4*cm, "Ket")
    
    # Fill almost full
    # Height remaining: table_y - row_h - y - 0.3cm = card_h - 1.8 - 0.55 - 0.3 = 9.35 cm
    # 9.35 / 0.55 = 17 rows
    for i in range(17):
        cur_y = table_y - row_h - (i+1)*row_h
        c.rect(x + 0.3*cm, cur_y, table_w, row_h)
        c.line(x + 0.3*cm + col1_w, cur_y + row_h, x + 0.3*cm + col1_w, cur_y)
        c.line(x + 0.3*cm + col1_w + col2_w, cur_y + row_h, x + 0.3*cm + col1_w + col2_w, cur_y)'''

code = code.replace(old_draw, new_draw)

with codecs.open('template_stiker.py', 'w', 'utf-8') as f:
    f.write(code)
