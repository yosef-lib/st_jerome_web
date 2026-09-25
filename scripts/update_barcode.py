import codecs
import re

with codecs.open('template_stiker.py', 'r', 'utf-8') as f:
    code = f.read()

# Add barcode library
code = code.replace('from reportlab.lib import colors\n', 'from reportlab.lib import colors\nfrom reportlab.graphics.barcode import code128\n')

# Update item_w and specs
old_specs = '''    # Spine label specs from User Image (1.7cm header + 3.3cm body = 5cm total)
    spine_w = 4.5 * cm
    spine_h = 5.0 * cm
    spine_gap = 0.5 * cm
    
    item_w = spine_w + spine_gap + stiker_w
    item_h = max(spine_h, stiker_h)'''
new_specs = '''    # Spine label specs from User Image (1.7cm header + 3.3cm body = 5cm total)
    spine_w = 4.5 * cm
    spine_h = 5.0 * cm
    spine_gap = 0.5 * cm
    
    # Barcode label specs
    barcode_w = 4.0 * cm
    barcode_h = 3.0 * cm
    
    item_w = spine_w + spine_gap + stiker_w + spine_gap + barcode_w
    item_h = max(spine_h, stiker_h)'''
code = code.replace(old_specs, new_specs)

# Add Barcode drawing
old_stiker_end = '''                # Kopi Ke
                c.setFont("Helvetica-Bold", 7)
                c.drawString(x_stiker + col_kiri_w + 0.2*cm, y_stiker + 0.1*cm, buku.get('copy_ke', '1'))'''

new_stiker_end = '''                # Kopi Ke
                c.setFont("Helvetica-Bold", 7)
                c.drawString(x_stiker + col_kiri_w + 0.2*cm, y_stiker + 0.1*cm, buku.get('copy_ke', '1'))
                
                # --- DRAW BARCODE LABEL ---
                x_barcode = x_stiker + stiker_w + spine_gap
                y_barcode = y_base + (item_h - barcode_h) # Top-aligned
                
                # Draw outer border
                c.setStrokeColor(colors.black)
                c.setLineWidth(1.0)
                c.rect(x_barcode, y_barcode, barcode_w, barcode_h)
                
                # Header "PERPUSTAKAAN IMAVI"
                c.setFillColor(colors.black)
                c.setFont("Helvetica-Bold", 7)
                c.drawCentredString(x_barcode + barcode_w/2, y_barcode + barcode_h - 0.4*cm, "PERPUSTAKAAN IMAVI")
                
                # Title (Truncated to 50 chars max)
                full_title = buku.get('judul', '')
                if len(full_title) > 50:
                    trunc_title = full_title[:47] + "..."
                else:
                    trunc_title = full_title
                c.setFont("Helvetica", 6.5)
                c.drawCentredString(x_barcode + barcode_w/2, y_barcode + barcode_h - 0.8*cm, trunc_title)
                
                # Barcode Number
                barcode_val = buku.get('no_induk', '')
                c.setFont("Helvetica-Bold", 7.5)
                c.drawCentredString(x_barcode + barcode_w/2, y_barcode + 0.2*cm, barcode_val)
                
                # Barcode Graphic
                if barcode_val:
                    bw = 1.2
                    max_width = barcode_w - 0.4*cm
                    bc = code128.Code128(barcode_val, barHeight=1.1*cm, barWidth=bw)
                    while bc.width > max_width and bw > 0.2:
                        bw -= 0.05
                        bc = code128.Code128(barcode_val, barHeight=1.1*cm, barWidth=bw)
                    
                    bc_x = x_barcode + (barcode_w - bc.width)/2
                    bc_y = y_barcode + 0.6*cm
                    bc.drawOn(c, bc_x, bc_y)'''

code = code.replace(old_stiker_end, new_stiker_end)

with codecs.open('template_stiker.py', 'w', 'utf-8') as f:
    f.write(code)

print("success barcode addition")
