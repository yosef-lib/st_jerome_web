from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.graphics.barcode import code128

c = canvas.Canvas('test_barcode.pdf')
barcode_val = "BK-2026-001"
max_width = 3.8 * cm

bw = 1.2
bc = code128.Code128(barcode_val, barHeight=1.0*cm, barWidth=bw)
while bc.width > max_width and bw > 0.2:
    bw -= 0.05
    bc = code128.Code128(barcode_val, barHeight=1.0*cm, barWidth=bw)

print(f"Final barWidth: {bw}, Width: {bc.width/cm} cm")
