from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.graphics.barcode import code128

c = canvas.Canvas('test_barcode.pdf')
barcode_w = 4.0 * cm
barcode_h = 3.0 * cm
x_barcode = 5 * cm
y_barcode = 15 * cm

# Draw outer border
c.setStrokeColor(colors.black)
c.setLineWidth(1.0)
c.rect(x_barcode, y_barcode, barcode_w, barcode_h)

# Header background
header_h = 0.6 * cm
c.setFillColorRGB(0.85, 0.85, 0.85)
c.rect(x_barcode, y_barcode + barcode_h - header_h, barcode_w, header_h, fill=1, stroke=0)

# Header border
c.setStrokeColor(colors.black)
c.line(x_barcode, y_barcode + barcode_h - header_h, x_barcode + barcode_w, y_barcode + barcode_h - header_h)

# Header text
c.setFillColor(colors.black)
c.setFont("Helvetica-Bold", 7.5)
c.drawCentredString(x_barcode + barcode_w/2, y_barcode + barcode_h - 0.45*cm, "PERPUSTAKAAN IMAVI")

# Title (Wrapped)
full_title = "Seri Dokumen Gerejawi No. 18; Dominum Et Vivifican asdf asdf"
trunc_title = full_title[:50]
if len(trunc_title) > 25:
    split_idx = trunc_title.rfind(' ', 0, 26)
    if split_idx == -1: split_idx = 25
    line1 = trunc_title[:split_idx].strip()
    line2 = trunc_title[split_idx:].strip()
    if len(full_title) > 50:
        line2 += "..."
else:
    line1 = trunc_title
    line2 = ""

c.setFont("Helvetica", 6.5)
c.drawCentredString(x_barcode + barcode_w/2, y_barcode + barcode_h - 0.95*cm, line1)
if line2:
    c.drawCentredString(x_barcode + barcode_w/2, y_barcode + barcode_h - 1.25*cm, line2)

# Barcode Number
barcode_val = "0381/26"
c.setFont("Helvetica-Bold", 7.5)
c.drawCentredString(x_barcode + barcode_w/2, y_barcode + 0.15*cm, barcode_val)

# Barcode Graphic
bw = 1.2
max_width = barcode_w - 0.4*cm
bc = code128.Code128(barcode_val, barHeight=1.2*cm, barWidth=bw)
while bc.width > max_width and bw > 0.2:
    bw -= 0.05
    bc = code128.Code128(barcode_val, barHeight=1.2*cm, barWidth=bw)

bc_x = x_barcode + (barcode_w - bc.width)/2
bc_y = y_barcode + 0.45*cm
bc.drawOn(c, bc_x, bc_y)

c.save()
print("Success")
