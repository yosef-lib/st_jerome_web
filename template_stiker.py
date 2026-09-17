import os
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from datetime import datetime

def generate_stiker_pdf(antrean_file='antrian_stiker.json', output_file='stiker_output.pdf'):
    if not os.path.exists(antrean_file):
        return False

    with open(antrean_file, 'r') as f:
        try:
            buku_list = json.load(f)
        except:
            buku_list = []

    if not buku_list:
        return False

    c = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4

    # Grid settings
    cols = 1
    rows = 5 # 5 rows * 5cm = 25cm. Fits well in 29.7cm A4 height
    
    stiker_w = 7.5 * cm
    stiker_h = 4.0 * cm
    
    # Spine label specs from User Image (1.7cm header + 3.3cm body = 5cm total)
    spine_w = 4.5 * cm
    spine_h = 5.0 * cm
    spine_gap = 0.5 * cm
    
    item_w = spine_w + spine_gap + stiker_w
    item_h = max(spine_h, stiker_h)
    
    # User requested margin to be shifted to the left
    margin_x = 2.0 * cm 
    margin_y = (height - (rows * item_h)) / 2

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
                y_base = height - margin_y - (r + 1) * item_h
                
                # --- DRAW SPINE LABEL ---
                x_spine = x_base
                y_spine = y_base + (item_h - spine_h) # Top-aligned
                
                # Draw header background (DRAW FIRST SO IT DOES NOT COVER BORDERS)
                header_h = 1.7 * cm
                c.setFillColorRGB(0.7, 0.7, 0.7) # Abu-abu agak tua
                c.rect(x_spine, y_spine + spine_h - header_h, spine_w, header_h, fill=1, stroke=0)
                
                # Draw main border and lines
                c.setLineWidth(1.5) # Garis agak tebal
                c.setStrokeColor(colors.black)
                
                # Kotak luar
                c.rect(x_spine, y_spine, spine_w, spine_h, fill=0, stroke=1)
                
                # Garis pemisah header
                c.line(x_spine, y_spine + spine_h - header_h, x_spine + spine_w, y_spine + spine_h - header_h)
                
                # Header Text
                c.setFillColor(colors.black)
                c.setFont("Helvetica-Bold", 12)
                c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - 0.7*cm, "PERPUSTAKAAN")
                c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - 1.3*cm, "IMAVI")
                
                # Body Text (Call Number)
                c.setFont("Helvetica-Bold", 14)
                klasifikasi = buku.get('klasifikasi', '')
                c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - header_h - 0.9*cm, klasifikasi)
                
                pengarang = buku.get('pengarang', '')
                cutter = buku.get('cutter', '')
                if not cutter and pengarang:
                    cutter = pengarang[:3].upper()
                c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - header_h - 1.8*cm, cutter)
                
                judul = buku.get('judul', '')
                huruf_judul = buku.get('huruf_judul', '')
                if not huruf_judul and judul:
                    huruf_judul = judul[0].lower()
                c.drawCentredString(x_spine + (spine_w/2), y_spine + spine_h - header_h - 2.7*cm, huruf_judul)
                
                
                # --- DRAW EXISTING STICKER ---
                c.setLineWidth(1.0) # Kembalikan tebal garis ke normal untuk stiker
                
                x_stiker = x_base + spine_w + spine_gap
                y_stiker = y_base + (item_h - stiker_h) # Top-aligned with spine
                
                # SET WARNA GARIS KE BIRU
                c.setStrokeColor(colors.blue)
                
                # Draw outer border
                c.rect(x_stiker, y_stiker, stiker_w, stiker_h)
                
                # Heights from top to bottom
                h1 = 0.6 * cm # NO INDUK
                h2 = 0.6 * cm # TGL TERIMA
                h3 = 0.8 * cm # BELI/HADIAH
                h4 = 1.6 * cm # NO. BUKU
                h5 = 0.4 * cm # KOPI KE
                
                y_kopi = y_stiker + h5
                y_nobuku = y_kopi + h4
                y_beli = y_nobuku + h3
                y_tgl = y_beli + h2
                
                # Draw horizontal lines (Biru)
                c.line(x_stiker, y_kopi, x_stiker + stiker_w, y_kopi)
                c.line(x_stiker, y_nobuku, x_stiker + stiker_w, y_nobuku)
                c.line(x_stiker, y_beli, x_stiker + stiker_w, y_beli)
                c.line(x_stiker, y_tgl, x_stiker + stiker_w, y_tgl)
                
                # Draw vertical line (Column separator - Biru)
                col_kiri_w = 3.0 * cm
                c.line(x_stiker + col_kiri_w, y_stiker, x_stiker + col_kiri_w, y_stiker + stiker_h)
                
                # SET WARNA TEKS STATIS KE BIRU DAN BOLD
                c.setFillColor(colors.blue)
                c.setFont("Helvetica-Bold", 7)
                
                # Left Column Texts
                c.drawString(x_stiker + 0.1*cm, y_tgl + 0.2*cm, "NO INDUK")
                c.drawString(x_stiker + 0.1*cm, y_beli + 0.2*cm, "TGL TERIMA")
                c.drawString(x_stiker + 0.1*cm, y_nobuku + 0.5*cm, "BELI")
                c.drawString(x_stiker + 0.1*cm, y_nobuku + 0.1*cm, "HADIAH")
                c.drawString(x_stiker + 0.1*cm, y_kopi + 0.7*cm, "NO. BUKU")
                c.setFont("Helvetica-Bold", 6)
                c.drawString(x_stiker + 0.1*cm, y_stiker + 0.1*cm, "KOPI KE")
                
                # SET WARNA TEKS ISIAN KE HITAM
                c.setFillColor(colors.black)
                
                # Right Column Texts (Hitam, Bold)
                c.setFont("Helvetica-Bold", 8)
                c.drawString(x_stiker + col_kiri_w + 0.2*cm, y_tgl + 0.2*cm, buku.get('no_induk', ''))
                
                # Format Tanggal ke DD-MM-YYYY
                tgl_terima_raw = buku.get('tgl_terima', '')
                tgl_terima_format = tgl_terima_raw
                if tgl_terima_raw:
                    try:
                        dt = datetime.strptime(tgl_terima_raw, '%Y-%m-%d')
                        tgl_terima_format = dt.strftime('%d-%m-%Y')
                    except Exception:
                        pass
                
                c.drawString(x_stiker + col_kiri_w + 0.2*cm, y_beli + 0.2*cm, tgl_terima_format)
                
                # Beli / Hadiah
                status = buku.get('status_buku', 'BELI').upper()
                c.drawString(x_stiker + col_kiri_w + 0.2*cm, y_nobuku + 0.3*cm, status)
                
                # No Buku / Call Number
                call_number = f"{klasifikasi} {cutter} {huruf_judul}"
                c.setFont("Helvetica-Bold", 10)
                c.drawString(x_stiker + col_kiri_w + 0.2*cm, y_kopi + 0.6*cm, call_number)
                
                # Kopi Ke
                c.setFont("Helvetica-Bold", 7)
                c.drawString(x_stiker + col_kiri_w + 0.2*cm, y_stiker + 0.1*cm, buku.get('copy_ke', '1'))
                
                idx += 1
            if idx >= len(buku_list):
                break
        if idx < len(buku_list):
            c.showPage()
            
    c.save()
    return True

if __name__ == "__main__":
    generate_stiker_pdf()
