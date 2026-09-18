import codecs, re

with codecs.open('template_stiker.py', 'r', 'utf-8') as f:
    code = f.read()

# Fix draw_kantong_buku definition and implementation
old_kantong_def = r"def draw_kantong_buku\(c, x, y\):.*?c\.line\(main_x \+ 0\.5\*cm, main_y \+ main_h - 1\.9\*cm, main_x \+ main_w - 0\.5\*cm, main_y \+ main_h - 1\.9\*cm\)"
new_kantong_def = '''def draw_kantong_buku(c, x, y, buku):
    # Total space: 10.5cm x 9cm
    # y is bottom left
    # Flaps
    c.setLineWidth(0.5)
    c.setFillColorRGB(0.98, 0.98, 0.98) # slightly gray for flaps to indicate glue
    c.rect(x, y + 1*cm, 1*cm, 8*cm, fill=1) # left flap
    c.rect(x + 9.5*cm, y + 1*cm, 1*cm, 8*cm, fill=1) # right flap
    c.rect(x + 1*cm, y, 8.5*cm, 1*cm, fill=1) # bottom flap
    
    c.setFillColorRGB(0, 0, 0)
    
    # Main pocket Dashed
    c.setDash(6, 3)
    c.rect(x + 1*cm, y + 1*cm, 8.5*cm, 8*cm)
    c.setDash(1, 0) # reset
    
    # Header
    main_x = x + 1*cm
    main_y = y + 1*cm
    main_w = 8.5*cm
    main_h = 8*cm
    
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(main_x + main_w/2, main_y + main_h - 1.0*cm, "PERPUSTAKAAN IMAVI")
    
    # Line
    c.line(main_x + 0.5*cm, main_y + main_h - 1.5*cm, main_x + main_w - 0.5*cm, main_y + main_h - 1.5*cm)
    
    judul = buku.get('judul', '')
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
    
code, count1 = re.subn(old_kantong_def, new_kantong_def, code, flags=re.DOTALL)

old_kantong_call = r"draw_kantong_buku\(c, current_x, y_base \+ item_h - comp\['h'\]\)"
new_kantong_call = r"draw_kantong_buku(c, current_x, y_base + item_h - comp['h'], buku)"
code, count2 = re.subn(old_kantong_call, new_kantong_call, code, flags=re.DOTALL)

with codecs.open('template_stiker.py', 'w', 'utf-8') as f:
    f.write(code)
print(f"Replaced {count1} and {count2} times")
