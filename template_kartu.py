import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    pdfmetrics.registerFont(TTFont('Impact', 'C:\\Windows\\Fonts\\impact.ttf'))
    FONT_MAIN = 'Impact'
except:
    FONT_MAIN = 'Helvetica-Bold'


def wrap_text(c, text, font, size, max_width):
    """Bagi teks menjadi beberapa baris agar tidak melebihi max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if c.stringWidth(test, font, size) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def generate_cards_pdf(anggota_list, output_filename="kartu_output.pdf"):
    """
    Layout mengacu pada foto fisik kartu:
    ┌──────────────────────────────────────────────┐
    │ [LOGO]    ST JEROME LIBRARY / KARTU ANGGOTA  │ ← header ungu
    │                                              │
    │  04920002                                    │
    │  ─────────  (garis = lebar angka)            │
    │  YOSEF PASKAH                                │
    │  KARYAWAN                    ┌─────────────┐ │
    │                              │ ▌▌▐▐▌▌▐▌▐▌  │ │ ← barcode hitam
    │                              │ EXP: 2030   │ │   di kotak putih
    │ Jl. Kalisari ...             └─────────────┘ │ ← strip bawah
    └──────────────────────────────────────────────┘

    Ukuran kartu CR80 = 85.6 x 54 mm
    """
    card_w = 85.6 * mm
    card_h = 54.0 * mm

    c = canvas.Canvas(output_filename, pagesize=(card_w, card_h))

    img1 = os.path.join(BASE_DIR, "1.png")
    img2 = os.path.join(BASE_DIR, "2.png")

    # ── Dimensi zona barcode (kanan bawah) ───────────────────────────
    # Berdasarkan foto fisik: kotak putih ≈ lebar 28mm, mulai ±56mm dari kiri
    BC_W       = 27 * mm    # lebar barcode itu sendiri
    BC_H       = 11 * mm    # tinggi batang barcode
    BC_X       = 54 * mm    # X kiri kotak putih (dari kiri kartu)
    BC_Y       = 9  * mm    # Y bawah kotak putih (dari bawah kartu)
    PAD        = 1.5 * mm   # quiet zone di sekeliling barcode
    EXP_H      = 4  * mm    # tinggi area teks EXP di bawah barcode

    # Total tinggi kotak putih = BC_H + PAD*2 + EXP_H
    BOX_H = BC_H + PAD * 2 + EXP_H
    BOX_W = BC_W + PAD * 2

    # ── Zona teks (kiri) — berhenti sebelum kotak putih ──────────────
    TEXT_MAX_X = BC_X - 3 * mm     # ≈ 51mm dari kiri

    for anggota in anggota_list:
        # ── Background (1.png) full bleed ──────────────────────────────
        if os.path.exists(img1):
            c.drawImage(img1, 0, 0, width=card_w, height=card_h,
                        preserveAspectRatio=False)

        member_id = str(anggota.get('member_id', ''))
        nama      = str(anggota.get('nama', '')).upper()
        tipe      = str(anggota.get('tipe_anggota', '')).upper()
        raw_exp   = str(anggota.get('masa_berlaku', ''))
        tahun_exp = raw_exp[:4] if len(raw_exp) >= 4 else raw_exp

        biru = (44/255, 62/255, 114/255)
        x0   = 7 * mm

        # ── Nomor ID ───────────────────────────────────────────────────
        # Dari foto fisik: ID ≈ 57% dari bawah = ~30.8mm
        id_y = 31 * mm
        c.setFillColorRGB(*biru)
        c.setFont(FONT_MAIN, 13)
        c.drawString(x0, id_y, member_id)

        # ── Garis biru — persis sepanjang teks Nomor ID ───────────────
        id_w    = c.stringWidth(member_id, FONT_MAIN, 13)
        garis_y = id_y - 1.5 * mm
        c.setStrokeColorRGB(*biru)
        c.setLineWidth(0.8)
        c.line(x0, garis_y, x0 + id_w, garis_y)

        # Maksimal 4 kata
        words = nama.split()
        if len(words) > 4:
            nama = " ".join(words[:4])
            
        NAMA_SIZE = 12
        LINE_HEIGHT = 5.5 * mm
        nama_lines = wrap_text(c, nama, FONT_MAIN, NAMA_SIZE, TEXT_MAX_X - x0)

        c.setFillColorRGB(*biru)
        c.setFont(FONT_MAIN, NAMA_SIZE)
        nama_y = garis_y - 6 * mm
        
        for line in nama_lines[:2]:      # maks 2 baris agar tidak nabrak
            c.drawString(x0, nama_y, line)
            nama_y -= LINE_HEIGHT

        # Status / Tipe
        c.setFont(FONT_MAIN, 11)
        c.drawString(x0, nama_y - 0.5 * mm, tipe)

        # ═══════════════════════════════════════════════════════════════
        # ── BARCODE — persis SLiMS (EXP di luar kotak putih) ───────────
        # ═══════════════════════════════════════════════════════════════
        BC_H  = 8 * mm      # tinggi bar pendek
        PAD   = 1.5 * mm    # padding tipis sekeliling barcode

        # lquiet=0, rquiet=0 → tidak ada margin bawaan
        bc = code128.Code128(member_id,
                             barHeight=BC_H,
                             barWidth=0.20 * mm,
                             lquiet=0,
                             rquiet=0)
        bc_w = bc.width

        # Kotak putih = hanya seukuran barcode + padding tipis
        box_w = bc_w + PAD * 2
        box_h = BC_H + PAD * 2

        # Posisi: rata kanan kartu, 5mm dari tepi kanan, digeser agak ke bawah
        box_x = card_w - box_w - 5 * mm
        box_y = 7.5 * mm     # diturunkan (sebelumnya 10.5mm)
        bc_x  = box_x + PAD
        bc_y  = box_y + PAD

        # 1. Kotak putih (hanya untuk barcode)
        c.saveState()
        c.setFillColorRGB(1, 1, 1)
        c.setStrokeColorRGB(1, 1, 1)
        c.rect(box_x, box_y, box_w, box_h, fill=1, stroke=0)
        c.restoreState()

        # 2. Barcode hitam
        c.saveState()
        c.setFillColorRGB(0, 0, 0)
        c.setStrokeColorRGB(0, 0, 0)
        bc.drawOn(c, bc_x, bc_y)
        c.restoreState()

        # 3. EXP di LUAR kotak, di bawahnya (warna biru)
        c.setFillColorRGB(*biru)
        c.setFont('Helvetica-Bold', 7)
        c.drawCentredString(box_x + box_w / 2,
                            box_y - 2.5 * mm,
                            f"EXP : {tahun_exp}")

        c.showPage()

    # ── Halaman terakhir: sisi belakang kartu (2.png) — 1 kali saja ──
    if os.path.exists(img2):
        c.drawImage(img2, 0, 0, width=card_w, height=card_h,
                    preserveAspectRatio=False)
        c.showPage()

    c.save()


if __name__ == '__main__':
    test_data = [
        {'member_id': '04920002', 'nama': 'YOSEF PASKAH',
         'tipe_anggota': 'Karyawan', 'masa_berlaku': '2030-01-01'},
        {'member_id': '700126004', 'nama': 'FRANCISCO KRISNA AJI PAMUNGKAS',
         'tipe_anggota': 'Frater', 'masa_berlaku': '2029-08-08'},
    ]
    generate_cards_pdf(test_data, 'test.pdf')
    print("Selesai: test.pdf")
