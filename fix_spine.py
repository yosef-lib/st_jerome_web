import codecs
import re

with codecs.open('template_stiker.py', 'r', 'utf-8') as f:
    code = f.read()

old_spine_drawing = '''                # --- DRAW SPINE LABEL ---
                x_spine = x_base
                y_spine = y_base + (item_h - spine_h) # Top-aligned
                
                # Draw main border
                c.setStrokeColor(colors.black)
                c.rect(x_spine, y_spine, spine_w, spine_h)
                
                # Draw header background
                header_h = 1.7 * cm
                c.setFillColorRGB(0.85, 0.85, 0.85) # Abu-abu terang
                c.rect(x_spine, y_spine + spine_h - header_h, spine_w, header_h, fill=1, stroke=0)
                
                # Header border line
                c.setStrokeColor(colors.black)
                c.line(x_spine, y_spine + spine_h - header_h, x_spine + spine_w, y_spine + spine_h - header_h)'''

new_spine_drawing = '''                # --- DRAW SPINE LABEL ---
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
                c.line(x_spine, y_spine + spine_h - header_h, x_spine + spine_w, y_spine + spine_h - header_h)'''

code = code.replace(old_spine_drawing, new_spine_drawing)

# Find where Identity sticker is drawn, and reset line width
old_stiker = '''                # --- DRAW EXISTING STICKER ---
                x_stiker = x_base + spine_w + spine_gap
                y_stiker = y_base + (item_h - stiker_h) # Top-aligned with spine
                
                # SET WARNA GARIS KE BIRU
                c.setStrokeColor(colors.blue)'''

new_stiker = '''                # --- DRAW EXISTING STICKER ---
                c.setLineWidth(1.0) # Kembalikan tebal garis ke normal untuk stiker
                
                x_stiker = x_base + spine_w + spine_gap
                y_stiker = y_base + (item_h - stiker_h) # Top-aligned with spine
                
                # SET WARNA GARIS KE BIRU
                c.setStrokeColor(colors.blue)'''

code = code.replace(old_stiker, new_stiker)

with codecs.open('template_stiker.py', 'w', 'utf-8') as f:
    f.write(code)

print("success")
