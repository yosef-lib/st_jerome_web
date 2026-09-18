import codecs

with codecs.open('template_stiker.py', 'r', 'utf-8') as f:
    code = f.read()

drawing_functions = '''
def draw_kartu_buku(c, x, y, buku):
    card_w = 7.5*cm
    card_h = 12.0*cm
    
    # Border
    c.setLineWidth(1)
    c.rect(x, y, card_w, card_h)
    
    judul = buku.get('judul', '')
    if len(judul) > 35:
        judul = judul[:32] + '...'
        
    no_induk = str(buku.get('no_induk', ''))
    klasifikasi = buku.get('klasifikasi', '')
    cutter = buku.get('cutter', '')
    huruf_judul = buku.get('huruf_judul', '')
    if not cutter and buku.get('pengarang'): cutter = buku.get('pengarang')[:3].upper()
    if not huruf_judul and judul: huruf_judul = judul[0].lower()
    no_buku = f"{klasifikasi} {cutter} {huruf_judul} / {no_induk}".strip()
    
    # Text
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
        c.line(x + 0.3*cm + col1_w + col2_w, cur_y + row_h, x + 0.3*cm + col1_w + col2_w, cur_y)

def draw_kantong_buku(c, x, y):
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
    c.setFont("Helvetica", 9)
    c.drawCentredString(main_x + main_w/2, main_y + main_h - 1.6*cm, "Kantong Buku")
    
    # Line
    c.line(main_x + 0.5*cm, main_y + main_h - 1.9*cm, main_x + main_w - 0.5*cm, main_y + main_h - 1.9*cm)
'''

# insert the functions before generate_stiker_pdf
code = code.replace("def generate_stiker_pdf", drawing_functions + "\ndef generate_stiker_pdf")

# Update components
old_comp = '''    components = []
    if options.get('identitas'): components.append({'type': 'identitas', 'w': 8.0*cm, 'h': 5.0*cm})
    if options.get('punggung'): components.append({'type': 'punggung', 'w': 4.5*cm, 'h': 5.0*cm})
    if options.get('barcode'): components.append({'type': 'barcode', 'w': 4.0*cm, 'h': 3.0*cm})'''

new_comp = '''    components = []
    if options.get('identitas'): components.append({'type': 'identitas', 'w': 8.0*cm, 'h': 5.0*cm})
    if options.get('punggung'): components.append({'type': 'punggung', 'w': 4.5*cm, 'h': 5.0*cm})
    if options.get('barcode'): components.append({'type': 'barcode', 'w': 4.0*cm, 'h': 3.0*cm})
    if options.get('kartu'): components.append({'type': 'kartu', 'w': 7.5*cm, 'h': 12.0*cm})
    if options.get('kantong'): components.append({'type': 'kantong', 'w': 10.5*cm, 'h': 9.0*cm})'''

code = code.replace(old_comp, new_comp)

# Update drawing dispatch
old_draw = '''            if comp['type'] == 'identitas':
                draw_identitas(c, cur_x, draw_y, buku)
            elif comp['type'] == 'punggung':
                draw_punggung(c, cur_x, draw_y, buku)
            elif comp['type'] == 'barcode':
                # Center vertically if shorter than others
                y_offset = (item_h - comp['h']) / 2
                draw_barcode(c, cur_x, draw_y + y_offset, buku)
            
            cur_x += comp['w'] + gap_x'''

new_draw = '''            if comp['type'] == 'identitas':
                draw_identitas(c, cur_x, draw_y, buku)
            elif comp['type'] == 'punggung':
                draw_punggung(c, cur_x, draw_y, buku)
            elif comp['type'] == 'barcode':
                # Center vertically if shorter than others
                y_offset = (item_h - comp['h']) / 2
                draw_barcode(c, cur_x, draw_y + y_offset, buku)
            elif comp['type'] == 'kartu':
                draw_kartu_buku(c, cur_x, draw_y, buku)
            elif comp['type'] == 'kantong':
                y_offset = item_h - comp['h'] # bottom align or top align? top align
                draw_kantong_buku(c, cur_x, draw_y + y_offset)
                
            cur_x += comp['w'] + gap_x'''

code = code.replace(old_draw, new_draw)

# Handle default options if none
old_opt = "options = {'identitas': True, 'punggung': True, 'barcode': True}"
new_opt = "options = {'identitas': True, 'punggung': True, 'barcode': True, 'kartu': False, 'kantong': False}"
code = code.replace(old_opt, new_opt)

with codecs.open('template_stiker.py', 'w', 'utf-8') as f:
    f.write(code)
print("template_stiker updated")
