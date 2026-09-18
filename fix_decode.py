import codecs

with codecs.open('template_stiker.py', 'r', 'utf-8') as f:
    code = f.read()

# Fix barcode_val = str(buku.get('no_induk', ''))
code = code.replace("barcode_val = buku.get('no_induk', '')", "barcode_val = str(buku.get('no_induk', ''))")

# Add "DATA TIDAK LENGKAP" warning on Spine label if klasifikasi or cutter is missing
old_spine = '''    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - header_h_spine - 0.9*cm, klasifikasi)
    c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - header_h_spine - 1.8*cm, cutter)
    c.setFont("Helvetica", 14)
    c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - header_h_spine - 2.7*cm, huruf_judul)'''

new_spine = '''    if not klasifikasi or not cutter:
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.red)
        c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - header_h_spine - 1.2*cm, "TIDAK")
        c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - header_h_spine - 1.8*cm, "LENGKAP")
    else:
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - header_h_spine - 0.9*cm, klasifikasi)
        c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - header_h_spine - 1.8*cm, cutter)
        c.setFont("Helvetica", 14)
        c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - header_h_spine - 2.7*cm, huruf_judul)'''

code = code.replace(old_spine, new_spine)

with codecs.open('template_stiker.py', 'w', 'utf-8') as f:
    f.write(code)
print("template fixed")
