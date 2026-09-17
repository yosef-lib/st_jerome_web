import json
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.graphics.barcode import code128

def draw_identitas(c, x_stiker, y_base, item_h, buku):
    stiker_w = 7.5 * cm
    stiker_h = 4.0 * cm
    y_stiker = y_base + (item_h - stiker_h)
    
    c.setLineWidth(1.0)
    c.setStrokeColor(colors.blue)
    c.rect(x_stiker, y_stiker, stiker_w, stiker_h)
    
    h1, h2, h3, h4, h5 = 0.6 * cm, 0.6 * cm, 0.8 * cm, 1.6 * cm, 0.4 * cm
    y_kopi = y_stiker + h5
    y_nobuku = y_kopi + h4
    y_beli = y_nobuku + h3
    y_tgl = y_beli + h2
    
    c.line(x_stiker, y_kopi, x_stiker + stiker_w, y_kopi)
    c.line(x_stiker, y_nobuku, x_stiker + stiker_w, y_nobuku)
    c.line(x_stiker, y_beli, x_stiker + stiker_w, y_beli)
    c.line(x_stiker, y_tgl, x_stiker + stiker_w, y_tgl)
    
    col_kiri_w = 3.0 * cm
    c.line(x_stiker + col_kiri_w, y_stiker, x_stiker + col_kiri_w, y_stiker + stiker_h)
    
    c.setFillColor(colors.blue)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(x_stiker + 0.1*cm, y_tgl + 0.2*cm, "NO INDUK")
    c.drawString(x_stiker + 0.1*cm, y_beli + 0.2*cm, "TGL TERIMA")
    c.drawString(x_stiker + 0.1*cm, y_nobuku + 0.5*cm, "BELI")
    c.drawString(x_stiker + 0.1*cm, y_nobuku + 0.1*cm, "HADIAH")
    c.drawString(x_stiker + 0.1*cm, y_kopi + 0.7*cm, "NO. BUKU")
    c.setFont("Helvetica-Bold", 6)
    c.drawString(x_stiker + 0.1*cm, y_stiker + 0.1*cm, "KOPI KE")
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x_stiker + col_kiri_w + 0.2*cm, y_tgl + 0.2*cm, buku.get('no_induk', ''))
    
    tgl_terima_raw = buku.get('tgl_terima', '')
    tgl_terima_format = tgl_terima_raw
    if tgl_terima_raw:
        try:
            dt = datetime.strptime(tgl_terima_raw, '%Y-%m-%d')
            tgl_terima_format = dt.strftime('%d-%m-%Y')
        except Exception:
            pass
    c.drawString(x_stiker + col_kiri_w + 0.2*cm, y_beli + 0.2*cm, tgl_terima_format)
    
    status = buku.get('status_buku', 'BELI').upper()
    c.drawString(x_stiker + col_kiri_w + 0.2*cm, y_nobuku + 0.3*cm, status)
    
    klasifikasi = buku.get('klasifikasi', '')
    pengarang = buku.get('pengarang', '')
    cutter = buku.get('cutter', '')
    if not cutter and pengarang: cutter = pengarang[:3].upper()
    judul = buku.get('judul', '')
    huruf_judul = buku.get('huruf_judul', '')
    if not huruf_judul and judul: huruf_judul = judul[0].lower()
        
    call_number = f"{klasifikasi} {cutter} {huruf_judul}"
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x_stiker + col_kiri_w + 0.2*cm, y_kopi + 0.6*cm, call_number)
    
    c.setFont("Helvetica-Bold", 7)
    c.drawString(x_stiker + col_kiri_w + 0.2*cm, y_stiker + 0.1*cm, buku.get('copy_ke', '1'))


def draw_punggung(c, x_spine, y_base, item_h, buku):
    spine_w = 4.5 * cm
    spine_h = 5.0 * cm
    y_spine = y_base + (item_h - spine_h)
    
    header_h_spine = 1.7 * cm
    c.setFillColorRGB(0.7, 0.7, 0.7)
    c.rect(x_spine, y_spine + spine_h - header_h_spine, spine_w, header_h_spine, fill=1, stroke=0)
    
    c.setLineWidth(1.5)
    c.setStrokeColor(colors.black)
    c.rect(x_spine, y_spine, spine_w, spine_h, fill=0, stroke=1)
    c.line(x_spine, y_spine + spine_h - header_h_spine, x_spine + spine_w, y_spine + spine_h - header_h_spine)
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - 0.7*cm, "PERPUSTAKAAN")
    c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - 1.3*cm, "IMAVI")
    
    klasifikasi = buku.get('klasifikasi', '')
    pengarang = buku.get('pengarang', '')
    cutter = buku.get('cutter', '')
    if not cutter and pengarang: cutter = pengarang[:3].upper()
    judul = buku.get('judul', '')
    huruf_judul = buku.get('huruf_judul', '')
    if not huruf_judul and judul: huruf_judul = judul[0].lower()
    
    if not klasifikasi or not cutter:
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.red)
        c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - header_h_spine - 1.2*cm, "TIDAK")
        c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - header_h_spine - 1.8*cm, "LENGKAP")
    else:
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - header_h_spine - 0.9*cm, klasifikasi)
        c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - header_h_spine - 1.8*cm, cutter)
        c.setFont("Helvetica", 14)
        c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - header_h_spine - 2.7*cm, huruf_judul)


def draw_barcode(c, x_barcode, y_base, item_h, buku):
    barcode_w = 4.0 * cm
    barcode_h = 3.0 * cm
    y_barcode = y_base + (item_h - barcode_h)
    
    header_h_bc = 0.6 * cm
    c.setFillColorRGB(0.85, 0.85, 0.85)
    c.rect(x_barcode, y_barcode + barcode_h - header_h_bc, barcode_w, header_h_bc, fill=1, stroke=0)
    
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.5)
    c.rect(x_barcode, y_barcode, barcode_w, barcode_h)
    c.line(x_barcode, y_barcode + barcode_h - header_h_bc, x_barcode + barcode_w, y_barcode + barcode_h - header_h_bc)
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(x_barcode + barcode_w/2, y_barcode + barcode_h - 0.45*cm, "PERPUSTAKAAN IMAVI")
    
    judul = buku.get('judul', '')
    trunc_title = judul[:50]
    if len(trunc_title) > 25:
        split_idx = trunc_title.rfind(' ', 0, 26)
        if split_idx == -1: split_idx = 25
        line1 = trunc_title[:split_idx].strip()
        line2 = trunc_title[split_idx:].strip()
        if len(judul) > 50: line2 += "..."
    else:
        line1 = trunc_title
        line2 = ""
    
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(x_barcode + barcode_w/2, y_barcode + barcode_h - 0.95*cm, line1)
    if line2:
        c.drawCentredString(x_barcode + barcode_w/2, y_barcode + barcode_h - 1.25*cm, line2)
    
    barcode_val = str(buku.get('no_induk', ''))
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(x_barcode + barcode_w/2, y_barcode + 0.15*cm, barcode_val)
    
    if barcode_val:
        bw = 1.2
        max_width = barcode_w - 0.4*cm
        bc = code128.Code128(barcode_val, barHeight=1.2*cm, barWidth=bw)
        while bc.width > max_width and bw > 0.2:
            bw -= 0.05
            bc = code128.Code128(barcode_val, barHeight=1.2*cm, barWidth=bw)
        
        bc_x = x_barcode + (barcode_w - bc.width)/2
        bc_y = y_barcode + 0.45*cm
        bc.drawOn(c, bc_x, bc_y)



def draw_kartu_buku(c, x, y, buku):
    card_w = 7.5*cm
    card_h = 12.0*cm
    
    # Border
    c.setLineWidth(1)
    c.rect(x, y, card_w, card_h)
    
    judul = buku.get('judul', '')
    
    # Reformat "Seri Dokumen Gerejawi" 
    if "Seri Dokumen Gerejawi" in judul and (";" in judul or ":" in judul or "-" in judul):
        # find the delimiter
        import re
        parts = re.split(r'[;:\-]', judul, maxsplit=1)
        if len(parts) >= 2:
            series_part = parts[0].strip()
            title_part = parts[1].strip()
            # If the series part is the one containing "Seri Dokumen"
            if "Seri Dokumen" in series_part:
                series_part = series_part.replace("Seri Dokumen Gerejawi", "SDG")
                judul = f"{title_part} ({series_part})"
            


        
    no_induk = str(buku.get('no_induk', ''))
    klasifikasi = buku.get('klasifikasi', '')
    cutter = buku.get('cutter', '')
    huruf_judul = buku.get('huruf_judul', '')
    if not cutter and buku.get('pengarang'): cutter = buku.get('pengarang')[:3].upper()
    if not huruf_judul and judul: huruf_judul = judul[0].lower()
    no_buku = f"{klasifikasi} {cutter} {huruf_judul} / {no_induk}".strip()
    
    # Text
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
    c.drawString(x + 0.3*cm, y + card_h - 1.4*cm, f"NO BUKU : {no_induk}")
    
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
        c.line(x + 0.3*cm + col1_w + col2_w, cur_y + row_h, x + 0.3*cm + col1_w + col2_w, cur_y)

def draw_kantong_buku(c, x, y, buku):
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
    c.drawCentredString(main_x + main_w/2, text_y - 0.3*cm, f"ID: {no_induk}")

def generate_stiker_pdf(antrean_file, output_file, options=None):
    if not os.path.exists(antrean_file):
        print(f"File {antrean_file} tidak ditemukan.")
        return
        
    try:
        with open(antrean_file, 'r') as f:
            buku_list = json.load(f)
    except Exception as e:
        print(f"Gagal membaca JSON antrean: {e}")
        buku_list = []
        
    if not buku_list:
        print("Antrean kosong.")
        return
        
    if options is None:
        options = {'identitas': True, 'punggung': True, 'barcode': True, 'kartu': False, 'kantong': False}
        
    components = []
    if options.get('identitas'): components.append({'type': 'identitas', 'w': 7.5*cm, 'h': 4.0*cm})
    if options.get('punggung'): components.append({'type': 'punggung', 'w': 4.5*cm, 'h': 5.0*cm})
    if options.get('barcode'): components.append({'type': 'barcode', 'w': 4.0*cm, 'h': 3.0*cm})
    if options.get('kartu'): components.append({'type': 'kartu', 'w': 7.5*cm, 'h': 12.0*cm})
    if options.get('kantong'): components.append({'type': 'kantong', 'w': 10.5*cm, 'h': 9.0*cm})
    
    if not components:
        print("Tidak ada opsi cetak yang dipilih.")
        return

    c = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4
    
    gap_x = 0.5 * cm
    gap_y = 0.6 * cm
    note_h = 0.4 * cm
    
    item_w = sum(c['w'] for c in components) + gap_x * (len(components) - 1)
    item_h = max(c['h'] for c in components)
    item_h_with_note = item_h + note_h
    
    cols = 1
    while (cols + 1) * item_w + cols * gap_x <= width - 1.0 * cm:
        cols += 1
        
    rows = 1
    while (rows + 1) * item_h_with_note + rows * gap_y <= height - 1.0 * cm:
        rows += 1
        
    total_grid_w = cols * item_w + (cols - 1) * gap_x
    margin_x = (width - total_grid_w) / 2
    
    total_grid_h = rows * item_h_with_note + (rows - 1) * gap_y
    margin_y = (height - total_grid_h) / 2

    idx = 0
    while idx < len(buku_list):
        for r in range(rows):
            for col in range(cols):
                if idx >= len(buku_list):
                    break
                
                buku = buku_list[idx]
                
                x_base = margin_x + col * (item_w + gap_x)
                y_base = height - margin_y - (r * (item_h_with_note + gap_y)) - item_h_with_note
                
                # Draw Librarian Note
                c.setFillColor(colors.gray)
                c.setFont("Helvetica", 7)
                note_text = f"[{buku.get('no_induk', '')}] - {buku.get('judul', '')[:35]} - {buku.get('pengarang', '')[:20]}"
                c.drawString(x_base, y_base + item_h + 0.15*cm, note_text)
                
                # Draw components
                current_x = x_base
                for comp in components:
                    if comp['type'] == 'identitas':
                        draw_identitas(c, current_x, y_base, item_h, buku)
                    elif comp['type'] == 'punggung':
                        draw_punggung(c, current_x, y_base, item_h, buku)
                    elif comp['type'] == 'barcode':
                        draw_barcode(c, current_x, y_base, item_h, buku)
                    elif comp['type'] == 'kartu':
                        draw_kartu_buku(c, current_x, y_base + item_h - comp['h'], buku)
                    elif comp['type'] == 'kantong':
                        draw_kantong_buku(c, current_x, y_base + item_h - comp['h'], buku)
                    
                    current_x += comp['w'] + gap_x
                
                idx += 1
            if idx >= len(buku_list):
                break
        if idx < len(buku_list):
            c.showPage()
            
    c.save()
