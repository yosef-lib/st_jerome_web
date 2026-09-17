import codecs

with codecs.open('template_stiker.py', 'r', 'utf-8') as f:
    code = f.read()

# Replace the layout configuration and drawing order
# We will use Regex or manual replacement for the whole logic inside the loop

start_marker = "    # Grid settings"
end_marker = "    c.save()"

new_layout = '''    # Grid settings
    cols = 1
    rows = 5
    
    stiker_w = 7.5 * cm
    stiker_h = 4.0 * cm
    
    spine_w = 4.5 * cm
    spine_h = 5.0 * cm
    
    barcode_w = 4.0 * cm
    barcode_h = 3.0 * cm
    
    gap_x = 0.5 * cm
    gap_y = 0.6 * cm # Vertical gap between rows to prevent touching!
    
    item_w = stiker_w + gap_x + spine_w + gap_x + barcode_w
    item_h = max(spine_h, stiker_h, barcode_h)
    
    margin_x = (width - item_w) / 2 # Centered perfectly on A4
    margin_y = (height - (rows * item_h + (rows-1) * gap_y)) / 2

    idx = 0
    items_per_page = cols * rows
    total_pages = (len(buku_list) // items_per_page) + (1 if len(buku_list) % items_per_page > 0 else 0)
    
    for page in range(total_pages):
        for r in range(rows):
            for col in range(cols):
                if idx >= len(buku_list):
                    break
                
                buku = buku_list[idx]
                
                # Coordinate of bottom-left corner of the ENTIRE item block
                x_base = margin_x + col * item_w
                # Adjusted for gap_y
                y_base = height - margin_y - (r * (item_h + gap_y)) - item_h
                
                # 1. --- DRAW EXISTING STICKER (LEFT) ---
                c.setLineWidth(1.0)
                x_stiker = x_base
                y_stiker = y_base + (item_h - stiker_h) # Top-aligned
                
                c.setStrokeColor(colors.blue)
                c.rect(x_stiker, y_stiker, stiker_w, stiker_h)
                
                h1 = 0.6 * cm
                h2 = 0.6 * cm
                h3 = 0.8 * cm
                h4 = 1.6 * cm
                h5 = 0.4 * cm
                
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
                if not cutter and pengarang:
                    cutter = pengarang[:3].upper()
                judul = buku.get('judul', '')
                huruf_judul = buku.get('huruf_judul', '')
                if not huruf_judul and judul:
                    huruf_judul = judul[0].lower()
                    
                call_number = f"{klasifikasi} {cutter} {huruf_judul}"
                c.setFont("Helvetica-Bold", 10)
                c.drawString(x_stiker + col_kiri_w + 0.2*cm, y_kopi + 0.6*cm, call_number)
                
                c.setFont("Helvetica-Bold", 7)
                c.drawString(x_stiker + col_kiri_w + 0.2*cm, y_stiker + 0.1*cm, buku.get('copy_ke', '1'))
                
                
                # 2. --- DRAW SPINE LABEL (MIDDLE) ---
                x_spine = x_stiker + stiker_w + gap_x
                y_spine = y_base + (item_h - spine_h) # Top-aligned
                
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
                
                c.setFont("Helvetica-Bold", 14)
                c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - header_h_spine - 0.9*cm, klasifikasi)
                c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - header_h_spine - 1.8*cm, cutter)
                c.setFont("Helvetica", 14)
                c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - header_h_spine - 2.7*cm, huruf_judul)
                
                
                # 3. --- DRAW BARCODE LABEL (RIGHT) ---
                x_barcode = x_spine + spine_w + gap_x
                y_barcode = y_base + (item_h - barcode_h) # Top-aligned
                
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
                
                barcode_val = buku.get('no_induk', '')
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
                
                idx += 1
            if idx >= len(buku_list):
                break
        if idx < len(buku_list):
            c.showPage()
            
    c.save()'''

# Splice the new logic in
pre = code[:code.find(start_marker)]
post = code[code.find(end_marker) + len(end_marker):]
new_full_code = pre + new_layout + post

with codecs.open('template_stiker.py', 'w', 'utf-8') as f:
    f.write(new_full_code)

print("done reordering layout")
