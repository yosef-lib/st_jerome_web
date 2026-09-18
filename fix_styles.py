import codecs, re

with codecs.open('template_stiker.py', 'r', 'utf-8') as f:
    code = f.read()

# Make sure we reset fill color for all drawing functions
# We'll just prepend c.setFillColorRGB(0, 0, 0) to draw_kartu_buku

def format_judul(judul):
    import re
    if "Seri Dokumen Gerejawi" in judul and (";" in judul or ":" in judul or "-" in judul):
        parts = re.split(r'[;:\-]', judul, maxsplit=1)
        if len(parts) >= 2:
            series_part = parts[0].strip()
            title_part = parts[1].strip()
            if "Seri Dokumen" in series_part:
                series_part = series_part.replace("Seri Dokumen Gerejawi", "SDG")
                return f"{title_part} ({series_part})"
    return judul

old_kartu_draw = '''    # Text
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

new_kartu_draw = '''    c.setFillColorRGB(0, 0, 0)
    # Text
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 0.3*cm, y + card_h - 0.6*cm, "JUDUL     : ")
    
    import textwrap
    wrapped = textwrap.wrap(judul, width=33)
    
    c.setFont("Courier-Bold", 8)
    if len(wrapped) >= 1:
        c.drawString(x + 1.8*cm, y + card_h - 0.6*cm, wrapped[0])
    if len(wrapped) >= 2:
        line2 = wrapped[1]
        if len(wrapped) > 2:
            line2 = line2[:29] + '...'
        c.drawString(x + 1.8*cm, y + card_h - 0.95*cm, line2)
        
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 0.3*cm, y + card_h - 1.4*cm, "NO BUKU : ")
    c.setFont("Courier-Bold", 8)
    c.drawString(x + 1.8*cm, y + card_h - 1.4*cm, no_induk)'''

code = code.replace(old_kartu_draw, new_kartu_draw)

# For kantong
old_kantong_draw = '''    judul = buku.get('judul', '')
    no_induk = str(buku.get('no_induk', ''))
    
    import textwrap
    wrapped = textwrap.wrap(judul, width=32)
    
    c.setFont("Helvetica-Bold", 9)
    text_y = main_y + main_h - 2.5*cm
    for line in wrapped[:3]:
        c.drawCentredString(main_x + main_w/2, text_y, line)
        text_y -= 0.5*cm
        
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(main_x + main_w/2, text_y - 0.3*cm, f"ID: {no_induk}")'''

new_kantong_draw = '''    judul = buku.get('judul', '')
    import re
    if "Seri Dokumen Gerejawi" in judul and (";" in judul or ":" in judul or "-" in judul):
        parts = re.split(r'[;:\-]', judul, maxsplit=1)
        if len(parts) >= 2:
            series_part = parts[0].strip()
            title_part = parts[1].strip()
            if "Seri Dokumen" in series_part:
                series_part = series_part.replace("Seri Dokumen Gerejawi", "SDG")
                judul = f"{title_part} ({series_part})"
                
    no_induk = str(buku.get('no_induk', ''))
    
    import textwrap
    wrapped = textwrap.wrap(judul, width=34)
    
    c.setFont("Courier-Bold", 9)
    text_y = main_y + main_h - 2.5*cm
    for line in wrapped[:3]:
        c.drawCentredString(main_x + main_w/2, text_y, line)
        text_y -= 0.5*cm
        
    c.setFont("Courier-Bold", 10)
    c.drawCentredString(main_x + main_w/2, text_y - 0.3*cm, no_induk)'''

code = code.replace(old_kantong_draw, new_kantong_draw)

with codecs.open('template_stiker.py', 'w', 'utf-8') as f:
    f.write(code)
print("Styles fixed")
