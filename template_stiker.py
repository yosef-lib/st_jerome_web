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
    cols = 2
    rows = 6
    stiker_w = 7.5 * cm
    stiker_h = 4.0 * cm
    
    margin_x = (width - (cols * stiker_w)) / 2
    margin_y = (height - (rows * stiker_h)) / 2

    idx = 0
    for page in range((len(buku_list) // 12) + 1):
        for r in range(rows):
            for col in range(cols):
                if idx >= len(buku_list):
                    break
                
                buku = buku_list[idx]
                
                # Coordinate of bottom-left corner of the sticker
                x = margin_x + col * stiker_w
                y = height - margin_y - (r + 1) * stiker_h
                
                # SET WARNA GARIS KE BIRU
                c.setStrokeColor(colors.blue)
                
                # Draw outer border
                c.rect(x, y, stiker_w, stiker_h)
                
                # Heights from top to bottom
                h1 = 0.6 * cm # NO INDUK
                h2 = 0.6 * cm # TGL TERIMA
                h3 = 0.8 * cm # BELI/HADIAH (adjusted to fit 4.0cm)
                h4 = 1.6 * cm # NO. BUKU
                h5 = 0.4 * cm # KOPI KE
                
                # Y coordinates for horizontal lines (from bottom up)
                y_kopi = y + h5
                y_nobuku = y_kopi + h4
                y_beli = y_nobuku + h3
                y_tgl = y_beli + h2
                
                # Draw horizontal lines (Biru)
                c.line(x, y_kopi, x + stiker_w, y_kopi)
                c.line(x, y_nobuku, x + stiker_w, y_nobuku)
                c.line(x, y_beli, x + stiker_w, y_beli)
                c.line(x, y_tgl, x + stiker_w, y_tgl)
                
                # Draw vertical line (Column separator - Biru)
                col_kiri_w = 3.0 * cm
                c.line(x + col_kiri_w, y, x + col_kiri_w, y + stiker_h)
                
                # SET WARNA TEKS STATIS KE BIRU DAN BOLD
                c.setFillColor(colors.blue)
                c.setFont("Helvetica-Bold", 7)
                
                # Left Column Texts (Biru, Bold)
                c.drawString(x + 0.1*cm, y_tgl + 0.2*cm, "NO INDUK")
                c.drawString(x + 0.1*cm, y_beli + 0.2*cm, "TGL TERIMA")
                c.drawString(x + 0.1*cm, y_nobuku + 0.5*cm, "BELI")
                c.drawString(x + 0.1*cm, y_nobuku + 0.1*cm, "HADIAH")
                c.drawString(x + 0.1*cm, y_kopi + 0.7*cm, "NO. BUKU")
                c.setFont("Helvetica-Bold", 6)
                c.drawString(x + 0.1*cm, y + 0.1*cm, "KOPI KE")
                
                # SET WARNA TEKS ISIAN KE HITAM
                c.setFillColor(colors.black)
                
                # Right Column Texts (Hitam, Bold)
                c.setFont("Helvetica-Bold", 8)
                c.drawString(x + col_kiri_w + 0.2*cm, y_tgl + 0.2*cm, buku.get('no_induk', ''))
                
                # Format Tanggal ke DD-MM-YYYY
                tgl_terima_raw = buku.get('tgl_terima', '')
                tgl_terima_format = tgl_terima_raw
                if tgl_terima_raw:
                    try:
                        # Assuming input from HTML date picker is YYYY-MM-DD
                        dt = datetime.strptime(tgl_terima_raw, '%Y-%m-%d')
                        tgl_terima_format = dt.strftime('%d-%m-%Y')
                    except Exception:
                        pass
                
                c.drawString(x + col_kiri_w + 0.2*cm, y_beli + 0.2*cm, tgl_terima_format)
                
                # Beli / Hadiah (Hitam)
                status = buku.get('status_buku', 'BELI').upper()
                c.drawString(x + col_kiri_w + 0.2*cm, y_nobuku + 0.3*cm, status)
                
                # No Buku / Call Number (Hitam)
                call_number = f"{buku.get('klasifikasi', '')} {buku.get('cutter', '')} {buku.get('huruf_judul', '')}"
                c.setFont("Helvetica-Bold", 10)
                c.drawString(x + col_kiri_w + 0.2*cm, y_kopi + 0.6*cm, call_number)
                
                # Kopi Ke (Hitam)
                c.setFont("Helvetica-Bold", 7)
                c.drawString(x + col_kiri_w + 0.2*cm, y + 0.1*cm, buku.get('copy_ke', '1'))
                
                idx += 1
            if idx >= len(buku_list):
                break
        if idx < len(buku_list):
            c.showPage()
            
    c.save()
    return True

if __name__ == "__main__":
    generate_stiker_pdf()
